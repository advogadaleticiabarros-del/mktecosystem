"""Pergunta v6 (09/10/2026): foto inteira com UM objeto do tema e luz real (sem recorte),
cartão de pergunta em vidro fosco sobre o degradê café, destaque dourado em itálico.
Referências da Letícia: maleta/ampulheta/papel amassado em primeiro plano, foto inteira.

Uso (de apps/api): python _saida_producao_1510/pergunta_v6.py [chave ...]
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

import carrossel_v4 as v4  # noqa: E402
from app.services import render_criativo  # noqa: E402
from pergunta_refinada import PERFIL, uri  # noqa: E402

AQUI = Path(__file__).resolve().parent
FOTOS = AQUI / "_fotos_pexels"

HTML = Template(r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600;1,700&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; } html { font-variant-numeric: lining-nums; font-feature-settings:"lnum" 1; }
.c { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif; background:#1E1814; }
.foto { position:absolute; left:0; top:430px; width:100%; height:920px; object-fit:cover; object-position:{{ pos }};
  filter: sepia(.22) saturate(.82) contrast(1.06) brightness({{ brilho }}); }
.veu { position:absolute; inset:0; background:
  linear-gradient(180deg, #1E1814 0%, #1E1814 32%, rgba(30,24,20,.7) 40%, rgba(30,24,20,.12) 54%, rgba(30,24,20,0) 66%, rgba(30,24,20,.1) 82%, rgba(30,24,20,.8) 100%); }
.luz { position:absolute; inset:0; mix-blend-mode:soft-light; background: radial-gradient(ellipse at 18% 8%, rgba(233,211,152,.55), transparent 45%); }
.grao { position:absolute; inset:0; z-index:9; opacity:.13; mix-blend-mode:overlay; background-image:url("{{ grao }}"); }
.topo { position:absolute; top:84px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:4;
  font-size:22px; font-weight:600; letter-spacing:5px; text-transform:uppercase; line-height:1.35; color:#E8DED1; }
.topo .d { text-align:right; color:#C9A962; }
.card { position:absolute; left:50%; top:196px; transform:translateX(-50%); width:880px; z-index:5; border-radius:26px; overflow:hidden;
  background: rgba(36,29,24,.58); backdrop-filter: blur(22px) saturate(1.1); border:1.5px solid rgba(201,169,98,.62);
  box-shadow: 0 30px 70px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,240,200,.18); }
.faixa { background: linear-gradient(180deg, #EBDBAE 0%, #D4BC7D 45%, #C9A962 100%); text-align:center; padding:16px 0;
  font-size:23px; font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#3B2E1D; }
.corpo { padding:44px 64px 40px; text-align:center; }
.q { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:{{ fs }}px; line-height:1.14; color:#FAF6F0; }
.q em { font-style:italic; color:#E2C77F; }
.perfil { margin-top:34px; padding-top:24px; border-top:1px solid rgba(201,169,98,.35); display:flex; align-items:center; justify-content:center; gap:14px; }
.av { width:54px; height:54px; border-radius:50%; object-fit:cover; object-position:50% 25%; border:2px solid #C9A962; }
.h { font-weight:700; font-size:23px; color:#FAF6F0; text-align:left; } .s { font-weight:500; font-size:22px; color:#C9A962; text-align:left; }
.cta { position:absolute; left:50%; bottom:92px; transform:translateX(-50%); z-index:5; white-space:nowrap;
  font-size:22px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#FAF6F0;
  padding:14px 30px; border-radius:999px; border:1.5px solid rgba(201,169,98,.8); background:rgba(30,24,20,.55); backdrop-filter:blur(10px); }
.cta b { color:#C9A962; }
</style></head><body><div class="c">
<img class="foto" src="{{ foto }}"><div class="veu"></div><div class="luz"></div>
<div class="topo"><div>Letícia Barros<br>Advocacia</div><div class="d">{{ area1 }}<br>{{ area2 }}</div></div>
<div class="card"><div class="faixa">{{ topo }}</div>
  <div class="corpo"><p class="q">{{ pergunta }}</p>
    <div class="perfil"><img class="av" src="{{ perfil }}"><div><div class="h">adv.leticiabarros2</div><div class="s">Advogada · {{ area_curta }}</div></div></div>
  </div></div>
<div class="cta">A resposta está na <b>legenda</b></div>
<div class="grao"></div>
</div></body></html>""")

