"""Cria no Orbit a programação de 08 a 14/10/2026 (roda dentro do container da API).

Para cada post do plano.json: pauta do tema (uma por tema), peça aprovada com a
arte pronta (imagem/imagens em /media) e a legenda, e o agendamento no horário
da regra. Mais os dois artigos do blog (10h dos dias de tema) com capa pronta.
Idempotente: se já existir agendamento para o mesmo (data, horário, tema), pula.

Uso: docker compose exec -T api python /tmp/prog/_programar.py
"""
import asyncio
import json
import re
from datetime import date
from html import unescape
from pathlib import Path

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant

AQUI = Path(__file__).resolve().parent
MIDIA = f"{settings.PUBLIC_API_URL}/media"
AREA = {
    "Assédio eleitoral no trabalho": "Trabalhista",
    "Guarda compartilhada de pet": "Família",
    "Abandono afetivo": "Família",
    "3 direitos trabalhistas pouco conhecidos": "Trabalhista",
    "Violência de gênero (STF)": "Família",
}
FORMATO = {"pergunta": "post", "frase": "post", "estatico": "post", "carrossel": "carrossel"}


def artigo(arquivo_artigo: Path, arquivo_corpo: Path, capa: str) -> dict:
    s = arquivo_artigo.read_text(encoding="utf-8")
    titulo = unescape(re.search(r"<title>(.*?)\s*\|", s).group(1)).strip()
    meta = unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    slug = re.search(r'rel="canonical" href="[^"]*/blog/([^"]+)\.html"', s).group(1)
    return {"titulo": titulo, "html": arquivo_corpo.read_text(encoding="utf-8"), "meta_description": meta,
            "resumo": meta, "slug": slug, "capa_arquivo": capa}


async def main():
    plano = json.loads((AQUI / "plano.json").read_text(encoding="utf-8"))
    blog = [
        ("2026-10-09", "Guarda compartilhada de pet",
         artigo(AQUI / "artigo-pets.html", AQUI / "corpo-pets.html", "capa-pet-blog.png")),
        ("2026-10-11", "Abandono afetivo",
         artigo(AQUI / "artigo-abandono-afetivo.html", AQUI / "corpo-abandono-afetivo.html", "capa-abandono-blog.png")),
    ]
    async with SessionLocal() as db:
        tenant = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first()
        pautas: dict[str, Pauta] = {}

        async def pauta(tema: str) -> Pauta:
            if tema not in pautas:
                p = Pauta(tenant_id=tenant.id, titulo=tema, angulo="direitos", area=AREA[tema], origem="manual",
                          fonte="editorial", relevante_para_conteudo=True, status="em_producao")
                db.add(p)
                await db.flush()
                pautas[tema] = p
            return pautas[tema]

        async def agendar(tipo, tema, corpo, data, hora, canal, formato):
            ja = (await db.execute(select(ScheduledPost).where(
                ScheduledPost.tenant_id == tenant.id, ScheduledPost.data_agendada == date.fromisoformat(data),
                ScheduledPost.horario == hora, ScheduledPost.titulo == tema, ScheduledPost.canal == canal,
            ))).scalar_one_or_none()
            if ja:
                print("já existia:", data, hora, tipo, tema)
                return
            p = await pauta(tema)
            piece = ContentPiece(tenant_id=tenant.id, pauta_id=p.id, tipo=tipo, corpo=corpo, status="aprovado", versao=1)
            db.add(piece)
            await db.flush()
            db.add(ScheduledPost(tenant_id=tenant.id, content_piece_id=piece.id, titulo=tema, canal=canal,
                                 formato=formato, data_agendada=date.fromisoformat(data), horario=hora, status="pronto"))
            print("agendado:", data, hora, canal, tipo, tema)

        for item in plano:
            imagens = [f"{MIDIA}/{n}" for n in item["imagens"]]
            corpo = {"legenda": item["legenda"]}
            corpo.update({"imagens": imagens} if item["tipo"] == "carrossel" else {"imagem": imagens[0]})
            await agendar(item["tipo"], item["tema"], corpo, item["data"], item["hora"], "instagram",
                          FORMATO[item["tipo"]])
        for data, tema, corpo in blog:
            await agendar("artigo", tema, corpo, data, "10:00", "blog", "artigo")
        await db.commit()


asyncio.run(main())
