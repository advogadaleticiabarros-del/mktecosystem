"""Carrossel cômico (capa com foto do tema e fechamento com retrato inteiro, sem recorte) "Guia de sobrevivência com pensão de R$ 300" (10/10/2026).

Releitura do guia de agosto/2025 (8 slides em papel bege) na linguagem do carrossel v5:
capa escura com a Letícia, slides de papel, cupom fiscal como piada visual em cada gasto,
conta final, slide salvável "agora sem piada" (Código Civil, arts. 1.694, 1.699 e 1.703)
e fechamento com CTA impessoal. Valores aproximados de outubro/2026.

Uso (de apps/api): python _saida_producao_1510/pensao300.py
"""
import asyncio
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

import capa_fecho  # noqa: E402
import carrossel_v4 as v4  # noqa: E402
from app.services import render_criativo  # noqa: E402

AQUI = Path(__file__).resolve().parent
CSS_V4 = re.search(r"<style>(.*?)</style>", (AQUI / "carrossel_v4.py").read_text(encoding="utf-8"), re.S).group(1)
TOTAL = 8
AREA = "Direito de Família"

CUPONS = [
    {"num": "01", "titulo": "Mercado <em>do mês</em>", "loja": "SUPERMERCADO DA VIDA REAL", "fundo": "claro",
     "itens": [("Arroz 5 kg", 27), ("Feijão 2 kg", 16), ("Leite 12 L", 66), ("Frango 3 kg", 54), ("Ovos 30 un", 24),
               ("Frutas do mês", 60), ("Iogurte e biscoito", 40), ("Higiene", 45)],
     "piada": "A pensão acabou no corredor <em>do iogurte</em>."},
    {"num": "02", "titulo": "A casa <em>dela</em>", "loja": "CONTAS DA CASA · PARTE DA CRIANÇA", "fundo": "escuro",
     "itens": [("Aluguel (o quarto dela)", 350), ("Luz (o desenho)", 90), ("Água (banho de 40 min)", 35),
               ("Gás", 40), ("Internet (dever de casa)", 50)],
     "piada": "Ela não aceitou dividir o quarto <em>com o cachorro</em>."},
    {"num": "03", "titulo": "Roupas e <em>calçados</em>", "loja": "MODA INFANTIL · CRESCE RÁPIDO", "fundo": "claro",
     "itens": [("Tênis (serve até março)", 160), ("Calça", 90), ("3 camisetas", 75), ("Uniforme da escola", 60)],
     "piada": "A criança cresce. <em>A pensão, não.</em>"},
    {"num": "04", "titulo": "Escola, saúde <em>e festa</em>", "loja": "DESPESAS QUE NINGUÉM LEMBRA", "fundo": "claro",
     "itens": [("Material escolar (média)", 60), ("Passagem de ônibus", 110), ("Farmácia", 70),
               ("Curativo de unicórnio", 15), ("Dia das Crianças", 50)],
     "piada": "Curativo comum não cura. <em>Tem que ser de unicórnio.</em>"},
]
PENSAO = 300


def reais(v: int) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


