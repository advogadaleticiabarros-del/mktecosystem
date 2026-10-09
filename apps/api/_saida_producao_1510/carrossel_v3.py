"""Carrossel v3 (pedido 08/10/2026): foto em TODOS os slides (Pexels, curadoria
manual), capa com a foto inteira e título de alto contraste, números legíveis
(Inter nos números grandes; Playfair com algarismos alinhados `lnum`).
Mantém a identidade: café/dourado, Playfair + Inter, acabamento dourado.

Uso (de apps/api): python _saida_producao_1510/carrossel_v3.py [chave ...]
"""
import asyncio
import base64
import io
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import httpx  # noqa: E402
from jinja2 import Template  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo  # noqa: E402
from capa_v2 import CAPAS  # noqa: E402
from conteudo import TEMAS  # noqa: E402

AQUI = Path(__file__).resolve().parent
FOTOS = AQUI / "_fotos_pexels"
PEXELS = json.loads((AQUI / "pexels_candidatas.json").read_text(encoding="utf-8"))

# Índices das candidatas do Pexels escolhidas à mão: [capa, item1..item5, final]
ESCOLHAS = {
    "outubro-rosa-trabalho": [16, 1, 14, 24, 17, 2, 21],
    "cancer-inss": [9, 7, 21, 26, 28, 22, 13],
    "violencia-domestica-inss": [0, 3, 12, 18, 26, 29, 13],
    "mesario-folga": [19, ("licenca-adotante", 17), 17, 15, ("outubro-rosa-trabalho", 7), 16, 20],
    "plano-mamografia": [16, 11, 20, 21, 13, 18, 22],
    "separacao-bens-70": [15, 27, 16, 9, 13, 3, 14],
    "licenca-adotante": [23, 4, 9, 10, 16, 18, 21],
    "penhora-salario": [16, 19, 8, 27, 10, 25, 26],
    "bebe-pensao-morte": [23, 20, 16, 21, 9, 28, 24],
    "banco-encerra-conta": [16, 1, 18, 14, 4, 22, 15],
}


async def baixar(c: httpx.AsyncClient, foto: dict) -> Path:
    FOTOS.mkdir(exist_ok=True)
    destino = FOTOS / f"{foto['id']}.jpg"
    if not destino.exists():
        r = await c.get(foto["url"] + "?auto=compress&cs=tinysrgb&w=1600")
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino


def enquadrar(caminho: Path, foco_y: float = 0.35) -> str:
    img = ImageOps.fit(Image.open(caminho).convert("RGB"), (1080, 1350), Image.LANCZOS, centering=(0.5, foco_y))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


