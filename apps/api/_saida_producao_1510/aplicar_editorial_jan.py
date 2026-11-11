"""Roda DENTRO do container da API: aplica o editorial até 31/01/2027 (editorial_jan.json, de montar_editorial_jan.py).
Pedido da Jessica em 10/11/2026: 2 publicações no feed por dia (post às 12h e Reels às 19h), Reels da Dra. no domingo,
feed claro e completo até o fim de janeiro.

Faz, nesta ordem:
1. todo post do feed (não Reels) agendado às 11h ou 14h de 11/11/2026 em diante, ainda "pronto", passa para 12:00;
2. acao "mover": muda um agendamento de dia/hora (Mito ou Lei de 07/01 para 06/01);
3. acao "dra": o Reels gravado pela Dra. (achado pelo título) vai para o domingo 15h30, com capa própria, PAUSADO
   (sai só depois da versão nova aprovada); o Limbo deixa a terça/sexta de janeiro para o Flagrante;
4. acao "agendar": peça aprovada da reserva entra na agenda;
5. acao "nova": cria pauta + peça aprovada (estático ou Reels) e agenda.
Idempotente: não duplica dia/hora ocupado nem arquivo já usado. Publicado nunca é tocado.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/editorial/aplicar_editorial_jan.py [--aplicar]"""
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
V = "jan1"
INICIO = date(2026, 11, 11)


def url(arq):
    return f"{settings.PUBLIC_API_URL}/media/{arq}?v={V}"


async def feed_do_dia(db, dia, reels):
    q = select(ScheduledPost).where(ScheduledPost.data_agendada == dia, ScheduledPost.canal == "instagram",
                                    ScheduledPost.status != "pausado")
    q = q.where(ScheduledPost.formato == "reels") if reels else q.where(
        ScheduledPost.formato.not_in(("reels", "story", "trial")))
    return (await db.execute(q)).scalars().all()


