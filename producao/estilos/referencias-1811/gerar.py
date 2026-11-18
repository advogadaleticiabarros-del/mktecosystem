"""Referências de 18/11/2026: 16 criativos de outros perfis que a Jessica mandou, adaptados aos assuntos da Dra. Letícia.
Cada função segue a estrutura de uma referência (composição, hierarquia, destaque), com as nossas cores, letras e as
faixas douradas. Nada de logo, nome ou texto das referências. Motor e acabamento: ../manchete/gerar.py.
Uso: python gerar.py [prefixo]. Grava em pecas/ (fora do git). Nunca sobrescreva peça pronta: versão nova = nome novo."""
import asyncio
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "manchete"))
from gerar import ACAB, AREIA, BANCO, CAFE, DRA, FOIL, FUNDO, MARCA, PAPEL, PERFIL, RAIZ, foto  # noqa: E402

FOTOS = AQUI / "fotos"
SAIDA = AQUI / "pecas"
PERFIL_IMG = RAIZ / "apps" / "api" / "_saida_producao_1510" / "perfil-instagram.jpg"
OURO_CLARO = "#e8d08a"
BASE = f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Playfair+Display:ital,wght@0,500;1,400;1,500&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel=stylesheet>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
.c{{width:1080px;height:1440px;position:relative;overflow:hidden;color:{CAFE};font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
.abs{{position:absolute}}
.g{{font-family:'EB Garamond',serif;font-variant-numeric:lining-nums}}
.ouro{{background:{FOIL};-webkit-background-clip:text;background-clip:text;color:transparent}}
.fx{{background:{MARCA};color:{CAFE}}}
.vidro{{background:rgb(255 255 255/.14);backdrop-filter:blur(18px) saturate(1.2);-webkit-backdrop-filter:blur(18px);border:1.5px solid rgb(255 255 255/.32);box-shadow:0 18px 50px rgb(0 0 0/.28)}}
.vidro-claro{{background:rgb(247 241 231/.7);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1.5px solid rgb(255 255 255/.7);box-shadow:0 18px 50px rgb(30 24 20/.18)}}
.grao::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.16;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
CSS</style></head><body><div class="c grao">CORPO</div>
<script>document.fonts.ready.then(()=>{{document.body.dataset.ok=1}})</script></body></html>"""


def fundo_foto(arq, pos="center", tam="cover", extra=""):
    return f'<div class=abs style="inset:0;background:url({foto(arq, 1600)}) {pos}/{tam} no-repeat;{extra}"></div>'


def topo(cor, dir="OAB/ES 39.948"):
    return f'<div class=abs style="left:72px;right:72px;top:56px;display:flex;justify-content:space-between;font:500 22px Inter;letter-spacing:.08em;color:{cor}"><span>LETÍCIA BARROS</span><span>{dir}</span></div>'


def arroba(cor, fundo="transparent", y=1302):
    return f'<div class=abs style="left:0;right:0;top:{y}px;text-align:center"><span style="display:inline-block;font:600 28px Inter;letter-spacing:.01em;padding:8px 24px;border-radius:40px;color:{cor};background:{fundo}">{PERFIL}</span></div>'


def legenda(cor, y=1318):
    return f'<div class=abs style="left:0;right:0;top:{y}px;text-align:center;font:500 24px Inter;letter-spacing:.12em;color:{cor}">LEIA A LEGENDA</div>'


SETA = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


# 01 · ref. "Quem tem direito aposentadoria por invalidez?": pessoa em tela cheia, pergunta no topo, faixa na palavra-chave.
def r01_incapacidade():
    return ("", f"""
{fundo_foto(BANCO / 'original-aposentadoria-mulher-2026.jpg', '38% 30%')}
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(30 24 20/.82) 0,rgb(30 24 20/.55) 30%,rgb(30 24 20/0) 52%,rgb(30 24 20/0) 78%,rgb(30 24 20/.8) 100%)"></div>
{topo(AREIA, 'DIREITO PREVIDENCIÁRIO')}
<div class=abs style="left:0;right:0;top:170px;text-align:center;color:#fff">
  <div style="font:400 60px/1.1 Inter;letter-spacing:-.01em">Quem tem direito à</div>
  <div style="font:800 96px/1.02 Inter;letter-spacing:-.035em;margin-top:6px">aposentadoria</div>
  <div style="font:800 96px/1.02 Inter;letter-spacing:-.035em">por <span class=fx style="padding:0 18px 4px;border-radius:6px">incapacidade?</span></div>
</div>
{arroba('#fff', 'rgb(30 24 20/.45)')}""")


# 02 · ref. "Inventário pode ser feito em cartório?": foto escura do carimbo, aspas grandes, serifa, pílula de requisitos.
def r02_divorcio_cartorio():
    aspas = "font:700 210px/1 'EB Garamond';position:absolute"
    return ("", f"""
{fundo_foto(FOTOS / '7654118.jpg', '62% 50%', 'auto 112%', 'transform:scaleX(-1)')}
<div class=abs style="inset:0;background:linear-gradient(90deg,{FUNDO} 0,rgb(35 30 26/.94) 38%,rgb(35 30 26/.35) 72%,rgb(35 30 26/.2) 100%),linear-gradient(180deg,rgb(35 30 26/.6) 0,transparent 20%,transparent 75%,rgb(35 30 26/.85) 100%)"></div>
<div class=abs style="left:0;right:0;top:150px;text-align:center">
  <div class="g ouro" style="font-size:54px;font-weight:600;letter-spacing:.04em">Letícia Barros</div>
  <div style="font:500 22px Inter;letter-spacing:.24em;color:{AREIA};margin-top:2px">ADVOGADA · OAB/ES 39.948</div>
</div>
<div class=abs style="left:72px;top:500px;width:640px;color:#fff">
  <span class=ouro style="{aspas};left:-10px;top:-120px">“</span>
  <div class=g style="font-size:112px;line-height:1.0;font-weight:600;letter-spacing:-.01em;padding-top:40px">Divórcio<br>pode ser<br>feito em<br><i class=ouro style="font-weight:500">cartório?</i></div>
  <div style="display:flex;align-items:center;gap:26px;margin-top:40px">
    <span style="font:500 28px Inter;padding:8px 24px;border:1.5px solid {AREIA};border-radius:8px;color:{AREIA}">Veja os requisitos</span>
    <span class=ouro style="{aspas};position:relative;line-height:.5;top:40px">”</span>
  </div>
</div>
{legenda(AREIA)}""")


# 03 · ref. "Aposentadoria negada? Veja como reverter": palavra gigante em cor forte acima da pessoa, apoio com marca-texto.
def r03_auxilio_negado():
    return ("", f"""
<div class=abs style="left:0;right:0;top:440px;bottom:0;background:url({foto(FOTOS / '5717310.jpg', 1600)}) 50% 20%/cover no-repeat"></div>
<div class=abs style="left:0;right:0;top:0;height:720px;background:linear-gradient(180deg,{PAPEL} 0,{PAPEL} 64%,rgb(247 241 231/.0) 100%)"></div>
<div class=abs style="left:0;right:0;bottom:0;height:300px;background:linear-gradient(180deg,rgb(30 24 20/0),rgb(30 24 20/.75))"></div>
{topo(CAFE, 'DIREITO PREVIDENCIÁRIO')}
<div class=abs style="left:60px;right:40px;top:150px;color:{CAFE}">
  <div style="font:600 80px/1 Inter;letter-spacing:-.03em;padding-left:10px">Auxílio-doença</div>
  <div style="font:900 236px/.86 Inter;letter-spacing:-.06em;margin-top:2px">negado?</div>
  <div style="display:flex;justify-content:flex-end;margin-top:22px;padding-right:30px">
    <div style="font:500 44px/1.22 Inter;letter-spacing:-.01em;text-align:left">Veja o que a lei<br>permite <span class=fx style="font-weight:800;font-style:italic;padding:0 12px 2px">fazer</span> depois.</div>
  </div>
</div>
{arroba('#fff', 'rgb(30 24 20/.35)')}""")


# 04 · ref. "Quais os requisitos para pedir a aposentadoria por idade?": blocos de cor atrás das palavras-chave.
def r04_salario_maternidade():
    bloco = f"display:inline-block;background:{MARCA};color:{CAFE};font:800 104px/1 Inter;letter-spacing:-.04em;padding:6px 26px 14px;border-radius:12px"
    return ("", f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
<div class=abs style="left:0;right:0;top:480px;bottom:0;background:url({foto(BANCO / 'original-gestante-6-direitos.jpg', 1600)}) 50% 8%/cover no-repeat"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,{PAPEL} 0,{PAPEL} 34%,rgb(247 241 231/0) 46%,rgb(30 24 20/0) 84%,rgb(30 24 20/.55) 100%)"></div>
{topo(CAFE, 'DIREITO PREVIDENCIÁRIO')}
<div class=abs style="left:0;right:0;top:160px;text-align:center;color:{CAFE}">
  <div style="font:500 58px/1.15 Inter;letter-spacing:-.02em">Quais os <i style="font-weight:800">requisitos</i><br>para pedir o</div>
  <div style="margin-top:20px"><span style="{bloco}">salário-</span></div>
  <div style="margin-top:-6px"><span style="{bloco}">maternidade?</span></div>
</div>
{arroba('#fff', 'rgb(30 24 20/.4)')}""")


