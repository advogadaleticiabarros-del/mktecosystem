"""Cartão de pergunta refinado (feed 1080×1350), pedido da Letícia em 08/10/2026:
mesma identidade (fundo com monograma, logo circular, cartão creme com cabeçalho
dourado, identificação do perfil), com fundo menos granulado, moldura fina,
sombras suaves e mais respiro. Foto de perfil = foto real do Instagram.

Uso (de apps/api): python _saida_producao_1510/pergunta_refinada.py
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

AQUI = Path(__file__).resolve().parent
FUNDO = Path("C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/ementos rdape dourado/use esse fundo.png")
LOGO = Path("C:/Users/prosy/Desktop/PROJETOS/modelo-visual-site/assets/logo/logo-800x800.png")
PERFIL = AQUI / "perfil-instagram.jpg"


def uri(p: Path) -> str:
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


HTML = Template("""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
.c { width:1080px; height:1350px; position:relative; overflow:hidden; font-family:'Inter',sans-serif;
  background: radial-gradient(ellipse at 50% 18%, #FDF9F0 0%, #F4EBD7 48%, #E8DABD 100%); }
.mono { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.5;
  filter: blur(1.4px) saturate(.85) contrast(.82) brightness(1.08); }
.luz { position:absolute; inset:0; background:
  linear-gradient(115deg, transparent 30%, rgba(255,255,255,.35) 48%, transparent 62%),
  radial-gradient(ellipse at 50% 40%, rgba(255,251,242,.55) 0%, transparent 60%); }
.moldura { position:absolute; inset:40px; border:1.5px solid rgba(184,148,63,.55); border-radius:22px; }
.conteudo { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:0; padding:0 120px; }
.logo { width:168px; height:168px; border-radius:50%; margin-bottom:64px;
  filter: drop-shadow(0 3px 6px rgba(120,90,35,.35)) drop-shadow(0 16px 30px rgba(120,90,35,.22)); }
.card { width:840px; border-radius:24px; overflow:hidden; background:#FFFCF6;
  border:1.5px solid rgba(184,148,63,.65);
  box-shadow: 0 2px 6px rgba(90,70,30,.10), 0 22px 48px rgba(90,70,30,.16); }
.topo { background: linear-gradient(180deg, #EBDBAE 0%, #D4BC7D 45%, #C9A962 100%);
  border-bottom:1px solid rgba(168,134,63,.55);
  text-align:center; padding:24px 32px; font-family:'Playfair Display',serif; font-weight:700; font-size:31px;
  color:#3B2E1D; letter-spacing:.3px; }
.corpo { padding:52px 70px 64px; text-align:center; }
.linha { width:140px; height:2px; margin:0 auto 40px; background:linear-gradient(90deg, transparent, #C9A962, transparent); }
.q { font-family:'Playfair Display',serif; font-weight:700; color:#3B2E1D; font-size:{{ fs }}px; line-height:1.24; }
.perfil { margin-top:48px; display:inline-flex; align-items:center; gap:18px; padding:12px 30px 12px 12px;
  background:rgba(255,252,246,.94); border:1.5px solid rgba(201,169,98,.7); border-radius:999px;
  box-shadow: 0 8px 22px rgba(90,70,30,.12); }
.av { width:70px; height:70px; border-radius:50%; object-fit:cover; object-position:50% 25%; border:2px solid #C9A962; }
.h { font-weight:700; font-size:25px; color:#2E241A; }
.s { font-weight:500; font-size:18px; color:#6B5B3E; margin-top:3px; }
</style></head><body><div class="c">
<img class="mono" src="{{ fundo }}"><div class="luz"></div><div class="moldura"></div>
<div class="conteudo">
  <img class="logo" src="{{ logo }}">
  <div class="card"><div class="topo">{{ topo }}</div>
    <div class="corpo"><div class="linha"></div><p class="q">{{ pergunta }}</p></div></div>
  <div class="perfil"><img class="av" src="{{ perfil }}"><div><div class="h">adv.leticiabarros2</div><div class="s">{{ especialidade }}</div></div></div>
</div></div></body></html>""")

FAM = "Advogada | Letícia Barros | Direito de Família"
TRAB = "Advogada | Letícia Barros | Direito Trabalhista"
PREV = "Advogada | Letícia Barros | Direito Previdenciário"
CONS = "Advogada | Letícia Barros | Direito do Consumidor"
PERGUNTA = "Me faça uma pergunta:"

# (arquivo de saída, topo, pergunta, especialidade)
PECAS = [
    ("pergunta-pet-v2.jpg", PERGUNTA, "Meu ex ficou com o cachorro depois da separação. Eu ainda tenho algum direito sobre ele?", FAM),
    ("relato-abandono-v2.jpg", "Me conta o que aconteceu:", "Você cresceu com um pai ou mãe presente só de nome? Como isso te marcou?", FAM),
    ("pergunta-clt-v2.jpg", PERGUNTA, "Cobri as férias de uma colega no trabalho. Eu tenho direito a receber o salário dela?", TRAB),
    ("outubro-rosa-trabalho-pergunta-v2.jpg", PERGUNTA, "Posso faltar no trabalho para fazer mamografia sem desconto no salário?", TRAB),
    ("cancer-inss-pergunta-v2.jpg", PERGUNTA, "Descobri um câncer de mama e só contribuí 4 meses. O INSS vai me pagar?", PREV),
    ("violencia-domestica-inss-pergunta-v2.jpg", PERGUNTA, "Tenho medida protetiva e não consigo ir trabalhar. Vou perder meu emprego?", PREV),
    ("mesario-folga-pergunta-v2.jpg", PERGUNTA, "Fui mesária na eleição. A empresa pode descontar o dia ou negar minha folga?", TRAB),
    ("plano-mamografia-pergunta-v2.jpg", PERGUNTA, "Tenho 35 anos e o plano negou minha mamografia por causa da idade. Pode?", CONS),
    ("separacao-bens-70-pergunta-v2.jpg", PERGUNTA, "Meu pai casou aos 72 anos. A esposa dele tem direito à herança?", FAM),
    ("licenca-adotante-pergunta-v2.jpg", PERGUNTA, "Vou adotar uma criança de 6 anos. Tenho direito à licença-maternidade inteira?", TRAB),
    ("penhora-salario-pergunta-v2.jpg", PERGUNTA, "Tenho uma dívida no cartão. O banco pode tirar dinheiro direto do meu salário?", CONS),
    ("bebe-pensao-morte-pergunta-v2.jpg", PERGUNTA, "Meu namorado morreu quando eu estava grávida. Meu bebê vai ter direito à pensão?", PREV),
    ("banco-encerra-conta-pergunta-v2.jpg", PERGUNTA, "O banco mandou mensagem dizendo que vai encerrar minha conta. Ele pode fazer isso?", CONS),
]


async def main(filtro: set[str]) -> None:
    (AQUI / "_png").mkdir(exist_ok=True)
    fundo, logo, perfil = uri(FUNDO), uri(LOGO), uri(PERFIL)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for nome, topo, pergunta, esp in PECAS:
            if filtro and nome not in filtro:
                continue
            fs = 60 if len(pergunta) <= 72 else 54 if len(pergunta) <= 90 else 48
            await page.set_content(HTML.render(fundo=fundo, logo=logo, perfil=perfil, topo=topo, pergunta=pergunta,
                                               especialidade=esp, fs=fs), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            png = AQUI / "_png" / nome.replace(".jpg", ".png")
            await page.screenshot(path=str(png))
            render_criativo._aplicar_acabamento_dourado(str(png))
            Image.open(png).convert("RGB").save(AQUI / "pecas" / nome, "JPEG", quality=92, optimize=True)
            print("ok", nome)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
