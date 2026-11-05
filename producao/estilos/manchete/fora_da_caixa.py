"""Manchete: lote de 10 criativos sobre assuntos fora da caixa. Cada função copia um layout da referência."""
from gerar import AREIA, BANCO, CAFE, FOIL, FUNDO, MARCA, PAPEL, PERFIL, RAIZ, foto

RECORTES = RAIZ / "apps" / "api" / "_saida_producao_1510" / "_recortes"
BALAO = f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12.5h5"/></svg>'


def pilula(cor=CAFE, fundo="transparent"):
    return f'<div class=abs style="left:0;right:0;top:50px;text-align:center"><span style="display:inline-block;font:500 24px Inter;padding:6px 20px;border:1.5px solid {cor};border-radius:30px;color:{cor};background:{fundo}">{PERFIL}</span></div>'


def topo(cor):
    return f'<div class=topo style="color:{cor}"><span>LETÍCIA BARROS</span><span>OAB/ES 39.948</span></div>'


def rodape(cor):
    return f'<div class=abs style="left:0;right:0;bottom:62px;text-align:center;font:500 24px Inter;letter-spacing:.08em;color:{cor}">LEIA A LEGENDA</div>'


def cabelo():
    """Layout 'Menores desacompanhados': pessoa à direita, título empilhado à esquerda."""
    return ("", f"""
<div class=abs style="left:-60px;top:-60px;width:1340px;height:2010px;background:url({foto(BANCO / '7468194.jpg', 1500)}) center/cover;transform:scaleX(-1)"></div>
<div class=abs style="inset:0;background:linear-gradient(90deg,rgb(30 24 20/.86) 0,rgb(30 24 20/.74) 46%,rgb(30 24 20/0) 64%),linear-gradient(180deg,rgb(30 24 20/.45) 0,rgb(30 24 20/0) 16%,rgb(30 24 20/0) 76%,rgb(30 24 20/.85) 100%)"></div>
{topo(AREIA)}
<div class=abs style="left:72px;top:430px;width:640px;color:#fff">
  <div style="font:300 42px/1.25 Inter;letter-spacing:.01em">NO TRABALHO,<br>PEDIRAM PARA</div>
  <div class=p style="font-size:128px;line-height:1.06;font-style:italic;font-weight:400;margin-top:24px">ALISAR<br>O SEU<br>CABELO?</div>
  <div style="margin-top:40px;font:400 34px/1.4 Inter;width:520px;padding-top:18px;border-top:3px solid #e8d08a">A lei proíbe discriminar para contratar ou manter alguém no emprego.</div>
</div>
{rodape(AREIA)}""")


def amigo_secreto():
    """Layout 'e se o drone causar um acidente?': frase, faixa com itálico, objeto e apoio."""
    return ("", f"""
<div class=abs style="inset:0;background:{FUNDO}"></div>
<div class=abs style="left:90px;top:360px;width:900px;height:860px;background:url({foto(BANCO / '33629668.jpg', 1300)}) 50% 30%/cover;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,{FUNDO} 26%,rgb(35 30 26/0) 40%,rgb(35 30 26/0) 70%,{FUNDO} 84%)"></div>
{pilula(AREIA)}
<div class=abs style="left:0;right:0;top:138px;text-align:center;font:300 66px Inter;letter-spacing:-.015em;color:#fff">o amigo secreto da firma é</div>
<div class="abs p" style="left:62px;right:62px;top:232px;text-align:center;background:{MARCA};color:{CAFE};font-size:112px;line-height:1.28;font-style:italic;font-weight:700;transform:rotate(-1deg)">obrigatório?</div>
<div class=abs style="left:110px;right:110px;top:1190px;text-align:center;font:300 36px/1.38 Inter;color:#fff">A empresa pode convidar. Obrigar a participar e descontar do salário é outra história.</div>
{rodape(AREIA)}""")


