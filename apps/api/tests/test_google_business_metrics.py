from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.models.tenant import Tenant
from app.services.google_business_metrics import coletar_metricas_google_business


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(
        SocialConnection(
            tenant_id=tenant.id,
            plataforma="google_business",
            page_id="accounts/123",
            ig_user_id="locations/456",
            nome_conta="Escritório",
            access_token_encrypted=encrypt_token("refresh_token_falso"),
            status="ativo",
        )
    )
    await db.commit()
    return tenant


@pytest.mark.anyio
async def test_coleta_metricas_google_business(db_session):
    tenant = await _setup(db_session)

    with patch("app.services.google_business_metrics.GoogleBusinessClient") as MockClient:
        instancia = MockClient.return_value
        instancia.renovar_access_token = AsyncMock(return_value="access_novo")
        instancia.buscar_metricas = AsyncMock(
            return_value={"buscas": 40, "chamadas": 8, "pedidos_rota": 2, "visualizacoes": 100}
        )
        coletados = await coletar_metricas_google_business(db_session)

    assert coletados == 1
    metrica = (await db_session.execute(select(SocialMetric))).scalar_one()
    assert metrica.tipo == "google_business"
    assert metrica.metricas["chamadas"] == 8


@pytest.mark.anyio
async def test_falha_na_coleta_nao_interrompe(db_session):
    await _setup(db_session)

    with patch("app.services.google_business_metrics.GoogleBusinessClient") as MockClient:
        instancia = MockClient.return_value
        instancia.renovar_access_token = AsyncMock(side_effect=Exception("token revogado"))
        coletados = await coletar_metricas_google_business(db_session)

    assert coletados == 0
