import asyncio
import base64
from pathlib import Path

from playwright.async_api import async_playwright

TEMPLATE_PATH = Path(
    "C:/tmp/blogautomaticoleticia/squads/@squad-design/criativos-estaticos/templates/carrossel-4x5.html"
)
LOGO_PATH = Path("C:/tmp/mktecosystem/apps/api/app/assets/logo-leticia.png")
ACABAMENTO_PATH = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/"
    "ementos rdape dourado/cabeçalho e rodape.png"
)
BANCO = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\IDOSAS APOSENTADORIA E BEM ESTAR")
OUT_DIR = Path(__file__).parent / "_teste_aposentadoria_mulher_v2_output"

SLIDES = [
    {
        "kicker": "Atenção, mulheres",
        "headline": "A idade da aposentadoria <em>mudou de novo</em>",
        "texto": "Você contribuiu a vida inteira. E o INSS moveu a régua outra vez.",
        "foto": "pexels-brianjiz-20158561.jpg",
    },
    {
        "kicker": "Regra de 2026",
        "headline": "<em>59 anos e 6 meses.</em> Essa é a nova idade mínima",
        "texto": "Junto com 30 anos de contribuição, na regra de transição por idade progressiva.",
        "foto": "pexels-giovanna-kamimura-399616174-36904368.jpg",
    },
    {
        "kicker": "Quem tem direito",
        "headline": "Só vale pra quem contribuía <em>antes de 2019</em>",
        "texto": "Se você já estava no INSS antes da reforma da Previdência, esse caminho pode ser seu.",
        "foto": "pexels-owonaropreye-11696017.jpg",
    },
    {
        "kicker": "O que decide o valor",
        "headline": "Seu benefício <em>não é fixo</em>",
        "texto": "É a média de todos os seus salários desde 1994. Quanto mais tempo, maior o percentual.",
        "foto": "pexels-beccacorreiaph-36904750.jpg",
    },
    {
        "kicker": "Antes de pedir",
        "headline": "Confira seu <em>CNIS</em> primeiro",
        "texto": "Um buraco no cadastro pode te tirar da regra sem você nem saber o motivo.",
        "foto": "pexels-carolina-ferreira-2154778491-36902205.jpg",
    },
]


def arquivo_para_data_uri(caminho: Path) -> str:
    mime = "image/png" if caminho.suffix.lower() == ".png" else "image/jpeg"
    dados = base64.b64encode(caminho.read_bytes()).decode()
    return f"data:{mime};base64,{dados}"


def montar_pager(indice: int, total: int) -> str:
    pontos = []
    for i in range(total):
        pontos.append(f'<i class="{"on" if i == indice else ""}"></i>')
    return "".join(pontos)


def montar_foot(final: bool) -> str:
    if final:
        return '<span class="cta">⚖️ Procure uma advogada</span><span class="handle">@adv.leticiabarros2</span>'
    return '<span class="swipe">Arraste pro lado <span class="arrow">›</span></span><span class="handle">@adv.leticiabarros2</span>'


def aplicar_acabamento(caminho_png: Path) -> None:
    from PIL import Image

    base = Image.open(caminho_png).convert("RGBA")
    acabamento = Image.open(ACABAMENTO_PATH).convert("RGBA")
    if acabamento.size != base.size:
        acabamento = acabamento.resize(base.size)
    Image.alpha_composite(base, acabamento).convert("RGB").save(caminho_png)


async def main():
    OUT_DIR.mkdir(exist_ok=True)
    template_raw = TEMPLATE_PATH.read_text(encoding="utf-8")
    logo_src = arquivo_para_data_uri(LOGO_PATH)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i, slide in enumerate(SLIDES):
            foto_src = arquivo_para_data_uri(BANCO / slide["foto"])
            final = i == len(SLIDES) - 1
            html = (
                template_raw.replace("[IMAGEM_FUNDO]", foto_src)
                .replace("[LOGO_SRC]", logo_src)
                .replace("[PAGER]", montar_pager(i, len(SLIDES)))
                .replace("[KICKER]", slide["kicker"])
                .replace("[HEADLINE]", slide["headline"])
                .replace("[TEXTO]", slide["texto"])
                .replace("[FOOT]", montar_foot(final))
            )
            page = await browser.new_page(viewport={"width": 1080, "height": 1350})
            await page.set_content(html)
            caminho = OUT_DIR / f"carrossel-slide-{i + 1}.png"
            await page.screenshot(path=str(caminho))
            await page.close()
            aplicar_acabamento(caminho)
            print(f"Slide {i + 1} salvo em {caminho}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
