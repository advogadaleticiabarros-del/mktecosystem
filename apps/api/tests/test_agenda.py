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