# 05 · ref. "Quero sair do meu trabalho e receber todos os meus direitos": título em caixa alta serifada, maleta embaixo.
def r05_rescisao_indireta():
    return ("", f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
<div class=abs style="left:-80px;right:-80px;top:560px;bottom:-60px;background:url({foto(FOTOS / '6538433.jpg', 1600)}) 64% 70%/cover no-repeat"></div>
<div class=abs style="left:0;right:0;top:540px;height:260px;background:linear-gradient(180deg,{PAPEL},rgb(247 241 231/0))"></div>
<div class=abs style="left:0;right:0;top:66px;text-align:center;font:500 24px Inter;letter-spacing:.3em;color:{CAFE}">LETÍCIA BARROS</div>
<div class=abs style="left:0;right:0;top:220px;text-align:center;color:{CAFE}">
  <div class=g style="font-size:104px;line-height:.98;font-weight:600;letter-spacing:.005em">QUERO SAIR DO<br>MEU TRABALHO</div>
  <div style="font:400 36px/1.35 Inter;letter-spacing:.06em;margin-top:22px">E RECEBER TODOS OS MEUS<br>DIREITOS. <span class=fx style="font-weight:600;padding:0 10px">É POSSÍVEL?</span></div>
</div>
""")


# 06 · ref. "Adverti, mas o problema continuou…": frase entre aspas em caixa alta, apoio com destaque, papel amassado na mão.
def r06_advertencia():
    return ("", f"""
{fundo_foto(FOTOS / '7927286.jpg', '40% 70%')}
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(30 24 20/.92) 0,rgb(30 24 20/.8) 36%,rgb(30 24 20/.2) 60%,rgb(30 24 20/.1) 80%,rgb(30 24 20/.6) 100%)"></div>
<div class=abs style="left:0;right:0;top:150px;text-align:center;color:{AREIA}">
  <div style="font:800 70px/1.06 Inter;letter-spacing:-.02em;color:#fff">“ASSINA AQUI,<br>É SÓ UMA ADVERTÊNCIA…”</div>
  <div style="font:400 42px/1.3 Inter;margin-top:26px">Essa assinatura pode <b class=ouro style="font-weight:800">pesar</b><br>numa demissão por justa causa.</div>
  <div style="display:inline-flex;align-items:center;gap:10px;margin-top:30px;font:500 28px Inter;padding:8px 18px 8px 26px;border:2px solid {AREIA};border-radius:40px">leia a legenda {SETA}</div>
