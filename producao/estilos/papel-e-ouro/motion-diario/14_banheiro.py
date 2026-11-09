"""Flagrante 14 · Recepcionista lavando banheiro de alto fluxo. Artigo mais visto do blog (Search Console, 24/10)."""
from motor import rodar

EP = {
    "nome": "14-banheiro",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#c0{top:336px}#pn{top:520px;font-size:170px}#pl{top:700px}
#cr{position:absolute;left:290px;width:500px;top:770px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:16px 26px;text-align:center;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#cr h3{font:600 20px Inter;letter-spacing:.12em;opacity:.6}#cr p{font:500 44px/1.2 'EB Garamond',serif}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>recepção · 7h58</div>
<div class=card id=c0><div class=t><span>Gerente</span><b>agora</b></div><div class=m>Antes de abrir, lava os banheiros. Hoje vai lotar.</div></div>
<div class="big ouro" id=pn data-m=1>0</div><div class=rot id=pl>pessoas por dia usam esse banheiro</div>
<div id=cr data-m=1><h3>CRACHÁ</h3><p>Recepcionista</p></div>
<div class=marca id=q><span>Isso é função dela?</span></div><div class=sub id=s>Comente o que você acha.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.1);nasce('c0',t,.5);sobe('pn',t,2.6);sobe('pl',t,2.8);$('pn').textContent=Math.round(300*ioo((t-2.8)/2.4));
 sobe('cr',t,6.0,.5);const r=t>6.6?Math.sin(Math.min(1,(t-6.6)/.5)*Math.PI)*3:0;$('cr').style.transform+=` rotate(${r}deg)`;
 marca('q',t,8.6);sobe('s',t,10.4);
 $('cena').style.transform=`translateX(${treme(t,[.5,5.2])}px)`;
}""",
    "sons": [(.5, "pop"), (.5, "vibra"), (2.8, "relogio", .7), (5.2, "carimbo"), (6.0, "pagina"), (6.6, "erro", .6),
             (8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/empresa-pode-obrigar-limpar-banheiro.html",
                "legenda": "Contratada como recepcionista.\n7h58: \"Antes de abrir, lava os banheiros. Hoje vai lotar.\"\n\nIsso é função dela?\n\nLimpar banheiro de uso público ou coletivo, com grande circulação de pessoas, dá direito ao adicional de insalubridade em grau máximo, de 40% (Súmula 448, II, do TST). E tarefa muito diferente da função contratada pode ser discutida como desvio ou acúmulo de função.\n\nO que vale saber:\n📌 Banheiro de escritório pequeno, usado por poucas pessoas, tem outra regra\n📌 Shopping, clínica, rodoviária, academia e loja com muito movimento costumam ser grande circulação\n📌 Guarde mensagens com a ordem e anote quantas vezes por dia você limpa\n📌 Equipamento de proteção não substitui o adicional quando a lei manda pagar\n\nO link do artigo completo está no primeiro comentário.\n\nComente o que você acha. E mande para quem lava banheiro sem ser contratada para isso.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #insalubridade #desviodefuncao #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
