"""Dia 5 · Vender as férias todas. Calendário de 30 dias fica dourado; depois só 10 continuam (1/3)."""
from motor import rodar

EP = {
    "nome": "05-ferias",
    "dur": 20.0,
    "salve": "Salve e mande para quem nunca tira férias.",
    "css": """#c0{top:300px}#r1{top:500px}
#cal{position:absolute;left:210px;width:660px;top:555px;display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
#cal div{height:62px;border-radius:12px;background:#EFE6D9;color:#1E1814;font:500 28px/62px Inter;text-align:center}
#q{top:960px}#s{top:1090px}""",
    "html": """<div class=card id=c0><div class=t><span>Chefe</span><b>agora</b></div><div class=m>Vende os 30 dias de férias esse ano?</div></div>
<div class=rot id=r1>dias vendidos: <span id=n>0</span></div><div id=cal data-m=1>"""
    + "".join(f"<div id=k{i}>{i + 1}</div>" for i in range(30))
    + """</div><div class=marca id=q><span>Pode vender tudo?</span></div><div class=sub id=s>Não. O máximo é 1/3: 10 dias.<br>E quem decide é você.</div>""",
    "js": """const FOIL=getComputedStyle(document.querySelector('.fx')).backgroundImage;
function cena(t){
 nasce('c0',t,.5);sobe('r1',t,2.2);sobe('cal',t,2.3,.5);
 const v=Math.floor(30*cl((t-3.0)/3.5)+.001),volta=t>11.6?Math.floor(20*cl((t-11.6)/1.4)):0;
 $('n').textContent=Math.min(v,30)-volta;
 for(let i=0;i<30;i++){const k=$('k'+i),ouro=i<v&&i<30-volta;k.style.background=ouro?FOIL:'#EFE6D9';
  k.style.transform=`scale(${i===v-1&&t<6.6?1.08:1})`;k.style.opacity=i>=10&&t>11.6&&!ouro?.55:1}
 marca('q',t,8.2);sobe('s',t,11.0);
 $('cena').style.transform=`translateX(${treme(t,[.5,6.6])}px)`;
}""",
    "sons": [(.5, "pop"), (.5, "vibra")] + [(3.0 + i * 3.5 / 30, "tique", .6) for i in range(30)]
            + [(6.6, "moedas"), (7.4, "erro", .6), (8.15, "whoosh"), (8.3, "escreve"), (8.8, "brilho", .7),
               (11.0, "boom", .5), (11.6, "pagina"), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "\"Vende os 30 dias de férias esse ano?\"\n\nPode vender tudo? Não.\n\nPela CLT (art. 143), dá para converter no máximo 1/3 das férias em dinheiro, ou seja, 10 dias de 30. E essa escolha é do trabalhador, não da empresa.\n\nO que vale saber:\n📌 O pedido para vender os 10 dias deve ser feito até 15 dias antes do fim do período aquisitivo\n📌 Os outros 20 dias são de descanso de verdade\n📌 Férias não tiradas no prazo podem ter de ser pagas em dobro\n📌 Guarde mensagens em que pedem para você não sair de férias\n\nComente: você já vendeu férias? E mande para quem nunca tira férias.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #ferias #clt #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
