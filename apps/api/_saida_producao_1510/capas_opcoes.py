"""Quatro opções de capa premium para o carrossel da pensão (09/10/2026).

Pedido da Letícia: capas com brilho, personalidade e título que chame atenção, fotos em alta
resolução sem cortes feios. Referência: "Cartão jurídico premium em tons dourados" (luz
dourada acetinada, medalhão, profundidade) + estudo de 09/10 (luz dramática, grão, serifa
grande + sans pequena, vidro). Renderiza em 2x (2160×2700) e reduz para 1080×1350.

Uso (de apps/api): python _saida_producao_1510/capas_opcoes.py
"""
import asyncio
import base64
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo  # noqa: E402

AQUI = Path(__file__).resolve().parent
FOTO = AQUI / "_fotos_pexels" / "original-pensao300.jpg"  # 3905×5857; rosto ~(0.52, 0.27), cupom ~(0.72, 0.63)
SAIDA = AQUI / "pecas" / "capas-opcoes"


def recorte(caminho: Path, w: int, h: int, cx: float, cy: float, zoom: float = 1.0) -> str:
    """Recorte na proporção w:h centrado em (cx, cy) da foto, em 2x da resolução pedida."""
    im = Image.open(caminho).convert("RGB")
    W, H = im.size
    alvo = w / h
    cw, ch = (W, W / alvo) if W / H < alvo else (H * alvo, H)
    cw, ch = cw / zoom, ch / zoom
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w * 2, h * 2), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=93)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


BASE = r"""
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;0,800;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html { font-variant-numeric: lining-nums; }
body { width:1080px; height:1350px; overflow:hidden; font-family:'Inter',sans-serif; }
.c { position:absolute; inset:0; overflow:hidden; }
.g { font-family:'EB Garamond',serif; }
.ouro { background: linear-gradient(100deg,#8E6E2E 0%,#D9BC74 18%,#FFF1C7 32%,#E2C77F 44%,#B8943F 58%,#F4E2AE 74%,#9C7B3A 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  filter: drop-shadow(0 2px 0 rgba(58,40,14,.55)) drop-shadow(0 14px 34px rgba(0,0,0,.45)); }
.ouro-claro { background: linear-gradient(100deg,#6B4F1D 0%,#A9853E 30%,#D9BC74 46%,#8E6E2E 62%,#B8943F 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent; }
.grao { position:absolute; inset:0; z-index:40; pointer-events:none; opacity:.13; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.25' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>"); }
.cab { position:absolute; top:78px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20;
  font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; }
.pag { position:absolute; bottom:72px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20; font-size:22px; font-weight:600; }
.brilho { position:absolute; z-index:15; width:26px; height:26px; }
.brilho::before { content:''; position:absolute; inset:0; background:#FFF6DA;
  clip-path: polygon(50% 0, 58% 42%, 100% 50%, 58% 58%, 50% 100%, 42% 58%, 0 50%, 42% 42%); filter: drop-shadow(0 0 6px #FFE7A8) drop-shadow(0 0 14px #E9C878); }
.mt { background: linear-gradient(transparent 58%, rgba(201,169,98,.55) 58%); }
</style>
"""

