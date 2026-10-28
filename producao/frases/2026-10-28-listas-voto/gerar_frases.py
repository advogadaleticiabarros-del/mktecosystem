"""Frases-notícia sobre as listas por causa do voto (28/10/2026), no mesmo estilo das frases da campanha do voto
(producao/frases/2026-10-28-demitido-posicao-politica): fundo escuro, caixa-alta grossa, fecho em dourado.
Assinatura das duas sócias (pedido de 28/10); as PNG sem o sufixo "-duas-advogadas" são a versão anterior, só com a Letícia.
Uso, de apps/api: py ../../producao/frases/2026-10-28-listas-voto/gerar_frases.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, ".")
from playwright.async_api import async_playwright  # noqa: E402
from app.services.render_criativo import _aplicar_acabamento_dourado, _logo_data_uri  # noqa: E402

AQUI = Path(__file__).resolve().parent
FONTE_GAZETA = "Fonte: A Gazeta, 28/10/2026."

FRASES = [
    ("frase-listas-6-cidades-es",
     "Listas por causa<br>do voto já<br>circulam em<br>6 cidades do ES.<br><em>Expor quem está<br>nelas pode<br>ser crime.</em>", FONTE_GAZETA),
    ("frase-listas-cachoeiro",
     "Cachoeiro.<br>Vitória.<br>Colatina.<br>Listas por causa<br>do voto no ES.<br><em>Não repasse.<br>Quem repassa<br>também responde.</em>", FONTE_GAZETA),
    ("frase-seu-nome-na-lista",
     "Seu nome está<br>numa lista por<br>causa do voto?<br><em>Quem criou e<br>quem repassou<br>podem responder<br>na Justiça.</em>", None),
    ("frase-recebeu-lista",
     "Recebeu uma<br>lista de “quem<br>votou em quem”?<br><em>Não repasse.<br>Quem repassa<br>também responde.</em>", None),
]

HTML = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
.card { width: 1080px; height: 1440px; background: #14110F; position: relative; overflow: hidden;
  display: flex; flex-direction: column; justify-content: center; padding: 0 96px 60px 104px; }
h1 { font-family: 'League Spartan', sans-serif; font-weight: 800; font-size: 112px; line-height: .93;
  letter-spacing: -1px; color: #FFFFFF; text-transform: uppercase; white-space: nowrap; }
h1 em { font-style: normal; color: #C9A962; }
.fonte { position: absolute; left: 104px; bottom: 262px; font: 500 22px 'Inter', sans-serif; color: rgba(232,222,209,.7); }
.assinatura { position: absolute; left: 104px; bottom: 150px; display: flex; align-items: center; gap: 18px;
  font-family: 'Inter', sans-serif; font-weight: 600; font-size: 26px; color: #E8DED1; letter-spacing: .5px; }
.assinatura img { width: 76px; height: 76px; object-fit: contain; }
.assinatura span { color: #C9A962; }
.assinatura p { line-height: 1.45; }
</style></head><body><div class="card">
<h1>FRASE</h1>
FONTE
<div class="assinatura"><img src="LOGO"><div><p>Dra. Letícia Barros <span>·</span> OAB/ES 39.948</p>
<p>Dra. Carolina Prado <span>·</span> OAB/ES 29.557</p></div></div>
</div></body></html>"""

# Diminui a letra até a frase caber na largura útil (880 px) e acima da assinatura.
AJUSTAR = """() => { const h = document.querySelector('h1'); let t = 112;
  while ((h.scrollWidth > 880 || h.offsetHeight > 1020) && t > 60) { t -= 2; h.style.fontSize = t + 'px'; }
  return t; }"""


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1440})
        for nome, frase, fonte in FRASES:
            html = (HTML.replace("FRASE", frase).replace("LOGO", _logo_data_uri())
                    .replace("FONTE", f'<div class="fonte">{fonte}</div>' if fonte else ""))
            await page.set_content(html, wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            tamanho = await page.evaluate(AJUSTAR)
            arquivo = AQUI / f"{nome}-duas-advogadas-1080x1440.png"
            await page.screenshot(path=str(arquivo))
            _aplicar_acabamento_dourado(str(arquivo))
            print(arquivo.name, f"{tamanho}px")
        await browser.close()


asyncio.run(main())