</div>
<div class=abs style="left:0;right:0;top:1290px;display:flex;justify-content:center;align-items:center;gap:18px">
  <img src="{foto(PERFIL_IMG, 200)}" style="width:84px;height:84px;border-radius:50%;border:3px solid {OURO_CLARO};object-fit:cover">
  <div style="color:#fff;text-shadow:0 2px 10px rgb(0 0 0/.5)"><div style="font:700 34px Inter">Letícia Barros</div><div style="font:400 24px Inter">{PERFIL}</div></div>
</div>""")


# 07 · ref. "Quanto tempo de contribuição você tem?": objeto à esquerda, caixa de cor com a pergunta, frase de alerta embaixo.
def r07_tempo_contribuicao():
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(FOTOS / '33795954.jpg', 1600)}) 30% 40%/auto 118% no-repeat;background-color:#0d0b09"></div>
<div class=abs style="inset:0;background:linear-gradient(90deg,rgb(13 11 9/.2) 0,rgb(13 11 9/0) 40%,rgb(13 11 9/.55) 100%),linear-gradient(180deg,rgb(13 11 9/.5) 0,transparent 22%,transparent 62%,rgb(13 11 9/.92) 84%)"></div>
<div class=abs style="right:72px;top:150px;text-align:right">
  <div class="g ouro" style="font-size:48px;font-weight:600">Letícia Barros</div>
  <div style="font:500 22px Inter;letter-spacing:.2em;color:{AREIA}">ADVOGADA · OAB/ES 39.948</div>
</div>
<div class=abs style="left:520px;right:0;top:470px;padding:50px 60px 54px 56px;border-radius:30px 0 0 30px;background:linear-gradient(135deg,rgb(122 92 58/.92),rgb(74 56 38/.92));box-shadow:0 20px 60px rgb(0 0 0/.4)">
  <div class=g style="font-size:84px;line-height:1.02;font-weight:500;color:{PAPEL}">Quanto tempo de <i class=ouro>contribuição</i> você tem?</div>
</div>
<div class=abs style="left:0;right:0;top:1060px;text-align:center;color:{PAPEL}">
  <div style="font:300 50px/1.25 Inter">Não saber esse número pode<br><b style="font-weight:700">atrasar a sua aposentadoria.</b></div>
  <div style="display:inline-flex;align-items:center;gap:12px;margin-top:30px;font:500 26px Inter;padding:8px 22px" class=fx>leia a legenda {SETA}</div>
</div>""")


