"""Capa de carrossel v2 (pedido 08/10/2026): título editorial em camadas (linha leve,
palavra gigante, tarja de destaque) e a pessoa da foto recortada NA FRENTE das letras,
mantendo a identidade (café, dourado, Playfair + Inter, acabamento dourado).

Uso (de apps/api): python _saida_producao_1510/capa_v2.py [chave ...]
"""
import asyncio
import base64
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo  # noqa: E402

AQUI = Path(__file__).resolve().parent
BANCO = json.loads((AQUI / "indice_fotos.json").read_text())
CORTES = AQUI / "_cortes"

# chave: (área, linha 1, palavra gigante, texto antes da tarja, tarja, nº da foto ou None, foco vertical %)
CAPAS = {
    "outubro-rosa-trabalho": ("Outubro Rosa", "Outubro Rosa:", "5 direitos", "da trabalhadora que", "quase ninguém usa", 228, 30),
    "cancer-inss": ("Câncer de mama", "Câncer de mama:", "5 direitos", "que você pode", "pedir hoje", 227, 30),
    "violencia-domestica-inss": ("Lei Maria da Penha", "Medida protetiva", "e emprego", "5 coisas que", "toda mulher precisa saber", None, 0),
    "mesario-folga": ("Eleições 2026", "Vai ser mesário no", "2º turno?", "5 regras da", "sua folga", None, 0),
    "plano-mamografia": ("Plano de saúde", "Plano de saúde e", "mamografia", "5 coberturas que", "a lei garante", 229, 25),
    "separacao-bens-70": ("Família", "Casou depois dos", "70 anos?", "5 respostas sobre", "bens e herança", 96, 60),
    "licenca-adotante": ("Adoção", "Mãe por adoção:", "5 direitos", "iguais aos da", "mãe biológica", 107, 30),
    "penhora-salario": ("Dívidas", "Seu salário pode ser", "penhorado?", "o que mudou com", "a decisão do STJ", 111, 35),
    "bebe-pensao-morte": ("Pensão por morte", "O pai faleceu na gravidez:", "e a pensão?", "5 respostas sobre", "o direito do bebê", 221, 40),
    "banco-encerra-conta": ("Consumidor", "O banco pode", "fechar sua conta?", "5 pontos da", "decisão do STJ", None, 0),
}


def uri_bytes(dados: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(dados).decode()}"


def preparar_foto(n: int, foco: int) -> tuple[str, str]:
    """Foto 1080×1350 recortada no enquadramento + PNG só da pessoa (mesmo enquadramento)."""
    CORTES.mkdir(exist_ok=True)
    img = Image.open(BANCO[n]).convert("RGB")
    w, h = img.size
    alvo = 1080 / 960
    if w / h > alvo:  # larga demais: corta laterais
        nw = int(h * alvo); x = (w - nw) // 2; img = img.crop((x, 0, x + nw, h))
    else:  # alta demais: corta em cima/baixo pelo foco
        nh = int(w / alvo); y = int((h - nh) * foco / 100); img = img.crop((0, y, w, y + nh))
    img = img.resize((1080, 960), Image.LANCZOS)
    cache = CORTES / f"{n}-{foco}.png"
    if not cache.exists():
        from rembg import new_session, remove
        global _SESSAO
        if "_SESSAO" not in globals():
            _SESSAO = new_session("u2net_human_seg")
        remove(img, session=_SESSAO).save(cache)
    buf = io.BytesIO(); img.save(buf, "JPEG", quality=92)
    return uri_bytes(buf.getvalue(), "image/jpeg"), uri_bytes(cache.read_bytes(), "image/png")


