"""Cartão de pergunta v4 (refeito após revisão) (09/10/2026): cartão refinado + recorte (pessoa ou objeto ligado à
pergunta) ocupando do cartão até o rodapé, centralizado para sobreviver ao corte 3:4 da
grade do perfil. Identificação da Letícia dentro do cartão. Faixas douradas mantidas.

Uso (de apps/api): python _saida_producao_1510/pergunta_v3.py [arquivo ...]
"""
import asyncio
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo  # noqa: E402
from pergunta_refinada import FAM, PERGUNTA, PREV, TRAB, CONS, FUNDO, LOGO, PERFIL, uri  # noqa: E402

AQUI = Path(__file__).resolve().parent
REC = AQUI / "_recortes"

HTML = Template("""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; } html { font-variant-numeric: lining-nums; }
.c { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif;
  background: radial-gradient(ellipse at 50% 18%, #FDF9F0 0%, #F4EBD7 48%, #E8DABD 100%); }
.mono { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.45; filter: blur(1.4px) saturate(.85) contrast(.82) brightness(1.08); }
.luz { position:absolute; inset:0; background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.35) 48%, transparent 62%); }
.moldura { position:absolute; inset:40px; border:1.5px solid rgba(184,148,63,.55); border-radius:22px; z-index:6; }
.logo { position:absolute; left:50%; top:72px; transform:translateX(-50%); width:118px; height:118px; z-index:5;
  filter: drop-shadow(0 3px 6px rgba(120,90,35,.35)) drop-shadow(0 12px 24px rgba(120,90,35,.2)); }
.card { position:absolute; left:50%; top:222px; transform:translateX(-50%); width:840px; border-radius:24px; overflow:hidden; background:#FFFCF6; z-index:4;
  border:1.5px solid rgba(184,148,63,.65); box-shadow: 0 2px 6px rgba(90,70,30,.10), 0 26px 52px rgba(90,70,30,.20); }
.topo { background: linear-gradient(180deg, #EBDBAE 0%, #D4BC7D 45%, #C9A962 100%); border-bottom:1px solid rgba(168,134,63,.55);
  text-align:center; padding:20px 32px; font-family:'Playfair Display',serif; font-weight:700; font-size:30px; color:#3B2E1D; }
.corpo { padding:40px 66px 74px; text-align:center; }
.linha { width:140px; height:2px; margin:0 auto 30px; background:linear-gradient(90deg, transparent, #C9A962, transparent); }
.q { font-family:'Playfair Display',serif; font-weight:700; color:#3B2E1D; font-size:{{ fs }}px; line-height:1.22; }
.perfil { margin:30px auto 0; display:flex; align-items:center; justify-content:center; gap:14px; padding-top:22px; border-top:1px solid rgba(184,148,63,.35); }
.av { width:52px; height:52px; border-radius:50%; object-fit:cover; object-position:50% 25%; border:2px solid #C9A962; }
.h { font-weight:700; font-size:23px; color:#2E241A; text-align:left; } .s { font-weight:500; font-size:18px; color:#6B5B3E; }
.palco { position:absolute; left:0; right:0; bottom:0; z-index:7; pointer-events:none; }
.item { position:absolute; bottom:78px; transform-origin:50% 100%;
  filter: contrast(.96) saturate(.86) sepia(.10) brightness(1.02) drop-shadow(0 22px 26px rgba(70,52,25,.30)) drop-shadow(0 4px 6px rgba(70,52,25,.25)); }
.sombra { position:absolute; bottom:58px; height:46px; border-radius:50%; z-index:6;
  background:radial-gradient(ellipse, rgba(70,52,25,.42) 0%, rgba(70,52,25,0) 70%); }
.chao { position:absolute; left:120px; right:120px; bottom:76px; height:1.5px; z-index:5;
  background:linear-gradient(90deg, transparent, rgba(184,148,63,.55), transparent); }
.grao { position:absolute; inset:0; z-index:8; opacity:.10; mix-blend-mode:overlay; pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.4' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>"); }
</style></head><body><div class="c">
<img class="mono" src="{{ fundo }}"><div class="luz"></div><div class="moldura"></div>
<img class="logo" src="{{ logo }}">
<div class="card" id="card"><div class="topo">{{ topo }}</div>
  <div class="corpo"><div class="linha"></div><p class="q">{{ pergunta }}</p>
    <div class="perfil"><img class="av" src="{{ perfil }}"><div><div class="h">adv.leticiabarros2</div><div class="s">{{ especialidade }}</div></div></div>
  </div></div>
<div class="chao"></div>
<div class="palco" id="palco">
{% for it in itens %}<div class="sombra" style="left:calc({{ it.x }}% - {{ it.sw }}px); width:{{ it.sw * 2 }}px;"></div>
<img class="item" src="{{ it.src }}" data-f="{{ it.f }}" style="left:{{ it.x }}%; max-width:{{ it.maxw }}px; object-fit:contain; transform:translateX(-50%) rotate({{ it.rot }}deg); z-index:{{ 10 + loop.index }};">
{% endfor %}</div>
<div class="grao"></div>
</div>
<script>

</script></body></html>""")

