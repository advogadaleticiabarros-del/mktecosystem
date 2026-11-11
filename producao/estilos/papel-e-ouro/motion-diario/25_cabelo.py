"""Flagrante 25 · 'Alisa o cabelo, fica mais profissional.' Discriminação pela aparência (Manchete 04)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.6, "pop"), (.6, "vibra"), (2.4, "pop"), (4.0, "digita", .6), (5.0, "bolha")]
EP = {
    "nome": "25-cabelo",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#b1{top:350px}#b2{top:520px}#b3{top:690px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>conversa com a gerente</div>
<div class="bo ele" id=b1>Aqui a gente pede cabelo alinhado.<small>08:02</small></div>
<div class="bo ele" id=b2>Alisa, que fica mais profissional.<small>08:02</small></div>
<div class="bo eu" id=b3>Meu cabelo é assim.<small>08:05</small></div>
<div class=marca id=q><span>Ela pode exigir?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('b1',t,.6);nasce('b2',t,2.4);nasce('b3',t,5.0);
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[2.4])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-04-cabelo"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
