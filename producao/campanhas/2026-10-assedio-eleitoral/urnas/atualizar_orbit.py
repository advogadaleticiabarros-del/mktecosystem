"""Roda DENTRO do container da API: troca as imagens das 11 peças da campanha pelas versões com urna (Stories v2,
frase v3, carrossel v10, estático v2), guardando a anterior em `corpo.versoes_anteriores`. Não muda status nem
programação; peça já publicada fica como está. Conta as peças por tipo antes e depois. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python - < atualizar_orbit.py
"""
import asyncio
from datetime import datetime, timezone

from sqlalchemy import String, cast, func, select
from sqlalchemy.orm.attributes import flag_modified

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece

V = "urna1"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
NOTA = "antes das fotos de urna (pedido de 27/10/2026: 'Todos inclua fotos das urnas brasileiras')"
STORIES = ["402b9a3e", "283f7a26", "7994b5cc", "ada4ff89", "b01f93c6", "b6abfe07", "29aaf3e7", "437b2d8f"]
ALT_URNA = " Ao fundo, foto real de urna eletrônica brasileira."


def url(nome: str) -> str:
    return f"{MIDIA}/{nome}?v={V}"


def novo_corpo(c: ContentPiece) -> dict | None:
    corpo = dict(c.corpo or {})
    if c.tipo == "stories":
        nova = url(f"story-assedio-eleitoral-v2-{corpo['ordem']}.jpg")
        chave, anterior = "imagem", corpo.get("imagem")
    elif c.tipo == "frase":
        nova, chave, anterior = url("assedio-eleitoral-frase-v3.jpg"), "imagem", corpo.get("imagem")
    elif c.tipo == "estatico":
        nova, chave, anterior = url("assedio-eleitoral-estatico-provas-v2.jpg"), "imagem", corpo.get("imagem")
    elif c.tipo == "carrossel":
        nova = [url(f"assedio-eleitoral-voto-v10-{i}.jpg") for i in range(1, 10)]
        chave, anterior = "imagens", corpo.get("imagens")
    else:
        return None
    if anterior == nova:
        return None
    corpo.setdefault("versoes_anteriores", []).append(
        {chave: anterior, "em": datetime.now(timezone.utc).isoformat(), "nota": NOTA})
    corpo[chave] = nova
    alt = corpo.get("texto_alternativo")
    if alt and ALT_URNA.strip() not in alt:
        corpo["texto_alternativo"] = alt.rstrip() + ALT_URNA
    return corpo


async def contagem(db) -> dict:
    return dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())


async def main():
    async with SessionLocal() as db:
        antes = await contagem(db)
        prefixos = STORIES + ["c9c4e179", "07c91c31", "66ac094b"]
        for pre in prefixos:
            achadas = (await db.execute(select(ContentPiece).where(cast(ContentPiece.id, String).like(f"{pre}%")))).scalars().all()
            if len(achadas) != 1:
                print(pre, "ERRO: achou", len(achadas))
                continue
            c = achadas[0]
            if c.status == "publicado":
                print(pre, c.tipo, "já publicado: não mexi")
                continue
            corpo = novo_corpo(c)
            if corpo is None:
                print(pre, c.tipo, c.status, "já estava na versão com urna")
                continue
            c.corpo = corpo
            flag_modified(c, "corpo")
            print(pre, c.tipo, c.status, "atualizado;", "versões guardadas:", len(corpo["versoes_anteriores"]),
                  "| programação:", corpo.get("programacao"))
        await db.commit()
        depois = await contagem(db)
        print("contagem igual:", antes == depois, sorted(depois.items()))


asyncio.run(main())
