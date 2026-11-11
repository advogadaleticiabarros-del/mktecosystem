"""Capa dos Reels gravados pela Dra. (domingo 15h30, pedido da Jessica em 10/11/2026: "no domingo um vídeo reels original
dela falando com a figura dela mesmo"). Antes esses Reels saíam sem capa própria (quadro do vídeo).

Papel claro com fibra, faixas e fio em dourado metálico com brilho, rótulo "Domingo com a Dra.", tema em EB Garamond com
o destaque em itálico dourado, e um retrato real da Dra. sentada (_retratos/) num quadro de moldura dourada grossa
girado em 3D, com sombra no papel (pedido de 10/11/2026: "Coloque em 3D alguma foto da Dra sentada"). Sem recorte
automático: o recorte do cabelo dela já foi reprovado. Tudo no recorte 3:4 da grade (y 240 a 1680). Capa pronta nunca é sobrescrita.

Uso: python capas_dra.py <saida_dir>   (lê CAPAS abaixo)"""
import asyncio
import base64
import sys
from pathlib import Path

from playwright.async_api import async_playwright

RETRATOS = Path(__file__).resolve().parents[2] / "apps" / "api" / "_saida_producao_1510" / "_retratos"
# dia: (retrato da Dra. sentada, foco vertical da foto, título, destaque em itálico, linha de apoio)
# 10/11/2026: a Jessica reprovou a capa com o quadro do vídeo e pediu "em 3D alguma foto da Dra sentada"
CAPAS = {
    "2026-11-15": ("estudio-claro-cadeira", "50% 30%", "Limbo", "previdenciário", "O INSS diz que pode, a empresa diz que não."),
    "2026-11-22": ("poltrona-terno-cinza", "50% 25%", "Quem paga", "o salário?", "Limbo previdenciário, parte 2."),
    "2026-11-29": ("estudio-livros", "50% 25%", "Hora extra:", "quanto vale?", "Hora extra, parte 1 de 3."),
    "2026-12-06": ("escritorio-cafe-blazer-bege", "50% 30%", "Banco", "de horas", "Hora extra, parte 2 de 3."),
    "2026-12-13": ("estudio-escuro-banco", "50% 25%", "Não bate", "ponto?", "Como provar hora extra. Parte 3 de 3."),
    "2026-12-20": ("escritorio-logo-escrevendo", "50% 25%", "Pediu", "demissão?", "A multa do 477 também vale para você."),
    "2026-12-27": ("escritorio-cafe-blazer-preto", "50% 25%", "Conselhos", "da advogada", "O que eu queria que você soubesse antes."),
}
OURO = "linear-gradient(112deg,#7a5418 0%,#b88a32 22%,#f3dc98 38%,#a8792a 55%,#7a5418 72%,#e1c172 88%,#8a6420 100%)"


def foto(nome):
    return "data:image/jpeg;base64," + base64.b64encode((RETRATOS / f"{nome}.jpg").read_bytes()).decode()


def pagina(foto, foco, titulo, destaque, apoio):
    return f"""<!doctype html><html><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,500&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#EFE6D9;color:#1E1814;font-family:Inter}}
.fibra{{position:absolute;inset:0;background:radial-gradient(120% 60% at 80% 10%,rgb(255 255 255/.55),transparent 60%),repeating-linear-gradient(93deg,rgb(120 90 50/.035) 0 2px,transparent 2px 7px)}}
.fx{{position:absolute;left:0;right:0;height:14px;background:{OURO};box-shadow:0 0 18px rgb(232 200 120/.5)}}
.rot{{position:absolute;top:300px;left:96px;right:96px;display:flex;justify-content:space-between;font:600 26px Inter;letter-spacing:.16em;text-transform:uppercase}}
.rot b{{background:{OURO};-webkit-background-clip:text;color:transparent}}
.fio{{position:absolute;top:350px;left:96px;right:96px;height:3px;background:{OURO}}}
h1{{position:absolute;top:388px;left:96px;right:96px;font:500 132px/1 'EB Garamond',serif;letter-spacing:-.01em}}
h1 i{{display:block;font-style:italic;background:{OURO};-webkit-background-clip:text;color:transparent;padding-bottom:8px}}
.palco{{position:absolute;top:735px;left:0;right:0;height:760px;perspective:1500px;display:flex;justify-content:center}}
.jan{{position:relative;width:520px;height:660px;transform:rotateY(-24deg) rotateX(5deg) rotateZ(-1deg);transform-style:preserve-3d}}
.frente{{position:absolute;inset:0;padding:16px;background:{OURO};box-shadow:inset 0 0 0 2px rgb(255 240 200/.7),inset 0 0 0 7px rgb(122 84 24/.5)}}
.frente img{{width:100%;height:100%;object-fit:cover;object-position:{foco};display:block;box-shadow:inset 0 0 0 1px #000}}
.brilho{{position:absolute;inset:16px;background:linear-gradient(115deg,rgb(255 255 255/.32) 0%,rgb(255 255 255/0) 34%,rgb(255 255 255/0) 70%,rgb(255 240 200/.18) 100%)}}
.lado{{position:absolute;top:0;right:-34px;width:34px;height:100%;background:linear-gradient(90deg,#8a6420,#5c4012);transform-origin:left;transform:rotateY(90deg)}}
.topo{{position:absolute;left:0;top:-34px;width:100%;height:34px;background:linear-gradient(0deg,#b88a32,#f3dc98);transform-origin:bottom;transform:rotateX(-90deg)}}
.sombra{{position:absolute;top:1372px;left:290px;width:540px;height:70px;border-radius:50%;background:radial-gradient(closest-side,rgb(30 24 20/.42),transparent);filter:blur(6px)}}
.ap{{position:absolute;top:1448px;left:96px;right:96px;text-align:center;font:400 34px/1.35 Inter}}
.pe{{position:absolute;top:1560px;left:96px;right:96px;display:flex;justify-content:space-between;align-items:center;font:500 26px Inter;letter-spacing:.06em}}
.pe span:last-child{{background:{OURO};color:#1E1814;padding:12px 26px;border-radius:999px;font-weight:600;letter-spacing:.12em}}
</style></head><body><div class=fibra></div><div class=fx style="top:0"></div><div class=fx style="bottom:0"></div>
<div class=rot><span>Domingo com a Dra.</span><b>Vídeo</b></div><div class=fio></div>
<h1>{titulo}<i>{destaque}</i></h1><div class=sombra></div><div class=palco><div class=jan><div class=topo></div><div class=lado></div><div class=frente><img src="{foto}"><div class=brilho></div></div></div></div><div class=ap>{apoio}</div>
<div class=pe><span>Letícia Barros · OAB/ES 39.948</span><span>▶ ASSISTA</span></div></body></html>"""


async def main(saida):
    saida.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for dia, (retrato, foco, tit, dest, apoio) in CAPAS.items():
            arq = saida / f"dra-capa-{dia}.jpg"
            if arq.exists():
                print(dia, "já existe (não sobrescrevo)")
                continue
            await pg.set_content(pagina(foto(retrato), foco, tit, dest, apoio), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(arq), type="jpeg", quality=92)
            print(dia, arq.name)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1])))
