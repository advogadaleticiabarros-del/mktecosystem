import asyncio
import base64
from pathlib import Path

from jinja2 import Template
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
LOGO = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\logo\logo-800x800.png")
LOGO_MARCA_DAGUA = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\logo\logo-sem-fundo.png")
FONTE_ROSALINE = Path(r"C:\Users\prosy\Downloads\Please write me a song.ttf")
OUT = BASE / "_saida_acho_chique"

TRABALHISTA = [
    {"capa": True, "subtitulo": "Direito Trabalhista"},
    {"texto": "Acho chique receber todas as <em>verbas rescisórias</em> certinho, sem precisar correr atrás do que já é seu.", "tamanho_fonte": 49},
    {"texto": "Acho chique <em>gestante</em> ter a estabilidade respeitada, mesmo quando a empresa diz que \"não sabia da gravidez\".", "tamanho_fonte": 46},
    {"texto": "Acho chique <em>hora extra</em> ser paga. Porque trabalho a mais não é \"ajudinha\".", "tamanho_fonte": 56},
    {"texto": "Acho chique bater o ponto, ir embora e não levar o expediente <em>no WhatsApp</em> pra casa.", "tamanho_fonte": 51},
    {"texto": "Acho chique <em>assédio moral</em> ser levado a sério, e não tratado como \"brincadeira\" ou \"exagero\".", "tamanho_fonte": 49},
    {"texto": "Acho chique <em>carteira assinada</em> ser direito básico, e não \"favor do patrão\".", "tamanho_fonte": 53},
    {"texto": "E acho <em>chiquérrimo</em> conhecer seus direitos antes de precisar correr atrás deles.", "tamanho_fonte": 53, "fechamento_forte": True},
]

FAMILIA = [
    {"capa": True, "subtitulo": "Direito de Família"},
    {"texto": "Acho chique <em>pensão</em> ser paga em dia, sem precisar mandar mensagem cobrando todo mês.", "tamanho_fonte": 53},
    {"texto": "Acho chique <em>guarda compartilhada</em> ser sobre dividir responsabilidades, e não disputar quem \"fica\" com o filho.", "tamanho_fonte": 44},
    {"texto": "Acho chique entender que <em>convivência e pensão</em> são direitos diferentes. Filho nunca deve virar moeda de troca.", "tamanho_fonte": 44},
    {"texto": "Acho chique quem já carrega praticamente tudo na criação dos filhos não precisar carregar sozinha também <em>uma batalha judicial</em>.", "tamanho_fonte": 40},
    {"texto": "Acho chique pensão ser <em>revista</em> quando a realidade muda. Necessidade e possibilidade não ficam congeladas no tempo.", "tamanho_fonte": 41},
    {"texto": "Acho chique entender que o fim do relacionamento dos pais <em>não significa o fim da parentalidade</em>.", "tamanho_fonte": 48},
    {"texto": "E acho <em>chiquérrimo</em> conhecer seus direitos antes do conflito virar processo.", "tamanho_fonte": 55, "fechamento_forte": True},
]


def _data_uri(caminho: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(caminho.read_bytes()).decode()


async def gerar_carrossel(nome_pasta: str, slides: list[dict]) -> None:
    tpl = Template((BASE / "_template_acho_chique.html").read_text(encoding="utf-8"))
    logo_src = _data_uri(LOGO, "image/png")
    logo_marca_dagua_src = _data_uri(LOGO_MARCA_DAGUA, "image/png")
    fonte_rosaline_src = _data_uri(FONTE_ROSALINE, "font/ttf")
    pasta_fotos = OUT / nome_pasta
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for i, slide in enumerate(slides, start=1):
            foto_path = pasta_fotos / f"foto_{i}.jpg"
            foto_src = _data_uri(foto_path, "image/jpeg")
            html = tpl.render(logo_src=logo_src, foto_src=foto_src, logo_marca_dagua_src=logo_marca_dagua_src, fonte_rosaline_src=fonte_rosaline_src, **slide)
            await page.set_content(html)
            caminho = pasta_fotos / f"slide-{i}.png"
            await page.screenshot(path=str(caminho))
            print(f"{nome_pasta} slide {i} -> {caminho}")
        await browser.close()


async def main():
    await gerar_carrossel("trabalhista", TRABALHISTA)
    await gerar_carrossel("familia", FAMILIA)


if __name__ == "__main__":
    asyncio.run(main())
