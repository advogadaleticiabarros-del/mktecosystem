"""Dia dos Professores 2026, v3 (pedido de ajuste da Letícia no Orbit, 15/10/2026): "mulher mais bonita, mostre
mais a sala de aula, não precisa ser de ângulo perto, pode ser na perspectiva do olhar de alguém".
Foto: Pexels 5427998 (Tima Miroshnichenko), professora sorrindo no quadro vista do fundo da sala, alunos de costas.
O quadro tem palavras em inglês: desfocado (profundidade de campo), professora nítida. Frase em ouro metálico
sobre o quadro desfocado, no alto; a turma e a professora ficam à vista.
Uso (de apps/api): py _saida_producao_1510/professores_v3.py
"""
import asyncio, base64, io, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw, ImageFilter
from playwright.async_api import async_playwright
from app.services import render_criativo as rc
import capa_fecho

AQUI = Path(__file__).resolve().parent
FOTO = AQUI / "_fotos_pexels" / "original-professora-sala.jpg"
DESTINO = AQUI / "pecas" / "professores-2026-v3.jpg"
QUADRO = (0.24, 0.0, 0.64, 0.74)      # fração da foto: área do quadro (texto em inglês) a desfocar
PROFESSORA = (0.535, 0.12, 0.685, 1.0)  # fração da foto: manter nítida
CENTRO_X = 0.58


def foto_tratada() -> str:
    im = Image.open(FOTO).convert("RGB")
    W, H = im.size
    borrada = im.filter(ImageFilter.GaussianBlur(radius=W / 180))
    mascara = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mascara)
    d.rectangle([QUADRO[0] * W, QUADRO[1] * H, QUADRO[2] * W, QUADRO[3] * H], fill=255)
    d.rectangle([PROFESSORA[0] * W, PROFESSORA[1] * H, PROFESSORA[2] * W, PROFESSORA[3] * H], fill=0)
    mascara = mascara.filter(ImageFilter.GaussianBlur(radius=W / 120))
    im = Image.composite(borrada, im, mascara)
    cw = int(H * 1080 / 1350)
    x0 = int(min(max(CENTRO_X * W - cw / 2, 0), W - cw))
    im = im.crop((x0, 0, x0 + cw, H)).resize((2160, 2700), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def html() -> str:
    foto = foto_tratada()
    cantos = "".join(
        f'<div style="position:absolute; {p} width:60px; height:60px; border-{x}:3px solid #E9D398; border-{y}:3px solid #E9D398; z-index:13;"></div>'
        for p, x, y in [("top:30px; left:30px;", "top", "left"), ("top:30px; right:30px;", "top", "right"),
                        ("bottom:30px; left:30px;", "bottom", "left"), ("bottom:30px; right:30px;", "bottom", "right")])
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,600;0,700;0,800;1,600;1,700&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
{capa_fecho.CSS_OURO}
.frase{{font-family:'EB Garamond',serif; font-weight:700; font-size:66px; line-height:1.08; text-align:center; text-wrap:balance}}
.frase em{{font-style:italic; font-weight:600}}</style></head><body>
<div style="position:relative; width:1080px; height:1350px; background:#1A1511; overflow:hidden;">
  <img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1350px; object-fit:cover; z-index:1; filter:sepia(.12) saturate(.95) contrast(1.05) brightness(.95);">
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(180deg, rgba(20,15,12,.8) 0%, rgba(20,15,12,.25) 11%, rgba(20,15,12,0) 18%, rgba(20,15,12,0) 50%, rgba(20,15,12,.82) 62%, rgba(20,15,12,.96) 74%, rgba(20,15,12,.98) 100%);"></div>
  <div style="position:absolute; inset:0; z-index:3; mix-blend-mode:screen; background:radial-gradient(ellipse at 85% 6%, rgba(255,214,140,.40), transparent 40%), radial-gradient(ellipse at 50% 60%, rgba(255,214,140,.12), transparent 35%);"></div>
  <div style="position:absolute; inset:38px; border:1.5px solid rgba(233,211,152,.55); border-radius:6px; z-index:12;"></div>
  {cantos}
  <div style="position:absolute; top:78px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20; font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#F4EADB;">
    <span>Letícia Barros · Advocacia</span><span style="color:#E9D398">15 de outubro</span></div>
  <div style="position:absolute; left:84px; right:84px; bottom:178px; z-index:20; text-align:center;">
    <div style="font-size:24px; font-weight:800; letter-spacing:6px; text-transform:uppercase; color:#E9D398;">Dia dos Professores</div>
    <div class="co-ouro" style="font-family:'EB Garamond',serif; font-size:110px; font-weight:800; line-height:.6; margin-top:24px;">&ldquo;</div>
    <div class="frase co-ouro" style="margin-top:-4px;">Toda advogada um dia foi aluna. <em>Obrigada, professores, por cada lição que virou caminho.</em></div>
  </div>
  <div style="position:absolute; left:84px; right:84px; bottom:84px; z-index:20; display:flex; align-items:center; justify-content:center; gap:22px;">
    <div style="flex:1; height:1px; background:linear-gradient(90deg, transparent, #C9A962);"></div>
    <img src="{rc._logo_data_uri()}" style="width:44px; height:44px; object-fit:contain;">
    <div style="text-align:center;"><div style="font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#F4EADB;">Letícia Barros · Advocacia</div>
      <div style="font-size:22px; font-weight:700; letter-spacing:4px; color:#E9D398; margin-top:6px;">OAB/ES 39.948</div></div>
    <div style="flex:1; height:1px; background:linear-gradient(90deg, #C9A962, transparent);"></div>
  </div>
  <div class="co-brilho" style="right:140px; top:150px;"></div><div class="co-brilho" style="left:150px; top:420px; transform:scale(.6)"></div>
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
