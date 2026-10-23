import asyncio, base64
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

LOGO = base64.b64encode(Path(r'C:/Users/prosy/mktecosystem/logo/logo-sem-fundo.png').read_bytes()).decode()
HTML = f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Raleway:wght@500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1584px;height:396px;overflow:hidden;background:#f4e9e3}}
.capa{{position:relative;width:1584px;height:396px;background:#f4e9e3}}
.faixa{{position:absolute;left:0;right:0;bottom:0;height:10px;background:#4d2a1f}}
.faixa::after{{content:'';position:absolute;left:0;right:0;top:-4px;height:2px;background:#b38b59}}
.texto{{position:absolute;left:430px;top:50%;transform:translateY(-54%);color:#1f1f1f}}
.eyebrow{{font-family:'Raleway',sans-serif;font-weight:700;font-size:21px;letter-spacing:4.5px;text-transform:uppercase;color:#4d2a1f}}
.nome{{font-family:'Playfair Display',Georgia,serif;font-weight:600;font-size:80px;line-height:1.02;margin-top:10px;color:#1f1f1f}}
.fio{{width:84px;height:3px;background:#b38b59;margin:20px 0 18px}}
.servicos{{white-space:nowrap;font-family:'Raleway',sans-serif;font-weight:600;font-size:27px;color:#1f1f1f}}
.servicos span{{color:#b38b59;padding:0 12px}}
.rodape{{white-space:nowrap;font-family:'Raleway',sans-serif;font-weight:600;font-size:22px;letter-spacing:.6px;color:#4d2a1f;margin-top:16px}}
.rodape span{{color:#b38b59;padding:0 10px}}
.divisoria{{position:absolute;left:1276px;top:78px;bottom:88px;width:1.5px;background:#b38b59;opacity:.7}}
.logo{{position:absolute;right:58px;top:50%;transform:translateY(-54%);width:224px;height:224px}}
</style></head><body><div class="capa">
<div class="texto">
  <div class="eyebrow">Advocacia trabalhista empresarial</div>
  <div class="nome">Letícia Barros</div>
  <div class="fio"></div>
  <div class="servicos">Adequação trabalhista<span>·</span>Prevenção de passivo<span>·</span>Rotinas de RH</div>
  <div class="rodape">OAB/ES 39.948<span>|</span>Vitória/ES<span>|</span>advogadaleticiabarros.com.br</div>
</div>
<div class="divisoria"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="faixa"></div>
</div></body></html>'''


async def main():
    arq = Path('capa_v3.html'); arq.write_text(HTML, encoding='utf-8')
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for escala, nome in [(1, 'capa_v3.png'), (2, 'capa_v3@2x.png')]:
            pg = await b.new_page(viewport={'width': 1584, 'height': 396}, device_scale_factor=escala)
            await pg.goto(arq.resolve().as_uri(), wait_until='networkidle')
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(700)
            larg = await pg.evaluate("Math.max(document.querySelector('.servicos').getBoundingClientRect().right, document.querySelector('.rodape').getBoundingClientRect().right, document.querySelector('.nome').getBoundingClientRect().right)")
            print('texto termina em x =', round(larg))
            await pg.screenshot(path=nome)
        await b.close()

asyncio.run(main())
capa = Image.open('capa_v3.png').convert('RGB')
W = 700; H = int(396 * W / 1584); c = capa.resize((W, H), Image.LANCZOS)
tela = Image.new('RGB', (W, H + 70), 'white'); tela.paste(c, (0, 0))
d = ImageDraw.Draw(tela); r = 66; cx, cy = 22 + r, H + 4
d.ellipse((cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4), fill='white'); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(120, 120, 120))
f = Image.new('RGB', (1584, 396 + 20 + H + 70), 'white'); f.paste(capa, (0, 0)); f.paste(tela, (0, 416)); f.save('capa_v3_previa.jpg', quality=88)
