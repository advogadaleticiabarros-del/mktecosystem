"""Roda DENTRO do container da API: cria as 5 frases da campanha do voto (28/10/2026) como RASCUNHO no Orbit.
Precisa de /tmp/voto-frases/ com este script, LEGENDAS.md e os JPGs (copiados também para /app/media).
Idempotente: não duplica peça com a mesma imagem na pauta.
Uso: docker exec -w /app -e PYTHONPATH=/app <api> python /tmp/voto-frases/subir_orbit.py
"""
import asyncio
import re
from datetime import date
from pathlib import Path

from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant

AQUI = Path(__file__).resolve().parent
HOJE = date(2026, 10, 28)
TITULO = "Assédio eleitoral: frases no estilo de referência (28/10)"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
COMENTARIO = "Passo a passo das provas e de como denunciar, inclusive no ES: advogadaleticiabarros.com.br/voto"

# (arquivo da arte, texto da frase, data, hora)
FRASES = [
    ("frase-demitido-posicao-politica", "Se você for demitido por sua posição política, nosso escritório vai te atender gratuitamente!", "2026-10-28", "19:00"),
    ("frase-eleicao-acabou", "A eleição acabou. As denúncias, não: mais de 500 em dois dias.", "2026-10-29", "12:00"),
    ("frase-2364-denuncias-es", "2.364 denúncias em 2026. 47 no Espírito Santo. Seu voto não pode custar o seu emprego.", "2026-10-30", "12:00"),
    ("frase-500-denuncias-ilegal", "Mais de 500 denúncias depois do 2º turno. Não importa em quem você votou: isso é ilegal.", "2026-10-31", "12:00"),
    ("frase-escritorio-orientar", "Se você for demitido por sua posição política, nosso escritório está aqui para te orientar.", "2026-11-01", "12:00"),
]


def legendas() -> dict[str, str]:
    texto = (AQUI / "LEGENDAS.md").read_text(encoding="utf-8")
    partes = re.split(r"^## \d+\. (\S+)\s*$", texto, flags=re.M)
    return {partes[i]: partes[i + 1].strip() for i in range(1, len(partes), 2)}


async def main():
    leg = legendas()
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one().id
        p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.titulo == TITULO))).scalars().first()
        if not p:
            p = Pauta(tenant_id=tid, titulo=TITULO, angulo="frases tipográficas", area="Trabalhista", origem="manual",
                      fonte="producao/frases/2026-10-28-demitido-posicao-politica",
                      relevante_para_conteudo=True, status="em_producao", data_editorial=HOJE)
            db.add(p)
            await db.flush()
        existentes = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == p.id))).scalars().all()
        imagens = {(c.corpo or {}).get("imagem") for c in existentes}
        for nome, frase, dia, hora in FRASES:
            imagem = f"{MIDIA}/voto-{nome}.jpg"
            if imagem in imagens:
                print("já existia", nome)
                continue
            corpo = {"imagem": imagem, "frase": frase, "legenda": leg[nome], "primeiro_comentario": COMENTARIO,
                     "texto_alternativo": f"{frase} Letícia Barros, advogada trabalhista em Vitória-ES, OAB/ES 39.948.",
                     "programacao": {"data": dia, "hora": hora}}
            c = ContentPiece(tenant_id=tid, pauta_id=p.id, tipo="frase", corpo=corpo, status="rascunho", versao=1)
            db.add(c)
            await db.flush()
            print("criada", nome, dia, hora, c.id)
        await db.commit()
        print("pauta", p.id)


asyncio.run(main())
