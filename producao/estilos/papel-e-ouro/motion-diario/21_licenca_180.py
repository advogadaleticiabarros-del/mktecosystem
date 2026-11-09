"""Flagrante 21 · Licença-maternidade: 120 ou 180 dias? Artigo entre os mais vistos (Search Console, 24/10)."""
from motor import rodar

EP = {
    "nome": "21-licenca-180",
    "dur": 20.0,
    "salve": "",
    "css": """#c0{top:300px}#r1{top:470px}#ld{top:520px;font-size:190px}#mais{top:740px;font:italic 500 60px 'EB Garamond',serif}
#q{top:960px}#s{top:1086px}""",
    "html": """<div class=card id=c0><div class=t><span>Grupo da família</span><b>agora</b></div><div class=m>Viu? O STF deu 180 dias de licença pra todas!</div></div>
<div class=rot id=r1>licença-maternidade</div><div class=big id=ld data-m=1>0 dias</div>
<div class="sub ouro" id=mais>+ 60 dias?</div>
<div class=marca id=q><span>180 pra todas?</span></div><div class=sub id=s>Não. A regra continua 120 dias.<br>Os 180 valem em casos específicos.</div>""",
    "js": """function cena(t){
 nasce('c0',t,.5);sobe('r1',t,2.2);sobe('ld',t,2.3);
 const v=t<5.6?Math.round(120*ioo((t-2.5)/2.4)):Math.round(120+60*ioo((t-5.6)/1.0)*(t<10.6?1:1-ioo((t-10.6)/.8)));
 $('ld').textContent=v+' dias';$('ld').style.color=v>120?'#d8b566':'';
 sobe('mais',t,5.0);$('mais').style.opacity=t>10.6?cl(1-(t-10.6)/.5):$('mais').style.opacity;
 marca('q',t,7.6);sobe('s',t,10.6);
 $('cena').style.transform=`translateX(${treme(t,[.5,10.6])}px)`;
}""",
    "sons": [(.5, "pop"), (.5, "vibra"), (2.5, "relogio", .6), (4.9, "carimbo"), (5.0, "whoosh", .5), (5.6, "moedas", .6),
             (7.55, "whoosh"), (7.7, "escreve"), (8.2, "brilho", .7), (10.6, "erro", .6), (10.7, "boom", .4),
             (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/stf-licenca-maternidade-180-dias-o-que-mudou-de-verdade.html",
                "legenda": "\"Viu? O STF deu 180 dias de licença pra todas!\"\n\n180 pra todas? Não.\n\nA regra continua: 120 dias de licença-maternidade remunerada, para a mãe gestante e para a mãe adotante. O que o STF decidiu na ADI 7.495 foi impedir que a mãe adotante tenha licença menor que a gestante.\n\nO que vale saber:\n📌 Os 60 dias a mais (total de 180) valem quando a empresa participa do Programa Empresa Cidadã (Lei 11.770/2008)\n📌 Também valem quando há convenção coletiva ou regra interna mais vantajosa, e para servidoras com previsão própria\n📌 Pergunte ao RH se a empresa é Empresa Cidadã\n📌 A gestante tem estabilidade da confirmação da gravidez até 5 meses depois do parto\n\nO link do artigo completo está no primeiro comentário.\n\nComente se você sabia disso. E mande para uma futura mamãe.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#licencamaternidade #direitotrabalhista #gestante #maternidade #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
