"""Flagrante 32 · O pai não paga a pensão; a avó pode ser chamada? (Manchete 12)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.5, "pop"), (.5, "vibra"), (3.2, "relogio", .6), (6.0, "erro", .5)]
EP = {
    "nome": "32-avo",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#c0{top:336px}#pn{top:560px;font-size:200px}#pl{top:770px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>mensagem do pai</div>
<div class=card id=c0><div class=t><span>Pai</span><b>agora</b></div><div class=m>Tô sem trabalho. Não tenho como pagar nada.</div></div>
<div class="big ouro" id=pn data-m=1>0</div><div class=rot id=pl>meses sem pensão</div>
<div class=marca id=q><span>E a avó?</span></div><div class=sub id=s>A lei prevê um caminho. Leia a legenda.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('c0',t,.5);sobe('pn',t,3.0);sobe('pl',t,3.2);$('pn').textContent=Math.round(8*ioo((t-3.2)/2.6));
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[.5,6.0])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-12-avo"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
