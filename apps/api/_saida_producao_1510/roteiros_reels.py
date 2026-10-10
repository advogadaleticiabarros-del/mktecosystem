"""Roteiros das séries de Reels para o NotebookLM (fonte + instrução), usados na página
"Roteiros dos Reels" (artefato https://claude.ai/artifact/Uxj3u5dK7TA2YQbQYFgjTe).

Cada série: 3 partes, cada uma com pergunta de abertura, falas e gancho para a próxima.
Fatos conferidos em 10/10/2026 (conteudo_nov.py e conteudo_dez.py).
"""

INSTRUCAO = """Siga o roteiro da fonte "{titulo}" na ordem exata: Parte 1, Parte 2 e Parte 3. Use as falas do roteiro quase literalmente; não acrescente informações, valores ou casos que não estejam no roteiro. As fontes oficiais servem só de apoio.
Público: trabalhadoras brasileiras e mães, assistindo no Instagram. Português do Brasil, tom caloroso, direto e sem juridiquês.
Cada parte deve começar com a pergunta de abertura do roteiro, dita de forma forte, e durar entre 40 e 50 segundos. Termine a Parte 1 e a Parte 2 com o gancho da próxima parte. Faça uma pausa curta entre as partes.
Diga as datas e os números por extenso, exatamente como no roteiro.
Nunca use as palavras "especialista", "ex" ou "deficiência" (diga "necessidades especiais"). Não ofereça serviços e não diga "fale comigo", "me chama" ou "conte seu caso".
Termine com a frase: "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança.\""""

FECHO = 'Encerramento: "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança."'


def fonte(titulo: str, partes: list[tuple[str, str, list[str], str]]) -> str:
    linhas = [f"ROTEIRO DA SÉRIE \"{titulo.upper()}\" (3 partes) · Direito brasileiro · fatos conferidos em outubro de 2026", ""]
    for i, (nome, abertura, falas, gancho) in enumerate(partes, 1):
        linhas += [f"PARTE {i}: {nome.upper()}", f"Pergunta de abertura: \"{abertura}\"", "Falas:"]
        linhas += [f"- {f}" for f in falas]
        linhas += [f"Gancho para a próxima parte: \"{gancho}\"" if gancho else FECHO, ""]
    return "\n".join(linhas).strip()


