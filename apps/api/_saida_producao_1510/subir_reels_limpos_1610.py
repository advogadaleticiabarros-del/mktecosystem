"""Roda DENTRO do container da API (16/10/2026). Reels refeitos no visual limpo (pedido da Letícia: sem pontos
dourados, profissional e moderno; Guarda com vídeos do banco nas cenas sem a Dra.; voz com redução de ruído).
- corpo.video de cada Reels aponta para o arquivo novo (?v=limpo1).
- A série Guarda estava em "ajuste" com o mesmo pedido: volta para "rascunho" (Para aprovar), com o pedido
  guardado em corpo.pedido_atendido.
Os agendamentos continuam pausados até ela aprovar a versão nova.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/limpos/subir_reels_limpos_1610.py
"""
import asyncio
import uuid

from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece

VIDEOS = {
    "f2bbd91f-": "gestante-reel-1.mp4", "0ae3b688-": "gestante-reel-2.mp4", "fcfde221-": "gestante-reel-3.mp4",
    "b5eae141-": "13-sem-susto-reel-1.mp4", "bba0e4a6-": "13-sem-susto-reel-2.mp4", "030d1f33-": "13-sem-susto-reel-3.mp4",
    "a6f71007-": "13-proporcional-calculo.mp4", "d07b5a50-": "gestante-insalubridade-1.mp4",
    "ad082540-": "gestante-insalubridade-2.mp4", "c8cde84e-": "gestante-insalubridade-3.mp4",
    "6ecf1d22-": "pensao-mito-30.mp4", "2ab545a9-": "13-quatro-regras.mp4",
    "edf05653-": "guarda-compartilhada-1.mp4", "6cfb0f26-": "guarda-compartilhada-2.mp4", "196a4767-": "guarda-compartilhada-3.mp4",
}


async def main():
    async with SessionLocal() as db:
        from sqlalchemy import select
        pecas = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars().all()
        n = 0
        for p in pecas:
            arq = next((v for k, v in VIDEOS.items() if str(p.id).startswith(k)), None)
            if not arq:
                continue
            corpo = {**(p.corpo or {}), "video": f"{settings.PUBLIC_API_URL}/media/{arq}?v=limpo1"}
            if p.status == "ajuste":
                corpo["pedido_atendido"] = corpo.pop("pedido_alteracao", None)
                p.status = "rascunho"
            p.corpo = corpo
            flag_modified(p, "corpo")
            n += 1
        await db.commit()
        print("reels atualizados:", n)


asyncio.run(main())
