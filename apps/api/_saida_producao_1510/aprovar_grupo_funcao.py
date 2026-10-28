"""Aprova os 5 artigos do grupo "O que a empresa pode exigir" e os 5 posts do Google (aprovação da usuária em 28/10/2026),
pelo mesmo caminho do PATCH status=aprovado de routers/content.py: status, MarketingMemory e agendar_conteudo_aprovado."""
import asyncio
from sqlalchemy import select
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.presenca_google import GooglePost
from app.services.agenda import agendar_conteudo_aprovado

SLUGS = ["acumulo-de-funcao-tenho-direito-a-aumento", "fgts-nao-depositado-como-consultar-e-o-que-fazer",
         "hora-extra-nao-paga-como-calcular-e-provar", "desconto-no-salario-o-que-a-empresa-pode-descontar",
         "banco-de-horas-regras-e-fim-da-6x1"]
B = "https://advogadaleticiabarros.com.br/blog/"

async def main():
    async with SessionLocal() as db:
        for slug in SLUGS:
            piece = (await db.execute(select(ContentPiece).where(ContentPiece.tipo == "artigo",
                     ContentPiece.corpo["slug"].as_string() == slug))).scalars().first()
            if piece.status != "aprovado":
                pauta = (await db.execute(select(Pauta).where(Pauta.id == piece.pauta_id))).scalar_one()
                piece.status = "aprovado"
                db.add(MarketingMemory(tenant_id=piece.tenant_id, content_piece_id=piece.id, tema=pauta.titulo,
                                       angulo=pauta.angulo, formato=piece.tipo, metricas={}, aprendizado=None))
                await agendar_conteudo_aprovado(db, piece)
            post = (await db.execute(select(GooglePost).where(GooglePost.link == f"{B}{slug}.html"))).scalars().first()
            if post and post.status == "rascunho":
                post.status = "aprovado"
            print(slug[:40], piece.status, "| post:", post.status if post else "-", post.publicar_em if post else "")
        await db.commit()

asyncio.run(main())
