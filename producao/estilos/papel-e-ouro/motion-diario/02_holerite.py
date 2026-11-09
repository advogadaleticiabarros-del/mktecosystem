"""Dia 2 · Holerite sem hora extra. Contador de horas a mais sobe, o recibo sai com hora extra zerada."""
from motor import rodar

LIN = [("Salário base", "R$ 2.400,00"), ("Horas extras", "R$ 0,00"), ("Descontos", "- R$ 212,00"), ("Líquido", "R$ 2.188,00")]
EP = {
    "nome": "02-holerite",
    "dur": 20.0,
    "salve": "Salve e confira o seu próximo holerite.",
    "css": """#r1{top:290px}#hn{top:330px}#papel{position:absolute;left:150px;width:780px;top:600px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:26px 36px 18px;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#papel h3{font:600 24px Inter;letter-spacing:.1em;opacity:.7;margin-bottom:8px}
.ln{display:flex;justify-content:space-between;font:400 34px/1.9 Inter;border-top:1.5px dashed rgb(30 24 20/.2);position:relative}
.ln b{font-weight:600}
#hl{position:absolute;left:-14px;right:-14px;top:6px;bottom:6px;border:4px solid #bb923f;border-radius:16px}
#q{top:1070px}#s{top:1196px}""",
    "html": """<div class=rot id=r1>horas a mais em outubro</div><div class="big ouro" id=hn data-m=1>00h</div>
<div id=papel data-m=1><h3>RECIBO DE PAGAMENTO · OUTUBRO</h3>"""
    + "".join(f'<div class=ln id=l{i}><span>{a}</span><b>{b}</b>{"<i id=hl></i>" if i == 1 else ""}</div>' for i, (a, b) in enumerate(LIN))
    + """</div><div class=marca id=q><span>Cadê as 46 horas?</span></div><div class=sub id=s>Comente se já aconteceu com você.</div>""",
    "js": """function cena(t){
 sobe('r1',t,.2);sobe('hn',t,.3);const h=Math.round(46*ioo((t-.6)/3.4));$('hn').textContent=pad(h)+'h';
 $('hn').style.transform+=` scale(${1+.04*Math.max(0,1-Math.abs(t-4.05)/.25)})`;
 sobe('papel',t,4.6,.5);[0,1,2,3].forEach(i=>sobe('l'+i,t,5.3+i*.7,.3));
 const k=ioo((t-8.5)/.5);$('hl').style.opacity=k;$('hl').style.clipPath=`inset(0 ${(1-k)*100}% 0 0)`;
 $('l1').style.color=t>8.5?'#8a5a12':'';
 marca('q',t,10.4);sobe('s',t,12.2);
 $('cena').style.transform=`translateX(${treme(t,[8.6])}px)`;
}""",
    "sons": [(.6, "relogio", .9), (4.05, "carimbo"), (4.6, "pagina"), (5.3, "tique"), (6.0, "tique"), (6.7, "tique"),
             (7.4, "tique"), (8.5, "escreve"), (8.6, "erro", .8), (10.35, "whoosh"), (10.5, "escreve"),
             (11.0, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "46 horas a mais no mês.\nNo holerite: horas extras R$ 0,00.\n\nCadê as 46 horas?\n\nPela Constituição (art. 7º, XVI), a hora extra vale no mínimo 50% a mais que a hora normal.\n\nO que vale saber:\n📌 Hora extra precisa aparecer no holerite ou ser compensada\n📌 Compensação só vale com banco de horas feito do jeito que a lei pede\n📌 Anote seus horários reais e guarde mensagens e e-mails fora do expediente\n📌 Confira todo mês: o holerite é a sua prova\n\nComente se já aconteceu com você. E mande para quem faz hora extra todo dia.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #horaextra #holerite #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
