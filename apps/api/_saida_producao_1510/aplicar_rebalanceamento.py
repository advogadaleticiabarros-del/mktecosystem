"""Roda DENTRO do container da API: aplica rebalancear_jan_fev.json (de rebalancear_jan_fev.py).
- "mover": acha a peça agendada pelo nome do arquivo da arte (corpo.imagem) entre 01/01 e 31/03/2027 e muda dia/hora;
- "nova": cria pauta + peça aprovada (carrossel com corpo.imagens, ou Reels) e agenda.
Confere no fim que nenhum dia/hora ficou com dois posts. Publicado nunca é tocado. Idempotente.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/editorial/aplicar_rebalanceamento.py [--aplicar]"""
import asyncio
import json
import sys
from collections import Counter
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
V = "jf1"
INI, FIM = date(2027, 1, 1), date(2027, 3, 31)


def url(arq):
    return f"{settings.PUBLIC_API_URL}/media/{arq}?v={V}"


async def main(aplicar):
    acoes = json.loads((AQUI / "rebalancear_jan_fev.json").read_text(encoding="utf-8"))
    async with SessionLocal() as db:
        tenant = (await db.execute(select(ScheduledPost.tenant_id).limit(1))).scalar_one()
        linhas = (await db.execute(select(ScheduledPost, ContentPiece).join(
            ContentPiece, ScheduledPost.content_piece_id == ContentPiece.id).where(
            ScheduledPost.data_agendada >= INI, ScheduledPost.data_agendada <= FIM,
            ScheduledPost.canal == "instagram", ScheduledPost.formato == "post"))).all()
        for a in acoes:
            dia = date.fromisoformat(a["dia"])
            if a["acao"] == "mover":
                achadas = [(s, p) for s, p in linhas if a["midia"] in str((p.corpo or {}).get("imagem", ""))]
                if len(achadas) != 1:
                    print("mover: achei", len(achadas), "para", a["midia"])
                    continue
                s, p = achadas[0]
                if s.status == "publicado":
                    continue
                if (s.data_agendada, s.horario) == (dia, a["hora"]):
                    continue
                print(f"mover {s.data_agendada} {s.horario} -> {a['dia']} {a['hora']}  {a['midia']}")
                if aplicar:
                    s.data_agendada, s.horario = dia, a["hora"]
                    if (p.corpo or {}).get("programacao"):
                        p.corpo = {**p.corpo, "programacao": {"data": a["dia"], "hora": a["hora"]}}
                        flag_modified(p, "corpo")
            else:
                arqs = a.get("imagens", []) + [a[k] for k in ("video", "capa") if k in a]
                falta = [x for x in arqs if not (MIDIA / x).exists()]
                if falta:
                    print("nova: SEM ARQUIVO", falta[:3])
                    continue
                chave = "video" if "video" in a else "imagens"
                principal = url(a["video"]) if "video" in a else [url(x) for x in a["imagens"]]
                existentes = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == a["tipo"]))).scalars().all()
                if any((p.corpo or {}).get(chave) == principal for p in existentes):
                    continue
                print(f"nova {a['dia']} {a['hora']} {a['tipo']:9} {a['titulo'][:60]}")
                if not aplicar:
                    continue
                pauta = Pauta(tenant_id=tenant, titulo=a["titulo"], angulo=a["tipo"], area=a["area"], origem="manual",
                              fonte=f"Rebalanceamento jan-fev 2027 ({a['estilo']})", relevante_para_conteudo=True,
                              status="em_producao", data_editorial=dia)
                db.add(pauta)
                await db.flush()
                corpo = {chave: principal, "legenda": a["legenda"], "primeiro_comentario": a.get("primeiro_comentario", ""),
                         "estilo": a["estilo"], "programacao": {"data": a["dia"], "hora": a["hora"]}, "rotulo_ia": False}
                if "capa" in a:
                    corpo["capa"] = url(a["capa"])
                if a.get("episodio"):
                    corpo["episodio"] = a["episodio"]
                peca = ContentPiece(tenant_id=tenant, pauta_id=pauta.id, tipo=a["tipo"], status="aprovado", corpo=corpo)
                db.add(peca)
                await db.flush()
                db.add(ScheduledPost(tenant_id=tenant, content_piece_id=peca.id, titulo=a["titulo"], canal="instagram",
                                     formato=a["formato"], data_agendada=dia, horario=a["hora"], status="pronto"))
        await db.flush()
        todos = (await db.execute(select(ScheduledPost).where(
            ScheduledPost.data_agendada >= INI, ScheduledPost.data_agendada <= FIM, ScheduledPost.canal == "instagram",
            ScheduledPost.status != "pausado", ScheduledPost.formato.not_in(("story", "trial"))))).scalars().all()
        dup = [k for k, n in Counter((s.data_agendada, s.horario) for s in todos).items() if n > 1]
        print("vagas com 2 posts:", dup if aplicar else "(só na aplicação)")
        if aplicar and dup:
            await db.rollback()
            print("DESFEITO: havia vaga repetida")
            return
        if aplicar:
            await db.commit()
            print("aplicado")


asyncio.run(main("--aplicar" in sys.argv))
