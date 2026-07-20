from unittest.mock import AsyncMock, patch

import pytest

from app.core.security import create_access_token, hash_password
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User
from app.services.insights import _coletar_dados


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}))
    user = User(
        tenant_id=tenant.id,
        email="l@example.com",
        nome="L",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    db.add(user)
    await db.commit()
    return tenant, user


@pytest.mark.anyio
async def test_coletar_dados_resume_o_banco(db_session):
    tenant, _ = await _setup(db_session)
    dados = await _coletar_dados(db_session, tenant.id)
    assert "Pautas pesquisadas: 0" in dados
    assert "Contatos ativos: 0" in dados


@pytest.mark.anyio
async def test_insights_endpoint_retorna_dicas(client, db_session):
    tenant, user = await _setup(db_session)
    token = create_access_token(user.id)

    mock_ai = AsyncMock()
    mock_ai.generate_json.return_value = {
        "dicas": [
            {
                "titulo": "Ative a captura de contatos",
                "diagnostico": "Nenhum contato ativo na base.",
                "acao": "Publique a landing page com o formulário.",
            },
            {"diagnostico": "sem título, deve ser filtrada", "acao": "x"},
        ]
    }
    with patch("app.routers.dashboard.get_ai_client", return_value=mock_ai):
        resp = await client.post(
            "/dashboard/insights", headers={"Authorization": f"Bearer {token}"}
        )
    assert resp.status_code == 200
    dicas = resp.json()["dicas"]
    assert len(dicas) == 1
    assert dicas[0]["titulo"] == "Ative a captura de contatos"
