import base64
import re
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
    cta_texto: str = "⚖️ Procure uma advogada",
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
        cta_texto=cta_texto,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.screenshot(path=caminho_saida)
        await browser.close()

    _aplicar_acabamento_dourado(caminho_saida)


async def renderizar_frase_impacto(
    frase_html: str,
    identidade_visual: dict,
    caminho_saida: str,
    nome_conta: str = "Letícia Barros",
    oab: str = "OAB/ES 39.948",
) -> None:
    """Card tipográfico de frase de impacto — sem foto, pensado pra compartilhar.

    `frase_html` pode usar <em>destaque</em> pra colorir de dourado a parte
    decisiva da frase.
    """
    cores = identidade_visual.get("cores", {})
    tamanho_fonte = 72 if len(frase_html) < 90 else 60 if len(frase_html) < 140 else 50
    html = _env.get_template("frase_impacto.html").render(
        frase=frase_html,
        fundo=cores.get("fundo_escuro", "#231E1A"),
        dourado=cores.get("dourado", "#C9A962"),
        areia=cores.get("areia", "#E8DED1"),
        tamanho_fonte=tamanho_fonte,
        nome_conta=nome_conta,
        oab=oab,
        logo_src=_logo_data_uri(),
    )
    await _fotografar(html, caminho_saida)


PERFIL_PATH = ASSETS_DIR / "perfil-leticia.jpg"

# Linha de cima do cabeçalho conforme a área ("Direito do / Consumidor").
_PREFIXO_AREA = {"Consumidor": "Direito do", "Família": "Direito de"}


def html_pergunta(
    pergunta: str,
    identidade_visual: dict,
    *,
    area: str = "Advocacia",
    rotulo: str = "Me faça uma pergunta",
    foto_src: str | None = None,
    foto_posicao: str = "50% 50%",
    brilho: float = 0.95,
    desce: int = 0,
    nome_conta: str = "Letícia Barros",
    instagram: str = "adv.leticiabarros2",
) -> str:
    """Pergunta no padrão aprovado (v6, 09/10/2026): foto inteira com um objeto do tema,
    caixa de vidro centralizada, trecho-chave em `<em>` (itálico dourado). `desce` empurra
    a foto para baixo quando o objeto ficaria atrás da caixa."""
    cores = identidade_visual.get("cores", {})
    n = len(re.sub(r"<[^>]+>", "", pergunta))
    return _env.get_template("pergunta_card.html").render(
        pergunta=pergunta,
        rotulo=rotulo,
        area=area if area != "Advocacia" else "OAB/ES 39.948",
        area_linha1=_PREFIXO_AREA.get(area, "Direito") if area != "Advocacia" else "Advogada",
        fundo=cores.get("fundo_escuro", "#231E1A"),
        dourado=cores.get("dourado", "#C9A962"),
        areia=cores.get("areia", "#E8DED1"),
        tamanho_fonte=62 if n <= 70 else 58 if n <= 85 else 54 if n <= 110 else 48,
        nome_conta=nome_conta,
        instagram=instagram,
        logo_src=_logo_data_uri(),
        perfil_src=_foto_data_uri(str(PERFIL_PATH)),
        foto_src=foto_src,
        foto_posicao=foto_posicao,
        brilho=brilho,
        desce=desce,
    )


async def renderizar_pergunta(
    pergunta: str,
    identidade_visual: dict,
    caminho_saida: str,
    *,
    foto_path: str | None = None,
    **opcoes,
) -> None:
    """Card da dúvida real de uma cliente; a resposta vai na legenda."""
    html = html_pergunta(pergunta, identidade_visual, foto_src=_foto_data_uri(foto_path) if foto_path else None, **opcoes)
    await _fotografar(html, caminho_saida)


async def _fotografar(html: str, caminho_saida: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.screenshot(path=caminho_saida)
        await browser.close()

    _aplicar_acabamento_dourado(caminho_saida)
