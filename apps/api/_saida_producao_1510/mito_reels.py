"""Roda DENTRO do container da API: troca a série Mito ou Lei (estático 19h nos dias pares) pelos Reels motion
(pedido da Jessica em 10/11/2026: "trocar todos dessa serie para reels nesse mesmo estilo"; dias "segunda, quarta e
sábado às 19h", que não têm Reels).

Para cada tema de mito_reels.json:
- cria uma peça nova tipo reels na mesma pauta (corpo.video, legenda, primeiro_comentario), aprovada;
- agenda essa peça no novo dia às 19h (formato reels);
- o estático antigo sai da agenda e vai para a reserva (corpo.reserva), sem ser apagado. Publicado não é tocado.
Idempotente (pula tema que já tem peça reels com o mesmo vídeo).

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/mitoreels/mito_reels.py [--aplicar]"""
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
V = "mito1"


async def main(aplicar):
    temas = json.loads((AQUI / "mito_reels.json").read_text(encoding="utf-8"))
    async with SessionLocal() as db:
        for t in temas:
            tema, novo = date.fromisoformat(t["tema"]), date.fromisoformat(t["dia"])
            if aplicar and not (MIDIA / t["video"]).exists():
                print(t["tema"], "SEM VÍDEO em /app/media:", t["video"])
                continue
            linhas = (await db.execute(select(ContentPiece, Pauta).join(Pauta, ContentPiece.pauta_id == Pauta.id).where(
                Pauta.data_editorial == tema, Pauta.angulo == "mito"))).all()
            est = [(p, pa) for p, pa in linhas if p.tipo == "estatico"]
            url = f"{settings.PUBLIC_API_URL}/media/{t['video']}?v={V}"
            if any(p.tipo == "reels" and (p.corpo or {}).get("video") == url for p, _ in linhas):
                print(t["tema"], "já trocado")
                continue
            if len(est) != 1:
                print(t["tema"], f"{len(est)} estáticos encontrados, nada feito")
                continue
            e, pauta = est[0]
            if e.status == "publicado":
                print(t["tema"], "estático já publicado, mantido")
                continue
            sp_antigos = (await db.execute(select(ScheduledPost).where(
                ScheduledPost.content_piece_id == e.id))).scalars().all()
            print(f"{t['tema']} -> {t['dia']} 19:00 reels | {pauta.titulo[:50]} | agenda antiga: "
                  f"{[(str(s.data_agendada), s.horario, s.status) for s in sp_antigos]}")
            if not aplicar:
                continue
            for s in sp_antigos:
                if s.status not in ("publicado", "publicando"):
                    await db.delete(s)
            corpo = {k: v for k, v in (e.corpo or {}).items() if k != "programacao"}
            corpo["reserva"] = {"desde": "2026-11-10", "motivo": "série Mito ou Lei virou Reels",
                                "programacao_antiga": (e.corpo or {}).get("programacao")}
            e.corpo = corpo
            flag_modified(e, "corpo")
            r = ContentPiece(tenant_id=e.tenant_id, pauta_id=e.pauta_id, tipo="reels", status="aprovado", corpo={
                "video": url, "legenda": t["legenda"], "primeiro_comentario": t["primeiro_comentario"],
                "capa_ms": 9000, "rotulo_ia": False, "estilo": "flagrante-mito-ou-lei",
                "programacao": {"data": t["dia"], "hora": "19:00"}})
            db.add(r)
            await db.flush()
            db.add(ScheduledPost(tenant_id=e.tenant_id, content_piece_id=r.id, titulo=pauta.titulo, canal="instagram",
                                 formato="reels", data_agendada=novo, horario="19:00", status="pronto"))
        if aplicar:
            await db.commit()
            print("aplicado")


asyncio.run(main("--aplicar" in sys.argv))
