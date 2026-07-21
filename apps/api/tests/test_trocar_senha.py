import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password, verify_password
from app.models.tenant import Tenant
from app.models.user import User


async def _make_tenant_and_user(db_session, senha="senha-atual-123"):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia",
        hashed_password=hash_password(senha),
        role="owner",
    )
    db_session.add(user)
    await db_session.commit()
    return tenant, user


@pytest.mark.anyio
async def test_trocar_senha_com_sucesso(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    user_id = user.id
    token = create_access_token(user_id)

    resp = await client.post(
        "/auth/trocar-senha",
        json={"senha_atual": "senha-atual-123", "senha_nova": "nova-senha-segura-456"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200

    db_session.expire_all()
    result = await db_session.execute(select(User).where(User.id == user_id))
    atualizado = result.scalar_one()
    assert verify_password("nova-senha-segura-456", atualizado.hashed_password)


@pytest.mark.anyio
async def test_trocar_senha_atual_errada_401(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    resp = await client.post(
        "/auth/trocar-senha",
        json={"senha_atual": "senha-errada", "senha_nova": "nova-senha-segura-456"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401

    result = await db_session.execute(select(User).where(User.id == user.id))
    inalterado = result.scalar_one()
    assert verify_password("senha-atual-123", inalterado.hashed_password)


@pytest.mark.anyio
async def test_trocar_senha_nova_curta_422(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    resp = await client.post(
        "/auth/trocar-senha",
        json={"senha_atual": "senha-atual-123", "senha_nova": "curta"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_login_funciona_com_a_senha_nova_apos_troca(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    await client.post(
        "/auth/trocar-senha",
        json={"senha_atual": "senha-atual-123", "senha_nova": "nova-senha-segura-456"},
        headers={"Authorization": f"Bearer {token}"},
    )

    resp = await client.post(
        "/auth/login",
        json={"email": "leticia@example.com", "password": "nova-senha-segura-456"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