# Composição: (arquivo, fração da altura livre, posição x em %, rotação, largura máx., meia-largura da sombra)
C = lambda f, h, x, r=0, w=620, sw=170: {"arq": f, "f": h, "x": x, "rot": r, "maxw": w, "sw": sw}
PECAS = [
    ("pergunta-pet-v4.jpg", PERGUNTA, "Meu ex ficou com o cachorro depois da separação. Eu ainda tenho algum direito sobre ele?", FAM,
     [C("obj-cachorro.png", 1.0, 50, 0, 640, 230)]),
    ("relato-abandono-v4.jpg", "Me conta o que aconteceu:", "Você cresceu com um pai ou mãe presente só de nome? Como isso te marcou?", FAM,
     [C("obj-ursinho2.png", .86, 50, -3, 640, 230)]),
    ("pergunta-clt-v4.jpg", PERGUNTA, "Cobri as férias de uma colega no trabalho. Eu tenho direito a receber o salário dela?", TRAB,
     [C("obj-cadeira.png", 1.0, 50, 0, 600, 220)]),
    ("outubro-rosa-trabalho-pergunta-v4.jpg", PERGUNTA, "Posso faltar no trabalho para fazer mamografia sem desconto no salário?", TRAB,
     [C("obj-atestado-rosa.png", .55, 40, -8, 560, 200), C("corte-laco.png", .95, 66, 6, 330, 110)]),
    ("cancer-inss-pergunta-v4.jpg", PERGUNTA, "Descobri um câncer de mama e só contribuí 4 meses. O INSS vai me pagar?", PREV,
     [C("corte-pasta.png", .9, 40, -6, 420, 150), C("corte-laco.png", .9, 64, 8, 320, 110)]),
    ("violencia-domestica-inss-pergunta-v4.jpg", PERGUNTA, "Tenho medida protetiva e não consigo ir trabalhar. Vou perder meu emprego?", PREV,
     [C("corte-pasta.png", .92, 42, -6, 420, 150), C("corte-chaves.png", .26, 66, 10, 400, 160)]),
    ("mesario-folga-pergunta-v4.jpg", PERGUNTA, "Fui mesária na eleição. A empresa pode descontar o dia ou negar minha folga?", TRAB,
     [C("corte-reais.png", .5, 38, -8, 520, 200), C("corte-carimbo.png", .88, 66, 0, 360, 130)]),
    ("plano-mamografia-pergunta-v4.jpg", PERGUNTA, "Tenho 35 anos e o plano negou minha mamografia por causa da idade. Pode?", CONS,
     [C("corte-laco2.png", .75, 36, -4, 460, 150), C("corte-estetoscopio.png", .5, 62, 4, 540, 190)]),
    ("separacao-bens-70-pergunta-v4.jpg", PERGUNTA, "Meu pai casou aos 72 anos. A esposa dele tem direito à herança?", FAM,
     [C("obj-envelope.png", .62, 40, -8, 540, 210), C("corte-chaves.png", .28, 68, 10, 400, 160)]),
    ("licenca-adotante-pergunta-v4.jpg", PERGUNTA, "Vou adotar uma criança de 6 anos. Tenho direito à licença-maternidade inteira?", TRAB,
     [C("obj-mae-filha.png", 1.0, 50, 0, 640, 240)]),
    ("penhora-salario-pergunta-v4.jpg", PERGUNTA, "Tenho uma dívida no cartão. O banco pode tirar dinheiro direto do meu salário?", CONS,
     [C("corte-reais.png", .5, 40, -8, 520, 200), C("corte-cartao.png", .85, 64, 6, 380, 130)]),
    ("bebe-pensao-morte-pergunta-v4.jpg", PERGUNTA, "Meu namorado morreu quando eu estava grávida. Meu bebê vai ter direito à pensão?", PREV,
     [C("corte-ultrassom.png", 1.0, 38, -10, 380, 130), C("corte-sapatinho.png", .45, 64, 0, 420, 160)]),
    ("banco-encerra-conta-pergunta-v4.jpg", PERGUNTA, "O banco mandou mensagem dizendo que vai encerrar minha conta. Ele pode fazer isso?", CONS,
     [C("corte-cofrinho.png", .7, 40, 0, 460, 190), C("corte-cartao.png", .8, 66, 8, 380, 130)]),
]


async def main(filtro: set[str]) -> None:
    fundo, logo, perfil = uri(FUNDO), uri(LOGO), uri(PERFIL)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for nome, topo, pergunta, esp, comp in PECAS:
            if filtro and nome not in filtro:
                continue
            fs = 50 if len(pergunta) <= 72 else 46 if len(pergunta) <= 90 else 42
            itens = [dict(c, src=uri(REC / c["arq"])) for c in comp]
            await page.set_content(HTML.render(fundo=fundo, logo=logo, perfil=perfil, topo=topo, pergunta=pergunta,
                                               especialidade=esp, fs=fs, itens=itens), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            # altura livre: da borda do cartão (sobrepondo 50 px, em primeiro plano) até a linha do chão
            await page.evaluate("""() => { const c = document.getElementById('card').getBoundingClientRect().bottom;
                const livre = (1350 - 78) - (c - 50);
                document.querySelectorAll('.item').forEach(el => { el.style.height = (livre * parseFloat(el.dataset.f)) + 'px'; }); }""")
            destino = AQUI / "pecas" / nome.replace(".jpg", ".png")
            await page.screenshot(path=str(destino))
            render_criativo._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(AQUI / "pecas" / nome, "JPEG", quality=92, optimize=True)
            destino.unlink()
            print("ok", nome)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
