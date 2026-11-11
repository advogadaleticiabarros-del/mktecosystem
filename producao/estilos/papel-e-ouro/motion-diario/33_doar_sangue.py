"""Flagrante 33 · Doar sangue e o gerente diz que é falta (Manchete 13)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.6, "bolha"), (2.6, "pop"), (2.6, "vibra"), (5.0, "brilho", .6)]
EP = {
    "nome": "33-doar-sangue",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#b1{top:350px}#b2{top:540px}#pn{top:720px;font-size:180px}#pl{top:900px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>conversa com o gerente</div>
<div class="bo eu" id=b1>Amanhã vou doar sangue de manhã.<small>17:50</small></div>
<div class="bo ele" id=b2>Vai ser falta, viu?<small>17:52</small></div>
<div class="big ouro" id=pn data-m=1>1 dia</div><div class=rot id=pl>a cada 12 meses, sem desconto</div>
<div class=marca id=q><span>Mito ou realidade?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('b1',t,.6);nasce('b2',t,2.6);sobe('pn',t,5.0,.5);sobe('pl',t,5.3);
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[2.6])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-13-doar-sangue"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
