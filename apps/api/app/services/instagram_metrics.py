import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import decrypt_token
from app.integrations.social.instagram_api import InstagramAPI
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric

logger = logging.getLogger(__name__)


async def coletar_metricas_diarias(db: AsyncSession) -> int:
    conexoes = (
        await db.execute(
            select(SocialConnection).where(
                SocialConnection.plataforma == "instagram", SocialConnection.status == "ativo"
            )
        )
    ).scalars().all()

    coletados = 0
    for conexao in conexoes:
        page_token = decrypt_token(conexao.access_token_encrypted)
        api = InstagramAPI(page_token=page_token)
        try:
            metricas = await api.buscar_metricas_conta(conexao.ig_user_id)
        except Exception:
            logger.exception("Falha ao coletar métricas do tenant %s", conexao.tenant_id)
            continue

        db.add(
            SocialMetric(tenant_id=conexao.tenant_id, tipo="conta", referencia_id=None, metricas=metricas)
        )
        await db.commit()
        coletados += 1

    return coletados
