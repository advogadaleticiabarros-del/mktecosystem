"""Dia 4 · "Pede demissão que é melhor pra você." Lista do que se perde, riscada item a item."""
from motor import rodar

ITENS = ["Multa de 40% do FGTS", "Saque do FGTS", "Seguro-desemprego", "Aviso prévio pago"]
EP = {
    "nome": "04-demissao",
    "dur": 20.0,
    "salve": "Salve antes de assinar qualquer pedido de demissão.",
    "css": """#topo{top:282px}#b0{top:350px}#r2{top:540px}
.it{position:absolute;left:150px;right:150px;text-align:center;font:500 50px 'EB Garamond',serif}
.it i{position:absolute;left:50%;top:54%;height:4px;background:#bb923f;transform:translateX(-50%)}
#q{top:1070px}#s{top:1196px}""",
    "html": """<div class=rot id=topo>Chefe</div><div class="bo ele" id=b0>Pede demissão. É melhor pra você.<small>17:58</small></div>
<div class=rot id=r2>Se você pedir, perde:</div>"""
    + "".join(f'<div class=it id=i{i} style="top:{610 + i * 100}px">{x}<i id=x{i}></i></div>' for i, x in enumerate(ITENS))
    + """<div class=marca id=q><span>Melhor pra quem?</span></div><div class=sub id=s>Comente o que você faria.</div>""",
    "js": """function cena(t){
 sobe('topo',t,.1);nasce('b0',t,.6);sobe('r2',t,3.4);
 for(let i=0;i<4;i++){sobe('i'+i,t,4.0+i*.5,.35);const s=6.4+i*.6,k=ioo((t-s)/.35);$('x'+i).style.width=(k*520)+'px';$('x'+i).style.opacity=t>s?1:0;
  $('i'+i).style.color=k>.5?'rgb(239 230 217/.45)':''}
 marca('q',t,10.4);sobe('s',t,12.2);
 $('cena').style.transform=`translateX(${treme(t,[.6,6.4,7,7.6,8.2],3)}px)`;
}""",
    "sons": [(.6, "pop"), (.6, "vibra"), (3.4, "whoosh", .5)] + [(4.0 + i * .5, "tique") for i in range(4)]
            + [(6.4 + i * .6, "escreve", .6) for i in range(4)] + [(6.4 + i * .6, "moedas", .35) for i in range(4)]
            + [(8.7, "erro", .7), (10.35, "whoosh"), (10.5, "escreve"), (11.0, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "\"Pede demissão. É melhor pra você.\"\n\nMelhor pra quem?\n\nQuando é você quem pede demissão, perde:\n📌 A multa de 40% do FGTS\n📌 O saque do FGTS\n📌 O seguro-desemprego\n📌 O aviso prévio pago pela empresa\n\nSe a empresa quer o desligamento, quem deve dispensar é ela. Existe também o acordo previsto na CLT (art. 484-A), com regras próprias. E pedido de demissão feito sob pressão pode ser questionado.\n\nAntes de assinar, guarde as mensagens e tire suas dúvidas.\n\nComente o que você faria. E mande para quem está ouvindo essa frase no trabalho.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #pedidodedemissao #fgts #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
