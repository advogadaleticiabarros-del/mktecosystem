"""Estilo Manchete (docs/ESTILO_MANCHETE.md): layouts da referência de 05/11/2026 em café e ouro, com as faixas douradas.
Uso: python gerar.py [prefixo]. As peças 04 a 13 ficam em fora_da_caixa.py. Grava em pecas/ (fora do git). Nunca sobrescreva peça pronta: peça nova = nome novo."""
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
ACAB = next((RAIZ / "apps" / "api" / "app" / "assets").glob("*dourad*"))
BANCO = RAIZ / "apps" / "api" / "_saida_producao_1510" / "_fotos_pexels"
DRA = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\images\hero-leticia-sem-fundo.png")
SAIDA = AQUI / "pecas"
CAFE, FUNDO, PAPEL, AREIA = "#1E1814", "#231E1A", "#F7F1E7", "#EFE6D9"
FOIL = "linear-gradient(112deg,#a57a2c 0%,#dcbc6a 14%,#f9efc2 27%,#d2aa54 41%,#a67c2e 56%,#ebd590 70%,#fcf4cc 80%,#bb923f 100%)"
MARCA = "linear-gradient(112deg,#c9a14e 0%,#e8d08a 18%,#f9efc2 34%,#d8b566 52%,#c9a14e 68%,#f1dfa2 84%,#cfa85a 100%)"
PERFIL = "@adv.leticiabarros2"

