"""Dia dos Professores 2026, versão com foto (pedido da Letícia em 15/10/2026: "imagem forte de uma professora preta,
com um sorriso bonito na sala de aula, letras no nosso dourado metálico, algo artístico; mantenha a frase").
Foto: Pexels (professora sorrindo diante do quadro). Tratamento da capa Ouro editorial (capa_fecho.CSS_OURO):
foto inteira, véu café embaixo, luz dourada, grão, moldura com cantoneiras, frase em ouro metálico EB Garamond.
Uso (de apps/api): py _saida_producao_1510/professores_v2.py
"""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from playwright.async_api import async_playwright
from app.services import render_criativo as rc
import capa_fecho

AQUI = Path(__file__).resolve().parent
FOTO = AQUI / "_fotos_pexels" / "original-professora.jpg"
DESTINO = AQUI / "pecas" / "professores-2026-v2.jpg"


def html() -> str:
    foto = capa_fecho.enquadrar(FOTO, alvo_x=0.5, alvo_y=0.2, w=1080, h=1350, escala=2)
    cantos = "".join(
        f'<div style="position:absolute; {p} width:60px; height:60px; border-{x}:3px solid #E9D398; border-{y}:3px solid #E9D398; z-index:13;"></div>'
        for p, x, y in [("top:30px; left:30px;", "top", "left"), ("top:30px; right:30px;", "top", "right"),
                        ("bottom:30px; left:30px;", "bottom", "left"), ("bottom:30px; right:30px;", "bottom", "right")])
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,600;0,700;0,800;1,600;1,700&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
{capa_fecho.CSS_OURO}
.frase{{font-family:'EB Garamond',serif; font-weight:700; font-size:70px; line-height:1.08; text-align:center; text-wrap:balance}}
.frase em{{font-style:italic; font-weight:600}}</style></head><body>
<div style="position:relative; width:1080px; height:1350px; background:#1A1511; overflow:hidden;">
  <img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1350px; object-fit:cover; z-index:1; filter:sepia(.14) saturate(.95) contrast(1.06) brightness(.92);">
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(180deg, rgba(20,15,12,.82) 0%, rgba(20,15,12,.35) 10%, rgba(20,15,12,0) 20%, rgba(20,15,12,0) 36%, rgba(20,15,12,.9) 50%, rgba(20,15,12,.98) 62%, rgba(20,15,12,.98) 100%);"></div>
  <div style="position:absolute; inset:0; z-index:3; mix-blend-mode:screen; background:radial-gradient(ellipse at 88% 8%, rgba(255,214,140,.45), transparent 40%), radial-gradient(ellipse at 10% 92%, rgba(201,169,98,.28), transparent 45%);"></div>
  <div style="position:absolute; inset:38px; border:1.5px solid rgba(233,211,152,.55); border-radius:6px; z-index:12;"></div>
  {cantos}
  <div style="position:absolute; top:78px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20; font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#F4EADB;">
    <span>Letícia Barros · Advocacia</span><span style="color:#E9D398">15 de outubro</span></div>
  <div style="position:absolute; left:84px; right:84px; bottom:178px; z-index:20; text-align:center;">
    <div style="font-size:24px; font-weight:800; letter-spacing:6px; text-transform:uppercase; color:#E9D398;">Dia dos Professores</div>
    <div class="co-ouro" style="font-family:'EB Garamond',serif; font-size:120px; font-weight:800; line-height:.6; margin-top:26px;">&ldquo;</div>
    <div class="frase co-ouro" style="margin-top:-6px;">Toda advogada um dia foi aluna. <em>Obrigada, professores, por cada lição que virou caminho.</em></div>
  </div>
  <div style="position:absolute; left:84px; right:84px; bottom:84px; z-index:20; display:flex; align-items:center; justify-content:center; gap:22px;">
    <div style="flex:1; height:1px; background:linear-gradient(90deg, transparent, #C9A962);"></div>
    <img src="{rc._logo_data_uri()}" style="width:44px; height:44px; object-fit:contain;">
    <div style="text-align:center;"><div style="font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#F4EADB;">Letícia Barros · Advocacia</div>
      <div style="font-size:22px; font-weight:700; letter-spacing:4px; color:#E9D398; margin-top:6px;">OAB/ES 39.948</div></div>
    <div style="flex:1; height:1px; background:linear-gradient(90deg, #C9A962, transparent);"></div>
  </div>
  <div class="co-brilho" style="right:150px; top:250px;"></div><div class="co-brilho" style="right:205px; top:330px; transform:scale(.6)"></div>
  <div class="co-brilho" style="left:120px; bottom:520px; transform:scale(.7)"></div>
  <div class="co-grao"></div>
</div></body></html>"""


async def main():
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        await pg.set_content(html(), wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(300)
        png = DESTINO.with_suffix(".png")
        await pg.screenshot(path=str(png))
        await nav.close()
    Image.open(png).resize((1080, 1350), Image.LANCZOS).save(png)
    rc._aplicar_acabamento_dourado(str(png))
    Image.open(png).convert("RGB").save(DESTINO, "JPEG", quality=92, optimize=True)
    png.unlink()
    print("ok", DESTINO.name)

asyncio.run(main())
