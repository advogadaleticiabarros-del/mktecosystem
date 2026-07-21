import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.integrations.social.google_business_client import GoogleBusinessClient
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric

logger = logging.getLogger(__name__)


async def coletar_metricas_google_business(db: AsyncSession) -> int:
    conexoes = (
        await db.execute(
            select(SocialConnection).where(
                SocialConnection.plataforma == "google_business", SocialConnection.status == "ativo"
            )
        )
    ).scalars().all()

    coletados = 0
    for conexao in conexoes:
        refresh_token = decrypt_token(conexao.access_token_encrypted)
        client = GoogleBusinessClient(
            client_id=settings.GOOGLE_CLIENT_ID, client_secret=settings.GOOGLE_CLIENT_SECRET
        )
        try:
            access_token = await client.renovar_access_token(refresh_token)
            metricas = await client.buscar_metricas(access_token, conexao.ig_user_id)
        except Exception:
            logger.exception(
                "Falha ao coletar métricas do Google Meu Negócio (tenant %s)", conexao.tenant_id
            )
            continue

        db.add(
            SocialMetric(
                tenant_id=conexao.tenant_id, tipo="google_business", referencia_id=None, metricas=metricas
            )
        )
        await db.commit()
        coletados += 1

    return coletados
