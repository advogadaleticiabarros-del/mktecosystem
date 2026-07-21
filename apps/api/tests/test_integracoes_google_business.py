from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User


async def _make_tenant_and_user(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(TenantConfig(tenant_id=tenant.id, voz={}))
    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()
    return tenant, user


@pytest.mark.anyio
async def test_callback_google_business_cria_conexao(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    state = create_access_token(user.id)

    mock_client = AsyncMock()
    mock_client.trocar_code_por_tokens.return_value = {
        "access_token": "access_curto",
        "refresh_token": "refresh_longo",
        "expires_in": 3599,
    }
    mock_client.listar_contas.return_value = [{"name": "accounts/123", "accountName": "Letícia Barros"}]
    mock_client.listar_locais.return_value = [
        {"name": "locations/456", "title": "Escritório Letícia Barros"}
    ]

    with patch("app.routers.integracoes.get_google_client", return_value=mock_client):
        resp = await client.get(
            f"/integracoes/google-business/callback?code=abc&state={state}",
            follow_redirects=False,
        )

    assert resp.status_code == 307
    assert "conectado=google_business" in resp.headers["location"]

    conexao = (
        await db_session.execute(
            select(SocialConnection).where(SocialConnection.plataforma == "google_business")
        )
    ).scalar_one()
    assert conexao.page_id == "accounts/123"
    assert conexao.ig_user_id == "locations/456"
    assert conexao.nome_conta == "Escritório Letícia Barros"
    assert conexao.status == "ativo"


@pytest.mark.anyio
async def test_desconectar_google_business(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)
    db_session.add(
        SocialConnection(
            tenant_id=tenant.id,
            plataforma="google_business",
            page_id="accounts/123",
            ig_user_id="locations/456",
            nome_conta="Escritório",
            access_token_encrypted="x",
            status="ativo",
        )
    )
    await db_session.commit()

    resp = await client.delete(
        "/integracoes/google-business", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 204

    conexao = (
        await db_session.execute(
            select(SocialConnection).where(SocialConnection.plataforma == "google_business")
        )
    ).scalar_one()
    assert conexao.status == "desconectado"
