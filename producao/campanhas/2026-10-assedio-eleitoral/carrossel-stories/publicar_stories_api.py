"""Publica os Stories 01-07 da campanha (pedido de 27/10/2026); a 08 (adesivo de link) é postada pela usuária no app."""
import asyncio
from datetime import datetime, timezone
from sqlalchemy import func, select
from sqlalchemy.orm.attributes import flag_modified
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.integrations.social.instagram_api import InstagramAPI
from app.services.instagram_publisher import _conexao_ativa
from app.core.crypto import decrypt_token
IDS = ["402b9a3e", "283f7a26", "7994b5cc", "ada4ff89", "b01f93c6", "b6abfe07", "29aaf3e7"]
async def main():
    async with SessionLocal() as db:
        pecas = []
        for prefixo in IDS:
            p = (await db.execute(select(ContentPiece).where(func.cast(ContentPiece.id, __import__("sqlalchemy").String).like(prefixo + "%")))).scalar_one()
            pecas.append(p)
        conexao = await _conexao_ativa(db, pecas[0].tenant_id)
        api = InstagramAPI(page_token=decrypt_token(conexao.access_token_encrypted))
        for n, p in enumerate(pecas, 1):
            corpo = dict(p.corpo or {})
            if corpo.get("story_publicado"):
                print(n, "já publicado", corpo["story_publicado"]); continue
            c = await api._post(f"/{conexao.ig_user_id}/media", {"media_type": "STORIES", "image_url": corpo["imagem"]})
            await api._aguardar(c["id"])
            pub = await api._post(f"/{conexao.ig_user_id}/media_publish", {"creation_id": c["id"]})
            corpo["story_publicado"] = {"id": pub["id"], "em": datetime.now(timezone.utc).isoformat()}
            p.corpo = corpo; flag_modified(p, "corpo"); p.status = "publicado"
            await db.commit()
            print(n, "publicado", pub["id"], flush=True)
asyncio.run(main())
