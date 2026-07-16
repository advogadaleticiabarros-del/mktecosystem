import pytest
from sqlalchemy import select

from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.tenant import Tenant


@pytest.mark.anyio
async def test_pauta_content_piece_and_memory_chain(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()

    pauta = Pauta(
        tenant_id=tenant.id,
        titulo="Revisão de benefício por incapacidade",
        angulo="direitos",
        area="Previdenciário",
        origem="buscada",
        fonte="STF - Informativo 1150",
        relevante_para_conteudo=True,
        status="sugerida",
    )
    db_session.add(pauta)
    await db_session.flush()

    piece = ContentPiece(
        tenant_id=tenant.id,
        pauta_id=pauta.id,
        tipo="artigo",
        corpo={"titulo": "Revisão de benefício", "html": "<p>...</p>"},
        status="rascunho",
        versao=1,
    )
    db_session.add(piece)
    await db_session.flush()

    memory = MarketingMemory(
        tenant_id=tenant.id,
        content_piece_id=piece.id,
        tema=pauta.titulo,
        angulo=pauta.angulo,
        formato="artigo",
        metricas={},
        aprendizado=None,
    )
    db_session.add(memory)
    await db_session.commit()

    result = await db_session.execute(select(MarketingMemory).where(MarketingMemory.content_piece_id == piece.id))
    saved = result.scalar_one()
    assert saved.tema == "Revisão de benefício por incapacidade"
    assert saved.metricas == {}
    assert saved.aprendizado is None