async def main(aplicar):
    acoes = json.loads((AQUI / "editorial_jan.json").read_text(encoding="utf-8"))
    async with SessionLocal() as db:
        tenant = (await db.execute(select(ScheduledPost.tenant_id).limit(1))).scalar_one()
        # 1. feed ao meio-dia
        sps = (await db.execute(select(ScheduledPost, ContentPiece).outerjoin(
            ContentPiece, ScheduledPost.content_piece_id == ContentPiece.id).where(
            ScheduledPost.data_agendada >= INICIO, ScheduledPost.canal == "instagram", ScheduledPost.status == "pronto",
            ScheduledPost.formato.not_in(("reels", "story", "trial")),
            ScheduledPost.horario.in_(("11:00", "14:00"))))).all()  # horários antigos; a frase de quinta 19h fica
        for sp, p in sps:
            print(f"12h  {sp.data_agendada} {sp.horario}->12:00 {sp.titulo[:60]}")
            if aplicar:
                sp.horario = "12:00"
                prog = (p.corpo or {}).get("programacao") if p else None
                if prog:
                    p.corpo = {**p.corpo, "programacao": {**prog, "hora": "12:00"}}
                    flag_modified(p, "corpo")
        for a in acoes:
            dia = date.fromisoformat(a["dia"]) if "dia" in a else None
            if a["acao"] == "mover":
                sp = (await db.execute(select(ScheduledPost).where(ScheduledPost.titulo == a["titulo"],
                      ScheduledPost.data_agendada == date.fromisoformat(a["de"])))).scalar_one_or_none()
                if not sp or sp.status == "publicado":
                    print("mover: não achado ou publicado", a["titulo"])
                    continue
                print(f"mover {a['de']} -> {a['para']} {a['hora']} {a['titulo'][:50]}")
                if aplicar:
                    sp.data_agendada, sp.horario = date.fromisoformat(a["para"]), a["hora"]
                    p = await db.get(ContentPiece, sp.content_piece_id)
                    if p and (p.corpo or {}).get("programacao"):
                        p.corpo = {**p.corpo, "programacao": {"data": a["para"], "hora": a["hora"]}}
                        flag_modified(p, "corpo")
            elif a["acao"] == "dra":
                linhas = (await db.execute(select(ContentPiece, Pauta).join(Pauta, ContentPiece.pauta_id == Pauta.id).where(
                    ContentPiece.tipo == "reels", Pauta.titulo.ilike(f"%{a['titulo_contem']}%")))).all()
                linhas = [(p, pa) for p, pa in linhas if p.status == "aprovado"]
                if len(linhas) != 1:
                    print("dra: achei", len(linhas), "para", a["titulo_contem"])
                    continue
                p, pa = linhas[0]
                if not (MIDIA / a["capa"]).exists():
                    print("dra: SEM CAPA em /app/media", a["capa"])
                    continue
                sp = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == p.id))).scalar_one_or_none()
                if sp and sp.status == "publicado":
                    print("dra: já publicado", pa.titulo)
                    continue
                print(f"dra  {a['dia']} {a['hora']} pausado  {pa.titulo[:60]}" + (f" (era {sp.data_agendada})" if sp else ""))
                if aplicar:
                    corpo = {k: v for k, v in (p.corpo or {}).items() if k != "reserva"}
                    corpo.update({"capa": url(a["capa"]), "programacao": {"data": a["dia"], "hora": a["hora"]},
                                  "domingo_da_dra": True})
                    p.corpo = corpo
                    flag_modified(p, "corpo")
                    if sp:
                        sp.data_agendada, sp.horario, sp.status = dia, a["hora"], a["status"]
                    else:
                        db.add(ScheduledPost(tenant_id=p.tenant_id, content_piece_id=p.id, titulo=pa.titulo,
                                             canal="instagram", formato="reels", data_agendada=dia, horario=a["hora"],
                                             status=a["status"]))
            elif a["acao"] == "agendar":
                p = await db.get(ContentPiece, __import__("uuid").UUID(a["piece_id"]))
                ja = (await db.execute(select(ScheduledPost).where(ScheduledPost.content_piece_id == p.id))).scalar_one_or_none()
                if ja:
                    print("agendar: já na agenda", ja.data_agendada, ja.titulo[:50])
                    continue
                ocup = [s for s in await feed_do_dia(db, dia, False) if s.horario == a["hora"]]
                if ocup:
                    print("agendar: horário ocupado", a["dia"], a["hora"], ocup[0].titulo[:40])
                    continue
                pa = await db.get(Pauta, p.pauta_id)
                print(f"res  {a['dia']} {a['hora']} {p.tipo} {pa.titulo[:60]}")
                if aplicar:
                    db.add(ScheduledPost(tenant_id=p.tenant_id, content_piece_id=p.id, titulo=pa.titulo, canal="instagram",
                                         formato=a["formato"], data_agendada=dia, horario=a["hora"], status=a["status"]))
            elif a["acao"] == "nova":
                arqs = [a[k] for k in ("arquivo", "video", "capa") if k in a]
                falta = [x for x in arqs if not (MIDIA / x).exists()]
                if falta:
                    print("nova: SEM ARQUIVO", falta)
                    continue
                principal = url(a.get("video") or a["arquivo"])
                ja = (await db.execute(select(ContentPiece).where(ContentPiece.corpo["video" if "video" in a else "imagem"].as_string() == principal))).first()
                if ja:
                    print("nova: já criada", a["titulo"][:50])
                    continue
                reels = a["tipo"] == "reels"
                ocup = [s for s in await feed_do_dia(db, dia, reels) if reels or s.horario == a["hora"]]
                if ocup:
                    print("nova: vaga ocupada", a["dia"], a["hora"], ocup[0].titulo[:50])
                    continue
                print(f"nova {a['dia']} {a['hora']} {a['tipo']:8} {a['estilo']:12} {a['titulo'][:55]}")
                if not aplicar:
                    continue
                pauta = Pauta(tenant_id=tenant, titulo=a["titulo"], angulo=a["tipo"], area=a["area"], origem="manual",
                              fonte=f"Editorial até 31/01/2027 ({a['estilo']})", relevante_para_conteudo=True,
                              status="em_producao", data_editorial=dia)
                db.add(pauta)
                await db.flush()
                corpo = {"legenda": a["legenda"], "primeiro_comentario": a.get("primeiro_comentario", ""),
                         "estilo": a["estilo"], "programacao": {"data": a["dia"], "hora": a["hora"]}, "rotulo_ia": False}
                if reels:
                    corpo.update({"video": principal, "capa": url(a["capa"])})
                    if a.get("episodio"):
                        corpo["episodio"] = a["episodio"]
                else:
                    corpo.update({"imagem": principal, "alt": a.get("alt", "")})
                peca = ContentPiece(tenant_id=tenant, pauta_id=pauta.id, tipo=a["tipo"], status="aprovado", corpo=corpo)
                db.add(peca)
                await db.flush()
                db.add(ScheduledPost(tenant_id=tenant, content_piece_id=peca.id, titulo=a["titulo"], canal="instagram",
                                     formato=a["formato"], data_agendada=dia, horario=a["hora"], status="pronto"))
            await db.flush()
        if aplicar:
            await db.commit()
            print("aplicado")


asyncio.run(main("--aplicar" in sys.argv))
