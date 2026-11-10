"""Roda DENTRO do container da API (só leitura): agenda de hoje em diante com a imagem de cada post, em TSV.
Colunas: data, hora, canal, formato, status, tipo da peça, título, imagem (capa do Reels, arte ou 1º slide)."""
import asyncio

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.services.agendamento_horario import hoje_brasilia


def imagem(p):
    c = (p.corpo or {}) if p else {}
    if c.get("capa"):
        return c["capa"]
    if c.get("imagem"):
        return c["imagem"]
    if c.get("imagens"):
        return c["imagens"][0]
    return ""


async def main():
    async with SessionLocal() as db:
        rows = (await db.execute(select(ScheduledPost, ContentPiece).outerjoin(
            ContentPiece, ScheduledPost.content_piece_id == ContentPiece.id).where(
            ScheduledPost.data_agendada >= hoje_brasilia()).order_by(
            ScheduledPost.data_agendada, ScheduledPost.horario))).all()
        for s, p in rows:
            print("\t".join([str(s.data_agendada), s.horario, s.canal, s.formato, s.status, p.tipo if p else "-",
                             s.titulo.replace("\t", " ")[:90], imagem(p)]))


asyncio.run(main())
