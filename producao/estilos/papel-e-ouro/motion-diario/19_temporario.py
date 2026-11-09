"""Flagrante 19 · Trabalho temporário de fim de ano. O contrato chega e os direitos vão sendo marcados."""
from motor import rodar

ITENS = ["Salário igual ao do efetivo", "Hora extra com 50% a mais", "FGTS todo mês", "13º proporcional", "Férias proporcionais + 1/3", "Adicional noturno"]
EP = {
    "nome": "19-temporario",
    "dur": 20.0,
    "salve": "",
    "css": """#c0{top:300px}#r1{top:470px}
.it{position:absolute;left:150px;width:780px;display:flex;gap:18px;align-items:center;font:400 34px Inter;padding:8px 0}
.it i{width:44px;height:44px;border-radius:50%;border:3px solid #bb923f;display:grid;place-items:center;font:700 26px Inter;font-style:normal;color:#1E1814;flex:none}
#q{top:1010px}#s{top:1136px}""",
    "html": """<div class=card id=c0><div class=t><span>Loja do shopping</span><b>agora</b></div><div class=m>Vaga temporária de Natal. Começa segunda!</div></div>
<div class=rot id=r1>temporário também tem direito a:</div>"""
    + "".join(f'<div class=it id=i{n} style="top:{520 + n * 76}px"><i id=v{n}></i><span>{x}</span></div>' for n, x in enumerate(ITENS))
    + """<div class=marca id=q><span>Você recebe tudo isso?</span></div><div class=sub id=s>Comente se já trabalhou como temporário.</div>""",
    "js": """const FOIL=getComputedStyle(document.querySelector('.fx')).backgroundImage;
function cena(t){
 nasce('c0',t,.5);sobe('r1',t,2.0);
 for(let n=0;n<6;n++){sobe('i'+n,t,2.5+n*.3,.3);const s=4.6+n*.55,v=$('v'+n);v.style.background=t>=s?FOIL:'transparent';v.textContent=t>=s?'✓':'';v.style.transform=`scale(${t>=s?1+.3*Math.max(0,1-(t-s)/.2):1})`}
 marca('q',t,8.6);sobe('s',t,10.4);
 $('cena').style.transform=`translateX(${treme(t,[.5])}px)`;
}""",
    "sons": [(.5, "pop"), (.5, "vibra"), (2.0, "whoosh", .4)] + [(4.6 + n * .55, "bolha", .6) for n in range(6)]
            + [(8.0, "moedas", .6), (8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/fgts-trabalhador-temporario-direitos-e-como-cobrar.html",
                "legenda": "Vaga temporária de Natal.\nÉ só por um tempo, mas os direitos são de verdade.\n\nVocê recebe tudo isso?\n\nO trabalho temporário tem lei própria (Lei 6.019/1974). O contrato pode durar até 180 dias, com prorrogação de mais 90, e o temporário tem direitos garantidos (art. 12).\n\nO que vale saber:\n📌 Salário igual ao de quem é efetivo na mesma função da empresa\n📌 Jornada de até 8 horas, com hora extra paga com no mínimo 50% a mais\n📌 FGTS, 13º e férias proporcionais com 1/3\n📌 Descanso semanal e adicional noturno quando trabalhar à noite\n📌 Registro na Carteira de Trabalho como temporário\n\nO link do artigo completo está no primeiro comentário.\n\nComente se já trabalhou como temporário. E mande para quem vai pegar vaga de fim de ano.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #trabalhotemporario #empregodefimdeano #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