BASE = f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500;1,700&family=Inter:wght@300;400;500;600&display=swap" rel=stylesheet>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
.c{{width:1080px;height:1440px;position:relative;overflow:hidden;color:{CAFE};font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
.abs{{position:absolute}}
.p{{font-family:'Playfair Display',serif}}
.topo{{position:absolute;left:72px;right:72px;top:52px;display:flex;justify-content:space-between;font:500 22px Inter;letter-spacing:.04em}}
CSS</style></head><body><div class=c>CORPO</div>
<script>document.fonts.ready.then(()=>{{document.body.dataset.ok=1}})</script></body></html>"""


def foto(caminho, largura=1500, formato="JPEG"):
    f = Image.open(caminho).convert("RGBA" if formato == "PNG" else "RGB")
    if f.width > largura:
        f.thumbnail((largura, largura * 2), Image.LANCZOS)
    elif formato == "PNG":
        f = f.resize((largura, round(f.height * largura / f.width)), Image.LANCZOS)
    b = io.BytesIO()
    f.save(b, formato, **({"quality": 92} if formato == "JPEG" else {}))
    return f"data:image/{formato.lower()};base64," + base64.b64encode(b.getvalue()).decode()


def te_disseram():
    """Layout 'Te disseram que só Atrasos...': foto em cima, escuro embaixo, título central com fita."""
    return ("", f"""
<div class=abs style="inset:0;background:{FUNDO}"></div>
<div class=abs style="left:0;top:-470px;width:1080px;height:1620px;background:url({foto(BANCO / 'original-desempregada-gravida-inss.jpg', 1400)}) center/cover"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(30 24 20/.55) 0,rgb(30 24 20/0) 13%,rgb(30 24 20/0) 50%,rgb(30 24 20/.88) 62%,{FUNDO} 69%)"></div>
<div class=topo style="color:{AREIA}"><span>LETÍCIA BARROS</span><span>DIREITO TRABALHISTA</span></div>
<div class=abs style="left:0;right:0;top:864px;text-align:center;color:#fff">
  <div style="font:300 56px Inter;letter-spacing:-.01em">Te disseram que só</div>
  <div class=p style="font-size:168px;line-height:1.02;font-style:italic;font-weight:400;margin-top:-4px;letter-spacing:-.01em">Gestantes</div>
  <div style="position:relative;display:inline-block;background:{MARCA};color:{CAFE};font:300 46px Inter;padding:4px 24px 7px;margin-top:-14px"><b style="font-weight:600">que já avisaram</b> têm</div>
  <div class=p style="font-size:142px;line-height:1.14;font-style:italic;font-weight:400;letter-spacing:-.01em">Estabilidade?</div>
</div>
<div class=abs style="left:0;right:0;bottom:64px;text-align:center;font:500 24px Inter;letter-spacing:.08em;color:{AREIA}">LEIA A LEGENDA</div>""")


def caderno():
    """Layout 'O passageiro não leu, mas assinou': caderno inclinado, espiral à esquerda, caneta à direita."""
    aros = "".join(f'<div class=aro style="top:{50 + i * 84}px"></div>' for i in range(17))
    css = f"""
.fl{{position:absolute;left:96px;top:-34px;width:1010px;height:1510px;transform:rotate(-4deg);background:{PAPEL};
background-image:repeating-linear-gradient(180deg,transparent 0 73px,rgb(30 24 20/.13) 73px 75px);
box-shadow:0 2px 3px rgb(30 24 20/.22),-14px 22px 60px rgb(30 24 20/.22)}}
.aro{{position:absolute;left:-44px;width:92px;height:17px;border-radius:10px;background:linear-gradient(180deg,#5d534b,#14100d 45%,#3a322c);box-shadow:0 3px 4px rgb(30 24 20/.45)}}
.aro::after{{content:"";position:absolute;right:-2px;top:-3px;width:23px;height:23px;border-radius:50%;background:#C9BFB0;z-index:-1}}
.mg{{position:absolute;font:600 22px Inter;letter-spacing:.03em;white-space:nowrap}}
"""
    caneta = """<svg class=abs style="left:834px;top:640px;filter:drop-shadow(16px 14px 12px rgb(30 24 20/.42))" width="170" height="680" viewBox="0 0 190 760">
<defs><linearGradient id="ou" x1="0" x2="1"><stop offset="0" stop-color="#a57a2c"/><stop offset=".35" stop-color="#f9efc2"/><stop offset=".7" stop-color="#c79c49"/><stop offset="1" stop-color="#8c6622"/></linearGradient>
<linearGradient id="co" x1="0" x2="1"><stop offset="0" stop-color="#0d0a07"/><stop offset=".3" stop-color="#5b4c3f"/><stop offset=".5" stop-color="#1a130e"/><stop offset="1" stop-color="#050403"/></linearGradient></defs>
<g transform="rotate(-6 95 380)"><path d="M72 42q23-30 46 0v22H72z" fill="url(#ou)"/><rect x="66" y="62" width="58" height="250" rx="8" fill="url(#co)"/><rect x="66" y="300" width="58" height="16" fill="url(#ou)"/><rect x="66" y="322" width="58" height="8" fill="url(#ou)"/>
<rect x="66" y="330" width="58" height="240" rx="6" fill="url(#co)"/><rect x="66" y="566" width="58" height="12" fill="url(#ou)"/><path d="M68 578h54l-14 66H82z" fill="url(#co)"/><path d="M80 644h30l-9 62-6 22-6-22z" fill="url(#ou)"/><path d="M95 690v30" stroke="#5b4518" stroke-width="2"/></g></svg>"""
    assina = f"""<svg class=abs style="left:840px;top:1252px" width="170" height="74" viewBox="0 0 170 74" fill="none" stroke="{CAFE}" stroke-width="3" stroke-linecap="round"><path d="M6 52c24-34 40-40 44-28s-16 34-20 26 26-26 38-20-6 24 4 22 18-18 30-16 2 14 14 12 22-10 44-14"/></svg>"""
    return (css, f"""
<div class=abs style="inset:0;background:linear-gradient(135deg,#fff 0%,{AREIA} 100%)"></div>
<div class=fl>{aros}
  <div class=mg style="left:70px;top:44px;opacity:.75">CLÁUSULA 1ª. PEDIDO DE DEMISSÃO. A EMPREGADA DECLARA, POR LIVRE E ESPONTÂNEA</div>
  <div class=mg style="left:70px;bottom:44px;opacity:.75">CLÁUSULA 2ª. NADA MAIS HAVENDO A RECLAMAR, A EMPREGADA DÁ PLENA QUITAÇÃO</div>
</div>
<div class=abs style="left:128px;top:236px;width:850px;transform:rotate(-4deg);text-align:center">
  <span style="display:inline-block;font:500 24px Inter;padding:7px 22px;border:1.5px solid {CAFE};border-radius:30px;background:{PAPEL}">{PERFIL}</span>
  <div style="font:300 84px Inter;letter-spacing:-.015em;margin-top:70px">A gestante</div>
  <div class=p style="font-size:112px;line-height:1.12;font-weight:500;margin-top:12px;letter-spacing:-.005em">NÃO LEU, MAS<br>ASSINOU:</div>
  <div class=p style="display:inline-block;font-size:72px;font-style:italic;font-weight:700;margin-top:18px;padding-bottom:6px;border-bottom:6px solid;border-image:{FOIL} 1">e agora?</div>
  <div style="margin-top:118px"><span style="display:inline-flex;align-items:center;gap:14px;background:{MARCA};font:500 34px Inter;padding:15px 34px">
  <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="{CAFE}" stroke-width="1.8"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12.5h5"/></svg>leia a legenda</span></div>
</div>
{assina}{caneta}""")


def palavra():
    """Layout 'ADVOGADO / dia do Advogado': palavra gigante atrás da pessoa, título em itálico na frente, selo redondo."""
    letra = f"position:absolute;left:-24px;font:600 356px/1 Inter;letter-spacing:-.03em;white-space:nowrap;background:{FOIL};-webkit-background-clip:text;background-clip:text;color:transparent;padding:0 40px 30px 0"
    selo = f"""<svg class=abs style="left:800px;top:770px" width="232" height="232" viewBox="0 0 232 232">
<defs><path id="cir" d="M116 116m-84 0a84 84 0 1 1 168 0a84 84 0 1 1-168 0"/></defs>
<circle cx="116" cy="116" r="114" fill="rgb(30 24 20/.72)" stroke="#e8d08a" stroke-width="2"/>
<text font-family="Inter" font-weight="500" font-size="23" fill="{AREIA}" letter-spacing="1.3"><textPath href="#cir">LETÍCIA BARROS · ADVOCACIA ·</textPath></text>
<text x="116" y="110" text-anchor="middle" font-family="Inter" font-weight="500" font-size="24" fill="{AREIA}">OAB/ES</text>
<text x="116" y="146" text-anchor="middle" font-family="Playfair Display" font-weight="500" font-size="36" fill="#e8d08a">39.948</text></svg>"""
    return ("", f"""
<div class=abs style="inset:0;background:radial-gradient(70% 55% at 50% 40%,#7a6856 0%,#4a3d32 52%,{FUNDO} 100%)"></div>
<div style="{letra};top:100px">TRABA</div>
<div style="{letra};top:420px;left:0;width:1080px;display:flex;justify-content:space-between;padding-right:0"><span>L</span><span>H</span><span>O</span></div>
<img class=abs src="{foto(DRA, 1200, 'PNG')}" style="left:120px;top:236px;width:840px">
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(35 30 26/0) 58%,rgb(35 30 26/.88) 76%,{FUNDO} 88%)"></div>
{selo}
<div class=topo style="color:{AREIA}"><span>LETÍCIA BARROS</span><span>DIREITO TRABALHISTA</span></div>
<div class=abs style="left:0;right:0;top:1022px;text-align:center;color:#fff">
  <div style="font:300 60px Inter;letter-spacing:-.01em">direito do</div>
  <div class=p style="font-size:196px;line-height:1.08;font-style:italic;font-weight:400;margin-top:-10px">Trabalho</div>
</div>
<div class="abs p" style="left:0;right:0;bottom:62px;text-align:center;font-size:34px;font-weight:500;letter-spacing:.14em;color:{AREIA}">LETÍCIA BARROS</div>""")


APROVADAS = {"manchete-01-te-disseram": te_disseram, "manchete-02-caderno": caderno, "manchete-03-palavra": palavra}


async def main():
    from fora_da_caixa import LOTE

    so = sys.argv[1:]
    pecas = APROVADAS | LOTE
    SAIDA.mkdir(exist_ok=True)
    ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for nome, fn in pecas.items():
            if so and not any(nome.startswith(x) for x in so):
                continue
            css, corpo = fn()
            await pg.set_content(BASE.replace("CSS</style>", css + "</style>").replace("CORPO", corpo), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(SAIDA / f"{nome}.jpg", quality=90)
            print(nome)
        await b.close()
    fs = [SAIDA / f"{n}.jpg" for n in pecas]
    if all(f.exists() for f in fs):
        linhas = (len(fs) + 3) // 4
        grade = Image.new("RGB", (4 * 480 + 24, linhas * 648 - 8), "white")
        for i, f in enumerate(fs):
            grade.paste(Image.open(f).resize((480, 640), Image.LANCZOS), ((i % 4) * 488, (i // 4) * 648))
        grade.save(AQUI / "grade.jpg", quality=86)


if __name__ == "__main__":
    asyncio.run(main())
