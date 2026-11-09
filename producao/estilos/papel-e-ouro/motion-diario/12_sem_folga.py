"""Dia 12 · Sem folga. Duas semanas de calendário marcadas como trabalhadas, nenhum descanso."""
from motor import rodar

LETRAS = "DSTQQSS"
EP = {
    "nome": "12-sem-folga",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:290px}#cnt{top:330px}
#cal{position:absolute;left:150px;width:780px;top:580px;display:grid;grid-template-columns:repeat(7,1fr);gap:12px}
#cal span{font:600 24px Inter;text-align:center;opacity:.7}
#cal div{height:84px;border-radius:12px;border:2px solid rgb(239 230 217/.3);font:500 26px/80px Inter;text-align:center}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>dias trabalhados sem folga</div><div class="big ouro" id=cnt data-m=1>0</div><div id=cal data-m=1>"""
    + "".join(f"<span>{c}</span>" for c in LETRAS) + "".join(f"<div id=k{i}></div>" for i in range(14))
    + """</div><div class=marca id=q><span>Quando é a folga?</span></div><div class=sub id=s>Comente quantos dias seguidos você já trabalhou.</div>""",
    "js": """const FOIL=getComputedStyle(document.querySelector('.fx')).backgroundImage;
function cena(t){
 sobe('r1',t,.2);sobe('cnt',t,.3);sobe('cal',t,.4,.5);
 const n=Math.max(0,Math.min(14,Math.floor((t-1.0)/.42)+1));$('cnt').textContent=n;
 for(let i=0;i<14;i++){const k=$('k'+i),on=i<n,dom=i%7===0;k.style.background=on?(dom?FOIL:'#EFE6D9'):'transparent';k.style.color='#1E1814';
  k.textContent=on?'✓':'';k.style.transform=`scale(${i===n-1&&t<7?1.1:1})`}
 marca('q',t,8.6);sobe('s',t,10.4);
 $('cena').style.transform=`translateX(${treme(t,[1.0,3.94,6.88],3)}px)`;
}""",
    "sons": [(1.0 + i * .42, "carimbo" if i % 7 == 0 else "tique", .55 if i % 7 == 0 else .8) for i in range(14)]
            + [(7.2, "erro", .7), (8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "14 dias seguidos de trabalho.\nDois domingos.\nNenhuma folga.\n\nQuando é a folga?\n\nTodo trabalhador tem direito a um descanso semanal remunerado de 24 horas seguidas, de preferência no domingo (Lei 605/1949 e CLT, art. 67).\n\nO que vale saber:\n📌 Quem trabalha aos domingos deve folgar num domingo de tempos em tempos, conforme a regra da sua atividade\n📌 Folga não dada no domingo ou no feriado, sem outro dia de descanso, deve ser paga em dobro (Súmula 146 do TST)\n📌 Anote os dias trabalhados e guarde as escalas\n📌 Convenções coletivas podem trazer regras próprias\n\nComente quantos dias seguidos você já trabalhou. E mande para quem não sabe o que é folga.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #folga #descansosemanal #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
