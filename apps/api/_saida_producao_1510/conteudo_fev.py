"""Mito ou Lei de fevereiro de 2027 (Reels Flagrante com roleta, seg/qua/sáb 19h). Pedido da Jessica em 11/11/2026:
"pode fazer até o máximo que der, até fevereiro ou março". Temas do mês: volta às aulas, Carnaval, gestante e pais,
rescisão e salário. Textos novos, escritos na voz da Dra.: PRECISAM da conferência jurídica dela antes de 01/02.
Mesmo formato de conteudo_nov.MITO_OU_LEI: (data, chave, afirmação, veredito, explicação, base, hashtags, -, -, manda, pergunta).
"""

TEMAS = []

MITO_OU_LEI = [
    ("2027-02-01", "material-escolar", "A escola pode pedir papel higiênico na lista de material.", "MITO",
     "Material de uso coletivo, como papel higiênico e produtos de limpeza, não pode entrar na lista. O custo já está na mensalidade.",
     "Lei 12.886/2013",
     "#MitoOuLei #VoltaÀsAulas #MaterialEscolar #DireitoDoConsumidor #AdvogadaVitóriaES", False, True,
     "manda pra quem está montando a lista agora", "Já pediram algo assim na escola do seu filho?"),
    ("2027-02-03", "mensalidade-prova", "Com a mensalidade atrasada, a escola pode impedir a criança de fazer prova.", "MITO",
     "A escola pode cobrar a dívida, mas não pode suspender provas, segurar documentos nem aplicar castigo por atraso.",
     "Lei 9.870/1999, art. 6º",
     "#MitoOuLei #Escola #Mensalidade #DireitoDoConsumidor #AdvogadaVitóriaES", False, True,
     "manda pra uma mãe que está com a mensalidade apertada", "Você sabia que isso é proibido?"),
    ("2027-02-06", "teste-gravidez", "A empresa pode exigir teste de gravidez na contratação.", "MITO",
     "Exigir teste ou atestado de gravidez para contratar ou manter alguém no emprego é crime e é discriminação.",
     "Lei 9.029/1995, art. 2º; CLT, art. 373-A, IV",
     "#MitoOuLei #Gestante #Discriminação #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem está em processo seletivo", "Já te pediram esse exame numa entrevista?"),
    ("2027-02-08", "carnaval-feriado", "Carnaval é feriado nacional.", "MITO",
     "Nenhuma lei federal faz do Carnaval um feriado. Só é folga se houver lei local, acordo coletivo ou costume da empresa.",
     "Lei 9.093/1995; Lei 662/1949",
     "#MitoOuLei #Carnaval #Feriado #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem vai trabalhar no Carnaval", "Na sua cidade, Carnaval é feriado?"),
    ("2027-02-10", "pai-pre-natal", "O pai pode faltar para acompanhar as consultas do pré-natal.", "LEI",
     "A CLT garante até 2 dias, sem desconto, para acompanhar consultas e exames da esposa ou companheira grávida.",
     "CLT, art. 473, X",
     "#MitoOuLei #PaternidadeAtiva #PréNatal #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pro futuro papai", "O pai do seu filho foi às consultas?"),
    ("2027-02-13", "filho-medico", "Você pode faltar 1 dia por ano para levar o filho ao médico.", "LEI",
     "A CLT garante 1 dia por ano, sem desconto, para acompanhar filho de até 6 anos em consulta médica.",
     "CLT, art. 473, XI",
     "#MitoOuLei #Maternidade #FilhoPequeno #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra uma mãe que trabalha", "Você já usou esse dia?"),
    ("2027-02-15", "demissao-fgts", "Quem pede demissão saca o FGTS.", "MITO",
     "No pedido de demissão, o FGTS fica na conta. Ele pode ser sacado depois em outras situações, como compra da casa própria ou aposentadoria.",
     "Lei 8.036/1990, art. 20",
     "#MitoOuLei #FGTS #PedidoDeDemissão #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem está pensando em pedir as contas", "Você achava que dava para sacar?"),
    ("2027-02-17", "aviso-previo-90", "O aviso prévio é sempre de 30 dias.", "MITO",
     "Na dispensa sem justa causa, são 30 dias mais 3 por ano completo na empresa, até o limite de 90 dias.",
     "Lei 12.506/2011",
     "#MitoOuLei #AvisoPrévio #Rescisão #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem trabalha há anos na mesma empresa", "Quantos anos você tem de casa?"),
    ("2027-02-20", "hora-extra-reflexo", "Hora extra frequente aumenta o 13º e as férias.", "LEI",
     "Hora extra feita com frequência entra na média do 13º e das férias. Confira no holerite dessas parcelas.",
     "Súmula 45 do TST; CLT, art. 142, § 5º",
     "#MitoOuLei #HoraExtra #13Salário #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem faz hora extra todo mês", "Você confere a média no seu 13º?"),
    ("2027-02-22", "uniforme-desconto", "A empresa pode descontar o uniforme do salário.", "MITO",
     "Se o uniforme é exigido pela empresa, o custo é dela. O salário só tem os descontos que a lei permite.",
     "CLT, arts. 2º e 462",
     "#MitoOuLei #Uniforme #DescontoNoSalário #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem pagou o próprio uniforme", "Já descontaram uniforme de você?"),
    ("2027-02-24", "vale-transporte-6", "O desconto do vale-transporte pode chegar a 6% do salário.", "LEI",
     "A empresa pode descontar até 6% do salário básico. O que passar disso no custo da passagem é por conta dela.",
     "Lei 7.418/1985, art. 4º, parágrafo único",
     "#MitoOuLei #ValeTransporte #Holerite #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem pega ônibus para trabalhar", "Quanto descontam do seu?"),
    ("2027-02-27", "domestica-fgts", "Empregada doméstica tem FGTS obrigatório.", "LEI",
     "Desde 2015, o FGTS da doméstica é obrigatório, junto com a indenização compensatória recolhida todo mês pelo eSocial.",
     "Lei Complementar 150/2015, arts. 21 e 22",
     "#MitoOuLei #TrabalhoDoméstico #FGTS #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem trabalha em casa de família", "Seu FGTS está sendo depositado?"),
]

