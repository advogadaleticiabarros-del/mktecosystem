"""Roda no container: troca as imagens do rascunho do carrossel de 27/10 (66ac094b) pela versão de 9 slides,
guardando a de 7 em corpo.versoes_anteriores. Só mexe se a peça ainda for rascunho."""
import asyncio, uuid
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.orm.attributes import flag_modified
from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece

ID = uuid.UUID("66ac094b-fe67-4c78-b66a-2f34e6dd39fc")
MIDIA = f"{settings.PUBLIC_API_URL}/media"


async def main():
    async with SessionLocal() as db:
        antes = dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())
        c = (await db.execute(select(ContentPiece).where(ContentPiece.id == ID))).scalars().one()
        assert c.status == "rascunho", c.status
        corpo = dict(c.corpo)
        if "-v9-" not in corpo["imagens"][0]:
            corpo.setdefault("versoes_anteriores", []).append(
                {"imagens": corpo["imagens"], "em": datetime.now(timezone.utc).isoformat(), "nota": "v1 de 7 slides"})
            corpo["imagens"] = [f"{MIDIA}/assedio-eleitoral-voto-v9-{i}.jpg?v=ae2" for i in range(1, 10)]
            c.corpo = corpo
            flag_modified(c, "corpo")
            await db.commit()
        depois = dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())
        print("imagens:", len(c.corpo["imagens"]), "| versões guardadas:", len(c.corpo.get("versoes_anteriores", [])),
              "| programação:", c.corpo.get("programacao"), "| contagem igual:", antes == depois)

asyncio.run(main())
