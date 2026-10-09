import asyncio, json
from datetime import date
from sqlalchemy import select
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
async def main():
    async with SessionLocal() as db:
        n = 0
        for p in (await db.execute(select(ContentPiece).where(ContentPiece.status == "rascunho"))).scalars():
            img = (p.corpo or {}).get("imagem") or ""
            if not img.endswith("-pergunta-v6.jpg"):
                continue
            prog = p.corpo.get("programacao") or {}
            ja = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == p.id))).scalar_one_or_none()
            if ja or not prog.get("data"):
                print("pulado", img, ja, prog); continue
            pauta = await db.get(Pauta, p.pauta_id)
            db.add(ScheduledPost(tenant_id=p.tenant_id, content_piece_id=p.id, titulo=pauta.titulo if pauta else "Pergunta",
                                 canal="instagram", formato="post", data_agendada=date.fromisoformat(prog["data"]),
                                 horario=prog.get("hora", "12:00"), status="pronto"))
            p.status = "aprovado"; n += 1
            print("agendado", prog["data"], prog.get("hora"), img.rsplit("/", 1)[1])
        await db.commit(); print("total", n)
asyncio.run(main())
