"""Roda DENTRO do container da API: sobe, em RASCUNHO, os 4 Stories das listas por causa do voto (28/10/2026) na mesma
pauta do carrossel. Postagem pelo app do Instagram; o story 4 leva o adesivo de link para o artigo.
Precisa dos JPGs em /app/media. Conta as peças por tipo antes e depois (nada pode sumir). Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/listas-voto/subir_stories.py
"""
import asyncio

from sqlalchemy import func, select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

TITULO = "Listas por causa do voto: frases-notícia (28/10)"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
ARTIGO = ("https://advogadaleticiabarros.com.br/blog/lista-por-causa-do-voto-e-crime.html"
          "?utm_source=instagram&utm_medium=stories&utm_campaign=assedio-eleitoral-2026&utm_content=listas")
RESERVA = "https://advogadaleticiabarros.com.br/voto"


def instrucao(n: int) -> str:
    base = (f"Story {n} de 4 da sequência \"Listas por causa do voto\". Postar os 4 em sequência, na ordem, pelo app do "
            "Instagram.\n\nNo Instagram: + > Story > escolher esta imagem (sem cortar) > Seu story.")
    if n == 4:
        base += ("\n\nAntes de publicar: adesivo LINK no espaço vazio abaixo de \"Passo a passo no link abaixo\".\n"
                 f"Link: {ARTIGO}\nTexto do adesivo: O que a lei garante\n"
                 f"Se o artigo ainda não estiver no ar, use {RESERVA}.\n"
                 "Depois: adicionar os 4 ao destaque \"Voto e emprego\".")
    return base


async def contagem(db) -> dict:
    return dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())


async def main():
    async with SessionLocal() as db:
        antes = await contagem(db)
        tid = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one().id
        p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == TITULO))).scalars().one()
        ja = {(c.corpo or {}).get("ordem") for c in (await db.execute(select(ContentPiece).where(
            ContentPiece.pauta_id == p.id, ContentPiece.tipo == "stories"))).scalars().all()}
        for n in range(1, 5):
            if n in ja:
                print("já existia story", n)
                continue
            c = ContentPiece(tenant_id=tid, pauta_id=p.id, tipo="stories", status="rascunho", versao=1, corpo={
                "ordem": n, "imagem": f"{MIDIA}/story-listas-voto-{n}.jpg", "legenda": instrucao(n),
                **({"link": ARTIGO} if n == 4 else {}),
                "programacao": {"data": "2026-10-28", "hora": f"18:{n + 4:02d}"}})
            db.add(c)
            await db.flush()
            print("criado story", n, c.id)
        await db.commit()
        depois = await contagem(db)
        print("antes:", antes)
        print("depois:", depois)
        print("sumiu:", {t: k for t, k in antes.items() if depois.get(t, 0) < k} or "nada")


asyncio.run(main())
