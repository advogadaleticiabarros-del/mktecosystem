"""Dia 8 · Salário por fora. Holerite de R$ 1.800 + Pix de R$ 1.200 "por fora"; direitos calculados só sobre 1.800."""
from motor import rodar

EP = {
    "nome": "08-por-fora",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:290px}#c0{top:350px}#c1{top:500px}#tot{top:660px;font-size:170px}
#base{position:absolute;left:150px;right:150px;top:880px;text-align:center;font:400 32px/1.35 Inter}
#base b{font-weight:600;color:#d8b566}
#q{top:1030px}#s{top:1160px}""",
    "html": """<div class=rot id=r1>salário de março</div>
<div class=card id=c0><div class=t><span>Holerite</span><b>dia 5</b></div><div class=m>Salário: R$ 1.800,00</div></div>
<div class=card id=c1><div class=t><span>Pix recebido</span><b>agora</b></div><div class=m>R$ 1.200,00 · “o resto, por fora”</div></div>
<div class="big ouro" id=tot data-m=1>R$ 0</div>
<div id=base>FGTS, férias e 13º calculados sobre:<br><b>R$ 1.800</b></div>
<div class=marca id=q><span>Quem perde com isso?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.2);nasce('c0',t,.6);nasce('c1',t,2.4);
 sobe('tot',t,4.2);const v=Math.round(3000*ioo((t-4.3)/1.6));$('tot').textContent='R$ '+v.toLocaleString('pt-BR');
 sobe('base',t,7.0);
 const dim=1-.55*ioo((t-9.6)/.6);['c0','c1','tot'].forEach(i=>$(i).style.filter=`brightness(${dim})`);
 marca('q',t,10.0);sobe('s',t,11.8);
 $('cena').style.transform=`translateX(${treme(t,[2.4,7.6])}px)`;
}""",
    "sons": [(.6, "pagina"), (2.4, "pop"), (2.4, "vibra"), (4.3, "moedas"), (5.9, "carimbo", .7), (7.0, "escreve", .6),
             (7.6, "erro", .7), (9.95, "whoosh"), (10.1, "escreve"), (10.6, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "No holerite: R$ 1.800.\nNo Pix: R$ 1.200 \"por fora\".\n\nQuem perde com isso?\n\nO valor pago por fora também é salário (CLT, art. 457). Quando ele não aparece no holerite, os direitos são calculados só sobre a parte registrada.\n\nO que vale saber:\n📌 FGTS, férias, 13º e horas extras ficam menores\n📌 O INSS também é recolhido a menos, o que pesa na aposentadoria e no auxílio-doença\n📌 Pix, depósitos e mensagens ajudam a provar o valor real\n📌 Guarde os comprovantes de todos os meses\n\nComente o que você acha. E mande para quem recebe parte do salário por fora.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #salario #fgts #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
