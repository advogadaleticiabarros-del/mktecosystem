import base64
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.async_api import async_playwright

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

ASSETS_DIR = Path(__file__).parent.parent / "assets"
ACABAMENTO_DOURADO_PATH = ASSETS_DIR / "acabamento-dourado.png"
LOGO_PATH = ASSETS_DIR / "logo-leticia.png"


def _logo_data_uri() -> str:
    dados = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{dados}"


def _foto_data_uri(caminho_foto: str) -> str:
    caminho = Path(caminho_foto)
    mime = "image/png" if caminho.suffix.lower() == ".png" else "image/jpeg"
    dados = base64.b64encode(caminho.read_bytes()).decode()
    return f"data:{mime};base64,{dados}"


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
    nome_conta: str = "Letícia Barros",
    instagram: str = "@adv.leticiabarros2",
    foto_path: str | None = None,
    foto_posicao: str = "center",
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
        indice=indice,
        total=total,
        final=final,
        logo_src=_logo_data_uri(),
        foto_src=_foto_data_uri(foto_path) if foto_path else None,
        foto_posicao=foto_posicao,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html)
        await page.screenshot(path=caminho_saida)
        await browser.close()

    _aplicar_acabamento_dourado(caminho_saida)
