from unittest.mock import AsyncMock, patch

import pytest

from app.core.security import create_access_token, hash_password
from app.models.pauta import Pauta
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User


@pytest.mark.anyio
async def test_gerar_creates_four_content_pieces(client, db_session):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    db_session.add(
        TenantConfig(
            tenant_id=tenant.id,
            voz={"principios": ["Sem juridiquês"], "oab": "OAB/ES 39.948"},
            identidade_visual={}, ctas={}, regras_compliance={}, canais={},
        )
    )
    user = User(
        tenant_id=tenant.id, email="l@example.com", nome="L",
        hashed_password=hash_password("senha"), role="owner",
    )
    db_session.add(user)
    pauta = Pauta(
        tenant_id=tenant.id, titulo="BPC/LOAS em 2026", angulo="direitos",
        area="Previdenciário", origem="manual", fonte="manual",
        relevante_para_conteudo=True, status="sugerida",
    )
    db_session.add(pauta)
    await db_session.commit()

    token = create_access_token(user.id)

    fake_results = {
        "artigo": {"titulo": "BPC/LOAS em 2026", "html": "<p>artigo</p>"},
        "carrossel": {"slides": ["s1", "s2", "s3", "s4", "s5"]},
        "legenda": {"texto": "legenda aqui"},
        "stories": {"roteiro": ["frame 1", "frame 2", "frame 3"]},
    }

    with patch("app.routers.content.get_ai_client") as mock_get_ai:
        mock_ai = AsyncMock()
        mock_ai.generate_json.side_effect = [
            fake_results["artigo"],
            fake_results["carrossel"],
            fake_results["legenda"],
            fake_results["stories"],
        ]
        mock_get_ai.return_value = mock_ai

        response = await client.post(
            "/content/gerar",
            json={"pauta_id": str(pauta.id)},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    body = response.json()
    tipos = {piece["tipo"] for piece in body}
    assert tipos == {"artigo", "carrossel", "legenda", "stories"}
    assert all(piece["status"] == "rascunho" for piece in body)
