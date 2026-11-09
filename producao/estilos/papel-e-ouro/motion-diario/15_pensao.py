"""Flagrante 15 · Pensão atrasada (público: a mãe que recebe pela criança). Extrato mês a mês e a mensagem do pai."""
from motor import rodar

MESES = [("Agosto", 1), ("Setembro", 0), ("Outubro", 0), ("Novembro", 0)]
EP = {
    "nome": "15-pensao",
    "dur": 20.0,
    "salve": "",
    "css": """#r1{top:286px}#ex{position:absolute;left:150px;width:780px;top:336px;background:#EFE6D9;color:#1E1814;border-radius:18px;padding:20px 30px;box-shadow:0 14px 34px rgb(0 0 0/.35)}
#ex h3{font:600 22px Inter;letter-spacing:.1em;opacity:.7;margin-bottom:4px}
.m{display:flex;justify-content:space-between;font:400 34px/2.0 Inter;border-top:1.5px dashed rgb(30 24 20/.2);position:relative;padding:0 12px}
.m b{font-weight:600}.m i{position:absolute;inset:6px -2px;border:4px solid #bb923f;border-radius:14px}
#b0{top:770px}#q{top:1000px}#s{top:1126px}""",
    "html": """<div class=rot id=r1>pensão do Pedro · vence dia 10</div><div id=ex data-m=1><h3>PIX RECEBIDOS</h3>"""
    + "".join(f'<div class=m id=m{i}><span>{a}</span><b>{"R$ 600,00" if ok else "—"}</b>{"" if ok else f"<i id=h{i}></i>"}</div>' for i, (a, ok) in enumerate(MESES))
    + """</div><div class="bo ele" id=b0>Esse mês não dá. Depois eu vejo.<small>22:14</small></div>
<div class=marca id=q><span>Atrasou. E agora?</span></div><div class=sub id=s>Comente se você passa por isso.</div>""",
    "js": """const F=[1,0,0,0];
function cena(t){
 sobe('r1',t,.1);sobe('ex',t,.3,.5);
 F.forEach((ok,i)=>{sobe('m'+i,t,.9+i*.8,.3);if(!ok){const h=$('h'+i),a=t-(.9+i*.8+.35);h.style.opacity=a<0?0:.6+.4*Math.abs(Math.cos(a*5));h.style.clipPath=`inset(0 ${(1-ioo(a/.4))*100}% 0 0)`}});
 nasce('b0',t,5.0);const d=1-.5*ioo((t-8.0)/.6);$('ex').style.filter=$('b0').style.filter=`brightness(${d})`;
 marca('q',t,8.4);sobe('s',t,10.2);
 $('cena').style.transform=`translateX(${treme(t,[2.05,2.85,3.65,5.0])}px)`;
}""",
    "sons": [(.3, "pagina"), (.9, "moedas", .7)] + [(1.7 + i * .8, "erro", .45) for i in range(3)]
            + [(5.0, "pop"), (5.0, "vibra"), (8.35, "whoosh"), (8.5, "escreve"), (9.0, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)],
    "legenda": {"primeiro_comentario": "Artigo completo: https://advogadaleticiabarros.com.br/blog/ex-nao-paga-pensao-o-que-fazer.html",
                "legenda": "Agosto: R$ 600.\nSetembro: nada. Outubro: nada. Novembro: nada.\n\"Esse mês não dá. Depois eu vejo.\"\n\nAtrasou. E agora?\n\nMãe, pensão não é favor: é direito da criança. Quando existe acordo homologado ou decisão da Justiça, o atraso pode ser cobrado no processo (CPC, art. 528).\n\nO que vale saber:\n📌 Com até 3 meses de atraso, dá para pedir a prisão civil de quem deve (Súmula 309 do STJ)\n📌 Também é possível pedir penhora de bens, desconto em folha e protesto do nome\n📌 Não precisa esperar acumular muitos meses para agir\n📌 Guarde os comprovantes de Pix e as mensagens\n📌 Se ainda não há pensão fixada na Justiça, o primeiro passo é pedir a fixação\n\nO link do artigo completo está no primeiro comentário.\n\nComente se você passa por isso. E mande para uma mãe que precisa saber disso.\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\nEsse é o perfil da Advogada Letícia Barros e aqui você encontra informação sobre os seus direitos e os do seu filho.\n\n#pensaoalimenticia #direitodefamilia #maesolo #direitosdacrianca #advogada"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
