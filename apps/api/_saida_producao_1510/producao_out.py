"""Peças dos artigos de 15/10/2026 e homenagem ao Dia dos Professores.

- capa do blog (1200x630) e post do Perfil da Empresa (1200x900), como em dezembro;
- Story "Leia no link" (1080x1920) no padrão da capa Ouro editorial do carrossel v5 (capa_fecho.CSS_OURO):
  foto do tema em tela cheia, véu café, moldura com cantoneiras, título em ouro EB Garamond, subtítulo itálico,
  pílula da lei. Topo e base com 250 px livres (manual) e espaço para o adesivo de link acima da base;
- frase v2 (render oficial) da homenagem aos professores.
Uso (de apps/api): py _saida_producao_1510/producao_out.py
"""
import asyncio, base64, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from playwright.async_api import async_playwright
from app.services import render_criativo as rc
from app.services.render_criativo import renderizar_frase_impacto
from artigos_out import ARTIGOS, B
from posts_google import HTML, uri
import capa_fecho

AQUI = Path(__file__).resolve().parent
PECAS = AQUI / "pecas"
IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

# Texto do Story por artigo: (kicker, título em ouro, subtítulo itálico, apoio, pílula da lei, foco da foto)
STORY = {
    "fim-da-escala-6x1-o-que-muda-e-quando-comeca": ("Aprovado no Senado", "Fim da 6x1", "40 horas e duas folgas por semana",
        "O que muda, quando começa e o que fazer agora.", "PEC 221/2019", (0.45, 0.4)),
    "licenca-paternidade-10-dias-2027-lei-15371": ("Licença-paternidade", "10 dias", "a partir de janeiro de 2027",
        "Salário-paternidade e estabilidade para o pai.", "Lei 15.371/2026", None),
    "saude-no-trabalho-2026-lei-15377-nr-1": ("Outubro Rosa", "3 dias", "por ano para exame preventivo, sem desconto",
        "E agora a empresa é obrigada a avisar.", "Lei 15.377/2026", (0.62, 0.45)),
    "acao-trabalhista-na-cidade-onde-moro-tst-tema-215": ("Decisão do TST", "Na sua cidade", "a ação trabalhista pode correr onde você mora",
        "Em casos excepcionais. Veja quando.", "Tema 215", None),
    "pejotizacao-stf-tema-1389-o-que-fazer": ("Pejotização", "PJ ou CLT?", "o que o STF vai decidir",
        "E por que não vale esperar para agir.", "Tema 1.389", (0.3, 0.4)),
    "pensao-alimenticia-para-pais-idosos-filho-e-obrigado": ("Pensão alimentícia", "Pais idosos", "podem pedir pensão aos filhos",
        "Os pedidos crescem no Espírito Santo.", "CF, art. 229", None),
}

AREA = {"Direito Trabalhista": "Direito Trabalhista", "Direito de Família": "Direito de Família"}

PROFESSORES = ("professores-2026-frase-v2.jpg",
               "Toda advogada um dia foi aluna. <em>Obrigada, professores, por cada lição que virou caminho.</em>")


def capa_blog(a):
    im = Image.open(AQUI / "_fotos_pexels" / a["foto"]).convert("RGB")
    W, H = im.size
    h = int(W * 630 / 1200)
    y = max(0, min(H - h, int(a["cy"] * H - h / 2)))
    im.crop((0, y, W, y + h)).resize((1200, 630), Image.LANCZOS).save(
        PECAS / f"capa-{a['slug']}.jpg", "JPEG", quality=85, optimize=True, progressive=True)


