"""Troca o vídeo dos 4 Reels do 13º pela versão com efeitos sonoros v2 (06/11/2026). Os arquivos antigos ficam em /app/media."""
import asyncio
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
NOMES = ["13-sem-susto-reel-2", "13-sem-susto-reel-3", "13-proporcional-calculo", "13-quatro-regras"]
async def m():
    async with SessionLocal() as db:
        for p in (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars():
            c = dict(p.corpo or {}); v = c.get("video") or ""
            for n in NOMES:
                if f"/media/{n}.mp4" in v:
                    c["video_antes_som2"] = v
                    c["video"] = v.split("/media/")[0] + f"/media/{n}-som2.mp4?v=v1"
                    p.corpo = c; flag_modified(p, "corpo"); print(p.status, n, "->", c["video"])
        await db.commit()
asyncio.run(m())