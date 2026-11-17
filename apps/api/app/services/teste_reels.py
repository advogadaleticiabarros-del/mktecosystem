"""Reels comum que só sai se o Reels de teste (Trial) foi bem.

Pedido da Jessica, 27/10/2026: o Reels vai primeiro como teste (só para quem não segue, graduação manual); "performando
bem", ele sai de novo para os seguidores como post novo, e o Orbit é quem monitora. A peça comum leva
`corpo.depende_do_teste` = id da mídia do teste; na hora de publicar, `avaliar` lê os números do teste na Meta e compara
com os Reels recentes do perfil já coletados (`InstagramPost`).

Régua: o teste vai bem se tiver pelo menos 70% da mediana de visualizações dos últimos 10 Reels, ou 3 ou mais
compartilhamentos + salvamentos (sinal forte de conteúdo que circula). Sem Reels de referência, libera.
"""
import uuid
from dataclasses import dataclass
from statistics import median
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.instagram_post import InstagramPost
from app.models.scheduled_post import ScheduledPost

FRACAO_DA_MEDIANA = 0.7
MIN_COMPARTILHA_SALVA = 3
N_REFERENCIA = 10


@dataclass(frozen=True)
class Veredito:
    liberado: bool
    motivo: str


class LeitorDeInsights(Protocol):
    async def insights_reels(self, media_id: str) -> dict: ...


def julgar(insights: dict, views_referencia: list[int]) -> Veredito:
    views = int(insights.get("views") or 0)
    espalha = int(insights.get("shares") or 0) + int(insights.get("saved") or 0)
    if not views_referencia:
        return Veredito(True, f"sem Reels de referência; teste com {views} visualizações")
    meta = round(median(views_referencia) * FRACAO_DA_MEDIANA)
    texto = (f"teste com {views} visualizações e {espalha} compartilhamentos+salvamentos; meta {meta} visualizações "
             f"(70% da mediana dos últimos {len(views_referencia)} Reels) ou {MIN_COMPARTILHA_SALVA} compartilhamentos+salvamentos")
    return Veredito(views >= meta or espalha >= MIN_COMPARTILHA_SALVA, texto)


async def views_referencia(db: AsyncSession, tenant_id: uuid.UUID, excluir: str | None = None) -> list[int]:
    """Visualizações dos últimos Reels do feed. Os Reels de teste ficam de fora: eles só vão a quem não segue e
    puxariam a mediana para baixo (o de 27/10/2026 ficou com 0)."""
    testes = select(ScheduledPost.platform_post_id).where(
        ScheduledPost.tenant_id == tenant_id, ScheduledPost.formato == "trial", ScheduledPost.platform_post_id.is_not(None))
    filtro = [InstagramPost.tenant_id == tenant_id, InstagramPost.formato == "Reels", InstagramPost.media_id.not_in(testes)]
    if excluir:
        filtro.append(InstagramPost.media_id != excluir)
    return list((await db.execute(select(InstagramPost.visualizacoes).where(*filtro)
                                  .order_by(InstagramPost.publicado_em.desc()).limit(N_REFERENCIA))).scalars().all())


async def avaliar(db: AsyncSession, api: LeitorDeInsights, tenant_id: uuid.UUID, media_id: str) -> Veredito:
    insights = await api.insights_reels(media_id)
    return julgar(insights, await views_referencia(db, tenant_id, excluir=media_id))
