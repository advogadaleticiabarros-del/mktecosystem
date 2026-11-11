"""Série Mito ou Lei em Reels (estilo Flagrante), a partir do piloto 34_mito_feriado.py aprovado em 10/11/2026
("perfeito, agora vamos trocar todos dessa serie para reels nesse mesmo estilo").

Uso: python mito_lei.py amostras|video [MM-DD ...]   (sem datas = todos)
Saída: mito-lei/<MM-DD>-<slug>/<MM-DD>-<slug>-v2.mp4 + legenda.json
O texto jurídico da legenda vem de apps/api/_saida_producao_1510/conteudo_{nov,dez}.py (MITO_OU_LEI)."""
import sys
from pathlib import Path

import motor

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "apps" / "api" / "_saida_producao_1510"))
import conteudo_dez  # noqa: E402
import conteudo_jan  # noqa: E402  (janeiro de 2027, pedido de 10/11/2026)
import conteudo_fev  # noqa: E402  (fevereiro de 2027, pedido de 11/11/2026)
import conteudo_nov  # noqa: E402

# data: (frase na tela, número/destaque, linha de apoio, chip (título, texto) ou None, pergunta em marca-texto)
TELA = {
    "11-08": ("O 13º pode ser pago numa parcela só, em dezembro.", "30/11", "último dia da 1ª parcela", ("PARCELA ÚNICA", "só se for até 30/11"), "Uma ou duas?"),
    "11-10": ("Grávida com estabilidade pode pedir demissão sozinha.", "Sindicato", "o pedido só vale com assistência", ("SEM ISSO", "pode ser anulado"), "Você sabia?"),
    "11-12": ("Aborto espontâneo dá direito a repouso remunerado.", "2 semanas", "de repouso pago, com atestado", ("NA VOLTA", "a mesma função"), "Você sabia?"),
    "11-14": ("A licença-maternidade pode começar antes do parto.", "28 dias", "antes do parto, com atestado", None, "Você sabia?"),
    "11-16": ("Pai não tem licença quando o filho nasce.", "5 dias", "ou 20 na Empresa Cidadã", ("2027", "o prazo começa a subir"), "Quantos dias?"),
    "11-18": ("Trabalhou no feriado? Recebe hora extra de 50%.", "100%", "sem folga em outro dia, é em dobro", ("OU ENTÃO", "folga em outro dia da semana"), "Você recebeu certo?"),
    "11-20": ("Piada racista no trabalho é só brincadeira.", "2 a 5 anos", "injúria racial é crime", ("EM TOM DE PIADA", "a pena aumenta"), "Ainda é piada?"),
    "11-22": ("A pensão da gravidez vira pensão do bebê depois do parto.", "Continua", "sem precisar de outro processo", ("REVISÃO", "só se alguém pedir"), "Você sabia?"),
    "11-24": ("Quem nunca contribuiu não recebe nada do INSS.", "BPC", "1 salário mínimo, sem contribuição", None, "Conhecia o BPC?"),
    "11-26": ("MEI tem salário-maternidade.", "120 dias", "de salário-maternidade para a MEI", ("CONDIÇÃO", "INSS em dia"), "Você sabia?"),
    "11-28": ("Aposentada perde a pensão por morte.", "Os dois", "aposentadoria e pensão juntas", ("O MENOR", "vem com redução"), "Achava que não?"),
    "11-30": ("Hoje vence a 1ª parcela do 13º.", "30/11", "último dia da 1ª parcela", ("HOJE", "confira o extrato"), "Já caiu?"),
    "12-02": ("Quem paga pensão pode levar o filho quando quiser.", "Acordo", "a convivência segue o combinado", ("PENSÃO", "não muda as datas"), "Já combinaram?"),
    "12-04": ("Quem vive com HIV precisa contar para a empresa.", "Escolha", "contar é decisão da pessoa", ("DEMITIR POR ISSO", "é crime"), "Você sabia?"),
    "12-06": ("Empresa com 100 funcionários precisa ter cota de inclusão.", "2% a 5%", "das vagas para PcD ou reabilitados", None, "Sua empresa cumpre?"),
    "12-08": ("Burnout não é doença do trabalho.", "Desde 2023", "na lista oficial de doenças do trabalho", ("PODE GERAR", "afastamento e estabilidade"), "Conhece alguém?"),
    "12-10": ("Gritar com funcionário na frente de todos é só jeito do chefe.", "Assédio", "humilhar pode gerar indenização", ("QUEM RESPONDE", "a empresa"), "Já viu isso?"),
    "12-12": ("Assédio sexual no trabalho é crime.", "1 a 2 anos", "de detenção, Código Penal", None, "Você sabia?"),
    "12-14": ("A 2ª parcela do 13º vem sem descontos.", "INSS + IR", "os descontos vêm na 2ª parcela", None, "Já conferiu?"),
    "12-16": ("BPC dá direito a 13º.", "12 parcelas", "por ano, sem abono", ("13º", "só aposentado e pensionista"), "Achava que tinha?"),
    "12-18": ("A 2ª parcela do 13º tem que cair até sexta, 18/12.", "18/12", "20/12 cai no domingo", ("ATÉ SEXTA", "confira o extrato"), "Já tem data?"),
    "12-20": ("Temporário de fim de ano não tem FGTS.", "FGTS", "depositado também no temporário", ("E MAIS", "13º e férias proporcionais"), "Já conferiu?"),
    "12-22": ("24 e 31 de dezembro são feriados nacionais.", "25/12 e 01/01", "esses são os feriados nacionais", ("VÉSPERAS", "dia normal, salvo lei local"), "Você trabalha?"),
    "12-24": ("Viajar com o filho no Brasil sempre exige autorização do outro genitor.", "No Brasil", "com o pai ou a mãe, não precisa", ("EXTERIOR", "precisa de autorização"), "Vai viajar?"),
    "12-26": ("Pensão em salário mínimo aumenta sozinha em janeiro.", "Sobe junto", "com o salário mínimo, sem processo", None, "Vai conferir?"),
    "12-28": ("Os prazos do processo trabalhista param no fim do ano.", "20/12 a 20/01", "prazos suspensos na Justiça do Trabalho", None, "Você sabia?"),
    "12-30": ("Férias coletivas podem ser divididas em 3 partes.", "2 partes", "no máximo, por ano", ("CADA UMA", "com 10 dias ou mais"), "Já está de férias?"),
    # janeiro de 2027 (conteudo_jan.py): afirmações já aprovadas como estático que ainda não tinham virado Reels
    "01-13": ("Quem foi demitido não recebe 13º.", "Proporcional", "1/12 por mês trabalhado", ("SÓ PERDE", "quem sai por justa causa"), "Recebeu o seu?"),
    "01-16": ("Atestado médico reduz o 13º.", "Não reduz", "falta justificada não desconta", ("MAIS DE 15 DIAS", "o INSS paga essa parte"), "Já descontaram?"),
    "01-18": ("Faltar para fazer mamografia dá desconto no salário.", "3 dias", "por ano, sem desconto", ("LEVE", "o comprovante do exame"), "Já marcou o seu?"),
    "01-20": ("Quem tem câncer recebe do INSS sem cumprir carência.", "Sem carência", "o câncer dispensa a carência", ("PRECISA", "ser segurada e passar na perícia"), "Você sabia?"),
    "01-23": ("Com medida protetiva, dá para se afastar do trabalho sem perder o emprego.", "6 meses", "de afastamento, com o emprego mantido", ("EM PERIGO", "ligue 190"), "Você sabia?"),
    "01-25": ("Mãe por adoção tem os mesmos 120 dias de licença.", "120 dias", "qualquer que seja a idade da criança", None, "Você sabia?"),
    "01-27": ("Salário nunca pode ser penhorado.", "Em parte", "em caso excepcional, decide o STJ", ("SEMPRE FICA", "o mínimo para viver"), "Achava que não?"),
    "01-30": ("Depois dos 70, o casamento é sempre com separação de bens.", "Escritura", "permite escolher outro regime", ("SEM ESCRITURA", "vale a separação"), "Conhece um casal?"),
    # fevereiro de 2027 (conteudo_fev.py, textos novos de 11/11/2026: conferência jurídica da Dra. pendente)
    "02-01": ("A escola pode pedir papel higiênico na lista.", "Proibido", "material de uso coletivo", ("JÁ ESTÁ", "no valor da mensalidade"), "Já te pediram?"),
    "02-03": ("Mensalidade atrasada: a escola pode barrar a prova.", "Proibido", "suspender prova por atraso", ("A ESCOLA PODE", "cobrar a dívida"), "Você sabia?"),
    "02-06": ("A empresa pode exigir teste de gravidez para contratar.", "Crime", "exigir teste de gravidez", ("TAMBÉM É", "discriminação"), "Já te pediram?"),
    "02-08": ("Carnaval é feriado nacional.", "Não é", "feriado por lei federal", ("FOLGA SÓ COM", "lei local ou acordo"), "É feriado aí?"),
    "02-10": ("O pai pode faltar para ir ao pré-natal.", "2 dias", "sem desconto no salário", ("CONSULTAS", "e exames da gestante"), "Ele foi junto?"),
    "02-13": ("Dá para faltar 1 dia por ano para levar o filho ao médico.", "1 dia", "por ano, sem desconto", ("FILHO", "de até 6 anos"), "Já usou o seu?"),
    "02-15": ("Quem pede demissão saca o FGTS.", "Fica", "o FGTS fica na conta", None, "Achava que sim?"),
    "02-17": ("O aviso prévio é sempre de 30 dias.", "Até 90", "dias, conforme os anos de casa", ("+3 DIAS", "por ano completo"), "Quantos anos?"),
    "02-20": ("Hora extra frequente aumenta o 13º e as férias.", "Entra", "na média do 13º e das férias", ("CONFIRA", "o holerite dessas parcelas"), "Você confere?"),
    "02-22": ("A empresa pode descontar o uniforme do salário.", "Não pode", "uniforme exigido é custo dela", None, "Já descontaram?"),
    "02-24": ("O vale-transporte pode descontar até 6% do salário.", "6%", "do salário básico, no máximo", ("PASSOU DISSO", "a empresa paga"), "Quanto é o seu?"),
    "02-27": ("Empregada doméstica tem FGTS obrigatório.", "Desde 2015", "FGTS e indenização todo mês", ("PELO", "eSocial"), "Está em dia?"),
}

