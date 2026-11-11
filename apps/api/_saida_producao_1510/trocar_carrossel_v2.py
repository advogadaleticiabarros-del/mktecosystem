"""Roda DENTRO do container: troca a arte dos 16 carrosséis de jan-fev/2027 pela versão V2 (11/11/2026, pedido da
Jessica). Acha a peça pelo nome da 1ª imagem v5 (carrossel-<chave>-v5-1.jpg); guarda a lista antiga em
corpo.imagens_anterior. Idempotente. Uso: python trocar_carrossel_v2.py [--aplicar]"""
import asyncio
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece

CHAVES = sys.argv[1].split(",")
MIDIA = Path("/app/media")


async def main(aplicar):
    async with SessionLocal() as db:
        ps = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "carrossel"))).scalars().all()
        for k in CHAVES:
            alvo = [p for p in ps if any(f"carrossel-{k}-v5-1.jpg" in str(u) for u in (p.corpo or {}).get("imagens", []))
                    or any(f"carrossel-{k}-v2-1.jpg" in str(u) for u in (p.corpo or {}).get("imagens", []))]
            if len(alvo) != 1:
                print(k, "achei", len(alvo)); continue
            p = alvo[0]
            novas = [f"{settings.PUBLIC_API_URL}/media/carrossel-{k}-v2-{i}.jpg?v=v2" for i in range(1, 8)]
            if p.corpo.get("imagens") == novas:
                continue
            faltam = [i for i in range(1, 8) if not (MIDIA / f"carrossel-{k}-v2-{i}.jpg").exists()]
            if faltam:
                print(k, "SEM ARQUIVO", faltam); continue
            print("trocar", k)
            if aplicar:
                p.corpo = {**p.corpo, "imagens_anterior": p.corpo.get("imagens"), "imagens": novas, "estilo": "carrossel-v2"}
                flag_modified(p, "corpo")
        if aplicar:
            await db.commit(); print("aplicado")


asyncio.run(main("--aplicar" in sys.argv))
