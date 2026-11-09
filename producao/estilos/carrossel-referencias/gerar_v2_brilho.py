"""V2 (panorama contínuo) refeita com a regra do dourado metálico com brilho (09/11/2026).
A V2 original em ./saida_v2/ fica intacta; esta sai em ./saida_v3/V2/.
Uso: python gerar_v2_brilho.py
"""
import asyncio
import re

from PIL import Image
from playwright.async_api import async_playwright

import gerar as v1
import gerar_v2 as v2
from gerar_v3 import GLOW, METAL, METAL_TXT, TXT_GLOW

SAIDA = v1.AQUI / "saida_v3" / "V2"
W, H, N = 1080, 1440, 7
FAIXA = ("height:24px;background:linear-gradient(180deg,#7d5f24 0%,#d9b866 22%,#fff8dc 46%,#fffbe8 52%,#e8c978 70%,#8a6a2a 100%);"
         "box-shadow:0 0 30px 8px rgba(255,214,130,.85),0 0 70px 14px rgba(255,200,100,.35)")


def brilho_css(css):
    css = re.sub(r"\.s::before,\.s::after\{[^}]*\}", '.s::before,.s::after{content:"";position:absolute;left:0;right:0;z-index:20;' + FAIXA + "}", css)
    css = css.replace(".cafe em{color:#C9A962}", f".cafe em{{background:{METAL_TXT};-webkit-background-clip:text;background-clip:text;color:transparent;filter:{TXT_GLOW}}}")
    css = re.sub(r"\.papel em\{[^}]*\}", f".papel em{{background:{METAL} no-repeat left bottom/100% 7px;padding-bottom:6px}}", css)
    css = css.replace("background:#C9A962;color:#231E1A;padding:10px 18px;border-radius:4px}", f"background:{METAL};color:#231E1A;padding:10px 18px;border-radius:4px;box-shadow:{GLOW}}}")
    css = css.replace("border:2px solid #C9A962;display:flex", f"border:2px solid #f2dc9a;box-shadow:{GLOW};display:flex")
    return css + f".ouro{{background:{METAL_TXT};-webkit-background-clip:text;background-clip:text;color:transparent;filter:{TXT_GLOW}}}"


def brilho_html(h):
    h = h.replace("background:#C9A962;clip-path", f"background:{METAL};clip-path")
    h = h.replace("border:3px solid #C9A962;border-radius:50%", f"border:4px solid #f2dc9a;box-shadow:{GLOW};border-radius:50%")
    h = h.replace("color:#C9A962;white-space:nowrap\">ADOÇÃO", "white-space:nowrap\"><span class=\"ouro\">ADOÇÃO</span>")
    h = h.replace('<div style="position:absolute;width:30px;height:30px;background:#C9A962;', f'<div style="position:absolute;width:30px;height:30px;background:{METAL};box-shadow:{GLOW};')
    h = h.replace("border:2px solid rgba(201,169,98,.7)", f"border:3px solid #f2dc9a;box-shadow:{GLOW}")
    h = h.replace("border:3px solid #C9A962;border-radius:5px", f"border:3px solid #f2dc9a;box-shadow:{GLOW};border-radius:5px")
    h = h.replace("color:#E6CF94\">Mãe por adoção", "\" class=\"ouro\">Mãe por adoção")
    h = h.replace("color:#C9A962\">Letícia Barros · OAB", "\"><span class=\"ouro\">Letícia Barros · OAB").replace("OAB/ES 39.948</div>", "OAB/ES 39.948</span></div>")
    h = h.replace('font-size:56px;margin-top:18px;color:#E6CF94"', 'font-size:56px;margin-top:18px"')
    return h


async def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    f = {"capa": v1.uri(v1.AQUI / "fotos/p19797693.jpg"), "fecho": v1.uri(v1.RETRATOS / "escritorio-cafe-blazer-bege.jpg"),
         "foto": v1.uri(v1.AQUI / "fotos/p10557890.jpg")}
    corpo = "".join(f'<div style="position:absolute;top:0;left:{i*W}px">{h}</div>' for i, h in enumerate(v2.ajustar(v1.slides(f))))
    css = brilho_css(v1.CSS).replace("body{width:1080px", f"body{{position:relative;width:{W*N}px")
    html = brilho_html(f'<!doctype html><html><head><meta charset="utf-8">{v1.FONTES}<style>{css}</style></head><body>{corpo}{v2.PONTES}</body></html>')
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W * N, "height": H})
        await pg.set_content(html)
        await pg.wait_for_load_state("networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=str(SAIDA / "panorama.png"))
        await b.close()
    im = Image.open(SAIDA / "panorama.png")
    for i in range(N):
        im.crop((i * W, 0, (i + 1) * W, H)).save(SAIDA / f"adocao-V2-{i+1:02d}.png")
    im.resize((W * N // 4, H // 4)).convert("RGB").save(SAIDA / "tira.jpg", quality=88)


if __name__ == "__main__":
    asyncio.run(main())