def html_story(a: dict) -> str:
    kicker, big, sub, apoio, lei, foco = STORY[a["slug"]]
    foto = capa_fecho.enquadrar(AQUI / "_fotos_pexels" / a["foto"], alvo_x=0.5, alvo_y=0.27, w=1080, h=1920, escala=1, foco=foco)
    cantos = "".join(
        f'<div style="position:absolute; {p} width:60px; height:60px; border-{x}:3px solid #E9D398; border-{y}:3px solid #E9D398; z-index:13;"></div>'
        for p, x, y in [("top:200px; left:30px;", "top", "left"), ("top:200px; right:30px;", "top", "right"),
                        ("bottom:200px; left:30px;", "bottom", "left"), ("bottom:200px; right:30px;", "bottom", "right")])
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,700;0,800;1,500&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1920px;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
{capa_fecho.CSS_OURO}</style></head><body>
<div style="position:relative; width:1080px; height:1920px; background:#1A1511; overflow:hidden;">
  <img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; z-index:1; filter:sepia(.18) saturate(.9) contrast(1.08) brightness(.86);">
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(180deg, rgba(20,15,12,.85) 0%, rgba(20,15,12,.6) 14%, rgba(20,15,12,0) 26%, rgba(20,15,12,0) 38%, rgba(20,15,12,.85) 58%, rgba(20,15,12,.97) 100%);"></div>
  <div style="position:absolute; inset:0; z-index:3; mix-blend-mode:screen; background:radial-gradient(ellipse at 92% 12%, rgba(255,214,140,.42), transparent 40%), radial-gradient(ellipse at 0% 88%, rgba(201,169,98,.25), transparent 45%);"></div>
  <div style="position:absolute; top:208px; bottom:208px; left:38px; right:38px; border:1.5px solid rgba(233,211,152,.55); border-radius:6px; z-index:12;"></div>
  {cantos}
  <div style="position:absolute; top:262px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20; font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#F4EADB;">
    <span>Letícia Barros · Advocacia</span><span style="color:#E9D398">{AREA[a['categoria']]}</span></div>
  <div style="position:absolute; left:84px; right:84px; bottom:520px; z-index:20;">
    <div style="font-size:26px; font-weight:800; letter-spacing:5px; text-transform:uppercase; color:#E9D398;">{kicker}</div>
    <div class="co-ouro" id="big" style="display:inline-block; font-family:'EB Garamond',serif; font-size:170px; font-weight:800; line-height:.92; margin-top:18px; white-space:nowrap;">{big}</div>
    <div style="font-family:'EB Garamond',serif; font-style:italic; font-size:60px; font-weight:500; color:#FAF6F0; margin-top:16px; line-height:1.08; text-wrap:balance;">{sub}</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:30px 0 22px;"></div>
    <div style="font-size:34px; line-height:1.45; color:#FAF6F0; text-wrap:pretty;">{apoio} <span class="co-lei" style="font-size:24px">{lei}</span></div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:420px; text-align:center; z-index:20; font-size:30px; font-weight:800; letter-spacing:4px; text-transform:uppercase; color:#E9D398;">Leia o artigo no link &#8595;</div>
  <div class="co-brilho" style="right:150px; bottom:1060px;"></div><div class="co-brilho" style="right:210px; bottom:1150px; transform:scale(.6)"></div>
  <div class="co-grao"></div>
</div>
</body></html>"""


async def main():
    saida = []
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={"width": 1200, "height": 900})
        st = await nav.new_page(viewport={"width": 1080, "height": 1920})
        for a in ARTIGOS:
            capa_blog(a)
            await pg.set_content(HTML % {"foto": uri(AQUI / "_fotos_pexels" / a["foto"]), "pos": f"{int(a['cy'] * 100)}%",
                                         "kicker": a["kicker"], "titulo": a["titulo"]}, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            png = await pg.screenshot(type="jpeg", quality=86)
            (PECAS / f"google-post-{a['slug']}.jpg").write_bytes(png)
            saida.append({"data": a["data"], "slug": a["slug"], "titulo": a["titulo"], "texto": a["post_google"],
                          "link": f"{B}{a['slug']}.html", "imagem": "data:image/jpeg;base64," + base64.b64encode(png).decode()})
            await st.set_content(html_story(a), wait_until="networkidle")
            await st.evaluate("document.fonts.ready")
            await st.evaluate("() => { const b = document.getElementById('big'); let s = 170; while (b.getBoundingClientRect().width > 900 && s > 90) { s -= 4; b.style.fontSize = s + 'px'; } }")
            await st.wait_for_timeout(200)
            destino = PECAS / f"story-{a['slug']}.png"
            await st.screenshot(path=str(destino))
            rc._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=90)
            destino.unlink()
            print("ok", a["slug"])
        await nav.close()
    (PECAS / "posts_google_out.json").write_text(json.dumps(saida, ensure_ascii=False), encoding="utf-8")
    nome, html = PROFESSORES
    png = PECAS / nome.replace(".jpg", ".png")
    await renderizar_frase_impacto(html, IV, str(png))
    Image.open(png).convert("RGB").save(PECAS / nome, "JPEG", quality=92, optimize=True); png.unlink(); print("ok", nome)

asyncio.run(main())
