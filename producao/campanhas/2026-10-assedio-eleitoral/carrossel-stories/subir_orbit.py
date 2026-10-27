"""Roda DENTRO do container da API: cria a pauta de 27/10/2026 "Assédio eleitoral: demissão pelo voto" e sobe, em
RASCUNHO, o carrossel (18h de hoje) e os 8 Stories (13h00 a 13h07). A Letícia/Jessica aprova no Editorial.
Conta as peças por tipo antes e depois (nada pode sumir). Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/assedio/subir_orbit.py
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
from legendas import LEGENDA_FB, LEGENDA_IG, LINK_STORIES, PC_FB, PC_IG, instrucao_story  # noqa: E402

V = "ae1"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
HOJE = date(2026, 10, 27)
TITULO = "Assédio eleitoral: demissão pelo voto (carrossel e Stories)"


def url(nome: str) -> str:
    return f"{MIDIA}/{nome}?v={V}"


async def contagem(db) -> dict:
    return dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())


async def main():
    async with SessionLocal() as db:
        antes = await contagem(db)
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.data_editorial == HOJE,
                                                  Pauta.titulo == TITULO))).scalars().first()
        if not p:
            p = Pauta(tenant_id=tid, titulo=TITULO, angulo="direitos", area="Trabalhista", origem="manual",
                      fonte="MPT 26/10/2026; Lei 9.029/1995; CF art. 5º VIII; Código Eleitoral art. 301; STF Tema 237",
                      relevante_para_conteudo=True, status="em_producao", data_editorial=HOJE)
            db.add(p)
            await db.flush()
        existentes = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == p.id))).scalars().all()
        ja = {(c.tipo, (c.corpo or {}).get("ordem")) for c in existentes}
        novas = []
        if ("carrossel", None) not in ja:
            novas.append(ContentPiece(tenant_id=tid, pauta_id=p.id, tipo="carrossel", status="rascunho", versao=1, corpo={
                "imagens": [url(f"assedio-eleitoral-voto-v5-{i}.jpg") for i in range(1, 8)],
                "legenda": LEGENDA_IG, "primeiro_comentario": PC_IG,
                "legenda_facebook": LEGENDA_FB, "primeiro_comentario_facebook": PC_FB,
                "programacao": {"data": "2026-10-27", "hora": "18:00"}}))
        for n in range(1, 9):
            if ("stories", n) not in ja:
                novas.append(ContentPiece(tenant_id=tid, pauta_id=p.id, tipo="stories", status="rascunho", versao=1, corpo={
                    "ordem": n, "imagem": url(f"story-assedio-eleitoral-{n}.jpg"), "legenda": instrucao_story(n),
                    **({"link": LINK_STORIES} if n == 8 else {}),
                    "programacao": {"data": "2026-10-27", "hora": f"13:{n - 1:02d}"}}))
        db.add_all(novas)
        await db.commit()
        depois = await contagem(db)
        print("antes:", antes)
        print("depois:", depois)
        sumiu = {t: n for t, n in antes.items() if depois.get(t, 0) < n}
        print("sumiu:", sumiu or "nada")
        for c in novas:
            print(c.tipo, (c.corpo or {}).get("ordem", ""), c.id)


asyncio.run(main())
