"""Roda no container: cria o post do Google da campanha do voto (ES) no Orbit, aprovado, e publica na hora pela
mesma função do job (`central_google.publicar_post`). A imagem precisa estar em /app/media. Idempotente pelo link.
"""
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import select
from app.config import settings
from app.db import SessionLocal
from app.models.presenca_google import GooglePost
from app.models.tenant import Tenant
from app.services.central_google import publicar_post

LINK = ("https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html?utm_source=google&utm_medium=gbp-post"
        "&utm_campaign=assedio-eleitoral-2026#espirito-santo")
IMAGEM = f"{settings.PUBLIC_API_URL}/media/google-post-demitido-voto-es-1200x900.jpg"


def texto() -> str:
    md = (Path(__file__).resolve().parent / "post-google.md").read_text(encoding="utf-8")
    return md.split("Texto (sem telefone, que o Google recusa no corpo do post):", 1)[1].strip()


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one().id
        post = (await db.execute(select(GooglePost).where(GooglePost.tenant_id == tid, GooglePost.link == LINK))).scalars().first()
        if post is None:
            post = GooglePost(tenant_id=tid, texto=texto(), botao="LEARN_MORE", link=LINK, imagem_url=IMAGEM,
                              status="aprovado", publicar_em=datetime.now(timezone.utc))
            db.add(post)
            await db.commit()
        if post.status == "publicado":
            print("já publicado:", post.link_publicado)
            return
        try:
            await publicar_post(db, post)
            print("publicado:", post.id, post.link_publicado)
        except Exception as e:  # o job tenta de novo, porque o post fica aprovado
            post.erro = str(e)[:500]
            await db.commit()
            print("erro ao publicar (fica aprovado para o job):", e)

asyncio.run(main())
