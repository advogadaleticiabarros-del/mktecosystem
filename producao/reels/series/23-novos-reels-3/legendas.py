"""Legenda e primeiro comentário da série 23 (16/11/2026). Voz real da Dra. Letícia (sem aviso de IA). Sem travessão,
sem oferta de serviço, sem caso concreto do escritório, 5 hashtags. Fatos e cortes no docstring de falas.py.
Horário: Reels gravado pela Dra. vai no domingo às 15h30 (grade de 10/11/2026): R1 em 22/11, R2 em 29/11."""

ASSINATURA = """Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança.

Dra. Letícia Barros · Direito Trabalhista · Vitória/ES · OAB/ES 39.948
Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.
Atualizado em novembro de 2026."""

LEGENDAS = {
    1: {"titulo": "Reels da Dra.: intermitente, o 13º já vem na diária (1/2)",
        "quando": "2026-11-22 15:30",
        "legenda": f"""Chegou dezembro e o 13º não veio? Se o seu contrato é intermitente, ele já veio, aos poucos.

O intermitente é o antigo bico com nome e carteira assinada: a empresa te convoca com 3 dias de antecedência, você tem 1 dia útil para responder e pode recusar. Se recusar, não recebe aquele dia.

No fim de cada período trabalhado você recebe o valor das horas e, junto, o 13º e as férias com 1/3, tudo proporcional. Por isso não chega um 13º inteiro em dezembro.

❓ As perguntas que mais chegam aqui:
📌 E o FGTS, vem na diária? Não. O FGTS é depositado pela empresa na sua conta, à parte.
📌 Então não tenho férias? Tem. O valor vem a cada período e, depois de 12 meses, você tem 1 mês sem ser convocado pela mesma empresa.
📌 E se eu trabalho todo dia? Isso é a parte 2.

📚 Base: CLT, art. 452-A, §§ 1º, 2º, 6º, 8º e 9º.

🔖 Salva e manda para quem trabalha por diária.

{ASSINATURA}

#DireitoTrabalhista #ContratoIntermitente #13Salario #DireitosDoTrabalhador #AdvogadaVitóriaES""",
        "pc": """📚 Base: CLT, art. 452-A (convocação, recusa, pagamento do 13º e das férias + 1/3 a cada período, FGTS depositado).
💬 Você já trabalhou por diária sem saber que era contrato intermitente?"""},
    2: {"titulo": "Reels da Dra.: intermitente de fachada (2/2)",
        "quando": "2026-11-29 15:30",
        "legenda": f"""Trabalhou todos os dias, por anos, e no fim do ano não tinha 13º nem férias? Pode ser um intermitente só no papel.

O intermitente é previsto na CLT desde a Reforma de 2017, e muitos juízes entendem que ele é válido. Mas o contrato foi feito para quem trabalha alternando períodos, quando é convocado.

Quando a pessoa vai todos os dias, recebe ordens, não pode recusar e tem como provar isso (com testemunhas, por exemplo), esse contrato pode ser questionado na Justiça. Se for reconhecido um contrato comum, o valor que você recebia vira o seu salário, e o 13º, as férias e o FGTS são calculados à parte.

❓ As perguntas que mais chegam aqui:
📌 O intermitente é ilegal? Não. Ele está na lei. O problema é usar o nome sem a realidade.
📌 Que prova eu preciso? Rotina de todos os dias, ordens, impossibilidade de recusar. Testemunhas ajudam.
📌 O que é o intermitente? Isso está na parte 1.

📚 Base: CLT, arts. 9º, 443, § 3º, e 452-A.

🔖 Salva e manda para quem trabalha todo dia.

{ASSINATURA}

#DireitoTrabalhista #ContratoIntermitente #CLT #DireitosDoTrabalhador #AdvogadaVitóriaES""",
        "pc": """📚 Base: CLT, art. 443, § 3º (definição do intermitente, Lei 13.467/2017) e art. 9º (nulidade do que desvirtua a CLT).
💬 Você conhece alguém que é intermitente só no papel?"""},
}

# Versões B (17/11/2026, pedido da Jessica: "o vídeo 1 é o que é o trabalho intermitente, o 2 é estudo de caso").
# A Dra. escolhe uma versão de cada vídeo; a data é a mesma da versão A que ela substitui.
PERGUNTAS_1 = """❓ As perguntas que mais chegam aqui:
📌 E o FGTS, vem na diária? Não. O FGTS é depositado pela empresa na sua conta, à parte.
📌 Então não tenho férias? Tem. O valor vem a cada período e, depois de 12 meses, você tem 1 mês sem ser convocado pela mesma empresa."""

LEGENDAS[3] = {"titulo": "Reels da Dra.: o que é o contrato intermitente (1/2, versão B)",
               "quando": "2026-11-22 15:30",
               "legenda": f"""O que é o contrato intermitente? É o antigo bico, agora com nome e carteira assinada.

A empresa te convoca com 3 dias de antecedência e você tem 1 dia útil para responder. Pode recusar, mas aquele dia não é pago.

E por que o 13º não chega inteiro em dezembro? Porque, no fim de cada período trabalhado, você já recebe junto com as horas o 13º e as férias com 1/3, tudo proporcional.

{PERGUNTAS_1}
📌 E se eu trabalho todo dia? Isso é a parte 2.

📚 Base: CLT, art. 452-A, §§ 1º, 2º, 6º, 8º e 9º.

🔖 Salva e manda para quem trabalha por diária.

{ASSINATURA}

#DireitoTrabalhista #ContratoIntermitente #CLT #DireitosDoTrabalhador #AdvogadaVitóriaES""",
               "pc": """📚 Base: CLT, art. 452-A (convocação com 3 dias, resposta em 1 dia útil, 13º e férias + 1/3 a cada período, FGTS depositado).
💬 Você já assinou um contrato intermitente sem saber o que era?"""}

LEGENDAS[4] = {"titulo": "Reels da Dra.: estudo de caso, o intermitente de todo dia (2/2, versão B)",
               "quando": "2026-11-29 15:30",
               "legenda": f"""📂 Estudo de caso (situação hipotética)

Um trabalhador assinou contrato intermitente sem saber o que era. Na prática, ia trabalhar todos os dias, por 3 ou 4 anos, recebia ordens e, no fim de cada ano, não tinha 13º nem férias.

O intermitente é legal: está na CLT desde a Reforma de 2017, e muitos juízes validam esse contrato. Mas há julgados que o questionam quando não existe alternância real entre trabalho e inatividade.

Com provas da rotina e testemunhas, o caso pode ser levado ao Judiciário. Se for reconhecido um contrato comum, o valor da diária vira salário, e o 13º, as férias com 1/3 e o FGTS são calculados à parte.

❓ As perguntas que mais chegam aqui:
📌 O intermitente é ilegal? Não. Ele está na lei. O problema é usar o nome sem a realidade.
📌 Que prova eu preciso? Rotina de todos os dias, ordens, impossibilidade de recusar. Testemunhas ajudam.
📌 O que é o intermitente? Isso está na parte 1.

📚 Base: CLT, arts. 9º, 443, § 3º, e 452-A.

🔖 Salva e manda para quem trabalha todo dia.

{ASSINATURA}

#DireitoTrabalhista #ContratoIntermitente #CLT #DireitosDoTrabalhador #AdvogadaVitóriaES""",
               "pc": """📚 Base: CLT, art. 443, § 3º (definição do intermitente, Lei 13.467/2017) e art. 9º (nulidade do que desvirtua a CLT).
💬 Você conhece alguém que vive essa situação?"""}
