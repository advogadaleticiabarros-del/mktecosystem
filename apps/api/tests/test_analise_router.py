from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from app.core.security import create_access_token, hash_password
from app.models.instagram_post import InstagramPost
from app.models.social_metric import SocialMetric
from app.models.tenant import Tenant
from app.models.user import User


async def _usuario(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    user = User(tenant_id=tenant.id, email="l@x.com", hashed_password=hash_password("x"), nome="Letícia", role="owner")
    db.add(user)
    await db.commit()
    return tenant, {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.mark.anyio
async def test_analise_devolve_secoes_com_explicacao(client, db_session):
    tenant, headers = await _usuario(db_session)
    db_session.add(InstagramPost(
        tenant_id=tenant.id, media_id="m1", publicado_em=datetime(2026, 5, 28, 23, tzinfo=timezone.utc),
        formato="Reels", area="Trabalhista", alcance=900, interacoes=50,
    ))
    db_session.add(SocialMetric(tenant_id=tenant.id, tipo="ig_raio_x", metricas={"perfil": {"followers_count": 416}}))
    await db_session.commit()

    resp = await client.get("/analise/instagram", headers=headers)

    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["total_posts"] == 1
    assert corpo["formatos"]["itens"][0]["formato"] == "Reels"
    assert corpo["atualizado_em"]
    assert corpo["resumo"]["kpis"][0]["valor"] == 416


@pytest.mark.anyio
async def test_atualizar_roda_a_coleta_e_devolve_a_analise_nova(client, db_session):
    tenant, headers = await _usuario(db_session)

    async def coleta_falsa(db, tenant_id=None, **_):
        db.add(SocialMetric(tenant_id=tenant.id, tipo="ig_raio_x", metricas={"perfil": {"followers_count": 500}}))
        await db.commit()
        return 1

    with patch("app.routers.analise.coletar_instagram", new=coleta_falsa):
        resp = await client.post("/analise/instagram/atualizar", headers=headers)

    assert resp.status_code == 200
    assert resp.json()["resumo"]["kpis"][0]["valor"] == 500


@pytest.mark.anyio
async def test_exige_login(client):
    assert (await client.get("/analise/instagram")).status_code == 401
