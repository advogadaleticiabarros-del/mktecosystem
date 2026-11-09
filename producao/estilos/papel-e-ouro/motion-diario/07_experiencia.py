"""Dia 7 · Experiência sem fim. Contador de dias até 90; o RH quer estender mais 30."""
from motor import rodar

EP = {
    "nome": "07-experiencia",
    "dur": 20.0,
    "salve": "Salve e mande para quem está em experiência.",
    "css": """#r1{top:290px}#dn{top:340px}#c0{top:600px}#q{top:820px}#s{top:950px}
#ok{position:absolute;left:150px;right:150px;top:1080px;text-align:center;font:italic 500 46px/1.2 'EB Garamond',serif}""",
    "html": """<div class=rot id=r1>contrato de experiência</div><div class=big id=dn data-m=1>dia 1</div>
<div class=card id=c0><div class=t><span>RH</span><b>agora</b></div><div class=m>Vamos estender sua experiência por mais 30 dias.</div></div>
<div class=marca id=q><span>Pode?</span></div><div class=sub id=s>A experiência tem no máximo 90 dias,<br>somando a prorrogação.</div>
<div id=ok class=ouro>Passou disso, o contrato vira por prazo indeterminado.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.2);sobe('dn',t,.3);const d=Math.max(1,Math.round(90*ioo((t-.6)/3.6)));$('dn').textContent='dia '+d;
 $('dn').style.color=t>4.2?'#d8b566':'';nasce('c0',t,5.0);
 marca('q',t,7.6);sobe('s',t,9.4);sobe('ok',t,11.6,.5);
 $('cena').style.transform=`translateX(${treme(t,[5.0])}px)`;
}""",
    "sons": [(.6 + i * .12, "pagina", .25) for i in range(30)]
            + [(4.2, "carimbo"), (4.3, "sino", .7), (5.0, "pop"), (5.0, "vibra"), (5.1, "erro", .6),
               (7.55, "whoosh"), (7.7, "escreve"), (8.2, "brilho", .7), (11.6, "boom", .5), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "Dia 90 de experiência.\nRH: \"Vamos estender sua experiência por mais 30 dias.\"\n\nPode? Não.\n\nPela CLT (art. 445), o contrato de experiência tem no máximo 90 dias. Ele pode ser prorrogado uma vez só (art. 451), mas a soma não passa de 90.\n\nO que vale saber:\n📌 Passou de 90 dias, o contrato passa a ser por prazo indeterminado\n📌 Aí, se houver dispensa sem justa causa, entram aviso prévio e multa de 40% do FGTS\n📌 Confira as datas no contrato que você assinou\n📌 Guarde a mensagem da prorrogação\n\nComente: você já passou por isso? E mande para quem está em experiência.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #contratodeexperiencia #clt #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
