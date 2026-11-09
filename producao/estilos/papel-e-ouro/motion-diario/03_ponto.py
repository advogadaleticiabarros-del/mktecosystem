"""Dia 3 · Ponto britânico. A folha sai igual todo dia; os horários reais aparecem escritos em ouro."""
from motor import rodar

DIAS = [("Seg", "18:40"), ("Ter", "19:15"), ("Qua", "18:55"), ("Qui", "20:10"), ("Sex", "19:30")]
EP = {
    "nome": "03-ponto",
    "dur": 20.0,
    "salve": "Salve e mande para quem assina o ponto pronto.",
    "css": """#r1{top:290px}#fl{position:absolute;left:150px;width:780px;top:350px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:22px 30px;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#fl h3{font:600 22px Inter;letter-spacing:.08em;opacity:.7;display:grid;grid-template-columns:90px 1fr 1fr 150px;margin-bottom:6px}
#fl h3 span:last-child{text-align:right}
.d{display:grid;grid-template-columns:90px 1fr 1fr 150px;align-items:center;font:400 34px/2.3 Inter;border-top:1.5px dashed rgb(30 24 20/.2)}
.d b{font-weight:600}.d .v{font:italic 500 46px 'EB Garamond',serif;color:#9a6e1c;text-align:right}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>folha de ponto · semana</div><div id=fl data-m=1><h3><span>DIA</span><span>ENTRADA</span><span>SAÍDA</span><span>REAL</span></h3>"""
    + "".join(f'<div class=d id=d{i}><b>{a}</b><span class=e>08:00</span><span class=e>17:00</span><span class=v id=v{i}>{v}</span></div>' for i, (a, v) in enumerate(DIAS))
    + """</div><div class=marca id=q><span>Ponto igual vale?</span></div><div class=sub id=s>Comente: o seu é assim?</div>""",
    "js": """function cena(t){
 sobe('r1',t,.2);sobe('fl',t,.4,.5);
 for(let i=0;i<5;i++){const e=$('d'+i).querySelectorAll('.e');e.forEach((x,j)=>{const a=t-(1.0+i*.55+j*.22);x.style.opacity=a<0?0:1;x.style.transform=`scale(${1+.25*Math.max(0,1-a/.15)})`});
  const v=$('v'+i),a=(t-(5.0+i*.75))/.5;v.style.opacity=a<0?0:1;v.style.clipPath=`inset(0 ${(1-ioo(a))*100}% 0 0)`;
  e[1].style.textDecoration=a>.6?'line-through':'';}
 marca('q',t,9.6);sobe('s',t,11.4);
 $('cena').style.transform=`translateX(${treme(t,[1,1.55,2.1,2.65,3.2],2)}px)`;
}""",
    "sons": [(.4, "pagina")] + [(1.0 + i * .55 + j * .22, "carimbo", .5) for i in range(5) for j in range(2)]
            + [(5.0 + i * .75, "escreve", .7) for i in range(5)]
            + [(8.9, "erro", .7), (9.55, "whoosh"), (9.7, "escreve"), (10.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "Segunda: 08h às 17h.\nTerça: 08h às 17h.\nQuarta, quinta, sexta: 08h às 17h.\nSaída de verdade: 18h40, 19h15, 20h10...\n\nPonto igual todo dia vale como prova?\n\nO TST (Súmula 338, III) diz que cartão de ponto com horários sempre iguais, o chamado ponto britânico, não serve como prova. Aí cabe à empresa provar a jornada.\n\nO que vale saber:\n📌 Ninguém entra e sai no mesmo minuto todo dia\n📌 Assinar folha pronta não apaga as horas feitas\n📌 Anote seus horários reais num caderno ou no celular\n📌 Mensagens, e-mails e testemunhas também contam\n\nComente: o seu ponto é assim? E mande para quem assina o ponto pronto.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #horaextra #pontobritanico #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
