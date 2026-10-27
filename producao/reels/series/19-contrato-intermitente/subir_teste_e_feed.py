"""Roda DENTRO do container da API (27/10/2026): R1 da série 19, estilo tela dividida (v3), em duas postagens separadas.
Pedido da Jessica: "poste esse no Reels de teste, vamos ver o desempenho; performando bem, amanhã no melhor horário
você vai postar também no feed comum (não vai converter teste para feed, vai postar novamente)".
- Peça 1: Trial Reels com graduação MANUAL (a Meta não leva o teste aos seguidores), agendada para HOJE no horário dado.
- Peça 2: Reels comum (seguidores), 28/10/2026 21:00 (melhor horário de Reels pelo alcance de 12 meses). Quarta-feira:
  fora da regra terça/sexta, por pedido explícito dela. Cancelar se o teste for mal.
Idempotente: não duplica se o vídeo já estiver numa peça com o mesmo modo.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/s19/subir_teste_e_feed.py HH:MM
"""
import asyncio
import sys
from datetime import date

from sqlalchemy import select

sys.path.insert(0, "/tmp/s19")
from legendas import LEGENDAS  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402
from app.models.scheduled_post import ScheduledPost  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402
from app.services.agendamento_horario import hoje_brasilia  # noqa: E402

ARQUIVO = "contrato-intermitente-dividida-v3-1.mp4"
FEED = (date(2026, 10, 28), "21:00")


async def main(horario_teste: str):
    leg = LEGENDAS[1]
    video = f"{settings.PUBLIC_API_URL}/media/{ARQUIVO}?v=1"
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        pauta = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == leg["titulo"]))).scalars().first()
        if not pauta:
            pauta = Pauta(tenant_id=tid, titulo=leg["titulo"], angulo="reels", area="Trabalhista", origem="manual",
                          fonte="Gravação da Dra. Letícia (NOVOS REELS/VIDEO 1, 26/10/2026)", relevante_para_conteudo=True,
                          status="em_producao", data_editorial=date(2026, 10, 27))
            db.add(pauta)
            await db.flush()
        pecas = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id))).scalars().all()
        base = {"video": video, "legenda": leg["legenda"], "primeiro_comentario": leg["pc"]}
        planos = [("trial", {**base, "trial_reels": True, "trial_graduacao": "MANUAL"}, (hoje_brasilia(), horario_teste)),
                  ("reels", base, FEED)]
        for versao, (formato, corpo, (dia, hora)) in enumerate(planos, start=1):
            if any((p.corpo or {}).get("video") == video and bool((p.corpo or {}).get("trial_reels")) == (formato == "trial")
                   for p in pecas):
                print("já existe:", formato)
                continue
            peca = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="aprovado", versao=versao, corpo=corpo)
            db.add(peca)
            await db.flush()
            db.add(ScheduledPost(tenant_id=tid, content_piece_id=peca.id, titulo=leg["titulo"], canal="instagram",
                                 formato=formato, data_agendada=dia, horario=hora, status="pronto"))
            print("agendado:", formato, dia, hora)
        await db.commit()


asyncio.run(main(sys.argv[1]))
