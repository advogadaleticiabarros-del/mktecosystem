"""Roda DENTRO do container da API (16/10/2026). Pedido da Letícia: todos os Reels distribuídos até 15/11, 13º em
novembro, cada tema no dia mais propício, pelos dados do perfil (melhor dia terça, depois quarta/sexta/quinta;
sábado e domingo fracos; Reels às 21h) e pela pesquisa (busca por 13º tem pico na semana de 6 a 12/11).
- Reels só em dia útil, às 21h; séries em dias alternados; 13º entre 4 e 12/11.
- Post do feed que estava num dia que virou de Reels muda para um dia que deixou de ser de Reels (mesmo prazo do
  tema); o Mito da mamografia (Outubro Rosa) fica sem vaga em outubro e vai para a reserva, sem ser apagado.
- O Reels novo "5 coisas que a empresa não pode fazer com a gestante" é aprovado e entra em 19/10.
Feed: 14h de segunda a sexta, 11h no sábado e no domingo. Mostra a contagem antes e depois.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/agenda1511/reels_ate_1511.py
"""
import asyncio
from collections import Counter
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.services.agenda import agendar_conteudo_aprovado, horario_instagram

D = date.fromisoformat
REELS = {  # trecho do nome do vídeo: novo dia
    "gestante-5-coisas": "2026-10-19", "gestante-reel-1": "2026-10-20", "guarda-compartilhada-1": "2026-10-21",
    "gestante-reel-2": "2026-10-22", "guarda-compartilhada-2": "2026-10-23", "gestante-reel-3": "2026-10-26",
    "guarda-compartilhada-3": "2026-10-27", "gestante-insalubridade-1": "2026-10-28", "gestante-insalubridade-2": "2026-10-30",
    "gestante-insalubridade-3": "2026-11-02", "pensao-mito-30": "2026-11-03", "13-sem-susto-reel-1": "2026-11-04",
    "13-sem-susto-reel-2": "2026-11-06", "13-sem-susto-reel-3": "2026-11-09", "13-proporcional-calculo": "2026-11-10",
    "13-quatro-regras": "2026-11-12",
}
FEED = {  # dia atual do post do feed: novo dia (None = reserva)
    "2026-10-20": "2026-10-17", "2026-10-22": "2026-10-25", "2026-10-26": "2026-11-29", "2026-10-28": "2026-11-05",
    "2026-10-30": None, "2026-11-02": "2026-11-13", "2026-11-04": "2026-11-11", "2026-11-06": "2026-11-15",
    "2026-11-10": "2026-11-07", "2026-11-12": "2026-11-23",
}


def programar(piece, dia, hora):
    piece.corpo = {**(piece.corpo or {}), "programacao": {"data": dia, "hora": hora}}
    flag_modified(piece, "corpo")


async def main():
    async with SessionLocal() as db:
        sps = (await db.execute(select(ScheduledPost).where(ScheduledPost.canal == "instagram"))).scalars().all()
        antes = Counter(s.formato for s in sps)
        pecas = {p.id: p for p in (await db.execute(select(ContentPiece))).scalars().all()}
        # feed primeiro (pelo dia atual, antes de os Reels ocuparem os dias)
        for s in [s for s in sps if s.formato != "reels" and s.formato != "story" and str(s.data_agendada) in FEED]:
            novo = FEED[str(s.data_agendada)]
            p = pecas[s.content_piece_id]
            if novo is None:
                corpo = {k: v for k, v in (p.corpo or {}).items() if k != "programacao"}
                corpo["reserva"] = {"desde": "2026-10-16", "motivo": "Reels até 15/11 (sem vaga no tema)",
                                    "programacao_antiga": (p.corpo or {}).get("programacao")}
                p.corpo = corpo
                flag_modified(p, "corpo")
                await db.delete(s)
                print("feed para a reserva:", s.data_agendada, p.tipo)
                continue
            s.data_agendada, s.horario = D(novo), horario_instagram(p.tipo, D(novo))
            programar(p, novo, s.horario)
            print("feed:", p.tipo, "->", novo, s.horario)
        await db.flush()
        for p in pecas.values():
            if p.tipo != "reels" or not (p.corpo or {}).get("video"):
                continue
            chave = next((k for k in REELS if f"/{k}" in p.corpo["video"]), None)
            if not chave:
                continue
            dia = REELS[chave]
            programar(p, dia, "21:00")
            s = next((x for x in sps if x.content_piece_id == p.id), None)
            if s is None and p.status == "rascunho":
                p.status = "aprovado"
                await db.flush()
                s = await agendar_conteudo_aprovado(db, p)
            if s is not None:
                s.data_agendada, s.horario = D(dia), "21:00"
                if s.status == "pausado":
                    s.status = "pronto"
            print("reels:", chave, "->", dia)
        await db.commit()
        sps2 = (await db.execute(select(ScheduledPost).where(ScheduledPost.canal == "instagram"))).scalars().all()
        dias = Counter(s.data_agendada for s in sps2 if s.formato != "story" and s.data_agendada >= D("2026-10-17"))
        print("antes:", dict(antes), "depois:", dict(Counter(s.formato for s in sps2)))
        print("dias com mais de 1 post:", sorted(str(d) for d, n in dias.items() if n > 1))
        print("dias vazios até 31/12:", sorted(str(d) for d in (D("2026-10-17") + __import__("datetime").timedelta(i) for i in range(76)) if d not in dias))


asyncio.run(main())
