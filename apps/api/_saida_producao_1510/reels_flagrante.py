"""Roda DENTRO do container da API: troca os 13 Reels antigos de terça e sexta (21h) pelos Reels Flagrante aprovados,
com a capa textura (pedido da Jessica em 10/11/2026: "Quero tudo nos formatos novos" ... "Pode aplicar").

Para cada item de reels_flagrante.json:
- cria uma pauta e uma peça reels nova, aprovada (corpo.video, capa, legenda, primeiro_comentario);
- o agendamento de terça/sexta 21h daquele dia passa a apontar para a peça nova (mesmo dia, mesma hora);
- a peça antiga sai da agenda e vai para a reserva (corpo.reserva), sem ser apagada. Publicado não é tocado.
Idempotente: pula o dia cujo agendamento já aponta para o vídeo Flagrante.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/flagrante/reels_flagrante.py [--aplicar]"""
import asyncio
import json
import sys
from datetime import date
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost

AQUI = Path(__file__).resolve().parent
MIDIA = Path("/app/media")
V = "flag1"


async def main(aplicar):
    itens = json.loads((AQUI / "reels_flagrante.json").read_text(encoding="utf-8"))
    async with SessionLocal() as db:
        for t in itens:
            dia = date.fromisoformat(t["dia"])
            faltam = [a for a in (t["video"], t["capa"]) if not (MIDIA / a).exists()]
            if faltam:
                print(t["dia"], "SEM ARQUIVO em /app/media:", faltam)
                continue
            url_video = f"{settings.PUBLIC_API_URL}/media/{t['video']}?v={V}"
            url_capa = f"{settings.PUBLIC_API_URL}/media/{t['capa']}?v={V}"
            ags = (await db.execute(select(ScheduledPost, ContentPiece).join(
                ContentPiece, ScheduledPost.content_piece_id == ContentPiece.id).where(
                ScheduledPost.data_agendada == dia, ScheduledPost.formato == "reels",
                ScheduledPost.horario == "21:00"))).all()
            if len(ags) != 1:
                print(t["dia"], f"{len(ags)} Reels às 21h nesse dia, nada feito")
                continue
            ag, antiga = ags[0]
            if (antiga.corpo or {}).get("video") == url_video:
                print(t["dia"], "já trocado")
                continue
            if ag.status != "pronto" or antiga.status == "publicado":
                print(t["dia"], f"agendamento {ag.status} / peça {antiga.status}: mantido")
                continue
            print(f"{t['dia']} 21:00 | {ag.titulo[:45]} -> Flagrante: {t['tema']}")
            if not aplicar:
                continue
            pauta = Pauta(tenant_id=antiga.tenant_id, titulo=f"Reels Flagrante: {t['tema']}", angulo="reels",
                          area=t["area"], origem="manual", fonte="Flagrante (producao/estilos/papel-e-ouro/motion-diario)",
                          relevante_para_conteudo=True, status="em_producao", data_editorial=dia)
            db.add(pauta)
            await db.flush()
            nova = ContentPiece(tenant_id=antiga.tenant_id, pauta_id=pauta.id, tipo="reels", status="aprovado", corpo={
                "video": url_video, "capa": url_capa, "legenda": t["legenda"],
                "primeiro_comentario": t["primeiro_comentario"], "rotulo_ia": False, "estilo": "flagrante",
                "episodio": t["ep"], "programacao": {"data": t["dia"], "hora": "21:00"}})
            db.add(nova)
            await db.flush()
            corpo = {k: v for k, v in (antiga.corpo or {}).items() if k != "programacao"}
            corpo["reserva"] = {"desde": "2026-11-10", "motivo": "trocado pelo Reels Flagrante " + t["ep"],
                                "programacao_antiga": {"data": t["dia"], "hora": "21:00"}}
            antiga.corpo = corpo
            flag_modified(antiga, "corpo")
            ag.content_piece_id = nova.id
            ag.titulo = pauta.titulo
        if aplicar:
            await db.commit()
            print("aplicado")


asyncio.run(main("--aplicar" in sys.argv))
