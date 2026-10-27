"""Roda no container: busca fotos verticais no Pexels com a chave do Orbit e imprime JSON (id, alt, fotógrafo, urls)."""
import asyncio, json, sys
import httpx
from sqlalchemy import select
from app.db import SessionLocal
from app.models.tenant import Tenant
from app.services.chaves_api import obter_chave

BUSCAS = sys.argv[1:]


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        chave = await obter_chave(db, tid, "pexels")
    out = {}
    async with httpx.AsyncClient(timeout=30) as c:
        for q in BUSCAS:
            r = await c.get("https://api.pexels.com/v1/search", params={"query": q, "orientation": "portrait", "per_page": 15},
                            headers={"Authorization": chave})
            out[q] = [{"id": p["id"], "alt": p.get("alt"), "autor": p["photographer"], "w": p["width"], "h": p["height"],
                       "med": p["src"]["medium"], "large2x": p["src"]["large2x"], "orig": p["src"]["original"]} for p in r.json().get("photos", [])]
    print(json.dumps(out, ensure_ascii=False))

asyncio.run(main())
