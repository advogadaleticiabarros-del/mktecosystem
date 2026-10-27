"""Stories v2 "Demissão pelo voto?" com fotos reais da urna eletrônica (27/10/2026).

Mesmo texto e ordem da v1 (`../carrossel-stories/stories.py`, que continua intacta). Muda: capa com a urna no alto e
fundo de urna escurecido nas telas 3, 5 e 7, com o crédito da foto. Telas 2 (enquete) e 8 (link) iguais à v1.

Uso (de apps/api): python ../../producao/campanhas/2026-10-assedio-eleitoral/urnas/stories_v2.py
Saída: apps/api/_saida_producao_1510/pecas/story-assedio-eleitoral-v2-1..8.jpg
"""
import asyncio
import sys
from pathlib import Path

AQUI_SCRIPT = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI_SCRIPT))
sys.path.insert(0, str(AQUI_SCRIPT.parent / "carrossel-stories"))

import stories as v1  # noqa: E402
import urnas  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

CREDITO_CSS = ("position:absolute; left:84px; right:84px; bottom:312px; z-index:20; font-size:22px; font-weight:500;"
               " color:rgba(232,222,209,.78); text-align:left;")


def tela_capa() -> str:
    foto = urnas.recorte("teclado", 1080, 1060, foco=(0.63, 0.45))
    return v1.pagina(f"""
<div class="tela">
  <img src="{foto}" style="position:absolute; left:0; top:0; width:1080px; height:1060px; z-index:1; filter:sepia(.16) saturate(.92) contrast(1.06) brightness(.9);">
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(180deg, rgba(20,15,12,.9) 0%, rgba(20,15,12,.82) 15%, rgba(20,15,12,.2) 24%, rgba(20,15,12,0) 30%, rgba(20,15,12,.15) 38%, rgba(20,15,12,.7) 46%, rgba(20,15,12,.97) 55%, #15110E 100%);"></div>
  <div style="position:absolute; inset:0; z-index:3; mix-blend-mode:screen; background:radial-gradient(ellipse at 92% 12%, rgba(255,214,140,.38), transparent 40%), radial-gradient(ellipse at 0% 88%, rgba(201,169,98,.22), transparent 45%);"></div>
  <div class="moldura" style="border-color:rgba(233,211,152,.55)"></div>{v1.cantos()}
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Assédio eleitoral</span></div>
  <div style="position:absolute; left:84px; right:84px; bottom:470px; z-index:20;">
    <div class="kick">Assédio eleitoral no trabalho</div>
    <div class="co-ouro" id="big" style="display:inline-block; font-family:'EB Garamond',serif; font-size:170px; font-weight:800; line-height:.92; margin-top:20px; white-space:nowrap;">Demissão<br>pelo voto?</div>
    <div style="font-family:'EB Garamond',serif; font-style:italic; font-size:60px; font-weight:500; color:#FAF6F0; margin-top:18px; line-height:1.08; text-wrap:balance;">Isso tem nome na lei. E a prova faz toda a diferença.</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:30px 0 22px;"></div>
    <div style="font-size:36px; line-height:1.45; color:#FAF6F0;">Veja o que a lei garante e como guardar as provas. <span class="co-lei" style="font-size:24px">Lei 9.029/1995</span></div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:330px; text-align:center; z-index:20; font-size:28px; font-weight:800; letter-spacing:4px; text-transform:uppercase; color:#E9D398;">Toque para ver o passo a passo ›</div>
  <div style="position:absolute; left:0; right:0; bottom:272px; text-align:center; z-index:20; font-size:22px; font-weight:500; color:rgba(232,222,209,.8);">{urnas.credito("teclado")}</div>
  <div class="co-grao"></div>
</div>""")


def com_urna(html: str, chave: str, foco: tuple[float, float] | None = None, veu: float = .72) -> str:
    """Põe a foto da urna, escurecida, por baixo do fundo café da tela tipográfica da v1, e o crédito."""
    foto = urnas.recorte(chave, 1080, 1920, foco=foco)
    camada = (f'<img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1920px; z-index:1;'
              f' filter:sepia(.25) saturate(.85) contrast(1.05) blur(1.5px);">'
              f'<div style="position:absolute; inset:0; z-index:1; background:linear-gradient(180deg, rgba(26,21,17,{veu}) 0%,'
              f' rgba(26,21,17,{veu + .08:.2f}) 50%, rgba(21,17,14,.93) 100%);"></div>'
              f'<div style="{CREDITO_CSS}">{urnas.credito(chave)}</div>')
    return html.replace('<div class="fundo"></div>', camada, 1)


TELAS = list(v1.TELAS)
TELAS[0] = tela_capa()
TELAS[2] = com_urna(v1.TELAS[2], "luz", foco=(0.40, 0.55))
TELAS[4] = com_urna(v1.TELAS[4], "confirma", foco=(0.74, 0.5))
TELAS[6] = com_urna(v1.TELAS[6], "ue2020", foco=(0.50, 0.55))


async def main() -> None:
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={"width": 1080, "height": 1920})
        for i, html in enumerate(TELAS, 1):
            await pg.set_content(html, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.evaluate("() => { const b = document.getElementById('big'); if (!b) return; let s = 170;"
                              " while (b.getBoundingClientRect().width > 900 && s > 90) { s -= 4; b.style.fontSize = s + 'px'; } }")
            await pg.wait_for_timeout(200)
            destino = v1.PECAS / f"story-assedio-eleitoral-v2-{i}.png"
            await pg.screenshot(path=str(destino))
            v1.rc._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=90)
            print("ok", destino.with_suffix(".jpg").name)
        await nav.close()


if __name__ == "__main__":
    asyncio.run(main())
