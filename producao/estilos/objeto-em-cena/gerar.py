"""Objeto em Cena (nome provisório): 3 peças de teste. Uso: python gerar.py [prefixo].
Um objeto ou gesto real em primeiro plano, e o texto integrado a ele. Grava em pecas/ (fora do git).
Nunca sobrescreva peça pronta: peça nova = nome novo."""
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "palavra-de-ouro"))
from base import ACAB, BASE, CAFE, FOIL, FUNDO, LOGO, MARCA  # noqa: E402

BANCO = AQUI.parents[2] / "apps" / "api" / "_saida_producao_1510" / "_fotos_pexels"
SAIDA = AQUI / "pecas"
PERFIL = "@adv.leticiabarros2"


def foto(caminho, largura=1500):
    f = Image.open(caminho).convert("RGB")
    f.thumbnail((largura, largura * 2), Image.LANCZOS)
    b = io.BytesIO()
    f.save(b, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


CSS = f"""
.pil{{position:absolute;left:50%;top:64px;transform:translateX(-50%);padding:9px 24px;border-radius:30px;font:500 24px Inter;white-space:nowrap}}
.pil.vd{{background:rgb(30 24 20/.62);color:#EFE6D9;backdrop-filter:blur(10px);border:1px solid rgb(232 208 138/.55)}}
.pil.cl{{background:#FBF6EC;color:{CAFE};border:1px solid rgb(30 24 20/.16)}}
.leia{{position:absolute;right:72px;bottom:82px;display:flex;align-items:center;gap:12px;padding:13px 26px;border-radius:30px;background:{MARCA};color:{CAFE};font:600 24px Inter}}
.rod{{position:absolute;left:72px;bottom:90px;display:flex;align-items:center;gap:14px;font:500 24px Inter}}
.rod img{{width:50px;height:50px}}
.fita{{background:{MARCA};color:{CAFE};padding:0 .2em .05em;margin-left:-.2em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
"""
BALAO = f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{CAFE}" stroke-width="2"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12.5h5"/></svg>'
LEIA = f'<div class=leia>{BALAO}leia a legenda</div>'


def rod(cor):
    return f'<div class=rod style="color:{cor}"><img src="{LOGO}">Letícia Barros · OAB/ES 39.948</div>'


def te_disseram():
    """Referência: foto de pessoa e pergunta 'Te disseram...' com fita no trecho-chave."""
    return (CSS, f"""
<div class=abs style="left:0;right:0;top:-170px;height:1440px;background:url({foto(AQUI / 'fotos' / 'ultrassom-sem-dados.png')}) center/cover"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(35 30 26/0) 44%,rgb(35 30 26/.88) 62%,{FUNDO} 72%)"></div>
<div class="pil vd">{PERFIL}</div>
<div class="abs g" style="left:72px;right:72px;top:770px;font-size:92px;line-height:1.14;color:#EFE6D9">Te disseram que<br>só tem <i>estabilidade</i><br>quem <span class=fita style="margin-left:0;padding:0 .16em .02em">já avisou o patrão?</span></div>
<div class="abs corpo" style="left:72px;width:900px;top:1110px;font-size:32px;color:#EFE6D9">A empresa não saber da gravidez não tira o direito. O que conta é a gravidez já existir na dispensa.</div>
<div class="abs peq" style="left:72px;top:1214px;color:#E8DED1">TST, Súmula 244, I. Cada caso precisa ser avaliado.</div>
{rod('#EFE6D9')}{LEIA}""", "esc")


def caderno():
    """Referência: caderno com o texto dentro do objeto. A prova é o clímax da voz da Dra."""
    aros = "".join(f'<div class=aro style="top:{38 + i * 62}px"></div>' for i in range(16))
    linhas = "".join(f'<div class=item><b>{a}</b><span>{b}</span></div>' for a, b in [
        ("Data e hora", "de cada episódio"),
        ("O que foi dito", "com as palavras exatas"),
        ("Quem viu", "ou quem ouviu"),
    ])
    css = CSS + f"""
.c{{background:#E8DED1!important}}
.cad{{position:absolute;left:84px;top:142px;width:912px;height:1060px;transform:rotate(-2deg);background:#FBF6EC;border-radius:6px 16px 16px 6px;
box-shadow:0 2px 3px rgb(30 24 20/.28),10px 16px 26px rgb(30 24 20/.2),30px 50px 90px rgb(30 24 20/.28),inset 34px 0 34px -30px rgb(30 24 20/.16)}}
.aro{{position:absolute;left:-26px;width:74px;height:20px;border-radius:12px;background:{FOIL};box-shadow:0 3px 4px rgb(30 24 20/.45),inset 0 1px 1px rgb(255 255 255/.6)}}
.aro::after{{content:"";position:absolute;left:58px;top:4px;width:12px;height:12px;border-radius:50%;background:#3b332b}}
.item{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid rgb(30 24 20/.2);padding:26px 0 18px;font:400 30px Inter}}
.item b{{font:500 56px 'EB Garamond',serif;letter-spacing:-.015em}}
"""
    caneta = """<svg class=abs style="left:716px;top:748px;filter:drop-shadow(10px 18px 12px rgb(30 24 20/.42))" width="330" height="500" viewBox="0 0 330 500">
<defs><linearGradient id="ou" x1="0" x2="1"><stop offset="0" stop-color="#a57a2c"/><stop offset=".35" stop-color="#f9efc2"/><stop offset=".7" stop-color="#c79c49"/><stop offset="1" stop-color="#8c6622"/></linearGradient>
<linearGradient id="co" x1="0" x2="1"><stop offset="0" stop-color="#16110d"/><stop offset=".38" stop-color="#5b4c3f"/><stop offset=".6" stop-color="#231a14"/><stop offset="1" stop-color="#0d0a07"/></linearGradient></defs>
<g transform="rotate(32 165 250)"><rect x="147" y="-50" width="38" height="390" rx="17" fill="url(#co)"/><rect x="147" y="150" width="38" height="16" fill="url(#ou)"/><rect x="178" y="-26" width="8" height="150" rx="4" fill="url(#ou)"/>
<path d="M147 340h38l-13 72h-12z" fill="url(#co)"/><path d="M152 372h28l-9 62-5 18-5-18z" fill="url(#ou)"/></g></svg>"""
    return (css, f"""
<div class="pil cl">{PERFIL}</div>
<div class=cad>{aros}
  <div class=abs style="left:92px;right:64px;top:62px">
    <div style="font:600 24px Inter;letter-spacing:.12em">ASSÉDIO MORAL</div>
    <div class=g style="font-size:112px;line-height:1.04;margin-top:30px">Humilhada no trabalho?</div>
    <div class=g style="font-size:66px;line-height:1.3;margin-top:24px"><i>Comece por</i> <span class=fita style="margin-left:0">este caderno.</span></div>
    <div style="margin-top:44px;width:680px">{linhas}</div>
    <div class=corpo style="margin-top:44px;width:600px;font-size:34px">Guarde também mensagens e <span style="white-space:nowrap">e-mails</span>. Anotar ajuda a provar.</div>
  </div>
</div>{caneta}
{rod(CAFE)}{LEIA}""", "")


def relogio():
    """Referência: objeto no centro, 'Você sabia?' e a fita que cinta o objeto."""
    arq = foto(AQUI / "fotos" / "relogio-sem-marca.png")
    texto = " &nbsp;✦&nbsp; ".join(["NO MÍNIMO 50% A MAIS", "CF, ART. 7º, XVI", "CLT, ART. 59"])
    css = CSS + f"""
.etq{{display:inline-block;background:{MARCA};color:{CAFE};font:600 26px Inter;padding:9px 20px;border-radius:8px;transform:rotate(-2deg)}}
.cinta{{position:absolute;left:-90px;width:1260px;height:62px;line-height:62px;background:{MARCA};color:{CAFE};font:600 25px Inter;letter-spacing:.06em;white-space:nowrap;text-align:center;box-shadow:0 10px 22px rgb(0 0 0/.45)}}
"""
    return (css, f"""
<div class=abs style="inset:0;background:url({arq}) center/cover;filter:blur(90px) sepia(.3) saturate(.8) brightness(.8);transform:scale(1.3)"></div>
<div class=abs style="left:80px;top:470px;width:920px;height:920px;background:url({arq}) center/cover;filter:sepia(.3) saturate(.8) contrast(1.05) brightness(.96);-webkit-mask-image:linear-gradient(90deg,transparent,#000 16%,#000 84%,transparent),linear-gradient(180deg,transparent,#000 18%);-webkit-mask-composite:source-in;mask-composite:intersect"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,{FUNDO} 30%,rgb(35 30 26/0) 52%,rgb(35 30 26/0) 82%,{FUNDO} 95%)"></div>
<div class="pil vd">{PERFIL}</div>
<div class=abs style="left:0;right:0;top:148px;text-align:center;color:#EFE6D9">
  <span class=etq>Você sabia?</span>
  <div class=g style="font-size:88px;line-height:1.2;margin-top:18px">Ficar depois da hora<br><i>não é favor,</i> <span class=fita style="margin-left:0;padding:0 .16em .02em">é hora extra.</span></div>
</div>
<div class=cinta style="top:1186px;transform:rotate(-5deg)">{texto}</div>
{rod('#EFE6D9')}{LEIA}""", "esc")


PECAS = {"01-te-disseram": te_disseram, "02-caderno": caderno, "03-relogio": relogio}


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for nome, fn in PECAS.items():
            if so and not any(nome.startswith(s) for s in so):
                continue
            css, corpo, classe = fn()
            await pg.set_content(BASE.replace("CSS</style>", css + "</style>").replace("CORPO", corpo).replace("CLASSE", classe), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(SAIDA / f"{nome}.jpg", quality=90)
            print(nome)
        await b.close()
    fs = [SAIDA / f"{n}.jpg" for n in PECAS]
    if all(f.exists() for f in fs):
        tira = Image.new("RGB", (3 * 720 + 16, 960), "white")
        for i, f in enumerate(fs):
            tira.paste(Image.open(f).resize((720, 960), Image.LANCZOS), (i * 728, 0))
        tira.save(AQUI / "tira.jpg", quality=88)


asyncio.run(main())
