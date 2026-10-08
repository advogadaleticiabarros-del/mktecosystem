import pytest
from sqlalchemy import select

from app.core.crypto import encrypt_token
from app.models.instagram_post import InstagramPost
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.models.tenant import Tenant
from app.services.coleta_instagram import coletar_instagram


class ApiFalsa:
    def __init__(self, alcance=900):
        self.alcance = alcance

    async def listar_publicacoes(self, ig_user_id):
        return [
            {"id": "m1", "media_type": "VIDEO", "media_product_type": "REELS", "timestamp": "2026-05-28T23:00:00+0000",
             "caption": "Fez a grávida chorar? Processamos", "permalink": "https://ig/m1",
             "insights": {"reach": self.alcance, "views": 1800, "likes": 40, "comments": 5, "shares": 5,
                          "saved": 1, "total_interactions": 51}},
            {"id": "m2", "media_type": "CAROUSEL_ALBUM", "media_product_type": "FEED",
             "timestamp": "2026-08-10T15:00:00+0000", "caption": "Pensão pelo Pix",
             "insights": {"reach": 100, "follows": 3, "profile_visits": 4}},
            {"id": "s1", "media_type": "IMAGE", "media_product_type": "STORY", "timestamp": "2026-08-10T15:00:00+0000",
             "insights": {}},
        ]

    async def buscar_raio_x(self, ig_user_id):
        return {"perfil": {"followers_count": 416}, "totais_30d": {"reach": 1256}}


async def _conexao(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(SocialConnection(tenant_id=tenant.id, plataforma="instagram", page_id="1", ig_user_id="999",
                            nome_conta="adv", access_token_encrypted=encrypt_token("tok"), status="ativo"))
    await db.commit()
    return tenant


@pytest.mark.anyio
async def test_grava_posts_com_formato_area_e_metricas_e_o_raio_x(db_session):
    tenant = await _conexao(db_session)

    assert await coletar_instagram(db_session, criar_api=lambda token: ApiFalsa()) == 1

    posts = {p.media_id: p for p in (await db_session.execute(select(InstagramPost))).scalars()}
    assert set(posts) == {"m1", "m2"}  # story fica de fora
    assert posts["m1"].formato == "Reels" and posts["m1"].area == "Trabalhista"
    assert posts["m1"].alcance == 900 and posts["m1"].interacoes == 51 and posts["m1"].salvamentos == 1
    assert posts["m2"].formato == "Carrossel" and posts["m2"].area == "Família"
    assert posts["m2"].seguidores_ganhos == 3
    raio_x = (await db_session.execute(select(SocialMetric).where(SocialMetric.tipo == "ig_raio_x"))).scalar_one()
    assert raio_x.metricas["perfil"]["followers_count"] == 416


@pytest.mark.anyio
async def test_segunda_coleta_atualiza_em_vez_de_duplicar(db_session):
    await _conexao(db_session)
    await coletar_instagram(db_session, criar_api=lambda token: ApiFalsa(alcance=900))
    await coletar_instagram(db_session, criar_api=lambda token: ApiFalsa(alcance=1200))

    posts = (await db_session.execute(select(InstagramPost))).scalars().all()
    assert len(posts) == 2
    assert next(p for p in posts if p.media_id == "m1").alcance == 1200
