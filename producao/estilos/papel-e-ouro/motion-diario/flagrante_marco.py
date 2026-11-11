"""Flagrantes de março de 2027 (episódios 35 a 40), pedido da Jessica em 11/11/2026 ("Faça todos!"). Mesma mecânica do
episódio 01 (conversa que chega, pausa, pergunta em marca-texto e fechamento fixo). Textos novos: conferência
jurídica da Dra. pendente.

Uso: python flagrante_marco.py amostras|video [35 36 ...]   → NN-assunto/NN-assunto-v2.mp4 + legenda.json"""
import sys

from motor import rodar

FIM = ("\n\nQuer ficar por dentro dos seus direitos? Clique em seguir e compartilhe com quem precisa saber disso."
       "\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\n"
       "Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre os seus direitos.\n\n")

CSS = """#topo{top:282px}
#topo i{display:inline-block;width:14px;height:14px;border-radius:50%;background:#7BB37A;margin-right:10px;vertical-align:2px}
.doc{width:330px;background:#EFE6D9;color:#1E1814;border-radius:14px;padding:18px 20px;margin-bottom:10px}
.doc b{display:block;font:600 22px Inter;letter-spacing:.08em}
.doc p{font:400 24px/1.4 Inter;margin-top:8px}
#b0{top:350px}#b1{top:640px}#b2,#p1{top:800px}#b3,#p2{top:940px}
#q{top:1100px}#s{top:1212px}"""

JS = """const pts=(id,a,b,t)=>{const e=$(id);e.style.opacity=t<a||t>b?0:cl((t-a)/.15);
 e.querySelectorAll('span').forEach((s,i)=>{s.style.opacity=.25+.5*Math.max(0,Math.sin((t-a)*7-i*.9))})};
function cena(t){
 sobe('topo',t,.1);nasce('b0',t,.5);nasce('b1',t,2.0);
 pts('p1',3.6,5.4,t);nasce('b2',t,5.4);pts('p2',6.9,8.2,t);nasce('b3',t,8.2);
 const dim=1-.6*ioo((t-10.2)/.6);['b0','b1','b2'].forEach(i=>$(i).style.filter=`brightness(${dim})`);
 $('b3').style.filter=`brightness(${1-.25*ioo((t-10.2)/.6)})`;
 marca('q',t,10.6);sobe('s',t,12.4);
 $('cena').style.transform=`translateX(${treme(t,[5.4,8.2])}px)`;
}"""

SONS = [(.5, "bolha"), (.55, "vibra", .5), (2.0, "bolha"), (3.6, "digita"), (5.4, "pop"), (5.4, "vibra"),
        (6.9, "digita", .8), (8.2, "pop"), (8.2, "vibra"), (8.25, "erro", .8), (10.55, "whoosh"),
        (10.7, "escreve"), (11.2, "brilho", .7), (15.9, "whoosh", .6), (16.3, "carimbo", .7)]


def ep(nome, contato, doc, b0, b1, b2, b3, horas, pergunta, sub, legenda, tags, comentario):
    h = horas
    html = f"""<div class=rot id=topo><i></i>{contato}</div>
<div class="bo eu" id=b0 data-m=1>{f'<div class=doc>{doc}</div>' if doc else ''}{b0}<small>{h[0]}</small></div>
<div class="bo eu" id=b1>{b1}<small>{h[1]}</small></div>
<div class="bo ele pts" id=p1 data-m=1><span></span><span></span><span></span></div>
<div class="bo ele" id=b2>{b2}<small>{h[2]}</small></div>
<div class="bo ele pts" id=p2 data-m=1><span></span><span></span><span></span></div>
<div class="bo ele" id=b3>{b3}<small>{h[3]}</small></div>
<div class=marca id=q><span>{pergunta}</span></div>
<div class=sub id=s>{sub}</div>"""
    return {"nome": nome, "dur": 20.0, "salve": "", "css": CSS, "html": html, "js": JS, "sons": SONS,
            "legenda": {"primeiro_comentario": comentario, "legenda": legenda + FIM + tags}}


