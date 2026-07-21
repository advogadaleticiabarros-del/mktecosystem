from unittest.mock import AsyncMock, patch

import pytest

from app.core.crypto import encrypt_token
from app.core.security import create_access_token, hash_password
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}))
    db.add(
        SocialConnection(
            tenant_id=tenant.id,
            plataforma="google_business",
            page_id="accounts/123",
            ig_user_id="locations/456",
            nome_conta="Escritório",
            access_token_encrypted=encrypt_token("refresh_falso"),
            status="ativo",
        )
    )
    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db.add(user)
    await db.commit()
    return tenant, user


@pytest.mark.anyio
async def test_listar_avaliacoes(client, db_session):
    tenant, user = await _setup(db_session)
    token = create_access_token(user.id)

    mock_client = AsyncMock()
    mock_client.renovar_access_token.return_value = "access_novo"
    mock_client.listar_avaliacoes.return_value = [
        {
            "name": "locations/456/reviews/789",
            "reviewer": {"displayName": "Maria S."},
            "starRating": "FIVE",
            "comment": "Excelente",
        }
    ]

    with patch("app.routers.avaliacoes.get_google_client", return_value=mock_client):
        resp = await client.get("/avaliacoes", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.json()[0]["reviewer"]["displayName"] == "Maria S."


@pytest.mark.anyio
async def test_responder_avaliacao(client, db_session):
    tenant, user = await _setup(db_session)
    token = create_access_token(user.id)

    mock_client = AsyncMock()
    mock_client.renovar_access_token.return_value = "access_novo"

    with patch("app.routers.avaliacoes.get_google_client", return_value=mock_client):
        resp = await client.post(
            "/avaliacoes/locations%2F456%2Freviews%2F789/responder",
            json={"texto": "Obrigada pela confiança!"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    mock_client.responder_avaliacao.assert_awaited_once()


@pytest.mark.anyio
async def test_listar_avaliacoes_sem_conexao_retorna_422(client, db_session):
    tenant = Tenant(nome="Outra", slug="outra", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(TenantConfig(tenant_id=tenant.id, voz={}))
    user = User(
        tenant_id=tenant.id,
        email="outra@example.com",
        nome="Outra",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()
    token = create_access_token(user.id)

    resp = await client.get("/avaliacoes", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 422
