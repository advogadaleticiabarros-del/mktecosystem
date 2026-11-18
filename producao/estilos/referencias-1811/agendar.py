"""Roda DENTRO do container da API. Agenda as 14 peças das referências de 18/11/2026 (aprovadas pela Jessica:
"perfeito, programe as postagens em horarios disponiveis e livres seguindo as regras").

Regras (agenda.py e CADERNO_DA_MARCA.md): 1 post do feed por dia, às 12:00; dia ocupado por outro post do feed
(qualquer formato, menos story e trial) não recebe outro. Cada peça tem uma data preferida (tema da época e dia da grade);
se estiver ocupada, vai para o primeiro dia livre depois dela.

Uso:
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/ref1811/agendar.py vagas            (só lista dias livres)
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/ref1811/agendar.py plano <json>     (simula)
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/ref1811/agendar.py aplicar <json>   (grava)
<json>: {"mover": [{id (ScheduledPost), dia}], "pecas": [{peca, titulo, area, dia (AAAA-MM-DD), legenda,
primeiro_comentario, alt}]}. "mover" troca de dia posts já agendados (a data do post, a da pauta e corpo.programacao),
para abrir vaga a peças que dependem da época; o post movido continua inteiro, só muda de dia. Idempotente pela imagem."""
import asyncio
import json
import sys
from datetime import date, timedelta

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant
from app.services.agendamento_horario import hoje_brasilia

HORA = "12:00"
FORA_DO_FEED = ("story", "trial", "reels")


async def ocupados(db, ini, fim):
    rows = (await db.execute(select(ScheduledPost.data_agendada, ScheduledPost.horario, ScheduledPost.formato,
                                    ScheduledPost.titulo, ScheduledPost.status).where(
        ScheduledPost.canal == "instagram", ScheduledPost.data_agendada >= ini, ScheduledPost.data_agendada <= fim,
        ScheduledPost.status.not_in(("cancelado", "falhou")), ScheduledPost.formato.not_in(FORA_DO_FEED)))).all()
    por_dia = {}
    for d, h, f, t, s in rows:
        por_dia.setdefault(d, []).append(f"{h} {f} {s} {t[:50]}")
    return por_dia


async def vagas():
    async with SessionLocal() as db:
        ini, fim = hoje_brasilia() + timedelta(days=1), date(2027, 3, 31)
        oc = await ocupados(db, ini, fim)
        d, livres = ini, []
        while d <= fim:
            if d not in oc:
                livres.append(d)
            d += timedelta(days=1)
        print("LIVRES:", " ".join(f"{x:%d/%m}({'smtqqss'[x.weekday()]})" for x in livres))
        print("ULTIMO OCUPADO:", max(oc) if oc else None, "| dias ocupados:", len(oc))
        st = (await db.execute(select(ScheduledPost.status).distinct())).scalars().all()
        print("STATUS EXISTENTES:", st)


async def agendar(arquivo, aplicar):
    plano = json.loads(open(arquivo, encoding="utf-8").read())
    itens = plano["pecas"]
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        for mv in plano.get("mover", []):
            sp = await db.get(ScheduledPost, mv["id"])
            novo = date.fromisoformat(mv["dia"])
            if sp.data_agendada == novo:
                print("já movido:", sp.titulo)
                continue
            livre = not (await ocupados(db, novo, novo))
            print(f"mover {sp.titulo[:60]} | {sp.data_agendada:%d/%m/%Y} -> {novo:%d/%m/%Y}", "" if livre else "OCUPADO!")
            if not livre:
                raise SystemExit("dia de destino ocupado; nada gravado")
            if not aplicar:
                continue
            sp.data_agendada = novo
            cp = await db.get(ContentPiece, sp.content_piece_id)
            corpo = dict(cp.corpo or {})
            corpo["programacao"] = {"data": novo.isoformat(), "hora": sp.horario}
            cp.corpo = corpo
            if cp.pauta_id:
                pauta = await db.get(Pauta, cp.pauta_id)
                if pauta:
                    pauta.data_editorial = novo
            await db.flush()
        oc = await ocupados(db, hoje_brasilia() + timedelta(days=1), date(2027, 12, 31))
        for mv in plano.get("mover", []) if not aplicar else []:  # na simulação, considera as trocas
            sp = await db.get(ScheduledPost, mv["id"])
            oc.pop(sp.data_agendada, None)
            oc[date.fromisoformat(mv["dia"])] = ["movido"]
        usados = set()
        for it in itens:
            img = f"{settings.PUBLIC_API_URL}/media/{it['peca']}.jpg"
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.tenant_id == tid,
                                                             ContentPiece.corpo["imagem"].as_string() == img))).scalars().first()
            if ja:
                print("já existe:", it["peca"])
                continue
            dia = date.fromisoformat(it["dia"])
            while dia in oc or dia in usados or dia <= hoje_brasilia():
                dia += timedelta(days=1)
            usados.add(dia)
            print(f"{dia:%a %d/%m/%Y} {HORA} {it['peca']} | {it['titulo']}")
            if not aplicar:
                continue
            pauta = Pauta(tenant_id=tid, titulo=it["titulo"], angulo="direitos", area=it["area"], origem="manual",
                          fonte="Referências de 18/11/2026 (producao/estilos/referencias-1811)",
                          relevante_para_conteudo=True, status="em_producao", data_editorial=dia)
            db.add(pauta)
            await db.flush()
            peca = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="estatico", status="aprovado", versao=1,
                                corpo={"imagem": img, "legenda": it["legenda"], "primeiro_comentario": it["primeiro_comentario"],
                                       "alt": it["alt"], "estilo": "referencias-1811", "rotulo_ia": False,
                                       "programacao": {"data": dia.isoformat(), "hora": HORA}})
            db.add(peca)
            await db.flush()
            db.add(ScheduledPost(tenant_id=tid, content_piece_id=peca.id, titulo=it["titulo"], canal="instagram",
                                 formato="post", data_agendada=dia, horario=HORA, status="pronto"))
        if aplicar:
            await db.commit()
            print("gravado")


if __name__ == "__main__":
    modo = sys.argv[1]
    asyncio.run(vagas() if modo == "vagas" else agendar(sys.argv[2], modo == "aplicar"))
