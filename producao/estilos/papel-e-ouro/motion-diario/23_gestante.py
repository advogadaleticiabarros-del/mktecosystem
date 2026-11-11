"""Flagrante 23 · Gestante dispensada sem saber da gravidez. Dispensa num dia, exame positivo depois (Manchete 01)."""
from manchete_leg import legenda
from motor import rodar

SONS = [(.5, "pop"), (.5, "vibra"), (3.6, "pagina"), (6.2, "carimbo")]
EP = {
    "nome": "23-gestante",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#c0{top:336px}#ex{position:absolute;left:250px;width:580px;top:560px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:22px 30px;text-align:center;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#ex h3{font:600 22px Inter;letter-spacing:.12em;opacity:.6}#ex p{font:500 64px/1.1 'EB Garamond',serif;margin-top:6px}#ex small{font:400 28px Inter;opacity:.7}
#st{position:absolute;left:300px;top:820px;font:700 40px Inter;letter-spacing:.14em;color:#bb923f;border:5px solid #bb923f;border-radius:10px;padding:6px 18px;transform:rotate(-10deg)}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>segunda · 17h40</div>
<div class=card id=c0><div class=t><span>RH</span><b>agora</b></div><div class=m>Sua dispensa sai hoje. Passa aqui pra assinar.</div></div>
<div id=ex data-m=1><h3>EXAME · 4 DIAS DEPOIS</h3><p>Positivo</p><small>gravidez de 6 semanas</small></div><div id=st>NÃO AVISOU</div>
<div class=marca id=q><span>Tem estabilidade?</span></div><div class=sub id=s>Mesmo sem ter avisado a empresa.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('c0',t,.5);sobe('ex',t,3.6,.5);
 const a=t-6.2;$('st').style.opacity=a<0?0:1;$('st').style.transform=`rotate(-10deg) scale(${a<0?1.6:1+.6*Math.max(0,1-a/.18)})`;
 marca('q',t,8.6);sobe('s',t,10.4);$('cena').style.transform=`translateX(${treme(t,[.5,6.2])}px)`;
}""",
    "sons": SONS + [(8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": legenda("manchete-01-te-disseram"),
}

if __name__ == "__main__":
    rodar(EP, __file__)
