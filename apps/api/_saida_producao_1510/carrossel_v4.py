"""Carrossel editorial v4 (pedido 08/10/2026): panorama contínuo de 7 slides
(7560×1350) fatiado em 7, com textura de papel, ritmo claro/escuro/foto, Cormorant
Garamond com itálico de destaque, objetos e a Letícia recortados vazando entre slides,
arco dourado atravessando o carrossel e faixas douradas em todos os slides.

Uso (de apps/api): python _saida_producao_1510/carrossel_v4.py
"""
import asyncio
import base64
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jinja2 import Template  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo  # noqa: E402

AQUI = Path(__file__).resolve().parent
REC = AQUI / "_recortes"
FOTOS = AQUI / "_fotos_pexels"


def png(nome: str) -> str:
    return "data:image/png;base64," + base64.b64encode((REC / nome).read_bytes()).decode()


def foto(caminho: Path, w: int = 1080, h: int = 1350, foco: float = 0.25) -> str:
    img = ImageOps.fit(Image.open(caminho).convert("RGB"), (w, h), Image.LANCZOS, centering=(0.5, foco))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _svg(corpo: str, w: int = 400, h: int = 400) -> str:
    return ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d'>%s</svg>" % (w, h, corpo)).replace("#", "%23")


GRAO = _svg("<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.4' numOctaves='2' stitchTiles='stitch'/>"
            "<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#g)'/>", 300, 300)
MANCHA = _svg("<filter id='m'><feTurbulence type='fractalNoise' baseFrequency='.006' numOctaves='3' seed='7'/>"
              "<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#m)'/>", 1080, 1350)
FIBRA = _svg("<filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.012 .55' numOctaves='2' seed='3'/>"
             "<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#f)'/>", 600, 600)

RUIDO = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 .5  0 0 0 0 .4  0 0 0 0 .3  0 0 0 .55 0'/></filter>"
         "<rect width='300' height='300' filter='url(%23n)'/></svg>")

