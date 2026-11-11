"""Flagrante 29 · Revista íntima na saída do turno (Manchete 08)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.6, "pop"), (2.4, "pop"), (4.4, "relogio", .6), (6.8, "erro", .6)]
EP = {
    "nome": "29-revista",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#b1{top:350px}#b2{top:520px}#pn{top:700px;font-size:170px}#pl{top:880px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>saída do turno · 18h</div>
<div class="bo ele" id=b1>Abre a bolsa e levanta a blusa.<small>18:01</small></div>
<div class="bo ele" id=b2>É rotina. Todo dia é assim.<small>18:01</small></div>
<div class="big ouro" id=pn data-m=1>0</div><div class=rot id=pl>dias seguidos de revista</div>
<div class=marca id=q><span>Isso é rotina?</span></div><div class=sub id=s>A lei responde na legenda.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('b1',t,.6);nasce('b2',t,2.4);sobe('pn',t,4.2);sobe('pl',t,4.4);$('pn').textContent=Math.round(87*ioo((t-4.4)/2.4));
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[.6,6.8])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-08-revista"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
