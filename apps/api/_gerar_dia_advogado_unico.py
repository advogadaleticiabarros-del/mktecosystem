import asyncio
import base64
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

from app.services.render_criativo import _aplicar_acabamento_dourado

TEMPLATES_DIR = Path(__file__).parent / "app" / "templates"
ASSETS_DIR = Path(__file__).parent / "app" / "assets"
_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
DOWNLOADS = Path(r"C:\Users\prosy\Downloads")
FUNDO = DOWNLOADS / "fundo.jpg"
LOGO = ASSETS_DIR / "logo-leticia.png"

PESSOAS = [
    DOWNLOADS / "FEED LETICIA.png",
    DOWNLOADS / "FEED LETICIA2.png",
    DOWNLOADS / "FEED LETICIA3.png",
    DOWNLOADS / "FEED LETICIA4.png",
]


def _data_uri(caminho: Path) -> str:
    mime = "image/png" if caminho.suffix.lower() == ".png" else "image/jpeg"
    dados = base64.b64encode(caminho.read_bytes()).decode()
    return f"data:{mime};base64,{dados}"


async def renderizar_versao(
    pessoa_path: Path,
    caminho_saida: Path,
    kicker: str = "Dia <em>do</em> Advogado",
    titulo: str = "Feliz dia!",
    script: str = "Parabéns",
    impacto: str = "",
    apoio: str = "Nossa homenagem a quem transforma o <strong>Direito</strong> em segurança para todos.",
) -> None:
    cores = IDENTIDADE["cores"]
    html = _env.get_template("dia_advogado_unico.html").render(
        fundo=cores["fundo_escuro"],
        dourado=cores["dourado"],
        areia=cores["areia"],
        nome_conta="Letícia Barros",
        instagram="@adv.leticiabarros2",
        oab="OAB/ES 39.948",
        fundo_src=_data_uri(FUNDO),
        pessoa_src=_data_uri(pessoa_path),
        logo_src=_data_uri(LOGO),
        kicker=kicker,
        titulo=titulo,
        script=script,
        impacto=impacto,
        apoio=apoio,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html)
        await page.screenshot(path=str(caminho_saida))
        await browser.close()

    _aplicar_acabamento_dourado(str(caminho_saida))


async def renderizar_capa_reels(
    pessoa_path: Path,
    caminho_saida: Path,
    kicker: str = "Dia <em>do</em> Advogado",
    titulo: str = "Feliz dia!",
    script: str = "Parabéns",
    impacto: str = "",
    apoio: str = "Nossa homenagem a quem transforma o <strong>Direito</strong> em segurança para todos.",
) -> None:
    cores = IDENTIDADE["cores"]
    html = _env.get_template("dia_advogado_reels_capa.html").render(
        fundo=cores["fundo_escuro"],
        dourado=cores["dourado"],
        areia=cores["areia"],
        nome_conta="Letícia Barros",
        instagram="@adv.leticiabarros2",
        oab="OAB/ES 39.948",
        fundo_src=_data_uri(FUNDO),
        pessoa_src=_data_uri(pessoa_path),
        logo_src=_data_uri(LOGO),
        kicker=kicker,
        titulo=titulo,
        script=script,
        impacto=impacto,
        apoio=apoio,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.set_content(html)
        await page.screenshot(path=str(caminho_saida))
        await browser.close()

    _aplicar_acabamento_dourado(str(caminho_saida))


async def main():
    out_dir = Path(__file__).parent / "_saida_dia_advogado_unico"
    out_dir.mkdir(exist_ok=True)
    for i, pessoa in enumerate(PESSOAS, start=1):
        caminho = out_dir / f"versao-{i}.png"
        await renderizar_versao(pessoa, caminho)
        print(f"versão {i} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
