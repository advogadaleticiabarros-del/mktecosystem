import asyncio
import base64
from pathlib import Path

from jinja2 import Template
from PIL import Image
from playwright.async_api import async_playwright

ACABAMENTO_PATH = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/"
    "ementos rdape dourado/cabeçalho e rodape.png"
)

TEMPLATE_PATH = Path(
    "C:/tmp/blogautomaticoleticia/squads/@squad-design/criativos-estaticos/templates/criativo-4x5.html"
)
LOGO_PATH = Path(
    "C:/tmp/blogautomaticoleticia/squads/@squad-design/criativos-estaticos/assets/logo-lb.png"
)
BANCO_IMAGENS_DIR = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/BPC"
)
OUT_DIR = Path(__file__).parent / "_teste_bpc_output" / "squad-criativos"

# Fotos escolhidas do banco próprio da usuária (Pexels, licença livre) —
# mãe/filho, tom terroso/quente, sem texto em inglês. Slides informativos
# (2-4) ficam só-tipografia, seguindo a própria regra da squad de variar
# formato em vez de imagem em todos os slides.
SLIDES = [
    {
        "kicker": "Você sabia?",
        "headline": 'Seu filho pode ter direito a <em>R$ 1.621 por mês</em>',
        "subheadline": "Mesmo que vocês nunca tenham contribuído com o INSS.",
        "cta": "Salva esse post",
        "imagem": "images (3).jpg",
    },
    {
        "kicker": "Não é aposentadoria",
        "headline": 'O BPC é <em>assistência social</em>, não previdência',
        "subheadline": "Por isso, seu filho não precisa ter contribuído com nada pra ter direito.",
        "cta": "Entenda seu caso",
        "imagem": None,
    },
    {
        "kicker": "Requisito 1",
        "headline": 'Renda de até <em>R$ 405,25</em> por pessoa',
        "subheadline": "Somando tudo que a família recebe e dividindo pelo número de moradores.",
        "cta": "Veja se é o seu caso",
        "imagem": None,
    },
    {
        "kicker": "Requisito 2",
        "headline": 'Deficiência de <em>longo prazo</em>, avaliada pelo INSS',
        "subheadline": "Autismo, síndrome de Down, paralisia cerebral e outras condições podem se enquadrar.",
        "cta": "Tire sua dúvida",
        "imagem": None,
    },
    {
        "kicker": "A parte que decide",
        "headline": 'A <em>prova certa</em> é o que aprova o pedido',
        "subheadline": "Laudos, relatórios da escola e da terapia bem organizados. Eu te ajudo a montar isso.",
        "cta": "Fale comigo agora",
        "imagem": "direito-autistas-direito-civil-1024x538.jpg",
    },
]

CATEGORIA = "PREVIDENCIÁRIO"


def carregar_template_como_jinja(caminho_original: Path) -> Template:
    html = caminho_original.read_text(encoding="utf-8")
    html = html.replace("[LOGO_SRC]", "{{ logo_src }}")
    html = html.replace("[CATEGORIA]", "{{ categoria }}")
    html = html.replace("[KICKER — ex: Você sabia?]", "{{ kicker }}")
    html = html.replace(
        "<h1 class=\"headline\">[HEADLINE — destaque <em>palavras-chave</em> em dourado]</h1>",
        '<h1 class="headline">{{ headline|safe }}</h1>',
    )
    html = html.replace("[SUBHEADLINE — complemento da headline]", "{{ subheadline }}")
    html = html.replace("💬 [CTA]", "💬 {{ cta }}")
    html = html.replace(
        '<img class="bg-image" src="[IMAGEM_FUNDO]" alt="">\n    <div class="bg-overlay"></div>',
        '{% if imagem_src %}<img class="bg-image" src="{{ imagem_src }}" alt="">\n'
        '    <div class="bg-overlay"></div>{% endif %}',
    )
    return Template(html)


def imagem_para_data_uri(nome_arquivo: str) -> str:
    caminho = BANCO_IMAGENS_DIR / nome_arquivo
    dados = base64.b64encode(caminho.read_bytes()).decode()
    return f"data:image/jpeg;base64,{dados}"


def aplicar_acabamento_dourado(caminho_png: Path) -> None:
    """Compõe o elemento padrão de cabeçalho/rodapé dourado por cima do
    criativo já renderizado — acabamento fixo da marca, aplicado sempre."""
    base = Image.open(caminho_png).convert("RGBA")
    acabamento = Image.open(ACABAMENTO_PATH).convert("RGBA")
    if acabamento.size != base.size:
        acabamento = acabamento.resize(base.size)
    composto = Image.alpha_composite(base, acabamento)
    composto.convert("RGB").save(caminho_png)


async def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    logo_src = f"data:image/png;base64,{logo_b64}"

    template = carregar_template_como_jinja(TEMPLATE_PATH)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i, slide in enumerate(SLIDES):
            imagem_src = (
                imagem_para_data_uri(slide["imagem"]) if slide["imagem"] else None
            )
            html = template.render(
                logo_src=logo_src,
                categoria=CATEGORIA,
                kicker=slide["kicker"],
                headline=slide["headline"],
                subheadline=slide["subheadline"],
                cta=slide["cta"],
                imagem_src=imagem_src,
            )
            page = await browser.new_page(viewport={"width": 1080, "height": 1350})
            await page.set_content(html)
            caminho = OUT_DIR / f"criativo-{i + 1}.png"
            await page.screenshot(path=str(caminho))
            await page.close()
            aplicar_acabamento_dourado(caminho)
            print(f"Slide {i + 1} salvo em {caminho}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
