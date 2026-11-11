"""Flagrante 26 · Amigo secreto da firma 'obrigatório', com desconto na folha (Manchete 05)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.5, "pop"), (.5, "vibra"), (3.6, "moedas"), (5.6, "erro", .6)]
EP = {
    "nome": "26-amigo-secreto",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#c0{top:336px}#pn{top:600px;font-size:190px}#pl{top:810px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>grupo da firma</div>
<div class=card id=c0><div class=t><span>Gerência</span><b>agora</b></div><div class=m>Amigo secreto obrigatório. Quem não entrar, a gente desconta da folha.</div></div>
<div class="big ouro" id=pn data-m=1>R$ 0</div><div class=rot id=pl>descontados do salário</div>
<div class=marca id=q><span>Pode descontar?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('c0',t,.5);sobe('pn',t,3.4);sobe('pl',t,3.6);$('pn').textContent='R$ '+Math.round(100*ioo((t-3.6)/1.8));
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[.5,5.6])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-05-amigo-secreto"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