# gancho (10/11/2026): afirmação na tela já no 1º segundo + desafio "responda antes da roleta parar"; roleta de 2,4 a 7,6 s
SONS_FIXOS = [(0, "whoosh"), (.1, "pop"), (.25, "digita", .6), (.75, "boom", .8), (1.25, "sino", .5), (2.3, "whoosh", .6),
              ] + [(2.4 + 5.2 * (1 - (1 - k / 40) ** (1 / 3)), "clique", .9) for k in range(1, 41)] + [(7.17, "vento", 1.0), (7.87, "batida", 1.0), (11.0, "whoosh", .7),
              (11.6, "moedas", .7), (13.0, "sino", .8), (13.0, "brilho", .6), (15.2, "pagina", .8), (16.4, "tique", .8), (19.4, "whoosh"), (19.6, "escreve"),
              (20.2, "brilho", .7), (24.5, "whoosh", .5), (25.3, "pop", 1.0), (25.35, "brilho", .7)]

CSS = """
#tt{position:absolute;top:300px;left:150px;right:150px;text-align:center;font:500 104px/1 'EB Garamond',serif;letter-spacing:.02em;white-space:nowrap}
#tt i{display:inline-block;font-style:normal}
#tt .q{font-style:italic}
#af{top:470px}
#af .m{font:500 46px/1.22 'EB Garamond',serif;min-height:170px}
#cur{display:inline-block;width:4px;height:44px;background:#1E1814;margin-left:4px;vertical-align:-6px}
#op{position:absolute;top:830px;left:150px;width:780px;display:flex;gap:40px;justify-content:center}
#op div{width:340px;height:150px;border-radius:24px;border:3px solid #6B5A45;display:flex;align-items:center;justify-content:center;font:500 82px 'EB Garamond',serif;letter-spacing:.06em}
#ca{position:absolute;top:500px;left:240px;width:600px;text-align:center;padding:10px 0 18px;border:14px double;border-radius:18px;font:700 170px/1 'EB Garamond',serif;letter-spacing:.08em}
#ca.mito{color:#FF2E2E;border-color:#FF2E2E;text-shadow:0 0 28px rgb(255 40 40/.6);box-shadow:0 0 40px rgb(255 40 40/.45),inset 0 0 30px rgb(255 40 40/.25)}
#ca.lei{border-color:#F5C451;background:linear-gradient(100deg,#B8862B,#FFE7A0 45%%,#C9932E 60%%,#FFF1C2);-webkit-background-clip:text;background-clip:text;color:transparent;box-shadow:0 0 44px rgb(255 205 90/.55),inset 0 0 30px rgb(255 205 90/.25);filter:drop-shadow(0 0 18px rgb(255 210 100/.6))}
#tinta{position:absolute;left:540px;top:600px;width:0;height:0}
#tinta i{position:absolute;border-radius:50%%}
#onda{position:absolute;left:540px;top:600px;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%%;border:8px solid}
#pc{top:500px;font-size:%(fs)dpx;white-space:nowrap}
#pr{top:%(prt)dpx;font-size:36px}
#ex{top:%(ext)dpx;padding:22px 30px 24px}#ex .m{font:400 33px/1.34 Inter;margin:0}
#bl{top:%(blt)dpx;font:500 27px Inter;color:#D8B566}
#cal{position:absolute;top:%(calt)dpx;left:240px;width:600px;background:#EFE6D9;color:#1E1814;border-radius:20px;overflow:hidden;box-shadow:0 12px 30px rgb(0 0 0/.35);text-align:center}
#cal b{display:block;background:#8E2F2A;color:#EFE6D9;font:600 26px/44px Inter;letter-spacing:.06em}
#cal span{display:block;font:500 32px/1.25 Inter;padding:22px 20px}
#rol{position:absolute;left:0;top:1281px;width:1080px;height:620px}
#dz{top:730px;font:600 38px Inter;color:#F5C451;letter-spacing:.02em}
#segue{position:absolute;left:190px;width:700px;top:1330px;display:flex;align-items:center;gap:22px;background:#EFE6D9;color:#1E1814;border-radius:999px;padding:16px 18px 16px 18px;box-shadow:0 14px 34px rgb(0 0 0/.4);opacity:0}
#segue .av{width:84px;height:84px;border-radius:50%%;background:linear-gradient(135deg,#B8862B,#FFE7A0,#C9932E);display:flex;align-items:center;justify-content:center;font:600 36px 'EB Garamond',serif;color:#1E1814;flex:none}
#segue .nm{flex:1;font:600 30px/1.2 Inter}#segue .nm small{display:block;font:400 25px Inter;opacity:.65}
#segue .bt{flex:none;padding:16px 30px;border-radius:16px;background:#1F6FEB;color:#fff;font:600 30px Inter;position:relative;overflow:visible}
#segue .rp{position:absolute;left:50%%;top:50%%;width:20px;height:20px;margin:-10px;border-radius:50%%;border:5px solid #F5C451;opacity:0}
#mao{position:absolute;font-size:84px;left:760px;top:1420px;opacity:0}
#q{top:820px}#s{top:950px}
"""

