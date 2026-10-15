"""Lista as peças com ajuste pedido pela Letícia (status "ajuste") para o Claude refazer.
Uso na VPS: docker compose exec -T -e PYTHONPATH=/app api python /tmp/pedidos_ajuste.py
"""
import asyncio

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta


async def main():
    async with SessionLocal() as db:
        linhas = (await db.execute(
            select(ContentPiece, Pauta).join(Pauta, Pauta.id == ContentPiece.pauta_id).where(ContentPiece.status == "ajuste")
        )).all()
        if not linhas:
            print("NENHUM_PEDIDO")
            return
        for c, p in linhas:
            corpo = c.corpo or {}
            pedido = corpo.get("pedido_alteracao") or {}
            prog = corpo.get("programacao") or {}
            midia = corpo.get("video") or corpo.get("imagem") or (corpo.get("imagens") or [""])[0] or corpo.get("imagem_capa", "")
            print(f"PECA {c.id} | tipo={c.tipo} | pauta={p.titulo} | data={prog.get('data')} {prog.get('hora')} | "
                  f"pedido_em={pedido.get('em')} | midia={midia}\n  PEDIDO: {pedido.get('texto')}")


asyncio.run(main())
