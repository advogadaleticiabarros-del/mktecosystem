"""Dia 10 · Salário atrasado. A data passa do 5º dia útil, o saldo continua zero e o atraso cresce."""
from motor import rodar

DIAS = ["06/03", "09/03", "10/03", "11/03", "12/03", "13/03"]
EP = {
    "nome": "10-salario-atrasado",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:290px}#dt{top:340px}#c0{top:600px}#at{top:760px}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>prazo do salário: 5º dia útil</div><div class=big id=dt data-m=1>06/03</div>
<div class=card id=c0><div class=t><span>Banco</span><b>agora</b></div><div class=m>Saldo disponível: R$ 0,00</div></div>
<div class=sub id=at>salário atrasado há <b id=n class=ouro>1</b> dia útil</div>
<div class=marca id=q><span>Até quando esperar?</span></div><div class=sub id=s>Comente se já aconteceu com você.</div>""",
    "js": """const D=%s;
function cena(t){
 sobe('r1',t,.2);sobe('dt',t,.3);const k=Math.min(D.length-1,Math.max(0,Math.floor((t-.8)/1.0)));$('dt').textContent=D[k];
 nasce('c0',t,.8);for(let i=1;i<D.length;i++)if(t>=.8+i&&t<.8+i+.35)$('c0').style.transform=`translateY(${-20*(1-mola((t-.8-i)/.35))}px)`;
 sobe('at',t,1.4);$('n').textContent=k+1;$('at').lastChild.textContent=k?' dias úteis':' dia útil';
 $('dt').style.color=k>=3?'#d8b566':'';
 marca('q',t,8.4);sobe('s',t,10.2);
 $('cena').style.transform=`translateX(${treme(t,[.8,1.8,2.8,3.8,4.8,5.8],3)}px)`;
}""" % ('["06/03","09/03","10/03","11/03","12/03","13/03"]'),
    "sons": [(.8 + i, "vibra", .8) for i in range(6)] + [(.8 + i, "bolha", .6) for i in range(6)]
            + [(6.9, "erro", .7), (8.35, "whoosh"), (8.5, "escreve"), (9.0, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "Prazo do salário: 5º dia útil.\nDia 06, 09, 10, 11, 12, 13...\nSaldo: R$ 0,00.\n\nAté quando esperar?\n\nPela CLT (art. 459), o salário mensal deve ser pago até o 5º dia útil do mês seguinte ao trabalhado.\n\nO que vale saber:\n📌 Atraso pode gerar multa prevista na convenção coletiva da categoria\n📌 Atrasos repetidos podem permitir a rescisão indireta, a \"justa causa do patrão\" (CLT, art. 483)\n📌 Guarde extratos e mensagens com as datas dos pagamentos\n📌 Não peça demissão por causa do atraso antes de se informar\n\nComente se já aconteceu com você. E mande para quem está com o salário atrasado.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #salarioatrasado #rescisaoindireta #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
