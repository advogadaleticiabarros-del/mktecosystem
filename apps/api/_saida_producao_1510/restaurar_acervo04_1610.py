"""Roda DENTRO do container da API (16/10/2026). Restaura o Reels 04 do acervo (Guarda compartilhada, gravação da
Dra. Letícia) como peça própria em "Para aprovar". Em 15/10 a peça dele foi reaproveitada como Parte 1 da série
Guarda dos filhos e o original sumiu do Estúdio. Regra desde então: material pronto nunca é sobrescrito; versão nova
é peça nova. O arquivo original (acervo-04-guarda-compartilhada.mp4) nunca foi apagado. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/restaurar/restaurar_acervo04_1610.py
"""
import asyncio

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

VIDEO = f"{settings.PUBLIC_API_URL}/media/acervo-04-guarda-compartilhada.mp4?v=acervo1"
TITULO = "Acervo de Reels: Guarda compartilhada (original da Dra. Letícia)"
AVISO = ("ACERVO: Reels original da Dra. Letícia sobre guarda compartilhada (versão completa, anterior à série "
         "Guarda dos filhos). Confira se ele já foi postado antes de aprovar.")


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        ja = [p for p in (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "reels"))).scalars().all()
              if (p.corpo or {}).get("video", "").startswith(VIDEO.split("?")[0])]
        if ja:
            print("já existe:", ja[0].id, ja[0].status)
            return
        pauta = Pauta(tenant_id=tid, titulo=TITULO, angulo="reels", area="Família", origem="manual",
                      fonte="Acervo de Reels (C:/tmp/videos-reels/04)", relevante_para_conteudo=True, status="em_producao")
        db.add(pauta)
        await db.flush()
        peca = ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="reels", status="rascunho", versao=1,
                            corpo={"video": VIDEO, "legenda": AVISO, "acervo": True})
        db.add(peca)
        await db.commit()
        print("restaurado:", peca.id)


asyncio.run(main())