PERG = "Me faça uma pergunta"
CONS, TRAB, PREV, FAM = ("Direito do", "Consumidor"), ("Direito", "Trabalhista"), ("Direito", "Previdenciário"), ("Direito de", "Família")
# chave: (arquivo, foto Pexels, enquadramento, brilho, faixa do cartão, pergunta, área)
PECAS = {
    "penhora-salario": ("penhora-salario-pergunta-v6.jpg", 8719576, "50% 45%", .9, PERG,
        "Tenho uma dívida no cartão. O banco pode <em>tirar dinheiro direto do meu salário?</em>", CONS),
    "banco-encerra-conta": ("banco-encerra-conta-pergunta-v6.jpg", 6969809, "50% 62%", .95, PERG,
        "O banco avisou que vai encerrar minha conta. <em>Ele pode fazer isso?</em>", CONS),
    "bebe-pensao-morte": ("bebe-pensao-morte-pergunta-v6.jpg", 35119986, "50% 32%", .95, PERG,
        "Meu namorado morreu quando eu estava grávida. <em>Meu bebê tem direito à pensão?</em>", PREV),
    "cancer-inss": ("cancer-inss-pergunta-v6.jpg", 5482984, "50% 28%", .9, PERG,
        "Descobri um câncer de mama e só contribuí 4 meses. <em>O INSS vai me pagar?</em>", PREV),
    "licenca-adotante": ("licenca-adotante-pergunta-v6.jpg", 6338775, "50% 45%", .92, PERG,
        "Vou adotar uma criança de 6 anos. <em>Tenho direito à licença-maternidade inteira?</em>", TRAB),
    "mesario-folga": ("mesario-folga-pergunta-v6.jpg", 29509519, "30% 60%", .9, PERG,
        "Fui mesária na eleição. <em>A empresa pode descontar o dia ou negar minha folga?</em>", TRAB),
    "outubro-rosa-trabalho": ("outubro-rosa-trabalho-pergunta-v6.jpg", 5483009, "50% 55%", .95, PERG,
        "Posso faltar no trabalho para fazer mamografia <em>sem desconto no salário?</em>", TRAB),
    "plano-mamografia": ("plano-mamografia-pergunta-v6.jpg", 6753425, "50% 50%", .82, PERG,
        "Tenho 35 anos e o plano negou minha mamografia por causa da idade. <em>Pode?</em>", CONS),
    "separacao-bens-70": ("separacao-bens-70-pergunta-v6.jpg", 8790972, "50% 68%", .92, PERG,
        "Meu pai casou aos 72 anos. <em>A esposa dele tem direito à herança?</em>", FAM),
    "violencia-domestica-inss": ("violencia-domestica-inss-pergunta-v6.jpg", 29894792, "50% 26%", 1.18, PERG,
        "Tenho medida protetiva e não consigo trabalhar. <em>Vou perder meu emprego?</em>", PREV),
    "abandono": ("relato-abandono-v6.jpg", 34393435, "50% 30%", .95, "Me conta o que aconteceu",
        "Você cresceu com um pai ou mãe presente só de nome? <em>Como isso te marcou?</em>", FAM),
    "clt": ("pergunta-clt-v6.jpg", 14792097, "45% 62%", .92, PERG,
        "Cobri as férias de uma colega. <em>Tenho direito a receber o salário dela?</em>", TRAB),
}


async def main(filtro: set[str]) -> None:
    perfil = uri(PERFIL)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for chave, (nome, foto, pos, brilho, topo, pergunta, area) in PECAS.items():
            if filtro and chave not in filtro:
                continue
            n = len(pergunta) - 9
            fs = 62 if n <= 70 else 58 if n <= 85 else 54
            curta = area[1]
            await page.set_content(HTML.render(foto=uri(FOTOS / f"{foto}.jpg"), pos=pos, brilho=brilho, topo=topo, pergunta=pergunta,
                                               area1=area[0], area2=area[1], area_curta=curta, fs=fs, perfil=perfil, grao=v4.GRAO),
                                   wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            destino = AQUI / "pecas" / nome.replace(".jpg", ".png")
            await page.screenshot(path=str(destino))
            render_criativo._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(AQUI / "pecas" / nome, "JPEG", quality=92, optimize=True)
            destino.unlink()
            print("ok", nome)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
