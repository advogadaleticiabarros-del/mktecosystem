import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.tenant import Tenant
from app.models.user import User


async def _setup(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    user = User(
        tenant_id=tenant.id, email="l@example.com", nome="L",
        hashed_password=hash_password("senha"), role="owner",
    )
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Tema X", angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True, status="sugerida",
    )
    db_session.add_all([user, pauta])
    await db_session.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo="artigo",
        corpo={"titulo": "rascunho"}, status="rascunho", versao=1,
    )
    db_session.add(piece)
    await db_session.commit()
    return tenant, user, pauta, piece


@pytest.mark.anyio
async def test_approving_a_piece_writes_marketing_memory(client, db_session):
    tenant, user, pauta, piece = await _setup(db_session)
    token = create_access_token(user.id)

    response = await client.patch(
        f"/content/{piece.id}",
        json={"status": "aprovado", "corpo": {"titulo": "final"}},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "aprovado"
    assert response.json()["corpo"]["titulo"] == "final"

    result = await db_session.execute(
        select(MarketingMemory).where(MarketingMemory.content_piece_id == piece.id)
    )
    memory = result.scalar_one()
    assert memory.tema == "Tema X"
    assert memory.formato == "artigo"
    assert memory.metricas == {}
    assert memory.aprendizado is None


@pytest.mark.anyio
async def test_rejecting_a_piece_does_not_write_marketing_memory(client, db_session):
    tenant, user, pauta, piece = await _setup(db_session)
    token = create_access_token(user.id)

    response = await client.patch(
        f"/content/{piece.id}",
        json={"status": "rejeitado"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    result = await db_session.execute(
        select(MarketingMemory).where(MarketingMemory.content_piece_id == piece.id)
    )
    assert result.scalar_one_or_none() is None
