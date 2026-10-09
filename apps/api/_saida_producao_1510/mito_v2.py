"""Série Mito ou Lei v2 (09/10/2026): diagramação editorial em eixo central, selo-medalhão
dourado como único ponto focal, afirmação riscada (MITO) ou sublinhada (LEI) em dourado,
acabamento fosco igual aos carrosséis e assinatura no rodapé igual às frases.

Uso (de apps/api): python _saida_producao_1510/mito_v2.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

import carrossel_v4 as v4  # noqa: E402
from app.services import render_criativo  # noqa: E402
from conteudo import MITO_OU_LEI  # noqa: E402

AQUI = Path(__file__).resolve().parent

HTML = Template(r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; } html { font-variant-numeric: lining-nums; font-feature-settings:"lnum" 1; }
.c { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; color:#E8DED1; text-align:center;
  background: radial-gradient(ellipse at 50% 32%, #3D332A 0%, #2A231E 55%, #1E1814 100%); }
.mancha { position:absolute; inset:0; opacity:.12; mix-blend-mode:soft-light; background-image:url("{{ mancha }}"); }
.vinheta { position:absolute; inset:0; background: radial-gradient(ellipse at 50% 45%, transparent 50%, rgba(0,0,0,.34) 100%); }
.marca { position:absolute; width:1100px; left:50%; top:50%; transform:translate(-50%,-46%); opacity:.05; }
.moldura { position:absolute; inset:36px; border:1.5px solid #C9A9628c; border-radius:18px; z-index:5; }
.grao { position:absolute; inset:0; z-index:8; opacity:.14; mix-blend-mode:overlay; background-image:url("{{ grao }}"); }

.topo { position:absolute; top:92px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:22px; z-index:4; }
.topo span { font-size:23px; font-weight:600; letter-spacing:7px; text-transform:uppercase; color:#C9A962; }
.fio { width:90px; height:1.5px; background:linear-gradient(90deg, transparent, #C9A962); } .fio.d { background:linear-gradient(90deg, #C9A962, transparent); }

.miolo { position:absolute; left:110px; right:110px; top:190px; bottom:230px; display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:4; }
.pergunta { font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:500; font-size:46px; color:#E8DED1cc; margin-bottom:24px; }
.af { position:relative; font-family:'Cormorant Garamond',serif; font-weight:600; font-size:{{ fs }}px; line-height:1.1; color:#FAF6F0; max-width:820px; }
.af .aspa { color:#C9A962; }
.af.mito { color:#FAF6F0b8; }
.risco { position:absolute; left:-2%; right:-2%; top:52%; height:5px; border-radius:3px; transform:rotate(-4deg);
  background:linear-gradient(90deg, transparent, #D9BF7E 8%, #C9A962 50%, #B8943F 92%, transparent); box-shadow:0 2px 10px rgba(0,0,0,.35); }
.sub { display:block; width:180px; height:3px; margin:26px auto 0; background:linear-gradient(90deg, transparent, #C9A962, transparent); }

.selo { position:relative; width:320px; height:320px; margin:44px 0 40px; border-radius:50%;
  background: radial-gradient(circle at 35% 28%, #FFF3CF 0%, #E9D398 22%, #C9A962 52%, #A4823A 78%, #7E6127 100%);
  box-shadow: 0 18px 40px rgba(0,0,0,.55), inset 0 3px 6px rgba(255,255,255,.45), inset 0 -6px 12px rgba(80,55,15,.45);
  transform: rotate(-8deg); display:flex; align-items:center; justify-content:center; }
.selo::before { content:''; position:absolute; inset:14px; border-radius:50%; border:2px solid rgba(80,55,15,.55); box-shadow: inset 0 0 0 6px rgba(255,240,200,.25); }
.selo::after { content:''; position:absolute; inset:30px; border-radius:50%; border:1.5px dashed rgba(80,55,15,.45); }
.selo .anel { position:absolute; inset:0; }
.selo .palavra { position:relative; z-index:2; font-family:'Cormorant Garamond',serif; font-weight:700; font-size:{{ 78 if veredito == 'MITO' else 104 }}px; letter-spacing:3px; color:#3A2A14;
  text-shadow: 0 1px 0 rgba(255,240,200,.55), 0 -1px 0 rgba(60,40,10,.35); }

.ex { font-size:32px; line-height:1.5; color:#E8DED1; max-width:780px; }
.ex b { color:#FAF6F0; font-weight:600; }
.ref { margin-top:22px; display:inline-block; font-size:22px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#C9A962;
  border:1.5px solid #C9A96299; padding:9px 18px; border-radius:999px; }

.ass { position:absolute; left:0; right:0; bottom:96px; display:flex; flex-direction:column; align-items:center; gap:12px; z-index:4; }
.linha-ass { display:flex; align-items:center; gap:22px; }
.ass img { width:54px; height:54px; }
.ass .nome { font-size:23px; font-weight:600; letter-spacing:6px; text-transform:uppercase; color:#E8DED1; }
.ass .oab { font-size:22px; font-weight:600; letter-spacing:4px; color:#C9A962; }
</style></head><body><div class="c">
<div class="mancha"></div><img class="marca" src="{{ logo }}"><div class="vinheta"></div><div class="moldura"></div>
<div class="topo"><div class="fio"></div><span>Série · Mito ou Lei</span><div class="fio d"></div></div>
<div class="miolo">
  <div class="pergunta">Você acredita que…</div>
  <div class="af {{ 'mito' if veredito == 'MITO' else '' }}"><span class="aspa">“</span>{{ afirmacao }}<span class="aspa">”</span>{% if veredito == 'MITO' %}<span class="risco"></span>{% endif %}</div>
  {% if veredito != 'MITO' %}<span class="sub"></span>{% endif %}
  <div class="selo">
    <svg class="anel" viewBox="0 0 320 320"><defs><path id="circ" d="M160,160 m-120,0 a120,120 0 1,1 240,0 a120,120 0 1,1 -240,0"/></defs>
      <text font-family="Inter" font-size="15" font-weight="700" letter-spacing="5" fill="rgba(60,40,10,.75)"><textPath href="#circ" startOffset="0">✦ VEREDITO · LETÍCIA BARROS · ADVOCACIA ✦ VEREDITO ·</textPath></text></svg>
    <span class="palavra">{{ veredito }}</span>
  </div>
  <div class="ex">{{ explicacao }}</div>
  <div class="ref">{{ ref }}</div>
</div>
<div class="ass"><div class="linha-ass"><div class="fio"></div><img src="{{ logo }}"><span class="nome">Letícia Barros · Advocacia</span><div class="fio d"></div></div><span class="oab">OAB/ES 39.948</span></div>
<div class="grao"></div>
</div></body></html>""")


async def main() -> None:
    logo = render_criativo._logo_data_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for dia, _k, af, ver, ex, ref, _tags in MITO_OU_LEI:
            fs = 66 if len(af) < 55 else 58 if len(af) < 75 else 52
            await page.set_content(HTML.render(afirmacao=af.rstrip("."), veredito=ver, explicacao=ex, ref=ref, fs=fs, logo=logo,
                                               mancha=v4.MANCHA, grao=v4.GRAO), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            destino = AQUI / "pecas" / f"mito-{dia}-v2.png"
            await page.screenshot(path=str(destino))
            render_criativo._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
            destino.unlink()
            print("ok", dia)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
