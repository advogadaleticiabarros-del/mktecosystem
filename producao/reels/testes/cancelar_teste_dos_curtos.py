"""Roda DENTRO do container da API (18/11/2026): desfaz o teste_dos_curtos.py. Pedido da Jessica: "se existe esse risco
cancele" (o mesmo vídeo duas vezes no mesmo dia pode ser tratado como repetido). Apaga só as cópias de teste ainda não
publicadas (agendamento formato trial + peça com corpo.teste_de); o Reels normal das 19h não é tocado."""
import asyncio
from sqlalchemy import select
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost


async def main():
    async with SessionLocal() as db:
        linhas = (await db.execute(select(ScheduledPost, ContentPiece)
                  .join(ContentPiece, ContentPiece.id == ScheduledPost.content_piece_id)
                  .where(ScheduledPost.formato == "trial"))).all()
        apagados = 0
        for sp, p in linhas:
            if not (p.corpo or {}).get("teste_de"):
                continue
            if sp.status != "pronto":
                print("NÃO apagado (status", sp.status, "):", sp.titulo, sp.data_agendada, sp.horario); continue
            await db.delete(sp); await db.flush(); await db.delete(p)
            apagados += 1
        await db.commit()
        print("apagados:", apagados)

asyncio.run(main())
