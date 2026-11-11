"""Flagrante 30 · Faltou para o exame preventivo e o chefe quer descontar (Manchete 09)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.5, "pop"), (.5, "vibra"), (2.6, "tique"), (3.1, "tique"), (3.6, "tique"), (4.6, "brilho", .6)]
EP = {
    "nome": "30-exame",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#c0{top:336px}#ds{position:absolute;left:150px;width:780px;top:580px;display:flex;justify-content:center;gap:24px}
.d{width:200px;height:220px;border-radius:18px;background:#EFE6D9;color:#1E1814;display:flex;flex-direction:column;align-items:center;justify-content:center;font:500 90px/1 'EB Garamond',serif;box-shadow:0 14px 30px rgb(0 0 0/.35);position:relative;overflow:hidden}
.d small{font:600 22px Inter;letter-spacing:.1em;opacity:.65;margin-top:10px}.d i{position:absolute;inset:0;background:linear-gradient(112deg,#c9a14e,#f9efc2 40%,#d8b566);mix-blend-mode:multiply}
#pl{top:840px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>de volta do exame preventivo</div>
<div class=card id=c0><div class=t><span>Chefe</span><b>agora</b></div><div class=m>Exame de novo? Vou descontar o dia.</div></div>
<div id=ds data-m=1><div class=d id=d0>1<small>EXAME</small><i id=i0></i></div><div class=d id=d1>2<small>EXAME</small><i id=i1></i></div><div class=d id=d2>3<small>EXAME</small><i id=i2></i></div></div>
<div class=rot id=pl>dias por ano, sem desconto</div>
<div class=marca id=q><span>Pode descontar?</span></div><div class=sub id=s>A resposta está na legenda.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('c0',t,.5);
 [0,1,2].forEach(i=>{nasce('d'+i,t,2.6+i*.5);$('i'+i).style.clipPath=`inset(${(1-ioo((t-4.6-i*.4)/.5))*100}% 0 0 0)`});
 sobe('pl',t,6.2);marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[.5])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-09-exame"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