HTML = Template("""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,500;1,600&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
.s { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; color:#E8DED1; background:#231E1A; }
.pf { font-family:'Playfair Display',serif; font-variant-numeric: lining-nums; font-feature-settings:"lnum" 1; }
.foto { position:absolute; inset:0; width:100%; height:100%; filter:sepia(.15) saturate(1.05); }
.veu-capa { position:absolute; inset:0; background:linear-gradient(180deg, rgba(35,30,26,.55) 0%, rgba(35,30,26,0) 16%, rgba(35,30,26,0) 38%, rgba(35,30,26,.72) 55%, rgba(35,30,26,.95) 70%, rgba(35,30,26,.98) 100%); }
.veu-item { position:absolute; inset:0; background:linear-gradient(180deg, rgba(35,30,26,.45) 0%, rgba(35,30,26,.15) 18%, rgba(35,30,26,.25) 34%, rgba(35,30,26,.85) 50%, rgba(35,30,26,.96) 64%, rgba(35,30,26,.98) 100%); }
.veu-final { position:absolute; inset:0; background:linear-gradient(180deg, rgba(35,30,26,.35) 0%, rgba(35,30,26,.15) 30%, rgba(35,30,26,.80) 58%, rgba(35,30,26,.97) 100%); }
.moldura { position:absolute; inset:36px; border:1.5px solid #C9A96299; border-radius:18px; }
.topo { position:absolute; top:76px; left:84px; right:84px; display:flex; justify-content:space-between; align-items:center; }
.brand { display:flex; align-items:center; gap:14px; }
.brand img { width:56px; height:56px; }
.nm { font-family:'Playfair Display',serif; font-size:27px; font-weight:700; color:#FAF6F0; }
.sb { font-size:16px; letter-spacing:4px; text-transform:uppercase; color:#C9A962; font-weight:600; }
.tag { font-size:20px; font-weight:800; letter-spacing:4px; text-transform:uppercase; color:#231E1A; background:#C9A962; padding:9px 18px; border-radius:6px; }
.pg { font-size:26px; font-weight:800; color:#C9A962; letter-spacing:1px; }
.pg span { color:#E8DED1aa; font-weight:600; }
/* capa */
.tit { position:absolute; left:80px; right:80px; bottom:180px; text-align:center; }
.l1 { font-style:italic; font-weight:600; font-size:62px; color:#FAF6F0; line-height:1.1; }
.big { font-weight:900; line-height:1; white-space:nowrap; letter-spacing:-1px; margin-top:6px;
  background:linear-gradient(180deg,#F6E8BF 0%,#E2C98A 45%,#C9A962 70%,#B8943F 100%); -webkit-background-clip:text; color:transparent;
  filter:drop-shadow(0 4px 14px rgba(0,0,0,.6)); }
.l3 { margin-top:20px; font-size:44px; font-weight:600; color:#FAF6F0; line-height:1.35; text-shadow:0 2px 10px rgba(0,0,0,.7); }
.chip { display:inline-block; background:#C9A962; color:#231E1A; font-weight:800; padding:2px 18px 6px; border-radius:8px; margin-top:8px; text-shadow:none; }
/* item */
.it { position:absolute; left:88px; right:88px; bottom:190px; }
.num { font-family:'Inter',sans-serif; font-weight:900; font-size:132px; line-height:1; color:#C9A962; letter-spacing:-4px; margin-bottom:24px;
  text-shadow:0 4px 18px rgba(0,0,0,.5); }
.t { font-size:64px; font-weight:700; color:#FAF6F0; line-height:1.14; margin-bottom:30px; text-shadow:0 2px 12px rgba(0,0,0,.5); }
.c { font-size:37px; line-height:1.45; color:#F2EBE0; }
.ref { display:inline-block; margin-top:28px; font-size:25px; font-weight:700; color:#231E1A; background:#C9A962; padding:6px 16px; border-radius:6px; }
/* final */
.fi { position:absolute; left:88px; right:88px; bottom:250px; }
.fi .h { font-size:66px; font-weight:700; color:#FAF6F0; line-height:1.15; text-shadow:0 2px 14px rgba(0,0,0,.6); }
.save { font-size:30px; font-weight:700; color:#C9A962; margin-top:30px; }
.rod { position:absolute; left:84px; right:84px; bottom:80px; display:flex; justify-content:space-between; align-items:center; }
.btn { font-size:26px; font-weight:800; color:#231E1A; background:#C9A962; padding:16px 30px; border-radius:999px; }
.handle { font-size:22px; font-weight:700; color:#FAF6F0; text-align:right; text-shadow:0 2px 8px rgba(0,0,0,.7); }
.handle b { display:block; font-size:18px; color:#C9A962; }
</style></head><body><div class="s">
<img class="foto" src="{{ foto }}">
<div class="veu-{{ modo }}"></div>
<div class="moldura"></div>
<div class="topo"><div class="brand"><img src="{{ logo }}"><div><div class="nm">Letícia Barros</div><div class="sb">Advocacia</div></div></div>
{% if modo == 'capa' %}<div class="tag">{{ area }}</div>{% else %}<div class="pg">{{ '%02d' % (i+1) }} <span>/ {{ '%02d' % total }}</span></div>{% endif %}</div>
{% if modo == 'capa' %}
<div class="tit"><div class="l1 pf">{{ l1 }}</div><div class="big pf" id="big">{{ big }}</div><div class="l3">{{ pre }}<br><span class="chip">{{ chip }}</span></div></div>
<div class="rod"><span class="btn">Arraste pro lado ›</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
{% elif modo == 'item' %}
<div class="it"><div class="num">{{ '%02d' % i }}</div><div class="t pf">{{ titulo }}</div><div class="c">{{ corpo }}{% if ref %}<br><span class="ref">{{ ref }}</span>{% endif %}</div></div>
<div class="rod"><span class="btn">Arraste pro lado ›</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
{% else %}
<div class="fi"><div class="h pf">{{ texto }}</div><div class="save">Salve este post e mande para quem precisa.</div></div>
<div class="rod"><span class="btn">⚖️ Procure uma advogada</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
{% endif %}
</div></body></html>""")


async def main(filtro: set[str]) -> None:
    from produzir import separar_ref

    logo = render_criativo._logo_data_uri()
    (AQUI / "_png").mkdir(exist_ok=True)
    async with httpx.AsyncClient(timeout=120) as c, async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for tema in TEMAS:
            k = tema["chave"]
            if filtro and k not in filtro:
                continue
            fotos = [await baixar(c, PEXELS[n[0]][n[1]] if isinstance(n, tuple) else PEXELS[k][n]) for n in ESCOLHAS[k]]
            area, l1, big, pre, chip, *_ = CAPAS[k]
            itens = tema["carrossel"]["itens"]
            total = len(itens) + 2
            for i in range(total):
                if i == 0:
                    html = HTML.render(modo="capa", i=i, total=total, logo=logo, foto=enquadrar(fotos[0], 0.2),
                                       area=area, l1=l1, big=big, pre=pre, chip=chip)
                elif i == total - 1:
                    html = HTML.render(modo="final", i=i, total=total, logo=logo, foto=enquadrar(fotos[-1], 0.3),
                                       texto=tema["carrossel"]["final"])
                else:
                    titulo, corpo = itens[i - 1]
                    corpo, ref = separar_ref(corpo)
                    html = HTML.render(modo="item", i=i, total=total, logo=logo, foto=enquadrar(fotos[i], 0.2),
                                       titulo=titulo, corpo=corpo, ref=ref)
                await page.set_content(html, wait_until="networkidle")
                await page.evaluate("document.fonts.ready")
                await page.evaluate("""() => { const el=document.getElementById('big'); if(!el) return; let fs=210; el.style.fontSize=fs+'px';
                    while (el.scrollWidth > 920 && fs > 90) { fs -= 4; el.style.fontSize = fs + 'px'; } }""")
                png = AQUI / "_png" / f"{k}-v3-{i + 1}.png"
                await page.screenshot(path=str(png))
                render_criativo._aplicar_acabamento_dourado(str(png))
                Image.open(png).convert("RGB").save(AQUI / "pecas" / f"{k}-v3-{i + 1}.jpg", "JPEG", quality=92, optimize=True)
            print("ok", k)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
