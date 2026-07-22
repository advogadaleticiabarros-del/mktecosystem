"""Publica automaticamente no blog os agendamentos aprovados e prontos.

Nunca publica rascunho: verifica que o content_piece está aprovado antes de
renderizar/publicar. Faz upload do HTML do artigo, da capa, do índice
atualizado e do sitemap atualizado via SFTP.
"""
import logging
from datetime import date, datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.integrations.publish.sftp_client import SFTPClient
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import TenantConfig
from app.services.agendamento_horario import horario_ja_chegou
from app.services.blog_index_editor import inserir_card, inserir_sitemap_entry
from app.services.blog_slug import gerar_slug
from app.services.render_artigo_blog import (
    estimar_tempo_leitura,
    renderizar_artigo_html,
    renderizar_capa_artigo,
)

logger = logging.getLogger(__name__)
MEDIA_DIR = Path(__file__).parent.parent.parent / "media"
LIMITE_TENTATIVAS = 3
BLOG_BASE_URL = "https://advogadaleticiabarros.com.br/blog/"


async def _agendamentos_prontos(db: AsyncSession) -> list[ScheduledPost]:
    agora = datetime.now(timezone.utc)
    hoje = agora.date()
    resultado = await db.execute(
        select(ScheduledPost).where(
            ScheduledPost.canal == "blog",
            ScheduledPost.status == "pronto",
            ScheduledPost.data_agendada <= hoje,
        )
    )
    candidatos = resultado.scalars().all()
    return [
        agendamento
        for agendamento in candidatos
        if horario_ja_chegou(agendamento.data_agendada, agendamento.horario, agora)
    ]


async def publicar_agendamentos_prontos(db: AsyncSession) -> int:
    publicados = 0
    MEDIA_DIR.mkdir(exist_ok=True)

    for agendamento in await _agendamentos_prontos(db):
        piece = (
            await db.execute(
                select(ContentPiece).where(ContentPiece.id == agendamento.content_piece_id)
            )
        ).scalar_one_or_none()
        if piece is None or piece.status != "aprovado":
            continue

        pauta = (
            await db.execute(select(Pauta).where(Pauta.id == piece.pauta_id))
        ).scalar_one_or_none()
        categoria = pauta.area if pauta else "Direito"

        tenant_config = (
            await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == agendamento.tenant_id))
        ).scalar_one_or_none()
        identidade_visual = tenant_config.identidade_visual if tenant_config else {}

        sftp = SFTPClient(
            host=settings.BLOG_SFTP_HOST,
            port=settings.BLOG_SFTP_PORT,
            user=settings.BLOG_SFTP_USER,
            password=settings.BLOG_SFTP_PASSWORD,
        )

        try:
            titulo = piece.corpo["titulo"]
            slug = gerar_slug(titulo) or "artigo"
            categoria_slug = gerar_slug(categoria)
            url_artigo = f"{BLOG_BASE_URL}{slug}.html"
            meta_description = piece.corpo.get("meta_description", "")
            resumo = piece.corpo.get("resumo", "")

            html_artigo = renderizar_artigo_html(
                titulo=titulo,
                meta_description=meta_description,
                categoria=categoria,
                resumo=resumo,
                corpo_html=piece.corpo["html"],
                slug=slug,
                data_publicacao=date.today(),
            )

            caminho_capa_local = MEDIA_DIR / f"{agendamento.id}-capa.png"
            await renderizar_capa_artigo(
                titulo=titulo,
                categoria=categoria,
                identidade_visual=identidade_visual,
                caminho_saida=str(caminho_capa_local),
            )
            capa_bytes = caminho_capa_local.read_bytes()

            index_atual = (await sftp.download(f"{settings.BLOG_SFTP_PATH}index.html")).decode("utf-8")
            sitemap_atual = (await sftp.download(f"{settings.BLOG_SFTP_PATH}../sitemap.xml")).decode("utf-8")

            index_novo = inserir_card(
                index_atual,
                url=f"{slug}.html",
                imagem=f"capas/{slug}.png",
                categoria=categoria,
                categoria_slug=categoria_slug,
                titulo=titulo,
                resumo=resumo,
                tempo_leitura=estimar_tempo_leitura(piece.corpo["html"]),
            )
            sitemap_novo = inserir_sitemap_entry(
                sitemap_atual, url=url_artigo, data_iso=date.today().isoformat()
            )

            await sftp.upload(f"{settings.BLOG_SFTP_PATH}{slug}.html", html_artigo.encode("utf-8"))
            await sftp.garantir_diretorio(f"{settings.BLOG_SFTP_PATH}capas")
            await sftp.upload(f"{settings.BLOG_SFTP_PATH}capas/{slug}.png", capa_bytes)
            await sftp.upload(f"{settings.BLOG_SFTP_PATH}index.html", index_novo.encode("utf-8"))
            await sftp.upload(f"{settings.BLOG_SFTP_PATH}../sitemap.xml", sitemap_novo.encode("utf-8"))
        except Exception:
            logger.exception("Falha ao publicar artigo do agendamento %s", agendamento.id)
            agendamento.tentativas += 1
            if agendamento.tentativas >= LIMITE_TENTATIVAS:
                agendamento.status = "erro"
            await db.commit()
            await sftp.close()
            continue

        await sftp.close()
        agendamento.status = "publicado"
        agendamento.platform_post_id = url_artigo
        await db.commit()
        publicados += 1

    return publicados
