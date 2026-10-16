"""Roda DENTRO do container da API (16/10/2026). Pedido da Letícia: 1 publicação por dia no Instagram; em dia de Reels,
só o Reels, à noite. Horários pelo alcance real do perfil (12 meses): Reels 21h, feed 14h (seg a sex) e 11h (sáb e dom).

- Agendamentos do plano: nova data/hora (ScheduledPost + corpo.programacao); Reels voltam para "pronto".
- Reserva: peças aprovadas que não cabem em 1 por dia saem da agenda (o agendamento é apagado) e ficam com
  corpo.reserva {desde, motivo, programacao_antiga}. Continuam aprovadas, para usar depois.
- Frases aprovadas na revisão: texto novo em corpo.frase e imagem nova (?v=rev1610).
- Reels re-renderizados na área segura nova: corpo.video aponta para ?v=sz1.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/cal/aplicar_calendario_1610.py
"""
import asyncio
import json
import re
import uuid
from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost

D = json.load(open("/tmp/cal/aplicar.json", encoding="utf-8"))
MEDIA = f"{settings.PUBLIC_API_URL}/media"


def mexer(piece: ContentPiece, **campos) -> None:
    piece.corpo = {**(piece.corpo or {}), **campos}
    flag_modified(piece, "corpo")


async def main():
    async with SessionLocal() as db:
        n = {"agendados": 0, "reserva": 0, "frases": 0, "reels": 0}
        for item in D["plano"]:
            piece = await db.get(ContentPiece, uuid.UUID(item["piece"]))
            mexer(piece, programacao={"data": item["dia"], "hora": item["hora"]})
            if item["tipo"] == "reels" and piece.status == "publicado":
                piece.status = "aprovado"  # gestante 1/3: o post antigo foi excluído do Instagram
            if item.get("sp"):
                sp = await db.get(ScheduledPost, uuid.UUID(item["sp"]))
                sp.data_agendada, sp.horario = date.fromisoformat(item["dia"]), item["hora"]
                if sp.status in ("pausado", "publicado"):
                    sp.status = "pronto"
            n["agendados"] += 1
        for item in D["reserva"]:
            piece = await db.get(ContentPiece, uuid.UUID(item["piece"]))
            antiga = (piece.corpo or {}).get("programacao")
            corpo = {k: v for k, v in (piece.corpo or {}).items() if k != "programacao"}
            corpo["reserva"] = {"desde": "2026-10-16", "motivo": item["motivo"], "programacao_antiga": antiga}
            piece.corpo = corpo
            flag_modified(piece, "corpo")
            await db.execute(delete(ScheduledPost).where(ScheduledPost.id == uuid.UUID(item["sp"])))
            n["reserva"] += 1
        for pid, f in D["frases"].items():
            piece = await db.get(ContentPiece, uuid.UUID(pid))
            mexer(piece, frase=re.sub(r"<[^>]+>", "", f["html"]), imagem=f"{MEDIA}/{f['arquivo']}?v=rev1610",
                  frase_antiga=piece.corpo.get("frase"))
            n["frases"] += 1
        for pid, arquivo in D["reels_video"].items():
            piece = await db.get(ContentPiece, uuid.UUID(pid))
            mexer(piece, video=f"{MEDIA}/{arquivo}?v=sz1")
            n["reels"] += 1
        await db.commit()
        print(n)


asyncio.run(main())