# 08 · ref. "Eu consigo me aposentar sem ter contribuído 30 anos?": pergunta entre aspas, número grande gravado no vidro.
def r08_experiencia_gestante():
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(FOTOS / '16399375.jpg', 1600)}) 70% 50%/auto 104% no-repeat;background-color:#050505;filter:sepia(.35) saturate(.9)"></div>
<div class=abs style="inset:0;background:linear-gradient(90deg,rgb(30 24 20/.95) 0,rgb(30 24 20/.75) 42%,rgb(30 24 20/0) 70%),linear-gradient(180deg,rgb(30 24 20/.5) 0,transparent 20%,transparent 80%,rgb(30 24 20/.8) 100%)"></div>
<div class=abs style="left:72px;right:72px;top:62px;display:flex;justify-content:space-between;font:500 22px/1.3 Inter;letter-spacing:.08em;color:{AREIA}"><span><b>LETÍCIA</b><br>BARROS</span><span style="text-align:right"><b>DIREITO</b><br>TRABALHISTA</span></div>
<div class=abs style="left:640px;top:820px;width:330px;text-align:center;font:200 250px/1 Inter;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:2px rgb(232 208 138/.75);text-shadow:0 0 30px rgb(232 208 138/.18)">90</div>
<div class=abs style="left:72px;top:420px;width:640px;color:{PAPEL}">
  <div style="font:300 54px/1.12 Inter">“Estou no contrato<br>de experiência. Se eu<br>engravidar, tenho</div>
  <div class=g style="font-size:132px;line-height:1;font-weight:500;letter-spacing:.01em;margin-top:14px">ESTABILI-</div>
  <div style="display:inline-block;margin-top:6px;padding:4px 18px 10px 14px;border-left:2px solid {OURO_CLARO};border-right:2px solid {OURO_CLARO};background:rgb(201 169 98/.22)"><span class="g ouro" style="font-size:132px;line-height:1;font-weight:500">DADE?”</span></div>
