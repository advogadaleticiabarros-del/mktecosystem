"""Publica automaticamente no Instagram os agendamentos aprovados e prontos.

Nunca publica rascunho: verifica que o content_piece está aprovado antes de
renderizar/publicar. Sem conexão ativa do tenant, pula silenciosamente.
"""
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.integrations.social.instagram_api import InstagramAPI
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import TenantConfig
from app.services.render_criativo import renderizar_slide

logger = logging.getLogger(__name__)
MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
LIMITE_TENTATIVAS = 3


async def _agendamentos_prontos(db: AsyncSession) -> list[ScheduledPost]:
    # Só "carrossel" tem publicador implementado hoje (renderiza slides e
    # monta o carrossel via Graph API). Legenda ("post") e stories ainda não
    # têm asset visual próprio — nunca selecionar, pra não tentar montar um
    # carrossel vazio e estourar tentativas à toa.
    agora = datetime.now(timezone.utc)
    hoje = agora.date()
    resultado = await db.execute(
        select(ScheduledPost).where(
            ScheduledPost.canal == "instagram",
            ScheduledPost.formato == "carrossel",
            ScheduledPost.status == "pronto",
            ScheduledPost.data_agendada <= hoje,
        )
    )
    return list(resultado.scalars().all())


async def _conexao_ativa(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection | None:
    resultado = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == tenant_id,
            SocialConnection.plataforma == "instagram",
            SocialConnection.status == "ativo",
        )
    )
    return resultado.scalar_one_or_none()


async def publicar_agendamentos_prontos(db: AsyncSession) -> int:
    publicados = 0
    MEDIA_DIR.mkdir(exist_ok=True)

    for agendamento in await _agendamentos_prontos(db):
        conexao = await _conexao_ativa(db, agendamento.tenant_id)
        if conexao is None:
            logger.info("Tenant %s sem conexão Instagram ativa; pulando.", agendamento.tenant_id)
            continue

        piece = (
            await db.execute(
                select(ContentPiece).where(ContentPiece.id == agendamento.content_piece_id)
            )
        ).scalar_one_or_none()
        if piece is None or piece.status != "aprovado":
            continue

        tenant_config = (
            await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == agendamento.tenant_id))
        ).scalar_one_or_none()
        identidade_visual = tenant_config.identidade_visual if tenant_config else {}

        page_token = decrypt_token(conexao.access_token_encrypted)
        api = InstagramAPI(page_token=page_token)

        try:
            slides = piece.corpo.get("slides", [])
            urls_imagens = []
            for i, texto in enumerate(slides):
                nome_arquivo = f"{agendamento.id}-{i}.png"
                caminho = MEDIA_DIR / nome_arquivo
                await renderizar_slide(texto, i, len(slides), identidade_visual, str(caminho))
                urls_imagens.append(f"{settings.PUBLIC_API_URL}/media/{nome_arquivo}")

            post_id = await api.publicar_carrossel(conexao.ig_user_id, urls_imagens)
        except Exception:
            logger.exception("Falha ao publicar agendamento %s", agendamento.id)
            agendamento.tentativas += 1
            if agendamento.tentativas >= LIMITE_TENTATIVAS:
                agendamento.status = "erro"
            await db.commit()
            continue

        agendamento.status = "publicado"
        agendamento.platform_post_id = post_id
        await db.commit()
        publicados += 1

    return publicados
