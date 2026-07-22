from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.async_api import async_playwright

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

ACABAMENTO_DOURADO_PATH = Path(__file__).parent.parent / "assets" / "acabamento-dourado.png"


def _aplicar_acabamento_dourado(caminho_imagem: str) -> None:
    """Compõe as barras de gradiente dourado (topo/rodapé) sobre a imagem final.

    Toque de marca fixo em toda peça gerada (carrossel, criativo único, capa) —
    não é opcional, decisão da usuária em 2026-07-22.
    """
    base = Image.open(caminho_imagem).convert("RGBA")
    acabamento = Image.open(ACABAMENTO_DOURADO_PATH).convert("RGBA")
    if acabamento.size != base.size:
        acabamento = acabamento.resize(base.size)
    composto = Image.alpha_composite(base, acabamento)
    composto.convert("RGB").save(caminho_imagem)


async def renderizar_slide(
    texto: str,
    indice: int,
    total: int,
    identidade_visual: dict,
    caminho_saida: str,
    nome_conta: str = "LETÍCIA BARROS",
    instagram: str = "@adv.leticiabarros2",
) -> None:
    cores = identidade_visual.get("cores", {})
    capa = indice == 0
    final = indice == total - 1
    html = _env.get_template("carrossel_slide.html").render(
        texto=texto,
        fundo=cores.get("fundo_escuro", "#231E1A"),
        dourado=cores.get("dourado", "#C9A962"),
        areia=cores.get("areia", "#E8DED1"),
        tamanho_fonte=72 if capa else 60 if final else 52,
        peso_fonte=700 if capa or final else 500,
        nome_conta=nome_conta,
        instagram=instagram,
        rodape_direita="OAB/ES 39.948" if final else f"{indice + 1} / {total}",
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html)
        await page.screenshot(path=caminho_saida)
        await browser.close()

    _aplicar_acabamento_dourado(caminho_saida)
