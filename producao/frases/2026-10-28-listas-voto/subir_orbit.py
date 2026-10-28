"""Roda DENTRO do container da API: cria, em RASCUNHO, o carrossel das 4 frases sobre as listas por causa do voto
(28/10/2026), com a legenda explicativa (seção 0 de LEGENDAS.md). A Jessica aprova no Editorial ou posta à mão.
Precisa de /tmp/listas-voto/ com este script e LEGENDAS.md, e dos JPGs em /app/media.
Conta as peças por tipo antes e depois (nada pode sumir). Idempotente; se o rascunho já existe, só atualiza a legenda.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/listas-voto/subir_orbit.py
"""
import asyncio
import re
from datetime import date
from pathlib import Path

from sqlalchemy import func, select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

AQUI = Path(__file__).resolve().parent
HOJE = date(2026, 10, 28)
TITULO = "Listas por causa do voto: frases-notícia (28/10)"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
IMAGENS = ["listas-voto-1-listas-cachoeiro.jpg", "listas-voto-2-listas-6-cidades-es.jpg",
           "listas-voto-3-seu-nome-na-lista.jpg", "listas-voto-4-recebeu-lista.jpg"]
COMENTARIO = "Passo a passo das provas e de como denunciar, inclusive no ES: advogadaleticiabarros.com.br/voto"
ALT = ("Cachoeiro, Vitória, Colatina: listas por causa do voto no ES. Não repasse, quem repassa também responde. "
       "Dra. Letícia Barros, OAB/ES 39.948, e Dra. Carolina Prado, OAB/ES 29.557.")


def legenda_explicativa() -> str:
    texto = (AQUI / "LEGENDAS.md").read_text(encoding="utf-8")
    secao = re.search(r"^## 0\. legenda-explicativa\s*$(.*?)^## 1\.", texto, flags=re.M | re.S).group(1)
    return secao[secao.index("🚨"):].strip()


async def contagem(db) -> dict:
    return dict((await db.execute(select(ContentPiece.tipo, func.count()).group_by(ContentPiece.tipo))).all())


async def main():
    legenda = legenda_explicativa()
    async with SessionLocal() as db:
        antes = await contagem(db)
        tid = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one().id
        p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == TITULO))).scalars().first()
        if not p:
            p = Pauta(tenant_id=tid, titulo=TITULO, angulo="frases tipográficas, notícia direta", area="Trabalhista",
                      origem="manual", fonte="A Gazeta 28/10/2026; CF arts. 5º e 14; CP arts. 139, 140, 147, 147-A; "
                      "Lei 9.029/1995", relevante_para_conteudo=True, status="em_producao", data_editorial=HOJE)
            db.add(p)
            await db.flush()
        existentes = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == p.id,
                                                                  ContentPiece.tipo == "carrossel"))).scalars().all()
        if existentes:
            c = existentes[0]
            if c.status == "rascunho" and (c.corpo or {}).get("legenda") != legenda:
                c.corpo = {**c.corpo, "legenda": legenda, "legenda_facebook": legenda}
                print("legenda atualizada", c.id, len(legenda))
            else:
                print("já existia", c.id)
        else:
            c = ContentPiece(tenant_id=tid, pauta_id=p.id, tipo="carrossel", status="rascunho", versao=1, corpo={
                "imagens": [f"{MIDIA}/{n}" for n in IMAGENS], "legenda": legenda, "primeiro_comentario": COMENTARIO,
                "legenda_facebook": legenda, "texto_alternativo": ALT,
                "programacao": {"data": "2026-10-28", "hora": "18:00"}})
            db.add(c)
            await db.flush()
            print("criado carrossel", c.id)
        await db.commit()
        depois = await contagem(db)
        print("antes:", antes)
        print("depois:", depois)
        print("sumiu:", {t: n for t, n in antes.items() if depois.get(t, 0) < n} or "nada")
        print("pauta", p.id)


asyncio.run(main())