SERIES = [
    {
        "id": "s5", "titulo": "Dezembro Vermelho e trabalho digno", "datas": ["ter 01/12", "qui 03/12", "sáb 05/12"], "prazo": "24/11",
        "links": ["https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12984.htm"],
        "partes": [
            ("HIV no trabalho", "Quem vive com HIV precisa contar para a empresa? Não precisa.", [
                "Revelar que vive com HIV é uma escolha da pessoa. Ninguém é obrigado a contar para a empresa ou para os colegas.",
                "A empresa não pode exigir teste de HIV na admissão, nos exames periódicos ou na demissão (Portaria do Ministério do Trabalho 1.246 de 2010).",
                "Demitir alguém por viver com HIV é crime, com pena de um a quatro anos de reclusão (Lei 12.984 de 2014).",
                "A Justiça do Trabalho presume que essa demissão é discriminatória, e a pessoa pode voltar ao emprego (Súmula 443 do TST).",
                "Quem vive com HIV pode sacar o FGTS sem sair do emprego.",
            ], "Na parte 2: a escravidão acabou mesmo?"),
            ("Trabalho escravo hoje", "A escravidão foi abolida. Mas o trabalho escravo ainda existe.", [
                "O Código Penal chama de trabalho análogo à escravidão quatro situações: trabalho forçado, jornada exaustiva, condições degradantes e dívida que impede a pessoa de ir embora (artigo 149).",
                "Basta uma delas para ser crime. A pena é de dois a oito anos de reclusão.",
                "O trabalho doméstico é um dos setores com mais casos: sem folga, sem salário certo, morando no emprego.",
                "A empregada doméstica tem direito a salário mínimo, jornada de 44 horas por semana, folga semanal, férias e FGTS.",
                "A denúncia pode ser feita em sigilo, pelo Sistema Ipê, na internet, ou pelo Disque 100.",
            ], "Na parte 3: empresa grande é obrigada a ter cota de inclusão?"),
            ("Cota de inclusão", "Empresa com cem funcionários é obrigada a ter cota de inclusão? É.", [
                "A partir de cem empregados, a empresa precisa reservar vagas para pessoas com necessidades especiais ou reabilitadas pelo INSS (Lei 8.213 de 1991, artigo 93).",
                "A cota vai de dois por cento, nas empresas de cem a duzentos empregados, até cinco por cento, nas empresas com mais de mil.",
                "Para demitir alguém contratado pela cota, a empresa precisa contratar outra pessoa na mesma condição.",
            ], ""),
        ],
    },
    {
        "id": "s6", "titulo": "Saúde mental e assédio", "datas": ["ter 08/12", "qui 10/12", "sáb 12/12"], "prazo": "01/12",
        "links": [],
        "partes": [
            ("Burnout", "Burnout é doença do trabalho? É.", [
                "Desde 2023, a síndrome de burnout está na lista oficial de doenças relacionadas ao trabalho do Ministério da Saúde.",
                "Os primeiros quinze dias de afastamento são pagos pela empresa. Depois disso, quem paga é o INSS.",
                "A CAT, Comunicação de Acidente de Trabalho, liga a doença ao emprego. Se a empresa não emitir, o médico ou o sindicato podem emitir.",
                "Com a relação reconhecida, na volta ao trabalho a pessoa tem doze meses de estabilidade (Lei 8.213 de 1991, artigo 118).",
                "A prova vem do laudo médico, das mensagens de cobrança fora de hora e dos registros de jornada.",
            ], "Na parte 2: chefe que humilha comete assédio?"),
            ("Assédio moral", "Chefe que humilha na frente da equipe comete assédio moral? Pode cometer.", [
                "Assédio moral é expor a trabalhadora a situações humilhantes: gritos, xingamentos, isolamento, tirar as tarefas para constranger.",
                "A empresa responde pelos atos dos chefes e dos colegas.",
                "O assédio gera indenização e, nos casos graves, permite a rescisão indireta: a pessoa sai e recebe como se tivesse sido demitida sem justa causa.",
                "Para provar: anote cada episódio com data, guarde prints, áudios e e-mails, e anote o nome de quem viu.",
            ], "Na parte 3: e se acontecer algo na festa da firma?"),
            ("Festa da firma", "Festa da firma não é passe livre.", [
                "Tocar alguém com conotação sexual sem consentimento é importunação sexual, com pena de um a cinco anos de reclusão (Código Penal, artigo 215-A).",
                "Usar o cargo para constranger alguém com fins sexuais é assédio sexual (Código Penal, artigo 216-A).",
                "A empresa responde pelo que acontece nos eventos que ela promove, e as empresas com CIPA precisam ter canal de denúncia.",
                "Se acontecer: registre boletim de ocorrência, anote quem viu e use o canal de denúncia da empresa.",
            ], ""),
        ],
    },
    {
        "id": "s7", "titulo": "Fim de ano no trabalho", "datas": ["ter 15/12", "qui 17/12", "sáb 19/12"], "prazo": "08/12",
        "links": ["https://www.planalto.gov.br/ccivil_03/leis/l4749.htm", "https://www.planalto.gov.br/ccivil_03/leis/l6019.htm"],
        "partes": [
            ("2ª parcela do 13º", "Por que a segunda parcela do décimo terceiro vem menor?", [
                "Porque todos os descontos de INSS e de imposto de renda ficam na segunda parcela, calculados sobre o décimo terceiro inteiro.",
                "A conta é: décimo terceiro total, menos a primeira parcela, menos o INSS e o imposto de renda.",
                "O prazo é vinte de dezembro. Em 2026, o dia vinte cai num domingo, então o pagamento precisa sair até sexta-feira, dezoito de dezembro.",
                "Se a pensão alimentícia é um percentual do salário, ela também incide sobre o décimo terceiro.",
            ], "Na parte 2: quem foi contratada só para o fim de ano tem direitos?"),
            ("Temporária de fim de ano", "Contratada só para o fim de ano? Você tem direitos.", [
                "O trabalho temporário, contratado por agência, tem salário igual ao de quem faz a mesma função na empresa (Lei 6.019 de 1974).",
                "Tem jornada de oito horas, com hora extra paga, FGTS, décimo terceiro e férias proporcionais.",
                "O contrato pode durar até cento e oitenta dias, prorrogáveis por mais noventa.",
                "E desde março de 2026, o Tribunal Superior do Trabalho reconhece a estabilidade da gestante também no trabalho temporário.",
            ], "Na parte 3: férias coletivas, como funcionam?"),
            ("Férias coletivas", "A empresa deu férias coletivas? Veja as regras.", [
                "As férias coletivas podem ser em até dois períodos por ano, e nenhum pode ter menos de dez dias (CLT, artigo 139).",
                "A empresa precisa avisar o Ministério do Trabalho e o sindicato com quinze dias de antecedência.",
                "Quem tem menos de doze meses de casa tira férias proporcionais e começa a contar um novo período.",
                "O pagamento, com o terço de férias, sai até dois dias antes do início.",
            ], ""),
        ],
    },
    {
        "id": "s8", "titulo": "Natal e Ano Novo com direitos", "datas": ["ter 22/12", "qui 24/12", "sáb 26/12"], "prazo": "15/12",
        "links": [],
        "partes": [
            ("Feriado trabalhado", "Vai trabalhar no Natal ou no Ano Novo? Recebe em dobro.", [
                "Vinte e cinco de dezembro e primeiro de janeiro são feriados nacionais.",
                "Quem trabalha no feriado recebe o dia em dobro, além do repouso, a não ser que a empresa dê outro dia de folga.",
                "Vinte e quatro e trinta e um de dezembro não são feriados nacionais.",
                "Na escala doze por trinta e seis, a lei considera que os feriados já estão compensados no salário.",
            ], "Na parte 2: precisa de autorização para viajar com os filhos?"),
            ("Viagem com os filhos", "Pais separados precisam de autorização para viajar com os filhos?", [
                "Dentro do Brasil, criança ou adolescente com até dezesseis anos viajando com o pai ou com a mãe não precisa de autorização do outro.",
                "Sem os pais, precisa de autorização dos pais ou do juiz.",
                "Para o exterior com só um dos pais, o outro precisa autorizar por escrito, com firma reconhecida, ou o juiz autoriza.",
                "E a viagem precisa respeitar as datas de convivência combinadas.",
            ], "Na parte 3: a pensão aumenta em janeiro?"),
            ("Pensão em janeiro", "A pensão do seu filho aumenta em janeiro?", [
                "Se a pensão foi fixada em percentual do salário mínimo, ela sobe sozinha junto com o novo salário mínimo, sem processo.",
                "Se é um percentual do salário de quem paga, acompanha esse salário, inclusive no décimo terceiro.",
                "Se é um valor fixo, só muda pelo índice previsto no acordo ou com pedido de revisão.",
                "Se continuarem pagando o valor antigo, a diferença pode ser cobrada na Justiça.",
            ], ""),
        ],
    },
]

for _s in SERIES:
    _s["fonte"] = fonte(_s["titulo"], _s["partes"])
    _s["instrucao"] = INSTRUCAO.format(titulo="ROTEIRO DA SÉRIE " + _s["titulo"].upper())
