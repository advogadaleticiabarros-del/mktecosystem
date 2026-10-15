"""Roda DENTRO do container da API: atende o pedido de ajuste do acervo 04 (Guarda compartilhada).
- A peça do pedido vira a Parte 1 (vídeo novo, legenda, primeiro comentário, 21/10 20h30), sem o pedido, em rascunho.
- Partes 2 e 3 entram como peças novas (23/10 e 25/10, 20h30), em rascunho, para a Letícia aprovar.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/guarda/subir_guarda.py
"""
import asyncio
import sys
import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

sys.path.insert(0, "/tmp/guarda")
from legendas import LEGENDAS  # noqa: E402

PEDIDO = uuid.UUID("edf05653-9e79-4e79-89c4-856f40335bfe")
DATAS = {1: "2026-10-21", 2: "2026-10-23", 3: "2026-10-25"}
TITULOS = {1: "Série Guarda dos filhos (1/3): quem decide", 2: "Série Guarda dos filhos (2/3): não deixa de ser pai",
           3: "Série Guarda dos filhos (3/3): quando o contato é suspenso"}


def corpo(n: int) -> dict:
    return {"video": f"{settings.PUBLIC_API_URL}/media/guarda-compartilhada-{n}.mp4?v=g1",
            "legenda": LEGENDAS[n]["legenda"], "primeiro_comentario": LEGENDAS[n]["primeiro_comentario"],
            "programacao": {"data": DATAS[n], "hora": "20:30"}}


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        c = await db.get(ContentPiece, PEDIDO)
        p = await db.get(Pauta, c.pauta_id)
        p.titulo, p.data_editorial, p.area = TITULOS[1], date.fromisoformat(DATAS[1]), "Família"
        c.corpo = corpo(1)
        flag_modified(c, "corpo")
        c.status, c.versao = "rascunho", (c.versao or 1) + 1
        print("parte 1 atualizada", c.id)
        for n in (2, 3):
            q = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == TITULOS[n]))).scalars().first()
            if not q:
                q = Pauta(tenant_id=tid, titulo=TITULOS[n], angulo="reels", area="Família", origem="manual",
                          fonte="Gravação da Dra. Letícia (15/08/2025)", relevante_para_conteudo=True, status="em_producao",
                          data_editorial=date.fromisoformat(DATAS[n]))
                db.add(q)
                await db.flush()
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == q.id, ContentPiece.tipo == "reels"))).scalars().first()
            if not ja:
                db.add(ContentPiece(tenant_id=tid, pauta_id=q.id, tipo="reels", status="rascunho", versao=1, corpo=corpo(n)))
                print("parte", n, "criada")
        await db.commit()


asyncio.run(main())
