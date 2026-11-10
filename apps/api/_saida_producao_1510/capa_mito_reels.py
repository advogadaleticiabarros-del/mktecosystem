"""Roda DENTRO do container da API: põe a capa Moldura Viva (capa padrão aprovada pela Jessica em 10/11/2026) nos
Reels Mito ou Lei. Acha a peça pelo vídeo (`mito-lei-<MM-DD>-<slug>-v3.mp4`) e grava corpo.capa com
`mito-lei-<MM-DD>-<slug>-capa.jpg`. O publicador manda essa URL como cover_url. Peça publicada não é tocada.
Idempotente.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/capamito/capa_mito_reels.py [--aplicar]"""
import asyncio
import re
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece

MIDIA = Path("/app/media")
V = "mv1"


async def main(aplicar):
    async with SessionLocal() as db:
        pecas = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars().all()
        trocadas = 0
        for p in pecas:
            m = re.search(r"/media/mito-lei-(\d\d-\d\d-[a-z0-9-]+)-v3\.mp4", (p.corpo or {}).get("video", ""))
            if not m:
                continue
            arquivo = f"mito-lei-{m.group(1)}-capa.jpg"
            url = f"{settings.PUBLIC_API_URL}/media/{arquivo}?v={V}"
            if not (MIDIA / arquivo).exists():
                print(m.group(1), "SEM CAPA em /app/media")
                continue
            if p.status == "publicado" or (p.corpo or {}).get("capa") == url:
                continue
            print(m.group(1), p.status, "->", arquivo)
            trocadas += 1
            if aplicar:
                corpo = dict(p.corpo)
                corpo["capa"] = url
                p.corpo = corpo
                flag_modified(p, "corpo")
        if aplicar:
            await db.commit()
        print(("aplicadas: " if aplicar else "aplicaria: ") + str(trocadas))


asyncio.run(main("--aplicar" in sys.argv))
