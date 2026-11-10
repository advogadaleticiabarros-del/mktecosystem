"""Preenche os dois dias sem post no feed até 31/12 (25/11 e 09/12) com perguntas Manchete aprovadas, às 14h (regra
de feed em dia útil do agenda.py). NÃO APLICADO: depende do ok da Jessica (09/11/2026). Idempotente: pula dia ocupado
e peça já agendada.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/manchete/agendar_vagas.py [--aplicar]"""
import asyncio
import sys
from datetime import date

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost

# (dia da vaga, data da pauta da pergunta): aposentadoria da mulher 2026 (sem nenhuma peça no feed) e assédio moral
# (chamada para o carrossel de 10/12).
VAGAS = [(date(2026, 11, 25), date(2026, 11, 24)), (date(2026, 12, 9), date(2026, 12, 10))]


async def main(aplicar):
    async with SessionLocal() as db:
        for dia, pauta_dia in VAGAS:
            ocupado = (await db.execute(select(ScheduledPost).where(
                ScheduledPost.data_agendada == dia, ScheduledPost.canal == "instagram",
                ScheduledPost.formato.not_in(("story", "trial"))))).scalars().all()
            if ocupado:
                print(dia, "já ocupado:", [o.titulo for o in ocupado])
                continue
            p, pa = (await db.execute(select(ContentPiece, Pauta).join(Pauta, ContentPiece.pauta_id == Pauta.id).where(
                Pauta.data_editorial == pauta_dia, Pauta.angulo == "direitos", ContentPiece.tipo == "pergunta"))).one()
            ja = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == p.id))).scalar_one_or_none()
            if ja:
                print(dia, "peça já agendada em", ja.data_agendada)
                continue
            print(dia, "14:00", p.status, (p.corpo or {}).get("imagem", "")[-60:], "|", pa.titulo)
            if aplicar and p.status == "aprovado" and "manchete-" in (p.corpo or {}).get("imagem", ""):
                db.add(ScheduledPost(tenant_id=p.tenant_id, content_piece_id=p.id, titulo=pa.titulo, canal="instagram",
                                     formato="post", data_agendada=dia, horario="14:00", status="pronto"))
        if aplicar:
            await db.commit()
            print("agendado")


asyncio.run(main("--aplicar" in sys.argv))
