"""Flagrante 17 · Férias de fim de ano com pais separados. O pai avisa que vai levar o filho no Natal e no Ano-Novo."""
from motor import rodar

DIAS = ["22", "23", "24", "25", "26", "29", "30", "31", "01", "02"]
EP = {
    "nome": "17-ferias-natal",
    "dur": 20.0,
    "salve": "",
    "css": """#b0{top:300px}#r1{top:520px}
#cal{position:absolute;left:150px;width:780px;top:570px;display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
#cal div{height:110px;border-radius:14px;background:#EFE6D9;color:#1E1814;text-align:center;padding-top:12px}
#cal b{display:block;font:500 46px/1 'EB Garamond',serif}#cal i{display:block;font:600 22px/1.8 Inter;font-style:normal}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class="bo ele" id=b0>Vou levar o Pedro pra viajar no Natal e no Ano-Novo.<small>19:40</small></div>
<div class=rot id=r1>dezembro e janeiro</div><div id=cal data-m=1>"""
    + "".join(f"<div id=k{i}><b>{d}</b><i id=w{i}></i></div>" for i, d in enumerate(DIAS))
    + """</div><div class=marca id=q><span>Pode levar assim?</span></div><div class=sub id=s>Depende do que foi decidido. Leia a legenda.</div>""",
    "js": """const FOIL=getComputedStyle(document.querySelector('.fx')).backgroundImage,FE=[2,3,7,8];
function cena(t){
 nasce('b0',t,.5);sobe('r1',t,2.2);sobe('cal',t,2.3,.5);
 for(let i=0;i<10;i++){const k=$('k'+i),w=$('w'+i),fe=FE.includes(i),s=3.6+FE.indexOf(i)*.6;
  k.style.background=fe&&t>=s?FOIL:'#EFE6D9';w.textContent=fe&&t>=s?'Pai':'';k.style.transform=`scale(${fe&&t>=s?1+.12*Math.max(0,1-(t-s)/.25):1})`;
  k.style.opacity=!fe&&t>6.4?.5:1}
 marca('q',t,8.4);sobe('s',t,10.2);
 $('cena').style.transform=`translateX(${treme(t,[.5,3.6,4.2,4.8,5.4],3)}px)`;
}""",
    "sons": [(.5, "pop"), (.5, "vibra"), (2.3, "pagina")] + [(3.6 + i * .6, "carimbo", .55) for i in range(4)]
            + [(6.4, "sino", .6), (8.35, "whoosh"), (8.5, "escreve"), (9.0, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/viagem-com-filhos-nas-ferias-autorizacao.html",
                "legenda": "\"Vou levar o Pedro pra viajar no Natal e no Ano-Novo.\"\n24, 25, 31 e 1º: todos com o pai.\n\nPode levar sem combinar?\n\nDepende do que foi decidido. As festas de fim de ano costumam estar no acordo ou na decisão de convivência, muitas vezes alternando a cada ano. O que está ali vale para os dois.\n\nO que vale saber:\n📌 Se não há regra para as festas, o ideal é combinar por escrito, pensando na criança\n📌 Viagem dentro do Brasil com o pai ou com a mãe não precisa de autorização judicial (ECA, art. 83)\n📌 Viagem para fora do país com só um dos pais precisa da autorização do outro, com firma reconhecida, ou da Justiça (ECA, art. 84)\n📌 Descumprir a convivência combinada pode ser levado ao juiz\n\nO link do artigo completo está no primeiro comentário.\n\nComente como é na sua família. E mande para uma mãe que está organizando as festas.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra informação sobre os seus direitos e os do seu filho.\n\n#guardacompartilhada #direitodefamilia #feriasescolares #natal #advogada"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