# Frases avulsas de fevereiro (papel claro, 12h), temas que ainda não saíram no feed. Textos novos de 11/11/2026:
# conferência jurídica da Dra. pendente. Campos: data, chave, área, frase (html com <em> no fecho), legenda, comentário.
_FIM = ("\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\n"
        "Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre os seus direitos.\n\n"
        "Letícia Barros · OAB/ES 39.948\n\n")


def _f(data, chave, area, html, legenda, base, pergunta, tags):
    return {"data": data, "chave": chave, "area": area, "frase": {"html": html},
            "legenda": legenda + _FIM + tags, "primeiro_comentario": f"📚 Base: {base}.\n💬 {pergunta}"}


FRASES_EXTRA = [
    _f("2027-02-02", "bebe-internado", "Trabalhista",
       "Bebê na UTI depois do parto? <em>A licença começa na alta.</em>",
       "Bebê na UTI depois do parto? A licença começa na alta.\n\nQuando a mãe ou o bebê fica internado por muito tempo depois "
       "do parto, os 120 dias da licença-maternidade passam a contar da alta hospitalar. O tempo de internação não "
       "come a licença.\n\n📌 Vale para a licença e para o salário-maternidade\n📌 Guarde o relatório da internação e o "
       "documento da alta\n\nSalve e mande para uma mãe que está no hospital agora.",
       "STF, ADI 6.327", "Você conhece alguém que passou por isso?",
       "#LicençaMaternidade #UTINeonatal #Prematuro #DireitoTrabalhista #DireitosDaMulher"),
    _f("2027-02-04", "pensao-18", "Família",
       "Pensão não acaba sozinha aos 18. <em>Precisa de decisão do juiz.</em>",
       "Pensão não acaba sozinha aos 18. Precisa de decisão do juiz.\n\nO filho fez 18 anos e o pai parou de pagar? Não "
       "pode. A pensão só termina com decisão judicial, e o filho tem a chance de mostrar que ainda precisa, por exemplo "
       "porque está estudando.\n\n📌 Parar de pagar por conta própria gera dívida\n📌 Faculdade e curso técnico costumam "
       "manter a pensão até cerca de 24 anos\n\nSalve e mande para quem está nessa fase.",
       "STJ, Súmula 358", "O seu filho está perto dos 18?",
       "#PensãoAlimentícia #DireitoDeFamília #Maioridade #MãeSolo #AdvogadaDeFamília"),
    _f("2027-02-05", "luto-2-dias", "Trabalhista",
       "Perdeu alguém da família? <em>São 2 dias sem desconto.</em>",
       "Perdeu alguém da família? São 2 dias sem desconto.\n\nA CLT garante até 2 dias seguidos de falta no falecimento do "
       "cônjuge, pais, filhos, irmãos ou de quem vive sob sua dependência econômica.\n\n📌 Leve a certidão de óbito\n"
       "📌 Convenção coletiva pode dar mais dias\n\nNinguém deveria ter que escolher entre o luto e o salário.",
       "CLT, art. 473, I", "Na sua empresa respeitam esses dias?",
       "#Luto #DireitoTrabalhista #CLT #DireitosDoTrabalhador #AdvogadaTrabalhista"),
    _f("2027-02-07", "casamento-3-dias", "Trabalhista",
       "Vai casar? <em>São 3 dias de folga sem desconto.</em>",
       "Vai casar? São 3 dias de folga sem desconto.\n\nA CLT garante até 3 dias seguidos de falta pelo casamento, sem "
       "desconto no salário.\n\n📌 Avise a empresa com antecedência e leve a certidão\n📌 Convenção coletiva pode dar mais"
       "\n\nSalve e mande para quem vai subir ao altar este ano.",
       "CLT, art. 473, II", "Você usou os seus 3 dias?",
       "#Casamento #DireitoTrabalhista #CLT #Noivas #AdvogadaTrabalhista"),
    _f("2027-02-11", "gestante-consultas", "Trabalhista",
       "Grávida pode sair para o pré-natal. <em>No mínimo 6 consultas, sem desconto.</em>",
       "Grávida pode sair para o pré-natal. No mínimo 6 consultas, sem desconto.\n\nA gestante tem direito a se ausentar "
       "pelo tempo necessário para, no mínimo, 6 consultas médicas e exames, sem perder salário.\n\n📌 Leve a declaração "
       "de comparecimento\n📌 E se o trabalho fizer mal à gestação, ela pode mudar de função e voltar à antiga depois"
       "\n\nSalve e mande para uma gestante.",
       "CLT, art. 392, § 4º", "Você teve dificuldade para sair para as consultas?",
       "#Gestante #PréNatal #DireitoTrabalhista #GestanteCLT #DireitosDaMulher"),
    _f("2027-02-14", "doenca-ocupacional", "Trabalhista",
       "Adoeceu por causa do trabalho? <em>Pode ter 12 meses de estabilidade.</em>",
       "Adoeceu por causa do trabalho? Pode ter 12 meses de estabilidade.\n\nQuem fica afastado pelo INSS por acidente ou "
       "doença ligada ao trabalho tem estabilidade de 12 meses depois que volta.\n\n📌 O benefício precisa ser o "
       "acidentário (código B91)\n📌 Se o INSS deu o comum, isso pode ser discutido\n📌 Guarde atestados, exames e a "
       "CAT\n\nSalve e mande para quem está afastado.",
       "Lei 8.213/1991, art. 118", "Você já precisou se afastar pelo trabalho?",
       "#DoençaOcupacional #INSS #Estabilidade #DireitoTrabalhista #AdvogadaTrabalhista"),
    _f("2027-02-18", "seguro-desemprego", "Trabalhista",
       "Pediu demissão? <em>O seguro-desemprego não vem.</em>",
       "Pediu demissão? O seguro-desemprego não vem.\n\nO seguro-desemprego é para quem foi dispensado sem justa causa. "
       "Antes de pedir as contas, vale saber o que você deixa de receber.\n\n📌 Também ficam de fora a multa de 40% e o "
       "saque do FGTS\n📌 Se a empresa está descumprindo a lei, pode existir outro caminho, a rescisão indireta\n\nSalve "
       "antes de tomar a decisão.",
       "Lei 7.998/1990, art. 3º", "Você está pensando em pedir demissão?",
       "#SeguroDesemprego #PedidoDeDemissão #DireitoTrabalhista #FGTS #AdvogadaTrabalhista"),
    _f("2027-02-21", "domestica-hora-extra", "Trabalhista",
       "Trabalha em casa de família? <em>Hora extra também é paga.</em>",
       "Trabalha em casa de família? Hora extra também é paga.\n\nA jornada da doméstica é de até 8 horas por dia e 44 por "
       "semana. O que passa disso é hora extra, com adicional de pelo menos 50%.\n\n📌 Controle de horário é obrigatório\n"
       "📌 Anote seus horários e guarde mensagens\n\nSalve e mande para quem trabalha em casa de família.",
       "Lei Complementar 150/2015, art. 2º", "Você faz mais horas do que combinou?",
       "#TrabalhoDoméstico #HoraExtra #DireitoTrabalhista #Doméstica #AdvogadaTrabalhista"),
    _f("2027-02-25", "gestante-troca-funcao", "Trabalhista",
       "O trabalho faz mal à gravidez? <em>Ela pode mudar de função.</em>",
       "O trabalho faz mal à gravidez? Ela pode mudar de função.\n\nQuando a saúde exige, a gestante pode ser transferida "
       "de função, com atestado, e volta à função antiga depois da licença.\n\n📌 O salário não diminui\n📌 Peça por escrito "
       "e guarde o atestado\n\nSalve e mande para uma gestante.",
       "CLT, art. 392, § 4º, I", "Você precisou mudar de função na gravidez?",
       "#Gestante #GestanteCLT #DireitoTrabalhista #Gravidez #DireitosDaMulher"),
]
