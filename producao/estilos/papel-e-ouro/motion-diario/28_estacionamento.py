"""Flagrante 28 · Carro arrombado e a placa 'não nos responsabilizamos' (Manchete 07)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.6, "carimbo", .6), (3.0, "pop"), (3.0, "vibra"), (5.6, "erro", .6), (5.9, "carimbo", .5)]
EP = {
    "nome": "28-estacionamento",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#pl{position:absolute;left:190px;width:700px;top:340px;background:#EFE6D9;color:#1E1814;border:6px solid #1E1814;border-radius:8px;padding:26px;text-align:center;font:700 40px/1.25 Inter;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#c0{top:660px}#x{position:absolute;left:190px;width:700px;top:340px;height:230px}
#x i{position:absolute;left:50%;top:50%;width:700px;height:10px;background:#bb923f;border-radius:5px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>estacionamento do mercado</div>
<div id=pl data-m=1>NÃO NOS RESPONSABILIZAMOS POR OBJETOS DEIXADOS NO VEÍCULO</div>
<div class=card id=c0><div class=t><span>Você</span><b>18h12</b></div><div class=m>Arrombaram o meu carro aqui dentro. Levaram a mochila.</div></div>
<div id=x><i id=x1></i><i id=x2></i></div>
<div class=marca id=q><span>A placa livra?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);sobe('pl',t,.6,.5);nasce('c0',t,3.0);
 [['x1',18],['x2',-18]].forEach(([i,r],k)=>{const w=ioo((t-5.6-k*.3)/.4);$(i).style.opacity=t<5.6+k*.3?0:1;$(i).style.transform=`translate(-50%,-50%) rotate(${r}deg) scaleX(${w})`});
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[3.0,5.6,5.9])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-07-estacionamento"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
