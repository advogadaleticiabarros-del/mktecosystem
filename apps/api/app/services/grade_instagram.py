"""Grade do Instagram: o perfil como vai ficar.

Interface: `montar_grade(db, tenant_id, leitor, hoje)` → posts do feed, do mais novo para o
mais antigo (a ordem do perfil): agendados no Orbit, rascunhos com data de programação
(`corpo.programacao`) e os já publicados lidos do Instagram pelo `leitor` (`recentes()`).
Stories, Reels sem arte e blog ficam de fora: não aparecem na grade do perfil.
Sem leitor (Instagram não conectado) ou com leitor quebrado, mostra só o que está no Orbit.
"""
import logging
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost

logger = logging.getLogger(__name__)
BRASILIA = timezone(timedelta(hours=-3))
TIPOS_FEED = ("carrossel", "pergunta", "frase", "estatico", "post")


@dataclass
class PostGrade:
    data: str
    hora: str
    tipo: str
    status: str  # rascunho | agendado | publicado
    imagens: list[str] = field(default_factory=list)
    legenda: str = ""
    primeiro_comentario: str = ""
    permalink: str | None = None
    piece_id: str | None = None


def _imagens(corpo: dict) -> list[str]:
    if isinstance(corpo.get("imagens"), list):
        return list(corpo["imagens"])
    return [corpo["imagem"]] if corpo.get("imagem") else []


def _da_peca(piece: ContentPiece, data: str, hora: str, status: str) -> PostGrade:
    corpo = piece.corpo or {}
    return PostGrade(data=data, hora=hora, tipo=piece.tipo, status=status, imagens=_imagens(corpo),
                     legenda=corpo.get("legenda", ""), primeiro_comentario=corpo.get("primeiro_comentario", ""),
                     piece_id=str(piece.id))


async def montar_grade(db: AsyncSession, tenant_id: uuid.UUID, leitor, hoje: date) -> list[PostGrade]:
    grade: list[PostGrade] = []

    agendados = (await db.execute(
        select(ScheduledPost, ContentPiece)
        .join(ContentPiece, ContentPiece.id == ScheduledPost.content_piece_id)
        .where(ScheduledPost.tenant_id == tenant_id, ScheduledPost.canal == "instagram",
               ScheduledPost.formato.in_(("carrossel", "post")))
    )).all()
    agendadas = set()
    for ag, piece in agendados:
        agendadas.add(piece.id)
        if ag.status == "publicado" and leitor is not None:
            continue  # vem do Instagram, com o link real
        status = "publicado" if ag.status == "publicado" else "agendado"
        grade.append(_da_peca(piece, ag.data_agendada.isoformat(), ag.horario, status))

    rascunhos = (await db.execute(
        select(ContentPiece).where(ContentPiece.tenant_id == tenant_id, ContentPiece.status == "rascunho",
                                   ContentPiece.tipo.in_(TIPOS_FEED))
    )).scalars().all()
    for piece in rascunhos:
        prog = (piece.corpo or {}).get("programacao") or {}
        if piece.id in agendadas or not prog.get("data") or prog["data"] < hoje.isoformat():
            continue
        grade.append(_da_peca(piece, prog["data"], prog.get("hora", ""), "rascunho"))

    if leitor is not None:
        try:
            for post in await leitor.recentes():
                quando = datetime.strptime(post["timestamp"], "%Y-%m-%dT%H:%M:%S%z").astimezone(BRASILIA)
                imagem = post.get("media_url") if post.get("media_type") != "VIDEO" else post.get("thumbnail_url")
                grade.append(PostGrade(
                    data=quando.date().isoformat(), hora=quando.strftime("%H:%M"),
                    tipo={"CAROUSEL_ALBUM": "carrossel", "VIDEO": "reels"}.get(post.get("media_type"), "post"),
                    status="publicado", imagens=[imagem] if imagem else [], legenda=post.get("caption") or "",
                    permalink=post.get("permalink"),
                ))
        except Exception:
            logger.exception("Grade: não consegui ler os posts publicados do Instagram")

    grade.sort(key=lambda g: (g.data, g.hora), reverse=True)
    return grade


class LeitorPublicados:
    """Últimos posts do perfil com a imagem, pela conta conectada."""

    def __init__(self, api, ig_user_id: str, limite: int = 12) -> None:
        self._api, self._ig, self._limite = api, ig_user_id, limite

    async def recentes(self) -> list[dict]:
        return await self._api.posts_com_imagem(self._ig, self._limite)
