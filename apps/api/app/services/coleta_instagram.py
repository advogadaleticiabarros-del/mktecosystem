"""Coleta completa do Instagram: cada publicação com suas métricas + retrato da conta.

Interface: `coletar_instagram(db, tenant_id=None, criar_api=...)` percorre as conexões ativas
(de um tenant, ou de todos),
grava/atualiza `InstagramPost` (um por publicação, sem duplicar) e guarda o
retrato da conta em `SocialMetric(tipo="ig_raio_x")`. Devolve quantas contas
foram coletadas. `criar_api(token)` permite trocar o cliente da Meta nos testes.
"""
import logging
import uuid
from datetime import datetime, timezone
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import decrypt_token
from app.integrations.social.instagram_api import InstagramAPI
from app.models.instagram_post import InstagramPost
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.services.analise_instagram import classificar_area

logger = logging.getLogger(__name__)

_FORMATO = {"REELS": "Reels", "CAROUSEL_ALBUM": "Carrossel", "IMAGE": "Imagem", "VIDEO": "Reels"}


def _formato(post: dict) -> str | None:
    if post.get("media_product_type") == "STORY":
        return None
    if post.get("media_product_type") == "REELS":
        return "Reels"
    return _FORMATO.get(post.get("media_type", ""))


def _campos(post: dict) -> dict:
    i = post.get("insights", {})
    return {
        "publicado_em": datetime.strptime(post["timestamp"], "%Y-%m-%dT%H:%M:%S%z"),
        "formato": _formato(post),
        "area": classificar_area(post.get("caption")),
        "legenda": post.get("caption"),
        "permalink": post.get("permalink"),
        "alcance": i.get("reach", 0),
        "visualizacoes": i.get("views", 0),
        "curtidas": i.get("likes", post.get("like_count", 0)),
        "comentarios": i.get("comments", post.get("comments_count", 0)),
        "compartilhamentos": i.get("shares", 0),
        "salvamentos": i.get("saved", 0),
        "interacoes": i.get("total_interactions", 0),
        "seguidores_ganhos": i.get("follows"),
        "visitas_perfil": i.get("profile_visits"),
        "atualizado_em": datetime.now(timezone.utc),
    }


async def coletar_instagram(
    db: AsyncSession,
    tenant_id: uuid.UUID | None = None,
    criar_api: Callable[[str], object] = lambda token: InstagramAPI(page_token=token),
) -> int:
    filtro = select(SocialConnection).where(
        SocialConnection.plataforma == "instagram", SocialConnection.status == "ativo"
    )
    if tenant_id is not None:
        filtro = filtro.where(SocialConnection.tenant_id == tenant_id)
    conexoes = (await db.execute(filtro)).scalars().all()

    coletadas = 0
    for conexao in conexoes:
        api = criar_api(decrypt_token(conexao.access_token_encrypted))
        try:
            publicacoes = await api.listar_publicacoes(conexao.ig_user_id)
            raio_x = await api.buscar_raio_x(conexao.ig_user_id)
        except Exception:
            logger.exception("Falha na coleta do Instagram do tenant %s", conexao.tenant_id)
            continue

        existentes = {
            p.media_id: p
            for p in (
                await db.execute(select(InstagramPost).where(InstagramPost.tenant_id == conexao.tenant_id))
            ).scalars()
        }
        for post in publicacoes:
            campos = _campos(post)
            if campos["formato"] is None:
                continue
            registro = existentes.get(post["id"])
            if registro is None:
                db.add(InstagramPost(tenant_id=conexao.tenant_id, media_id=post["id"], **campos))
            else:
                for chave, valor in campos.items():
                    setattr(registro, chave, valor)

        db.add(SocialMetric(tenant_id=conexao.tenant_id, tipo="ig_raio_x", referencia_id=None, metricas=raio_x))
        await db.commit()
        coletadas += 1
    return coletadas
