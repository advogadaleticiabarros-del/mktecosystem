"""Roda DENTRO do container da API (20/10/2026): sobe a v2 dos 2 Reels da série 18 (falas limpas, sem o travamento)
como peças NOVAS (versao=2) em rascunho, nas mesmas pautas da v1. A v1 não é alterada (regra "material pronto nunca
some"). Idempotente: não duplica se o vídeo da v2 já estiver numa peça.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s18/subir_v2.py
"""
import asyncio
import sys

from sqlalchemy import func, select

sys.path.insert(0, "/tmp/s18")
from legendas import LEGENDAS  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402

ARQUIVOS = {1: "limbo-previdenciario-1-v2.mp4", 2: "limbo-previdenciario-2-v2.mp4"}


async def contar(db) -> int:
    return (await db.execute(select(func.count()).select_from(ContentPiece).where(ContentPiece.tipo == "reels"))).scalar_one()


async def main():
    async with SessionLocal() as db:
        antes = await contar(db)
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        for n, arq in ARQUIVOS.items():
            leg = LEGENDAS[n]
            pauta = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == leg["titulo"]))).scalars().first()
            assert pauta, f"pauta da v1 não encontrada: {leg['titulo']}"
            video = f"{settings.PUBLIC_API_URL}/media/{arq}?v=1"
            pecas = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == "reels"))).scalars().all()
            if any((p.corpo or {}).get("video") == video for p in pecas):
                continue
            db.add(ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=2, corpo={
                "video": video, "legenda": leg["legenda"], "primeiro_comentario": leg["pc"]}))
        await db.commit()
        print("reels antes:", antes, "depois:", await contar(db))


asyncio.run(main())
