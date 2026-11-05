"""Palavra de Ouro: dourado, textura fosca, tipografia, cabeçalho e assinatura."""
import asyncio
import base64
import io
import json
import random
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

API = Path(__file__).resolve().parents[3] / "apps" / "api"
ENSAIO = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\images\hero-leticia-sem-fundo.png")
AQUI = Path(__file__).resolve().parent
ACAB = next((API / "app/assets").glob("*dourad*"))
LOGO = "data:image/png;base64," + base64.b64encode((API / "app/assets/logo-leticia.png").read_bytes()).decode()
PAPEL, CAFE, FUNDO = "#EFE6D9", "#1E1814", "#231E1A"
FOIL = "linear-gradient(112deg,#a57a2c 0%,#dcbc6a 14%,#f9efc2 27%,#d2aa54 41%,#a67c2e 56%,#ebd590 70%,#fcf4cc 80%,#bb923f 100%)"
MARCA = "linear-gradient(112deg,#c9a14e 0%,#e8d08a 18%,#f9efc2 34%,#d8b566 52%,#c9a14e 68%,#f1dfa2 84%,#cfa85a 100%)"
PARADAS = [("0", "#a57a2c"), (".14", "#dcbc6a"), (".27", "#f9efc2"), (".41", "#d2aa54"), (".56", "#a67c2e"), (".7", "#ebd590"), (".8", "#fcf4cc"), ("1", "#bb923f")]
DEF_FOIL = '<linearGradient id="fo" x1="0" y1="0" x2="1" y2=".35">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in PARADAS) + "</linearGradient>"


def dra(largura):
    m = Image.open(ENSAIO).convert("RGBA")
    if largura > m.width:
        m = m.resize((largura, round(m.height * largura / m.width)), Image.LANCZOS)
    b = io.BytesIO()
    m.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def ruido(freq, cor, alfa, oit=3):
    return ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='900' height='900'%3E%3Cfilter id='n'%3E"
            f"%3CfeTurbulence type='fractalNoise' baseFrequency='{freq}' numOctaves='{oit}' stitchTiles='stitch'/%3E"
            f"%3CfeColorMatrix values='0 0 0 0 {cor} 0 0 0 0 {cor} 0 0 0 0 {cor} 0 0 0 {alfa} 0'/%3E%3C/filter%3E"
            "%3Crect width='900' height='900' filter='url(%23n)'/%3E%3C/svg%3E")


BASE = """<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{margin:0;padding:0;box-sizing:border-box}
.c{width:1080px;height:1440px;position:relative;overflow:hidden;background:PAPEL;color:CAFE;font-family:Inter,sans-serif;font-variant-numeric:lining-nums;font-kerning:normal;isolation:isolate}
.c.esc{background:FUNDO;color:PAPEL}
.c::before,.c::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none}
.c::before{background:url("GRAO1");mix-blend-mode:multiply;opacity:.085}
.c::after{background:url("GRAO2");mix-blend-mode:multiply;opacity:.045}
.c.esc::before{background:url("GRAO3");mix-blend-mode:screen;opacity:.03}.c.esc::after{display:none}
.abs{position:absolute}
.cab{position:absolute;left:96px;right:96px;top:72px}
.ox1{height:5px;background:FOIL}.ox2{height:2px;background:FOIL;margin-top:4px}
.lin{display:flex;justify-content:space-between;align-items:baseline;font:500 24px Inter;margin-top:20px}
.lin span:first-child{font-weight:600;letter-spacing:.12em;text-transform:uppercase}
.g{font-family:'EB Garamond',serif;font-weight:500;letter-spacing:-.015em}
.g i{font-weight:400}
.f{background:FOIL;-webkit-background-clip:text;background-clip:text;color:transparent;padding:.12em .1em .16em 0;margin-bottom:-.16em;display:inline-block}
.m{background:MARCA;padding:.02em .2em .06em;margin-left:-.2em;color:CAFE;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.rr{position:relative;display:inline-block}
.rr::after{content:"";position:absolute;left:-10px;right:-10px;top:52%;height:7px;background:FOIL;transform:rotate(-1deg);box-shadow:0 2px 6px rgb(30 24 20/.3)}
.rr.fino::after{height:4px;top:54%}
.corpo{font:400 36px/1.34 Inter}
.peq{font:500 24px/1.4 Inter}
.ass{position:absolute;left:96px;bottom:96px;display:flex;align-items:center;gap:16px;font:500 24px Inter}
.ass img{width:52px;height:52px}
CSS</style></head><body><div class="c CLASSE">CORPO</div>
<script>document.fonts.ready.then(()=>{document.body.dataset.ok=1})</script></body></html>"""
BASE = (BASE.replace("GRAO1", ruido(".95", ".25", ".9")).replace("GRAO2", ruido(".012 .85", ".3", ".8", 2)).replace("GRAO3", ruido(".95", ".9", ".9"))
        .replace("PAPEL", PAPEL).replace("CAFE", CAFE).replace("FUNDO", FUNDO).replace("FOIL", FOIL).replace("MARCA", MARCA))


def cab(a, b="Letícia Barros · OAB/ES 39.948"):
    return f'<div class=cab><div class=ox1></div><div class=ox2></div><div class=lin><span>{a}</span><span>{b}</span></div></div>'


ASS = f'<div class=ass><img src="{LOGO}">Letícia Barros &nbsp;·&nbsp; OAB/ES 39.948</div>'
