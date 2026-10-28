"""Frases no estilo do post de referência (28/10/2026): fundo escuro, caixa-alta grossa, alinhada à esquerda, fecho
em dourado. Uma imagem nova por frase; a primeira (frase-demitido-posicao-politica-1080x1440.png) fica intacta.
Uso, de apps/api: py ../../producao/frases/2026-10-28-demitido-posicao-politica/gerar_frases.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, ".")
from playwright.async_api import async_playwright  # noqa: E402
from app.services.render_criativo import _aplicar_acabamento_dourado, _logo_data_uri  # noqa: E402

AQUI = Path(__file__).resolve().parent
FONTE_MPT = "Fonte: Ministério Público do Trabalho, balanços de 27/10/2026."

FRASES = [
    ("frase-escritorio-orientar",
     "Se você for<br>demitido por<br>sua posição<br>política,<br>nosso<br>escritório<br>está aqui para<br><em>te orientar.</em>", None),
    ("frase-500-denuncias-ilegal",
     "Mais de 500<br>denúncias<br>depois do<br>2º turno.<br>Não importa<br>em quem você<br>votou:<br><em>isso é ilegal.</em>", FONTE_MPT),
    ("frase-eleicao-acabou",
     "A eleição<br>acabou.<br>As denúncias,<br>não:<br><em>mais de 500<br>em dois dias.</em>", FONTE_MPT),
    ("frase-2364-denuncias-es",
     "2.364<br>denúncias<br>em 2026.<br>47 no<br>Espírito Santo.<br>Seu voto não<br>pode custar<br><em>o seu emprego.</em>", FONTE_MPT),
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
.fonte { position: absolute; left: 104px; bottom: 236px; font: 500 22px 'Inter', sans-serif; color: rgba(232,222,209,.7); }
.assinatura { position: absolute; left: 104px; bottom: 150px; display: flex; align-items: center; gap: 18px;
  font-family: 'Inter', sans-serif; font-weight: 600; font-size: 26px; color: #E8DED1; letter-spacing: .5px; }
.assinatura img { width: 64px; height: 64px; object-fit: contain; }
.assinatura span { color: #C9A962; }
</style></head><body><div class="card">
<h1>FRASE</h1>
FONTE
<div class="assinatura"><img src="LOGO">Letícia Barros <span>·</span> OAB/ES 39.948</div>
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
            arquivo = AQUI / f"{nome}-1080x1440.png"
            await page.screenshot(path=str(arquivo))
            _aplicar_acabamento_dourado(str(arquivo))
            print(arquivo.name, f"{tamanho}px")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
