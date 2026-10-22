import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw


def html(tema):
    if tema == 'clara':
        fundo, tinta, suave, linha, marca, faixa = '#f4e9e3', '#1f1f1f', '#4d2a1f', '#b38b59', '#4d2a1f', '#4d2a1f'
    else:
        fundo, tinta, suave, linha, marca, faixa = '#1f1f1f', '#f4e9e3', '#c9b8ae', '#b38b59', '#b38b59', '#b38b59'
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Raleway:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1584px;height:396px;overflow:hidden;background:{fundo}}}
.capa{{position:relative;width:1584px;height:396px;background:{fundo}}}
.faixa{{position:absolute;left:0;right:0;bottom:0;height:6px;background:{faixa}}}
.texto{{position:absolute;left:540px;top:50%;transform:translateY(-52%);width:720px;color:{tinta}}}
.eyebrow{{font-family:'Raleway',sans-serif;font-weight:600;font-size:17px;letter-spacing:4px;text-transform:uppercase;color:{suave}}}
.nome{{font-family:'Playfair Display',Georgia,serif;font-weight:500;font-size:62px;line-height:1.05;margin-top:12px}}
.fio{{width:64px;height:2px;background:{linha};margin:22px 0 20px}}
.servicos{{white-space:nowrap;font-family:'Raleway',sans-serif;font-weight:500;font-size:21px;line-height:1.5;color:{tinta}}}
.servicos span{{color:{linha};padding:0 10px}}
.rodape{{font-family:'Raleway',sans-serif;font-size:16px;letter-spacing:1px;color:{suave};margin-top:18px}}
.mono{{position:absolute;right:150px;top:50%;transform:translateY(-50%);width:170px;height:170px;border:1.5px solid {linha};border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',Georgia,serif;font-weight:500;font-size:62px;letter-spacing:2px;color:{marca}}}
.mono::after{{content:'';position:absolute;inset:9px;border:1px solid {linha};border-radius:50%;opacity:.45}}
</style></head><body><div class="capa">
<div class="texto">
  <div class="eyebrow">Advocacia trabalhista empresarial</div>
  <div class="nome">Letícia Barros</div>
  <div class="fio"></div>
  <div class="servicos">Adequação trabalhista<span>·</span>Prevenção de passivo<span>·</span>Rotinas de RH</div>
  <div class="rodape">OAB/ES 39.948 · Vitória/ES · advogadaleticiabarros.com.br</div>
</div>
<div class="mono">LB</div>
<div class="faixa"></div>
</div></body></html>'''


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for tema in ['clara', 'escura']:
            arq = Path(f'capa_{tema}.html'); arq.write_text(html(tema), encoding='utf-8')
            pg = await b.new_page(viewport={'width': 1584, 'height': 396})
            await pg.goto(arq.resolve().as_uri(), wait_until='networkidle')
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(700)
            await pg.screenshot(path=f'capa_{tema}.png')
        await b.close()

asyncio.run(main())
ims = [Image.open('capa_clara.png').convert('RGB'), Image.open('capa_escura.png').convert('RGB')]
f = Image.new('RGB', (1584, 396 * 2 + 30), 'white'); f.paste(ims[0], (0, 0)); f.paste(ims[1], (0, 426))
d = ImageDraw.Draw(f)
for y in (0, 426):
    d.ellipse((40, y + 236, 40 + 300, y + 536), fill=(150, 150, 150), outline='white', width=8)
f.save('capas_opcoes.jpg', quality=85)
print('ok')
