"""Roda DENTRO do container da API: lista a agenda de 10/11/2026 em diante (só leitura), em TSV."""
import asyncio
from datetime import date

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost


async def main():
    async with SessionLocal() as db:
        rows = (await db.execute(select(ScheduledPost, ContentPiece).outerjoin(
            ContentPiece, ScheduledPost.content_piece_id == ContentPiece.id).where(
            ScheduledPost.data_agendada >= date(2026, 11, 10)).order_by(
            ScheduledPost.data_agendada, ScheduledPost.horario))).all()
        for s, p in rows:
            print("\t".join([str(s.data_agendada), s.horario, s.canal, s.formato, s.status, p.tipo if p else "-",
                             p.status if p else "-", s.titulo[:70]]))


asyncio.run(main())
