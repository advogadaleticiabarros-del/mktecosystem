"""Capas dos Reels Mito ou Lei (1080×1920), pedido da Jessica em 10/11/2026: "Siga nossa nova identidade. Acho que pode
ser um pouco mais clara para não escurecer tanto o nosso feed".

Papel claro com fibra, faixas douradas metálicas (como as capas Flagrante), "Mito ou Lei?" com Lei em ouro, a afirmação
do vídeo num cartão "Ouvi por aí" e os botões MITO / LEI sem revelar o veredito (a resposta fica para o vídeo).
Tudo o que importa fica no recorte da grade (y 240 a 1680).

Variações: papel (toda clara) e faixa (título numa faixa café em cima, cartão no papel).
Uso: python capas_mito.py [--papel|--faixa] [MM-DD ...]  → mito-lei/<MM-DD>-<slug>/capa-<variação>.jpg (arquivo novo)."""
import asyncio
import html
import sys
from pathlib import Path

from playwright.async_api import async_playwright

import mito_lei

sys.path.insert(0, r"C:\Users\prosy\mktecosystem\producao\estilos\palavra-de-ouro")
from base import FOIL, LOGO, MARCA, ruido  # noqa: E402

AQUI = Path(__file__).resolve().parent
CAFE, PAPEL, AREIA, OURO_ESCURO = "#1E1814", "#EFE6D9", "#E2D3BB", "#8A6420"
EIXO = 96


def afirmacao(md, m):
    return mito_lei.AJUSTE.get(md, {}).get("afirm") or mito_lei.TELA[md][0]


def pagina(md, m, variacao):
    faixa = variacao == "faixa"
    titulo_cor = PAPEL if faixa else CAFE
    return f"""<!doctype html><html><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap" rel=stylesheet>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(168deg,#FBF7F0 0%,{PAPEL} 46%,{AREIA} 100%)}}
#fibra{{position:absolute;inset:0;background:url("{ruido('.9', '30 24 20', '.5')}");mix-blend-mode:multiply;opacity:.16}}
#luz{{position:absolute;inset:0;background:radial-gradient(ellipse 60% 34% at 82% 26%,rgb(233 205 130/.38),transparent 70%),radial-gradient(ellipse 55% 30% at 10% 88%,rgb(201 169 98/.22),transparent 70%)}}
#topo{{position:absolute;left:0;right:0;top:0;height:{690 if faixa else 0}px;background:radial-gradient(ellipse 70% 60% at 78% 40%,#3a2f27,{CAFE} 70%)}}
.fx{{position:absolute;left:0;right:0;height:14px;background:{FOIL};box-shadow:0 0 22px rgb(240 210 130/.55);z-index:3}}
.cab,.rod{{position:absolute;left:{EIXO}px;right:{EIXO}px;display:flex;justify-content:space-between;align-items:center;font:500 24px Inter;letter-spacing:.06em}}
.cab{{top:290px;color:{'#D8C7A6' if faixa else OURO_ESCURO};text-transform:uppercase;font-weight:600;letter-spacing:.16em}}
.rod{{top:1574px;color:#5a4a3c}}
.ass{{display:flex;align-items:center;gap:16px}} .ass img{{height:46px}}
.ver{{display:flex;align-items:center;gap:12px;font-weight:600;color:{CAFE}}}
.ver b{{width:46px;height:46px;border-radius:50%;background:{FOIL};display:grid;place-items:center;box-shadow:0 4px 12px rgb(138 100 32/.35)}}
.ver b::after{{content:"";border-left:14px solid {CAFE};border-top:9px solid transparent;border-bottom:9px solid transparent;margin-left:4px}}
#tt{{position:absolute;left:{EIXO}px;right:{EIXO}px;top:380px;font:italic 500 168px/1 'EB Garamond',serif;color:{titulo_cor};letter-spacing:-.01em;white-space:nowrap}}
#tt .ouro{{background:{FOIL};-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 6px rgb(138 100 32/.35))}}
#tt::after{{content:"";display:block;width:140px;height:4px;background:{FOIL};margin-top:34px}}
.card{{position:absolute;left:{EIXO}px;right:{EIXO}px;top:760px;background:#FFFDF8;border-radius:28px;padding:44px 52px 52px;box-shadow:0 26px 60px rgb(60 40 20/.18),0 0 0 1.5px rgb(201 169 98/.55)}}
.card .t{{display:flex;justify-content:space-between;font:600 24px Inter;letter-spacing:.14em;text-transform:uppercase;color:{OURO_ESCURO};margin-bottom:26px}}
.card .m{{font:400 74px/1.16 'EB Garamond',serif;color:{CAFE};text-wrap:balance}}
.ops{{position:absolute;left:{EIXO}px;right:{EIXO}px;display:flex;gap:28px;align-items:center}}
.ops div{{flex:1;text-align:center;font:800 64px Inter;letter-spacing:.1em;padding:22px 0;border-radius:22px}}
.ops .mi{{color:{CAFE};border:5px solid {CAFE};background:rgb(255 253 248/.6)}}
.ops .le{{color:{CAFE};background:{MARCA};box-shadow:0 10px 26px rgb(138 100 32/.35)}}
.ops span{{font:italic 500 64px 'EB Garamond',serif;color:{OURO_ESCURO}}}
.dica{{position:absolute;left:{EIXO}px;right:{EIXO}px;font:500 30px Inter;color:#5a4a3c;text-align:center}}
</style></head><body><div id=c>
<div id=fibra></div><div id=luz></div><div id=topo></div>
<div class=fx style="top:240px"></div><div class=fx style="top:1666px"></div>
<div class=cab><span>Letícia Barros</span><span>Mito ou Lei</span></div>
<div id=tt>Mito ou <span class=ouro>Lei?</span></div>
<div class=card><div class=t><span>Ouvi por aí</span><span>Você sabe?</span></div><div class=m data-max=380>“{html.escape(afirmacao(md, m))}”</div></div>
<div class=ops><div class=mi>MITO</div><span>ou</span><div class=le>LEI</div></div>
<div class=dica>Responda antes de assistir</div>
<div class=rod><span class=ass><img src="{LOGO}">Letícia Barros · OAB/ES 39.948</span><span class=ver><b></b>Assista</span></div>
</div><script>document.fonts.ready.then(()=>{{
 const m=document.querySelector('.card .m');let s=74;while(m.offsetHeight>380&&s>50){{s-=2;m.style.fontSize=s+'px'}}
 const card=document.querySelector('.card'),ops=document.querySelector('.ops'),dica=document.querySelector('.dica');
 const fim=card.offsetTop+card.offsetHeight; ops.style.top=(fim+64)+'px'; dica.style.top=(fim+64+ops.offsetHeight+34)+'px';
 document.body.dataset.ok=1}})</script></body></html>"""


async def main():
    args = sys.argv[1:]
    variacoes = [args.pop(0)[2:]] if args and args[0].startswith("--") else ["papel", "faixa"]
    so = args
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for md, m in mito_lei.itens():
            if so and md not in so:
                continue
            pasta = AQUI / "mito-lei" / f"{md}-{m[1]}"
            if not pasta.exists():
                continue
            for v in variacoes:
                destino = pasta / f"capa-{v}.jpg"
                if destino.exists():  # capa pronta nunca é sobrescrita
                    continue
                await pg.set_content(pagina(md, m, v), wait_until="networkidle")
                await pg.wait_for_selector("body[data-ok]", state="attached")
                await pg.screenshot(path=str(destino), type="jpeg", quality=92)
                print(pasta.name, v)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
