"""Flagrante 18 · 13º salário. As datas viram, as duas parcelas caem e a segunda chega menor por causa dos descontos."""
from motor import rodar

EP = {
    "nome": "18-decimo-terceiro",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#dt{top:330px;font-size:190px}#c0{top:560px}#c1{top:710px}
.card .m b{font-weight:600}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>13º salário · prazo da 1ª parcela</div><div class=big id=dt data-m=1>25/11</div>
<div class=card id=c0><div class=t><span>Banco</span><b>30/11</b></div><div class=m>13º · 1ª parcela: <b>R$ 1.200,00</b></div></div>
<div class=card id=c1><div class=t><span>Banco</span><b>20/12</b></div><div class=m>13º · 2ª parcela: <b>R$ 1.010,00</b></div></div>
<div class=marca id=q><span>Por que veio menor?</span></div><div class=sub id=s>Porque os descontos ficam nela. Leia a legenda.</div>""",
    "js": """const D1=['25/11','26/11','27/11','28/11','29/11','30/11'],D2=['15/12','16/12','17/12','18/12','19/12','20/12'];
function cena(t){
 sobe('r1',t,.1);sobe('dt',t,.2);
 let d;if(t<4.2){d=D1[Math.min(5,Math.floor(Math.max(0,t-.6)/.45))];$('r1').textContent='13º salário · prazo da 1ª parcela'}
 else{d=D2[Math.min(5,Math.floor(Math.max(0,t-4.4)/.4))];$('r1').textContent='13º salário · prazo da 2ª parcela'}
 $('dt').textContent=d;$('dt').style.color=d==='30/11'||d==='20/12'?'#d8b566':'';
 nasce('c0',t,3.0);nasce('c1',t,6.8);
 marca('q',t,8.8);sobe('s',t,10.6);
 $('cena').style.transform=`translateX(${treme(t,[3.0,6.8])}px)`;
}""",
    "sons": [(.6 + i * .45, "tique", .7) for i in range(6)] + [(3.0, "pop"), (3.0, "moedas")]
            + [(4.4 + i * .4, "tique", .7) for i in range(6)] + [(6.8, "pop"), (6.8, "moedas", .6), (7.3, "erro", .5),
               (8.75, "whoosh"), (8.9, "escreve"), (9.4, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/13-salario-como-calcular-segunda-parcela-descontos.html",
                "legenda": "30/11: 1ª parcela do 13º, R$ 1.200.\n20/12: 2ª parcela, R$ 1.010.\n\nPor que a 2ª vem menor?\n\nPorque os descontos ficam nela. A 1ª parcela é metade do 13º, sem descontos, e deve ser paga até 30 de novembro. A 2ª deve ser paga até 20 de dezembro, e é nela que saem o INSS e o Imposto de Renda de todo o 13º (Lei 4.749/1965).\n\nO que vale saber:\n📌 Quem trabalhou parte do ano recebe proporcional: 1/12 por mês com 15 dias ou mais trabalhados\n📌 Horas extras, adicional noturno e comissões frequentes entram na conta\n📌 Atraso no pagamento pode gerar multa\n📌 Confira o valor no holerite das duas parcelas\n\nO valor do exemplo é ilustrativo, para um salário de R$ 2.400. O link do artigo completo está no primeiro comentário.\n\nComente: a sua 1ª parcela já caiu? E mande para quem vai receber o 13º.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #13salario #decimoterceiro #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
