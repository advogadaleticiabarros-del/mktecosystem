"""Roda DENTRO do container da API (18/10/2026). A Letícia aprovou os 5 Reels da série 17 e pediu para distribuir em
dias de Reels pela estratégia de crescimento (novembro: 3 a 4 Reels por semana; dias úteis de melhor alcance, 21h).
Datas escolhidas fora de conteúdo com prazo (20/11, 30/11, Dezembro Vermelho, 13º, Natal). O post do feed que estava
no dia vai para a reserva (corpo.reserva), sem ser apagado. Contagem antes e depois; 1 publicação por dia.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s17ag/agendar_serie17.py
"""
import asyncio
from collections import Counter
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.services.agenda import agendar_conteudo_aprovado

DIAS = {"multa-477-pedido-demissao-v1": "2026-11-24", "hora-extra-1-v1": "2026-11-25", "hora-extra-2-v1": "2026-11-27",
        "hora-extra-3-v1": "2026-12-02", "conselhos-advogada-v1": "2026-12-09"}


async def main():
    async with SessionLocal() as db:
        sps = (await db.execute(select(ScheduledPost).where(ScheduledPost.canal == "instagram"))).scalars().all()
        antes = Counter(s.formato for s in sps)
        pecas = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars().all()
        for p in pecas:
            nome = next((k for k in DIAS if f"/{k}.mp4" in (p.corpo or {}).get("video", "")), None)
            if not nome:
                continue
            dia = DIAS[nome]
            for s in [s for s in sps if str(s.data_agendada) == dia and s.formato not in ("story", "reels")]:
                feed = await db.get(ContentPiece, s.content_piece_id)
                corpo = {k: v for k, v in (feed.corpo or {}).items() if k != "programacao"}
                corpo["reserva"] = {"desde": "2026-10-18", "motivo": "dia passou a ser de Reels (série 17)",
                                    "programacao_antiga": (feed.corpo or {}).get("programacao")}
                feed.corpo = corpo
                flag_modified(feed, "corpo")
                await db.delete(s)
                print("feed para a reserva:", dia, feed.tipo)
            p.corpo = {**p.corpo, "programacao": {"data": dia, "hora": "21:00"}}
            flag_modified(p, "corpo")
            p.status = "aprovado"
            await db.flush()
            novo = await agendar_conteudo_aprovado(db, p)
            print("reels:", nome, "->", (novo.data_agendada, novo.horario) if novo else "já tinha agendamento")
        await db.commit()
        sps2 = (await db.execute(select(ScheduledPost).where(ScheduledPost.canal == "instagram"))).scalars().all()
        dias = Counter(s.data_agendada for s in sps2 if s.formato != "story" and s.data_agendada >= date(2026, 10, 18))
        print("antes:", dict(antes), "depois:", dict(Counter(s.formato for s in sps2)))
        print("dias com mais de 1 post:", sorted(str(d) for d, n in dias.items() if n > 1))


asyncio.run(main())