JS = """const FR=%(fr)s,VER=%(ver)d,BIG=%(big)s,NUM=%(num)s;
function cena(t){
 document.querySelectorAll('#tt i').forEach((e,i)=>{const a=t-.15-i*.07;e.style.opacity=a<0?0:1;
  e.style.transform=`translateY(${-120*(1-mola(a/.6))}px) rotate(${(1-mola(a/.6))*(i%%2?8:-8)}deg)`});
 const z=1+.06*Math.exp(-(t-.75)*6)*(t>.75?1:0);$('tt').style.transform=`scale(${z})`;
 nasce('af',t,.1);const n=Math.floor(cl((t-.25)/.85)*FR.length);$('tx').textContent=FR.slice(0,n);
 $('cur').style.opacity=t<7.6&&Math.floor(t*2.4)%%2==0?1:0;
 sobe('op',t,2.3,.4);sobe('dz',t,1.25,.35);if(t>7.4)$('dz').style.opacity=1-cl((t-7.4)/.2);
 const cz=t>=1.25&&t<7.6?1+.04*Math.sin(t*9):1;$('dz').style.scale=cz;let lado=-1;
 {const cv=$('rol'),x=cv.getContext('2d'),N=8,W=2*Math.PI/N,R=520,cx=540,cy=620;
  const alvo=-Math.PI/2-(VER===0?0:W)-W/2,gir=alvo-10*Math.PI;
  const u=cl((t-2.4)/5.2),ang=gir+(alvo-gir)*(1-Math.pow(1-u,3));
  const ap=t<2.3?0:cl((t-2.3)/.4)*(1-cl((t-10.6)/.4));cv.style.opacity=ap;
  x.clearRect(0,0,1080,620);
  for(let i=0;i<N;i++){const a0=ang+i*W,mito=i%%2===0,ganha=t>=7.89&&(mito?0:1)===VER&&Math.abs(((a0+W/2+Math.PI/2)%%(2*Math.PI)+2*Math.PI)%%(2*Math.PI))<.01;
   x.beginPath();x.moveTo(cx,cy);x.arc(cx,cy,R,a0,a0+W);x.closePath();
   x.fillStyle=mito?(ganha?'#FF2E2E':'#6E2320'):(ganha?'#FFE58F':'#A8823F');x.fill();x.strokeStyle='#1E1814';x.lineWidth=4;x.stroke();
   x.save();x.translate(cx,cy);x.rotate(a0+W/2);x.fillStyle=mito?'#EFE6D9':'#1E1814';x.font="600 54px 'EB Garamond'";x.textAlign='right';x.textBaseline='middle';x.fillText(mito?'MITO':'LEI',R-44,0);x.restore()}
  x.beginPath();x.arc(cx,cy,R,Math.PI,2*Math.PI);x.strokeStyle='#D8B566';x.lineWidth=6;x.stroke();
  x.beginPath();x.arc(cx,cy,90,0,2*Math.PI);x.fillStyle='#231E1A';x.fill();x.strokeStyle='#D8B566';x.lineWidth=5;x.stroke();
  const bat=t>=2.4&&t<7.6?Math.sin(t*60)*Math.pow(1-u,2)*.25:0;
  x.save();x.translate(cx,cy-R-6);x.rotate(bat);x.beginPath();x.moveTo(-30,-34);x.lineTo(30,-34);x.lineTo(0,32);x.closePath();x.fillStyle='#F5C451';x.fill();x.restore();}
 if(t>=2.4&&t<7.6){lado=Math.floor(Math.pow(t-2.4,1.3)*2.4)%%2}
 if(t>=7.6)lado=VER;
 [['om',0],['ol',1]].forEach(([id,k])=>{const e=$(id),on=lado===k;
  const fim=t>=7.89&&on;e.style.background=on?(fim&&VER===0?'#E3262A':'#C9A15A'):'transparent';e.style.color=on?(fim&&VER===0?'#FFF':'#1E1814'):'#EFE6D9';
  e.style.transform=`scale(${on?1.06:1})`;e.style.opacity=t>=7.6&&k!==VER?.3:1});
 const c=t-7.55,D=.34,CR=VER?[255,205,90]:[255,46,46];$('ca').style.opacity=c<0?0:cl(c/.15)*(1-cl((t-10.6)/.4));
 $('ca').style.transform=`rotate(${-9+(c>D?3*Math.exp(-(c-D)*10)*Math.sin((c-D)*50):0)}deg) scale(${c<0?3.2:c<D?3.2-2.2*Math.pow(c/D,3):1+.09*Math.exp(-(c-D)*9)*Math.cos((c-D)*45)})`;
 {const e=c-D,o=$('onda');o.style.opacity=e<0?0:.9*(1-cl(e/.55));{const w=20+io(e/.55)*760;o.style.width=o.style.height=w+'px';o.style.margin=`${-w/2}px 0 0 ${-w/2}px`}o.style.borderWidth='6px';o.style.borderColor=`rgb(${CR})`;
  document.querySelectorAll('#tinta i').forEach((g,i)=>{const a=i*2.399,v=180+(i*53%%170),k=io(e/.35);g.style.opacity=e<0?0:1-cl((e-.6)/.8);
  g.style.transform=`translate(${Math.cos(a)*v*k}px,${Math.sin(a)*v*k*.7}px) scale(${e<0?0:1})`;g.style.background=`rgb(${CR})`})}
 $('cena').style.scale=1+(c>D?.05*Math.exp(-(c-D)*7):0);
 {const f=c<D?0:.6*Math.exp(-(c-D)*8);$('c').style.background=`rgb(${35+(CR[0]-35)*f},${30+(CR[1]-30)*f},${26+(CR[2]-26)*f})`}
 $('af').style.filter=`blur(${cl((t-10.6)/.4)*6}px)`;$('af').style.opacity=t>=.1?(1-cl((t-10.6)/.4)):0;
 $('op').style.opacity=t>=2.3?cl((t-2.3)/.4)*(1-cl((t-10.6)/.4)):0;
 const p=t-11.0,sai=1-cl((t-19.0)/.4);
 if(NUM){const k=io((p-.4)/1.2);$('pc').textContent=BIG.replace(/\\d+/,m=>Math.round(+m*k));}
 else{const L=Math.floor(cl((p-.2)/.9)*BIG.length);$('pc').textContent=BIG.slice(0,Math.max(1,L));}
 $('pc').style.opacity=p<0?0:cl(p/.3)*sai;
 $('pc').style.transform=`scale(${1+.12*Math.exp(-(p-1.8)*7)*(p>1.8?1:0)})`;
 sobe('pr',t,13.0);if(t>19)$('pr').style.opacity=sai;
 $('bl').style.top=($('ex').offsetTop+$('ex').offsetHeight+22)+'px';sobe('ex',t,15.2,.45);sobe('bl',t,16.4,.4);if(t>19){$('ex').style.opacity=sai;$('bl').style.opacity=sai}
 const ca=$('cal');if(ca){ca.style.transform=`scale(${t<14.6?0:mola((t-14.6)/.7)})`;ca.style.opacity=t<14.6?0:sai}
 {const sg=$('segue'),mo=$('mao');if(sg.parentElement.id==='cena'){$('c').appendChild(sg);$('c').appendChild(mo)}
  const a=t-24.5;sg.style.opacity=cl(a/.35);sg.style.transform=`translateY(${(1-io(a/.5))*40}px) scale(${t>=25.3?1+.05*Math.exp(-(t-25.3)*8):1})`;
  mo.style.opacity=cl((t-24.8)/.2)*(1-cl((t-26.2)/.3));const pm=io((t-24.8)/.5);mo.style.transform=`translate(${(1-pm)*120}px,${(1-pm)*160+(t>=25.2&&t<25.4?14:0)}px)`;
  const on=t>=25.3,bt=sg.querySelector('.bt');bt.style.background=on?'#C9A15A':'#1F6FEB';bt.style.color=on?'#1E1814':'#fff';$('btx').textContent=on?'Seguindo ✓':'Seguir';
  const r=t-25.3,rp=$('rp');rp.style.opacity=r<0?0:1-cl(r/.5);rp.style.transform=`scale(${1+io(r/.5)*9})`}
 marca('q',t,19.5);sobe('s',t,20.6);
 $('cena').style.transform=`translate(${treme(t,[.75,13.0],9)+treme(t,[7.89,8.1],26)}px,${treme(t+.05,[7.89,8.1],18)}px)`;
}"""


