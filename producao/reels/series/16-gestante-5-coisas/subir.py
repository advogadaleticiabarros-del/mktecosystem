"""Roda DENTRO do container da API (16/10/2026): sobe o Reels "5 coisas que a empresa não pode fazer com a gestante"
como peça NOVA em rascunho (Para aprovar), sem data (a Letícia escolhe o dia: a agenda até 31/12 está cheia, 1 por dia).
Não altera nenhuma peça existente. Conta os Reels antes e depois. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/g5/subir.py
"""
import asyncio
import sys
from datetime import date

from sqlalchemy import func, select

sys.path.insert(0, "/tmp/g5")
from legendas import LEGENDA, PRIMEIRO_COMENTARIO  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402

TITULO = "Reels: 5 coisas que a empresa não pode fazer com a gestante"
VIDEO = f"{settings.PUBLIC_API_URL}/media/gestante-5-coisas-v1.mp4?v=1"


async def contar(db) -> int:
    return (await db.execute(select(func.count()).select_from(ContentPiece).where(ContentPiece.tipo == "reels"))).scalar_one()


async def main():
    async with SessionLocal() as db:
        antes = await contar(db)
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        pauta = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == TITULO))).scalars().first()
        if not pauta:
            pauta = Pauta(tenant_id=tid, titulo=TITULO, angulo="reels", area="Trabalhista", origem="manual",
                          fonte="Gravação da Dra. Letícia (7 partes, 31/07/2026)", relevante_para_conteudo=True,
                          status="em_producao", data_editorial=date(2026, 10, 16))
            db.add(pauta)
            await db.flush()
        ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == "reels"))).scalars().first()
        if not ja:
            db.add(ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=1, corpo={
                "video": VIDEO, "legenda": LEGENDA, "primeiro_comentario": PRIMEIRO_COMENTARIO}))
        await db.commit()
        print("reels antes:", antes, "depois:", await contar(db))


asyncio.run(main())
