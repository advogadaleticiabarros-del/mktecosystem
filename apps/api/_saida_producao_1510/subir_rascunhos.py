"""Roda DENTRO do container da API. Duas partes:

A) Ajusta a programação já aprovada de 10 a 14/10 às regras do manual (5 hashtags,
   sem convite a contar o caso, primeiro comentário) e põe cada dia do Editorial
   na data em que vai ao ar (remove as duplicatas em rascunho de 02/10 e 04/10).
B) Sobe a produção de 15/10 a 02/11 como RASCUNHO (sem agendamento), cada dia
   numa pauta com data_editorial = data de postagem, para a Letícia aprovar.

Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/prod1510/subir_rascunhos.py
"""
import asyncio
import json
import re
import uuid
from datetime import date
from pathlib import Path

from sqlalchemy import func, select, text

from app.config import settings
from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant

AQUI = Path(__file__).resolve().parent
MIDIA = f"{settings.PUBLIC_API_URL}/media"
U = uuid.UUID

VG = "#ViolênciaDeGênero #LeiMariaDaPenha #MedidaProtetiva #DireitosDaMulher #AdvogadaVitóriaES"
VG_PC = "📚 Base legal: STF, Tema 1.412 (ARE 1.537.713, 19/08/2026); Lei 11.340/2006.\n"
AJUSTES = {
    # piece_id: (hashtags novas ou None, (trecho velho, novo) ou None, primeiro comentário)
    "f827c986-70ab-4555-87b1-91f228b9dc88": (VG, None, VG_PC + "💬 Você sabia que a medida protetiva vale fora de casa também? Marca quem precisa saber."),
    "cbba2da8-e407-4b5c-b14a-f53f435a6d25": (
        "#AbandonoAfetivo #DireitoDeFamília #Lei152402025 #DireitosDaCriança #AdvogadaVitóriaES",
        ("💛 Me conta nos comentários: como foi crescer com essa ausência, ou como você está tentando não repetir isso com os seus filhos?",
         "💛 Salva esse post e manda pra quem carrega essa história."),
        "📚 Base legal: Lei 15.240/2025.\n💬 Deixe um 💛 se esse tema tocou você."),
    "627324f6-717d-4a87-af01-a7580dcd754e": (None, None, "📚 Base legal: Lei 15.240/2025.\n💬 Marca aqui quem precisa ler isso hoje."),
    "931b4eb3-9f46-4801-8833-828c1e2082e5": (
        "#AbandonoAfetivo #DireitoDeFamília #Lei152402025 #DireitosDaCriança #AdvogadaVitóriaES", None,
        "📚 Base legal: Lei 15.240/2025.\n💬 Você já conhecia essa lei?"),
    "cc60dfaf-3367-4aea-8280-fa730a98ab61": (VG, None, VG_PC + "💬 Compartilhe: informação também protege."),
    "840a2801-7a97-46be-962a-567bad77cc91": (
        None, ("Já passou por isso? Me conta nos comentários.", "💛 Salva esse post e manda pra quem cobre férias de colega."),
        "📚 Base legal: Súmula 159 do TST.\n💬 Você já cobriu as férias de um colega? Marca quem também já."),
    "ea2f38a0-3d46-4009-a6bc-be5198362f7b": (None, None, "📚 Base legal: Súmula 159 do TST; CLT, arts. 72 e 462, § 1º.\n💬 Ativa o sininho: hoje às 20h tem o carrossel completo."),
    "5e71d39e-21e9-4a83-8e7f-fe889308b9fe": (
        "#DireitoTrabalhista #CLT #DireitosDoTrabalhador #SalárioSubstituição #AdvogadaVitóriaES", None,
        "📚 Base legal: Súmula 159 do TST; CLT, arts. 72 e 462, § 1º.\n💬 Qual desses direitos você não conhecia?"),
    "3833c9c2-0359-4f69-bcc7-c008f7b50ffe": (VG, None, VG_PC + "💬 Manda pra uma amiga: ninguém deveria descobrir esse direito tarde demais."),
}


