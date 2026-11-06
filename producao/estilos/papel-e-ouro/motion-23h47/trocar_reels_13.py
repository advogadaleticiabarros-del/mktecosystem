"""Troca pedida pela Jessica em 06/11/2026: o Reels 23h47 entra hoje 21h; os 4 Reels do 13º descem uma vaga (ter/sex 21h)."""
import asyncio
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from app.db import SessionLocal
from app.models.scheduled_post import ScheduledPost
from app.models.content_piece import ContentPiece
MOVER = [("ab803465-23a5-4230-8a3e-c9cc1e90419f", "2026-11-10"), ("c9ec4153-8ed5-46ba-8e11-dc6c7dffa750", "2026-11-13"),
         ("a6b4a53d-b884-4803-836e-2f976edddce3", "2026-11-17"), ("86a8ee1f-cbfe-45de-b138-2878c9699f8a", "2026-11-20")]
async def m():
    async with SessionLocal() as db:
        livre = (await db.execute(select(ScheduledPost).where(ScheduledPost.canal == "instagram", ScheduledPost.data_agendada == date(2026, 11, 20),
                 ScheduledPost.horario == "21:00", ScheduledPost.status != "cancelado"))).scalars().first()
        assert livre is None, f"20/11 21h ocupado: {livre.titulo}"
        for sid, dia in reversed(MOVER):
            sp = await db.get(ScheduledPost, sid)
            assert sp.status == "pronto", (sp.titulo, sp.status)
            sp.data_agendada = date.fromisoformat(dia)
            if sp.content_piece_id:
                p = await db.get(ContentPiece, sp.content_piece_id)
                if isinstance(p.corpo, dict) and p.corpo.get("programacao"):
                    p.corpo = {**p.corpo, "programacao": {**p.corpo["programacao"], "data": dia}}; flag_modified(p, "corpo")
            print("movido", sp.titulo, "->", dia)
        await db.commit()
asyncio.run(m())