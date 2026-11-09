"""Dia 1 · Atestado recusado. Conversa de WhatsApp com o gerente, que diz que atestado do posto não vale."""
from motor import rodar

EP = {
    "nome": "01-atestado",
    "dur": 20.0,
    "salve": "Salve e mande para quem já teve atestado recusado.",
    "css": """#topo{top:282px}
#topo i{display:inline-block;width:14px;height:14px;border-radius:50%;background:#7BB37A;margin-right:10px;vertical-align:2px}
.doc{width:300px;background:#EFE6D9;color:#1E1814;border-radius:14px;padding:18px 20px;margin-bottom:10px}
.doc b{display:block;font:600 22px Inter;letter-spacing:.08em}
.doc p{font:400 22px/1.4 Inter;margin-top:8px}
.doc hr{border:0;height:6px;border-radius:3px;background:#1E1814;opacity:.15;margin-top:10px}
#b0{top:350px}#b1{top:640px}#b2,#p1{top:800px}#b3,#p2{top:940px}
#q{top:1070px}#s{top:1196px}""",
    "html": """<div class=rot id=topo><i></i>Gerente</div>
<div class="bo eu" id=b0 data-m=1><div class=doc><b>ATESTADO MÉDICO</b><p>Afastamento: 2 dias</p><hr><hr style="width:70%"></div>Tô com febre. Atestado do posto.<small>07:12</small></div>
<div class="bo eu" id=b1>Levo o original amanhã.<small>07:12</small></div>
<div class="bo ele pts" id=p1 data-m=1><span></span><span></span><span></span></div>
<div class="bo ele" id=b2>Atestado de posto aqui não vale.<small>07:31</small></div>
<div class="bo ele pts" id=p2 data-m=1><span></span><span></span><span></span></div>
<div class="bo ele" id=b3>Vou descontar os 2 dias.<small>07:32</small></div>
<div class=marca id=q><span>Pode descontar?</span></div>
<div class=sub id=s>Comente: sim ou não?</div>""",
    "js": """const pts=(id,a,b,t)=>{const e=$(id);e.style.opacity=t<a||t>b?0:cl((t-a)/.15);
 e.querySelectorAll('span').forEach((s,i)=>{s.style.opacity=.25+.5*Math.max(0,Math.sin((t-a)*7-i*.9))})};
function cena(t){
 sobe('topo',t,.1);nasce('b0',t,.5);nasce('b1',t,2.0);
 pts('p1',3.6,5.4,t);nasce('b2',t,5.4);pts('p2',6.9,8.2,t);nasce('b3',t,8.2);
 const dim=1-.6*ioo((t-10.2)/.6);['b0','b1','b2','b3'].forEach(i=>$(i).style.filter=`brightness(${dim})`);
 $('b3').style.filter=`brightness(${1-.25*ioo((t-10.2)/.6)})`;
 marca('q',t,10.6);sobe('s',t,12.4);
 $('cena').style.transform=`translateX(${treme(t,[5.4,8.2])}px)`;
}""",
    "sons": [(.5, "bolha"), (.55, "vibra", .5), (2.0, "bolha"), (3.6, "digita"), (5.4, "pop"), (5.4, "vibra"),
             (6.9, "digita", .8), (8.2, "pop"), (8.2, "vibra"), (8.25, "erro", .8), (10.55, "whoosh"),
             (10.7, "escreve"), (11.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {
        "primeiro_comentario": "",
        "legenda": "07h12. Atestado do posto, 2 dias de afastamento.\n07h31. \"Atestado de posto aqui não vale.\"\n07h32. \"Vou descontar os 2 dias.\"\n\nPode descontar?\n\nA lei não diz que atestado do SUS vale menos. A Lei 605/1949 diz que a falta por doença, comprovada por atestado médico, não pode ser descontada.\n\nO que vale saber:\n📌 Existe uma ordem de preferência: se a empresa tem médico próprio ou convênio, ele pode ser o primeiro a avaliar\n📌 Sem isso, o atestado de outro médico, inclusive do SUS, comprova a doença\n📌 Recusar sem motivo e descontar pode ser irregular\n📌 Guarde uma cópia ou foto do atestado e a conversa\n\nComente: pode descontar ou não? E mande para quem já teve atestado recusado.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #atestadomedico #direitosdotrabalhador #clt #advogadatrabalhista",
    },
}

if __name__ == "__main__":
    rodar(EP, __file__)
