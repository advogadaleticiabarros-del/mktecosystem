import pytest
from sqlalchemy import select

from app.models.tenant import Tenant, TenantConfig


@pytest.mark.anyio
async def test_tenant_and_config_persist_with_json_fields(db_session):
    tenant = Tenant(nome="Advogada Letícia Barros", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()

    config = TenantConfig(
        tenant_id=tenant.id,
        voz={"oab": "OAB/ES 39.948"},
        identidade_visual={"cores": {"dourado": "#C9A962"}},
        ctas={"whatsapp": "5527995151402"},
        regras_compliance={"oab": True},
        canais={"blog": True},
    )
    db_session.add(config)
    await db_session.commit()

    result = await db_session.execute(select(TenantConfig).where(TenantConfig.tenant_id == tenant.id))
    saved = result.scalar_one()
    assert saved.voz["oab"] == "OAB/ES 39.948"
    assert saved.identidade_visual["cores"]["dourado"] == "#C9A962"
