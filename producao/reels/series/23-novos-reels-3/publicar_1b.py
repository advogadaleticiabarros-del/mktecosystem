"""Roda DENTRO do container da API (20/11/2026): publica para os seguidores a versão 1B ("o que é o contrato
intermitente"), já no ar como Reels de teste desde 17/11. Pedido da Jessica: "Publique esse hoje" + "post você agora",
avisada do risco de vídeo repetido. Capa própria (capas_dra.py, "Com a Dra."), legenda e comentário de legendas.py.
Idempotente. Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s23/publicar_1b.py
"""
import asyncio
import sys
from datetime import datetime

from sqlalchemy import select

sys.path.insert(0, "/tmp/s23")
from legendas import LEGENDAS  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402
from app.models.scheduled_post import ScheduledPost  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402
from app.services.agendamento_horario import FUSO_PADRAO  # noqa: E402

TITULO = "Reels da Dra.: o que é o contrato intermitente (1/2)"


async def main():
    agora = datetime.now(FUSO_PADRAO)
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        if (await db.execute(select(ScheduledPost).where(ScheduledPost.titulo == TITULO, ScheduledPost.formato == "reels"))).scalars().first():
            print("já existe"); return
        leg = LEGENDAS[3]
        pauta = Pauta(tenant_id=tid, titulo=TITULO, angulo="reels", area="Trabalhista", origem="manual",
                      fonte="Gravação da Dra. Letícia (NOVOS REELS/3, série 23, versão 1B)", relevante_para_conteudo=True,
                      status="em_producao", data_editorial=agora.date())
        db.add(pauta)
        await db.flush()
        corpo = {"video": f"{settings.PUBLIC_API_URL}/media/o-que-e-o-intermitente-3.mp4?v=grade1",
                 "capa": f"{settings.PUBLIC_API_URL}/media/dra-capa-2026-11-20.jpg?v=1",
                 "legenda": leg["legenda"], "primeiro_comentario": leg["pc"], "rotulo_ia": False}
        peca = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="aprovado", versao=1, corpo=corpo)
        db.add(peca)
        await db.flush()
        db.add(ScheduledPost(tenant_id=tid, content_piece_id=peca.id, titulo=TITULO, canal="instagram", formato="reels",
                             data_agendada=agora.date(), horario=agora.strftime("%H:%M"), status="pronto"))
        await db.commit()
        print("agendado para agora:", agora.strftime("%d/%m %H:%M"))


asyncio.run(main())