def trocar_hashtags(legenda: str, novas: str) -> str:
    linhas = legenda.rstrip().split("\n")
    assert linhas[-1].lstrip().startswith("#"), linhas[-1]
    linhas[-1] = novas
    return "\n".join(linhas)


async def apagar_duplicata(db, pid: str) -> None:
    peca = await db.get(ContentPiece, U(pid))
    refs = (await db.execute(text("select count(*) from marketing_memory where content_piece_id=:i"), {"i": pid})).scalar()
    ags = (await db.execute(select(func.count()).select_from(ScheduledPost).where(ScheduledPost.content_piece_id == U(pid)))).scalar()
    assert peca.status == "rascunho" and refs == 0 and ags == 0, (pid, peca.status, refs, ags)
    await db.delete(peca)


async def parte_a(db) -> None:
    for pid, (tags, troca, pc) in AJUSTES.items():
        peca = await db.get(ContentPiece, U(pid))
        corpo = dict(peca.corpo)
        if troca:
            assert troca[0] in corpo["legenda"], pid
            corpo["legenda"] = corpo["legenda"].replace(troca[0], troca[1])
        if tags:
            corpo["legenda"] = trocar_hashtags(corpo["legenda"], tags)
        assert len(re.findall(r"#\w", corpo["legenda"])) <= 5, pid
        corpo["primeiro_comentario"] = pc
        peca.corpo = corpo

    # Editorial = data em que vai ao ar
    (await db.get(Pauta, U("a3621096-14f4-4b8f-9660-1b1f6354ac77"))).data_editorial = date(2026, 10, 11)
    (await db.get(Pauta, U("97cc950b-084b-4ea6-90b3-435ce285a17e"))).data_editorial = date(2026, 10, 13)
    vg = await db.get(Pauta, U("5d2d18cb-242c-4bf3-b5da-76b7bc12d7dc"))
    vg.data_editorial = date(2026, 10, 10)
    for dia, pid in ((date(2026, 10, 12), "cc60dfaf-3367-4aea-8280-fa730a98ab61"),
                     (date(2026, 10, 14), "3833c9c2-0359-4f69-bcc7-c008f7b50ffe")):
        nova = Pauta(tenant_id=vg.tenant_id, titulo=vg.titulo, angulo=vg.angulo, area=vg.area, origem=vg.origem,
                     fonte=vg.fonte, relevante_para_conteudo=True, status=vg.status, data_editorial=dia)
        db.add(nova)
        await db.flush()
        (await db.get(ContentPiece, U(pid))).pauta_id = nova.id

    # Duplicatas em rascunho de 02/10 e 04/10 (o texto programado é o mesmo)
    orig_art = (await db.get(ContentPiece, U("5acfce01-1359-4d74-8ffa-698ca503d81f"))).corpo.get("html", "")
    copia_art = (await db.get(ContentPiece, U("ed63525b-0b91-4642-9058-2027f640289f"))).corpo.get("html", "")
    texto = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style|head|nav|footer)\b.*?</\1>", "", h))).strip()
    assert texto(copia_art)[:400] in texto(orig_art), "artigo do abandono difere"
    for pid in ("5acfce01-1359-4d74-8ffa-698ca503d81f", "9a77da67-833e-4056-a5f6-22633ecfba35",
                "85439c00-45b4-471b-b2fe-7cec8878c0fb", "c1e01402-5c52-484d-b69d-c8b83a5d0f99"):
        await apagar_duplicata(db, pid)
    (await db.get(ContentPiece, U("37496774-77be-42fa-b816-5e5eebffd17e"))).pauta_id = U("97cc950b-084b-4ea6-90b3-435ce285a17e")
    await db.flush()
    for pauta_id in ("18ba7485-7383-41d5-9b27-1705211ac8f6", "680fa063-def8-4c83-bfa0-64adeed8bc3a"):
        resto = (await db.execute(select(func.count()).select_from(ContentPiece).where(ContentPiece.pauta_id == U(pauta_id)))).scalar()
        assert resto == 0, (pauta_id, resto)
        await db.delete(await db.get(Pauta, U(pauta_id)))
    print("A: 10 a 14/10 ajustados; Editorial por data de postagem")


