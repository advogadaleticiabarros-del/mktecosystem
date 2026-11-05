"""Palavra de Ouro: peças do estilo. Uso: python gerar.py [prefixo]. Regras em docs/ESTILO_PALAVRA_DE_OURO.md.
Grava em pecas/ (fora do git). Nunca sobrescreva peça pronta: peça nova = nome novo."""
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

from base import ACAB, ASS, BASE, FOIL, cab

AQUI = Path(__file__).resolve().parent
BANCO = Path(__file__).resolve().parents[3] / "apps" / "api" / "_saida_producao_1510" / "_fotos_pexels"
SAIDA = AQUI / "pecas"
PB = "filter:grayscale(1) sepia(.14) contrast(1.06)"


def foto(nome, largura=1300):
    f = Image.open(BANCO / nome).convert("RGB")
    f.thumbnail((largura, largura * 2), Image.LANCZOS)
    b = io.BytesIO()
    f.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def faixa(nome, chapeu, direita, palavra, frase, corpo, pos="50% 50%", tamanho="cover"):
    """Modelo C: palavra, faixa de cinema entre fios de ouro, frase."""
    return ("", f"""{cab(chapeu, direita)}
<div class="abs g f ajusta" style="left:92px;top:150px;font-size:226px;line-height:1;width:max-content;letter-spacing:.005em;white-space:nowrap">{palavra}</div>
<div class=abs style="left:0;right:0;top:396px"><div class=ox1></div><div class=ox2></div></div>
<div class=abs style="left:0;right:0;top:412px;height:470px;background:#111 url({foto(nome)}) {pos}/{tamanho} no-repeat;{PB}"></div>
<div class=abs style="left:0;right:0;top:884px"><div class=ox2></div><div class=ox1 style="margin-top:4px"></div></div>
<div class="abs g" style="left:92px;top:936px;font-size:136px;line-height:1.02;white-space:nowrap">{frase}</div>
<div class="abs corpo" style="left:96px;width:800px;top:1112px">{corpo}</div>
{ASS}""", "esc")


def rosto(nome, palavra, frase, corpo, topo=0, largura=1080, esq=0, luz=1):
    """Modelo B: foto grande em cima, palavra na base."""
    return ("", f"""<img class=abs src="{foto(nome)}" style="left:{esq}px;top:{topo}px;width:{largura}px;{PB} brightness({luz})">
<div class=abs style="left:0;right:0;top:790px;bottom:0;background:linear-gradient(transparent,#231E1A 30%)"></div>
<div class="abs g f ajusta" style="left:92px;top:950px;font-size:226px;line-height:1;width:max-content;letter-spacing:.005em;white-space:nowrap">{palavra}</div>
<div class="abs g" style="left:92px;top:1192px;font-size:74px;line-height:1.08;white-space:nowrap">{frase}</div>
<div class=abs style="left:96px;right:96px;top:1280px;font:500 24px/1.45 Inter">{corpo}<br>Letícia Barros · OAB/ES 39.948</div>""", "esc")


