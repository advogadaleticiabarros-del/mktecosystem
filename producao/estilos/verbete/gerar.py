"""Verbete: peça em forma de definição de dicionário. Uso: python gerar.py. Regras em docs/ESTILO_VERBETE.md.
Grava em pecas/ (fora do git). Nunca sobrescreva peça pronta: peça nova = nome novo."""
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "palavra-de-ouro"))
from base import ACAB, ASS, BASE, cab  # noqa: E402

RET = Path(__file__).resolve().parents[3] / "apps" / "api" / "_saida_producao_1510" / "_retratos"
SAIDA = AQUI / "pecas"
FIO = "linear-gradient(90deg,#9a7026 0%,#c9a14e 18%,#e2c77c 32%,#b98f3c 48%,#9a7026 62%,#d8b768 78%,#ecd591 88%,#a67c2e 100%)"
CSS = f".ox1,.ox2{{background:{FIO}}}"


def foto(nome, caixa, largura=560):
    """Só recorta e redimensiona: o rosto da Dra. não recebe filtro."""
    f = Image.open(RET / nome).convert("RGB").crop(caixa)
    f = f.resize((largura, round(f.height * largura / f.width)), Image.LANCZOS)
    b = io.BytesIO()
    f.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def verbete(letra, termo, silabas, definicao, detalhe, exemplo, imagem, legenda, chapeu="Dicionário"):
    return f"""{cab(chapeu, letra)}
<div class="abs g" style="left:96px;top:176px;font-size:128px;line-height:1">{termo}</div>
<div class="abs g" style="left:96px;top:318px;font-size:42px;line-height:1.2;letter-spacing:0"><i>{silabas}</i></div>
<div class=abs style="left:96px;right:96px;top:396px;height:2px;background:{FIO}"></div>
<div class=abs style="left:96px;width:500px;top:444px">
<div class=g style="font-size:80px;line-height:1.08"><span style="font-size:36px;vertical-align:.5em;margin-right:8px">1.</span>{definicao}</div>
<div class=corpo style="margin-top:56px;font-size:32px"><b style="font-weight:600">2.</b> {detalhe}</div>
<div class=g style="margin-top:56px;font-size:42px;line-height:1.2;letter-spacing:0"><i>Ex.: “{exemplo}”</i></div></div>
<div class=abs style="left:640px;right:96px;top:452px"><img src="{imagem}" style="width:344px;display:block"><div class=peq style="margin-top:14px">{legenda}</div></div>
{ASS}"""


P = {
    "01-leticia-barros": verbete(
        "L", "Letícia Barros", "le.tí.ci.a bar.ros · substantivo próprio, feminino",
        "A advogada da mulher que trabalha.",
        "Atua em direito do trabalho, direito das gestantes e das famílias.",
        "Foi a Letícia Barros que explicou o art. 391.",
        foto("estudio-claro-cadeira.jpg", (250, 240, 850, 1140)), "Fig. 1. Em atividade."),
}


async def main():
    SAIDA.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
        for nome, corpo in P.items():
            await pg.set_content(BASE.replace("CSS</style>", CSS + "</style>").replace("CORPO", corpo).replace("CLASSE", ""), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(SAIDA / f"{nome}.jpg", quality=90)
            print(nome)
        await b.close()


asyncio.run(main())
