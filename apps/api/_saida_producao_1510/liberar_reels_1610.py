"""Roda DENTRO do container da API (16/10/2026). A Letícia aprovou os Reels na versão limpa ("Está aprovado").
- Os agendamentos de Reels pausados voltam para "pronto" (mesmas datas, 21h).
- A série Guarda (rascunho) é aprovada e agendada pela programação combinada (23, 25 e 27/10, 21h).
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/liberar/liberar_reels_1610.py
"""
import asyncio
from collections import Counter
from datetime import date

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.services.agenda import agendar_conteudo_aprovado

GUARDA = ("edf05653", "6cfb0f26", "196a4767")


async def main():
    async with SessionLocal() as db:
        sps = (await db.execute(select(ScheduledPost).where(ScheduledPost.formato == "reels",
                                                             ScheduledPost.status == "pausado"))).scalars().all()
        for sp in sps:
            sp.status = "pronto"
        print("reels liberados:", sorted(f"{s.data_agendada} {s.horario}" for s in sps))
        pecas = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars().all()
        for p in pecas:
            if str(p.id)[:8] in GUARDA and p.status == "rascunho":
                p.status = "aprovado"
                await db.flush()
                novo = await agendar_conteudo_aprovado(db, p)
                print("guarda aprovada:", str(p.id)[:8], novo.data_agendada if novo else "já agendada", novo.horario if novo else "")
        await db.commit()
        dias = Counter(s.data_agendada for s in (await db.execute(select(ScheduledPost).where(
            ScheduledPost.canal == "instagram", ScheduledPost.formato != "story",
            ScheduledPost.data_agendada >= date(2026, 10, 17)))).scalars().all())
        print("dias com mais de 1 post:", sorted(str(d) for d, n in dias.items() if n > 1))


asyncio.run(main())
