import pytest

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant
from app.services.agenda import agendar_conteudo_aprovado


@pytest.mark.anyio
async def test_jornal_aprovado_agenda_como_newsletter_no_canal_blog(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Radar Jurídico — NR-1", angulo="direitos",
        area="Trabalhista", origem="radar_juridico_manchete", fonte="chatgpt-radar",
        relevante_para_conteudo=True, status="sugerida",
    )
    db_session.add(pauta)
    await db_session.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="jornal",
        corpo={"titulo": "Radar Jurídico — NR-1", "html": "<p>edição</p>"},
        status="aprovado", versao=1,
    )
    db_session.add(piece)
    await db_session.flush()

    agendamento = await agendar_conteudo_aprovado(db_session, piece)

    assert agendamento is not None
    assert agendamento.canal == "blog"
    assert agendamento.formato == "newsletter"


@pytest.mark.anyio
async def test_reels_aprovado_agenda_no_instagram_formato_reels(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Direitos da gestante", angulo="direitos",
        area="Trabalhista", origem="manual", fonte="manual",
        relevante_para_conteudo=True, status="sugerida",
    )
    db_session.add(pauta)
    await db_session.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="reels",
        corpo={"gancho": "gancho", "roteiro": []}, status="aprovado", versao=1,
    )
    db_session.add(piece)
    await db_session.flush()

    agendamento = await agendar_conteudo_aprovado(db_session, piece)

    assert agendamento is not None
    assert agendamento.canal == "instagram"
    assert agendamento.formato == "reels"


@pytest.mark.anyio
async def test_estatico_aprovado_agenda_no_instagram_formato_post(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Direitos da gestante", angulo="direitos",
        area="Trabalhista", origem="manual", fonte="manual",
        relevante_para_conteudo=True, status="sugerida",
    )
    db_session.add(pauta)
    await db_session.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="estatico",
        corpo={"conceito_visual": "x"}, status="aprovado", versao=1,
    )
    db_session.add(piece)
    await db_session.flush()

    agendamento = await agendar_conteudo_aprovado(db_session, piece)

    assert agendamento is not None
    assert agendamento.canal == "instagram"
    assert agendamento.formato == "post"


@pytest.mark.anyio
async def test_aprovado_com_programacao_agenda_na_data_e_hora_combinadas(db_session):
    """Peça produzida com data marcada (corpo.programacao) sai exatamente nessa data/hora,
    não na próxima vaga do ciclo (aprovação pelo Editorial, 09/10/2026)."""
    from datetime import date

    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Pensão de R$ 300", angulo="humor", area="Família",
        origem="manual", fonte="manual", relevante_para_conteudo=True, status="em_producao",
    )
    db_session.add(pauta)
    await db_session.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="carrossel",
        corpo={"imagens": ["a.jpg"], "programacao": {"data": "2026-10-10", "hora": "15:00"}},
        status="aprovado", versao=1,
    )
    db_session.add(piece)
    await db_session.flush()

    agendamento = await agendar_conteudo_aprovado(db_session, piece)

    assert agendamento.data_agendada == date(2026, 10, 10)
    assert agendamento.horario == "15:00"
    assert agendamento.formato == "carrossel"
    assert agendamento.titulo == "Pensão de R$ 300"