</div>
<div class=abs style="left:0;right:0;top:1300px;text-align:center"><div class="g" style="font-size:40px;letter-spacing:.14em;color:{AREIA}">LETÍCIA BARROS</div><div style="font:400 22px Inter;letter-spacing:.2em;color:{AREIA};opacity:.8">ADVOCACIA · OAB/ES 39.948</div></div>""")


# 09 · ref. "Se 2026 fosse igual a 2025 na sua advocacia": ampulheta em luz natural, itálico grande cruzando a foto.
def r09_virada_do_ano():
    return ("", f"""
<div class=abs style="inset:0;background:#cbc3c0"></div>
<div class=abs style="left:0;right:0;top:330px;bottom:0;background:url({foto(FOTOS / '4397906.jpg', 1600)}) 22% 100%/cover no-repeat"></div>
<div class=abs style="left:0;right:0;top:330px;height:160px;background:linear-gradient(180deg,#cbc3c0,transparent)"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(239 230 217/.55) 0,rgb(239 230 217/.15) 45%,rgb(239 230 217/0) 70%,rgb(239 230 217/.5) 100%)"></div>
<div class=abs style="left:72px;top:66px;font:600 22px/1.4 Inter;letter-spacing:.1em;color:{CAFE}">LETÍCIA BARROS<br><span style="font-weight:400">ADVOGADA DA MULHER QUE TRABALHA</span></div>
<div class=abs style="left:72px;right:60px;top:280px;color:{CAFE}">
  <div style="display:flex;align-items:flex-end;gap:24px">
    <div style="font:500 38px/1.2 Inter;text-align:right;padding-bottom:30px">Se <b>2027</b> fosse<br>igual a <b>2026</b></div>
    <div class=g style="font-size:150px;line-height:.9;font-style:italic;font-weight:400">no seu</div>
  </div>
  <div class=g style="font-size:200px;line-height:.92;font-style:italic;font-weight:400;letter-spacing:-.02em;margin-left:-6px">trabalho,</div>
  <div style="font:400 52px/1.2 Inter;margin:18px 0 0 560px">você ficaria<br>satisfeita?</div>
</div>
<div class=abs style="right:72px;top:1250px;text-align:right;font:600 22px/1.45 Inter;letter-spacing:.1em;color:{CAFE}">FÉRIAS, 13º E FGTS<br><span style="font-weight:400">CONFIRA ANTES DE VIRAR O ANO</span></div>""")


# 10 · ref. "Seu conteúdo não converte porque você esqueceu do mais importante": cartão de papel em cima, cadeira de couro.
def r10_acerto_aviso_previo():
    eco = " ".join(["seu acerto pode vir menor se ninguém conferir o mais importante"] * 3)
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(FOTOS / '14792097.jpg', 1600)}) 70% 100%/cover no-repeat"></div>
<div class=abs style="left:150px;right:150px;top:700px;font:300 34px/1.15 Inter;color:rgb(30 24 20/.16);text-align:justify;text-transform:lowercase">{eco}</div>
<div class=abs style="left:100px;right:100px;top:0;height:690px;background:{PAPEL};border-radius:0 0 46px 46px;box-shadow:0 16px 40px rgb(30 24 20/.16)"></div>
<div class=abs style="left:100px;right:100px;top:84px;text-align:center;color:{CAFE}">
  <div style="font:400 28px Inter"><b>Letícia Barros</b> | Direito do trabalho</div>
  <div style="font:500 60px/1.05 Inter;letter-spacing:-.03em;margin-top:52px">Seu acerto pode vir</div>
  <div style="display:flex;justify-content:center;align-items:baseline;gap:18px;margin-top:-4px">
    <span style="font:900 150px/1 Inter;letter-spacing:-.06em">menor</span>
  </div>
  <div style="font:500 46px/1.3 Inter;letter-spacing:-.02em;margin-top:6px">se ninguém <span class=fx style="font-weight:700;padding:0 12px 2px">conferir</span> o<br><u style="text-decoration-thickness:3px;text-underline-offset:8px">aviso prévio proporcional</u></div>
</div>
<div class=abs style="left:150px;top:648px;transform:rotate(-6deg);font:600 28px Inter;padding:10px 26px;border-radius:40px;color:{PAPEL};background:linear-gradient(135deg,#6b4a2c,#3a281a);border:2px solid {PAPEL}">{PERFIL}</div>""")