OPCOES = {
    # 1 · Ouro editorial: foto em tela cheia, título metalizado embaixo à esquerda, cupom visível à direita
    "1-ouro-editorial": lambda f: f"""
<div class="c" style="background:#1A1511">
  <img src="{f}" style="position:absolute; inset:0; width:1080px; height:1350px; object-fit:cover; filter:sepia(.18) saturate(.9) contrast(1.08) brightness(.86);">
  <div class="c" style="background:linear-gradient(180deg, rgba(20,15,12,.7) 0%, rgba(20,15,12,0) 22%, rgba(20,15,12,0) 50%, rgba(20,15,12,.82) 74%, rgba(20,15,12,.95) 100%);"></div>
  <div class="c" style="background:linear-gradient(90deg, rgba(20,15,12,.8) 0%, rgba(20,15,12,.35) 45%, rgba(20,15,12,0) 65%);"></div>
  <div class="c" style="mix-blend-mode:screen; background:radial-gradient(ellipse at 92% 6%, rgba(255,214,140,.42), transparent 42%), radial-gradient(ellipse at 0% 100%, rgba(201,169,98,.25), transparent 45%);"></div>
  <div style="position:absolute; inset:38px; border:1.5px solid rgba(233,211,152,.55); border-radius:6px; z-index:12;"></div>
  {''.join(f'<div style="position:absolute; {p} width:60px; height:60px; border-{a}:3px solid #E9D398; border-{b}:3px solid #E9D398; z-index:13;"></div>' for p, a, b in [("top:30px; left:30px;", "top", "left"), ("top:30px; right:30px;", "top", "right"), ("bottom:30px; left:30px;", "bottom", "left"), ("bottom:30px; right:30px;", "bottom", "right")])}
  <div class="cab" style="color:#F4EADB"><span>Letícia Barros · Advocacia</span><span style="color:#E9D398">Pensão alimentícia</span></div>
  <div style="position:absolute; left:84px; bottom:180px; width:600px; z-index:20;">
    <div style="font-size:24px; font-weight:800; letter-spacing:6px; text-transform:uppercase; color:#E9D398;">Pensão de R$ 300</div>
    <div class="g ouro fit" data-w="600" style="font-size:150px; font-weight:800; line-height:.88; margin-top:18px;">Guia de<br>sobrevivência</div>
    <div class="g" style="font-style:italic; font-size:52px; font-weight:500; color:#FAF6F0; margin-top:16px;">para mães que fazem milagre</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:30px 0 22px;"></div>
    <div style="font-size:30px; line-height:1.4; color:#FAF6F0;">Fizemos as contas do mês.<br><b class="mt">Spoiler: não fecha.</b></div>
  </div>
  <div class="brilho" style="left:690px; bottom:520px;"></div><div class="brilho" style="left:640px; bottom:610px; transform:scale(.6)"></div>
  <div class="pag" style="color:#F4EADB"><span>Arraste pro lado ›</span><span style="letter-spacing:3px">01 / 08</span></div>
  <div class="grao"></div>
</div>""",

    # 2 · Luxo acetinado: fundo creme e dourado iluminado, medalhão, foto inteira no arco dourado
    "2-luxo-acetinado": lambda f: f"""
<div class="c" style="background:
   radial-gradient(ellipse at 18% 12%, rgba(255,250,235,.95), transparent 40%),
   radial-gradient(ellipse at 85% 85%, rgba(255,244,214,.8), transparent 45%),
   repeating-linear-gradient(118deg, rgba(255,255,255,0) 0 120px, rgba(255,250,232,.55) 160px, rgba(255,255,255,0) 210px),
   linear-gradient(135deg, #EADBB7 0%, #F6EBCF 30%, #E2CC97 55%, #F3E5C2 78%, #D9C089 100%);">
  <svg style="position:absolute; left:-260px; top:180px; opacity:.35; z-index:1" width="1100" height="1100" viewBox="0 0 1100 1100" fill="none" stroke="#B8943F" stroke-width="2.5"><circle cx="550" cy="550" r="520"/><circle cx="550" cy="550" r="470"/><circle cx="550" cy="550" r="300" stroke-width="1.5"/></svg>
  <div style="position:absolute; inset:34px; border:2px solid rgba(184,148,63,.65); border-radius:22px; z-index:12;"></div>
  <div class="cab" style="color:#5A4420"><span>Letícia Barros · Advocacia</span><span style="color:#8E6E2E">Pensão alimentícia</span></div>
  <img src="{render_criativo._logo_data_uri()}" style="position:absolute; left:466px; top:140px; width:148px; z-index:14; filter:drop-shadow(0 14px 22px rgba(90,62,20,.45));">
  <div style="position:absolute; left:200px; top:250px; width:680px; height:690px; z-index:10; padding:8px; border-radius:340px 340px 26px 26px;
       background:linear-gradient(160deg,#FFF1C7,#C9A962 30%,#8E6E2E 55%,#E9D398 80%,#B8943F); box-shadow:0 40px 70px rgba(90,62,20,.38);">
    <img src="{f}" style="width:100%; height:100%; object-fit:cover; border-radius:332px 332px 20px 20px; filter:sepia(.12) saturate(.92) contrast(1.05);">
  </div>
  <div style="position:absolute; left:84px; right:84px; top:970px; text-align:center; z-index:20;">
    <div style="font-size:23px; font-weight:800; letter-spacing:6px; text-transform:uppercase; color:#7A5C24;">Pensão alimentícia de R$ 300</div>
    <div class="g fit" data-w="912" style="font-size:112px; font-weight:800; line-height:.95; color:#3A2A14; margin-top:12px; text-shadow:0 2px 0 rgba(255,250,235,.8);">Guia de sobrevivência</div>
    <div class="g" style="font-style:italic; font-size:50px; font-weight:600; color:#6B4F1D; margin-top:10px;">para mães que <span style="border-bottom:4px solid #C9A962">fazem milagre</span></div>
  </div>
  <div class="pag" style="color:#5A4420"><span>Arraste pro lado ›</span><span style="letter-spacing:3px">01 / 08</span></div>
  <div class="grao" style="opacity:.08"></div>
</div>""",

    # 3 · Impacto tipográfico: R$ 300 gigante em ouro com relevo, cupom do mês atravessando
    "3-impacto-tipografico": lambda f: """
<div class="c" style="background:radial-gradient(ellipse at 50% 34%, #4A3C30 0%, #2A231E 50%, #15110E 100%);">
  <div class="c" style="mix-blend-mode:screen; background:radial-gradient(ellipse at 50% 30%, rgba(255,214,140,.22), transparent 55%), linear-gradient(115deg, transparent 40%, rgba(255,226,160,.10) 48%, transparent 56%);"></div>
  <div style="position:absolute; inset:38px; border:1.5px solid rgba(233,211,152,.5); border-radius:6px; z-index:12;"></div>
  <div class="cab" style="color:#F4EADB"><span>Letícia Barros · Advocacia</span><span style="color:#E9D398">Pensão alimentícia</span></div>
  <div style="position:absolute; left:0; right:0; top:205px; text-align:center; z-index:20;">
    <div class="g" style="font-style:italic; font-size:56px; font-weight:500; color:#F4EADB;">Pensão alimentícia de</div>
    <div class="g ouro" style="font-size:330px; font-weight:800; line-height:.86; letter-spacing:-6px; margin-top:6px;">R$ 300</div>
  </div>
  <div id="cupom" style="position:absolute; right:92px; top:918px; width:282px; z-index:16; transform:rotate(6deg); zoom:.9; background:#FCFAF5; color:#2B231C; font-family:'Courier New',monospace; padding:30px 30px 34px;
       box-shadow:0 40px 70px rgba(0,0,0,.55);
       -webkit-mask: conic-gradient(from -45deg at bottom, #0000, #000 1deg 89deg, #0000 90deg) bottom/24px 51% repeat-x, conic-gradient(from 135deg at top, #0000, #000 1deg 89deg, #0000 90deg) top/24px 51% repeat-x;">
    <div style="text-align:center; font-weight:700; font-size:22px;">CUPOM DO MÊS</div>
    <div style="border-top:2px dashed #2B231C80; margin:12px 0;"></div>
    <div style="display:flex; justify-content:space-between; font-size:23px; line-height:1.6"><span>Mercado</span><span>332,00</span></div>
    <div style="display:flex; justify-content:space-between; font-size:23px; line-height:1.6"><span>Casa</span><span>565,00</span></div>
    <div style="display:flex; justify-content:space-between; font-size:23px; line-height:1.6"><span>Roupas</span><span>385,00</span></div>
    <div style="display:flex; justify-content:space-between; font-size:23px; line-height:1.6"><span>Escola</span><span>305,00</span></div>
    <div style="border-top:2px dashed #2B231C80; margin:12px 0;"></div>
    <div style="display:flex; justify-content:space-between; font-size:26px; font-weight:700"><span>FALTA</span><span style="background:#2B231C; color:#FCFAF5; padding:0 8px">1.287,00</span></div>
  </div>
  <div style="position:absolute; left:84px; top:640px; width:912px; z-index:20;">
    <div class="g fit" data-w="912" style="font-size:104px; font-weight:800; line-height:.92; color:#FAF6F0; text-shadow:0 10px 40px rgba(0,0,0,.5);">Guia de<br>sobrevivência</div>
    <div class="g" style="font-style:italic; font-size:54px; font-weight:600; color:#E2C77F; margin-top:16px;">para mães que fazem milagre</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:30px 0 22px;"></div>
    <div style="font-size:30px; color:#FAF6F0; width:520px;">Fizemos as contas do mês.<br><b class="mt">Spoiler: não fecha.</b></div>
  </div>
  <div class="brilho" style="left:250px; top:300px;"></div><div class="brilho" style="right:180px; top:520px; transform:scale(.7)"></div><div class="brilho" style="left:880px; top:300px; transform:scale(.5)"></div>
  <div class="pag" style="color:#F4EADB"><span>Arraste pro lado ›</span><span style="letter-spacing:3px">01 / 08</span></div>
  <div class="grao"></div>
</div>""",

    # 4 · Painel com luz: texto no café à esquerda, foto inteira em painel vertical à direita
    "4-painel-luz": lambda f: f"""
<div class="c" style="background:radial-gradient(ellipse at 20% 30%, #3D332A 0%, #231E1A 55%, #15110E 100%);">
  <div style="position:absolute; right:0; top:0; width:500px; height:1350px; z-index:5;">
    <img src="{f}" style="width:100%; height:100%; object-fit:cover; filter:sepia(.15) saturate(.92) contrast(1.06) brightness(.95);">
    <div class="c" style="background:linear-gradient(90deg, rgba(21,17,14,.55), transparent 30%), linear-gradient(180deg, rgba(21,17,14,.45), transparent 18%, transparent 82%, rgba(21,17,14,.6));"></div>
  </div>
  <div style="position:absolute; left:578px; top:0; width:4px; height:1350px; z-index:8; background:linear-gradient(180deg, transparent, #E9D398 20%, #FFF3CF 50%, #E9D398 80%, transparent); box-shadow:0 0 30px 6px rgba(233,200,120,.55);"></div>
  <div class="c" style="mix-blend-mode:screen; z-index:9; background:radial-gradient(ellipse at 54% 50%, rgba(255,214,140,.28), transparent 30%);"></div>
  <div style="position:absolute; inset:38px; border:1.5px solid rgba(233,211,152,.5); border-radius:6px; z-index:12;"></div>
  <div class="cab" style="color:#F4EADB; right:540px;"><span>Letícia Barros</span></div>
  <div style="position:absolute; left:84px; top:300px; width:460px; z-index:20;">
    <div style="font-size:23px; font-weight:800; letter-spacing:5px; text-transform:uppercase; color:#E9D398;">Pensão de R$ 300</div>
    <div class="g ouro fit" data-w="460" style="font-size:120px; font-weight:800; line-height:.92; margin-top:22px;">Guia de<br>sobrevivência</div>
    <div class="g" style="font-style:italic; font-size:48px; font-weight:500; color:#FAF6F0; margin-top:22px; line-height:1.08;">para mães que fazem milagre</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:34px 0 24px;"></div>
    <div style="font-size:30px; line-height:1.4; color:#FAF6F0;">Fizemos as contas do mês.<br><b class="mt">Spoiler: não fecha.</b></div>
  </div>
  <div class="brilho" style="left:568px; top:640px;"></div>
  <div class="pag" style="color:#F4EADB; right:560px;"><span>Arraste pro lado ›</span></div>
  <div class="pag" style="left:640px; color:#F4EADB; justify-content:flex-end;"><span style="letter-spacing:3px">01 / 08</span></div>
  <div class="grao"></div>
</div>""",
}