def preco():
    """Layout 'Conta de luz e água alta?': título, pílula escura e objeto no centro."""
    moeda = '<div class=abs style="left:{}px;top:{}px;width:{}px;height:{}px;border-radius:50%;background:' + MARCA + ';box-shadow:0 8px 18px rgb(30 24 20/.25)"></div>'
    return ("", f"""
<div class=abs style="inset:0;background:{PAPEL};background-image:radial-gradient(rgb(30 24 20/.13) 1.6px,transparent 1.7px);background-size:30px 30px"></div>
{pilula(CAFE, PAPEL)}
<div class="abs p" style="left:0;right:0;top:152px;text-align:center;font-size:84px;line-height:1.22;font-weight:400">Um preço na prateleira,<br><i style="font-weight:500">outro no caixa?</i></div>
<div class=abs style="left:0;right:0;top:432px;text-align:center"><span style="display:inline-flex;align-items:center;gap:12px;background:{CAFE};color:{AREIA};border-radius:30px;padding:14px 32px;font:400 32px Inter">{BALAO}Entenda a regra e como reagir</span></div>
{moeda.format(70, 620, 110, 110)}{moeda.format(900, 1080, 120, 120)}{moeda.format(880, 590, 70, 70)}
<img class=abs src="{foto(RECORTES / 'corte-reais.png', 1040, 'PNG')}" style="left:30px;top:640px;width:1020px;transform:rotate(-5deg);filter:drop-shadow(14px 26px 22px rgb(30 24 20/.35))">
<div class=abs style="left:0;right:0;top:1262px;text-align:center;font:400 28px Inter">Lei 10.962/2004, art. 5º</div>
{rodape(CAFE)}""")


def estacionamento():
    """Layout 'Bagagem sumida?': etiqueta redonda presa ao objeto e frase com itálico no fim."""
    return ("", f"""
<div class=abs style="inset:0;background:linear-gradient(170deg,#8c755c 0,#5a4a3b 42%,{FUNDO} 78%)"></div>
{pilula(AREIA)}
<img class=abs src="{foto(RECORTES / 'corte-chaves.png', 1055, 'PNG')}" style="left:-30px;top:170px;width:1100px;transform:rotate(-14deg);filter:drop-shadow(12px 24px 18px rgb(0 0 0/.5))">
<svg class=abs style="left:300px;top:360px" width="240" height="190" viewBox="0 0 240 190" fill="none" stroke="#efe6d9" stroke-width="3"><path d="M60 8C0 70 70 130 178 178"/></svg>
<div class=abs style="left:286px;top:462px;width:430px;height:430px;border-radius:50%;background:{FOIL};box-shadow:0 26px 50px rgb(0 0 0/.5);transform:rotate(-14deg);display:flex;align-items:center;justify-content:center;text-align:center;color:{CAFE}">
  <div style="position:absolute;top:30px;left:185px;width:60px;height:24px;border-radius:12px;background:#231a14"></div>
  <div style="font:600 38px/1.22 Inter;letter-spacing:-.01em">Não nos<br>responsabilizamos</div>
</div>
<div class=abs style="left:0;right:0;top:936px;text-align:center;color:#fff">
  <div style="font:600 66px Inter;letter-spacing:-.015em">Furto no estacionamento?</div>
  <div style="font:300 62px Inter;letter-spacing:-.015em;margin-top:18px">A placa não apaga a</div>
  <div class=p style="font-size:112px;line-height:1.25;font-style:italic;font-weight:700;color:#e8d08a">responsabilidade!</div>
</div>
{rodape(AREIA)}""")


