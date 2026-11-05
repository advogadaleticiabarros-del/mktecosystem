"""Papel e Ouro: as 9 peças aprovadas. Uso: python gerar.py [prefixo]. Regras em docs/ESTILO_PAPEL_E_OURO.md.
As composições vêm de linha_clara.py e linha_objetos.py. Grava em pecas/ (fora do git).
Nunca sobrescreva peça pronta: peça nova = nome novo."""
import asyncio
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "pecas"


def carregar(arq):
    ns = {"__file__": str(arq), "__name__": "linha"}
    exec(compile(arq.read_text(encoding="utf-8").rsplit("asyncio.run(main())", 1)[0], str(arq), "exec"), ns)
    return ns


V2 = carregar(AQUI / "linha_clara.py")
FORA = carregar(AQUI / "linha_objetos.py")
BR = carregar(AQUI.parent / "palavra-de-ouro" / "base.py")
FOIL, MARCA, DEF = BR["FOIL"], BR["MARCA"], BR["DEF_FOIL"]
ruido = BR["ruido"]
G1, G2, G3 = ruido(".95", ".25", ".9"), ruido(".012 .85", ".3", ".8", 2), ruido(".95", ".9", ".9")
OURO = "#C9A962"
FIO = "linear-gradient(90deg,#9a7026 0%,#c9a14e 18%,#e2c77c 32%,#b98f3c 48%,#9a7026 62%,#d8b768 78%,#ecd591 88%,#a67c2e 100%)"
PARADAS = [("0", "#9a7026"), (".3", "#e2c77c"), (".6", "#9a7026"), (".85", "#ecd591"), ("1", "#a67c2e")]
DEF_FIO = '<linearGradient id="fo" x1="0" y1="0" x2="0" y2="1">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in PARADAS) + "</linearGradient>"
ACABAMENTO = f"""
.grao{{display:none}}
.c{{isolation:isolate}}
.c:not(.esc){{background:#EFE6D9}}
.c::before,.c::after{{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none}}
.c::before{{background:url("{G1}");mix-blend-mode:multiply;opacity:.085}}
.c::after{{background:url("{G2}");mix-blend-mode:multiply;opacity:.045}}
.c.esc::before{{background:url("{G3}");mix-blend-mode:screen;opacity:.03}}
.c.esc::after{{display:none}}
.rc::after{{content:"";position:absolute;inset:0;background:url("{G1}");mix-blend-mode:multiply;opacity:.085;pointer-events:none}}
.ox1,.ox2{{background:{FOIL}}}
.ox1{{height:5px}}
.m{{background:{MARCA};padding:.02em .2em .06em}}
.s,.r{{position:relative;display:inline-block;text-decoration:none}}
.s::after,.r::after{{content:"";position:absolute;background:{FOIL}}}
.s::after{{left:0;right:0;top:95%;height:.055em}}
.r::after{{left:-6px;right:-6px;top:54%;height:.06em}}
.pl,.pl>div+div{{border-image:{FOIL} 1}}
[style*="solid {OURO}"]{{border-image:{FOIL} 1}}
[style*="background:{OURO}"]{{background:{FOIL}!important}}
[style*="background:{OURO}"][style*="color:{BR['CAFE']}"]{{background:{MARCA}!important}}
.c:not(.esc) .ox1,.c:not(.esc) .ox2,.c:not(.esc) .s::after,.c:not(.esc) .r::after{{background:{FIO}}}
.c:not(.esc) .pl,.c:not(.esc) .pl>div+div,.c:not(.esc) [style*="solid {OURO}"]{{border-image:{FIO} 1}}
.c:not(.esc) .r::after{{height:.05em}}
.c:not(.esc) [style*="background:{OURO}"][style*="height:2px"]{{background:{FIO}!important}}
[style*="border-radius:50%;background:{OURO}"]{{background-attachment:fixed!important}}
[style*=";color:{OURO}"],[style^="color:{OURO}"]{{background:{FOIL};-webkit-background-clip:text;background-clip:text;color:transparent!important;padding:.14em .08em .18em 0;margin-top:-.14em;margin-bottom:-.18em}}
"""
# Ordem da grade aprovada pela Jessica em 04/11/2026.
GRADE = ["clara-02-capa-nome", "fora-03-positivo", "clara-05-gritar", "fora-06-recibo", "clara-08-nunca-prometo", "fora-04-errata", "clara-01-lei-tarjada", "fora-10-23h47", "clara-07-rapidinho"]
TODAS = {"clara-" + k: (V2, k) for k in V2["P"]} | {"fora-" + k: (FORA, k) for k in FORA["P"]}
PECAS = [(n, *TODAS[n]) for n in GRADE]


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        ac = Image.open(BR["ACAB"]).convert("RGBA").resize((1080, 1440))
        for novo, ns, chave in PECAS:
            if so and not any(novo.startswith(s) for s in so):
                continue
            item = ns["P"][chave]
            css, corpo = item[0], item[1]
            classe = item[2] if len(item) > 2 else ""
            css = css() if callable(css) else css
            corpo = corpo.replace(f'stroke="{OURO}"', 'stroke="url(#fo)"').replace("<polyline", f"<defs>{DEF_FIO}</defs><polyline")
            html = ns["BASE"].replace("CSS</style>", css + ACABAMENTO + "</style>").replace("CORPO", corpo).replace("CLASSE", classe)
            await pg.set_content(html, wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(SAIDA / f"{novo}.jpg", quality=86)
            print(novo)
        await b.close()
    if not so:
        grade = Image.new("RGB", (3 * 360 + 8, 3 * 480 + 8), "white")
        for i, n in enumerate(GRADE):
            grade.paste(Image.open(SAIDA / f"{n}.jpg").resize((360, 480), Image.LANCZOS), ((i % 3) * 364, (i // 3) * 484))
        grade.save(AQUI / "grade.jpg", quality=86)


asyncio.run(main())
