"""Dia 13 · Aviso prévio no horário normal. RH manda cumprir o aviso sem redução; aparecem as duas opções da lei."""
from motor import rodar

EP = {
    "nome": "13-aviso-previo",
    "dur": 20.0,
    "salve": "",
    "css": """#c0{top:300px}#r1{top:510px}#rel{top:560px;font-size:170px}
#op{position:absolute;left:150px;width:780px;top:780px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
#op div{border:3px solid #bb923f;border-radius:20px;padding:16px 18px;text-align:center;font:400 30px/1.3 Inter}
#op b{display:block;font:500 50px/1.1 'EB Garamond',serif;color:#d8b566}
#q{top:1010px}#s{top:1136px}""",
    "html": """<div class=card id=c0><div class=t><span>RH</span><b>agora</b></div><div class=m>Você vai cumprir o aviso trabalhando no horário normal.</div></div>
<div class=rot id=r1>saída no aviso prévio</div><div class=big id=rel data-m=1>17:00</div>
<div id=op><div id=o1><b>2h a menos</b>por dia, sem desconto</div><div id=o2><b>7 dias</b>corridos de folga no fim</div></div>
<div class=marca id=q><span>Horário normal?</span></div><div class=sub id=s>Não. Quando a empresa dispensa,<br>a escolha entre as duas é sua.</div>""",
    "js": """function cena(t){
 nasce('c0',t,.5);sobe('r1',t,2.4);sobe('rel',t,2.5);
 const h=17-2*ioo((t-6.0)/1.0),hh=Math.floor(h),mm=Math.round((h-hh)*60)%60;$('rel').textContent=pad(hh+(mm>59?1:0))+':'+pad(mm);
 $('rel').style.color=t>7?'#d8b566':'';
 marca('q',t,4.0);sobe('o1',t,6.0);sobe('o2',t,7.4);sobe('s',t,9.4);
 $('cena').style.transform=`translateX(${treme(t,[.5])}px)`;
}""",
    "sons": [(.5, "pop"), (.5, "vibra"), (2.5, "tique"), (3.95, "whoosh"), (4.1, "escreve"), (4.6, "brilho", .7),
             (6.0, "relogio", .7), (7.0, "sino", .7), (7.4, "pagina"), (9.4, "boom", .5), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "RH: \"Você vai cumprir o aviso trabalhando no horário normal.\"\n\nHorário normal? Não.\n\nQuando é a empresa que dispensa e o aviso prévio é trabalhado, a CLT (art. 488) garante uma redução, sem desconto no salário. A escolha é do trabalhador:\n📌 Sair 2 horas mais cedo todos os dias do aviso, ou\n📌 Trabalhar no horário normal e folgar os últimos 7 dias corridos\n\nO que vale saber:\n📌 Se a empresa não concede a redução, o aviso pode ser considerado não cumprido\n📌 Isso vale para o aviso dado pela empresa, não para o pedido de demissão\n📌 Guarde a comunicação do aviso e anote os horários\n\nComente se você sabia disso. E mande para quem está cumprindo aviso.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #avisoprevio #clt #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
