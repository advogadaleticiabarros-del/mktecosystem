"""Radar de referências: vigia perfis públicos do Instagram (escolhidos pela
Letícia) e transforma os posts que bombaram em sugestões de pauta.

Interface: `vigiar(db, tenant_id, leitor, perfis, agora)` → pautas criadas, da
mais forte para a mais fraca. O `leitor` entrega os posts recentes de um perfil
(em produção, `LeitorInstagram`, via business discovery da Graph API).

Regras:
- Destaque = post dos últimos 3 dias com engajamento (curtidas + 3× comentários)
  de pelo menos 2× a mediana do próprio perfil. Assim um perfil de 400 mil e um
  de 20 mil seguidores são medidos cada um pela sua régua.
- No máximo 3 por perfil por rodada; o mesmo post nunca vira pauta duas vezes.
- A pauta é inspiração: nada de repostar (originalidade da Meta e ética da OAB).
  Fica `sugerida`, sem data no Editorial, para a Letícia escolher no Planejamento.
- Perfil que falha (privado, fora do ar) não derruba os outros.
"""
import logging
import re
import statistics
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pauta import Pauta

logger = logging.getLogger(__name__)

ORIGEM = "referencia_instagram"
JANELA_DIAS = 3
MULTIPLO_MINIMO = 2.0
MAX_POR_PERFIL = 3

_AREAS = {
    "Trabalhista": ("trabalh", "tst", "trt", "clt", "empreg", "demiss", "fgts", "justa causa", "rescis", "salári", "férias"),
    "Família": ("pensão aliment", "divórci", "guarda", "herança", "famíl", "filho", "casament", "união estável"),
    "Previdenciário": ("inss", "aposent", "previd", "bpc", "loas", "auxílio-doença", "pensão por morte"),
    "Consumidor": ("banco", "consumidor", "pix", "plano de saúde", "compra", "cartão", "golpe"),
}


@dataclass(frozen=True)
class PostReferencia:
    perfil: str
    legenda: str
    formato: str
    curtidas: int
    comentarios: int
    publicado_em: datetime
    link: str

    @property
    def engajamento(self) -> int:
        return self.curtidas + 3 * self.comentarios


class LeitorInstagram:
    """Lê perfis públicos (contas comerciais/criador) pela conta conectada da Letícia."""

    def __init__(self, api, ig_user_id: str) -> None:
        self._api = api
        self._ig_user_id = ig_user_id

    async def posts_recentes(self, perfil: str) -> list[PostReferencia]:
        brutos = await self._api.posts_de_perfil_publico(self._ig_user_id, perfil)
        return [
            PostReferencia(
                perfil=perfil, legenda=m.get("caption") or "", formato=m.get("media_type", ""),
                curtidas=m.get("like_count") or 0, comentarios=m.get("comments_count") or 0,
                publicado_em=datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z"), link=m["permalink"],
            )
            for m in brutos
            if m.get("permalink") and m.get("timestamp")
        ]


def _titulo(legenda: str) -> str:
    texto = re.sub(r"#\w+", "", legenda)
    texto = re.sub(r"[^\w\s.,;:!?()%/ºª°'\"-]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    m = re.match(r"(.+?)([.!?])(\s|$)", texto)
    titulo = (m.group(1) + ("?" if m.group(2) == "?" else "")) if m else texto
    if len(titulo) > 120:
        titulo = titulo[:120].rsplit(" ", 1)[0] + "…"
    return titulo or "Post de referência"


def _area(legenda: str) -> str:
    texto = legenda.lower()
    pontos = {area: sum(texto.count(p) for p in palavras) for area, palavras in _AREAS.items()}
    melhor = max(pontos, key=pontos.get)
    return melhor if pontos[melhor] else "Geral"


async def _links_ja_sugeridos(db: AsyncSession, tenant_id: uuid.UUID) -> set[str]:
    pautas = (await db.execute(select(Pauta).where(Pauta.tenant_id == tenant_id, Pauta.origem == ORIGEM))).scalars()
    return {(p.apuracao or {}).get("link") for p in pautas}


async def vigiar(db: AsyncSession, tenant_id: uuid.UUID, leitor, perfis: list[str], agora: datetime) -> list[Pauta]:
    vistos = await _links_ja_sugeridos(db, tenant_id)
    criadas: list[Pauta] = []
    for perfil in perfis:
        try:
            posts = await leitor.posts_recentes(perfil)
        except Exception:
            logger.exception("Radar de referências: não consegui ler @%s", perfil)
            continue
        if not posts:
            continue
        mediana = statistics.median(p.engajamento for p in posts) or 1
        destaques = sorted(
            (p for p in posts
             if p.publicado_em >= agora - timedelta(days=JANELA_DIAS)
             and p.engajamento >= MULTIPLO_MINIMO * mediana
             and p.link not in vistos),
            key=lambda p: p.engajamento, reverse=True,
        )[:MAX_POR_PERFIL]
        for post in destaques:
            multiplo = post.engajamento / mediana
            pauta = Pauta(
                tenant_id=tenant_id, titulo=_titulo(post.legenda), angulo="direitos", area=_area(post.legenda),
                origem=ORIGEM, fonte=f"@{perfil}", relevante_para_conteudo=True, status="sugerida",
                relevancia=min(99, 60 + int(multiplo * 4)), urgencia="media",
                conteudo_bruto=(
                    f"Inspiração de @{perfil}. Não repostar: transformar em conteúdo próprio, com a nossa voz "
                    f"e as regras da OAB.\nPublicado em {post.publicado_em:%d/%m/%Y}: {post.curtidas} curtidas, "
                    f"{post.comentarios} comentários ({multiplo:.1f}x a média do perfil). Formato: {post.formato}.\n"
                    f"Link: {post.link}\n\nLegenda original:\n{post.legenda}"
                ),
                apuracao={"link": post.link, "perfil": perfil, "curtidas": post.curtidas,
                          "comentarios": post.comentarios, "multiplo_media": round(multiplo, 1),
                          "formato": post.formato},
            )
            db.add(pauta)
            vistos.add(post.link)
            criadas.append(pauta)
    await db.commit()
    return sorted(criadas, key=lambda p: p.relevancia, reverse=True)
