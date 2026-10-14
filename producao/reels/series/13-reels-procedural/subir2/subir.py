"""Sobe os 6 Reels extras, aprova e programa (pedido da Letícia em 10/10/2026: "Pode produzir todos e programar"). Idempotente."""
import asyncio, json
from datetime import date
from sqlalchemy import select
from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
LEG = json.load(open("/tmp/subir2/legendas.json", encoding="utf-8"))
M = f"{settings.PUBLIC_API_URL}/media"
REELS = [  # nome, data, título da pauta, título do agendamento
    ("gestante-insalubridade-1", "2026-11-10", "Série de Reels: Gestante e insalubridade (1/3)", "Reels 1/3 gestante e insalubridade"),
    ("gestante-insalubridade-2", "2026-11-12", "Série de Reels: Gestante e insalubridade (2/3)", "Reels 2/3 gestante e insalubridade"),
    ("gestante-insalubridade-3", "2026-11-14", "Série de Reels: Gestante e insalubridade (3/3)", "Reels 3/3 gestante e insalubridade"),
    ("13-proporcional-calculo", "2026-11-09", "Reels: como calcular o 13º proporcional", "Reels 13º proporcional (cálculo)"),
    ("pensao-mito-30", "2026-11-16", "Reels: pensão não é sempre 30%", "Reels pensão: mito dos 30%"),
    ("13-quatro-regras", "2026-11-29", "Reels: as 4 regras do 13º", "Reels 13º: as 4 regras"),
]
async def main():
    async with SessionLocal() as db:
        base = (await db.execute(select(Pauta).where(Pauta.titulo.like("Série de Reels: Depois do parto%")))).scalars().first()
        modelo = base or (await db.execute(select(Pauta).where(Pauta.titulo.like("Série de Reels: 13º sem susto%")))).scalars().first()
        cols = [c.name for c in Pauta.__table__.columns if c.name not in ("id", "criado_em", "atualizado_em", "created_at", "updated_at")]
        for nome, dia, titulo, tit_sp in REELS:
            d = date.fromisoformat(dia)
            pauta = (await db.execute(select(Pauta).where(Pauta.titulo == titulo))).scalars().first()
            if not pauta and nome.endswith("insalubridade-1") and base:
                pauta = base; pauta.titulo = titulo  # a série substitui "Depois do parto" no mesmo dia
            if not pauta:
                pauta = Pauta(**{c: getattr(modelo, c) for c in cols}); pauta.titulo = titulo; pauta.data_editorial = d
                db.add(pauta); await db.flush()
            pauta.status = "em_producao"
            p = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == "reels"))).scalars().first()
            if not p:
                p = ContentPiece(tenant_id=pauta.tenant_id, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=1, corpo={})
                db.add(p); await db.flush()
            p.corpo = {"video": f"{M}/{nome}.mp4?v=v1", "video_sem_musica": f"{M}/{nome}-sem-musica.mp4?v=v1",
                       "legenda": LEG[nome]["legenda"], "primeiro_comentario": LEG[nome]["primeiro_comentario"],
                       "programacao": {"data": dia, "hora": "20:30"}, "rotulo_ia": True}
            choque = (await db.execute(select(ScheduledPost).where(ScheduledPost.tenant_id == p.tenant_id, ScheduledPost.canal == "instagram",
                      ScheduledPost.data_agendada == d, ScheduledPost.horario == "20:30", ScheduledPost.status != "cancelado",
                      ScheduledPost.content_piece_id != p.id))).scalars().first()
            if choque:
                print("CHOQUE", dia, choque.titulo); continue
            sp = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == p.id))).scalar_one_or_none()
            if sp is None:
                db.add(ScheduledPost(tenant_id=p.tenant_id, content_piece_id=p.id, titulo=tit_sp, canal="instagram", formato="reels",
                                     data_agendada=d, horario="20:30", status="pronto"))
            p.status = "aprovado"
            print("programado", dia, "20:30", nome)
        await db.commit()
asyncio.run(main())