HTML = Template("""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,700;0,800;0,900;1,500&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
.c { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; background:#231E1A; }
.foto, .pessoa { position:absolute; left:0; top:390px; width:1080px; height:960px; }
.foto { filter: sepia(.18) saturate(1.05) brightness(.92); }
.pessoa { -webkit-mask-image:linear-gradient(180deg, transparent 0px, #000 110px); z-index:3; filter: sepia(.18) saturate(1.05) brightness(.92); }
.veu { position:absolute; inset:0; z-index:1; background:
  radial-gradient(ellipse at 50% 12%, #C9A96233, transparent 50%),
  linear-gradient(180deg, #231E1A 0%, #231E1A 29%, rgba(35,30,26,.5) 42%, rgba(35,30,26,.12) 55%, rgba(35,30,26,0) 68%, rgba(35,30,26,.7) 100%); }
.semfoto { position:absolute; inset:0; z-index:1; background:
  radial-gradient(circle at 85% 15%, #C9A96240, transparent 45%), radial-gradient(circle at 10% 90%, #C9A96226, transparent 45%), #231E1A; }
.mono { position:absolute; right:-260px; bottom:-200px; width:900px; opacity:.07; z-index:1; filter:grayscale(1) brightness(2); }
.moldura { position:absolute; inset:36px; border:1.5px solid #C9A96299; border-radius:18px; z-index:6; }
.topo { position:absolute; top:76px; left:84px; right:84px; z-index:6; display:flex; justify-content:space-between; align-items:center; }
.brand { display:flex; align-items:center; gap:14px; }
.brand img { width:54px; height:54px; }
.nm { font-family:'Playfair Display',serif; font-size:26px; font-weight:700; color:#FAF6F0; }
.sb { font-size:16px; letter-spacing:4px; text-transform:uppercase; color:#C9A962; font-weight:600; }
.area { font-size:20px; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#231E1A; background:#C9A962; padding:9px 18px; border-radius:6px; }
.titulo { position:absolute; left:84px; right:84px; top:{{ topo }}px; text-align:center; }
.l1 { z-index:4; position:relative; font-family:'Playfair Display',serif; font-style:italic; font-weight:500; font-size:60px; color:#F2EBE0; line-height:1.1; }
.big { z-index:2; position:relative; font-family:'Playfair Display',serif; font-weight:900; line-height:.95; white-space:nowrap; letter-spacing:-2px;
  background:linear-gradient(180deg,#F1E2B3 0%,#D4BC7D 40%,#C9A962 62%,#A8863F 100%); -webkit-background-clip:text; color:transparent;
  filter: drop-shadow(0 6px 18px rgba(0,0,0,.45)); }
.l3 { text-shadow:0 2px 12px rgba(0,0,0,.55); z-index:4; position:relative; margin-top:18px; font-size:44px; font-weight:600; color:#F2EBE0; line-height:1.35; }
.chip { display:inline-block; background:#C9A962; color:#231E1A; font-weight:800; padding:2px 18px 6px; border-radius:8px; margin-top:8px; }
.camada4 { z-index:4; }
.rodape { position:absolute; left:84px; right:84px; bottom:80px; z-index:6; display:flex; justify-content:space-between; align-items:center; }
.swipe { font-size:24px; font-weight:700; color:#231E1A; background:#C9A962; padding:14px 26px; border-radius:999px; }
.handle { font-size:22px; font-weight:700; color:#FAF6F0; text-shadow:0 2px 8px rgba(0,0,0,.6); }
.handle b { display:block; font-size:18px; color:#C9A962; text-align:right; }
</style></head><body><div class="c">
{% if foto %}<img class="foto" src="{{ foto }}"><div class="veu"></div>{% else %}<div class="semfoto"></div><img class="mono" src="{{ logo }}">{% endif %}
<div class="moldura"></div>
<div class="topo"><div class="brand"><img src="{{ logo }}"><div><div class="nm">Letícia Barros</div><div class="sb">Advocacia</div></div></div><div class="area">{{ area }}</div></div>
<div class="titulo" style="z-index:2"><div class="l1" style="visibility:hidden">{{ l1 }}</div><div class="big" id="big">{{ big }}</div><div class="l3" style="visibility:hidden">{{ pre }}<br><span class="chip">{{ chip }}</span></div></div>
{% if pessoa %}<img class="pessoa" src="{{ pessoa }}">{% endif %}
<div class="titulo" style="z-index:4"><div class="l1">{{ l1 }}</div><div class="big" style="visibility:hidden" id="big2">{{ big }}</div><div class="l3">{{ pre }}<br><span class="chip">{{ chip }}</span></div></div>
<div class="rodape"><span class="swipe">Arraste pro lado ›</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
</div>
<script>
for (const id of ['big','big2']) { const el=document.getElementById(id); let fs=230; el.style.fontSize=fs+'px';
  while (el.scrollWidth > 912 && fs > 90) { fs -= 4; el.style.fontSize = fs + 'px'; } }
</script></body></html>""")


async def main(filtro: set[str]) -> None:
    logo = render_criativo._logo_data_uri()
    (AQUI / "_png").mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for chave, (area, l1, big, pre, chip, n, foco) in CAPAS.items():
            if filtro and chave not in filtro:
                continue
            foto = pessoa = None
            if n is not None:
                foto, pessoa = preparar_foto(n, foco)
            html = HTML.render(logo=logo, area=area, l1=l1, big=big, pre=pre, chip=chip, foto=foto, pessoa=pessoa,
                               topo=170 if foto else 330)
            await page.set_content(html, wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            await page.evaluate("""() => { for (const id of ['big','big2']) { const el=document.getElementById(id); let fs=230; el.style.fontSize=fs+'px';
                while (el.scrollWidth > 912 && fs > 90) { fs -= 4; el.style.fontSize = fs + 'px'; } } }""")
            png = AQUI / "_png" / f"{chave}-capa-v2.png"
            await page.screenshot(path=str(png))
            render_criativo._aplicar_acabamento_dourado(str(png))
            Image.open(png).convert("RGB").save(AQUI / "pecas" / f"{chave}-car-1-v2.jpg", "JPEG", quality=92, optimize=True)
            print("ok", chave)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
