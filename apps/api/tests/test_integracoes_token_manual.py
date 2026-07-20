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
async def test_conectar_com_token_manual_cria_conexao(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    mock_meta = AsyncMock()
    mock_meta.buscar_paginas.return_value = [
        {"id": "111", "name": "Advogada Letícia Barros", "access_token": "page_token_do_system_user"}
    ]
    mock_meta.buscar_conta_instagram.return_value = {"id": "999"}
    mock_meta.buscar_nome_conta_instagram.return_value = "adv.leticiabarros2"

    with patch("app.routers.integracoes.get_meta_client", return_value=mock_meta):
        resp = await client.post(
            "/integracoes/instagram/token",
            json={"access_token": "EAA_token_do_system_user"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["nome_conta"] == "adv.leticiabarros2"
    assert body["status"] == "ativo"

    conexao = (await db_session.execute(select(SocialConnection))).scalar_one()
    assert conexao.ig_user_id == "999"
    assert conexao.expira_em is None


@pytest.mark.anyio
async def test_conectar_com_token_manual_sem_pagina_retorna_422(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    mock_meta = AsyncMock()
    mock_meta.buscar_paginas.return_value = []

    with patch("app.routers.integracoes.get_meta_client", return_value=mock_meta):
        resp = await client.post(
            "/integracoes/instagram/token",
            json={"access_token": "token_sem_pagina"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 422
