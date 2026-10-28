"""Imagem do post do Perfil da Empresa no Google (1200x900), LP do Espírito Santo, 28/10/2026. Rodar de apps/api."""
import asyncio, base64, sys
from pathlib import Path
sys.path.insert(0, ".")
from playwright.async_api import async_playwright
from app.services.render_criativo import _logo_data_uri

AQUI = Path(__file__).resolve().parent
foto = base64.b64encode((AQUI.parent / "blog-lp" / "lp-demissao-voto-urna.jpg").read_bytes()).decode()
html = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}
.c{width:1200px;height:900px;position:relative;overflow:hidden;background:#14110F}
.f{position:absolute;inset:0;background:url(data:image/jpeg;base64,FOTO) right center/cover}
.v{position:absolute;inset:0;background:linear-gradient(100deg,rgba(20,17,15,.97) 0%,rgba(20,17,15,.9) 48%,rgba(20,17,15,.35) 85%)}
.t{position:absolute;left:80px;top:110px;width:720px}
.k{font:600 24px Inter;letter-spacing:3px;color:#C9A962;text-transform:uppercase}
h1{font:800 84px/0.95 'League Spartan';color:#fff;text-transform:uppercase;margin-top:22px}
h1 em{font-style:normal;color:#C9A962}
p{font:500 30px/1.35 Inter;color:#E8DED1;margin-top:28px}
.a{position:absolute;left:80px;bottom:70px;display:flex;gap:16px;align-items:center;font:600 24px Inter;color:#E8DED1}
.a img{width:56px;height:56px}
.cr{position:absolute;right:16px;bottom:12px;font:500 22px Inter;color:rgba(232,222,209,.8)}
</style></head><body><div class="c"><div class="f"></div><div class="v"></div>
<div class="t"><div class="k">Espírito Santo · 47 denúncias no MPT-ES</div>
<h1>Demitido por causa do <em>voto?</em></h1>
<p>Dispensa por opinião política é proibida por lei. Veja seus direitos e como denunciar.</p></div>
<div class="a"><img src="LOGO">Letícia Barros · OAB/ES 39.948</div>
<div class="cr">Foto: Alejandro Zambrana/TSE</div></div></body></html>""".replace("FOTO", foto).replace("LOGO", _logo_data_uri())


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 900})
        await pg.set_content(html, wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.screenshot(path=str(AQUI / "google-post-demitido-voto-es-1200x900.jpg"), type="jpeg", quality=90)
        await b.close()

asyncio.run(main())
