from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.email_campaign import EmailCampaign
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User

FAKE_WELCOME = {
    "emails": [
        {"assunto": f"Assunto {i}", "corpo_html": f"<p>Corpo {i}</p>", "corpo_texto": f"Corpo {i}"}
        for i in (1, 2, 3)
    ]
}


async def _make_tenant_and_user(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(TenantConfig(tenant_id=tenant.id, voz={"oab": "OAB/ES 39.948"}))
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
async def test_gerar_boas_vindas_cria_3_rascunhos(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    mock_ai = AsyncMock()
    mock_ai.generate_json.return_value = FAKE_WELCOME
    with patch("app.routers.email.get_ai_client", return_value=mock_ai):
        resp = await client.post(
            "/email/campaigns/gerar-boas-vindas",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert [c["tipo"] for c in body] == ["boas_vindas_1", "boas_vindas_2", "boas_vindas_3"]
    assert all(c["status"] == "rascunho" for c in body)


@pytest.mark.anyio
async def test_regerar_arquiva_rascunhos_antigos(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    mock_ai = AsyncMock()
    mock_ai.generate_json.return_value = FAKE_WELCOME
    with patch("app.routers.email.get_ai_client", return_value=mock_ai):
        headers = {"Authorization": f"Bearer {token}"}
        await client.post("/email/campaigns/gerar-boas-vindas", headers=headers)
        await client.post("/email/campaigns/gerar-boas-vindas", headers=headers)

    result = await db_session.execute(select(EmailCampaign))
    todas = result.scalars().all()
    assert len(todas) == 6
    assert sum(1 for c in todas if c.status == "rascunho") == 3
    assert sum(1 for c in todas if c.status == "arquivado") == 3


@pytest.mark.anyio
async def test_aprovar_campanha_grava_aprovado_em(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)
    campanha = EmailCampaign(
        tenant_id=tenant.id, tipo="boas_vindas_1", assunto="Oi", corpo_html="<p>x</p>"
    )
    db_session.add(campanha)
    await db_session.commit()

    resp = await client.patch(
        f"/email/campaigns/{campanha.id}",
        json={"status": "aprovado"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "aprovado"
    assert resp.json()["aprovado_em"] is not None


@pytest.mark.anyio
async def test_status_enviado_nao_e_setavel_via_api(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)
    campanha = EmailCampaign(
        tenant_id=tenant.id, tipo="newsletter", assunto="Oi", corpo_html="<p>x</p>"
    )
    db_session.add(campanha)
    await db_session.commit()

    resp = await client.patch(
        f"/email/campaigns/{campanha.id}",
        json={"status": "enviado"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422