def itens():
    for mes, dados in (("nov", conteudo_nov), ("dez", conteudo_dez), ("jan", conteudo_jan), ("fev", conteudo_fev)):
        for m in dados.MITO_OU_LEI:
            md = m[0][5:]
            if md in TELA and TELA[md]:
                yield md, m


def tamanho(txt):
    n = len(txt)
    return 220 if n <= 5 else 180 if n <= 8 else 140 if n <= 11 else 110


# ajustes por causa da data nova (segunda, quarta e sábado às 19h, pedido de 10/11/2026)
AJUSTE = {
    "12-18": {"afirm": "A 2ª parcela do 13º tem que cair até sexta, 18/12.",
              "expl": "O prazo legal é 20/12, um domingo em 2026. Por isso, o pagamento deve sair até sexta, 18/12.",
              "pergunta": "A sua 2ª parcela já tem data?"},
    "11-20": {"pergunta": "Deixa um ✊🏾 pela Consciência Negra."},
}


def legenda(m):
    _, _, afirm, ver, expl, base, tags, _, _, manda, pergunta = m
    aj = AJUSTE.get(m[0][5:], {})
    afirm, expl, pergunta = aj.get("afirm", afirm), aj.get("expl", expl), aj.get("pergunta", pergunta)
    tags = " ".join(t for t in tags.split() if t != "#AdvogadaVitóriaES")
    texto = (f"{afirm.rstrip('.')}? {ver.capitalize()}.\n\n{expl}\n\n"
             f"💬 {pergunta}\n📤 Salve e {manda}.\n\n📚 Base legal: {base}.\n\n"
             "Cada caso tem detalhes. Procure uma advogada de confiança.\n\n"
             "Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre os seus direitos.\n\n"
             f"Letícia Barros · OAB/ES 39.948\n\n{tags}")
    return {"legenda": texto, "primeiro_comentario": f"💬 {pergunta}"}


