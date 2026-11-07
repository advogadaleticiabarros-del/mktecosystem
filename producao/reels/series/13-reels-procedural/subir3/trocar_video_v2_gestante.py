"""Troca o vídeo da série Gestante e insalubridade (1/3, 2/3, 3/3) e do Pensão: mito dos 30% pela versão 2 (07/11/2026:
eixo central, rosto sem texto por cima, efeitos sonoros reais da Mixkit). Arquivos antigos ficam em /app/media."""
import asyncio
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
NOMES = ["gestante-insalubridade-1", "gestante-insalubridade-2", "gestante-insalubridade-3", "pensao-mito-30"]
async def m():
    async with SessionLocal() as db:
        for p in (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars():
            c = dict(p.corpo or {}); v = c.get("video") or ""
            for n in NOMES:
                if f"/media/{n}.mp4" in v:
                    c["video_antes_v2"] = v
                    c["video"] = v.split("/media/")[0] + f"/media/{n}-v2.mp4?v=v1"
                    p.corpo = c; flag_modified(p, "corpo"); print(p.status, n, "->", c["video"])
        await db.commit()
asyncio.run(m())
