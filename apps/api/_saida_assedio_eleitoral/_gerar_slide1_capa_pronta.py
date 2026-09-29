import asyncio
import base64
from pathlib import Path

from jinja2 import Template
from PIL import Image
from playwright.async_api import async_playwright

ACABAMENTO_PATH = Path(__file__).parent.parent / "app" / "assets" / "acabamento-dourado.png"
LOGO_PATH = Path(__file__).parent.parent / "app" / "assets" / "logo-leticia.png"
FOTO_PATH = Path(__file__).parent / "capa-chatgpt-slide1.png"
OUT_PATH = Path(__file__).parent / "carrossel_slides" / "slide-1.png"

TOTAL_SLIDES = 5
INDICE = 0  # slide 1

TEMPLATE_HTML = """
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { margin: 0; }

  .slide {
    width: 1080px; height: 1350px;
    position: relative; overflow: hidden;
    font-family: 'Inter', sans-serif;
    color: #F3EAD4;
  }

  .bg-foto {
    position: absolute; inset: 0; width: 100%; height: 100%;
    object-fit: cover; object-position: center 30%;
    z-index: 0;
  }

  /* leve escurecimento só no topo (pra logo) e no rodapé (pra perfil), preservando o centro da arte intacto */
  .bg-shade-top {
    position: absolute; top: 0; left: 0; right: 0; height: 220px; z-index: 1;
    background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 100%);
  }
  .bg-shade-bottom {
    position: absolute; bottom: 0; left: 0; right: 0; height: 180px; z-index: 1;
    background: linear-gradient(0deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0) 100%);
  }

  .slide::before {
    content: '';
    position: absolute;
    inset: 36px;
    border: 1.5px solid rgba(201,169,98,0.55);
    border-radius: 18px;
    pointer-events: none;
    z-index: 3;
  }

  .top {
    position: absolute; top: 44px; left: 88px; right: 88px; z-index: 3;
    display: flex; align-items: center; justify-content: space-between;
  }
  .brand { display: flex; align-items: center; gap: 16px; }
  .brand img { width: 56px; height: 56px; object-fit: contain; filter: drop-shadow(0 2px 8px rgba(0,0,0,.5)); }
  .brand .nm { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; line-height: 1.1; }
  .brand .sb { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #C9A962; margin-top: 4px; }

  .pager { display: flex; gap: 9px; align-items: center; }
  .pager i { width: 12px; height: 12px; border-radius: 50%; background: rgba(243,234,212,0.35); display: block; }
  .pager i.on { background: #C9A962; width: 30px; border-radius: 999px; }

  .foot {
    position: absolute; bottom: 0; left: 0; right: 0; z-index: 3;
    padding: 20px 88px 32px;
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0) 100%);
  }
  .swipe { display: inline-flex; align-items: center; gap: 12px; font-size: 24px; font-weight: 600; color: #E8D7A6; }
  .swipe .arrow { font-size: 30px; }
  .handle { font-size: 20px; color: rgba(243,234,212,0.75); font-weight: 600; text-align: right; }
  .handle .oab { display: block; font-size: 15px; color: #C9A962; margin-top: 2px; }
</style>
</head>
<body>
  <div class="slide">
    <img class="bg-foto" src="{{ foto_src }}" alt="Assédio eleitoral">
    <div class="bg-shade-top"></div>
    <div class="bg-shade-bottom"></div>

    <div class="top">
      <div class="brand">
        <img src="{{ logo_src }}" alt="Letícia Barros">
        <div>
          <div class="nm">Letícia Barros</div>
          <div class="sb">Advocacia</div>
        </div>
      </div>
      <div class="pager">
        {% for i in range(total) %}
          <i class="{{ 'on' if i == indice else '' }}"></i>
        {% endfor %}
      </div>
    </div>

    <div class="foot">
      <span class="swipe">Arraste pro lado <span class="arrow">›</span></span>
      <span class="handle">
        @adv.leticiabarros2
        <span class="oab">OAB/ES 39.948</span>
      </span>
    </div>
  </div>
</body>
</html>
"""


def arquivo_para_data_uri(caminho: Path, mime: str) -> str:
    dados = base64.b64encode(caminho.read_bytes()).decode()
    return f"data:{mime};base64,{dados}"


def aplicar_acabamento_dourado(caminho_png: Path) -> None:
    base = Image.open(caminho_png).convert("RGBA")
    acabamento = Image.open(ACABAMENTO_PATH).convert("RGBA")
    if acabamento.size != base.size:
        acabamento = acabamento.resize(base.size)
    composto = Image.alpha_composite(base, acabamento)
    composto.convert("RGB").save(caminho_png)


async def main():
    template = Template(TEMPLATE_HTML)
    html = template.render(
        foto_src=arquivo_para_data_uri(FOTO_PATH, "image/png"),
        logo_src=arquivo_para_data_uri(LOGO_PATH, "image/png"),
        total=TOTAL_SLIDES,
        indice=INDICE,
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html)
        await page.screenshot(path=str(OUT_PATH.resolve()).replace("\\", "/"))
        await browser.close()
    aplicar_acabamento_dourado(OUT_PATH)
    print(f"Salvo em {OUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
