"""Capa da PÁGINA do escritório no LinkedIn (1128×191, recomendado pelo LinkedIn para páginas).

Mesma identidade da capa aprovada do perfil (gerar_capa_logo_oficial.py), mas sem a logo grande: na página a logo
já aparece no avatar, que cobre o canto inferior esquerdo da capa. Por isso o texto começa em x=300.
Saída: capa-pagina-linkedin.png (1128×191) e capa-pagina-linkedin@2x.png (2256×382, a que se envia).
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

DIR = Path(__file__).parent
HTML = '''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Raleway:wght@500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1128px;height:191px;overflow:hidden;background:#f4e9e3}
.capa{position:relative;width:1128px;height:191px;background:#f4e9e3}
.faixa{position:absolute;left:0;right:0;bottom:0;height:6px;background:#4d2a1f}
.faixa::after{content:'';position:absolute;left:0;right:0;top:-3px;height:1.5px;background:#b38b59}
.texto{position:absolute;left:300px;top:50%;transform:translateY(-56%);color:#1f1f1f}
.eyebrow{font-family:'Raleway',sans-serif;font-weight:700;font-size:13px;letter-spacing:3.5px;text-transform:uppercase;color:#4d2a1f}
.nome{font-family:'Playfair Display',Georgia,serif;font-weight:600;font-size:44px;line-height:1.05;margin-top:6px}
.fio{width:56px;height:2px;background:#b38b59;margin:10px 0 9px}
.servicos{white-space:nowrap;font-family:'Raleway',sans-serif;font-weight:600;font-size:17px}
.servicos span{color:#b38b59;padding:0 9px}
.lado{position:absolute;right:46px;top:50%;transform:translateY(-56%);text-align:right;font-family:'Raleway',sans-serif;font-weight:600;font-size:14px;line-height:1.75;color:#4d2a1f}
.lado b{display:block;font-family:'Playfair Display',serif;font-size:19px;color:#1f1f1f;font-weight:600}
.divisoria{position:absolute;left:846px;top:40px;bottom:46px;width:1px;background:#b38b59;opacity:.7}
</style></head><body><div class="capa">
<div class="texto">
  <div class="eyebrow">Advocacia trabalhista empresarial</div>
  <div class="nome">Letícia Barros</div>
  <div class="fio"></div>
  <div class="servicos">Adequação trabalhista<span>·</span>Prevenção de passivo<span>·</span>Rotinas de RH</div>
</div>
<div class="divisoria"></div>
<div class="lado"><b>OAB/ES 39.948</b>Vitória/ES<br>advogadaleticiabarros.com.br</div>
<div class="faixa"></div>
</div></body></html>'''


async def main() -> None:
    arq = DIR / "_capa_pagina.html"
    arq.write_text(HTML, encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for escala, nome in [(1, "capa-pagina-linkedin.png"), (2, "capa-pagina-linkedin@2x.png")]:
            pg = await b.new_page(viewport={"width": 1128, "height": 191}, device_scale_factor=escala)
            await pg.goto(arq.as_uri(), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(700)
            fim = await pg.evaluate("document.querySelector('.servicos').getBoundingClientRect().right")
            print(nome, "texto termina em x =", round(fim), "(divisória em 846)")
            await pg.screenshot(path=str(DIR / nome))
        await b.close()
    arq.unlink()


if __name__ == "__main__":
    asyncio.run(main())
