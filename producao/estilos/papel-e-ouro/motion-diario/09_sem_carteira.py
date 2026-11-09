"""Dia 9 · Sem carteira na experiência. Contador de dias trabalhados; a carteira digital segue sem contrato."""
from motor import rodar

EP = {
    "nome": "09-sem-carteira",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:290px}#dn{top:340px}#c0{top:590px}
#ct{position:absolute;left:150px;width:780px;top:790px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:20px 30px;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#ct h3{font:600 22px Inter;letter-spacing:.1em;opacity:.7}#ct p{font:400 34px/1.4 Inter;margin-top:6px}#ct b{color:#9a2a1c}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>trabalhando desde</div><div class=big id=dn data-m=1>dia 1</div>
<div class=card id=c0><div class=t><span>RH</span><b>agora</b></div><div class=m>A carteira a gente assina depois da experiência.</div></div>
<div id=ct data-m=1><h3>CARTEIRA DE TRABALHO DIGITAL</h3><p>Contratos de trabalho: <b>nenhum</b></p></div>
<div class=marca id=q><span>Pode?</span></div><div class=sub id=s>Não. O registro vale desde o 1º dia,<br>inclusive na experiência.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.2);sobe('dn',t,.3);$('dn').textContent='dia '+Math.max(1,Math.round(45*ioo((t-.6)/3.2)));
 $('dn').style.color=t>3.8?'#d8b566':'';nasce('c0',t,4.4);sobe('ct',t,6.6,.5);
 marca('q',t,9.0);sobe('s',t,10.8);
 $('cena').style.transform=`translateX(${treme(t,[4.4,7.1])}px)`;
}""",
    "sons": [(.6 + i * .11, "pagina", .25) for i in range(28)]
            + [(3.8, "carimbo"), (4.4, "pop"), (4.4, "vibra"), (6.6, "pagina"), (7.1, "erro", .7),
               (8.95, "whoosh"), (9.1, "escreve"), (9.6, "brilho", .7), (10.8, "boom", .5), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "Dia 45 de trabalho.\nRH: \"A carteira a gente assina depois da experiência.\"\n\nPode? Não.\n\nO contrato de experiência também é um contrato de trabalho e precisa ser registrado. Pela CLT (art. 29), a empresa tem 5 dias úteis para fazer a anotação, contados do início do trabalho.\n\nO que vale saber:\n📌 Sem registro, não há depósito de FGTS nem contribuição ao INSS\n📌 Confira a sua Carteira de Trabalho Digital no aplicativo\n📌 Mensagens, escalas, crachá e testemunhas ajudam a provar o vínculo\n📌 O tempo sem registro pode ser reconhecido depois\n\nComente se já passou por isso. E mande para quem está começando num emprego novo.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #carteiraassinada #clt #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
