"""Estilo MOLDURA VIVA (nome dado em 10/11/2026; docs/ESTILO_MOLDURA_VIVA.md): capa padrão dos Reels Mito ou Lei.
Foto do tema saindo da moldura (10/11/2026). A Jessica mandou uma referência de foto
emoldurada em papel, com a pessoa saindo do quadro, e disse: "poderíamos fazer as capas com fotos que seguem o tema".

Nossa identidade: papel claro com fibra, faixas e fio em dourado metálico, "Mito ou Lei?" em EB Garamond com Lei em
ouro, afirmação do vídeo em itálico, MITO / LEI sem revelar o veredito. A foto é a do tema (banco Pexels das
perguntas). Cada capa tem foto própria (FOTOS, abaixo): nunca a mesma de outro post, nem de pergunta ou carrossel do mesmo
tema (pedido da Jessica, 10/11/2026). O recorte (rembg, isnet) acha o topo da pessoa ou do objeto, e a foto é posicionada para esse topo passar
por cima da borda de cima da moldura. Se a pessoa já está cortada no alto da foto, fica só a moldura, sem sair.
Tudo o que importa fica no recorte da grade (y 240 a 1680).

Uso: python capas_mito_foto.py [MM-DD ...]  → mito-lei/<MM-DD>-<slug>/capa-moldura-viva.jpg (arquivo novo; recortes em _recortes/)."""
import asyncio
import base64
import html
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

import mito_lei

sys.path.insert(0, r"C:\Users\prosy\mktecosystem\producao\estilos\palavra-de-ouro")
from base import FOIL, LOGO, MARCA, ruido  # noqa: E402

AQUI = Path(__file__).resolve().parent
BANCO = AQUI.parents[3] / "apps" / "api" / "_saida_producao_1510" / "_fotos_pexels"
RECORTES = AQUI / "mito-lei" / "_recortes"
OURO_TEXTO = "linear-gradient(112deg,#7a5418 0%,#b88a32 22%,#e8cf86 38%,#a8792a 55%,#7a5418 72%,#c9a14e 88%,#8a6420 100%)"
CAFE, PAPEL, AREIA, OURO_ESCURO = "#1E1814", "#EFE6D9", "#E2D3BB", "#8A6420"
EIXO = 96
FX, FY, FW, FH = 150, 610, 780, 560  # janela da moldura
SAIDA = 120  # quanto a pessoa passa acima da borda de cima
_SESSAO = None
# foto Pexels de cada Mito ou Lei, escolhida pela afirmação; todas inéditas no banco e diferentes entre si
FOTOS = {"11-08": 7550933, "11-10": 7485259, "11-12": 7622513, "11-14": 7993402, "11-16": 6392894, "11-18": 18703556,
         "11-20": 5668881, "11-22": 3763583, "11-24": 18225736, "11-26": 7156512, "11-28": 8871515, "11-30": 5900158,
         "12-02": 39999216, "12-04": 12903128, "12-06": 4063537, "12-08": 4491431, "12-10": 6690448, "12-12": 6632528,
         "12-14": 7845468, "12-16": 35985680, "12-18": 6969756, "12-20": 34654342, "12-22": 15422833, "12-24": 8786851,
         "12-26": 19773937, "12-28": 8730366, "12-30": 18088839,
         # janeiro de 2027 (10/11/2026)
         "01-13": 7552577, "01-16": 5711457, "01-18": 6798766, "01-20": 6303669, "01-23": 6190658, "01-25": 8524998,
         "01-27": 6328951, "01-30": 30007526}
CENTRO = {4063537}  # fotos em que o recorte pega objeto solto no alto (luminária): enquadrar pelo centro
assert len(set(FOTOS.values())) == len(FOTOS), "foto repetida entre capas"


def fotos_por_tema():
    return {t["chave"]: t.get("pergunta", {}) for d in (mito_lei.conteudo_nov, mito_lei.conteudo_dez, mito_lei.conteudo_jan) for t in d.TEMAS}


def data_uri(im, fmt):
    b = io.BytesIO()
    im.save(b, fmt, **({"quality": 88} if fmt == "JPEG" else {}))
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()