# 11 · ref. grade do consumidor (checklist): cartão café, lista numerada em blocos, objeto no canto.
def r11_checklist_demissao():
    itens = [("01", "Leia o motivo escrito no papel"), ("02", "Confira a data do último dia"),
             ("03", "Grávida? Só vale com o sindicato"), ("04", "Fique com uma cópia assinada")]
    linhas = "".join(f'<div style="display:flex;align-items:center;gap:28px;margin-top:22px"><div style="width:110px;height:96px;border-radius:14px;display:flex;align-items:center;justify-content:center;font:700 44px Inter" class=fx>{n}</div><div style="flex:1;height:96px;border-radius:14px;background:rgb(247 241 231/.1);border:1.5px solid rgb(232 208 138/.35);display:flex;align-items:center;padding:0 30px;font:500 36px Inter;color:{PAPEL}">{t}</div></div>' for n, t in itens)
    return ("", f"""
<div class=abs style="inset:0;background:radial-gradient(120% 80% at 80% 10%,#5a4330 0,#3a2b1f 45%,{FUNDO} 100%)"></div>
<div class=abs style="right:-120px;bottom:-60px;width:620px;height:620px;background:url({foto(FOTOS / '6358834.jpg', 900)}) center/cover;border-radius:50%;opacity:.35;filter:sepia(.5)"></div>
{topo(AREIA, 'DIREITO TRABALHISTA')}
<div class=abs style="left:80px;right:80px;top:190px;color:{PAPEL}">
  <div class="g ouro" style="font-size:96px;font-style:italic;font-weight:500;line-height:1">Checklist:</div>
  <div class=g style="font-size:66px;line-height:1.08;font-weight:500;margin-top:12px">confira antes de assinar<br>o pedido de demissão</div>
  <div style="font:400 30px Inter;color:{AREIA};margin-top:20px;padding-bottom:16px">Quatro pontos que evitam surpresa no acerto.</div>
  {linhas}
</div>
{legenda(AREIA, 1310)}""")


# 12 · ref. grade do consumidor ("Comprei e não recebi. E agora?"): foto em tom café, pergunta em serifa itálica.
def r12_compra_nao_recebida():
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(FOTOS / '6994295.jpg', 1600)}) 50% 50%/cover no-repeat;filter:sepia(.45) saturate(.8) brightness(.8)"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(58 43 31/.55) 0,rgb(58 43 31/.82) 38%,rgb(58 43 31/.88) 64%,rgb(30 24 20/.7) 100%)"></div>
<div class=abs style="left:72px;top:60px;display:flex;align-items:center;gap:16px;color:{PAPEL}">
  <img src="{foto(PERFIL_IMG, 200)}" style="width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid {OURO_CLARO}">
  <div><div style="font:600 26px Inter">Letícia Barros</div><div style="font:400 22px Inter;opacity:.85">{PERFIL}</div></div>
