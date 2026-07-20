from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.models.tenant import Tenant
from app.services.instagram_metrics import coletar_metricas_diarias


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(
        SocialConnection(
            tenant_id=tenant.id, plataforma="instagram", page_id="111", ig_user_id="999",
            nome_conta="adv.leticiabarros2", access_token_encrypted=encrypt_token("token"), status="ativo",
        )
    )
    await db.commit()
    return tenant


@pytest.mark.anyio
async def test_coleta_metricas_grava_social_metric(db_session):
    tenant = await _setup(db_session)

    with patch("app.services.instagram_metrics.InstagramAPI") as MockAPI:
        instancia = MockAPI.return_value
        instancia.buscar_metricas_conta = AsyncMock(
            return_value={"seguidores": 1200, "alcance_7d": 3400}
        )
        coletados = await coletar_metricas_diarias(db_session)

    assert coletados == 1
    metrica = (await db_session.execute(select(SocialMetric))).scalar_one()
    assert metrica.tipo == "conta"
    assert metrica.metricas["seguidores"] == 1200


@pytest.mark.anyio
async def test_falha_na_coleta_nao_interrompe_outros_tenants(db_session):
    tenant1 = await _setup(db_session)

    with patch("app.services.instagram_metrics.InstagramAPI") as MockAPI:
        instancia = MockAPI.return_value
        instancia.buscar_metricas_conta = AsyncMock(side_effect=Exception("erro da API"))
        coletados = await coletar_metricas_diarias(db_session)

    assert coletados == 0
    assert (await db_session.execute(select(SocialMetric))).scalar_one_or_none() is None
