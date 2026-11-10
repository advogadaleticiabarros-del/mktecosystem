"""Flagrante 34 · Série Mito ou Lei (piloto dinâmico): "Feriado trabalhado é hora extra de 50%" -> MITO.

Mecânica nova: título que cai letra a letra, afirmação digitada, roleta MITO/LEI com suspense,
carimbo com impacto, contador 50% -> 100% e calendário de folga.
"""
from motor import rodar

LEG = (
    "Trabalhou no feriado? Então é hora extra de 50%. Mito.\n\n"
    "Muita gente recebe o feriado como se fosse uma hora extra comum, e perde dinheiro sem perceber.\n\n"
    "Eu explico, sem juridiquês:\n\n"
    "📌 Feriado trabalhado sem outro dia de folga na semana deve ser pago em dobro (100%), não com 50%.\n"
    "📌 Se a empresa der uma folga compensatória em outro dia, ela não precisa pagar o dobro.\n"
    "📌 Convenção coletiva pode trazer regra própria da sua categoria. Vale conferir.\n"
    "📂 Essa é a parte decisiva: guarde a escala e o holerite do mês do feriado.\n\n"
    "📚 Base legal: Lei 605/1949, art. 9º; Súmula 146 do TST.\n\n"
    "Cada caso tem detalhes. Procure uma advogada de confiança.\n\n"
    "Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.\n\n"
    "Letícia Barros · OAB/ES 39.948\n\n"
    "#MitoOuLei #DireitoTrabalhista #Feriado #DireitosDoTrabalhador #HoraExtra"
)