</div>
<div class=abs style="left:72px;right:72px;top:500px;color:{PAPEL}">
  <div class=g style="font-size:132px;line-height:1;font-style:italic;font-weight:500">Comprei e<br>não recebi.</div>
  <div class="g ouro" style="font-size:132px;line-height:1.05;font-style:italic;font-weight:500">E agora?</div>
  <div style="font:400 38px/1.35 Inter;margin-top:34px;max-width:780px;color:{AREIA}">O que o Código de Defesa do Consumidor garante quando o pedido não chega.</div>
</div>
{legenda(AREIA, 1318)}""")


# 13 · ref. "Importa com segurança" (3 peças): pessoa em ambiente quente, notificações de vidro flutuando, barra de vidro embaixo.
def r13_notificacoes():
    def notif(x, y, rot, quem, hora, txt, larg=470):
        return f'<div class="abs vidro" style="left:{x}px;top:{y}px;width:{larg}px;border-radius:24px;padding:20px 24px;transform:rotate({rot}deg);color:#fff"><div style="display:flex;justify-content:space-between;font:600 24px Inter"><span>{quem}</span><span style="font-weight:400;opacity:.8">{hora}</span></div><div style="font:400 26px/1.3 Inter;margin-top:6px">{txt}</div></div>'
    item = 'display:flex;align-items:center;gap:12px;font:500 24px/1.2 Inter;color:#fff'
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(FOTOS / '30289341.jpg', 1600)}) 50% 20%/cover no-repeat"></div>
<div class=abs style="inset:0;background:radial-gradient(60% 40% at 50% 30%,transparent 0,rgb(30 24 20/.25) 100%),linear-gradient(180deg,rgb(30 24 20/.35) 0,transparent 18%,transparent 52%,rgb(30 24 20/.86) 72%,{FUNDO} 100%)"></div>
{topo('#fff', 'DIREITO TRABALHISTA')}
{notif(40, 150, -3, 'Gerente', '23:47', 'Consegue ver isso agora? É rapidinho.')}
{notif(600, 640, 2, 'RH', 'domingo', 'Plantão amanhã às 6h, confirma?', 440)}
{notif(40, 820, -1.5, 'Grupo da equipe', '22:10', 'Quem não responder, conversamos segunda.', 500)}
<div class=abs style="left:72px;right:72px;top:985px;color:#fff">
  <div style="font:300 64px/1.1 Inter;letter-spacing:-.02em">Responder o chefe</div>
  <div style="font:300 64px/1.1 Inter;letter-spacing:-.02em"><b style="font-weight:700">fora do horário</b> conta</div>
  <div style="font:300 64px/1.1 Inter;letter-spacing:-.02em">como <span class=fx style="font-weight:700;padding:0 14px 4px;border-radius:8px">trabalho?</span></div>
</div>
<div class="abs vidro" style="left:56px;right:56px;top:1262px;height:96px;border-radius:24px;display:flex;justify-content:space-around;align-items:center;background:rgb(30 24 20/.5)">
  <div style="{item}"><span class=ouro style="font-size:30px">§</span>CLT, art. 6º</div>
  <div style="{item}"><span class=ouro style="font-size:30px">✦</span>Leia a legenda</div>
  <div style="{item}"><span class=ouro style="font-size:30px">@</span>adv.leticiabarros2</div>
</div>""")


