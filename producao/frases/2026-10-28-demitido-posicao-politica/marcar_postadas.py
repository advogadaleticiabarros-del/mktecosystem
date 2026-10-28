"""Marca as 5 frases da campanha do voto (pauta d7b867af, 28/10/2026) como postadas à mão e tira a programação."""
import asyncio
import uuid
from sqlalchemy import select
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost

PAUTA = uuid.UUID("d7b867af-0436-48cc-ad1b-a875ef8f78b0")


async def main():
    async with SessionLocal() as db:
        pecas = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == PAUTA))).scalars().all()
        for c in pecas:
            corpo = dict(c.corpo or {})
            prog = corpo.pop("programacao", None)
            corpo["postado_manualmente"] = {"em": "2026-10-28", "programacao_removida": prog}
            c.corpo = corpo
            c.status = "publicado"
            ags = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == c.id))).scalars().all()
            for a in ags:
                a.status = "publicado"
            print(c.id, "publicado", (corpo.get("frase") or "")[:45], "| agendamentos:", len(ags))
        await db.commit()
        print("total", len(pecas))

asyncio.run(main())
