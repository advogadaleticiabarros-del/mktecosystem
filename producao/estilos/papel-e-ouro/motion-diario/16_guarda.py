"""Flagrante 16 · Guarda compartilhada, responsabilidade dividida. Tarefas da semana, todas caem para a mãe."""
from motor import rodar

TAREFAS = ["Levar à escola", "Consulta no pediatra", "Reunião de pais", "Comprar uniforme", "Remédio de madrugada", "Lição de casa"]
EP = {
    "nome": "16-guarda",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#pl{top:330px;font-size:120px}
.tf{position:absolute;left:150px;width:780px;display:flex;justify-content:space-between;align-items:center;font:400 34px Inter;padding:10px 0;border-top:1.5px solid rgb(239 230 217/.15)}
.tf b{font:600 26px Inter;padding:6px 18px;border-radius:99px;color:#1E1814}
#q{top:1010px}#s{top:1136px}""",
    "html": """<div class=rot id=r1>guarda compartilhada · esta semana</div><div class=big id=pl data-m=1>Mãe 0 × Pai 0</div>"""
    + "".join(f'<div class=tf id=t{i} style="top:{500 + i * 78}px"><span>{x}</span><b id=g{i}>Mãe</b></div>' for i, x in enumerate(TAREFAS))
    + """<div class=marca id=q><span>Compartilhada?</span></div><div class=sub id=s>Comente se é assim na sua casa.</div>""",
    "js": """const MARCA=getComputedStyle(document.querySelector('.fx')).backgroundImage;
function cena(t){
 sobe('r1',t,.1);sobe('pl',t,.2);let n=0;
 for(let i=0;i<6;i++){sobe('t'+i,t,.8+i*.35,.3);const s=3.2+i*.7,g=$('g'+i);g.style.background=MARCA;g.style.opacity=t<s?0:1;g.style.transform=`scale(${t<s?.6:1+.25*Math.max(0,1-(t-s)/.2)})`;if(t>=s)n++}
 $('pl').textContent='Mãe '+n+' × Pai 0';$('pl').style.color=n===6?'#d8b566':'';
 marca('q',t,8.6);sobe('s',t,10.4);
 $('cena').style.transform=`translateX(${treme(t,[7.4])}px)`;
}""",
    "sons": [(.8 + i * .35, "tique", .6) for i in range(6)] + [(3.2 + i * .7, "carimbo", .5) for i in range(6)]
            + [(7.4, "erro", .6), (8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/guarda-compartilhada-como-funciona.html",
                "legenda": "Escola: mãe. Pediatra: mãe. Reunião de pais: mãe.\nUniforme, remédio de madrugada, lição de casa: mãe.\nGuarda: compartilhada.\n\nCompartilhada com quem?\n\nGuarda compartilhada quer dizer responsabilidade dos dois: decisões, cuidados e deveres com o filho são divididos entre pai e mãe (Código Civil, art. 1.583, §1º). O tempo de convivência também deve ser equilibrado, pensando no que é melhor para a criança.\n\nO que vale saber:\n📌 Guarda compartilhada não acaba com a pensão alimentícia\n📌 Os dois têm direito de saber da escola, da saúde e da rotina do filho\n📌 Se um dos dois não cumpre a parte dele, dá para pedir ajuste na Justiça\n📌 Anote quem fez o quê e guarde as mensagens\n\nO link do artigo completo está no primeiro comentário.\n\nComente se é assim na sua casa. E mande para uma mãe que faz tudo sozinha.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra informação sobre os seus direitos e os do seu filho.\n\n#guardacompartilhada #direitodefamilia #pensaoalimenticia #maesolo #advogada"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
