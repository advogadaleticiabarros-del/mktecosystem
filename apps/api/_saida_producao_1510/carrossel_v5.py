"""Carrossel editorial v5 (capa com foto do tema e fechamento com retrato inteiro desde 09/10/2026, sem recorte da Letícia): o padrão aprovado do v4 (fosco, papel, Cormorant, recortes
e arco contínuos, faixas douradas) aplicado a todos os temas, com as melhorias da
análise de 09/10/2026: títulos-gancho (slide 2 = segunda capa), números em bronze nos
slides claros (contraste), selo "Salve para conferir" no checklist, lei na capa e o
logotipo dourado como marca d'água no slide escuro do meio.

Uso (de apps/api): python _saida_producao_1510/carrossel_v5.py [chave ...]
"""
import asyncio
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

import capa_fecho  # noqa: E402
import carrossel_v4 as v4  # noqa: E402
from app.services import render_criativo  # noqa: E402
import os  # noqa: E402

if os.environ.get("DADOS") in ("nov", "dez"):  # planos mensais (conteudo_nov.py, conteudo_dez.py)
    import importlib  # noqa: E402
    _MES = importlib.import_module("conteudo_" + os.environ["DADOS"])
    CARROSSEIS = {t["chave"]: t["carrossel"] for t in _MES.TEMAS}
    # cada mês continua o rodízio de onde o anterior parou, sem repetir retrato dentro do mês
    _INICIO = {"nov": 11, "dez": 4}[os.environ["DADOS"]]
    RODIZIO = capa_fecho.ORDEM_RETRATOS[_INICIO:] + capa_fecho.ORDEM_RETRATOS[:_INICIO] + ["estudio-livros"]
else:
    from carrosseis_v5_dados import CARROSSEIS  # noqa: E402
    RODIZIO = None

AQUI = Path(__file__).resolve().parent
PEXELS = json.loads((AQUI / "pexels_candidatas.json").read_text(encoding="utf-8"))
CSS = re.search(r"<style>(.*?)</style>", v4.HTML.source if hasattr(v4.HTML, "source") else open(AQUI / "carrossel_v4.py", encoding="utf-8").read(), re.S).group(1)

EXTRA = """
.claro .num { color:#8F7032 !important; }
.marca-logo { position:absolute; z-index:1; opacity:.09; filter:grayscale(.2); }
.guarde { position:absolute; right:84px; top:150px; z-index:6; display:flex; align-items:center; gap:12px; background:#231E1A; color:#E8DED1;
  font-size:23px; font-weight:700; letter-spacing:2px; text-transform:uppercase; padding:12px 20px; border-radius:6px; }
.guarde i { display:inline-block; width:18px; height:24px; background:#C9A962; clip-path:polygon(0 0,100% 0,100% 100%,50% 75%,0 100%); }
.lei { display:inline-block; margin-top:28px; font-size:22px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#231E1A; background:#C9A962; padding:9px 16px; border-radius:4px; }
.check { margin-top:26px; font-size:32px; line-height:1.75; color:#231E1A; }
.check span { display:inline-block; width:26px; height:26px; border:2.5px solid #8F7032; border-radius:4px; margin-right:16px; vertical-align:-3px; }
.obj img, img.obj { max-width:760px; max-height:470px; object-fit:contain; }
/* Objeto em arco (desde 10/10/2026): foto real do objeto do tema, ou recorte aprovado, dentro de um arco dourado. */
.arco-obj { position:absolute; width:380px; height:470px; border-radius:190px 190px 14px 14px; overflow:hidden; z-index:3;
  border:3px solid #C9A962; box-shadow:0 26px 52px rgba(35,30,26,.30); background:radial-gradient(circle at 50% 40%, #F7F0E4, #E6D9C4); }
.arco-obj img { width:100%; height:100%; object-fit:cover; filter:sepia(.12) saturate(.92) contrast(1.03); }
.sangra-obj { position:absolute; width:1080px; height:560px; top:790px; z-index:2; overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg, transparent 0%, #000 42%); mask-image:linear-gradient(180deg, transparent 0%, #000 42%); }
.sangra-obj img { width:100%; height:100%; object-fit:cover; filter:sepia(.14) saturate(.9) contrast(1.02); }
.ponte-obj { position:absolute; height:430px; top:830px; z-index:2; overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg, transparent 0%, #000 34%, #000 86%, transparent 100%), linear-gradient(90deg, transparent 0%, #000 12%, #000 88%, transparent 100%);
  -webkit-mask-composite:source-in; mask-image:linear-gradient(180deg, transparent 0%, #000 34%, #000 86%, transparent 100%), linear-gradient(90deg, transparent 0%, #000 12%, #000 88%, transparent 100%); mask-composite:intersect; }
.ponte-obj img { width:100%; height:100%; object-fit:cover; filter:sepia(.14) saturate(.9) contrast(1.02); }
.arco-obj.recorte img { object-fit:contain; padding:46px 34px; filter:drop-shadow(0 14px 18px rgba(35,30,26,.28)); }
"""

