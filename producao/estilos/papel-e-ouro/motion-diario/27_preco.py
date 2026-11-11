"""Flagrante 27 · Um preço na prateleira, outro no caixa (Manchete 06)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.6, "tique"), (2.6, "sino"), (3.0, "erro", .5), (4.8, "moedas")]
EP = {
    "nome": "27-preco",
    "dur": 20.0,
    "salve": "",
    "css": """.et{position:absolute;width:340px;top:420px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:22px;text-align:center;box-shadow:0 14px 34px rgb(0 0 0/.35)}
.et h3{font:600 22px Inter;letter-spacing:.12em;opacity:.6}.et p{font:500 84px/1.1 'EB Garamond',serif}
#e1{left:170px}#e2{left:570px}#e2 p{color:#9a2e1f}#r1{top:300px}#df{top:740px;font-size:150px}#dl{top:900px}#q{top:1020px}#s{top:1146px}""",
    "html": """<div class=rot id=r1>supermercado</div>
<div class=et id=e1 data-m=1><h3>PRATELEIRA</h3><p>9,90</p></div><div class=et id=e2 data-m=1><h3>CAIXA</h3><p>12,90</p></div>
<div class="big ouro" id=df>+R$ 3</div><div class=rot id=dl>a mais, sem ninguém avisar</div>
<div class=marca id=q><span>Qual preço vale?</span></div><div class=sub id=s>Comente o que você faria.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('e1',t,.6);nasce('e2',t,2.6);sobe('df',t,4.8);sobe('dl',t,5.0);
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[2.6])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-06-preco"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
