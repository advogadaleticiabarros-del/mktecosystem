"""Flagrante 22 · Fim da escala 6x1. A semana de 6 dias vira 5 com 2 folgas em 16/12/2026 (EC 141, ver CONTEXTO_PROJETO)."""
from motor import rodar

LETRAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
EP = {
    "nome": "22-fim-6x1",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#dt{top:330px;font-size:150px}#hr{top:520px;font:500 40px Inter}
#sem{position:absolute;left:150px;width:780px;top:600px;display:grid;grid-template-columns:repeat(7,1fr);gap:10px}
#sem div{height:150px;border-radius:14px;text-align:center;padding-top:22px;color:#1E1814}
#sem b{display:block;font:600 24px Inter}#sem i{display:block;font:italic 500 30px/2 'EB Garamond',serif}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>sua escala</div><div class=big id=dt data-m=1>hoje</div><div class=rot id=hr>6x1 · até 44 horas por semana</div><div id=sem data-m=1>"""
    + "".join(f"<div id=k{i}><b>{d}</b><i id=w{i}></i></div>" for i, d in enumerate(LETRAS))
    + """</div><div class=marca id=q><span>Sua escala muda?</span></div><div class=sub id=s>Comente qual é a sua escala hoje.</div>""",
    "js": """const FOIL=getComputedStyle(document.querySelector('.fx')).backgroundImage;
function cena(t){
 sobe('r1',t,.1);sobe('dt',t,.2);sobe('hr',t,.4);sobe('sem',t,.5,.5);
 const novo=t>=5.2;$('dt').textContent=novo?'16/12/2026':'hoje';$('dt').style.color=novo?'#d8b566':'';
 $('hr').textContent=novo?'2 folgas · até 42 horas por semana':'6x1 · até 44 horas por semana';
 for(let i=0;i<7;i++){const folga=novo?i>=5:i===6,s=novo?5.4+i*.12:1.0+i*.3,on=t>=s;const k=$('k'+i);
  k.style.background=!on?'rgb(239 230 217/.15)':folga?FOIL:'#EFE6D9';$('w'+i).textContent=on?(folga?'folga':'trabalho'):'';
  k.style.transform=`scale(${on?1+.1*Math.max(0,1-(t-s)/.2):1})`}
 marca('q',t,8.6);sobe('s',t,10.4);
 $('cena').style.transform=`translateX(${treme(t,[5.2])}px)`;
}""",
    "sons": [(1.0 + i * .3, "carimbo" if i == 6 else "tique", .5 if i == 6 else .7) for i in range(7)]
            + [(4.6, "relogio", .5), (5.2, "boom", .5), (5.3, "pagina"), (6.3, "brilho", .6), (6.4, "sino", .6),
               (8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/fim-da-escala-6x1-o-que-muda-e-quando-comeca.html",
                "legenda": "Hoje: 6 dias de trabalho, 1 de folga.\n16/12/2026: 2 folgas por semana.\n\nSua escala vai mudar?\n\nA Emenda Constitucional 141, publicada em 16/10/2026, reduz a jornada aos poucos: a partir de 16/12/2026, até 42 horas por semana com 2 folgas. A partir de 16/12/2027, até 40 horas.\n\nO que vale saber:\n📌 O salário não pode ser reduzido por causa da nova jornada\n📌 Hora trabalhada além do novo limite é hora extra, com 50% a mais\n📌 Escalas especiais, como 12x36, têm regras próprias e podem depender de acordo coletivo\n📌 Anote sua escala em dezembro e compare com o holerite\n\nO link do artigo completo está no primeiro comentário.\n\nComente qual é a sua escala hoje. E mande para quem trabalha na 6x1.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #fimda6x1 #escala6x1 #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
