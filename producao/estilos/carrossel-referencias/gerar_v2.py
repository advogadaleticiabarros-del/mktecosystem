"""V2 do carrossel "Mãe por adoção" (09/11/2026): mesmos slides do gerar.py, renderizados como
um panorama contínuo (7 × 1080 px) e fatiados, com elementos que atravessam as divisas,
como nas referências: fundo café entrando em diagonal (2|3 e 5|6), foto vazando (3|4),
arcos dourados (4|5) e a palavra ADOÇÃO em pé sobre a divisa (6|7).

Uso: python gerar_v2.py   (saída em ./saida_v2/; a v1 em ./saida/ fica intacta)
"""
import asyncio
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

import gerar as v1

SAIDA = v1.AQUI / "saida_v2"
W, H, N = 1080, 1440, 7


def ajustar(s):
    s[1] = s[1].replace("right:-60px;bottom:120px", "left:40px;bottom:40px")  # palavra-fantasma longe da diagonal
    s[2] = (s[2].replace("right:110px", "right:220px").replace("right:95px", "right:205px")
            .replace("right:180px", "right:290px"))  # moldura recua para a foto vazar
    s[3] = (s[3].replace('<div class="s papel">', '<div class="s papel" style="overflow:visible;z-index:5">', 1)
            .replace("left:80px;right:80px;top:140px;height:640px", "left:-160px;right:80px;top:140px;height:640px"))
    s[5] = s[5].replace("right:-40px;top:50%", "visibility:hidden;")  # ADOÇÃO vai para a divisa
    s[6] = s[6].replace("left:80px;right:80px;bottom:110px", "left:200px;right:80px;bottom:110px")
    return s


def diagonal(x):
    return (f'<div style="position:absolute;z-index:15;left:{x-366}px;top:964px;width:366px;height:476px;background:#C9A962;clip-path:polygon(100% 0,100% 100%,0 100%)"></div>'
            f'<div style="position:absolute;z-index:16;left:{x-340}px;top:1000px;width:340px;height:440px;background:#231E1A;clip-path:polygon(100% 0,100% 100%,0 100%)"></div>')


PONTES = (
    diagonal(2 * W) + diagonal(5 * W)
    + "".join(f'<div style="position:absolute;z-index:15;left:{4*W-r}px;top:{H-r}px;width:{2*r}px;height:{2*r}px;border:3px solid #C9A962;border-radius:50%"></div>' for r in (230, 160))
    + f'''<div class="serif" style="position:absolute;z-index:15;left:{6*W-125}px;top:{H//2-125}px;width:250px;height:250px;display:flex;align-items:center;justify-content:center;
      transform:rotate(90deg);font-size:250px;font-weight:600;letter-spacing:10px;color:#C9A962;white-space:nowrap">ADOÇÃO</div>'''
)


async def main():
    SAIDA.mkdir(exist_ok=True)
    f = {"capa": v1.uri(v1.RETRATOS / "estudio-escuro-banco.jpg"), "fecho": v1.uri(v1.RETRATOS / "escritorio-cafe-blazer-bege.jpg"),
         "foto": v1.uri(v1.AQUI / "fotos/p10557890.jpg")}
    corpo = "".join(f'<div style="position:absolute;top:0;left:{i*W}px">{h}</div>' for i, h in enumerate(ajustar(v1.slides(f))))
    css = v1.CSS.replace("body{width:1080px", f"body{{position:relative;width:{W*N}px")
    html = f'<!doctype html><html><head><meta charset="utf-8">{v1.FONTES}<style>{css}</style></head><body>{corpo}{PONTES}</body></html>'
    pano = SAIDA / "panorama.png"
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W * N, "height": H})
        await pg.set_content(html)
        await pg.wait_for_load_state("networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=str(pano))
        await b.close()
    im = Image.open(pano)
    for i in range(N):
        im.crop((i * W, 0, (i + 1) * W, H)).save(SAIDA / f"adocao-v2-{i+1:02d}.png")
    im.resize((W * N // 4, H // 4)).convert("RGB").save(SAIDA / "tira.jpg", quality=88)


if __name__ == "__main__":
    asyncio.run(main())