def foto_e_recorte(foto_id):
    """Foto reduzida e o recorte limpo (só o que o modelo tem certeza de ser a pessoa ou o objeto)."""
    global _SESSAO
    RECORTES.mkdir(exist_ok=True)
    im = Image.open(BANCO / f"{foto_id}.jpg").convert("RGB")
    im.thumbnail((1400, 1400))
    im.foto_id = foto_id
    cache = RECORTES / f"{foto_id}.png"
    if not cache.exists():
        from rembg import new_session, remove
        # o modelo padrão (birefnet) estoura a memória nesta máquina; o isnet é leve e recorta bem pessoas e objetos
        _SESSAO = _SESSAO or new_session("isnet-general-use")
        remove(im, session=_SESSAO).save(cache)
    rec = Image.open(cache).convert("RGBA")
    a = rec.getchannel("A").point(lambda v: 255 if v > 150 else 0)
    rec.putalpha(a)
    return im, rec, a


def geometria(im, bbox, alfa):
    """Escala e posição da foto: cobre a janela e põe o topo da pessoa SAIDA px acima da borda de cima."""
    w, h = im.size
    sai = bool(bbox) and bbox[1] > h * .04  # pessoa cortada no alto da foto não sai da moldura
    if sai:  # fiapo solto (vapor, reflexo) não conta: precisa de massa na faixa que vai passar da borda
        faixa = alfa.crop((bbox[0], bbox[1], bbox[2], min(h, bbox[1] + int(h * .12))))
        sai = sum(faixa.histogram()[255:]) > faixa.width * faixa.height * .12
    topo = bbox[1] if sai else 0
    s = max(FW / w, (FH + (SAIDA if sai else 0)) / (h - topo))
    y = FY - (SAIDA if sai else 0) - topo * s
    if not sai and bbox:  # sem sair da moldura: centraliza a pessoa na janela
        alta = (bbox[3] - bbox[1]) * s > FH - 60 and getattr(im, 'foto_id', None) not in CENTRO  # pessoa maior que a janela: mostra a cabeça, com folga em cima
        y = FY + 30 - bbox[1] * s if alta else FY + FH / 2 - (bbox[1] + bbox[3]) / 2 * s
    y = max(min(y, FY), FY + FH - h * s)
    cx = ((bbox[0] + bbox[2]) / 2 if bbox else w / 2) * s
    x = min(FX, max(FX + FW - w * s, FX + FW / 2 - cx))
    return sai, s, x, y, w * s, h * s


