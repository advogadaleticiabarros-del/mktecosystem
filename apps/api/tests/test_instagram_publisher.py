from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.core.security import hash_password
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User
from app.services.instagram_publisher import publicar_agendamentos_prontos


async def _setup(db, com_conexao=True):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}, identidade_visual={"cores": {}}))
    if com_conexao:
        db.add(
            SocialConnection(
                tenant_id=tenant.id,
                plataforma="instagram",
                page_id="111",
                ig_user_id="999",
                nome_conta="adv.leticiabarros2",
                access_token_encrypted=encrypt_token("token-falso"),
                status="ativo",
            )
        )
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Tema", angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True,
    )
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="carrossel",
        corpo={"slides": ["a", "b", "c"]}, status="aprovado",
    )
    db.add(piece)
    await db.flush()
    agendamento = ScheduledPost(
        tenant_id=tenant.id, content_piece_id=piece.id, titulo="Tema",
        canal="instagram", formato="carrossel",
        data_agendada=date.today() - timedelta(days=1), horario="11:00", status="pronto",
    )
    db.add(agendamento)
    await db.commit()
    return tenant, agendamento


@pytest.mark.anyio
async def test_publica_agendamento_pronto(db_session):
    tenant, agendamento = await _setup(db_session)

    with patch("app.services.instagram_publisher.renderizar_slide", new=AsyncMock()), patch(
        "app.services.instagram_publisher.InstagramAPI"
    ) as MockAPI:
        instancia = MockAPI.return_value
        instancia.publicar_carrossel = AsyncMock(return_value="post_123")
        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 1
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"
    assert agendamento.platform_post_id == "post_123"


@pytest.mark.anyio
async def test_sem_conexao_pula_silenciosamente(db_session):
    tenant, agendamento = await _setup(db_session, com_conexao=False)
    publicados = await publicar_agendamentos_prontos(db_session)
    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "pronto"


@pytest.mark.anyio
async def test_falha_incrementa_tentativas_e_marca_erro_apos_3(db_session):
    tenant, agendamento = await _setup(db_session)
    agendamento.tentativas = 2
    await db_session.commit()

    with patch("app.services.instagram_publisher.renderizar_slide", new=AsyncMock()), patch(
        "app.services.instagram_publisher.InstagramAPI"
    ) as MockAPI:
        instancia = MockAPI.return_value
        instancia.publicar_carrossel = AsyncMock(side_effect=Exception("erro da API"))
        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "erro"
    assert agendamento.tentativas == 3