EP = {
    "nome": "34-mito-feriado",
    "dur": 24.0,
    "salve": "",
    "css": """
#tt{position:absolute;top:300px;left:150px;right:150px;text-align:center;font:500 104px/1 'EB Garamond',serif;letter-spacing:.02em;white-space:nowrap}
#tt i{display:inline-block;font-style:normal}
#tt .q{font-style:italic}
#af{top:470px;min-height:250px}
#af .m{font:500 50px/1.22 'EB Garamond',serif;min-height:190px}
#cur{display:inline-block;width:4px;height:48px;background:#1E1814;margin-left:4px;vertical-align:-6px}
#op{position:absolute;top:800px;left:150px;width:780px;display:flex;gap:40px;justify-content:center}
#op div{width:340px;height:150px;border-radius:24px;border:3px solid #6B5A45;display:flex;align-items:center;justify-content:center;font:500 82px 'EB Garamond',serif;letter-spacing:.06em}
#ca{position:absolute;top:500px;left:240px;width:600px;text-align:center;padding:10px 0 18px;border:12px double #C9A15A;border-radius:18px;color:#D9B26B;font:600 170px/1 'EB Garamond',serif;letter-spacing:.08em}
#pc{top:780px;font-size:240px}
#pr{top:760px;font-size:36px}
#cal{position:absolute;top:1130px;left:390px;width:300px;height:150px;background:#EFE6D9;color:#1E1814;border-radius:20px;overflow:hidden;box-shadow:0 12px 30px rgb(0 0 0/.35);text-align:center}
#cal b{display:block;background:#8E2F2A;color:#EFE6D9;font:600 26px/44px Inter}
#cal span{font:500 30px/100px Inter}
#q{top:820px}#s{top:950px}
""",
    "html": """<div id=tt><i>M</i><i>i</i><i>t</i><i>o</i>&nbsp;<i>o</i><i>u</i>&nbsp;<i class=ouro>L</i><i class=ouro>e</i><i class=ouro>i</i><i class=q>?</i></div>
<div class=card id=af><div class=t><b>Ouvi no trabalho</b><span>feriado</span></div><div class=m><span id=tx></span><span id=cur></span></div></div>
<div id=op><div id=om>MITO</div><div id=ol>LEI</div></div>
<div id=ca>MITO</div>
<div class="big ouro" id=pc data-m=1>50%</div>
<div class=rot id=pr>sem folga em outro dia, é em dobro</div>
<div id=cal><b>FOLGA</b><span>outro dia da semana</span></div>
<div class=marca id=q><span>Você recebeu certo?</span></div><div class=sub id=s>Comente aqui embaixo.</div>""",
    "js": """const FR='Trabalhou no feriado? Recebe hora extra de 50%.';
function cena(t){
 // título cai letra a letra
 document.querySelectorAll('#tt i').forEach((e,i)=>{const a=t-.15-i*.07;e.style.opacity=a<0?0:1;
  e.style.transform=`translateY(${-120*(1-mola(a/.6))}px) rotate(${(1-mola(a/.6))*(i%2?8:-8)}deg)`});
 const z=1+.06*Math.exp(-(t-1.0)*6)*(t>1?1:0);$('tt').style.transform=`scale(${z})`;
 // afirmação digitada
 nasce('af',t,1.6);const n=Math.floor(cl((t-2.0)/1.9)*FR.length);$('tx').textContent=FR.slice(0,n);
 $('cur').style.opacity=t<7.6&&Math.floor(t*2.4)%2==0?1:0;
 // roleta MITO / LEI
 sobe('op',t,4.3,.4);const r=t>=4.6&&t<7.6;let lado=-1;
 if(r){const v=Math.floor(Math.pow(t-4.6,1.6)*2.2);lado=v%2}
 if(t>=7.6)lado=0;
 [['om',0],['ol',1]].forEach(([id,k])=>{const e=$(id),on=lado===k;
  e.style.background=on?'#C9A15A':'transparent';e.style.color=on?'#1E1814':'#EFE6D9';
  e.style.transform=`scale(${on?1.06:1})`;e.style.opacity=t>=7.6&&k===1?.3:1});
 // carimbo
 const c=t-7.8;$('ca').style.opacity=c<0?0:cl(c/.06)*(1-cl((t-10.6)/.4));
 $('ca').style.transform=`rotate(-9deg) scale(${c<0?2.6:2.6-1.6*io(c/.16)+(c>.16?.05*Math.exp(-(c-.16)*8)*Math.sin((c-.16)*40):0)})`;
 {const f=c<0?0:.5*Math.exp(-c*9);$('c').style.background=`rgb(${35+(243-35)*f},${30+(212-30)*f},${26+(140-26)*f})`}
 $('af').style.filter=`blur(${cl((t-10.6)/.4)*6}px)`;$('af').style.opacity=t>=1.6?(1-cl((t-10.6)/.4)):0;
 $('op').style.opacity=t>=4.3?cl((t-4.3)/.4)*(1-cl((t-10.6)/.4)):0;
 // contador 50% -> 100%
 const p=t-11.0;$('pc').style.opacity=p<0?0:cl(p/.3)*(1-cl((t-17.0)/.4));
 const k=io((p-.6)/1.4);$('pc').textContent=Math.round(50+50*k)+'%';
 $('pc').style.transform=`translateY(-280px) scale(${1+.12*Math.exp(-(p-2.0)*7)*(p>2?1:0)})`;
 sobe('pr',t,13.0);if(t>17)$('pr').style.opacity=1-cl((t-17)/.4);
 $('cal').style.transform=`translateY(-280px) scale(${t<14.6?0:mola((t-14.6)/.7)})`;$('cal').style.opacity=t<14.6?0:1-cl((t-17)/.4);
 // pergunta
 marca('q',t,17.5);sobe('s',t,18.6);
 $('cena').style.transform=`translate(${treme(t,[1.0,7.8,13.0],9)}px,${treme(t,[7.8],6)}px)`;
}""",
    "sons": [(.15, "whoosh"), (1.0, "boom", .7), (1.6, "pop"), (2.0, "digita", .9), (4.3, "whoosh", .6),
             (4.7, "relogio", .8), (7.6, "erro", .5), (7.8, "carimbo"), (7.8, "boom"), (11.0, "whoosh", .7),
             (11.6, "moedas"), (13.0, "sino", .8), (13.0, "brilho", .6), (14.6, "pagina"), (14.7, "bolha"),
             (17.4, "whoosh"), (17.6, "escreve"), (18.2, "brilho", .7)],
    "legenda": {"legenda": LEG, "primeiro_comentario": "💬 Você já trabalhou num feriado? Recebeu em dobro ou só 50%?"},
}

if __name__ == "__main__":
    rodar(EP, __file__)