def revista():
    """Layout 'Você sabia? Overbooking': faixa, frase, objeto grande e fita curva com a palavra-tema."""
    texto = " ✦ ".join(["REVISTA ÍNTIMA"] * 7)
    return ("", f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
<div class=abs style="left:0;top:470px;width:1080px;height:1620px;background:url({foto(BANCO / '6650020.jpg', 1400)}) center/cover;filter:sepia(.25)"></div>
<div class=abs style="inset:0;background:linear-gradient(180deg,{PAPEL} 33%,rgb(247 241 231/0) 46%)"></div>
{pilula(CAFE, PAPEL)}
<div class=abs style="left:0;right:0;top:124px;text-align:center">
  <span class=p style="display:inline-block;background:{MARCA};font-size:60px;font-style:italic;font-weight:700;padding:4px 30px 10px">Você sabia?</span>
  <div style="font:300 76px/1.14 Inter;letter-spacing:-.02em;margin-top:18px">Revista íntima não é<br>rotina, <b style="font-weight:600;border-bottom:7px solid;border-image:{FOIL} 1">é proibida</b></div>
  <div style="display:inline-flex;align-items:center;gap:10px;margin-top:24px;font:400 30px Inter">{BALAO}leia a legenda</div>
</div>
<svg class=abs style="left:0;top:0;filter:drop-shadow(0 12px 14px rgb(0 0 0/.45))" width="1080" height="1440" viewBox="0 0 1080 1440" fill="none">
<defs><linearGradient id="fi" x1="0" x2="1" y1="0" y2=".3"><stop offset="0" stop-color="#c9a14e"/><stop offset=".25" stop-color="#f9efc2"/><stop offset=".5" stop-color="#d8b566"/><stop offset=".75" stop-color="#f1dfa2"/><stop offset="1" stop-color="#c9a14e"/></linearGradient>
<path id="cu" d="M-60 1120C200 1500 560 1460 780 1250C960 1080 1090 900 1000 760C940 680 860 730 880 840C910 1000 1060 1120 1160 1090"/></defs>
<use href="#cu" stroke="url(#fi)" stroke-width="66"/>
<text font-family="Inter" font-weight="700" font-size="32" letter-spacing="2.5" fill="{CAFE}" dy="11"><textPath href="#cu">{texto}</textPath></text></svg>""")


def exame():
    """Layout 'DRONES: eles voam': título central, palavra repetida ao fundo e objeto na frente."""
    fantasma = "".join(f'<div class=p style="font-size:300px;line-height:.98;font-weight:500;letter-spacing:-.02em;white-space:nowrap;color:#E9DCC0;margin-left:-20px">EXAME</div>' for _ in range(3))
    return ("", f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
<div class=abs style="left:0;top:540px">{fantasma}</div>
{topo(CAFE)}
<div class="abs p" style="left:0;right:0;top:136px;text-align:center;font-size:168px;line-height:1.06;font-weight:400">3 DIAS:</div>
<div class=abs style="left:0;right:0;top:330px;text-align:center;font:300 42px/1.3 Inter;letter-spacing:.01em">POR ANO, SEM DESCONTO,<br><b style="font-weight:600">PARA EXAME PREVENTIVO DE CÂNCER.</b></div>
<div class=abs style="right:72px;top:488px;text-align:right;font:500 26px/1.3 Inter">CLT, art. 473, XII</div>
<img class=abs src="{foto(RECORTES / 'corte-estetoscopio.png', 1200, 'PNG')}" style="left:-30px;top:690px;width:1140px;transform:rotate(-16deg);filter:drop-shadow(14px 24px 18px rgb(30 24 20/.35))">
{rodape(CAFE)}""")


def banheiro():
    """Layout 'Novas regras': foto escura com forma grande transparente e frase no centro."""
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(BANCO / '7071.jpg', 1880)}) 40% 50%/cover;filter:grayscale(1) sepia(.55) brightness(.72) contrast(1.1)"></div>
<div class=abs style="left:90px;top:120px;width:1140px;height:1140px;border-radius:50%;border:170px solid;border-color:#c9a14e;opacity:.3;mix-blend-mode:screen"></div>
<div class=abs style="inset:0;background:rgb(30 24 20/.42)"></div>
{pilula(AREIA)}
<div class=abs style="left:60px;right:60px;top:490px;text-align:center;color:#fff">
  <div style="font:300 72px/1.2 Inter;letter-spacing:-.02em">Anotaram quantas vezes</div>
  <div style="font:600 86px/1.18 Inter;letter-spacing:-.025em;margin-top:6px">você foi ao banheiro?</div>
  <div style="font:300 38px/1.4 Inter;margin:48px auto 0;width:800px">Controle assim pode ser considerado abuso. Limite de ida ao banheiro já gerou indenização na Justiça do Trabalho.</div>
</div>
{rodape(AREIA)}""")


def story():
    """Layout '5 garantias': mãos segurando o objeto, com o título dentro dele."""
    return ("", f"""