EPISODIOS = {
    "35": ep("35-salario-igual", "Colega do setor", "",
             "Descobri que o Rafael ganha R$ 800 a mais.", "Mesma função, mesmo horário.",
             "É que ele é homem, né. Sempre foi assim.", "Melhor nem falar nada no RH.",
             ("12:03", "12:03", "12:10", "12:11"), "Pode isso?", "Comente: pode ou não pode?",
             "12h03. \"Descobri que o Rafael ganha R$ 800 a mais.\"\n12h10. \"É que ele é homem.\"\n\nPode isso?\n\nNão. Mesma função e mesmo valor de trabalho exigem o mesmo salário, sem diferença por sexo, raça ou idade. Desde 2023, a empresa que discrimina paga multa e indenização.\n\nO que vale saber:\n📌 Compare função, tarefas e tempo na função, não só o cargo no papel\n📌 Empresas com 100 ou mais empregados publicam relatório de transparência salarial\n📌 Guarde holerites e qualquer prova da diferença\n\nComente: pode ou não pode? E mande para uma mulher que trabalha.",
             "#IgualdadeSalarial #DiaDaMulher #DireitoTrabalhista #DireitosDaMulher #AdvogadaTrabalhista",
             "📚 Base legal: CLT, art. 461; Lei 14.611/2023.\n💬 Você já descobriu que ganhava menos?"),
    "36": ep("36-cobranca-dobro", "Banco", "<b>FATURA DO CARTÃO</b><p>Seguro Proteção · R$ 29,90</p>",
             "Nunca contratei esse seguro.", "Já paguei 6 meses sem perceber.",
             "Vamos cancelar a partir de agora.", "Os valores já pagos não são devolvidos.",
             ("09:15", "09:16", "09:40", "09:41"), "Devolve ou não?", "Comente: quanto você acha que volta?",
             "09h15. Um seguro que você nunca contratou na fatura.\n09h41. \"Os valores já pagos não são devolvidos.\"\n\nDevolve ou não?\n\nDevolve, e em dobro. Quem pagou cobrança indevida tem direito a receber o dobro do que pagou, com correção, salvo engano justificável de quem cobrou.\n\nO que vale saber:\n📌 Peça o cancelamento e a devolução por escrito, com protocolo\n📌 Reclame no Consumidor.gov.br e no Procon\n📌 Guarde as faturas com a cobrança\n\nComente: já te cobraram algo que você não contratou? E mande para quem precisa conferir a fatura.",
             "#DiaDoConsumidor #CobrançaIndevida #DireitoDoConsumidor #Consumidor #AdvogadaVitóriaES",
             "📚 Base legal: Código de Defesa do Consumidor, art. 42, parágrafo único.\n💬 Você confere a fatura todo mês?"),
    "37": ep("37-exame-admissional", "RH · Vaga de recepcionista", "",
             "Fui aprovada! Quando começo?", "Já estou com os documentos.",
             "Parabéns! Antes, faça o exame admissional.", "É por sua conta: R$ 120. Traga o recibo.",
             ("10:02", "10:02", "10:20", "10:21"), "Quem paga?", "Comente: você ou a empresa?",
             "10h20. \"Faça o exame admissional.\"\n10h21. \"É por sua conta: R$ 120.\"\n\nQuem paga?\n\nA empresa. Os exames médicos de admissão, periódicos e de demissão são obrigação e custo do empregador.\n\nO que vale saber:\n📌 Cobrar o exame da candidata transfere para você um custo que é da empresa\n📌 Guarde a mensagem e o recibo, se pagou\n📌 O exame não pode incluir teste de gravidez\n\nComente: você ou a empresa? E mande para quem está começando em emprego novo.",
             "#ExameAdmissional #EmpregoNovo #DireitoTrabalhista #CLT #AdvogadaTrabalhista",
             "📚 Base legal: CLT, art. 168; Lei 9.029/1995.\n💬 Já te cobraram exame admissional?"),
    "38": ep("38-pensao-ir", "Contadora", "<b>DECLARAÇÃO IR 2027</b><p>Rendimentos · pensão do filho</p>",
             "A pensão do meu filho entra na declaração?", "Recebo R$ 900 por mês.",
             "Entra como rendimento tributável.", "Vai dar imposto a pagar.",
             ("18:30", "18:31", "18:52", "18:53"), "Paga imposto?", "Comente: paga ou não paga?",
             "18h52. \"A pensão entra como rendimento tributável.\"\n18h53. \"Vai dar imposto a pagar.\"\n\nPaga imposto?\n\nNão. O STF decidiu que a pensão alimentícia não é renda nova de quem recebe e, por isso, não sofre imposto de renda. Ela é informada como rendimento isento.\n\nO que vale saber:\n📌 Quem paga a pensão por decisão judicial ou escritura pode deduzir\n📌 Declare como rendimento isento e não tributável\n📌 Pagou imposto sobre pensão em anos anteriores? Pode ser possível pedir de volta\n\nComente: paga ou não paga? E mande para uma mãe que recebe pensão.",
             "#ImpostoDeRenda #PensãoAlimentícia #DireitoDeFamília #MãeSolo #AdvogadaDeFamília",
             "📚 Base legal: STF, ADI 5.422.\n💬 Você já declarou a pensão como renda?"),
    "39": ep("39-gravida-aviso", "RH", "<b>AVISO PRÉVIO</b><p>Último dia: 15/04</p>",
             "Recebi o aviso ontem.", "Hoje o exame deu positivo. 🤰🏾",
             "Seu aviso já foi dado.", "Não muda nada, você sai no dia 15.",
             ("08:05", "08:05", "08:30", "08:31"), "E agora?", "Comente: sai ou fica?",
             "08h05. \"Hoje o exame deu positivo.\"\n08h31. \"Não muda nada, você sai no dia 15.\"\n\nE agora?\n\nMuda, sim. A gravidez confirmada durante o aviso prévio, trabalhado ou indenizado, garante a estabilidade da gestante.\n\nO que vale saber:\n📌 A estabilidade vai da confirmação da gravidez até 5 meses depois do parto\n📌 Avise a empresa por escrito e guarde o exame com a data\n📌 Se a empresa mantiver a dispensa, busque orientação\n\nComente: sai ou fica? E mande para uma mulher que está de aviso.",
             "#Gestante #AvisoPrévio #EstabilidadeDaGestante #DireitoTrabalhista #GestanteCLT",
             "📚 Base legal: CLT, art. 391-A; ADCT, art. 10, II, b.\n💬 Você conhece alguém que descobriu a gravidez no aviso?"),
    "40": ep("40-interjornada", "Supervisor", "",
             "Fechei a loja agora. 23h.", "Chegando em casa.",
             "Amanhã abre às 6h.", "Preciso de você lá às 5h45.",
             ("23:04", "23:05", "23:12", "23:12"), "Pode isso?", "Comente: dá tempo de descansar?",
             "23h04. \"Fechei a loja agora.\"\n23h12. \"Preciso de você lá às 5h45.\"\n\nPode isso?\n\nNão. Entre o fim de um dia de trabalho e o começo do outro, a lei garante pelo menos 11 horas seguidas de descanso.\n\nO que vale saber:\n📌 Saiu às 23h, só pode voltar às 10h\n📌 As horas que faltaram para as 11 podem ser pagas como extras\n📌 Anote seus horários e guarde as mensagens\n\nComente: dá tempo de descansar? E mande para quem fecha e abre a loja.",
             "#Jornada #Descanso #DireitoTrabalhista #Comércio #AdvogadaTrabalhista",
             "📚 Base legal: CLT, art. 66; Súmula 110 do TST; OJ 355 da SDI-1 do TST.\n💬 Você já fechou e abriu no dia seguinte?"),
}

if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "amostras"
    so = sys.argv[2:]
    sys.argv = [sys.argv[0], modo]
    for k, e in EPISODIOS.items():
        if so and k not in so:
            continue
        print("==", e["nome"], flush=True)
        rodar(e, __file__)
