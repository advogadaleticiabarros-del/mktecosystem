"""Roda DENTRO do container da API: sobe a produção de novembro/2026 como RASCUNHO (sem agendar) para a
Letícia aprovar em "Revisar e aprovar". Cada peça vai para a pauta de novembro do dia (criada em
09/10/2026, docs/PLANO_CONTEUDO_NOV_2026.md), com programação (data + hora). Idempotente.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/nov/subir_nov.py
"""
import asyncio
import re
import sys
from datetime import date
from pathlib import Path

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from artigos_nov import ARTIGOS  # noqa: E402
from conteudo_nov import MITO_OU_LEI, TEMAS, legenda_mito  # noqa: E402

V = "nov1"
MIDIA = f"{settings.PUBLIC_API_URL}/media"


def url(nome: str) -> str:
    return f"{MIDIA}/{nome}?v={V}"


def texto(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


async def pauta_do_dia(db, tenant_id, dia: str, angulo: str, titulo: str | None = None) -> Pauta:
    q = select(Pauta).where(Pauta.tenant_id == tenant_id, Pauta.data_editorial == date.fromisoformat(dia), Pauta.angulo == angulo)
    if titulo:
        q = q.where(Pauta.titulo == titulo)
    p = (await db.execute(q)).scalars().first()
    assert p, (dia, angulo, titulo)
    p.status = "em_producao"
    return p


async def criar(db, tenant_id, pauta: Pauta, tipo: str, corpo: dict) -> bool:
    ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == pauta.id, ContentPiece.tipo == tipo))).scalars().first()
    if ja:
        return False
    db.add(ContentPiece(tenant_id=tenant_id, pauta_id=pauta.id, tipo=tipo, corpo=corpo, status="rascunho", versao=1))
    return True


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        n = 0
        for t in TEMAS:
            p = await pauta_do_dia(db, tid, t["data"], "direitos")
            k, prog = t["chave"], lambda h: {"data": t["data"], "hora": h}
            n += await criar(db, tid, p, "pergunta", {
                "imagem": url(f"{k}-pergunta-v6.jpg"), "pergunta": texto(t["pergunta"]["html"]),
                "legenda": t["pergunta"]["legenda"], "primeiro_comentario": t["pergunta"]["pc"], "programacao": prog("12:00")})
            n += await criar(db, tid, p, "frase", {
                "imagem": url(f"{k}-frase-v2.jpg"), "frase": texto(t["frase"]["html"]),
                "legenda": t["frase"]["legenda"], "primeiro_comentario": t["frase"]["pc"], "programacao": prog("15:00")})
            c = t["carrossel"]
            n += await criar(db, tid, p, "carrossel", {
                "imagens": [url(f"{k}-v5-{i}.jpg") for i in range(1, 8)],
                "legenda": c["legenda"], "primeiro_comentario": c["pc"], "programacao": prog("18:00")})
        for m in MITO_OU_LEI:
            dia, af = m[0], m[2]
            p = await pauta_do_dia(db, tid, dia, "mito")
            leg, pc = legenda_mito(m)
            n += await criar(db, tid, p, "estatico", {
                "imagem": url(f"mito-{dia}-v3-topo.jpg"), "texto_overlay": af,
                "legenda": leg, "primeiro_comentario": pc, "programacao": {"data": dia, "hora": "19:00"}})
        for a in ARTIGOS:
            p = await pauta_do_dia(db, tid, a["data"], "artigo", a["pauta"])
            n += await criar(db, tid, p, "artigo", {
                "titulo": a["titulo"], "slug": a["slug"], "html": a["html"], "meta_description": a["meta"],
                "resumo": a["resumo"], "capa_arquivo": f"capa-{a['slug']}.png", "imagem_capa": url(f"capa-{a['slug']}.png"),
                "programacao": {"data": a["data"], "hora": "09:00"}})
        await db.commit()
        print("peças criadas em rascunho:", n)


asyncio.run(main())
