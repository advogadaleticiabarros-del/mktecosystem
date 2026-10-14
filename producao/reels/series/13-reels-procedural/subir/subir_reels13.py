"""Sobe a série de Reels "13º sem susto" como RASCUNHO (Letícia aprova em Revisar e aprovar). Idempotente."""
import asyncio, json
from datetime import date
from sqlalchemy import select
from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
LEG = json.load(open("/tmp/reels13_legendas.json", encoding="utf-8"))
DATAS = {1: "2026-11-03", 2: "2026-11-05", 3: "2026-11-07"}
M = f"{settings.PUBLIC_API_URL}/media"
async def main():
    async with SessionLocal() as db:
        base = (await db.execute(select(Pauta).where(Pauta.titulo.like("Série de Reels: 13º sem susto%")))).scalars().first()
        cols = [c.name for c in Pauta.__table__.columns if c.name not in ("id", "criado_em", "atualizado_em", "created_at", "updated_at")]
        for n in (1, 2, 3):
            d = date.fromisoformat(DATAS[n])
            if n == 1:
                pauta = base
            else:
                titulo = f"Série de Reels: 13º sem susto ({n}/3)"
                pauta = (await db.execute(select(Pauta).where(Pauta.titulo == titulo))).scalars().first()
                if not pauta:
                    pauta = Pauta(**{c: getattr(base, c) for c in cols}); pauta.titulo = titulo; pauta.data_editorial = d
                    db.add(pauta); await db.flush()
            pauta.status = "em_producao"
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == "reels"))).scalars().first()
            if ja:
                print("já existe", n); continue
            db.add(ContentPiece(tenant_id=pauta.tenant_id, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=1, corpo={
                "video": f"{M}/13-sem-susto-reel-{n}.mp4?v=v2", "video_sem_musica": f"{M}/13-sem-susto-reel-{n}-sem-musica.mp4?v=v2",
                "legenda": LEG[str(n)]["legenda"], "primeiro_comentario": LEG[str(n)]["primeiro_comentario"],
                "programacao": {"data": DATAS[n], "hora": "20:30"}, "rotulo_ia": True}))
            print("rascunho criado", n, DATAS[n])
        await db.commit()
asyncio.run(main())
