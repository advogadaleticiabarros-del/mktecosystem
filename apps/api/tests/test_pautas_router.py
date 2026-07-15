from unittest.mock import AsyncMock, patch

import pytest

from app.integrations.sources.base import SourceDocument
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User
from app.core.security import hash_password, create_access_token


async def _make_tenant_and_user(db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"areas": ["Trabalhista", "Previdenciário"]},
            identidade_visual={},
            ctas={},
            regras_compliance={},
            canais={},
        )
    )
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
async def test_buscar_pautas_persists_ranked_results(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    fake_ai_result = {
        "pautas": [
            {
                "titulo": "Revisão de benefício por incapacidade",
                "angulo": "direitos",
                "area": "Previdenciário",
                "fonte": "STF",
                "relevante_para_conteudo": True,
            },
            {
                "titulo": "Alteração de rito em recurso especial",
                "angulo": "tecnico",
                "area": "Processual",
                "fonte": "STF",
                "relevante_para_conteudo": False,
            },
        ]
    }

    with (
        patch("app.routers.pautas.fetch_stf", new=AsyncMock(return_value=SourceDocument("STF", "url", "texto stf"))),
        patch("app.routers.pautas.fetch_tst", new=AsyncMock(return_value=SourceDocument("TST", "url", "texto tst"))),
        patch("app.routers.pautas.fetch_cnj", new=AsyncMock(return_value=SourceDocument("CNJ", "url", "texto cnj"))),
        patch("app.routers.pautas.get_ai_client") as mock_get_ai,
    ):
        mock_ai = AsyncMock()
        mock_ai.generate_json.return_value = fake_ai_result
        mock_get_ai.return_value = mock_ai

        response = await client.post(
            "/pautas/buscar", headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert any(p["relevante_para_conteudo"] is True for p in body)
    assert any(p["relevante_para_conteudo"] is False for p in body)


@pytest.mark.anyio
async def test_list_pautas_filters_by_relevante_para_conteudo(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    from app.models.pauta import Pauta

    db_session.add_all(
        [
            Pauta(
                tenant_id=tenant.id, titulo="Pauta de conteúdo", angulo="direitos",
                area="Trabalhista", origem="buscada", fonte="CNJ",
                relevante_para_conteudo=True, status="sugerida",
            ),
            Pauta(
                tenant_id=tenant.id, titulo="Pauta só informativa", angulo="tecnico",
                area="Processual", origem="buscada", fonte="CNJ",
                relevante_para_conteudo=False, status="sugerida",
            ),
        ]
    )
    await db_session.commit()

    response = await client.get(
        "/pautas", params={"relevante_para_conteudo": "true"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["titulo"] == "Pauta de conteúdo"


@pytest.mark.anyio
async def test_create_manual_pauta(client, db_session):
    tenant, user = await _make_tenant_and_user(db_session)
    token = create_access_token(user.id)

    response = await client.post(
        "/pautas",
        json={
            "titulo": "BPC/LOAS negado por erro no CadÚnico",
            "angulo": "direitos",
            "area": "Previdenciário",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["origem"] == "manual"
    assert body["relevante_para_conteudo"] is True
