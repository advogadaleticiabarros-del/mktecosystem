"""5 variações contínuas do carrossel "Mãe por adoção" (09/11/2026), cada uma a partir de uma
referência enviada pela Jessica. Regra fixa: capa = foto do assunto; última página = retrato
real da Dra. Cada variação é um panorama 7 × 1080 × 1440 fatiado em 7 slides.

A  Ouro em diagonal   (ref. "Abogados caros": painéis claros em diagonal sobre fundo escuro)
B  Revista            (ref. juros abusivos: fundos alternados, foto partida entre slides, palavra-fantasma)
C  Fio condutor       (ref. advocacia séria: linha dourada com marcos e fotos na divisa)
D  Cartões            (ref. Revalida: cartões arredondados que atravessam a divisa sobre fundo escuro)
E  Objetos e arco     (ref. Revalida/juros: papel, arco dourado e objetos recortados na divisa)

Uso: python gerar_v3.py [A B ...]   (saída em ./saida_v3/<letra>/)
"""
import asyncio
import base64
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
RET = RAIZ / "apps/api/_saida_producao_1510/_retratos"
REC = RAIZ / "apps/api/_saida_producao_1510/_recortes"
FOT = AQUI / "fotos"
SAIDA = AQUI / "saida_v3"
W, H, N = 1080, 1440, 7
CAFE, PAPEL, OURO, BRONZE, CLARO, OURO_CL = "#231E1A", "#F7F1E7", "#C9A962", "#8F7032", "#E8DED1", "#E6CF94"


METAL = "linear-gradient(100deg,#7d5f24 0%,#c9a962 18%,#fff3c8 34%,#e2c172 48%,#9c7a34 64%,#f2dc9a 82%,#a8843c 100%)"
GLOW = "0 0 22px rgba(255,214,130,.75),0 0 6px rgba(255,236,180,.9)"
METAL_TXT = "linear-gradient(100deg,#d9b866 0%,#fff3c8 30%,#e8c978 55%,#fff0bd 80%,#d4b064 100%)"
TXT_GLOW = "drop-shadow(0 0 10px rgba(255,210,120,.55))"


def uri(p):
    tipo = "png" if p.suffix == ".png" else "jpeg"
    return f"data:image/{tipo};base64," + base64.b64encode(p.read_bytes()).decode()


