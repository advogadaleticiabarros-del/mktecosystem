"""Roda DENTRO do container da API: troca a arte das perguntas, frases e Mito ou Lei de novembro (a partir de 10/11) e
dezembro pela versão no estilo Manchete (pedido da Jessica em 09/11/2026: "Aprovadíssimo! ... altere todos para esse
novo estilo"). Só muda corpo.imagem; o texto, a legenda, o horário e o status ficam como estão. A URL antiga fica em
corpo.imagem_anterior (material pronto nunca some) e peça já publicada não é tocada. Idempotente.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/manchete/trocar_arte_manchete.py [--aplicar]
Sem --aplicar, só mostra o que mudaria. Os JPG precisam estar em /app/media com o nome manchete-<arquivo>.jpg."""
import asyncio
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
import conteudo_dez  # noqa: E402
import conteudo_nov  # noqa: E402

INICIO = "2026-11-10"
MIDIA = Path("/app/media")
V = "manchete1"


def alvos():
    """(data, ângulo da pauta, tipo da peça, arquivo novo)."""
    for mes, dados in (("nov", conteudo_nov), ("dez", conteudo_dez)):
        for t in dados.TEMAS:
            if t["data"] < INICIO:
                continue
            base = f"{mes}-{t['data'][5:]}"
            yield t["data"], "direitos", "pergunta", f"manchete-{base}-pergunta-{t['chave']}.jpg"
            yield t["data"], "direitos", "frase", f"manchete-{base}-frase-{t['chave']}.jpg"
        for m in dados.MITO_OU_LEI:
            if m[0] < INICIO:
                continue
            yield m[0], "mito", "estatico", f"manchete-{mes}-{m[0][5:]}-mito-{m[1]}.jpg"


async def main(aplicar):
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        trocadas, avisos = 0, []
        for dia, angulo, tipo, arquivo in alvos():
            if not (MIDIA / arquivo).exists():
                avisos.append(f"sem arquivo em /app/media: {arquivo}")
                continue
            pecas = (await db.execute(select(ContentPiece).join(Pauta, ContentPiece.pauta_id == Pauta.id).where(
                Pauta.tenant_id == tid, Pauta.data_editorial == date.fromisoformat(dia), Pauta.angulo == angulo,
                ContentPiece.tipo == tipo))).scalars().all()
            if len(pecas) != 1:
                avisos.append(f"{dia} {tipo}: {len(pecas)} peças encontradas, nada trocado")
                continue
            p = pecas[0]
            corpo = dict(p.corpo or {})
            novo = f"{settings.PUBLIC_API_URL}/media/{arquivo}?v={V}"
            if p.status == "publicado":
                avisos.append(f"{dia} {tipo}: já publicada, mantida")
                continue
            if corpo.get("imagem") == novo:
                continue
            print(f"{dia} {tipo:9} {p.status:9} {corpo.get('imagem', '')[-40:]} -> {arquivo}")
            if aplicar:
                corpo.setdefault("imagem_anterior", corpo.get("imagem"))
                corpo["imagem"] = novo
                p.corpo = corpo
            trocadas += 1
        if aplicar:
            await db.commit()
        print(("trocadas: " if aplicar else "trocaria: ") + str(trocadas))
        print("\n".join(avisos))


asyncio.run(main("--aplicar" in sys.argv))
