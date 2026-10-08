"""Publica automaticamente no Instagram os agendamentos aprovados e prontos.

Nunca publica rascunho: verifica que o content_piece está aprovado antes de
renderizar/publicar. Sem conexão ativa do tenant, pula silenciosamente.

Formatos: carrossel e post de imagem única (frase, pergunta, estático). A
transformação peça → imagens + legenda fica em `midia_instagram`; peças sem
imagem própria (legenda solta, stories, reels) continuam como "pronto" para
publicação manual, sem gastar tentativas.

Depois de publicar, posta o primeiro comentário do próprio perfil quando a peça
traz um (regra de docs/MANUAL_CONTEUDO_REDES.md). Falha no comentário só gera
log: o post já está no ar e não pode ser republicado.
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
from app.services.agendamento_horario import horario_ja_chegou
from app.services.midia_instagram import PecaSemConteudo, Renderizador, montar_midia, publicavel

logger = logging.getLogger(__name__)
MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
LIMITE_TENTATIVAS = 3


async def _agendamentos_prontos(db: AsyncSession) -> list[tuple[ScheduledPost, ContentPiece]]:
    agora = datetime.now(timezone.utc)
    resultado = await db.execute(
        select(ScheduledPost, ContentPiece)
        .join(ContentPiece, ContentPiece.id == ScheduledPost.content_piece_id)
        .where(
            ScheduledPost.canal == "instagram",
            ScheduledPost.formato.in_(["carrossel", "post"]),
            ScheduledPost.status == "pronto",
            ScheduledPost.data_agendada <= agora.date(),
            ContentPiece.status == "aprovado",
        )
    )
    return [
        (agendamento, piece)
        for agendamento, piece in resultado.all()
        if publicavel(piece.tipo)
        and horario_ja_chegou(agendamento.data_agendada, agendamento.horario, agora)
    ]


async def _conexao_ativa(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection | None:
    resultado = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == tenant_id,
            SocialConnection.plataforma == "instagram",
            SocialConnection.status == "ativo",
        )
    )
    return resultado.scalar_one_or_none()


async def publicar_agendamentos_prontos(
    db: AsyncSession, renderizador: Renderizador | None = None
) -> int:
    publicados = 0

    for agendamento, piece in await _agendamentos_prontos(db):
        conexao = await _conexao_ativa(db, agendamento.tenant_id)
        if conexao is None:
            logger.info("Tenant %s sem conexão Instagram ativa; pulando.", agendamento.tenant_id)
            continue

        tenant_config = (
            await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == agendamento.tenant_id))
        ).scalar_one_or_none()
        identidade_visual = tenant_config.identidade_visual if tenant_config else {}
        api = InstagramAPI(page_token=decrypt_token(conexao.access_token_encrypted))

        try:
            midia = await montar_midia(
                piece,
                identidade_visual=identidade_visual,
                pasta=MEDIA_DIR,
                base_url=f"{settings.PUBLIC_API_URL}/media",
                prefixo=str(agendamento.id),
                renderizador=renderizador,
            )
            if len(midia.imagens) == 1:
                post_id = await api.publicar_imagem_unica(
                    conexao.ig_user_id, midia.imagens[0], legenda=midia.legenda
                )
            else:
                post_id = await api.publicar_carrossel(
                    conexao.ig_user_id, midia.imagens, legenda=midia.legenda
                )
        except PecaSemConteudo:
            logger.warning("Agendamento %s sem conteúdo de imagem; marcado como erro.", agendamento.id)
            agendamento.status = "erro"
            await db.commit()
            continue
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

        if midia.primeiro_comentario:
            try:
                await api.comentar(post_id, midia.primeiro_comentario)
            except Exception:
                logger.exception("Post %s publicado, mas o primeiro comentário falhou", post_id)

    return publicados
