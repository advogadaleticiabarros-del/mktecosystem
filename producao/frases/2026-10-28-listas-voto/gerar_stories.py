"""As 4 frases das listas por causa do voto em formato Stories (1080x1920), mesmo estilo e assinatura das duas sócias.
Áreas livres do Instagram: 270 px no topo e 420 px embaixo. O story 4 deixa espaço para o adesivo de link.
Uso, de apps/api: py ../../producao/frases/2026-10-28-listas-voto/gerar_stories.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, ".")
from playwright.async_api import async_playwright  # noqa: E402
from app.services.render_criativo import _aplicar_acabamento_dourado, _logo_data_uri  # noqa: E402

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from gerar_frases import FRASES  # noqa: E402  (mesmos textos e fontes das artes do feed)

ORDEM = ["frase-listas-cachoeiro", "frase-listas-6-cidades-es", "frase-seu-nome-na-lista", "frase-recebeu-lista"]
LINK = '<div class="link">Passo a passo no link abaixo <b>↓</b></div><div class="espaco"></div>'

HTML = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
.card { width: 1080px; height: 1920px; background: #14110F; position: relative; overflow: hidden;
  display: flex; flex-direction: column; justify-content: center; padding: 270px 96px 560px 104px; }
h1 { font-family: 'League Spartan', sans-serif; font-weight: 800; font-size: 120px; line-height: .93;
  letter-spacing: -1px; color: #FFFFFF; text-transform: uppercase; white-space: nowrap; }
h1 em { font-style: normal; color: #C9A962; }
.link { margin-top: 64px; font: 600 34px 'Inter', sans-serif; color: #E8DED1; }
.link b { color: #C9A962; }
.espaco { height: 150px; }
.fonte { position: absolute; left: 104px; bottom: 552px; font: 500 24px 'Inter', sans-serif; color: rgba(232,222,209,.7); }
.assinatura { position: absolute; left: 104px; bottom: 430px; display: flex; align-items: center; gap: 18px;
  font-family: 'Inter', sans-serif; font-weight: 600; font-size: 28px; color: #E8DED1; letter-spacing: .5px; }
.assinatura img { width: 80px; height: 80px; object-fit: contain; }
.assinatura span { color: #C9A962; }
.assinatura p { line-height: 1.45; }
</style></head><body><div class="card">
<h1>FRASE</h1>
LINK
FONTE
<div class="assinatura"><img src="LOGO"><div><p>Dra. Letícia Barros <span>·</span> OAB/ES 39.948</p>
<p>Dra. Carolina Prado <span>·</span> OAB/ES 29.557</p></div></div>
</div></body></html>"""

# Diminui a letra até a frase caber na largura útil (880 px) e na altura livre entre as áreas do Instagram.
AJUSTAR = """() => { const h = document.querySelector('h1'); let t = 120;
  const max = document.querySelector('.link') ? 820 : 1000;
  while ((h.scrollWidth > 880 || h.offsetHeight > max) && t > 60) { t -= 2; h.style.fontSize = t + 'px'; }
  return t; }"""


async def main() -> None:
    textos = {nome: (frase, fonte) for nome, frase, fonte in FRASES}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for n, nome in enumerate(ORDEM, 1):
            frase, fonte = textos[nome]
            html = (HTML.replace("FRASE", frase).replace("LOGO", _logo_data_uri())
                    .replace("LINK", LINK if n == len(ORDEM) else "")
                    .replace("FONTE", f'<div class="fonte">{fonte}</div>' if fonte else ""))
            await page.set_content(html, wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            tamanho = await page.evaluate(AJUSTAR)
            arquivo = AQUI / f"story-listas-voto-{n}-1080x1920.png"
            await page.screenshot(path=str(arquivo))
            _aplicar_acabamento_dourado(str(arquivo))
            print(arquivo.name, f"{tamanho}px")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
