"""Flagrante 24 · Gestante assina pedido de demissão 'só formalidade', sem sindicato (Manchete 02)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.5, "pop"), (2.6, "pagina"), (4.2, "assina"), (6.4, "erro", .6)]
EP = {
    "nome": "24-assinou",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#c0{top:336px}#doc{position:absolute;left:200px;width:680px;top:540px;height:400px;background:#EFE6D9;color:#1E1814;border-radius:10px;padding:30px 36px;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#doc h3{font:600 30px Inter;letter-spacing:.08em}#doc .l{height:14px;border-radius:7px;background:rgb(30 24 20/.15);margin-top:22px}
#ass{position:absolute;left:380px;top:770px}#ass path{stroke:#1E1814;stroke-width:4;fill:none;stroke-dasharray:400}
#sd{position:absolute;left:200px;width:680px;top:880px;text-align:right;font:600 28px Inter;color:#9a6a1f;padding-right:36px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>sala do RH</div>
<div class=card id=c0><div class=t><span>RH</span><b>agora</b></div><div class=m>Assina aqui. É só uma formalidade.</div></div>
<div id=doc data-m=1><h3>PEDIDO DE DEMISSÃO</h3><div class=l></div><div class=l style="width:85%"></div><div class=l></div><div class=l style="width:60%"></div></div>
<svg id=ass width=300 height=80><path d="M6 52c24-34 40-40 44-28s-16 34-20 26 26-26 38-20-6 24 4 22 18-18 30-16 2 14 14 12 22-10 44-14 40-10 60-12"/></svg>
<div id=sd>sindicato: ninguém</div>
<div class=marca id=q><span>Isso vale?</span></div><div class=sub id=s>Ela estava grávida.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('c0',t,.5);sobe('doc',t,2.6,.5);
 const w=cl((t-4.2)/1.4);$('ass').style.opacity=t<4.2?0:1;$('ass').querySelector('path').style.strokeDashoffset=400*(1-w);
 sobe('sd',t,6.4);marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[6.4])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-02-caderno"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