FOCOS = {  # recorte da foto por opção: (largura, altura, cx, cy, zoom)
    "1-ouro-editorial": (1080, 1350, 0.36, 0.44, 1.12),
    "2-luxo-acetinado": (680, 690, 0.56, 0.42, 1.25),
    "3-impacto-tipografico": None,
    "4-painel-luz": (500, 1350, 0.6, 0.5, 1.0),
}


async def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for nome, html in OPCOES.items():
            foco = FOCOS[nome]
            f = recorte(FOTO, *foco) if foco else ""
            await pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'>{BASE}</head><body>{html(f)}</body></html>", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.evaluate("""() => document.querySelectorAll('.fit').forEach(el => { const max = +el.dataset.w; let fs = parseFloat(getComputedStyle(el).fontSize);
                el.style.whiteSpace = 'nowrap'; while (el.scrollWidth > max && fs > 50) { fs -= 2; el.style.fontSize = fs + 'px'; } })""")
            colisoes = await pg.evaluate("""() => { const c = document.getElementById('cupom'); if (!c) return [];
                const r = c.getBoundingClientRect(); const out = [];
                document.querySelectorAll('.pag span, .g, .mt').forEach(el => { const rg = document.createRange(); rg.selectNodeContents(el);
                  for (const t of rg.getClientRects()) if (!(t.right < r.left || t.left > r.right || t.bottom < r.top || t.top > r.bottom)) { out.push(el.textContent.trim().slice(0, 30)); break; } });
                return out; }""")
            if colisoes:
                print("SOBREPOSIÇÃO em", nome, colisoes)
            mestre = SAIDA / f"capa-{nome}-2x.png"
            await pg.screenshot(path=str(mestre))
            render_criativo._aplicar_acabamento_dourado(str(mestre))
            Image.open(mestre).convert("RGB").save(mestre.with_suffix(".jpg"), "JPEG", quality=95)
            Image.open(mestre).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(SAIDA / f"capa-{nome}.jpg", "JPEG", quality=95)
            mestre.unlink()
            print("ok", nome)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
