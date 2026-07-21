from datetime import date, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant, TenantConfig
from app.services.blog_publisher import publicar_agendamentos_prontos

INDEX_FIXTURE = (
    '<div class="blog-grid" id="blogGridRecent"></div>'
    '<div class="blog-grid" id="blogGrid"></div>'
)
SITEMAP_FIXTURE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n'
)


async def _setup(db, status_piece="aprovado"):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}, identidade_visual={"cores": {}}))
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Carga horária máxima CLT", angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True,
    )
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="artigo",
        corpo={
            "titulo": "Carga horária máxima CLT",
            "html": "<p>Conteúdo do artigo</p>",
            "meta_description": "Descrição SEO",
            "resumo": "Resumo curto",
        },
        status=status_piece,
    )
    db.add(piece)
    await db.flush()
    agendamento = ScheduledPost(
        tenant_id=tenant.id, content_piece_id=piece.id, titulo="Carga horária máxima CLT",
        canal="blog", formato="artigo",
        data_agendada=date.today() - timedelta(days=1), horario="11:00", status="pronto",
    )
    db.add(agendamento)
    await db.commit()
    return tenant, agendamento


async def _fake_renderizar_capa_artigo(*, titulo, categoria, identidade_visual, caminho_saida):
    # A implementação real (Playwright) grava o PNG em caminho_saida; o mock
    # precisa replicar isso, já que blog_publisher lê os bytes de volta do disco.
    Path(caminho_saida).write_bytes(b"fake-png-bytes")


@pytest.mark.anyio
async def test_publica_agendamento_pronto(db_session):
    tenant, agendamento = await _setup(db_session)

    with patch(
        "app.services.blog_publisher.renderizar_capa_artigo",
        new=AsyncMock(side_effect=_fake_renderizar_capa_artigo),
    ), patch(
        "app.services.blog_publisher.SFTPClient"
    ) as MockSFTP:
        instancia = MockSFTP.return_value
        instancia.download = AsyncMock(side_effect=[INDEX_FIXTURE.encode(), SITEMAP_FIXTURE.encode()])
        instancia.upload = AsyncMock()
        instancia.garantir_diretorio = AsyncMock()
        instancia.close = AsyncMock()

        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 1
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"
    assert agendamento.platform_post_id == "https://advogadaleticiabarros.com.br/blog/carga-horaria-maxima-clt.html"
    # 4 uploads: HTML do artigo, capa, index.html, sitemap.xml
    assert instancia.upload.await_count == 4
    instancia.garantir_diretorio.assert_awaited_once_with("capas")
    instancia.close.assert_awaited_once()


@pytest.mark.anyio
async def test_content_piece_nao_aprovado_nao_publica(db_session):
    tenant, agendamento = await _setup(db_session, status_piece="rascunho")

    with patch("app.services.blog_publisher.renderizar_capa_artigo", new=AsyncMock()), patch(
        "app.services.blog_publisher.SFTPClient"
    ) as MockSFTP:
        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 0
    MockSFTP.assert_not_called()
    await db_session.refresh(agendamento)
    assert agendamento.status == "pronto"


@pytest.mark.anyio
async def test_falha_incrementa_tentativas_e_marca_erro_apos_3(db_session):
    tenant, agendamento = await _setup(db_session)
    agendamento.tentativas = 2
    await db_session.commit()

    with patch("app.services.blog_publisher.renderizar_capa_artigo", new=AsyncMock()), patch(
        "app.services.blog_publisher.SFTPClient"
    ) as MockSFTP:
        instancia = MockSFTP.return_value
        instancia.download = AsyncMock(side_effect=Exception("falha de conexão"))
        instancia.upload = AsyncMock()
        instancia.close = AsyncMock()

        publicados = await publicar_agendamentos_prontos(db_session)

    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "erro"
    assert agendamento.tentativas == 3
