import pytest

from app.core.security import hash_password
from app.models.tenant import Tenant
from app.models.user import User


@pytest.mark.anyio
async def test_login_returns_token_for_valid_credentials(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()

    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia Barros",
        hashed_password=hash_password("senha-forte-123"),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"email": "leticia@example.com", "password": "senha-forte-123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_rejects_wrong_password(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()

    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia Barros",
        hashed_password=hash_password("senha-forte-123"),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/auth/login",
        json={"email": "leticia@example.com", "password": "errada"},
    )
    assert response.status_code == 401


@pytest.mark.skip(reason="pautas router added in Task 10")
@pytest.mark.anyio
async def test_protected_route_rejects_missing_token(client):
    response = await client.get("/pautas")
    assert response.status_code == 401