async def pauta_por_prefixo(db, prefixo: str) -> Pauta:
    return (await db.execute(select(Pauta).where(text("pautas.id::text like :p")).params(p=prefixo + "%"))).scalar_one()


async def parte_b(db, tenant_id) -> None:
    from conteudo import MITO_OU_LEI, TEMAS

    plano = json.loads((AQUI / "plano.json").read_text(encoding="utf-8"))
    pautas_por_dia: dict[str, Pauta] = {}

    for tema in TEMAS:
        if tema["pautas"]:
            principal = await pauta_por_prefixo(db, tema["pautas"][0])
            for extra in tema["pautas"][1:]:
                fundida = await pauta_por_prefixo(db, extra)
                fundida.data_editorial = None
                fundida.status = "guardada"
        else:
            principal = Pauta(tenant_id=tenant_id, titulo=tema["titulo"], angulo="direitos", area=tema["area"],
                              origem="manual", fonte="banco de temas", relevante_para_conteudo=True, status="sugerida")
            db.add(principal)
        principal.titulo = tema["titulo"]
        principal.area = tema["area"]
        principal.status = "em_producao"
        principal.data_editorial = date.fromisoformat(tema["data"])
        await db.flush()
        pautas_por_dia[tema["data"]] = principal

    areas = {t["chave"]: t["area"] for t in TEMAS}
    for dia, chave, af, *_ in MITO_OU_LEI:
        p = Pauta(tenant_id=tenant_id, titulo=f"Mito ou Lei: {af}", angulo="direitos", area=areas[chave],
                  origem="manual", fonte="editorial", relevante_para_conteudo=True, status="em_producao",
                  data_editorial=date.fromisoformat(dia))
        db.add(p)
        await db.flush()
        pautas_por_dia[dia] = p

    criadas = 0
    for item in plano:
        p = pautas_por_dia[item["data"]]
        imagens = [f"{MIDIA}/{n}" for n in item["imagens"]]
        corpo = {"legenda": item["legenda"], "primeiro_comentario": item["primeiro_comentario"],
                 "programacao": {"data": item["data"], "hora": item["hora"]}}
        corpo.update({"imagens": imagens} if item["tipo"] == "carrossel" else {"imagem": imagens[0]})
        if item["tipo"] in ("pergunta", "frase"):
            corpo[item["tipo"]] = item["texto"]
        if item["tipo"] == "estatico":
            corpo["texto_overlay"] = item["texto"]
        db.add(ContentPiece(tenant_id=tenant_id, pauta_id=p.id, tipo=item["tipo"], corpo=corpo, status="rascunho", versao=1))
        criadas += 1
    print("B:", criadas, "peças em rascunho,", len(pautas_por_dia), "dias no Editorial")


async def main():
    import sys
    sys.path.insert(0, str(AQUI))
    async with SessionLocal() as db:
        tenant = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().first()
        await parte_a(db)
        await parte_b(db, tenant.id)
        await db.commit()
        linhas = await db.execute(text("""
            select p.data_editorial, left(p.titulo,45), count(c.id), string_agg(c.tipo||':'||c.status, ' ' order by c.tipo)
            from pautas p left join content_pieces c on c.pauta_id=p.id
            where p.data_editorial between '2026-09-27' and '2026-11-03' group by 1,2 having count(c.id)>0 order by 1"""))
        for linha in linhas:
            print(*linha)


asyncio.run(main())
