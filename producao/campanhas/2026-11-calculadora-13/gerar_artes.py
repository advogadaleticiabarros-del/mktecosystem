"""Artes da calculadora do 13º (09/11/2026), no estilo Papel e Ouro (docs/ESTILO_PAPEL_E_OURO.md):
- story-calculadora-13-1080x1920.png: Story com espaço para o adesivo de link (áreas livres: 270 px no topo e 420 embaixo).
- og-calculadora-13-1200x630.jpg: imagem de compartilhamento da LP (WhatsApp, Facebook, Google Discover).
Uso: py producao/campanhas/2026-11-calculadora-13/gerar_artes.py
"""
import base64
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
LOGO = AQUI.parents[2] / "logo" / "logo-sem-fundo.png"
LOGO_URI = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()

ESTILO = """
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #EFE6D9; }
.peca { position: relative; overflow: hidden; background: #EFE6D9; color: #2B231D; font-family: 'Inter', sans-serif;
  background-image: radial-gradient(rgba(43,35,29,.035) 1px, transparent 1px); background-size: 5px 5px; }
.faixa { position: absolute; left: 0; right: 0; height: 10px; background: linear-gradient(90deg,#B4914F,#D8BF86 50%,#B4914F); }
h1 { font-family: 'EB Garamond', serif; font-weight: 500; letter-spacing: -.015em; line-height: 1.02; }
h1 i { font-weight: 400; }
.marca { background: linear-gradient(transparent 60%, #E3CC98 60%); padding: 0 .06em; }
.recibo { background: #FFFDF9; border: 1.5px solid #D6C8B3; position: relative; box-shadow: 0 18px 40px -22px rgba(43,35,29,.45); }
.recibo::before { content: ""; position: absolute; left: 0; right: 0; top: 0; border-top: 5px double #B4914F; }
.cab { display: flex; justify-content: space-between; color: #6E6052; border-bottom: 2px dashed #C9BBA6; }
.lin { display: flex; justify-content: space-between; align-items: baseline; gap: 24px; }
.lin + .lin { border-top: 1.5px solid #E6DCCD; }
.lin span { color: #5A4C40; }
.lin b { font-family: 'EB Garamond', serif; font-weight: 500; white-space: nowrap; }
.assina { display: flex; align-items: center; color: #2B231D; font-weight: 500; }
.assina img { object-fit: contain; }
.assina small { display: block; font-weight: 400; color: #6E6052; }
"""

STORY = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{ESTILO}
.peca {{ width: 1080px; height: 1920px; padding: 300px 96px 0; }}
.faixa.t {{ top: 0; }} .faixa.b {{ bottom: 0; }}
.fio {{ border-top: 5px double #B4914F; width: 180px; margin-bottom: 30px; }}
h1 {{ font-size: 112px; }}
.sub {{ margin-top: 30px; font-size: 36px; line-height: 1.4; color: #5A4C40; max-width: 820px; }}
.recibo {{ margin-top: 52px; padding: 34px 40px 10px; }}
.cab {{ font-size: 26px; letter-spacing: .04em; padding-bottom: 22px; }}
.lin {{ padding: 20px 0; font-size: 30px; }}
.lin b {{ font-size: 46px; }}
.chamada {{ margin-top: 46px; display: flex; align-items: center; gap: 22px; font-size: 40px; font-weight: 500; }}
.chamada svg {{ flex-shrink: 0; }}
.assina {{ position: absolute; left: 96px; bottom: 360px; gap: 20px; font-size: 28px; }}
.assina img {{ width: 76px; height: 76px; }}
.assina small {{ font-size: 24px; }}
</style></head><body><div class="peca">
<div class="faixa t"></div>
<div class="fio"></div>
<h1>Quanto você vai receber de <span class="marca"><i>13º</i></span> este ano?</h1>
<p class="sub">Cada parcela, já com INSS e IR de 2026.</p>
<div class="recibo">
  <div class="cab"><span>Demonstrativo do 13º</span><span>2026</span></div>
  <div class="lin"><span>1ª parcela, sem desconto</span><b>até 30/11</b></div>
  <div class="lin"><span>2ª parcela, com INSS e IR</span><b>até 18/12</b></div>
  <div class="lin"><span>Quem ganha até R$ 5 mil</span><b>sem IR</b></div>
</div>
<div class="chamada">Faça a sua conta no link abaixo
  <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="#B4914F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v15M6 13l6 6 6-6"/></svg></div>
<div class="assina"><img src="{LOGO_URI}" alt=""><div>Letícia Barros<small>Advocacia &amp; Consultoria · OAB/ES 39.948</small></div></div>
<div class="faixa b"></div>
</div></body></html>"""

OG = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{ESTILO}
.peca {{ width: 1200px; height: 630px; padding: 70px 72px; display: grid; grid-template-columns: 1fr 470px; gap: 56px; align-items: center; }}
.faixa.t {{ top: 0; height: 8px; }}
h1 {{ font-size: 70px; }}
.assina {{ margin-top: 40px; gap: 14px; font-size: 21px; }}
.assina img {{ width: 54px; height: 54px; }}
.assina small {{ font-size: 18px; }}
.recibo {{ padding: 28px 30px 10px; }}
.cab {{ font-size: 18px; padding-bottom: 14px; letter-spacing: .04em; }}
.lin {{ padding: 16px 0; font-size: 21px; }}
.lin b {{ font-size: 32px; }}
</style></head><body><div class="peca">
<div class="faixa t"></div>
<div><h1>Calculadora do <span class="marca"><i>13º salário</i></span> 2026</h1>
<div class="assina"><img src="{LOGO_URI}" alt=""><div>Letícia Barros<small>Advocacia &amp; Consultoria · OAB/ES 39.948</small></div></div></div>
<div class="recibo">
  <div class="cab"><span>Demonstrativo do 13º</span><span>2026</span></div>
  <div class="lin"><span>1ª parcela</span><b>até 30/11</b></div>
  <div class="lin"><span>2ª parcela</span><b>até 18/12</b></div>
  <div class="lin"><span>Até R$ 5 mil</span><b>sem IR</b></div>
</div>
</div></body></html>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for html, (w, h), nome in [(STORY, (1080, 1920), "story-calculadora-13-1080x1920.png"),
                                   (OG, (1200, 630), "og-calculadora-13-1200x630.png")]:
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.set_content(html, wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(AQUI / nome))
        b.close()
    png = AQUI / "og-calculadora-13-1200x630.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "3",
                    str(AQUI / "og-calculadora-13-1200x630.jpg")], check=True)
    png.unlink()
    print("ok")


if __name__ == "__main__":
    main()
