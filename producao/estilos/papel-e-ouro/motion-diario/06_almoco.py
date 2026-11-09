"""Dia 6 · Almoço de 20 minutos. Cronômetro corre, o chefe chama de volta, a barra mostra o que faltou."""
from motor import rodar

EP = {
    "nome": "06-almoco",
    "dur": 20.0,
    "salve": "Salve e mande para quem almoça correndo.",
    "css": """#r1{top:290px}#cr{top:340px}#c0{top:600px}
#bar{position:absolute;left:150px;width:780px;top:820px;height:44px;border-radius:22px;background:rgb(239 230 217/.12);overflow:hidden}
#bar i{position:absolute;top:0;bottom:0;border-radius:22px}
#b1{left:0;width:33.3%}#b2{left:33.3%;width:66.7%;background:repeating-linear-gradient(45deg,rgb(239 230 217/.25) 0 10px,transparent 10px 22px)}
#lb{position:absolute;left:150px;width:780px;top:880px;display:flex;justify-content:space-between;font:500 30px Inter}
#q{top:1010px}#s{top:1136px}""",
    "html": """<div class=rot id=r1>intervalo de almoço</div><div class=big id=cr data-m=1>00:00</div>
<div class=card id=c0><div class=t><span>Chefe</span><b>agora</b></div><div class=m>Já pode voltar? Tá cheio aqui.</div></div>
<div id=bar><i id=b1></i><i id=b2></i></div><div id=lb><span id=l1>20 min</span><span id=l2 class=ouro>faltaram 40 min</span></div>
<div class=marca id=q><span>Isso é normal?</span></div><div class=sub id=s>Comente quanto tempo você tem de almoço.</div>""",
    "js": """const FOIL=getComputedStyle(document.querySelector('.fx')).backgroundImage;$('b1').style.background=FOIL;
function cena(t){
 sobe('r1',t,.2);sobe('cr',t,.3);const m=20*ioo((t-.6)/3.8),mm=Math.floor(m),ss=Math.floor((m-mm)*60);$('cr').textContent=pad(mm)+':'+pad(t>4.4?0:ss);
 $('cr').style.color=t>4.4?'#d8b566':'';nasce('c0',t,4.6);
 sobe('bar',t,6.6);$('b1').style.clipPath=`inset(0 ${(1-ioo((t-6.8)/.6))*100}% 0 0)`;$('b2').style.opacity=cl((t-7.6)/.4);
 sobe('l1',t,7.2);sobe('l2',t,7.9);
 marca('q',t,9.8);sobe('s',t,11.6);
 $('cena').style.transform=`translateX(${treme(t,[4.6])}px)`;
}""",
    "sons": [(.6, "relogio", .9), (4.4, "sino"), (4.6, "pop"), (4.6, "vibra"), (6.8, "whoosh", .5),
             (7.9, "erro", .6), (9.75, "whoosh"), (9.9, "escreve"), (10.4, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "Sentou para almoçar.\n20 minutos depois: \"Já pode voltar? Tá cheio aqui.\"\n\nIsso é normal?\n\nPela CLT (art. 71), quem trabalha mais de 6 horas por dia tem direito a no mínimo 1 hora de intervalo.\n\nO que vale saber:\n📌 Jornada de 4 a 6 horas: intervalo de 15 minutos\n📌 Intervalo cortado: a empresa deve pagar o tempo que faltou, com 50% a mais\n📌 Redução só em casos que a lei permite, como por acordo coletivo\n📌 Anote os dias em que o almoço foi interrompido\n\nComente quanto tempo você tem de almoço. E mande para quem almoça correndo.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #intervalo #clt #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
