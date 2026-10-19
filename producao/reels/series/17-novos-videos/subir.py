"""Roda DENTRO do container da API (18/10/2026): sobe os 5 Reels da série 17 como peças NOVAS em rascunho (Para
aprovar), sem data (a agenda até 31/12 está cheia: a Letícia escolhe os dias). Não altera nenhuma peça existente.
Conta os Reels antes e depois. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s17/subir.py
"""
import asyncio
import sys
from datetime import date

from sqlalchemy import func, select

sys.path.insert(0, "/tmp/s17")
from legendas import LEGENDAS  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402

ARQUIVOS = {1: "multa-477-pedido-demissao-v1.mp4", 2: "conselhos-advogada-v1.mp4", 3: "hora-extra-1-v1.mp4",
            4: "hora-extra-2-v1.mp4", 5: "hora-extra-3-v1.mp4"}


async def contar(db) -> int:
    return (await db.execute(select(func.count()).select_from(ContentPiece).where(ContentPiece.tipo == "reels"))).scalar_one()


async def main():
    async with SessionLocal() as db:
        antes = await contar(db)
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        for n, arq in ARQUIVOS.items():
            leg = LEGENDAS[n]
            pauta = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == leg["titulo"]))).scalars().first()
            if not pauta:
                pauta = Pauta(tenant_id=tid, titulo=leg["titulo"], angulo="reels", area="Trabalhista", origem="manual",
                              fonte="Gravações da Dra. Letícia (Desktop/novo video)", relevante_para_conteudo=True,
                              status="em_producao", data_editorial=date(2026, 10, 18))
                db.add(pauta)
                await db.flush()
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == "reels"))).scalars().first()
            if ja:
                continue
            db.add(ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=1, corpo={
                "video": f"{settings.PUBLIC_API_URL}/media/{arq}?v=1", "legenda": leg["legenda"], "primeiro_comentario": leg["pc"]}))
        await db.commit()
        print("reels antes:", antes, "depois:", await contar(db))


asyncio.run(main())
