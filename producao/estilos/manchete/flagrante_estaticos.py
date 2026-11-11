"""Manchete: estáticos únicos com os temas dos Reels Flagrante (09/11/2026, pedido da Jessica: "Manchete vira o padrão de
todo estático único" + "com os temas dos reels motions que fizemos"). Peças 14 a 34. O Flagrante 20 (pausa no banheiro)
fica de fora porque já existe a manchete-10. Os layouts da referência viram funções com parâmetros; a faixa dourada
de cima e de baixo entra pela moldura de gerar.py, como nas outras."""
from fora_da_caixa import BALAO, RECORTES, pilula, rodape, topo
from gerar import AREIA, CAFE, FOIL, FUNDO, MARCA, PAPEL, foto


def obj(nome, css, largura=1100):
    return f'<img class=abs src="{foto(RECORTES / nome, largura, "PNG")}" style="{css};filter:drop-shadow(14px 24px 18px rgb(30 24 20/.38))">'


def escuro(l1, grande, faixa, grande2="", objeto="", apoio=""):
    """Layout 01 sem foto: objeto no alto sobre café, título central com fita dourada."""
    return lambda: ("", f"""
<div class=abs style="inset:0;background:radial-gradient(75% 45% at 50% 26%,#5c4d40 0,#3a3028 50%,{FUNDO} 80%)"></div>
{objeto}
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(35 30 26/0) 46%,rgb(35 30 26/.9) 58%,{FUNDO} 64%)"></div>
{topo(AREIA)}
<div class=abs style="left:0;right:0;top:800px;text-align:center;color:#fff">
  <div style="font:300 56px Inter;letter-spacing:-.01em">{l1}</div>
  <div class=p style="font-size:150px;line-height:1.04;font-style:italic;font-weight:400;letter-spacing:-.01em">{grande}</div>
  <div style="display:inline-block;background:{MARCA};color:{CAFE};font:300 46px Inter;padding:4px 24px 7px;margin-top:6px">{faixa}</div>
  {f'<div class=p style="font-size:124px;line-height:1.14;font-style:italic;font-weight:400">{grande2}</div>' if grande2 else ''}
  {f'<div style="font:300 32px/1.4 Inter;margin:26px auto 0;width:820px">{apoio}</div>' if apoio else ''}
</div>
{rodape(AREIA)}""")


def pontilhado(titulo, pilula_txt, objeto, base):
    """Layout 06: fundo pontilhado, título, pílula escura e objeto."""
    return lambda: ("", f"""
<div class=abs style="inset:0;background:{PAPEL};background-image:radial-gradient(rgb(30 24 20/.13) 1.6px,transparent 1.7px);background-size:30px 30px"></div>
{pilula(CAFE, PAPEL)}
<div class="abs p" style="left:0;right:0;top:152px;text-align:center;font-size:84px;line-height:1.22;font-weight:400">{titulo}</div>
<div class=abs style="left:0;right:0;top:432px;text-align:center"><span style="display:inline-flex;align-items:center;gap:12px;background:{CAFE};color:{AREIA};border-radius:30px;padding:14px 32px;font:400 32px Inter">{BALAO}{pilula_txt}</span></div>
{objeto}
<div class=abs style="left:0;right:0;top:1262px;text-align:center;font:400 28px Inter">{base}</div>
{rodape(CAFE)}""")


def sabia(frase, fita, objeto):
    """Layout 08: 'Você sabia?', frase, objeto grande e fita curva com a palavra-tema."""
    texto = " ✦ ".join([fita] * 7)
    return lambda: ("", f"""
<div class=abs style="inset:0;background:linear-gradient(180deg,{PAPEL} 40%,#E6D8C0 100%)"></div>
{pilula(CAFE, PAPEL)}
<div class=abs style="left:0;right:0;top:124px;text-align:center">
  <span class=p style="display:inline-block;background:{MARCA};font-size:60px;font-style:italic;font-weight:700;padding:4px 30px 10px">Você sabia?</span>
  <div style="font:300 76px/1.14 Inter;letter-spacing:-.02em;margin-top:18px">{frase}</div>
  <div style="display:inline-flex;align-items:center;gap:10px;margin-top:24px;font:400 30px Inter">{BALAO}leia a legenda</div>
</div>
{objeto}
<svg class=abs style="left:0;top:0;filter:drop-shadow(0 12px 14px rgb(0 0 0/.35))" width="1080" height="1440" viewBox="0 0 1080 1440" fill="none">
<defs><linearGradient id="fi" x1="0" x2="1" y1="0" y2=".3"><stop offset="0" stop-color="#c9a14e"/><stop offset=".25" stop-color="#f9efc2"/><stop offset=".5" stop-color="#d8b566"/><stop offset=".75" stop-color="#f1dfa2"/><stop offset="1" stop-color="#c9a14e"/></linearGradient>
<path id="cu" d="M-60 1200C200 1520 560 1480 780 1300C960 1150 1090 1000 1160 980"/></defs>
<use href="#cu" stroke="url(#fi)" stroke-width="66"/>
<text font-family="Inter" font-weight="700" font-size="32" letter-spacing="2.5" fill="{CAFE}" dy="11"><textPath href="#cu">{texto}</textPath></text></svg>""")


