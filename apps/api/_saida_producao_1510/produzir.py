"""Renderiza as artes da produção 15/10 a 02/11/2026 e gera plano.json + folha de conferência.

Uso (de apps/api): python _saida_producao_1510/produzir.py [chave-do-tema ...]
"""
import asyncio
import base64
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from jinja2 import Template  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo  # noqa: E402
from conteudo import MITO_OU_LEI, TEMAS  # noqa: E402

AQUI = Path(__file__).resolve().parent
PNG = AQUI / "_png"
SAIDA = AQUI / "pecas"
BANCO = json.loads((AQUI / "indice_fotos.json").read_text())
IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
FUNDO_CREME = Path("C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/ementos rdape dourado/use esse fundo.png")
ESPECIALIDADE = {
    "Trabalhista": "Advogada | Letícia Barros | Direito Trabalhista",
    "Família": "Advogada | Letícia Barros | Direito de Família",
    "Previdenciário": "Advogada | Letícia Barros | Direito Previdenciário",
    "Consumidor": "Advogada | Letícia Barros | Direito do Consumidor",
}


def uri(caminho: Path) -> str:
    mime = "image/png" if caminho.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(caminho.read_bytes()).decode()}"


LOGO = render_criativo._logo_data_uri()

BASE_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,700&display=swap" rel="stylesheet">
<style>
:root { --d:#C9A962; --f:#231E1A; --a:#E8DED1; --b:#FAF6F0; }
* { margin:0; padding:0; box-sizing:border-box; }
.slide { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; color:var(--a);
  background: radial-gradient(circle at 82% 10%, #C9A96233, transparent 45%), radial-gradient(circle at 10% 95%, #C9A9621f, transparent 40%), var(--f); }
.slide::before { content:''; position:absolute; inset:36px; border:1.5px solid #C9A9628c; border-radius:18px; z-index:5; pointer-events:none; }
.bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; filter:sepia(.3) saturate(1.15) brightness(.85); }
.ov { position:absolute; inset:0; z-index:1; background:linear-gradient(180deg,#231E1A59 0%,#231E1AA6 45%,#231E1AF2 85%); }
.top { position:absolute; top:76px; left:88px; right:88px; z-index:4; display:flex; align-items:center; justify-content:space-between; }
.brand { display:flex; align-items:center; gap:16px; }
.brand img { width:60px; height:60px; object-fit:contain; }
.nm { font-family:'Playfair Display',serif; font-size:28px; font-weight:700; color:var(--b); }
.sb { font-size:18px; letter-spacing:4px; text-transform:uppercase; color:var(--d); margin-top:2px; font-weight:600; }
.pg { font-size:24px; font-weight:700; color:var(--d); letter-spacing:2px; }
.pg span { color:#E8DED199; }
.foot { position:absolute; left:88px; right:88px; bottom:84px; z-index:4; display:flex; align-items:center; justify-content:space-between; }
.swipe { font-size:24px; font-weight:600; color:#C9A962e6; }
.handle { font-size:22px; color:#E8DED1b3; font-weight:600; text-align:right; }
.handle b { display:block; font-size:22px; color:var(--d); margin-top:2px; font-weight:600; }
em { font-style:italic; color:var(--d); }
</style>"""

TOPO = """<div class="top"><div class="brand"><img src="{{ logo }}"><div><div class="nm">Letícia Barros</div><div class="sb">Advocacia</div></div></div>
<div class="pg">{{ '%02d' % (i+1) }} <span>/ {{ '%02d' % total }}</span></div></div>"""

CARROSSEL = Template("""<!doctype html><html><head><meta charset="utf-8">""" + BASE_CSS + """
<style>
.capa { position:absolute; left:88px; right:88px; bottom:190px; z-index:3; }
.kicker { font-size:26px; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:var(--d); margin-bottom:28px; }
.h { font-family:'Playfair Display',serif; font-weight:700; color:var(--b); line-height:1.12; font-size:{{ fs }}px; }
.item { position:absolute; left:88px; right:88px; top:250px; bottom:190px; z-index:3; display:flex; flex-direction:column; justify-content:center; }
.num { font-family:'Playfair Display',serif; font-size:150px; font-weight:800; color:var(--d); line-height:1; margin-bottom:30px; }
.t { font-family:'Playfair Display',serif; font-size:62px; font-weight:700; color:var(--b); line-height:1.15; margin-bottom:34px; }
.c { font-size:36px; line-height:1.45; color:var(--a); font-weight:400; }
.c .ref { display:block; margin-top:26px; font-size:26px; color:#C9A962; font-weight:600; letter-spacing:.3px; }
.final { position:absolute; left:88px; right:88px; bottom:300px; z-index:3; }
.save { font-size:28px; font-weight:600; color:var(--d); margin-top:34px; }
.cta { position:absolute; left:88px; bottom:76px; z-index:4; background:var(--d); color:var(--f); font-size:28px; font-weight:800; padding:22px 40px; border-radius:999px; }
</style></head><body><div class="slide">
{% if foto %}<img class="bg" src="{{ foto }}" style="object-position:{{ pos }}"><div class="ov"></div>{% endif %}
""" + TOPO + """
{% if modo == 'capa' %}
  <div class="capa"><div class="kicker">{{ kicker }}</div><div class="h">{{ texto }}</div></div>
  <div class="foot"><span class="swipe">Arraste pro lado ›</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
{% elif modo == 'item' %}
  <div class="item"><div class="num">{{ '%02d' % i }}</div><div class="t">{{ titulo }}</div><div class="c">{{ corpo }}{% if ref %}<span class="ref">{{ ref }}</span>{% endif %}</div></div>
  <div class="foot"><span class="swipe">Arraste pro lado ›</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
{% else %}
  <div class="final"><div class="h">{{ texto }}</div><div class="save">Salve este post e mande para quem precisa.</div></div>
  <div class="cta">⚖️ Procure uma advogada</div>
  <div class="foot" style="justify-content:flex-end"><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
{% endif %}
</div></body></html>""")

MITO = Template("""<!doctype html><html><head><meta charset="utf-8">""" + BASE_CSS + """
<style>
.wrap { position:absolute; left:96px; right:96px; top:230px; bottom:200px; z-index:3; display:flex; flex-direction:column; justify-content:center; }
.k { font-size:28px; font-weight:800; letter-spacing:6px; color:var(--d); margin-bottom:40px; }
.af { font-family:'Playfair Display',serif; font-size:{{ fs }}px; font-weight:700; color:var(--b); line-height:1.18; }
.selo { align-self:flex-start; margin:56px 0 48px; padding:14px 46px; border:6px solid {{ cor }}; border-radius:16px; color:{{ cor }};
  font-weight:900; font-size:104px; letter-spacing:10px; transform:rotate(-6deg); line-height:1; }
.ex { font-size:36px; line-height:1.45; color:var(--a); }
.ref { margin-top:26px; font-size:24px; color:#C9A962; font-weight:600; }
.foot2 { position:absolute; left:96px; right:96px; bottom:84px; z-index:4; display:flex; justify-content:space-between; align-items:center; }
.serie { font-size:22px; font-weight:700; letter-spacing:3px; color:#E8DED199; text-transform:uppercase; }
</style></head><body><div class="slide">
<div class="top"><div class="brand"><img src="{{ logo }}"><div><div class="nm">Letícia Barros</div><div class="sb">Advocacia</div></div></div></div>
<div class="wrap"><div class="k">MITO OU LEI?</div><div class="af">“{{ afirmacao }}”</div><div class="selo">{{ veredito }}</div>
<div class="ex">{{ explicacao }}</div><div class="ref">{{ ref }}</div></div>
<div class="foot2"><span class="serie">Série Mito ou Lei</span><span class="handle">@adv.leticiabarros2<b>OAB/ES 39.948</b></span></div>
</div></body></html>""")


def pergunta_template() -> Template:
    src = (AQUI.parent / "_saida_programacao_0810" / "_gerar_pergunta_clt.py").read_text(encoding="utf-8")
    html = re.search(r'TEMPLATE_HTML = """(.*?)"""', src, re.S).group(1)
    # Sem selo de verificado (o perfil não é verificado) e avatar = logo, nunca imagem de IA da advogada.
    html = html.replace(' <span class="verificado">&#10003;</span>', "")
    return Template(html)


PERGUNTA = pergunta_template()


async def foto(page, html: str, destino: Path) -> None:
    await page.set_content(html, wait_until="networkidle")
    await page.evaluate("document.fonts.ready")
    await page.screenshot(path=str(destino))
    render_criativo._aplicar_acabamento_dourado(str(destino))


def jpeg(png: Path, nome: str) -> str:
    Image.open(png).convert("RGB").save(SAIDA / nome, "JPEG", quality=92, optimize=True)
    return nome


def separar_ref(texto: str) -> tuple[str, str]:
    m = re.search(r"\s*\(([^()]*(?:Lei|CLT|STF|STJ|TST|CPC|Súmula|ADI|Tema|ANS|art\.|Código|TRF)[^()]*)\)\s*$", texto)
    return (texto[: m.start()], m.group(1)) if m else (texto, "")


async def main(filtro: set[str]) -> None:
    PNG.mkdir(exist_ok=True)
    SAIDA.mkdir(exist_ok=True)
    plano = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for tema in TEMAS:
            k = tema["chave"]
            if filtro and k not in filtro:
                continue
            c = tema["carrossel"]
            total = len(c["itens"]) + 2
            imagens = []
            for i in range(total):
                destino = PNG / f"{k}-car-{i + 1}.png"
                if i == 0:
                    f = c["foto_capa"]
                    html = CARROSSEL.render(modo="capa", i=i, total=total, logo=LOGO, kicker=tema["area"],
                                            texto=c["capa"], fs=84 if len(c["capa"]) < 70 else 74,
                                            foto=uri(Path(BANCO[f])) if f is not None else None, pos="center 30%")
                elif i == total - 1:
                    f = c["foto_final"]
                    html = CARROSSEL.render(modo="final", i=i, total=total, logo=LOGO, texto=c["final"], fs=66,
                                            foto=uri(Path(BANCO[f])) if f is not None else None, pos="center 30%")
                else:
                    titulo, corpo = c["itens"][i - 1]
                    corpo, ref = separar_ref(corpo)
                    html = CARROSSEL.render(modo="item", i=i, total=total, logo=LOGO, titulo=titulo, corpo=corpo, ref=ref)
                await foto(page, html, destino)
                imagens.append(jpeg(destino, f"{k}-car-{i + 1}.jpg"))

            q = tema["pergunta"]
            destino = PNG / f"{k}-pergunta.png"
            await foto(page, PERGUNTA.render(logo_src=LOGO, fundo_src=uri(FUNDO_CREME), avatar_src=LOGO,
                                             topo="Me faça uma pergunta:", pergunta=q["texto"],
                                             especialidade=ESPECIALIDADE[tema["area"]]), destino)
            img_pergunta = jpeg(destino, f"{k}-pergunta.jpg")

            destino = PNG / f"{k}-frase.png"
            await render_criativo.renderizar_frase_impacto(tema["frase"]["html"], IV, str(destino))
            img_frase = jpeg(destino, f"{k}-frase.jpg")

            dia = tema["data"]
            plano += [
                {"data": dia, "hora": "12:00", "tipo": "pergunta", "chave": k, "imagens": [img_pergunta],
                 "legenda": q["legenda"], "primeiro_comentario": q["primeiro_comentario"], "texto": q["texto"]},
                {"data": dia, "hora": "15:00", "tipo": "frase", "chave": k, "imagens": [img_frase],
                 "legenda": tema["frase"]["legenda"], "primeiro_comentario": tema["frase"]["primeiro_comentario"],
                 "texto": re.sub(r"</?em>", "", tema["frase"]["html"])},
                {"data": dia, "hora": "20:00", "tipo": "carrossel", "chave": k, "imagens": imagens,
                 "legenda": c["legenda"], "primeiro_comentario": c["primeiro_comentario"]},
            ]
            print("ok", k)

        for dia, k, af, ver, ex, ref, tags in MITO_OU_LEI:
            if filtro and k not in filtro:
                continue
            nome = f"mito-{dia}"
            destino = PNG / f"{nome}.png"
            cor = "#C9A962" if ver == "LEI" else "#E8DED1"
            await foto(page, MITO.render(logo=LOGO, afirmacao=af, veredito=ver, explicacao=ex, ref=ref, cor=cor,
                                         fs=68 if len(af) < 60 else 58), destino)
            legenda = (
                f"{'✅' if ver == 'LEI' else '❌'} {ver}! {af}\n\n{ex}\n\n"
                "Toda semana tem Mito ou Lei por aqui. Salva e manda pra quem vive repetindo esse mito."
                if ver == "MITO" else
                f"✅ {ver}! {af}\n\n{ex}\n\nToda semana tem Mito ou Lei por aqui. Salva e manda pra quem precisa saber."
            ) + "\n\nSe essa é a sua situação, procure uma advogada de confiança.\n\n" + tags
            plano.append({"data": dia, "hora": "19:00", "tipo": "estatico", "chave": k, "imagens": [jpeg(destino, f"{nome}.jpg")],
                          "legenda": legenda, "texto": af,
                          "primeiro_comentario": f"📚 Base legal: {ref}.\n💬 Você achava que era mito ou lei? Responde aqui antes de ler a legenda."})
            print("ok", nome)
        await browser.close()

    anterior = json.loads((AQUI / "plano.json").read_text(encoding="utf-8")) if (AQUI / "plano.json").exists() and filtro else []
    chaves = {(x["data"], x["hora"]) for x in plano}
    plano = sorted([x for x in anterior if (x["data"], x["hora"]) not in chaves] + plano, key=lambda x: (x["data"], x["hora"]))
    (AQUI / "plano.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(plano), "posts;", sum(len(x["imagens"]) for x in plano), "imagens")


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