<div class=abs style="inset:0;background:url({foto(BANCO / '7120126.jpg', 1300)}) center/cover"></div>
<div class=abs style="inset:0;background:#6b5238;mix-blend-mode:color"></div>
<div class=abs style="inset:0;background:radial-gradient(90% 70% at 50% 50%,rgb(30 24 20/0) 45%,rgb(30 24 20/.6) 100%)"></div>
{pilula(AREIA)}
<div class=abs style="left:306px;top:402px;width:388px;height:788px;border-radius:22px 22px 44px 44px;background:{PAPEL};color:{CAFE};padding:74px 30px 0;text-align:center">
  <div style="font:500 24px Inter;letter-spacing:.06em">NOVO STORY</div>
  <div class=p style="font-size:62px;line-height:1.12;font-weight:500;margin-top:36px">Seu story pode virar</div>
  <div class=p style="display:inline-block;background:{MARCA};font-size:80px;line-height:1.3;font-style:italic;font-weight:700;padding:0 18px;margin-top:12px">prova</div>
  <div style="font:400 28px/1.35 Inter;margin-top:30px">Foto, comentário e mensagem podem entrar no processo.</div>
  <div style="display:inline-flex;align-items:center;gap:10px;font:500 25px Inter;margin-top:30px">{BALAO}leia a legenda</div>
</div>""")


def avo():
    """Layout 'Cancelamento de voo funerário': fundo escuro texturizado, pessoa à direita, itálico e apoio."""
    return ("", f"""
<div class=abs style="inset:0;background:radial-gradient(80% 60% at 20% 30%,#5c4d40 0,#3a3028 55%,{FUNDO} 100%)"></div>
<div class=abs style="left:300px;top:440px;width:780px;height:1000px;background:url({foto(BANCO / '36810448.jpg', 1300)}) 60% top/cover;filter:sepia(.28);-webkit-mask-image:linear-gradient(90deg,transparent,#000 24%),linear-gradient(180deg,transparent,#000 20%);-webkit-mask-composite:source-in;mask-composite:intersect"></div>
{topo(AREIA)}
<div class="abs p" style="left:72px;top:150px;font-size:112px;line-height:1.14;font-style:italic;font-weight:400;color:#fff">Avó também<br><span style="color:#e8d08a">pode pagar pensão?</span></div>
<div class=abs style="left:72px;top:440px;font:300 34px/1.34 Inter;color:#fff">QUANDO OS PAIS<br><b style="font-weight:600">NÃO CONSEGUEM ARCAR,</b><br>A LEI PREVÊ UM CAMINHO.</div>
<div class=abs style="left:72px;bottom:62px;font:500 24px/1.4 Inter;letter-spacing:.06em;color:{AREIA}">LEIA A<br>LEGENDA</div>""")


def doar_sangue():
    """Layout 'Assento em pé no avião': título, faixa 'Mito ou Realidade?' e fileira de objetos."""
    cadeira = foto(RECORTES / "obj-cadeira.png", 700, "PNG")
    fileira = "".join(f'<img src="{cadeira}" style="width:258px;margin-left:{0 if i == 0 else -6}px;filter:sepia(.75) saturate(.75) brightness(.92) drop-shadow(6px 14px 10px rgb(30 24 20/.3))">' for i in range(4))
    return ("", f"""
<div class=abs style="inset:0;background:linear-gradient(180deg,#fff,{AREIA})"></div>
{topo(CAFE)}
<div class=abs style="left:0;right:0;top:136px;text-align:center">
  <div class=p style="font-size:136px;line-height:1.06;font-style:italic;font-weight:600">Doar sangue</div>
  <div style="font:300 96px/1.2 Inter;letter-spacing:-.03em"><i class=p style="font-weight:600">dá</i> folga no trabalho?</div>
  <div class=p style="display:inline-block;background:{MARCA};font-size:62px;font-style:italic;font-weight:700;padding:6px 34px 12px;margin-top:30px;transform:rotate(-1deg)">Mito ou Realidade?</div>
</div>
<div class=abs style="left:20px;top:650px;width:1040px;display:flex;justify-content:center">{fileira}</div>
<div class=abs style="left:60px;right:60px;top:1060px;height:2px;background:{FOIL}"></div>
<div class=abs style="left:90px;right:90px;top:1104px;text-align:center;font:300 42px/1.35 Inter">Uma cadeira vazia pode ser falta justificada: a lei prevê um dia a cada 12 meses.</div>
{rodape(CAFE)}""")


LOTE = {
    "manchete-04-cabelo": cabelo, "manchete-05-amigo-secreto": amigo_secreto, "manchete-06-preco": preco,
    "manchete-07-estacionamento": estacionamento, "manchete-08-revista": revista, "manchete-09-exame": exame,
    "manchete-10-banheiro": banheiro, "manchete-11-story": story, "manchete-12-avo": avo, "manchete-13-doar-sangue": doar_sangue,
}