def repetida(numero, apoio, base, palavra, objeto, tam=300):
    """Layout 09: número grande, palavra repetida ao fundo e objeto na frente."""
    fantasma = "".join(f'<div class=p style="font-size:{tam}px;line-height:.98;font-weight:500;letter-spacing:-.02em;white-space:nowrap;color:#E9DCC0;margin-left:-20px">{palavra}</div>' for _ in range(3))
    return lambda: ("", f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
<div class=abs style="left:0;top:540px">{fantasma}</div>
{topo(CAFE)}
<div class="abs p" style="left:0;right:0;top:136px;text-align:center;font-size:168px;line-height:1.06;font-weight:400">{numero}</div>
<div class=abs style="left:60px;right:60px;top:330px;text-align:center;font:300 42px/1.3 Inter;letter-spacing:.01em">{apoio}</div>
<div class=abs style="right:72px;top:488px;text-align:right;font:500 26px/1.3 Inter">{base}</div>
{objeto}
{rodape(CAFE)}""")


def mito(t1, t2, faixa, fileira, apoio):
    """Layout 13: título, faixa em itálico e fileira de objetos."""
    return lambda: ("", f"""
<div class=abs style="inset:0;background:linear-gradient(180deg,#fff,{AREIA})"></div>
{topo(CAFE)}
<div class=abs style="left:0;right:0;top:136px;text-align:center">
  <div class=p style="font-size:128px;line-height:1.06;font-style:italic;font-weight:600">{t1}</div>
  <div style="font:300 90px/1.2 Inter;letter-spacing:-.03em">{t2}</div>
  <div class=p style="display:inline-block;background:{MARCA};font-size:62px;font-style:italic;font-weight:700;padding:6px 34px 12px;margin-top:30px;transform:rotate(-1deg)">{faixa}</div>
</div>
<div class=abs style="left:20px;top:650px;width:1040px;height:380px;display:flex;justify-content:center;align-items:center">{fileira}</div>
<div class=abs style="left:60px;right:60px;top:1060px;height:2px;background:{FOIL}"></div>
<div class=abs style="left:90px;right:90px;top:1104px;text-align:center;font:300 42px/1.35 Inter">{apoio}</div>
{rodape(CAFE)}""")


def celular(cabeca, linha, palavra, apoio):
    """Layout 11 sem foto: celular dourado sobre café, com o título dentro da tela."""
    return lambda: ("", f"""
<div class=abs style="inset:0;background:radial-gradient(70% 55% at 50% 48%,#5c4d40 0,#3a3028 55%,{FUNDO} 100%)"></div>
{pilula(AREIA)}
<div class=abs style="left:282px;top:220px;width:516px;height:1010px;border-radius:66px;background:{FOIL};box-shadow:0 30px 60px rgb(0 0 0/.55)"></div>
<div class=abs style="left:300px;top:238px;width:480px;height:974px;border-radius:52px;background:#14100d"></div>
<div class=abs style="left:318px;top:256px;width:444px;height:938px;border-radius:40px;background:{PAPEL};color:{CAFE};padding:110px 34px 0;text-align:center">
  <div style="position:absolute;left:172px;top:20px;width:100px;height:28px;border-radius:14px;background:#14100d"></div>
  <div style="font:500 24px Inter;letter-spacing:.06em">{cabeca}</div>
  <div class=p style="font-size:52px;line-height:1.14;font-weight:500;margin-top:40px">{linha}</div>
  <div class=p style="display:inline-block;background:{MARCA};font-size:64px;line-height:1.3;font-style:italic;font-weight:700;padding:0 18px;white-space:nowrap;margin-top:14px">{palavra}</div>
  <div style="font:400 29px/1.38 Inter;margin-top:34px">{apoio}</div>
  <div style="display:inline-flex;align-items:center;gap:10px;font:500 25px Inter;margin-top:34px">{BALAO}leia a legenda</div>
</div>""")


def empilhado(l1, italico, apoio, direita, fundo_claro=False):
    """Layouts 04/12: título empilhado à esquerda, objeto à direita."""
    cor, txt = (PAPEL, CAFE) if fundo_claro else (FUNDO, "#fff")
    fundo = (f"background:linear-gradient(160deg,#fff 0,{AREIA} 100%)" if fundo_claro
             else f"background:radial-gradient(80% 60% at 80% 55%,#5c4d40 0,#3a3028 55%,{FUNDO} 100%)")
    return lambda: ("", f"""
<div class=abs style="inset:0;{fundo}"></div>
{direita}
{topo(CAFE if fundo_claro else AREIA)}
<div class=abs style="left:72px;top:330px;width:640px;color:{txt}">
  <div style="font:300 42px/1.25 Inter;letter-spacing:.01em">{l1}</div>
  <div class=p style="font-size:124px;line-height:1.06;font-style:italic;font-weight:400;margin-top:24px">{italico}</div>
  <div style="margin-top:40px;font:400 34px/1.4 Inter;width:540px;padding-top:18px;border-top:3px solid #c9a14e">{apoio}</div>
</div>
{rodape(CAFE if fundo_claro else AREIA)}""")


def caderno(l1, grande, italico, margem1, margem2):
    """Layout 02: caderno inclinado com espiral e caneta."""
    from gerar import caderno as base
    css, corpo = base()
    corpo = (corpo.replace("CLÁUSULA 1ª. PEDIDO DE DEMISSÃO. A EMPREGADA DECLARA, POR LIVRE E ESPONTÂNEA", margem1)
             .replace("CLÁUSULA 2ª. NADA MAIS HAVENDO A RECLAMAR, A EMPREGADA DÁ PLENA QUITAÇÃO", margem2)
             .replace(">A gestante<", f">{l1}<").replace("NÃO LEU, MAS<br>ASSINOU:", grande).replace(">e agora?<", f">{italico}<"))
    return lambda: (css, corpo)


def faixa_frase(frase, faixa, objeto, apoio):
    """Layout 05: frase, faixa em itálico, objeto e apoio."""
    return lambda: ("", f"""
<div class=abs style="inset:0;background:{FUNDO}"></div>
{objeto}
{pilula(AREIA)}
<div class=abs style="left:0;right:0;top:138px;text-align:center;font:300 62px Inter;letter-spacing:-.015em;color:#fff">{frase}</div>
<div class="abs p" style="left:62px;right:62px;top:232px;text-align:center;background:{MARCA};color:{CAFE};font-size:104px;line-height:1.28;font-style:italic;font-weight:700;transform:rotate(-1deg)">{faixa}</div>
<div class=abs style="left:110px;right:110px;top:1170px;text-align:center;font:300 36px/1.38 Inter;color:#fff">{apoio}</div>
{rodape(AREIA)}""")


def dias(n, marcados, rotulo):
    """Fileira de dias de calendário em cartões cor de papel; marcados em ouro."""
    return "".join(f'<div style="width:112px;height:132px;margin:8px;border-radius:14px;background:{MARCA if i in marcados else PAPEL};box-shadow:0 8px 16px rgb(30 24 20/.22);display:flex;flex-direction:column;align-items:center;justify-content:center;font:600 46px Inter;color:{CAFE}">{i + 1}<span style="font:500 22px Inter;opacity:.7">{rotulo(i)}</span></div>' for i in range(n))


SEM = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]

LOTE2 = {
    "manchete-14-atestado": faixa_frase("o atestado do posto de saúde", "não vale?", obj("obj-atestado-rosa.png", "left:240px;top:420px;width:600px;transform:rotate(-7deg)", 900),
                                        "Atestado médico, inclusive do SUS, comprova a doença. Falta assim não pode ser descontada."),
    "manchete-15-holerite": repetida("46 HORAS:", "A MAIS NO MÊS. NO HOLERITE,<br><b style='font-weight:600'>HORA EXTRA: R$ 0,00.</b>", "Constituição, art. 7º, XVI", "HORAS",
                                     obj("corte-calculadora.png", "left:250px;top:640px;width:600px;transform:rotate(-10deg)", 900)),
    "manchete-16-ponto": caderno("Ponto igual", "TODO DIA VALE<br>COMO PROVA?", "nem sempre", "SEG 08:00 17:00 · TER 08:00 17:00 · QUA 08:00 17:00 · QUI 08:00 17:00",
                                 "SAÍDA DE VERDADE: 18:40 · 19:15 · 20:10 · TST, SÚMULA 338, III"),
    "manchete-17-demissao": escuro("“Pede demissão,", "é melhor", "<b style='font-weight:600'>pra você</b>”", "Pra quem?",
                                   obj("corte-carimbo.png", "left:290px;top:150px;width:500px;transform:rotate(-12deg)", 800)),
    "manchete-18-ferias": mito("Vender os 30", "dias de <i class=p style='font-weight:600'>férias?</i>", "Só 10 podem",
                               dias(6, {0, 1}, lambda i: "VENDE" if i < 2 else "FOLGA").replace("width:112px", "width:140px"),
                               "Dá para vender no máximo 1/3 das férias. E a escolha é sua, não da empresa."),
    "manchete-19-almoco": pontilhado("Almoço de<br><i style='font-weight:500'>20 minutos?</i>", "Mais de 6 horas: 1 hora de intervalo",
                                     f'<div class=abs style="left:290px;top:600px;width:500px;height:500px;border-radius:50%;background:{PAPEL};border:22px solid #c9a14e;box-shadow:0 24px 44px rgb(30 24 20/.3);display:flex;align-items:center;justify-content:center;flex-direction:column"><div class=p style="font-size:150px;line-height:1">20:00</div><div style="font:500 28px Inter;letter-spacing:.1em;margin-top:10px">DE 60 MINUTOS</div></div>', "CLT, art. 71"),
    "manchete-20-experiencia": repetida("90 DIAS:", "É O MÁXIMO DA EXPERIÊNCIA.<br><b style='font-weight:600'>PRORROGAR NÃO PASSA DISSO.</b>", "CLT, arts. 445 e 451", "PRAZO",
                                        obj("corte-ampulheta.png", "left:330px;top:600px;width:420px;transform:rotate(-8deg)", 700)),
    "manchete-21-por-fora": pontilhado("Um salário no holerite,<br><i style='font-weight:500'>outro no Pix?</i>", "Pago por fora também é salário",
                                       obj("obj-envelope.png", "left:240px;top:600px;width:600px;transform:rotate(-7deg)", 900), "CLT, art. 457"),
    "manchete-22-sem-carteira": sabia("Experiência <b style='font-weight:600;border-bottom:7px solid;border-image:" + FOIL + " 1'>sem carteira</b><br>não existe",
                                      "CARTEIRA ASSINADA", obj("corte-pasta.png", "left:250px;top:590px;width:580px;transform:rotate(-6deg)", 900)),
    "manchete-23-salario-atrasado": escuro("Salário depois do", "5º dia útil", "<b style='font-weight:600'>está</b> atrasado", "",
                                           obj("corte-cofrinho.png", "left:300px;top:150px;width:480px;transform:rotate(-8deg)", 800),
                                           "Atraso repetido pode permitir a rescisão indireta, a “justa causa do patrão”."),
    "manchete-24-fgts": empilhado("A EMPRESA DEPOSITOU<br>O SEU", "FGTS<br>ESTE<br>MÊS?", "São 8% do salário, todo mês. Confira no aplicativo FGTS.",
                                  obj("corte-reais.png", "left:560px;top:520px;width:640px;transform:rotate(-16deg)", 900)),
    "manchete-25-sem-folga": mito("14 dias", "seguidos, <i class=p style='font-weight:600'>sem folga?</i>", "Quando é a folga?",
                                  f'<div style="display:flex;flex-wrap:wrap;width:900px;justify-content:center">{dias(14, set(range(14)), lambda i: SEM[i % 7])}</div>'.replace("width:112px;height:132px", "width:104px;height:116px"),
                                  "Todo trabalhador tem direito a 24 horas seguidas de descanso por semana."),
    "manchete-26-aviso-previo": sabia("Aviso prévio <b style='font-weight:600;border-bottom:7px solid;border-image:" + FOIL + " 1'>tem redução</b><br>de jornada",
                                      "2 HORAS POR DIA OU 7 DIAS", obj("corte-prancheta.png", "left:280px;top:580px;width:520px;transform:rotate(-7deg)", 800)),
    "manchete-27-lavar-banheiro": empilhado("CONTRATADA COMO<br>RECEPCIONISTA,", "LAVA O<br>BANHEIRO?",
                                            "Banheiro de grande circulação dá adicional de insalubridade de 40%.",
                                            f'<div class=abs style="left:760px;top:820px;width:260px;padding:40px 20px;border-radius:22px;background:{PAPEL};text-align:center;transform:rotate(8deg);box-shadow:0 22px 40px rgb(0 0 0/.45)"><div style="width:70px;height:18px;border-radius:9px;background:{FUNDO};margin:0 auto 26px"></div><div style="font:600 22px Inter;letter-spacing:.12em;color:{CAFE};opacity:.7">CRACHÁ</div><div class=p style="font-size:44px;color:{CAFE};margin-top:10px">Recep-<br>cionista</div></div>'),
    "manchete-28-pensao": escuro("Pensão", "atrasada?", "<b style='font-weight:600'>não é favor:</b> é direito da criança", "",
                                 obj("obj-ursinho2.png", "left:330px;top:140px;width:420px", 700),
                                 "Com acordo ou decisão da Justiça, o atraso pode ser cobrado no processo."),
    "manchete-29-guarda": faixa_frase("a guarda é compartilhada, mas a", "rotina é só sua?",
                                      obj("obj-mae-filha.png", "left:250px;top:440px;width:580px", 900),
                                      "Compartilhada quer dizer responsabilidade dos dois: decisões, cuidados e deveres."),
    "manchete-30-ferias-natal": celular("MENSAGEM DO PAI", "“Vou levar no Natal e no", "Ano‑Novo”",
                                        "Pode, sem combinar? Depende do acordo de convivência. O que está nele vale para os dois."),
    "manchete-31-decimo-terceiro": repetida("13º:", "1ª PARCELA ATÉ 30/11, 2ª ATÉ 20/12.<br><b style='font-weight:600'>OS DESCONTOS FICAM NA SEGUNDA.</b>", "Lei 4.749/1965", "PARCELA",
                                            obj("corte-reais.png", "left:60px;top:690px;width:960px;transform:rotate(-8deg)", 1000), 260),
    "manchete-32-temporario": mito("Temporário", "tem <i class=p style='font-weight:600'>direitos?</i>", "Mito ou Realidade?",
                                   "".join(f'<div style="width:220px;height:260px;margin:0 10px;border-radius:18px;background:{MARCA if i % 2 == 0 else PAPEL};box-shadow:0 14px 26px rgb(30 24 20/.25);display:flex;align-items:center;justify-content:center;text-align:center;transform:rotate({r}deg)"><span class=p style="font-size:44px;line-height:1.1;font-style:italic;font-weight:600">{t}</span></div>' for i, (t, r) in enumerate([("FGTS", -4), ("13º", 3), ("Férias<br>+ 1/3", -2), ("Salário<br>igual", 4)])),
                                   "Realidade: FGTS, 13º, férias com 1/3 e salário igual ao do efetivo."),
    "manchete-33-licenca-180": pontilhado("180 dias de licença<br><i style='font-weight:500'>para todas?</i>", "A regra é 120. Os 180 têm condição",
                                          obj("corte-sapatinho.png", "left:250px;top:610px;width:580px;transform:rotate(-6deg)", 900), "Lei 11.770/2008 (Empresa Cidadã)"),
    "manchete-34-fim-6x1": empilhado("A PARTIR DE 16/12/2026,", "DUAS<br>FOLGAS<br>POR<br>SEMANA", "Até 42 horas por semana, sem redução do salário (EC 141).",
                                     f'<div class=abs style="left:700px;top:430px;width:300px;display:flex;flex-direction:column;align-items:center">{dias(7, {5, 6}, lambda i: SEM[i]).replace("width:112px;height:132px", "width:230px;height:84px").replace("flex-direction:column", "flex-direction:row;gap:16px")}</div>',
                                     fundo_claro=True),
}
