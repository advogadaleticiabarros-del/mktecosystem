"""Flagrante 31 · Story na praia no dia do atestado (Manchete 11)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.6, "whoosh", .5), (1.4, "pop"), (4.4, "carimbo"), (5.0, "erro", .5)]
EP = {
    "nome": "31-story",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#cel{position:absolute;left:330px;width:420px;top:340px;height:620px;border-radius:44px;background:linear-gradient(112deg,#a57a2c,#f9efc2 30%,#bb923f);padding:12px;box-shadow:0 20px 40px rgb(0 0 0/.5)}
#tela{width:100%;height:100%;border-radius:34px;background:linear-gradient(180deg,#5d8aa8,#e9d7a8 70%,#d9c08a);position:relative;overflow:hidden}
#bar{position:absolute;left:20px;right:20px;top:18px;height:6px;border-radius:3px;background:rgb(255 255 255/.4)}#bar i{display:block;height:100%;width:0;background:#fff;border-radius:3px}
#leg{position:absolute;left:0;right:0;top:260px;text-align:center;font:600 46px Inter;color:#1E1814}
#at{top:760px;left:170px;width:420px}#q{top:1020px}#s{top:1146px}""",
    "html": """<div class=rot id=r1>terça · atestado de 2 dias</div>
<div id=cel data-m=1><div id=tela><div id=bar><i id=bi></i></div><div id=leg>dia de praia</div></div></div>
<div class=card id=at><div class=t><span>ATESTADO</span><b>2 dias</b></div><div class=m>Repouso absoluto.</div></div>
<div class=marca id=q><span>Vira prova?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);sobe('cel',t,.6,.5);$('bi').style.width=cl((t-1)/5)*100+'%';sobe('leg',t,1.4);
 nasce('at',t,4.4);$('at').style.transform+=' rotate(-6deg)';marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[4.4])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-11-story"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