HTML = Template(r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
<style>
{{ css_v4 }}
{{ css_capa }}
body { width:1080px; height:1350px; }
.s { left:0; }
/* cupom fiscal: a piada visual */
.cupom { position:absolute; left:50%; width:720px; z-index:5; background:#FCFAF5; color:#2B231C; font-family:'Courier Prime',monospace;
  padding:40px 48px 44px; box-shadow:0 30px 60px rgba(35,30,26,.30);
  -webkit-mask: conic-gradient(from -45deg at bottom, #0000, #000 1deg 89deg, #0000 90deg) bottom/28px 51% repeat-x,
                conic-gradient(from 135deg at top, #0000, #000 1deg 89deg, #0000 90deg) top/28px 51% repeat-x; }
.cupom::after { content:''; position:absolute; inset:0; background-image:url("{{ ruido }}"); opacity:.10; mix-blend-mode:multiply; }
.cupom .loja { text-align:center; font-weight:700; font-size:26px; letter-spacing:1px; }
.cupom .sub { text-align:center; font-size:22px; margin-top:4px; opacity:.75; }
.cupom .tr { border-top:2px dashed #2B231C80; margin:18px 0; }
.cupom .it { display:flex; align-items:baseline; font-size:29px; line-height:1.55; }
.cupom .it .n { white-space:nowrap; }
.cupom .it .p { flex:1; border-bottom:2px dotted #2B231C55; margin:0 10px; transform:translateY(-8px); }
.cupom .it .v { white-space:nowrap; }
.cupom .tot { display:flex; justify-content:space-between; font-weight:700; font-size:34px; }
.cupom .tot.s2 { font-weight:400; font-size:29px; margin-top:6px; }
.cupom .tot.neg { margin-top:6px; font-size:31px; }
.cupom .tot.neg span:last-child { background:#2B231C; color:#FCFAF5; padding:0 10px; }
.cupom .obs { text-align:center; font-size:22px; margin-top:16px; opacity:.7; }
.piada { position:absolute; left:84px; right:84px; text-align:center; text-wrap:balance; font-family:'EB Garamond',serif; font-style:italic; font-weight:600; font-size:50px; line-height:1.12; z-index:5; }
.claro .piada em { font-style:italic; border-bottom:3px solid #C9A962; }
.escuro .piada { color:#FAF6F0; } .escuro .piada em { color:#C9A962; font-style:italic; }
.linha-tit { position:absolute; left:84px; right:84px; top:168px; display:flex; align-items:baseline; gap:26px; z-index:5; }
.linha-tit .num { font-size:104px; }
.linha-tit .tit { font-size:76px; margin:0; }
.chk { list-style:none; margin-top:34px; }
.chk li { position:relative; padding-left:58px; font-size:33px; line-height:1.4; margin-bottom:22px; color:#3D2B1F; }
.chk li::before { content:''; position:absolute; left:0; top:8px; width:30px; height:30px; border:2.5px solid #B8943F; border-radius:6px; }
.chk li b { color:#231E1A; }
.ref { display:inline-block; font-size:22px; font-weight:700; letter-spacing:1px; padding:10px 18px; border-radius:4px; background:#231E1A; color:#E8DED1; }
.conta { position:absolute; left:84px; right:84px; top:330px; z-index:5; }
.conta .lin { display:flex; justify-content:space-between; align-items:baseline; padding:26px 0; border-bottom:1px solid #C9A96266; }
.conta .lin span:first-child { font-size:30px; font-weight:600; letter-spacing:4px; text-transform:uppercase; color:#E8DED1cc; }
.conta .lin span:last-child { font-family:'EB Garamond',serif; font-weight:700; font-size:92px; line-height:1; color:#FAF6F0; }
.conta .lin.falta { border-bottom:none; }
.conta .lin.falta span:last-child { color:#C9A962; font-size:124px; }
</style></head><body><div class="pano">
{% if slide == 1 %}
{{ capa_html }}
{% elif cupom %}
<div class="s {{ cupom.fundo }} textura">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Pensão de R$ 300</span></div>
  <div class="linha-tit"><div class="num">{{ cupom.num }}</div><div class="tit">{{ cupom.titulo }}</div></div>
  <div class="cupom" style="top:{{ topo_cupom }}px; transform:translateX(-50%) rotate({{ giro }}deg);">
    <div class="loja">{{ cupom.loja }}</div><div class="sub">CUPOM NÃO FISCAL · 10/2026</div>
    <div class="tr"></div>
    {% for nome, valor in cupom.itens %}<div class="it"><span class="n">{{ nome }}</span><span class="p"></span><span class="v">{{ reais(valor) }}</span></div>{% endfor %}
    <div class="tr"></div>
    <div class="tot"><span>TOTAL</span><span>{{ reais(total_cupom) }}</span></div>
    <div class="tot s2"><span>PENSÃO</span><span>{{ reais(pensao_cupom) }}</span></div>
    <div class="tot neg"><span>SALDO</span><span>- {{ reais(total_cupom - pensao_cupom) }}</span></div>
    <div class="obs">{{ '*a pensão acabou no mercado' if pensao_cupom == 0 else '*valores aproximados' }}</div>
  </div>
  <div class="piada" style="bottom:200px;">{{ cupom.piada }}</div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">{{ '%02d' % slide }} / {{ total }}</span></div>
</div>
{% elif slide == 6 %}
<div class="s escuro textura">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>A conta do mês</span></div>
  <div class="bloco" style="top:170px;"><div class="tit" style="font-size:84px;">A conta <em>final</em></div></div>
  <div class="conta">
    <div class="lin"><span>Gastos do mês</span><span>{{ reais(gastos) }}</span></div>
    <div class="lin"><span>Pensão</span><span>{{ reais(pensao) }}</span></div>
    <div class="lin falta"><span>Falta</span><span>{{ reais(gastos - pensao) }}</span></div>
  </div>
  <div class="piada" style="bottom:300px;">Parabéns: você acaba de se formar <em>em mágica</em>.</div>
  <div style="position:absolute; left:84px; right:84px; bottom:200px; text-align:center; font-size:30px; color:#E8DED1; z-index:5;">E a diferença, <span class="mt">adivinha quem paga?</span></div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">06 / {{ total }}</span></div>
</div>
{% elif slide == 7 %}
<div class="s claro textura">
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>{{ area }}</span></div>
  <div class="bloco" style="top:150px; right:84px;">
    <div class="selo" style="margin-top:0;">✦ Salve para conferir</div>
    <div class="tit" style="font-size:80px; margin-top:34px;">Agora, <em>sem piada</em>:<br>o que a lei diz</div>
    <ul class="chk">
      <li>A pensão olha a <b>necessidade da criança</b> e a <b>possibilidade de quem paga</b>.</li>
      <li>Os dois genitores contribuem, <b>cada um na proporção do que ganha</b>.</li>
      <li>A situação mudou? A lei prevê <b>pedido de revisão</b>.</li>
      <li>Pensão combinada de boca não dá segurança. <b>Formalizada, pode ser cobrada.</b></li>
    </ul>
    <div class="ref">Código Civil, arts. 1.694, 1.699 e 1.703</div>
    <div style="font-size:26px; color:#3D2B1F; margin-top:22px;">Cada caso tem detalhes.</div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">07 / {{ total }}</span></div>
</div>
{% else %}
{{ fecho_html }}
{% endif %}
<div class="fosco grao"></div><div class="fosco veu"></div>
</div></body></html>""")


async def main() -> None:
    gastos = sum(v for c in CUPONS for _n, v in c["itens"])
    comum = dict(css_v4=CSS_V4.replace("{{ ruido }}", v4.RUIDO).replace("{{ fibra }}", v4.FIBRA)
                 .replace("{{ mancha }}", v4.MANCHA).replace("{{ grao }}", v4.GRAO),
                 ruido=v4.RUIDO, total=f"{TOTAL:02d}", area=AREA, pensao=PENSAO, gastos=gastos, reais=reais,
                 css_capa=capa_fecho.CSS + capa_fecho.CSS_OURO,
                 capa_html=capa_fecho.capa_ouro(
                     capa_fecho.enquadrar(AQUI / "_fotos_pexels" / "original-pensao300.jpg"), area="Pensão alimentícia",
                     kicker="Pensão de R$ 300", titulo="Guia de<br>sobrevivência", subtitulo="para mães que fazem milagre",
                     apoio='Fizemos as contas do mês.<br><span class="co-mt">Spoiler: não fecha.</span>', total=f"{TOTAL:02d}"),
                 fecho_html=capa_fecho.fecho(
                     "estudio-livros", area=AREA, titulo="A piada acaba aqui. A conta, <em>não</em>.",
                     sub="Ninguém deveria fazer milagre sozinha.",
                     apoio='<span class="mt">Salve este post</span> e mande para a amiga que faz milagre todo mês.'))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for slide in range(1, TOTAL + 1):
            cupom = CUPONS[slide - 2] if 2 <= slide <= 5 else None
            extra = {}
            if cupom:
                n = len(cupom["itens"])
                extra = dict(total_cupom=sum(v for _n, v in cupom["itens"]), pensao_cupom=PENSAO if slide == 2 else 0, giro=(-1.6 if slide % 2 else 1.4),
                             topo_cupom=330 if n > 6 else 360)
            await page.set_content(HTML.render(slide=slide, cupom=cupom, **comum, **extra), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            destino = AQUI / "pecas" / f"pensao300-{slide}.png"
            await page.evaluate("""() => { const el = document.getElementById('big'); if (!el) return; let fs = 150; el.style.fontSize = fs + 'px';
                while (el.offsetWidth > 620 && fs > 70) { fs -= 2; el.style.fontSize = fs + 'px'; } }""")
            await page.screenshot(path=str(destino))
            render_criativo._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(destino.with_suffix(".jpg"), "JPEG", quality=93, optimize=True)
            destino.unlink()
            print("ok", slide)
        await browser.close()
    print("gastos", gastos, "falta", gastos - PENSAO)


if __name__ == "__main__":
    asyncio.run(main())
