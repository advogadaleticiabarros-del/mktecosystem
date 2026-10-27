"""Roda DENTRO do container da API: cria a frase (15h) e o estático (20h) de 27/10/2026 como RASCUNHO.
As imagens já devem estar em /app/media. Idempotente (não duplica peça da mesma pauta e tipo).
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/assedio-fe/subir.py
"""
import asyncio
import sys
from datetime import date
from pathlib import Path

from sqlalchemy import func, select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

sys.path.insert(0, str(Path(__file__).resolve().parent))
import textos as t  # noqa: E402

HOJE = date(2026, 10, 27)
TITULO = "Assédio eleitoral: demissão pelo voto (frase e estático)"
MIDIA = f"{settings.PUBLIC_API_URL}/media"


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one().id
        antes = dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())
        p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.data_editorial == HOJE,
                                                  Pauta.titulo == TITULO))).scalars().first()
        if not p:
            p = Pauta(tenant_id=tid, titulo=TITULO, angulo="frase e estático", area="Trabalhista", origem="manual",
                      fonte="Campanha assédio eleitoral 27/10/2026 (producao/campanhas/2026-10-assedio-eleitoral)",
                      relevante_para_conteudo=True, status="em_producao", data_editorial=HOJE)
            db.add(p)
            await db.flush()
        pecas = [
            ("frase", {"imagem": f"{MIDIA}/assedio-eleitoral-frase-v2.jpg", "frase": t.FRASE_TEXTO,
                       "legenda": t.FRASE_LEGENDA, "primeiro_comentario": t.FRASE_PRIMEIRO_COMENTARIO,
                       "texto_alternativo": t.FRASE_ALT, "programacao": {"data": "2026-10-27", "hora": "15:00"}}),
            ("estatico", {"imagem": f"{MIDIA}/assedio-eleitoral-estatico-provas-v1.jpg",
                          "texto_overlay": "Demitido por causa do voto? 5 provas para guardar agora",
                          "legenda": t.ESTATICO_LEGENDA, "primeiro_comentario": t.ESTATICO_PRIMEIRO_COMENTARIO,
                          "texto_alternativo": t.ESTATICO_ALT, "programacao": {"data": "2026-10-27", "hora": "20:00"}}),
        ]
        ids = []
        for tipo, corpo in pecas:
            ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == p.id,
                                                              ContentPiece.tipo == tipo))).scalars().first()
            if ja:
                ids.append((tipo, ja.id, "já existia"))
                continue
            c = ContentPiece(tenant_id=tid, pauta_id=p.id, tipo=tipo, corpo=corpo, status="rascunho", versao=1)
            db.add(c)
            await db.flush()
            ids.append((tipo, c.id, "criada"))
        await db.commit()
        depois = dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())
        print("pauta", p.id)
        for x in ids:
            print(*x)
        print("antes ", sorted(antes.items()))
        print("depois", sorted(depois.items()))


asyncio.run(main())
