import asyncio
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
async def main():
    async with SessionLocal() as db:
        n = 0
        for p in (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars():
            c = dict(p.corpo or {})
            if "13-sem-susto-reel-3" in (c.get("video") or ""):
                c["video"] = c["video"].replace("?v=v2", "?v=v3"); c["video_sem_musica"] = c["video_sem_musica"].replace("?v=v2", "?v=v3")
                p.corpo = c; flag_modified(p, "corpo"); n += 1
        await db.commit(); print("atualizado", n)
asyncio.run(main())
