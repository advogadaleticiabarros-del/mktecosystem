"""Baixa o perfil e os 12 posts mais recentes do Instagram da Dra. (conta conectada no Orbit). Só leitura."""
import asyncio, json, os, httpx
from sqlalchemy import select
from app.db import SessionLocal
from app.core.crypto import decrypt_token
from app.integrations.social.instagram_api import InstagramAPI
from app.models.social_connection import SocialConnection
OUT = "/tmp/igfeed"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with SessionLocal() as db:
        c = (await db.execute(select(SocialConnection).where(SocialConnection.plataforma == "instagram", SocialConnection.status == "ativo"))).scalars().first()
    api = InstagramAPI(decrypt_token(c.access_token_encrypted))
    perfil = await api._get(f"/{c.ig_user_id}", {"fields": "username,name,biography,website,profile_picture_url,followers_count,follows_count,media_count"})
    posts = await api.posts_com_imagem(c.ig_user_id, 12)
    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as h:
        if perfil.get("profile_picture_url"):
            open(f"{OUT}/avatar.jpg", "wb").write((await h.get(perfil["profile_picture_url"])).content)
        for i, p in enumerate(posts):
            url = p.get("thumbnail_url") if p.get("media_type") == "VIDEO" else p.get("media_url")
            if url: open(f"{OUT}/post{i:02d}.jpg", "wb").write((await h.get(url)).content)
    perfil.pop("profile_picture_url", None)
    json.dump({"perfil": perfil, "tipos": [p.get("media_type") for p in posts]}, open(f"{OUT}/perfil.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(perfil, ensure_ascii=False))
asyncio.run(main())
