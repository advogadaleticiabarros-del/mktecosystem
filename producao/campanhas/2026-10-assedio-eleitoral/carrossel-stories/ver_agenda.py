"""Roda no container: agenda de 26/10 a 31/10, peças com programação nesses dias e contagem de peças por tipo."""
import asyncio
from datetime import date
from sqlalchemy import select, func
from app.db import SessionLocal
from app.models.scheduled_post import ScheduledPost
from app.models.content_piece import ContentPiece


async def main():
    async with SessionLocal() as db:
        r = (await db.execute(select(ScheduledPost).where(ScheduledPost.data_agendada >= date(2026, 10, 26),
             ScheduledPost.data_agendada <= date(2026, 10, 31)).order_by(ScheduledPost.data_agendada, ScheduledPost.horario))).scalars().all()
        for s in r:
            print(s.data_agendada, s.horario, s.canal, s.formato, s.status, (s.titulo or "")[:60])
        print("--- contagem por tipo")
        for t, n in (await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all():
            print(t, n)
        print("--- programação 27/10 (rascunho/aprovado)")
        for c in (await db.execute(select(ContentPiece))).scalars().all():
            pr = (c.corpo or {}).get("programacao") or {}
            if pr.get("data") in ("2026-10-27", "2026-10-28"):
                print(c.tipo, c.status, pr, str(c.id)[:8])

asyncio.run(main())