P = {
    "01-hora-extra": faixa("35070219.jpg", "Jornada", "CF, art. 7º, XVI", "HORA EXTRA", "se <i>paga.</i>", "Com adicional de, no mínimo, 50% sobre a hora normal.", "50% 50%"),
    "02-salario": rosto("8719576.jpg", "SALÁRIO", "tem <i>data.</i>", "Até o 5º dia útil do mês seguinte. CLT, art. 459, § 1º.", topo=-60),
    "03-assinar": faixa("16282318.jpg", "Antes de assinar", "Letícia Barros · OAB/ES 39.948", "ASSINAR", "sem ler, <i>não.</i>", "Leia tudo antes de assinar acordo, rescisão ou pedido de demissão.", "50% 40%"),
    "04-gravida": ("", f"""<div class=abs style="left:440px;top:500px;width:640px;height:920px;-webkit-mask-image:linear-gradient(transparent,#000 14%);mask-image:linear-gradient(transparent,#000 14%)"><img src="{foto('3863209.jpg')}" style="width:640px;display:block;{PB};-webkit-mask-image:linear-gradient(90deg,transparent,#000 18%);mask-image:linear-gradient(90deg,transparent,#000 18%)"></div>
<div class="abs g f" style="left:84px;top:1352px;width:max-content;font-size:270px;line-height:1;white-space:nowrap;transform-origin:0 0;transform:rotate(-90deg);letter-spacing:.015em;padding-top:.24em">GRÁVIDA</div>
<div class=abs style="left:470px;right:96px;top:96px">
<div style="font:600 24px Inter;letter-spacing:.12em">GESTANTE</div><div style="font:500 24px Inter;margin-top:8px">Letícia Barros · OAB/ES 39.948</div>
<div class=g style="font-size:96px;line-height:1.04;margin-top:26px">não é <i>motivo.</i></div>
<div class=corpo style="font-size:30px;margin-top:20px">A gravidez não é justo motivo para a rescisão do contrato. CLT, art. 391.</div></div>
""", "esc"),
    "05-antes": rosto("4672015.jpg", "ANTES", "de <i>nascer.</i>", "A pensão pode ser pedida durante a gestação. Lei 11.804/2008.", topo=-120),
    "06-burnout": rosto("original-burnout-trabalho.jpg", "BURNOUT", "tem <i>nome.</i>", "Está na CID-11, como fenômeno ligado ao trabalho.", topo=-520, luz=1.2),
}
def foto_grito(nome, caixa=None):
    f = Image.open(AQUI / "fotos" / f"{nome}.jpg").convert("L").convert("RGB")
    if caixa:
        f = f.crop(caixa)
    b = io.BytesIO()
    f.save(b, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


VERTICAL = f'<div class="abs g f" style="left:84px;top:1352px;width:max-content;font-size:318px;line-height:1;white-space:nowrap;transform-origin:0 0;transform:rotate(-90deg);letter-spacing:.015em">GRITAR</div>'
GRITO = {}
# A. A composição dela: ele grita em direção à palavra. Luz de cinema, sem véu.
GRITO["A-perfil"] = ("", f"""<img class=abs src="{foto_grito('10675499')}" style="left:250px;top:250px;width:860px;mix-blend-mode:screen;filter:sepia(.14) contrast(1.05);-webkit-mask-image:radial-gradient(ellipse 60% 56% at 60% 50%,#000 72%,transparent 100%);mask-image:radial-gradient(ellipse 60% 56% at 60% 50%,#000 72%,transparent 100%)">
{VERTICAL}
<div class=abs style="left:440px;right:96px;top:96px">
<div style="display:flex;justify-content:space-between;font:500 24px Inter"><span style="font-weight:600;letter-spacing:.12em">ASSÉDIO MORAL</span></div>
<div class=g style="font-size:112px;line-height:1.02;margin-top:28px">não é <i>cobrar.</i></div>
<div class=corpo style="font-size:32px;margin-top:22px">Humilhação repetida no trabalho pode ser assédio moral.</div></div>
<div class="abs peq" style="right:96px;bottom:96px;text-align:right">Letícia Barros<br>OAB/ES 39.948</div>""", "esc")

# B. Rosto inteiro: o close ocupa a peça e a palavra entra na base.
GRITO["B-close"] = ("", f"""<img class=abs src="{foto_grito('5089721')}" style="left:0;top:-176px;width:1080px;filter:sepia(.14) contrast(1.04)">
<div class=abs style="left:0;right:0;top:790px;bottom:0;background:linear-gradient(transparent,#231E1A 30%)"></div>
<div class="abs g f" style="left:90px;top:950px;font-size:226px;line-height:1;width:max-content;letter-spacing:.005em">GRITAR</div>
<div class="abs g" style="left:92px;top:1192px;font-size:74px;line-height:1.1">não é <i>cobrar.</i></div>
<div class=abs style="left:96px;right:96px;top:1280px;font:500 24px/1.45 Inter">Humilhação repetida pode ser assédio moral.<br>Letícia Barros · OAB/ES 39.948</div>""", "esc")

# C. Só a boca: faixa de cinema entre dois fios de ouro; a pessoa fica menos identificável.
GRITO["C-boca"] = ("", f"""{cab('Assédio moral')}
<div class="abs g f" style="left:90px;top:150px;font-size:226px;line-height:1;width:max-content;letter-spacing:.005em">GRITAR</div>
<div class=abs style="left:0;right:0;top:396px"><div class=ox1></div><div class=ox2></div></div>
<div class=abs style="left:0;right:0;top:412px;height:470px;overflow:hidden;background:#111"><img src="{foto_grito('5089721', (40, 930, 1240, 1452))}" style="width:1080px;display:block;filter:sepia(.14) contrast(1.04)"></div>
<div class=abs style="left:0;right:0;top:884px"><div class=ox2></div><div class=ox1 style="margin-top:4px"></div></div>
<div class="abs g" style="left:92px;top:936px;font-size:148px;line-height:1.02">não é <i>cobrar.</i></div>
<div class="abs corpo" style="left:96px;width:720px;top:1120px">Humilhação repetida no trabalho pode ser assédio moral.</div>
{ASS}""", "esc")


P.update({"grito-" + k: v for k, v in GRITO.items()})
AJUSTA = """()=>{document.querySelectorAll('.ajusta').forEach(e=>{const s=parseFloat(getComputedStyle(e).fontSize),w=e.getBoundingClientRect().width;e.style.fontSize=Math.min(s,s*892/w)+'px'});return 1}"""


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
        for nome, (css, corpo, classe) in P.items():
            if so and not any(nome.startswith(s) for s in so):
                continue
            await pg.set_content(BASE.replace("CSS</style>", css + "</style>").replace("CORPO", corpo).replace("CLASSE", classe), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            await pg.evaluate(AJUSTA)
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(SAIDA / f"{nome}.jpg", quality=89)
            print(nome)
        await b.close()


asyncio.run(main())
