"""Roda DENTRO do container da API (16/10/2026). A Letícia aprovou os 6 artigos de atualidade ("pode publicar todos").
- Atualiza o texto a partir de artigos_out.py (6x1 promulgada em 16/10; "Atualizado em 16 de outubro").
- Aprova e agenda no blog para hoje, a partir de agora + 5 min, com 10 min entre um e outro. O publicador do blog
  (job a cada 5 min) sobe por SFTP.
- Os Stories de cada artigo passam para hoje, 20 min depois do artigo (são postados à mão no app).
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/artigos/publicar_artigos_1610.py
"""
import asyncio
import sys
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

sys.path.insert(0, "/tmp/artigos")
from artigos_out import ARTIGOS  # noqa: E402

from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.scheduled_post import ScheduledPost  # noqa: E402
from app.services.agenda import agendar_conteudo_aprovado  # noqa: E402

BRASILIA = timezone(timedelta(hours=-3))


async def main():
    agora = datetime.now(BRASILIA) + timedelta(minutes=5)
    async with SessionLocal() as db:
        artigos = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "artigo"))).scalars().all()
        stories = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "stories"))).scalars().all()
        for i, a in enumerate(ARTIGOS):
            quando = agora + timedelta(minutes=10 * i)
            dia, hora = quando.date().isoformat(), quando.strftime("%H:%M")
            piece = next(p for p in artigos if (p.corpo or {}).get("slug") == a["slug"])
            piece.corpo = {**piece.corpo, "titulo": a["titulo"], "html": a["html"], "meta_description": a["meta"],
                           "resumo": a["resumo"], "programacao": {"data": dia, "hora": hora},
                           "legenda": "Post para o Perfil da Empresa no Google (Adicionar atualização):\n\n" + a["post_google"]}
            flag_modified(piece, "corpo")
            piece.status = "aprovado"
            await db.flush()
            sp = await agendar_conteudo_aprovado(db, piece)
            print("artigo", a["slug"], dia, hora, "agendado" if sp else "já tinha agendamento")
            story = next((s for s in stories if (s.corpo or {}).get("link", "").endswith(f"{a['slug']}.html")), None)
            if story:
                h2 = (quando + timedelta(minutes=20)).strftime("%H:%M")
                story.corpo = {**story.corpo, "programacao": {"data": dia, "hora": h2}}
                flag_modified(story, "corpo")
                ssp = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == story.id))).scalars().first()
                if ssp:
                    ssp.data_agendada, ssp.horario = quando.date(), h2
        await db.commit()


asyncio.run(main())