HTML = Template(r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html { font-variant-numeric: lining-nums; font-feature-settings:"lnum" 1; }
body { width:7560px; height:1350px; }
.pano { position:relative; width:7560px; height:1350px; overflow:hidden; font-family:'Inter',sans-serif; }
.s { position:absolute; top:0; width:1080px; height:1350px; overflow:hidden; }
.claro { background:#F2EBE0; color:#231E1A; }
.escuro { background:radial-gradient(ellipse at 70% 20%, #3A3027 0%, #231E1A 60%); color:#E8DED1; }
.textura::after { content:''; position:absolute; inset:0; background-image:url("{{ ruido }}"); opacity:.22; mix-blend-mode:multiply; pointer-events:none; }
.escuro.textura::after { opacity:.30; mix-blend-mode:overlay; }
.cab { position:absolute; top:78px; left:84px; right:84px; display:flex; justify-content:space-between; font-size:22px; font-weight:600; letter-spacing:5px; text-transform:uppercase; z-index:6; }
.claro .cab { color:#3D2B1Fcc; } .escuro .cab, .foto .cab { color:#E8DED1cc; }
.cab::after { content:''; position:absolute; left:0; right:0; top:42px; height:1px; background:#C9A96299; }
.rod { position:absolute; bottom:80px; left:84px; right:84px; display:flex; justify-content:space-between; align-items:center; font-size:22px; font-weight:600; z-index:6; }
.claro .rod { color:#3D2B1F; } .escuro .rod, .foto .rod { color:#E8DED1; }
.rod .pg { letter-spacing:3px; }
.cg { font-family:'EB Garamond',serif; }
.marca { position:absolute; font-family:'EB Garamond',serif; font-weight:600; line-height:.8; z-index:1; }
.claro .marca { color:#3D2B1F; opacity:.07; } .escuro .marca { color:#C9A962; opacity:.12; }
.bloco { position:absolute; left:84px; z-index:5; }
.num { font-family:'EB Garamond',serif; font-weight:700; font-size:120px; line-height:1; color:#C9A962; }
.claro .num { color:#B8943F; }
.tit { font-family:'EB Garamond',serif; font-weight:600; font-size:84px; line-height:1.02; margin-top:10px; }
.claro .tit em { font-style:italic; color:#3D2B1F; border-bottom:4px solid #C9A962; }
.escuro .tit em, .foto .tit em { font-style:italic; color:#C9A962; }
.txt { font-size:35px; line-height:1.45; margin-top:34px; max-width:600px; }
.claro .txt { color:#3D2B1F; } .escuro .txt { color:#E8DED1; }
.mt { background:linear-gradient(transparent 55%, #C9A96266 55%); font-weight:600; }
.escuro .mt { background:linear-gradient(transparent 55%, #C9A96255 55%); color:#FAF6F0; }
.selo { display:inline-block; margin-top:30px; font-size:24px; font-weight:700; letter-spacing:1px; padding:10px 18px; border-radius:4px; }
.claro .selo { background:#231E1A; color:#E8DED1; } .escuro .selo, .foto .selo { background:#C9A962; color:#231E1A; }
.obj { position:absolute; z-index:4; filter:drop-shadow(0 24px 30px rgba(35,30,26,.35)); }
.arco { position:absolute; border:3px solid #C9A962; border-radius:50%; z-index:3; opacity:.85; }
.papel { position:absolute; background:#FAF6F0; color:#231E1A; padding:64px 60px; box-shadow:0 30px 60px rgba(0,0,0,.35); z-index:5; }
.papel::after { content:''; position:absolute; inset:0; background-image:url("{{ ruido }}"); opacity:.18; mix-blend-mode:multiply; }
.btn { background:#C9A962; color:#231E1A; font-weight:800; font-size:27px; padding:18px 34px; border-radius:999px; }

/* acabamento fosco */
.escuro { background:radial-gradient(ellipse at 65% 25%, #3B3129 0%, #2A231E 55%, #211B17 100%) !important; }
.escuro::before { content:''; position:absolute; inset:0; background:radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,.28) 100%); z-index:0; pointer-events:none; }
.claro { background:#F0E8DB !important; }
.claro::before { content:''; position:absolute; inset:0; background-image:url("{{ fibra }}"); opacity:.10; mix-blend-mode:multiply; z-index:0; pointer-events:none; }
.textura::after { background-image:url("{{ mancha }}") !important; opacity:.10 !important; mix-blend-mode:soft-light !important; }
.foto img:first-child { filter:contrast(.88) brightness(1.04) saturate(.85) sepia(.12); }
.fosco { position:absolute; inset:0; pointer-events:none; z-index:20; }
.fosco.grao { background-image:url("{{ grao }}"); opacity:.13; mix-blend-mode:overlay; }
.fosco.veu { background:rgba(240,232,219,.035); mix-blend-mode:screen; }
.obj { filter:drop-shadow(0 24px 30px rgba(35,30,26,.35)) contrast(.92) saturate(.9) !important; }
</style></head><body><div class="pano">

<!-- 1 CAPA -->
<div class="s escuro textura" style="left:0">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Outubro Rosa</span></div>
  <div class="marca" style="right:-40px; top:180px; font-size:900px;">5</div>
  <div class="bloco" style="top:250px; width:560px;">
    <div class="cg" style="font-style:italic; font-size:64px; color:#E8DED1; line-height:1.05;">Os direitos da trabalhadora</div>
    <div class="cg" style="font-size:150px; font-weight:700; line-height:.95; color:#C9A962; margin-top:18px; white-space:nowrap;">5 direitos</div>
    <div class="cg" style="font-style:italic; font-size:62px; color:#E8DED1; line-height:1.1; margin-top:14px;">que quase ninguém usa</div>
    <div style="width:120px; height:2px; background:#C9A962; margin:44px 0 26px;"></div>
    <div style="font-size:30px; line-height:1.45; color:#E8DED1; width:470px;">Exames, FGTS e proteção contra demissão: o que a lei garante <span class="mt">neste Outubro Rosa</span>.</div>
  </div>
  <img class="obj" src="{{ leticia_capa }}" style="right:-90px; bottom:0; height:940px; filter:drop-shadow(-20px 10px 40px rgba(0,0,0,.45)); z-index:4;">
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">01 / 07</span></div>
</div>

<!-- 2 ITEM 1 (claro) -->
<div class="s claro textura" style="left:1080px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>
  <div class="marca" style="right:20px; top:150px; font-size:560px;">01</div>
  <div class="bloco" style="top:300px;">
    <div class="num">01</div>
    <div class="tit">Até 3 dias por ano<br>para <em>exames</em></div>
    <div class="txt">Mamografia, preventivo e outros exames de câncer, <span class="mt">sem desconto no salário</span>. Leve o comprovante da clínica.</div>
    <div class="selo">CLT, art. 473, XII</div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">02 / 07</span></div>
</div>

<!-- 3 ITEM 2 (escuro) -->
<div class="s escuro textura" style="left:2160px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>
  <div class="marca" style="right:20px; top:150px; font-size:560px;">02</div>
  <div class="bloco" style="top:300px;">
    <div class="num">02</div>
    <div class="tit">A empresa tem que<br>falar de <em>prevenção</em></div>
    <div class="txt">A Lei 15.377/2026 obriga as empresas a divulgar <span class="mt">campanhas de prevenção ao câncer</span> e de vacinação contra o HPV.</div>
    <div class="selo">Lei 15.377/2026</div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">03 / 07</span></div>
</div>

<!-- 4 ITEM 3 (claro) -->
<div class="s claro textura" style="left:3240px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>
  <div class="marca" style="right:20px; top:150px; font-size:560px;">03</div>
  <div class="bloco" style="top:300px;">
    <div class="num">03</div>
    <div class="tit">O diagnóstico<br>libera o <em>FGTS</em></div>
    <div class="txt">Câncer da trabalhadora ou de um dependente permite <span class="mt">sacar o saldo do FGTS</span>.</div>
    <div class="selo">Lei 8.036/1990, art. 20, XI</div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">04 / 07</span></div>
</div>

<!-- 5 ITEM 4 (foto + papel) -->
<div class="s foto" style="left:4320px">
  <img src="{{ foto5 }}" style="position:absolute; inset:0; width:1080px; height:1350px;">
  <div style="position:absolute; inset:0; background:linear-gradient(180deg, rgba(35,30,26,.55), rgba(35,30,26,.35) 40%, rgba(35,30,26,.75));"></div>
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>
  <div class="papel" style="left:120px; top:360px; width:760px; transform:rotate(-3deg);">
    <div class="num" style="color:#B8943F;">04</div>
    <div class="cg" style="font-size:78px; font-weight:600; line-height:1.02; margin-top:6px;">Demissão por causa<br>da <em style="font-style:italic; border-bottom:4px solid #C9A962;">doença</em></div>
    <div style="font-size:33px; line-height:1.45; margin-top:28px; color:#3D2B1F;">A Justiça presume discriminatória a dispensa de quem tem doença grave. <span class="mt">Pode gerar reintegração.</span></div>
    <div class="selo" style="background:#231E1A; color:#E8DED1;">Súmula 443 do TST</div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">05 / 07</span></div>
</div>

<!-- 6 ITEM 5 (claro, o que guardar) -->
<div class="s claro textura" style="left:5400px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>
  <div class="marca" style="right:20px; top:150px; font-size:560px;">05</div>
  <div class="bloco" style="top:290px;">
    <div class="num">05</div>
    <div class="tit">Confira a <em>convenção</em><br>da sua categoria</div>
    <div class="txt" style="max-width:640px;">Muitos acordos coletivos garantem mais. Salve e confira na sua:</div>
    <div style="margin-top:26px; font-size:31px; line-height:1.7; color:#231E1A;">
      ☐ Estabilidade após o afastamento<br>☐ Dias para acompanhar exames<br>☐ Complemento do auxílio-doença
    </div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">06 / 07</span></div>
</div>

<!-- 7 FECHAMENTO (escuro) -->
<div class="s escuro textura" style="left:6480px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Outubro Rosa</span></div>
  <div class="bloco" style="top:330px; left:500px; width:520px;">
    <div class="cg" style="font-size:78px; font-weight:600; line-height:1.02; color:#FAF6F0;">Cuidar da saúde<br>é <em style="font-style:italic; color:#C9A962;">direito</em>.</div>
    <div class="cg" style="font-style:italic; font-size:56px; color:#E8DED1; margin-top:18px;">Não é favor da empresa.</div>
    <div style="font-size:30px; line-height:1.45; color:#E8DED1; margin-top:40px;"><span class="mt">Salve este post</span> e mande para uma colega de trabalho.</div>
    <div style="margin-top:48px;"><span class="btn">⚖️ Procure uma advogada</span></div>
  </div>
  <div class="rod"><span>@adv.leticiabarros2</span><span class="pg">OAB/ES 39.948</span></div>
</div>
<img class="obj" src="{{ leticia_fecho }}" style="left:6400px; bottom:0; height:800px; z-index:4;">

<!-- elementos contínuos -->
<div class="arco" style="left:1700px; top:860px; width:1150px; height:1150px;"></div>
<div class="arco" style="left:4950px; top:-620px; width:1000px; height:1000px;"></div>
<img class="obj" src="{{ estetoscopio }}" style="left:1640px; top:930px; width:720px; transform:rotate(-12deg);">
<img class="obj" src="{{ laco }}" style="left:2900px; top:930px; height:620px; transform:rotate(58deg);">
<img class="obj" src="{{ reais }}" style="left:3800px; top:960px; width:700px; transform:rotate(-8deg);">
<div class="fosco grao"></div><div class="fosco veu"></div>
</div></body></html>""")


async def main() -> None:
    html = HTML.render(
        grao=GRAO, mancha=MANCHA, fibra=FIBRA, ruido=RUIDO, leticia_capa=png("leticia-real-sentada.png"), leticia_fecho=png("leticia-real-sorrindo.png"), estetoscopio=png("corte-estetoscopio.png"),
        laco=png("corte-laco2.png"), reais=png("corte-reais.png"),
        foto5=foto(FOTOS / "8872674.jpg", foco=0.2),
    )
    (AQUI / "pecas").mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 7560, "height": 1350})
        await page.set_content(html, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        buf = await page.screenshot(type="png")
        await browser.close()
    pano = Image.open(io.BytesIO(buf)).convert("RGB")
    for i in range(7):
        destino = AQUI / "pecas" / f"outubro-rosa-trabalho-v4-{i + 1}.png"
        pano.crop((i * 1080, 0, (i + 1) * 1080, 1350)).save(destino)
        render_criativo._aplicar_acabamento_dourado(str(destino))
        Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
        destino.unlink()
    print("ok")


if __name__ == "__main__":
    asyncio.run(main())
