"""Roda DENTRO do container da API (20/11/2026): agenda para os seguidores as duas versões do vídeo 2 da série 23.
Pedido da Jessica: 2B ("estudo de caso, o intermitente de todo dia") "para amanhã, mesmo horário" do 1B (publicado em
20/11 às 19h31) e 2A ("intermitente de fachada") "no domingo" (horário da Dra., 15h30). Capas de capas_dra.py.
Idempotente. Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s23/agendar_parte2.py
"""
import asyncio
import sys
from datetime import date

from sqlalchemy import select

sys.path.insert(0, "/tmp/s23")
from legendas import LEGENDAS  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402
from app.models.scheduled_post import ScheduledPost  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402

ITENS = [  # (n da legenda, vídeo, capa, dia, hora)
    (4, "intermitente-estudo-de-caso-4.mp4", "dra-capa-2026-11-21.jpg", date(2026, 11, 21), "19:30"),
    (2, "intermitente-de-fachada-2.mp4", "dra-capa-2026-11-22-intermitente.jpg", date(2026, 11, 22), "15:30"),
]


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        for n, video, capa, dia, hora in ITENS:
            leg = LEGENDAS[n]
            titulo = leg["titulo"]
            if (await db.execute(select(ScheduledPost).where(ScheduledPost.titulo == titulo, ScheduledPost.formato == "reels"))).scalars().first():
                print("já existe:", titulo); continue
            pauta = Pauta(tenant_id=tid, titulo=titulo, angulo="reels", area="Trabalhista", origem="manual",
                          fonte="Gravação da Dra. Letícia (NOVOS REELS/3, série 23)", relevante_para_conteudo=True,
                          status="em_producao", data_editorial=dia)
            db.add(pauta)
            await db.flush()
            corpo = {"video": f"{settings.PUBLIC_API_URL}/media/{video}?v=grade1",
                     "capa": f"{settings.PUBLIC_API_URL}/media/{capa}?v=1",
                     "legenda": leg["legenda"], "primeiro_comentario": leg["pc"], "rotulo_ia": False}
            peca = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="aprovado", versao=1, corpo=corpo)
            db.add(peca)
            await db.flush()
            db.add(ScheduledPost(tenant_id=tid, content_piece_id=peca.id, titulo=titulo, canal="instagram",
                                 formato="reels", data_agendada=dia, horario=hora, status="pronto"))
            print("agendado:", dia, hora, titulo)
        await db.commit()


asyncio.run(main())
