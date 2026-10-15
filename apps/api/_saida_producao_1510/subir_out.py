"""Roda DENTRO do container da API: sobe as peças de 15/10/2026 como RASCUNHO, com programação para hoje.
- 6 artigos de atualidade (artigos_out.py), 1 por hora das 10h às 15h; o publicador do blog sobe no minuto :15
  depois que a Letícia aprovar no Editorial.
- 6 Stories "Leia o artigo no link" (tipo stories): o Orbit não publica Stories; ela posta pelo app com o
  adesivo de link (a legenda da peça traz o link e o passo a passo).
- Homenagem ao Dia dos Professores (frase v2) às 10h.
Cria as pautas do dia se não existirem. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/out/subir_out.py
"""
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from artigos_out import ARTIGOS, B  # noqa: E402

V = "out1"
MIDIA = f"{settings.PUBLIC_API_URL}/media"
HOJE = date(2026, 10, 15)

LEGENDA_PROF = """Hoje é Dia dos Professores, e eu não poderia deixar passar em branco.

Antes da OAB, antes do primeiro processo, antes de qualquer audiência, teve alguém me ensinando a ler, a escrever e a perguntar o porquê das coisas.

Cada direito que eu explico aqui começou numa sala de aula. Na alfabetização, na escola, na faculdade de Direito.

Aos professores que acreditaram em mim quando eu ainda nem sabia o caminho: obrigada. E a todos que seguem ensinando, com sala cheia e coração inteiro: vocês mudam vidas todos os dias.

Marque aqui um professor que marcou a sua história. 💛

Dra. Letícia Barros · OAB/ES 39.948

#diadosprofessores #professores #gratidao #educacao #vitoriaes"""

PC_PROF = "Qual professor marcou a sua vida? Conta aqui o nome e o que ele te ensinou. 📚"


def url(nome: str) -> str:
    return f"{MIDIA}/{nome}?v={V}"


def legenda_story(a: dict) -> str:
    link = f"{B}{a['slug']}.html"
    h = int(a["hora"][:2])
    return (f"Story para postar depois que o artigo estiver no ar (a partir das {h}h20).\n\n"
            f"No Instagram: Story > escolher esta imagem > adesivo LINK > colar:\n{link}\n"
            "Texto do adesivo: Ler o artigo. Posicione o adesivo logo abaixo de \"LEIA O ARTIGO NO LINK\".\n\n"
            "Opcional: adicionar a enquete \"Você já sabia?\" (Sim / Não) para aumentar as respostas.")


async def pauta(db, tid, titulo: str, angulo: str, area: str) -> Pauta:
    p = (await db.execute(select(Pauta).where(Pauta.tenant_id == tid, Pauta.data_editorial == HOJE,
                                              Pauta.titulo == titulo))).scalars().first()
    if not p:
        p = Pauta(tenant_id=tid, titulo=titulo, angulo=angulo, area=area, origem="manual",
                  fonte="Atualidades 15/10/2026 (fontes no artigo)", relevante_para_conteudo=True,
                  status="em_producao", data_editorial=HOJE)
        db.add(p)
        await db.flush()
    return p


async def criar(db, tid, p: Pauta, tipo: str, corpo: dict) -> bool:
    ja = (await db.execute(select(ContentPiece).where(ContentPiece.pauta_id == p.id, ContentPiece.tipo == tipo))).scalars().first()
    if ja:
        return False
    db.add(ContentPiece(tenant_id=tid, pauta_id=p.id, tipo=tipo, corpo=corpo, status="rascunho", versao=1))
    return True


async def main():
    async with SessionLocal() as db:
        tid = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first().id
        n = 0
        for a in ARTIGOS:
            area = "Família" if a["categoria"] == "Direito de Família" else "Trabalhista"
            p = await pauta(db, tid, a["pauta"], "artigo", area)
            capa = f"capa-{a['slug']}.jpg"
            n += await criar(db, tid, p, "artigo", {
                "titulo": a["titulo"], "slug": a["slug"], "html": a["html"], "meta_description": a["meta"],
                "resumo": a["resumo"], "capa_arquivo": capa, "imagem_capa": url(capa),
                "legenda": "Post para o Perfil da Empresa no Google (Adicionar atualização):\n\n" + a["post_google"],
                "programacao": {"data": a["data"], "hora": a["hora"]}})
            h = int(a["hora"][:2])
            n += await criar(db, tid, p, "stories", {
                "imagem": url(f"story-{a['slug']}.jpg"), "legenda": legenda_story(a),
                "link": f"{B}{a['slug']}.html", "programacao": {"data": a["data"], "hora": f"{h:02d}:30"}})
        p = await pauta(db, tid, "Dia dos Professores (homenagem)", "data", "Institucional")
        n += await criar(db, tid, p, "frase", {
            "imagem": url("professores-2026-frase-v2.jpg"),
            "frase": "Toda advogada um dia foi aluna. Obrigada, professores, por cada lição que virou caminho.",
            "legenda": LEGENDA_PROF, "primeiro_comentario": PC_PROF, "programacao": {"data": "2026-10-15", "hora": "10:00"}})
        await db.commit()
        print("peças criadas em rascunho:", n)


asyncio.run(main())