def episodio(md, m):
    import json
    frase, big, rot, chip, perg = TELA[md]
    ver = 0 if m[3] == "MITO" else 1
    fs = tamanho(big)
    prt = 500 + int(fs * 1.05) + 30
    calt = prt + 90
    num = any(ch.isdigit() for ch in big) and "/" not in big and "a " not in big
    expl = AJUSTE.get(md, {}).get("expl", m[4])
    linhas = -(-len(expl) // 38)
    ext = (calt + 170) if chip else (prt + 80)
    chip_html = f"<div id=cal><b>{chip[0]}</b><span>{chip[1]}</span></div>" if chip else ""
    sons = list(SONS_FIXOS) + ([(14.6, "pagina"), (14.7, "bolha")] if chip else [])
    return {
        "nome": f"{md}-{m[1]}",
        "dur": 26.0,
        "salve": "",
        "css": CSS % {"fs": fs, "prt": prt, "calt": calt, "ext": ext, "blt": ext + 76 + 45 * linhas},
        "html": f"""<div id=tt><i>M</i><i>i</i><i>t</i><i>o</i>&nbsp;<i>o</i><i>u</i>&nbsp;<i class=ouro>L</i><i class=ouro>e</i><i class=ouro>i</i><i class=q>?</i></div>
<div class=card id=af><div class=t><b>Ouvi por aí</b><span>{"MITO OU LEI"}</span></div><div class=m><span id=tx></span><span id=cur></span></div></div>
<div id=op><div id=om>MITO</div><div id=ol>LEI</div></div><canvas id=rol width=1080 height=620></canvas>
<div id=onda></div><div id=tinta>{"".join(f"<i style=width:{14+(k*7)%22}px;height:{14+(k*7)%22}px></i>" for k in range(14))}</div><div id=ca class={m[3].lower()}>{m[3]}</div>
<div class="big ouro" id=pc data-m=1>{big}</div>
<div class=rot id=pr>{rot}</div>{chip_html}<div class=card id=ex><div class=m>{expl}</div></div><div class=rot id=bl>📚 {m[5]}</div>
<div class=rot id=dz>⏱ Responda antes da roleta parar</div><div id=segue><div class=av>LB</div><div class=nm>Dra. Letícia Barros<small>@adv.leticiabarros2</small></div><div class=bt><span id=btx>Seguir</span><i class=rp id=rp></i></div></div><div id=mao>👆</div><div class=marca id=q><span>{perg}</span></div><div class=sub id=s>Comente aqui embaixo.</div>""",
        "js": JS % {"fr": json.dumps(frase, ensure_ascii=False), "ver": ver,
                    "big": json.dumps(big, ensure_ascii=False), "num": "true" if num else "false"},
        "sons": sons,
        "legenda": legenda(m),
    }


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "amostras"
    datas = sys.argv[2:]
    raiz = AQUI / "mito-lei"
    raiz.mkdir(exist_ok=True)
    motor.VERSAO = "v3"  # carimbo novo (10/11/2026); v2 fica guardado
    sys.argv = [sys.argv[0], modo, "1,3.5,6,8,12.5,15.5,19"] if modo == "amostras" else [sys.argv[0], modo]
    for md, m in itens():
        if datas and md not in datas:
            continue
        print("==", md, m[1], flush=True)
        motor.rodar(episodio(md, m), str(raiz / "x.py"))
    if modo == "video":
        # Regra (10/11/2026, Jessica): todo Reels Mito ou Lei sai com a capa Moldura Viva junto.
        # A capa pronta nunca é sobrescrita; tema sem foto inédita em FOTOS (capas_mito_foto.py) é avisado.
        import subprocess
        subprocess.run([sys.executable, str(AQUI / "capas_mito_foto.py"), *datas], check=True)
