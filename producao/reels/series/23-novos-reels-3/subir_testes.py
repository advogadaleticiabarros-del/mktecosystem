"""Roda DENTRO do container da API (17/11/2026): as 4 versões da série 23 como Reels de teste (Trial Reels).
Pedido da Jessica: "em primeiro momento, vamos postar no Reels teste, todos, e depois vamos escolher 2 ou 3 para postar
na grade; é um assunto extremamente relevante nesse momento".
Graduação MANUAL: a Meta mostra só a quem não segue e não leva o teste aos seguidores; o post da grade sai depois como
peça nova (como na série 19). Trial não ocupa o dia do feed (agenda.py). Capa: quadro do gancho (capa_ms padrão).
Idempotente: não duplica se o vídeo já estiver numa peça de teste.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s23/subir_testes.py
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

DIA = date(2026, 11, 17)
TESTES = [  # (n da legenda, arquivo, horário de Brasília)
    (3, "o-que-e-o-intermitente-3.mp4", "09:30"),
    (4, "intermitente-estudo-de-caso-4.mp4", "11:30"),
    (1, "intermitente-13-na-diaria-1.mp4", "14:30"),
    (2, "intermitente-de-fachada-2.mp4", "16:30"),
]


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        for n, arquivo, hora in TESTES:
            leg = LEGENDAS[n]
            titulo = f"Teste · {leg['titulo']}"
            video = f"{settings.PUBLIC_API_URL}/media/{arquivo}?v=1"
            pauta = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == titulo))).scalars().first()
            if not pauta:
                pauta = Pauta(tenant_id=tid, titulo=titulo, angulo="reels", area="Trabalhista", origem="manual",
                              fonte="Gravação da Dra. Letícia (NOVOS REELS/3, série 23)", relevante_para_conteudo=True,
                              status="em_producao", data_editorial=DIA)
                db.add(pauta)
                await db.flush()
            pecas = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id))).scalars().all()
            if any((p.corpo or {}).get("video") == video and (p.corpo or {}).get("trial_reels") for p in pecas):
                print("já existe:", arquivo)
                continue
            corpo = {"video": video, "legenda": leg["legenda"], "primeiro_comentario": leg["pc"],
                     "trial_reels": True, "trial_graduacao": "MANUAL"}
            peca = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="aprovado", versao=1, corpo=corpo)
            db.add(peca)
            await db.flush()
            db.add(ScheduledPost(tenant_id=tid, content_piece_id=peca.id, titulo=titulo, canal="instagram",
                                 formato="trial", data_agendada=DIA, horario=hora, status="pronto"))
            print("agendado teste:", arquivo, DIA, hora)
        await db.commit()


asyncio.run(main())
