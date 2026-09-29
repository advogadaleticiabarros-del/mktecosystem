"""Importa o backlog de editorial já produzido nas pastas do Desktop pro banco do Orbit.

Script avulso, rodado manualmente uma vez (não é feature do produto).
Assume a estrutura já em uso:

    C:\\Users\\prosy\\Desktop\\Editorial\\AAAA-MM\\DD-MM-AAAA\\
        blog\\ (capa.png, artigo-pronto-para-publicar.html, link.txt opcional)
        carrossel\\ (slide-1.png..slide-N.png, legenda.html)
        pergunta\\ (criativo.png, legenda.html)
        story\\ (story-artigo-no-ar.png)

Uso:
    python scripts/importar_editorial_desktop.py --dry-run
    python scripts/importar_editorial_desktop.py
    python scripts/importar_editorial_desktop.py --tenant-id <uuid> --raiz "C:\\...\\Editorial"
"""
import argparse
import asyncio
import re
import shutil
import sys
import uuid
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select  # noqa: E402

from app.config import settings  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models.content_piece import ContentPiece  # noqa: E402
from app.models.pauta import Pauta  # noqa: E402

MEDIA_DIR = Path(__file__).parent.parent / "media"
PASTA_PARA_TIPO = {"carrossel": "carrossel", "pergunta": "pergunta", "story": "stories"}
NOME_LEGENDA_HTML = re.compile(r'<div class="legenda">(.*?)</div>\s*<p class="dica">', re.DOTALL)


def extrair_titulo_do_index(pasta_dia: Path) -> str | None:
    index = pasta_dia / "index.html"
    if not index.exists():
        return None
    match = re.search(r"Tema:\s*([^<\n]+)", index.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else None


def extrair_legenda(caminho_legenda_html: Path) -> str:
    conteudo = caminho_legenda_html.read_text(encoding="utf-8")
    match = NOME_LEGENDA_HTML.search(conteudo)
    if not match:
        return ""
    return match.group(1).strip()


def copiar_imagem(caminho_origem: Path) -> str:
    extensao = caminho_origem.suffix.lower()
    nome_novo = f"{uuid.uuid4()}{extensao}"
    shutil.copy2(caminho_origem, MEDIA_DIR / nome_novo)
    return f"{settings.PUBLIC_API_URL}/media/{nome_novo}"


async def importar_pasta_dia(db, tenant_id: uuid.UUID, pasta_dia: Path, dry_run: bool) -> None:
    try:
        data_editorial = datetime.strptime(pasta_dia.name, "%d-%m-%Y").date()
    except ValueError:
        print(f"  pulando (nome de pasta inesperado): {pasta_dia.name}")
        return

    titulo = extrair_titulo_do_index(pasta_dia) or pasta_dia.name

    pauta_existente = await db.execute(
        select(Pauta).where(
            Pauta.tenant_id == tenant_id,
            Pauta.data_editorial == data_editorial,
            Pauta.titulo == titulo,
        )
    )
    pauta = pauta_existente.scalar_one_or_none()

    print(f"\n=== {pasta_dia.name} — {titulo} ===")
    if pauta is None:
        print(f"  criaria Pauta (data_editorial={data_editorial}, titulo={titulo!r})")
        if not dry_run:
            pauta = Pauta(
                tenant_id=tenant_id,
                titulo=titulo,
                angulo="direitos",
                area="",
                origem="manual",
                fonte="manual",
                relevante_para_conteudo=True,
                status="sugerida",
                data_editorial=data_editorial,
            )
            db.add(pauta)
            await db.flush()
    else:
        print(f"  Pauta já existe (id={pauta.id}), reaproveitando")

    for nome_pasta, tipo in PASTA_PARA_TIPO.items():
        pasta_formato = pasta_dia / nome_pasta
        if not pasta_formato.exists():
            continue

        slides = sorted(pasta_formato.glob("slide-*.png"))
        imagens_unicas = [
            f for f in pasta_formato.glob("*.png") if not f.name.startswith("slide-")
        ]
        legenda_html = pasta_formato / "legenda.html"
        legenda_texto = extrair_legenda(legenda_html) if legenda_html.exists() else ""

        if tipo == "carrossel" and slides:
            print(f"  [{tipo}] {len(slides)} slides + legenda ({len(legenda_texto)} chars)")
            if not dry_run:
                urls = [copiar_imagem(s) for s in slides]
                db.add(
                    ContentPiece(
                        tenant_id=tenant_id,
                        pauta_id=pauta.id,
                        tipo="carrossel",
                        corpo={"imagens": urls, "legenda": legenda_texto},
                        status="rascunho",
                        versao=1,
                    )
                )
        elif tipo in {"pergunta", "stories"} and imagens_unicas:
            print(f"  [{tipo}] 1 imagem + legenda ({len(legenda_texto)} chars)")
            if not dry_run:
                url = copiar_imagem(imagens_unicas[0])
                corpo = {"imagem": url, "legenda": legenda_texto}
                if tipo == "pergunta":
                    corpo["pergunta"] = ""
                db.add(
                    ContentPiece(
                        tenant_id=tenant_id,
                        pauta_id=pauta.id,
                        tipo=tipo,
                        corpo=corpo,
                        status="rascunho",
                        versao=1,
                    )
                )

    pasta_blog = pasta_dia / "blog"
    capa = pasta_blog / "capa.png"
    artigo_html = pasta_blog / "artigo-pronto-para-publicar.html"
    if pasta_blog.exists() and (capa.exists() or artigo_html.exists()):
        print(f"  [blog] capa={capa.exists()} artigo_html={artigo_html.exists()}")
        if not dry_run:
            corpo = {}
            if capa.exists():
                corpo["imagem_capa"] = copiar_imagem(capa)
            if artigo_html.exists():
                corpo["html"] = artigo_html.read_text(encoding="utf-8")
            db.add(
                ContentPiece(
                    tenant_id=tenant_id,
                    pauta_id=pauta.id,
                    tipo="artigo",
                    corpo=corpo,
                    status="rascunho",
                    versao=1,
                )
            )

    if not dry_run:
        await db.commit()


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raiz", default=r"C:\Users\prosy\Desktop\Editorial")
    parser.add_argument("--tenant-id", required=True, help="UUID do tenant (Letícia Barros)")
    parser.add_argument("--dry-run", action="store_true", help="Só lista o que seria criado")
    args = parser.parse_args()

    tenant_id = uuid.UUID(args.tenant_id)
    raiz = Path(args.raiz)
    if not raiz.exists():
        print(f"Pasta raiz não encontrada: {raiz}")
        return

    MEDIA_DIR.mkdir(exist_ok=True)

    pastas_dia = sorted(
        p for pasta_mes in raiz.iterdir() if pasta_mes.is_dir()
        for p in pasta_mes.iterdir() if p.is_dir()
    )
    print(f"{len(pastas_dia)} pasta(s) de dia encontrada(s) em {raiz}")
    if args.dry_run:
        print("MODO DRY-RUN: nada será gravado no banco nem copiado para media/\n")

    async with SessionLocal() as db:
        for pasta_dia in pastas_dia:
            await importar_pasta_dia(db, tenant_id, pasta_dia, args.dry_run)

    print("\nConcluído.")


if __name__ == "__main__":
    asyncio.run(main())
