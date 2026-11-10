"""So leitura: lista o calendario a partir de 09/11/2026 e as pecas aprovadas sem agendamento. Roda no container."""
import asyncio
from datetime import date
from collections import Counter
from sqlalchemy import select
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost

async def main():
    async with SessionLocal() as db:
        ags = (await db.execute(select(ScheduledPost, ContentPiece).outerjoin(ContentPiece, ScheduledPost.content_piece_id == ContentPiece.id)
               .where(ScheduledPost.data_agendada >= date(2026,11,9)).order_by(ScheduledPost.data_agendada, ScheduledPost.horario))).all()
        for a, p in ags:
            img = str(((p.corpo or {}) if p else {}).get("imagem",""))
            print(a.data_agendada, a.data_agendada.strftime("%a"), a.horario, a.canal[:4], a.formato[:8], (p.tipo if p else "-")[:9], a.status, "MANCHETE" if "manchete-" in img else "", a.titulo[:45])
        print("ultimo:", ags[-1][0].data_agendada if ags else None)
        # pecas aprovadas sem agendamento
        sub = select(ScheduledPost.content_piece_id).where(ScheduledPost.content_piece_id.is_not(None))
        livres = (await db.execute(select(ContentPiece).where(ContentPiece.status=="aprovado", ContentPiece.id.not_in(sub)))).scalars().all()
        print("aprovadas sem agendamento:", Counter(p.tipo for p in livres))
asyncio.run(main())