def pagina(md, im, rec, alfa):
    bbox = alfa.getbbox()
    afirm = mito_lei.AJUSTE.get(md, {}).get("afirm") or mito_lei.TELA[md][0]
    sai, s, x, y, bw, bh = geometria(im, bbox, alfa)
    caixa = f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;background-size:100% 100%"
    # o recorte só aparece acima da janela (e um pouco para os lados), por cima do fio dourado
    corte = f"inset(0 {x + bw - FX - FW - 30:.0f}px {y + bh - FY - 6:.0f}px {FX - x - 30:.0f}px)"
    return f"""<!doctype html><html><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600;700;800&display=swap" rel=stylesheet>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(168deg,#FBF7F0 0%,{PAPEL} 48%,{AREIA} 100%)}}
#fibra{{position:absolute;inset:0;background:url("{ruido('.9', '30 24 20', '.5')}");mix-blend-mode:multiply;opacity:.16}}
#luz{{position:absolute;inset:0;background:radial-gradient(ellipse 55% 30% at 85% 22%,rgb(233 205 130/.34),transparent 70%)}}
.fx{{position:absolute;left:0;right:0;height:12px;background:{FOIL};box-shadow:0 0 18px rgb(240 210 130/.5);z-index:5}}
.cab,.rod{{position:absolute;left:{EIXO}px;right:{EIXO}px;display:flex;justify-content:space-between;align-items:center;font:600 22px Inter;letter-spacing:.16em;text-transform:uppercase}}
.cab{{top:286px;color:{OURO_ESCURO}}}
.rod{{top:1590px;color:#5a4a3c;text-transform:none;letter-spacing:.04em;font-weight:500}}
.ass{{display:flex;align-items:center;gap:14px}} .ass img{{height:42px}}
.ver{{display:flex;align-items:center;gap:12px;font-weight:600;color:{CAFE}}}
.ver b{{width:44px;height:44px;border-radius:50%;background:{FOIL};display:grid;place-items:center}}
.ver b::after{{content:"";border-left:13px solid {CAFE};border-top:8px solid transparent;border-bottom:8px solid transparent;margin-left:4px}}
#tt{{position:absolute;left:{EIXO}px;top:340px;font:italic 500 124px/1 'EB Garamond',serif;color:{CAFE};white-space:nowrap}}
#tt .ouro{{background:{OURO_TEXTO};-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 5px rgb(138 100 32/.35))}}
#janela{{position:absolute;left:{FX}px;top:{FY}px;width:{FW}px;height:{FH}px;overflow:hidden;box-shadow:0 30px 60px rgb(60 40 20/.25)}}
#janela div{{{caixa.replace(f'left:{x:.0f}px;top:{y:.0f}px', f'left:{x - FX:.0f}px;top:{y - FY:.0f}px')};background-image:url({data_uri(im, 'JPEG')})}}
#fio{{position:absolute;left:{FX - 20}px;top:{FY - 20}px;width:{FW + 40}px;height:{FH + 40}px;border:3px solid transparent;border-image:{FOIL} 1}}
#sai{{{caixa};background-image:url({data_uri(rec, 'PNG')});clip-path:{corte};filter:drop-shadow(0 14px 14px rgb(60 40 20/.3));display:{'block' if sai else 'none'}}}
.txt{{position:absolute;left:{EIXO}px;right:{EIXO}px;top:{FY + FH + 58}px}}
.txt .m{{font:italic 400 58px/1.12 'EB Garamond',serif;color:{CAFE};text-wrap:balance}}
.ops{{position:absolute;left:{EIXO}px;display:flex;gap:22px;align-items:center}}
.ops div{{width:220px;text-align:center;font:800 36px Inter;letter-spacing:.12em;padding:12px 0;border-radius:14px}}
.ops .mi{{color:{CAFE};border:4px solid {CAFE}}}
.ops .le{{color:{CAFE};background:{MARCA};box-shadow:0 8px 20px rgb(138 100 32/.3)}}
.ops span{{font:italic 500 44px 'EB Garamond',serif;color:{OURO_ESCURO}}}
.ops em{{font:600 20px Inter;letter-spacing:.16em;text-transform:uppercase;color:{OURO_ESCURO};font-style:normal;margin-left:14px}}
</style></head><body><div id=c>
<div id=fibra></div><div id=luz></div>
<div class=fx style="top:240px"></div><div class=fx style="top:1668px"></div>
<div class=cab><span>Letícia Barros</span><span>Ouvi por aí</span></div>
<div id=tt>Mito ou <span class=ouro>Lei?</span></div>
<div id=fio></div><div id=janela><div></div></div><div id=sai></div>
<div class=txt><div class=m>“{html.escape(afirm)}”</div></div>
<div class=ops><div class=mi>MITO</div><span>ou</span><div class=le>LEI</div></div>
<div class=rod><span class=ass><img src="{LOGO}">Letícia Barros · OAB/ES 39.948</span><span class=ver><b></b>Assista</span></div>
</div><script>document.fonts.ready.then(()=>{{
 // afirmação até 3 linhas; os botões vêm logo abaixo e nunca passam do rodapé
 const t=document.querySelector('.txt'),m=t.querySelector('.m'),ops=document.querySelector('.ops');
 let s=58; while(t.offsetTop+t.offsetHeight>1460&&s>40){{s-=2;m.style.fontSize=s+'px'}}
 ops.style.top=Math.min(t.offsetTop+t.offsetHeight+30,1490)+'px'; document.body.dataset.ok=1}})</script></body></html>"""


async def main():
    so = sys.argv[1:]
    repetidas = [f for f in set(FOTOS.values()) if list(FOTOS.values()).count(f) > 1]
    if repetidas:  # nunca a mesma foto em dois posts (10/11/2026)
        sys.exit(f"foto repetida em FOTOS: {repetidas}")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for md, m in mito_lei.itens():
            if so and md not in so:
                continue
            pasta = AQUI / "mito-lei" / f"{md}-{m[1]}"
            destino = pasta / "capa-moldura-viva.jpg"
            if not pasta.exists() or destino.exists():  # capa pronta nunca é sobrescrita
                continue
            if md not in FOTOS:
                print(md, "sem foto escolhida em FOTOS")
                continue
            im, rec, alfa = foto_e_recorte(FOTOS[md])
            await pg.set_content(pagina(md, im, rec, alfa), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            await pg.screenshot(path=str(destino), type="jpeg", quality=92)
            print(pasta.name, "foto", "sai" if geometria(im, alfa.getbbox(), alfa)[0] else "sem sair")
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
