"""Flagrante 20 · Pausa para o banheiro proibida e exposta. Contagem das idas e mensagens do supervisor."""
from motor import rodar

EP = {
    "nome": "20-pausa-banheiro",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#ct{top:330px;font-size:150px}#b0{top:540px}#b1{top:660px}#b2{top:780px}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>idas ao banheiro hoje</div><div class=big id=ct data-m=1>0</div>
<div class="bo ele" id=b0>Já é a 3ª vez hoje.<small>14:05</small></div>
<div class="bo ele" id=b1>Agora só no intervalo.<small>14:05</small></div>
<div class="bo ele" id=b2>E seu nome vai pro quadro da equipe.<small>14:06</small></div>
<div class=marca id=q><span>Pode proibir?</span></div><div class=sub id=s>Comente se já viu isso no trabalho.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);sobe('ct',t,.2);const n=t<1?0:t<2?1:t<3?2:3;$('ct').textContent=n;
 $('ct').style.transform+=` scale(${1+.1*Math.max(0,1-((t-1)%1)/.2)*(t>1&&t<3.2?1:0)})`;$('ct').style.color=n===3?'#d8b566':'';
 nasce('b0',t,3.6);nasce('b1',t,4.9);nasce('b2',t,6.3);
 const d=1-.5*ioo((t-8.0)/.6);['b0','b1','b2','ct'].forEach(i=>$(i).style.filter=`brightness(${d})`);
 marca('q',t,8.4);sobe('s',t,10.2);
 $('cena').style.transform=`translateX(${treme(t,[3.6,4.9,6.3])}px)`;
}""",
    "sons": [(1.0, "tique"), (2.0, "tique"), (3.0, "carimbo", .7), (3.6, "pop"), (3.6, "vibra"), (4.9, "pop"), (4.9, "vibra"),
             (6.3, "pop"), (6.3, "vibra"), (6.4, "erro", .7), (8.35, "whoosh"), (8.5, "escreve"), (9.0, "brilho", .7),
             (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "",
                "legenda": "\"Já é a 3ª vez hoje.\"\n\"Agora só no intervalo.\"\n\"E seu nome vai pro quadro da equipe.\"\n\nPode proibir?\n\nIr ao banheiro é necessidade básica. A empresa pode organizar a rotina, mas proibir, controlar de forma exagerada ou expor quem vai ao banheiro fere a dignidade de quem trabalha (Constituição, art. 1º, III, e art. 5º, X). A Justiça do Trabalho tem condenado empresas a pagar indenização por dano moral nesses casos.\n\nO que vale saber:\n📌 Limite de idas, pedido de autorização humilhante ou lista com nomes podem ser abuso\n📌 Gestantes e pessoas com problema de saúde podem precisar de mais pausas\n📌 Guarde mensagens, fotos do quadro e nomes de quem viu\n📌 Leve a situação ao RH ou ao sindicato por escrito\n\nComente se já viu isso no trabalho. E mande para quem passa por isso.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #danomoral #assediomoral #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