ITENS = [
    ("<em>120 dias</em>, qualquer que seja a idade da criança",
     "A mãe adotante tem a mesma licença da mãe biológica, <b>de bebê ou de criança maior</b>.", "CLT, art. 392-A"),
    ("Igual em <em>todos</em> os regimes",
     "O STF acabou com prazos menores para <b>servidoras federais e militares</b>.", "STF · ADI 7495 (23/09/2026)"),
    ("A licença começa na <em>guarda</em>",
     "Conta da adoção ou da <b>guarda para fins de adoção</b>. Não precisa esperar a sentença.", "CLT, art. 392-A, § 4º"),
    ("Mais <em>60 dias</em> em empresas cidadãs",
     "Se a empresa aderiu ao Empresa Cidadã, <b>a prorrogação vale igual</b> para quem adota: 180 dias.", "Lei 11.770/2008"),
    ("Licenças em curso <em>já</em> entram",
     "Quem estava de licença em 23/09/2026 já segue a regra nova. Separe:", "STF · ADI 7495"),
]
CHECK = ["Termo de guarda ou sentença de adoção", "Aviso ao RH com a data de início", "Confirmar se a empresa é Empresa Cidadã"]

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{position:relative;width:{W*N}px;height:{H}px;overflow:hidden;font-family:Inter,sans-serif;font-variant-numeric:lining-nums;background:{CAFE}}}
.abs{{position:absolute}}
.b{{position:absolute;z-index:10;display:flex;flex-direction:column;gap:26px}}
.n{{font-family:'EB Garamond',serif;font-size:44px;font-weight:600}}
.t{{font-family:'EB Garamond',serif;line-height:1.04;font-weight:500}}
.x{{font-size:34px;line-height:1.45}} .x b{{font-weight:700}}
.esc{{color:{CLARO}}} .esc .n{{color:{OURO}}} .esc em,.esc .n,.ouro{{font-style:italic;background:{METAL_TXT};-webkit-background-clip:text;background-clip:text;color:transparent;filter:{TXT_GLOW}}}
.esc .n{{font-style:normal}} .esc .x b{{color:{OURO_CL}}}
.cla{{color:{CAFE}}} .cla .n{{color:{BRONZE}}}
.cla em{{font-style:italic;background:{METAL} no-repeat left bottom/100% 7px;padding-bottom:6px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.selo{{display:inline-block;font-size:22px;font-weight:700;letter-spacing:2px;text-transform:uppercase;background:{METAL};color:{CAFE};padding:10px 18px;border-radius:4px;box-shadow:{GLOW}}}
.cla .selo.inv{{background:{CAFE};color:{OURO_CL};box-shadow:0 0 0 2px #e2c172,{GLOW}}}
.ck{{display:flex;gap:22px;align-items:flex-start;font-size:32px;line-height:1.35}}
.ck i{{flex:none;width:32px;height:32px;border:3px solid #f2dc9a;border-radius:5px;margin-top:5px;box-shadow:{GLOW}}}
.cla .ck i{{border-color:{BRONZE}}}
.cab{{position:absolute;top:56px;z-index:40;display:flex;justify-content:space-between;font-size:22px;font-weight:600;letter-spacing:3px;text-transform:uppercase}}
.faixa{{position:absolute;left:0;width:{W*N}px;height:24px;z-index:60;background:linear-gradient(180deg,#7d5f24 0%,#d9b866 22%,#fff8dc 46%,#fffbe8 52%,#e8c978 70%,#8a6a2a 100%);box-shadow:0 0 30px 8px rgba(255,214,130,.85),0 0 70px 14px rgba(255,200,100,.35)}}
.serif{{font-family:'EB Garamond',serif}}
"""
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500;1,600'
          '&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">')


def bloco(x, y, w, n, esc, tam=84, centro=False, check=False, selo_inv=False):
    t, txt, selo = ITENS[n - 1]
    ck = "".join(f'<div class="ck"><i></i>{c}</div>' for c in CHECK) if check else ""
    al = "text-align:center;align-items:center;" if centro else ""
    return (f'<div class="b {"esc" if esc else "cla"}" style="left:{x}px;top:{y}px;width:{w}px;{al}">'
            f'<div class="n">{n:02d}</div><div class="t" style="font-size:{tam}px">{t}</div><div class="x">{txt}</div>'
            f'{ck}<div><span class="selo{" inv" if selo_inv else ""}">{selo}</span></div></div>')


def cabs(esc):
    return "".join(f'<div class="cab" style="left:{i*W+80}px;width:{W-160}px;color:{CLARO if e else CAFE}"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>'
                   for i, e in enumerate(esc))


def fundo(i, cor):
    return f'<div class="abs" style="left:{i*W}px;top:0;width:{W}px;height:{H}px;background:{cor}"></div>'


def foto(src, x, y, w, h, pos="center", raio=0, extra="", z=2):
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{raio}px;overflow:hidden;z-index:{z};{extra}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}"></div>')


def fatia(i, inner, z=3):
    return f'<div class="abs" style="left:{i*W}px;top:0;width:{W}px;height:{H}px;overflow:hidden;z-index:{z}">{inner}</div>'


def capa(src, pos="center", larg=W, fade_dir=None):
    mask = f"-webkit-mask-image:linear-gradient(90deg,#000 {int(W/larg*100)-8}%,transparent);" if larg > W else ""
    return (foto(src, 0, 0, larg, H, pos, extra=mask)
            + f'<div class="abs" style="left:0;top:0;width:{W}px;height:{H}px;z-index:3;background:linear-gradient(180deg,rgba(35,30,26,.55) 0%,rgba(35,30,26,0) 28%,rgba(35,30,26,.25) 48%,{CAFE} 80%)"></div>'
            + f'''<div class="b esc" style="left:80px;width:920px;bottom:150px;gap:16px">
  <div style="font-size:30px;font-weight:600;letter-spacing:4px;text-transform:uppercase" class="ouro">Mãe por adoção</div>
  <div class="t" style="font-size:150px;line-height:.95"><em>5 direitos</em></div>
  <div class="t" style="font-size:64px;line-height:1.1">iguais aos da mãe biológica</div>
  <div class="x" style="margin-top:12px">O STF fechou em setembro <b>uma diferença antiga</b> entre as mães.</div>
  <div style="margin-top:12px"><span class="selo">STF · ADI 7495</span></div></div>''')


def fecho(src, pos="center 25%", esq=80):
    x0 = 6 * W
    return (foto(src, x0, 0, W, H, pos)
            + f'<div class="abs" style="left:{x0}px;top:0;width:{W}px;height:{H}px;z-index:3;background:linear-gradient(180deg,rgba(35,30,26,.5) 0%,rgba(35,30,26,0) 24%,rgba(35,30,26,.2) 44%,{CAFE} 76%)"></div>'
            + f'''<div class="b esc" style="left:{x0+esq}px;width:{W-esq-80}px;bottom:150px;gap:20px">
  <div class="t" style="font-size:96px">Família se forma de muitos <em>jeitos</em>.</div>
  <div class="t" style="font-size:54px"><em>O direito é o mesmo.</em></div>
  <div class="x">Salve e <b>mande para quem está adotando.</b> Na dúvida, procure uma advogada.</div>
  <div style="padding-top:22px;border-top:2px solid #e2c172;box-shadow:0 -8px 14px -10px rgba(255,214,130,.9);font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase"><span class="ouro" style="font-style:normal">Letícia Barros · OAB/ES 39.948</span></div></div>''')


def adocao_vertical(x):
    return (f'<div class="serif abs" style="z-index:15;left:{x-125}px;top:{H//2-125}px;width:250px;height:250px;display:flex;align-items:center;justify-content:center;'
            f'transform:rotate(90deg);font-size:250px;font-weight:600;letter-spacing:10px;white-space:nowrap"><span class="ouro" style="font-style:normal">ADOÇÃO</span></div>')


def F(nome):
    return uri(FOT / nome)


# ---------------------------------------------------------------- variações
def var_a():
    esc = [True, True, False, True, False, True, True]
    svg = (f'<svg class="abs" style="left:0;top:0;z-index:1" width="{W*N}" height="{H}"><defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c7a34"/><stop offset=".25" stop-color="#fff3c8"/><stop offset=".45" stop-color="#d9b866"/><stop offset=".65" stop-color="#fff0bd"/><stop offset=".85" stop-color="#c9a962"/><stop offset="1" stop-color="#8a6a2a"/></linearGradient><linearGradient id="mc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9be7e"/><stop offset=".45" stop-color="#f7e6b5"/><stop offset="1" stop-color="#cfae66"/></linearGradient></defs>'
           f'<polygon points="2160,0 3100,0 3400,{H} 1960,{H}" fill="url(#mc)"/>'
           f'<polygon points="4320,0 5260,0 5560,{H} 4120,{H}" fill="url(#mc)"/>'
           f'<line x1="3100" y1="0" x2="3400" y2="{H}" stroke="url(#m)" stroke-width="8"/><line x1="5260" y1="0" x2="5560" y2="{H}" stroke="url(#m)" stroke-width="8"/></svg>')
    return (svg + capa(F("p15003426.jpg"), "center 30%", larg=W + 280)
            + bloco(W + 300, 280, 600, 1, True, tam=78)
            + bloco(2 * W + 110, 260, 760, 2, False, tam=92, selo_inv=True)
            + bloco(3 * W + 200, 260, 760, 3, True, tam=84)
            + foto(F("p10557890.jpg"), 4 * W - 330, 980, 660, 380, "center 35%", raio=24, extra=f"box-shadow:0 24px 50px rgba(0,0,0,.35),{GLOW};border:4px solid #f2dc9a", z=12)
            + bloco(4 * W + 120, 240, 760, 4, False, tam=84, selo_inv=True)
            + bloco(5 * W + 200, 220, 660, 5, True, tam=80, check=True)
            + adocao_vertical(6 * W) + fecho(RETS["A"], esq=200) + cabs(esc))


def var_b():
    esc = [True, True, False, False, False, True, True]
    bgs = [CAFE, CAFE, PAPEL, PAPEL, PAPEL, CAFE, CAFE]
    fan = lambda i, cor: fatia(i, f'<div class="serif abs" style="left:{1180 - i*W}px;top:1010px;font-size:380px;font-style:italic;line-height:1;color:{cor};white-space:nowrap">adoção</div>', z=2)
    regua = (f'<div class="abs" style="z-index:11;left:{W+80}px;top:1372px;width:{5*W-160}px;height:3px;background:{METAL};box-shadow:{GLOW}"></div>'
             + "".join(f'<div class="abs" style="z-index:11;left:{i*W-9}px;top:1364px;width:18px;height:18px;background:{METAL};box-shadow:{GLOW};transform:rotate(45deg)"></div>' for i in range(2, 6)))
    return ("".join(fundo(i, c) for i, c in enumerate(bgs)) + fan(1, "rgba(201,169,98,.14)") + fan(2, "rgba(35,30,26,.07)")
            + capa(F("p8525000.jpg"), "center 30%")
            + bloco(W + 90, 280, 860, 1, True, tam=92)
            + bloco(2 * W + 110, 260, 860, 2, False, tam=96)
            + foto(F("p10557890.jpg"), 3 * W + 560, 0, W - 560 + 400, H, "center 35%", z=4)
            + f'<div class="abs" style="z-index:5;left:{3*W+560}px;top:0;width:10px;height:{H}px;background:linear-gradient(180deg,#9c7a34,#fff3c8 25%,#d9b866 50%,#fff0bd 75%,#9c7a34);box-shadow:{GLOW}"></div>'
            + bloco(3 * W + 80, 300, 440, 3, False, tam=66)
            + bloco(4 * W + 450, 300, 560, 4, False, tam=66)
            + bloco(5 * W + 90, 220, 880, 5, True, tam=84, check=True)
            + regua + fecho(RETS["B"]) + cabs(esc))


def var_c():
    esc = [True, False, True, False, True, False, True]
    bgs = [CAFE, PAPEL, CAFE, PAPEL, CAFE, PAPEL, CAFE]
    linha = (f'<div class="abs" style="z-index:30;left:80px;top:1338px;width:{W*N-160}px;height:4px;background:{METAL};box-shadow:{GLOW}"></div>'
             + "".join(f'<div class="abs serif" style="z-index:31;left:{i*W+540-26}px;top:1313px;width:52px;height:52px;border-radius:50%;background:{METAL};box-shadow:{GLOW};color:{CAFE};font-size:28px;font-weight:600;display:flex;align-items:center;justify-content:center">{i}</div>' for i in range(1, 6)))
    cart = lambda src, x, pos: foto(src, x - 280, 900, 560, 340, pos, raio=20, extra=f"border:4px solid #f2dc9a;box-shadow:0 20px 40px rgba(0,0,0,.3),{GLOW}", z=12)
    return ("".join(fundo(i, c) for i, c in enumerate(bgs))
            + capa(F("p19797693.jpg"), "center 40%").replace("bottom:150px", "bottom:190px")
            + bloco(W + 90, 240, 860, 1, False, tam=90)
            + bloco(2 * W + 110, 240, 860, 2, True, tam=96)
            + bloco(3 * W + 110, 240, 860, 3, False, tam=90)
            + bloco(4 * W + 110, 240, 860, 4, True, tam=86)
            + bloco(5 * W + 110, 200, 860, 5, False, tam=80, check=True)
            + cart(F("p10557890.jpg"), 2 * W, "center 35%") + cart(F("p8524973.jpg"), 4 * W, "center 40%")
            + linha + fecho(RETS["C"]).replace("bottom:150px", "bottom:190px") + cabs(esc))


def var_d():
    esc = [True, False, True, False, False, True, True]
    onda = (f'<svg class="abs" style="left:0;top:0;z-index:1;filter:drop-shadow(0 0 10px rgba(255,214,130,.7))" width="{W*N}" height="{H}"><defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c7a34"/><stop offset=".25" stop-color="#fff3c8"/><stop offset=".45" stop-color="#d9b866"/><stop offset=".65" stop-color="#fff0bd"/><stop offset=".85" stop-color="#c9a962"/><stop offset="1" stop-color="#8a6a2a"/></linearGradient><linearGradient id="mc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9be7e"/><stop offset=".45" stop-color="#f7e6b5"/><stop offset="1" stop-color="#cfae66"/></linearGradient></defs><path d="M0 1150 C 1200 900, 2200 1400, 3600 1100 S 6200 900, {W*N} 1200" '
            f'fill="none" stroke="url(#m)" stroke-opacity=".9" stroke-width="4"/><path d="M0 1190 C 1200 940, 2200 1440, 3600 1140 S 6200 940, {W*N} 1240" fill="none" stroke="url(#m)" stroke-opacity=".5" stroke-width="2"/></svg>')
    cartao = lambda x, w: f'<div class="abs" style="z-index:5;left:{x}px;top:190px;width:{w}px;height:800px;border-radius:36px;background:{PAPEL};box-shadow:0 30px 60px rgba(0,0,0,.4)"></div>'
    return (f'<div class="abs" style="left:0;top:0;width:{W*N}px;height:{H}px;background:radial-gradient(ellipse at 50% 30%,#3A2F27,{CAFE} 70%)"></div>' + onda
            + capa(F("p9478785.jpg"), "center 30%")
            + cartao(W + 70, W - 70 + 140) + bloco(W + 150, 300, 820, 1, False, tam=90)
            + foto(F("p10557890.jpg"), 2 * W + 240, 170, 760, 560, "center 35%", raio=36, extra="box-shadow:0 30px 60px rgba(0,0,0,.4)", z=6)
            + f'<div class="abs" style="z-index:7;left:{2*W+270}px;top:650px;background:{METAL};box-shadow:{GLOW};color:{CAFE};font-size:24px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:12px 20px;border-radius:6px">Todas as mães</div>'
            + bloco(2 * W + 240, 790, 760, 2, True, tam=76)
            + bloco(3 * W + 110, 280, 760, 3, True, tam=88)
            + cartao(4 * W - 140, W + 140 - 80) + bloco(4 * W + 80, 300, 840, 4, False, tam=88)
            + bloco(5 * W + 110, 220, 860, 5, True, tam=84, check=True)
            + fecho(RETS["D"]) + cabs(esc))


def var_e():
    esc = [True, False, False, True, False, False, True]
    bgs = [CAFE, PAPEL, PAPEL, CAFE, PAPEL, PAPEL, CAFE]
    arco = (f'<svg class="abs" style="left:0;top:0;z-index:4" width="{W*N}" height="{H}"><defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c7a34"/><stop offset=".25" stop-color="#fff3c8"/><stop offset=".45" stop-color="#d9b866"/><stop offset=".65" stop-color="#fff0bd"/><stop offset=".85" stop-color="#c9a962"/><stop offset="1" stop-color="#8a6a2a"/></linearGradient><linearGradient id="mc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9be7e"/><stop offset=".45" stop-color="#f7e6b5"/><stop offset="1" stop-color="#cfae66"/></linearGradient></defs>'
            + "".join(f'<circle cx="3780" cy="{3000+d}" r="{2000+d}" fill="none" stroke="url(#m)" stroke-width="{w+2}"/>' for d, w in ((0, 4), (46, 2)))
            + "</svg>")
    obj = lambda nome, x, y, h: f'<img class="abs" src="{uri(REC / nome)}" style="z-index:13;left:{x}px;top:{y}px;height:{h}px;filter:drop-shadow(0 20px 24px rgba(35,30,26,.35))">'
    marca = lambda i, cor: fatia(i, f'<div class="serif abs" style="right:30px;top:110px;font-size:520px;line-height:1;font-weight:600;color:{cor}">0{i}</div>', z=2)
    return ("".join(fundo(i, c) for i, c in enumerate(bgs)) + marca(1, "rgba(143,112,50,.10)") + marca(2, "rgba(143,112,50,.10)")
            + marca(4, "rgba(143,112,50,.10)") + marca(5, "rgba(143,112,50,.10)") + arco
            + capa(F("p8524973.jpg"), "center 40%")
            + bloco(W + 90, 300, 860, 1, False, tam=92)
            + bloco(2 * W + 260, 300, 720, 2, False, tam=92)
            + bloco(3 * W + 110, 280, 860, 3, True, tam=92)
            + bloco(4 * W + 110, 280, 860, 4, False, tam=88)
            + bloco(5 * W + 260, 220, 720, 5, False, tam=80, check=True)
            + obj("obj-ursinho2.png", 2 * W - 200, 1000, 380) + obj("corte-sapatinho.png", 5 * W - 230, 1040, 300)
            + fecho(RETS["E"]) + cabs(esc))


RETS = {k: uri(RET / v) for k, v in {"A": "escritorio-cafe-blazer-bege.jpg", "B": "estudio-claro-cadeira.jpg",
                                     "C": "poltrona-terno-cinza.jpg", "D": "tablet-blazer-marrom.jpg",
                                     "E": "escritorio-logo-escrevendo.jpg"}.items()}
VARS = {"A": var_a, "B": var_b, "C": var_c, "D": var_d, "E": var_e}


async def main(letras):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W * N, "height": H})
        for L in letras:
            out = SAIDA / L
            out.mkdir(parents=True, exist_ok=True)
            corpo = VARS[L]() + f'<div class="faixa" style="top:0"></div><div class="faixa" style="bottom:0"></div>'
            await pg.set_content(f'<!doctype html><html><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{corpo}</body></html>')
            await pg.wait_for_load_state("networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(out / "panorama.png"))
            im = Image.open(out / "panorama.png")
            for i in range(N):
                im.crop((i * W, 0, (i + 1) * W, H)).save(out / f"adocao-{L}-{i+1:02d}.png")
            im.resize((W * N // 4, H // 4)).convert("RGB").save(out / "tira.jpg", quality=88)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or list(VARS)))
