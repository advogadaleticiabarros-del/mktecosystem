"""Série Mito ou Lei v3 (09/10/2026): o selo sai do meio da leitura.

Afirmação e explicação ficam juntas num cartão de vidro (mesma linguagem da pergunta v6);
o selo-medalhão vira o carimbo do veredito, aplicado sobre o cartão. Duas posições:
  - "canto":  carimbo no canto superior direito, texto alinhado à esquerda (documento carimbado)
  - "topo":   selo encaixado no topo do cartão, eixo central

Uso (de apps/api): python _saida_producao_1510/mito_v3.py [canto|topo] [AAAA-MM-DD ...]
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
.c { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; color:#E8DED1;
  background: radial-gradient(ellipse at 50% 38%, #3D332A 0%, #2A231E 55%, #1E1814 100%); }
.mancha { position:absolute; inset:0; opacity:.12; mix-blend-mode:soft-light; background-image:url("{{ mancha }}"); }
.marca { position:absolute; width:1180px; left:50%; top:50%; transform:translate(-50%,-48%); opacity:.035; }
.vinheta { position:absolute; inset:0; background: radial-gradient(ellipse at 50% 45%, transparent 48%, rgba(0,0,0,.38) 100%); }
.luz { position:absolute; inset:0; mix-blend-mode:soft-light; background: radial-gradient(ellipse at 22% 10%, rgba(233,211,152,.40), transparent 46%); }
.moldura { position:absolute; inset:36px; border:1.5px solid #C9A96270; border-radius:18px; z-index:6; }
.grao { position:absolute; inset:0; z-index:9; opacity:.13; mix-blend-mode:overlay; background-image:url("{{ grao }}"); }

.topo { position:absolute; top:92px; left:0; right:0; display:flex; justify-content:center; align-items:center; gap:22px; z-index:4; }
.topo span { font-size:22px; font-weight:600; letter-spacing:7px; text-transform:uppercase; color:#C9A962; }
.fio { width:90px; height:1.5px; background:linear-gradient(90deg, transparent, #C9A962); } .fio.d { background:linear-gradient(90deg, #C9A962, transparent); }

/* palco: área útil entre o topo e a assinatura, cartão no centro óptico */
.palco { position:absolute; left:0; right:0; top:{{ 160 if pos == 'canto' else 262 }}px; bottom:{{ 210 if pos == 'canto' else 186 }}px; display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:5; }
.card { position:relative; width:{{ 880 if pos == 'canto' else 860 }}px; border-radius:26px;
  background: linear-gradient(180deg, rgba(58,48,40,.72) 0%, rgba(36,29,24,.78) 100%);
  border:1.5px solid #C9A9629e; box-shadow: 0 34px 80px rgba(0,0,0,.50), inset 0 1px 0 rgba(255,240,200,.18); }
.sec1 { padding:{{ '64px 64px 44px' if pos == 'canto' else '164px 70px 40px' }}; text-align:{{ 'left' if pos == 'canto' else 'center' }}; }
.kicker { font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:500; font-size:40px; color:#E2C77F; margin-bottom:18px; }
.af { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:{{ fs }}px; line-height:1.12; color:#FAF6F0; text-wrap:balance;
  {% if pos == 'canto' %}max-width:700px;{% endif %} }
.af.mito { color:#FAF6F0c4; text-decoration: line-through; text-decoration-color:#C9A962d0; text-decoration-thickness:2px; }
.af .aspa { color:#C9A962; text-decoration:none; }
.sec2 { margin:0 {{ 64 if pos == 'canto' else 70 }}px; padding:36px 0 52px; border-top:1px solid #C9A96259; text-align:{{ 'left' if pos == 'canto' else 'center' }}; }
.rot { font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#C9A962; margin-bottom:16px; }
.ex { font-size:30px; line-height:1.5; color:#E8DED1; text-wrap:pretty; }
.ref { margin-top:26px; display:inline-block; font-size:22px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#C9A962;
  border:1.5px solid #C9A96299; padding:9px 18px; border-radius:999px; white-space:nowrap; }
.ref.longa { letter-spacing:1.5px; }

/* selo: medalha gravada, sem brilho de moeda */
.selo { position:absolute; width:{{ 236 if pos == 'canto' else 268 }}px; aspect-ratio:1; border-radius:50%; z-index:7;
  {% if pos == 'canto' %}right:-46px; top:-92px; transform:rotate(-11deg);{% else %}left:50%; top:-134px; transform:translateX(-50%);{% endif %}
  background: radial-gradient(circle at 34% 26%, #F4E6BC 0%, #DCC385 28%, #C3A25A 58%, #9C7B3A 84%, #7A5E28 100%);
  box-shadow: 0 22px 44px rgba(0,0,0,.55), 0 0 0 6px rgba(30,24,20,.85), 0 0 0 7.5px #C9A962a6,
              inset 0 2px 4px rgba(255,248,225,.55), inset 0 -5px 10px rgba(70,48,14,.45); }
.selo .raios { position:absolute; inset:0; border-radius:50%; opacity:.22; mix-blend-mode:multiply;
  background: repeating-conic-gradient(from 0deg, rgba(90,62,20,.9) 0deg 1deg, transparent 1deg 4deg);
  -webkit-mask-image: radial-gradient(circle, transparent 0 60%, #000 61% 100%); }
.selo .a1 { position:absolute; inset:10px; border-radius:50%; border:1.5px solid rgba(70,48,14,.55); }
.selo .a2 { position:absolute; inset:46px; border-radius:50%; border:1.5px solid rgba(70,48,14,.50); box-shadow: inset 0 0 0 4px rgba(255,240,200,.18); }
.selo svg { position:absolute; inset:0; }
.selo .miolo { position:absolute; inset:46px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px; }
.selo .ver { font-size:{{ 12 if pos == 'canto' else 13 }}px; font-weight:700; letter-spacing:4px; color:rgba(58,40,14,.85); padding-left:4px; }
.selo .palavra { font-family:'Cormorant Garamond',serif; font-weight:700; font-size:{{ (52 if veredito == 'MITO' else 64) if pos == 'canto' else (60 if veredito == 'MITO' else 76) }}px; line-height:1; letter-spacing:2px; color:#3A2A14;
  text-shadow: 0 1px 0 rgba(255,244,210,.6), 0 -1px 0 rgba(60,40,10,.3); }
.salve { margin-top:30px; font-size:22px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:#E8DED1d9; }
.salve b { color:#C9A962; font-weight:600; }
.selo .est { font-size:13px; color:rgba(58,40,14,.75); }

.ass { position:absolute; left:0; right:0; bottom:96px; display:flex; flex-direction:column; align-items:center; gap:12px; z-index:4; }
.linha-ass { display:flex; align-items:center; gap:22px; }
.ass img { width:54px; height:54px; }
.ass .nome { font-size:23px; font-weight:600; letter-spacing:6px; text-transform:uppercase; color:#E8DED1; }
.ass .oab { font-size:22px; font-weight:600; letter-spacing:4px; color:#C9A962; }
</style></head><body><div class="c">
<div class="mancha"></div><img class="marca" src="{{ logo }}"><div class="vinheta"></div><div class="luz"></div><div class="moldura"></div>
<div class="topo"><div class="fio"></div><span>Série · Mito ou Lei</span><div class="fio d"></div></div>
<div class="palco"><div class="card">
  <div class="selo"><div class="raios"></div><div class="a1"></div><div class="a2"></div>
    <svg viewBox="0 0 200 200"><defs><path id="circ" d="M100,100 m-80,0 a80,80 0 1,1 160,0 a80,80 0 1,1 -160,0"/></defs>
      <text font-family="Inter" font-size="10.4" font-weight="700" letter-spacing="3.1" fill="rgba(58,40,14,.82)"><textPath href="#circ" startOffset="0">LETÍCIA BARROS ✦ ADVOCACIA ✦ OAB/ES 39.948 ✦</textPath></text></svg>
    <div class="miolo"><span class="ver">VEREDITO</span><span class="palavra">{{ veredito }}</span><span class="est">✦</span></div>
  </div>
  <div class="sec1"><div class="kicker">Você acredita que…</div>
    <div class="af {{ 'mito' if veredito == 'MITO' else '' }}"><span class="aspa">“</span>{{ afirmacao }}<span class="aspa">”</span></div></div>
  <div class="sec2"><div class="rot">{{ 'A verdade' if veredito == 'MITO' else 'O que diz a lei' }}</div>
    <div class="ex">{{ explicacao }}</div><div class="ref{{ ' longa' if ref|length > 40 else '' }}">{{ ref }}</div></div>
</div>{% if pos == 'topo' %}<div class="salve"><b>✦</b> Salve para consultar quando precisar <b>✦</b></div>{% endif %}</div>
<div class="ass"><div class="linha-ass"><div class="fio"></div><img src="{{ logo }}"><span class="nome">Letícia Barros · Advocacia</span><div class="fio d"></div></div><span class="oab">OAB/ES 39.948</span></div>
<div class="grao"></div>
</div></body></html>""")


def ref_curta(ref: str) -> str:
    """Abrevia a referência legal para caber numa linha da pílula."""
    return ref.replace("Código Eleitoral", "Cód. Eleitoral").replace("Resolução", "Res.")


def tamanho_fonte(afirmacao: str) -> int:
    n = len(afirmacao)
    return 60 if n < 55 else 54 if n < 75 else 50


async def main(pos: str, dias: list[str]) -> None:
    logo = render_criativo._logo_data_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for dia, _k, af, ver, ex, ref, _tags in MITO_OU_LEI:
            if dias and dia not in dias:
                continue
            await page.set_content(HTML.render(afirmacao=af.rstrip("."), veredito=ver, explicacao=ex, ref=ref_curta(ref), pos=pos,
                                               fs=tamanho_fonte(af) + (4 if pos == 'canto' else 0), logo=logo, mancha=v4.MANCHA, grao=v4.GRAO),
                                   wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            destino = AQUI / "pecas" / f"mito-{dia}-v3-{pos}.png"
            await page.screenshot(path=str(destino))
            render_criativo._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
            destino.unlink()
            print("ok", dia, pos)
        await browser.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    asyncio.run(main(args[0] if args else "canto", args[1:]))
