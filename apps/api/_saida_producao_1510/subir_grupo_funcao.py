"""Roda DENTRO do container da API: sobe o grupo "O que a empresa pode exigir" (artigos_grupo_funcao.py) como
RASCUNHO para a Letícia aprovar em "Revisar e aprovar". Uma pauta nova por artigo (quintas, 9h; as pautas de
gestante das mesmas quintas, sem texto, ficam como estão) e um post do Perfil da Empresa em rascunho por artigo
(tela "Google e site"), para o mesmo dia às 10h. Idempotente (pelo slug do artigo e pelo link do post).

Antes: docker compose cp pecas/<capas e posts>. api:/app/media/
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/funcao/subir_grupo_funcao.py
"""
import asyncio
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.presenca_google import GooglePost
from app.models.tenant import Tenant

sys.path.insert(0, str(Path(__file__).resolve().parent))
from artigos_grupo_funcao import ARTIGOS, B  # noqa: E402

V = "funcao1"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
BRT = timezone(timedelta(hours=-3))


def url(nome: str) -> str:
    return f"{MIDIA}/{nome}?v={V}"


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        artigos = posts = 0
        for a in ARTIGOS:
            ja = (await db.execute(select(ContentPiece).where(
                ContentPiece.tenant_id == tid, ContentPiece.tipo == "artigo",
                ContentPiece.corpo["slug"].as_string() == a["slug"]))).scalars().first()
            if not ja:
                pauta = Pauta(tenant_id=tid, titulo=a["pauta"], angulo="artigo", area="Trabalhista", origem="manual",
                              fonte="grupo \"O que a empresa pode exigir\" (27/10/2026, producao/seo e search console)",
                              relevante_para_conteudo=True, status="em_producao", data_editorial=date.fromisoformat(a["data"]))
                db.add(pauta)
                await db.flush()
                capa = f"capa-{a['slug']}.jpg"
                db.add(ContentPiece(tenant_id=tid, pauta_id=pauta.id, tipo="artigo", status="rascunho", versao=1, corpo={
                    "titulo": a["titulo"], "slug": a["slug"], "html": a["html"], "meta_description": a["meta"],
                    "resumo": a["resumo"], "capa_arquivo": capa, "imagem_capa": url(capa),
                    "legenda": "Post para o Perfil da Empresa no Google (já criado em rascunho na tela Google e site):\n\n" + a["post_google"],
                    "programacao": {"data": a["data"], "hora": "09:00"}}))
                artigos += 1
            link = f"{B}{a['slug']}.html"
            if not (await db.execute(select(GooglePost).where(GooglePost.tenant_id == tid, GooglePost.link == link))).scalars().first():
                dia = date.fromisoformat(a["data"])
                db.add(GooglePost(tenant_id=tid, texto=a["post_google"], botao="LEARN_MORE", link=link,
                                  imagem_url=url(f"google-post-{a['slug']}.jpg"), status="rascunho",
                                  publicar_em=datetime(dia.year, dia.month, dia.day, 10, 0, tzinfo=BRT)))
                posts += 1
        await db.commit()
        print(f"artigos criados em rascunho: {artigos}; posts do Google em rascunho: {posts}")


asyncio.run(main())
