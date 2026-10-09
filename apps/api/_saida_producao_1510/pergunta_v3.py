"""Cartão de pergunta v3 (09/10/2026): cartão refinado + recorte (pessoa ou objeto ligado à
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
.corpo { padding:40px 66px 30px; text-align:center; }
.linha { width:140px; height:2px; margin:0 auto 30px; background:linear-gradient(90deg, transparent, #C9A962, transparent); }
.q { font-family:'Playfair Display',serif; font-weight:700; color:#3B2E1D; font-size:{{ fs }}px; line-height:1.22; }
.perfil { margin:30px auto 0; display:flex; align-items:center; justify-content:center; gap:14px; padding-top:22px; border-top:1px solid rgba(184,148,63,.35); }
.av { width:52px; height:52px; border-radius:50%; object-fit:cover; object-position:50% 25%; border:2px solid #C9A962; }
.h { font-weight:700; font-size:23px; color:#2E241A; text-align:left; } .s { font-weight:500; font-size:18px; color:#6B5B3E; }
.chao { position:absolute; left:50%; bottom:20px; transform:translateX(-50%); width:620px; height:70px; border-radius:50%;
  background:radial-gradient(ellipse, rgba(90,70,30,.35) 0%, rgba(90,70,30,0) 70%); z-index:2; }
.recorte { position:absolute; left:50%; transform:translateX(-50%); bottom:0; z-index:3; max-width:880px; object-fit:contain; object-position:bottom;
  filter: drop-shadow(0 18px 30px rgba(90,70,30,.28)) contrast(.95) saturate(.92); }
</style></head><body><div class="c">
<img class="mono" src="{{ fundo }}"><div class="luz"></div><div class="moldura"></div>
<img class="logo" src="{{ logo }}">
<div class="card" id="card"><div class="topo">{{ topo }}</div>
  <div class="corpo"><div class="linha"></div><p class="q">{{ pergunta }}</p>
    <div class="perfil"><img class="av" src="{{ perfil }}"><div><div class="h">adv.leticiabarros2</div><div class="s">{{ especialidade }}</div></div></div>
  </div></div>
<div class="chao"></div>
<img class="recorte" id="rec" src="{{ recorte }}">
</div>
<script>
const card = document.getElementById('card'), rec = document.getElementById('rec');
const topo = card.getBoundingClientRect().bottom - 70;   // a cabeça passa um pouco atrás do cartão
rec.style.height = (1350 - topo) + 'px';
</script></body></html>""")

# (arquivo de saída, topo, pergunta, especialidade, recorte)
PECAS = [
    ("pergunta-pet-v3.jpg", PERGUNTA, "Meu ex ficou com o cachorro depois da separação. Eu ainda tenho algum direito sobre ele?", FAM, "pergunta-pet.png"),
    ("relato-abandono-v3.jpg", "Me conta o que aconteceu:", "Você cresceu com um pai ou mãe presente só de nome? Como isso te marcou?", FAM, "pergunta-abandono.png"),
    ("pergunta-clt-v3.jpg", PERGUNTA, "Cobri as férias de uma colega no trabalho. Eu tenho direito a receber o salário dela?", TRAB, "pergunta-clt.png"),
    ("outubro-rosa-trabalho-pergunta-v3.jpg", PERGUNTA, "Posso faltar no trabalho para fazer mamografia sem desconto no salário?", TRAB, "pergunta-outubro-rosa-trabalho.png"),
    ("cancer-inss-pergunta-v3.jpg", PERGUNTA, "Descobri um câncer de mama e só contribuí 4 meses. O INSS vai me pagar?", PREV, "pergunta-cancer-inss.png"),
    ("violencia-domestica-inss-pergunta-v3.jpg", PERGUNTA, "Tenho medida protetiva e não consigo ir trabalhar. Vou perder meu emprego?", PREV, "pergunta-violencia-domestica-inss.png"),
    ("mesario-folga-pergunta-v3.jpg", PERGUNTA, "Fui mesária na eleição. A empresa pode descontar o dia ou negar minha folga?", TRAB, "pergunta-mesario-folga.png"),
    ("plano-mamografia-pergunta-v3.jpg", PERGUNTA, "Tenho 35 anos e o plano negou minha mamografia por causa da idade. Pode?", CONS, "pergunta-plano-mamografia.png"),
    ("separacao-bens-70-pergunta-v3.jpg", PERGUNTA, "Meu pai casou aos 72 anos. A esposa dele tem direito à herança?", FAM, "pergunta-separacao-bens-70.png"),
    ("licenca-adotante-pergunta-v3.jpg", PERGUNTA, "Vou adotar uma criança de 6 anos. Tenho direito à licença-maternidade inteira?", TRAB, "pergunta-licenca-adotante.png"),
    ("penhora-salario-pergunta-v3.jpg", PERGUNTA, "Tenho uma dívida no cartão. O banco pode tirar dinheiro direto do meu salário?", CONS, "pergunta-penhora-salario.png"),
    ("bebe-pensao-morte-pergunta-v3.jpg", PERGUNTA, "Meu namorado morreu quando eu estava grávida. Meu bebê vai ter direito à pensão?", PREV, "pergunta-bebe-pensao-morte.png"),
    ("banco-encerra-conta-pergunta-v3.jpg", PERGUNTA, "O banco mandou mensagem dizendo que vai encerrar minha conta. Ele pode fazer isso?", CONS, "pergunta-banco-encerra-conta.png"),
]


async def main(filtro: set[str]) -> None:
    fundo, logo, perfil = uri(FUNDO), uri(LOGO), uri(PERFIL)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for nome, topo, pergunta, esp, rec in PECAS:
            if filtro and nome not in filtro:
                continue
            fs = 50 if len(pergunta) <= 72 else 46 if len(pergunta) <= 90 else 42
            await page.set_content(HTML.render(fundo=fundo, logo=logo, perfil=perfil, topo=topo, pergunta=pergunta,
                                               especialidade=esp, fs=fs, recorte=uri(REC / rec)), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            await page.evaluate("""() => { const c=document.getElementById('card'), r=document.getElementById('rec');
                r.style.height = (1350 - (c.getBoundingClientRect().bottom - 70)) + 'px'; }""")
            destino = AQUI / "pecas" / nome.replace(".jpg", ".png")
            await page.screenshot(path=str(destino))
            render_criativo._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(AQUI / "pecas" / nome, "JPEG", quality=92, optimize=True)
            destino.unlink()
            print("ok", nome)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
