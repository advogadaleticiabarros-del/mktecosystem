from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.async_api import async_playwright

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)

MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]

BLOG_BASE_URL = "https://advogadaleticiabarros.com.br/blog/"


def estimar_tempo_leitura(html: str) -> int:
    texto = BeautifulSoup(html, "html.parser").get_text()
    palavras = len(texto.split())
    return max(1, round(palavras / 200))


def renderizar_artigo_html(
    *,
    titulo: str,
    meta_description: str,
    categoria: str,
    resumo: str,
    corpo_html: str,
    slug: str,
    data_publicacao: date,
    whatsapp: str = "5527995151402",
    oab: str = "OAB/ES 39.948",
) -> str:
    data_extenso = f"{data_publicacao.day} de {MESES[data_publicacao.month - 1]} de {data_publicacao.year}"
    template = _env.get_template("blog_artigo.html")
    return template.render(
        titulo=titulo,
        meta_description=meta_description,
        categoria=categoria,
        resumo=resumo,
        corpo_html=corpo_html,
        canonical_url=f"{BLOG_BASE_URL}{slug}.html",
        capa_url=f"{BLOG_BASE_URL}capas/{slug}.png",
        data_iso=data_publicacao.isoformat(),
        data_extenso=data_extenso,
        tempo_leitura=estimar_tempo_leitura(corpo_html),
        whatsapp=whatsapp,
        oab=oab,
    )


async def renderizar_capa_artigo(
    *,
    titulo: str,
    categoria: str,
    identidade_visual: dict,
    caminho_saida: str,
) -> None:
    cores = identidade_visual.get("cores", {})
    html = _env.get_template("capa_artigo.html").render(
        titulo=titulo,
        categoria=categoria,
        fundo=cores.get("fundo_escuro", "#231E1A"),
        dourado=cores.get("dourado", "#C9A962"),
        areia=cores.get("areia", "#E8DED1"),
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 630})
        await page.set_content(html)
        await page.screenshot(path=caminho_saida)
        await browser.close()