PAGINAS = Template(r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{{ css }}{{ extra }}{{ css_capa }}</style></head><body><div class="pano">

{{ capa_html }}

{% for i in range(4) %}{% set it = d.itens[i] %}{% set esc = (i == 1) %}
{% if i < 3 %}
<div class="s {{ 'escuro' if esc else 'claro' }} textura" style="left:{{ (i + 1) * 1080 }}px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>{{ d.area }}</span></div>
  {% if esc %}<img class="marca-logo" src="{{ logo }}" style="right:-300px; top:330px; width:980px;">{% else %}<div class="marca" style="right:20px; top:150px; font-size:560px;">0{{ i + 1 }}</div>{% endif %}
  <div class="bloco" style="top:300px;">
    <div class="num">0{{ i + 1 }}</div>
    <div class="tit">{{ it[0] }}</div>
    <div class="txt">{{ it[1] }}</div>
    {% if it[2] %}<div class="selo">{{ it[2] }}</div>{% endif %}
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">0{{ i + 2 }} / 07</span></div>
</div>
{% else %}
<div class="s foto" style="left:4320px">
  <img src="{{ foto5 }}" style="position:absolute; inset:0; width:1080px; height:1350px;">
  <div style="position:absolute; inset:0; background:linear-gradient(180deg, rgba(35,30,26,.55), rgba(35,30,26,.35) 40%, rgba(35,30,26,.75));"></div>
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>{{ d.area }}</span></div>
  <div class="papel" style="left:120px; top:360px; width:760px; transform:rotate(-3deg);">
    <div class="num" style="color:#8F7032;">04</div>
    <div class="cg" style="font-size:72px; font-weight:600; line-height:1.04; margin-top:6px;">{{ it[0] | replace('<em>', '<em style="font-style:italic; border-bottom:4px solid #C9A962;">') }}</div>
    <div style="font-size:32px; line-height:1.45; margin-top:26px; color:#3D2B1F;">{{ it[1] }}</div>
    {% if it[2] %}<div class="selo" style="background:#231E1A; color:#E8DED1;">{{ it[2] }}</div>{% endif %}
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">05 / 07</span></div>
</div>
{% endif %}{% endfor %}

{% set it = d.itens[4] %}
<div class="s claro textura" style="left:5400px">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>{{ d.area }}</span></div>
  <div class="guarde"><i></i>Salve para conferir</div>
  <div class="marca" style="right:20px; top:250px; font-size:560px;">05</div>
  <div class="bloco" style="top:290px;">
    <div class="num">05</div>
    <div class="tit">{{ it[0] }}</div>
    <div class="txt" style="max-width:700px;">{{ it[1] }}</div>
    <div class="check">{% for c in d.checklist %}<span></span>{{ c }}<br>{% endfor %}</div>
    {% if it[2] %}<div class="selo">{{ it[2] }}</div>{% endif %}
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">06 / 07</span></div>
</div>

{{ fecho_html }}

<div class="arco" style="left:1700px; top:860px; width:1150px; height:1150px;"></div>
<div class="arco" style="left:4950px; top:-620px; width:1000px; height:1000px;"></div>
{{ objetos_html }}
<div class="fosco grao"></div><div class="fosco veu"></div>
</div></body></html>""")


def retrato(nome: str) -> str:
    """Corpo inteiro vira plano americano (da cabeça ao meio da coxa), para a pessoa aparecer grande."""
    import base64
    im = Image.open(v4.REC / nome).convert("RGBA")
    w, h = im.size
    if h / w > 1.55:
        im = im.crop((0, 0, w, int(w * 1.45)))
        a = im.getchannel("A")
        # suaviza o corte inferior para não parecer recortado
        from PIL import ImageDraw
        grad = Image.new("L", im.size, 255); dr = ImageDraw.Draw(grad)
        for y in range(int(im.height * 0.86), im.height):
            dr.line([(0, y), (w, y)], fill=int(255 * (im.height - y) / (im.height * 0.14)))
        from PIL import ImageChops
        im.putalpha(ImageChops.multiply(a, grad))
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


POSICOES_LEGADO = [("1700px", "930px", -10), ("2880px", "900px", 10), ("3820px", "930px", -7)]
ARCO_LEFT = [1680, 2760, 3840]  # mesmo ponto em cada slide (x 600 do slide), longe do texto e da paginação


def objetos_html(objetos: list) -> str:
    """Recorte solto (padrão até nov/2026) ou objeto em arco: "foto:<id Pexels>" ou "arco:<recorte>.png"."""
    partes = []
    for i, o in enumerate(objetos):
        if isinstance(o, str) and o.startswith("foto:"):
            partes.append(f'<div class="arco-obj" style="left:{ARCO_LEFT[i]}px; top:740px;"><img src="{v4.foto(v4.FOTOS / (o[5:] + '.jpg'), w=760, h=940, foco=0.45)}"></div>')
        elif isinstance(o, str) and o.startswith("sangra:"):
            # foto do objeto ocupando a base do slide, sem moldura, dissolvendo no papel
            partes.append(f'<div class="sangra-obj" style="left:{ARCO_LEFT[i] - 600}px;"><img src="{v4.foto(v4.FOTOS / (o[7:] + '.jpg'), w=2160, h=1120, foco=0.5)}"></div>')
        elif isinstance(o, str) and o.startswith("ponte:"):
            # foto que atravessa a divisão entre este slide e o próximo (continua quando a pessoa arrasta)
            esquerda = 1080 * (i + 1) + 380  # começa no slide do item e termina antes do fim do slide seguinte
            partes.append(f'<div class="ponte-obj" style="left:{esquerda}px; width:1400px;"><img src="{v4.foto(v4.FOTOS / (o[6:] + '.jpg'), w=2800, h=860, foco=0.42)}"></div>')
        elif o in (None, "", "nenhum"):
            continue
        elif isinstance(o, str) and o.startswith("arco:"):
            partes.append(f'<div class="arco-obj recorte" style="left:{ARCO_LEFT[i]}px; top:740px;"><img src="{v4.png(o[5:])}"></div>')
        else:
            left, top, rot = POSICOES_LEGADO[i]
            partes.append(f'<img class="obj" src="{v4.png(o)}" style="left:{left}; top:{top}; transform:rotate({rot}deg);">')
    return "\n".join(partes)


# Fotos de capa sem rosto frontal detectável: ponto de foco manual (fração da foto).
FOCO_CAPA = {"violencia-domestica-inss": (0.42, 0.30), "mesario-folga": (0.48, 0.32), "separacao-bens-70": (0.5, 0.45),
             "amamentacao-trabalho": (0.42, 0.22), "pensao-13": (0.6, 0.3),
             "licenca-paternidade-2027": (0.42, 0.62)}


async def renderizar(chave: str, page) -> None:
    d = CARROSSEIS[chave]
    if isinstance(d["foto5"], int):  # id Pexels direto (novembro em diante)
        foto5 = v4.FOTOS / f"{d['foto5']}.jpg"
    else:
        tema_px, n = d["foto5"]
        foto5 = v4.FOTOS / f"{PEXELS[tema_px][n]['id']}.jpg"
    ordem = list(CARROSSEIS).index(chave)
    capa_html = capa_fecho.capa_ouro(
        capa_fecho.enquadrar(AQUI / "_fotos_pexels" / f"original-{chave}.jpg", foco=FOCO_CAPA.get(chave)), area=d["tag"],
        kicker=d["capa"][0], titulo=d["capa"][1], subtitulo=d["capa"][2],
        apoio=f'{d["capa"][3]}<span class="co-lei">{d["capa"][4]}</span>', total="07")
    fecho_html = capa_fecho.fecho(
        RODIZIO[ordem] if RODIZIO else ordem + 1, area=d["tag"], titulo=d["fecho"][0], sub=d["fecho"][1],
        apoio=f'<span class="mt">Salve este post</span> e {d["fecho"][2]}', left=6480)
    html = PAGINAS.render(
        css=CSS, extra=EXTRA, d=d, logo=render_criativo._logo_data_uri(),
        grao=v4.GRAO, mancha=v4.MANCHA, fibra=v4.FIBRA, ruido=v4.RUIDO,
        capa_html=capa_html, fecho_html=fecho_html, css_capa=capa_fecho.CSS + capa_fecho.CSS_OURO, foto5=v4.foto(foto5, foco=0.25),
        objetos_html=objetos_html(d["objetos"]),
    )
    # o CSS do v4 usa variáveis do Jinja ({{ grao }} etc.): renderiza de novo para resolvê-las
    html = Template(html).render(grao=v4.GRAO, mancha=v4.MANCHA, fibra=v4.FIBRA, ruido=v4.RUIDO)
    await page.set_content(html, wait_until="networkidle")
    await page.evaluate("document.fonts.ready")
    await page.evaluate("""() => { const el=document.getElementById('big'); let fs=150; el.style.fontSize=fs+'px';
        while (el.offsetWidth > 620 && fs > 70) { fs -= 4; el.style.fontSize = fs + 'px'; } }""")
    pano = Image.open(io.BytesIO(await page.screenshot(type="png"))).convert("RGB")
    for i in range(7):
        destino = AQUI / "pecas" / f"{chave}-v5-{i + 1}.png"
        pano.crop((i * 2160, 0, (i + 1) * 2160, 2700)).resize((1080, 1350), Image.LANCZOS).save(destino)
        render_criativo._aplicar_acabamento_dourado(str(destino))
        Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
        destino.unlink()
    print("ok", chave)


async def main(filtro: set[str]) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 7560, "height": 1350}, device_scale_factor=2)
        for chave in CARROSSEIS:
            if not filtro or chave in filtro:
                await renderizar(chave, page)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
