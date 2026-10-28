"""Roda DENTRO do container da API: sobe, em RASCUNHO, os 5 Stories das frases da campanha do voto (28/10/2026) na
pauta das frases. Postagem pelo app do Instagram; o story 5 leva o adesivo de link para a LP (formulário).
Precisa dos JPGs em /app/media. Conta as peças por tipo antes e depois (nada pode sumir). Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app -w /app api python /tmp/voto-stories/subir_stories.py
"""
import asyncio
import uuid

from sqlalchemy import func, select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece

PAUTA = uuid.UUID("d7b867af-0436-48cc-ad1b-a875ef8f78b0")  # Assédio eleitoral: frases no estilo de referência (28/10)
MIDIA = f"{settings.PUBLIC_API_URL}/media"
LP = ("https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html"
      "?utm_source=instagram&utm_medium=stories&utm_campaign=assedio-eleitoral-2026&utm_content=frases")
ARTIGO = "https://advogadaleticiabarros.com.br/blog/demitido-por-causa-do-voto-o-que-a-lei-garante.html"
TOTAL = 5


def instrucao(n: int) -> str:
    base = (f"Story {n} de {TOTAL} da sequência \"Demitido por causa do voto\". Postar os {TOTAL} em sequência, na ordem, "
            "pelo app do Instagram.\n\nNo Instagram: + > Story > escolher esta imagem (sem cortar) > Seu story.")
    if n == TOTAL:
        base += ("\n\nAntes de publicar: adesivo LINK no espaço vazio abaixo de \"Fale com a gente no link abaixo\".\n"
                 f"Link: {LP}\nTexto do adesivo: Quero orientação\n"
                 f"(Artigo do blog, se preferir: {ARTIGO})\n"
                 "Depois: adicionar os 5 ao destaque \"Voto e emprego\".")
    return base


async def contagem(db) -> dict:
    return dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())


async def main():
    async with SessionLocal() as db:
        antes = await contagem(db)
        tid = (await db.execute(select(ContentPiece.tenant_id).where(ContentPiece.pauta_id == PAUTA).limit(1))).scalar_one()
        ja = {(c.corpo or {}).get("ordem") for c in (await db.execute(select(ContentPiece).where(
            ContentPiece.pauta_id == PAUTA, ContentPiece.tipo == "stories"))).scalars().all()}
        for n in range(1, TOTAL + 1):
            if n in ja:
                print("já existia story", n)
                continue
            c = ContentPiece(tenant_id=tid, pauta_id=PAUTA, tipo="stories", status="rascunho", versao=1, corpo={
                "ordem": n, "imagem": f"{MIDIA}/story-demissao-voto-{n}.jpg", "legenda": instrucao(n),
                **({"link": LP} if n == TOTAL else {}),
                "programacao": {"data": "2026-10-28", "hora": f"20:{n:02d}"}})
            db.add(c)
            await db.flush()
            print("criado story", n, c.id)
        await db.commit()
        depois = await contagem(db)
        print("antes:", antes)
        print("depois:", depois)
        print("sumiu:", {t: k for t, k in antes.items() if depois.get(t, 0) < k} or "nada")


asyncio.run(main())
