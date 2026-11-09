"""Sobe o Reels da calculadora do 13º (v3, aprovado pela Jessica em 09/11/2026) e programa para 09/11/2026 21h
(pedido: "postar hoje no horário em que os seguidores mais estão ativos"). Idempotente."""
import asyncio, json
from datetime import date
from sqlalchemy import select
from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost

LEG = json.load(open("/tmp/legenda-calc13.json", encoding="utf-8"))
NOME, DIA, HORA = "reels-bio-calculadora-13-v3", "2026-11-09", "21:00"
TITULO = "Reels: onde achar a calculadora do 13º no link da bio"

async def main():
    d = date.fromisoformat(DIA)
    async with SessionLocal() as db:
        modelo = (await db.execute(select(Pauta).where(Pauta.titulo.like("Reels:%")))).scalars().first()
        cols = [c.name for c in Pauta.__table__.columns if c.name not in ("id", "criado_em", "atualizado_em", "created_at", "updated_at")]
        pauta = (await db.execute(select(Pauta).where(Pauta.titulo == TITULO))).scalars().first()
        if not pauta:
            pauta = Pauta(**{c: getattr(modelo, c) for c in cols}); pauta.titulo = TITULO; pauta.data_editorial = d
            db.add(pauta); await db.flush()
        pauta.status = "em_producao"
        p = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == "reels"))).scalars().first()
        if not p:
            p = ContentPiece(tenant_id=pauta.tenant_id, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=1, corpo={})
            db.add(p); await db.flush()
        p.corpo = {"video": f"{settings.PUBLIC_API_URL}/media/{NOME}.mp4?v=v1", "legenda": LEG["legenda"],
                   "primeiro_comentario": LEG["primeiro_comentario"], "programacao": {"data": DIA, "hora": HORA}, "rotulo_ia": False}
        choque = (await db.execute(select(ScheduledPost).where(ScheduledPost.tenant_id == p.tenant_id, ScheduledPost.canal == "instagram",
                  ScheduledPost.data_agendada == d, ScheduledPost.horario == HORA, ScheduledPost.status != "cancelado",
                  ScheduledPost.content_piece_id != p.id))).scalars().first()
        if choque:
            print("CHOQUE", DIA, HORA, choque.titulo, choque.status); return
        sp = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == p.id))).scalar_one_or_none()
        if sp is None:
            db.add(ScheduledPost(tenant_id=p.tenant_id, content_piece_id=p.id, titulo="Reels calculadora do 13º no link da bio",
                                 canal="instagram", formato="reels", data_agendada=d, horario=HORA, status="pronto"))
        p.status = "aprovado"
        await db.commit()
        print("programado", DIA, HORA, "peça", p.id, "pauta", pauta.id)

asyncio.run(main())
