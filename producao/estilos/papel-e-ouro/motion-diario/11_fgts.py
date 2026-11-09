"""Dia 11 · FGTS não depositado. Extrato mês a mês; os meses em branco piscam em ouro."""
from motor import rodar

MESES = [("Janeiro", 1), ("Fevereiro", 1), ("Março", 0), ("Abril", 1), ("Maio", 0), ("Junho", 0)]
EP = {
    "nome": "11-fgts",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:290px}#ex{position:absolute;left:150px;width:780px;top:350px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:22px 30px;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#ex h3{font:600 22px Inter;letter-spacing:.1em;opacity:.7;margin-bottom:6px}
.m{display:flex;justify-content:space-between;font:400 34px/2.1 Inter;border-top:1.5px dashed rgb(30 24 20/.2);position:relative;padding:0 12px}
.m b{font-weight:600}.m i{position:absolute;inset:6px -2px;border:4px solid #bb923f;border-radius:14px}
#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>extrato do FGTS</div><div id=ex data-m=1><h3>DEPÓSITOS · 8% DE R$ 2.400</h3>"""
    + "".join(f'<div class=m id=m{i}><span>{a}</span><b>{"R$ 192,00" if ok else "—"}</b>{"" if ok else f"<i id=h{i}></i>"}</div>' for i, (a, ok) in enumerate(MESES))
    + """</div><div class=marca id=q><span>Cadê o depósito?</span></div><div class=sub id=s>Confira no aplicativo FGTS.</div>""",
    "js": """const F=%s;
function cena(t){
 sobe('r1',t,.2);sobe('ex',t,.4,.5);
 F.forEach((ok,i)=>{sobe('m'+i,t,1.0+i*.7,.3);if(!ok){const h=$('h'+i),a=t-(6.0+[0,0,0,0,.5,1][i]);h.style.opacity=a<0?0:.6+.4*Math.abs(Math.cos(a*5));h.style.clipPath=`inset(0 ${(1-ioo(a/.4))*100}%% 0 0)`}});
 marca('q',t,8.6);sobe('s',t,10.4);
 $('cena').style.transform=`translateX(${treme(t,[6.0,6.5,7.0])}px)`;
}""" % str([ok for _, ok in MESES]).replace("True", "1").replace("False", "0"),
    "sons": [(.4, "pagina")] + [(1.0 + i * .7, "tique" if ok else "carimbo", .8 if ok else .4) for i, (_, ok) in enumerate(MESES)]
            + [(6.0, "erro", .6), (6.5, "erro", .5), (7.0, "erro", .5), (8.55, "whoosh"), (8.7, "escreve"), (9.2, "brilho", .7),
               (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "", "legenda": "Janeiro: depositado.\nFevereiro: depositado.\nMarço: nada. Maio: nada. Junho: nada.\n\nCadê o depósito?\n\nA empresa deve depositar todo mês 8% do salário na conta do FGTS do trabalhador (Lei 8.036/1990, art. 15). O desconto não sai do seu salário: é obrigação da empresa.\n\nO que vale saber:\n📌 Confira o extrato no aplicativo FGTS, mês a mês\n📌 Falta de depósito pode ser cobrada, com correção\n📌 Falta repetida pode permitir a rescisão indireta (CLT, art. 483)\n📌 Tire um print do extrato e guarde\n\nComente: você já conferiu o seu FGTS? E mande para quem nunca abriu o aplicativo.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n#direitotrabalhista #fgts #clt #direitosdotrabalhador #advogadatrabalhista"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