# 14 · ref. cartão de perfil flutuando na mão / celular de vidro: retrato real da Dra., cartão de perfil de vidro em 3D.
def r14_cartao_perfil():
    return ("", f"""
<div class=abs style="inset:0;background:radial-gradient(70% 60% at 50% 35%,#7a5f45 0,#4a3a2c 50%,{FUNDO} 100%)"></div>
<img class=abs src="{foto(DRA, 1100, 'PNG')}" style="left:150px;top:150px;width:780px;filter:brightness(.92)">
<div class=abs style="inset:0;background:linear-gradient(180deg,transparent 0,transparent 62%,rgb(35 30 26/.7) 80%,{FUNDO} 96%)"></div>
<div class=abs style="left:0;right:0;top:66px;text-align:center;font:500 24px Inter;letter-spacing:.3em;color:{AREIA}">PRAZER, LETÍCIA BARROS</div>
<div class="abs vidro" style="left:110px;top:760px;width:860px;border-radius:34px;padding:34px 40px;transform:perspective(1400px) rotateX(10deg) rotateY(-12deg) rotateZ(-3deg);color:#fff;background:linear-gradient(135deg,rgb(30 24 20/.55),rgb(30 24 20/.35))">
  <div style="display:flex;align-items:center;gap:28px">
    <div style="padding:5px;border-radius:50%;background:{FOIL}"><img src="{foto(PERFIL_IMG, 300)}" style="display:block;width:140px;height:140px;border-radius:50%;object-fit:cover;border:4px solid {FUNDO}"></div>
    <div><div style="font:700 40px Inter">adv.leticiabarros2</div><div style="font:400 28px Inter;opacity:.85;margin-top:4px">Letícia Barros · Advogada</div></div>
  </div>
  <div style="font:400 29px/1.45 Inter;margin-top:24px">A advogada da mulher que trabalha.<br>Trabalho, previdência e família, sem juridiquês.<br>Vitória/ES · OAB/ES 39.948</div>
  <div style="display:flex;gap:16px;margin-top:26px">
    <div class=fx style="flex:1;text-align:center;font:700 28px Inter;padding:14px;border-radius:14px">Seguir</div>
    <div style="flex:1;text-align:center;font:600 28px Inter;padding:14px;border-radius:14px;background:rgb(255 255 255/.16)">Salvar os posts</div>
  </div>
</div>
<div class=abs style="left:0;right:0;top:1250px;text-align:center;color:{PAPEL}"><div class=g style="font-size:58px;font-style:italic;font-weight:500">Eu explico, <span class=ouro>sem juridiquês.</span></div></div>""")


LOTE = {
    "ref-01-incapacidade": r01_incapacidade, "ref-02-divorcio-cartorio": r02_divorcio_cartorio,
    "ref-03-auxilio-negado": r03_auxilio_negado, "ref-04-salario-maternidade": r04_salario_maternidade,
    "ref-05-rescisao-indireta": r05_rescisao_indireta, "ref-06-advertencia": r06_advertencia,
    "ref-07-tempo-contribuicao": r07_tempo_contribuicao, "ref-08-experiencia-gestante": r08_experiencia_gestante,
    "ref-09-virada-do-ano": r09_virada_do_ano, "ref-10-acerto-aviso-previo": r10_acerto_aviso_previo,
    "ref-11-checklist-demissao": r11_checklist_demissao, "ref-12-compra-nao-recebida": r12_compra_nao_recebida,
    "ref-13-notificacoes": r13_notificacoes, "ref-14-cartao-perfil": r14_cartao_perfil,
}


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for nome, fn in LOTE.items():
            if so and not any(nome.startswith(x) for x in so):
                continue
            css, corpo = fn()
            await pg.set_content(BASE.replace("CSS</style>", css + "</style>").replace("CORPO", corpo), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(SAIDA / f"{nome}.jpg", quality=90)
            print(nome)
        await b.close()
    fs = [SAIDA / f"{n}.jpg" for n in LOTE]
    if all(f.exists() for f in fs):
        cols = 4
        grade = Image.new("RGB", (cols * 488 - 8, ((len(fs) + cols - 1) // cols) * 648 - 8), "white")
        for i, f in enumerate(fs):
            grade.paste(Image.open(f).resize((480, 640), Image.LANCZOS), ((i % cols) * 488, (i // cols) * 648))
        grade.save(AQUI / "grade.jpg", quality=86)


if __name__ == "__main__":
    asyncio.run(main())
