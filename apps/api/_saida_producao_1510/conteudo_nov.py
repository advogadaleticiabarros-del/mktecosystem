"""Conteúdo do plano 03/11 a 02/12/2026 (docs/PLANO_CONTEUDO_NOV_2026.md), aprovado pela Letícia em 09/10/2026.

Mesmo padrão de outubro: pergunta v6 (12h), frase v2 (15h), carrossel v5 com capa Ouro editorial (18h)
nos dias de tema; Mito ou Lei v3 (19h) nos dias pares. Legendas no método SEO/IA (skill ai-seo +
REGRAS_LEGENDA do Orbit). Fatos conferidos em 09/10/2026 (fontes no fim do arquivo).
"""

CTA = "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança."
ENT_GESTANTE = "Dra. Letícia Barros, a advogada da Gestante trabalhadora · Vitória/ES · OAB/ES 39.948"
ENT = "Dra. Letícia Barros · Advogada · Vitória/ES · OAB/ES 39.948"
BORDAO = "Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista."
CONS, TRAB, PREV, FAM = ("Direito do", "Consumidor"), ("Direito", "Trabalhista"), ("Direito", "Previdenciário"), ("Direito de", "Família")


def fecho_legenda(tema: dict, tags: str, mes: str | None = None) -> str:
    linhas = [CTA, "", ENT_GESTANTE if tema.get("gestante") else ENT]
    if tema.get("trabalhista"):
        linhas.append(BORDAO)
    linhas.append(f"Atualizado em {mes or tema.get('mes', 'novembro de 2026')}.")
    return "\n".join(linhas) + "\n\n" + tags


def legenda(tema: dict, gancho: str, resposta: str, *, faq=(), passos=(), alerta="", fontes="", convite="", tags="") -> str:
    partes = [gancho, resposta]
    if passos:
        partes.append("📌 O que fazer:\n" + "\n".join(f"✅ {p}" for p in passos))
    if alerta:
        partes.append(f"⚠️ {alerta}")
    if faq:
        partes.append("❓ As perguntas que mais chegam aqui:\n" + "\n".join(f"📌 {q}" for q in faq))
    if fontes:
        partes.append(f"📚 Fontes: {fontes}")
    if convite:
        partes.append(f"🔖 {convite}")
    return "\n\n".join(partes) + "\n\n" + fecho_legenda(tema, tags)


TEMAS = []


def tema(**t):
    TEMAS.append(t)
    return t


# ───────────────────────── Semana 1: 13º salário e a gestante ─────────────────────────

t = tema(chave="13-salario-2026", data="2026-11-03", area="Trabalhista", trabalhista=True,
         titulo="13º salário 2026: prazos e quem tem direito")
t["pergunta"] = dict(
    foto=6334545, pos="50% 50%", brilho=.9, area=TRAB,
    html="Quando cai a 1ª parcela do 13º? <em>A empresa pode pagar tudo só em dezembro?</em>",
    legenda=legenda(t,
        "Quando cai a 1ª parcela do 13º salário em 2026? Até segunda, 30 de novembro. E a empresa não pode jogar tudo para dezembro. 🎁",
        "O 13º é pago em duas parcelas. A primeira, metade do salário e sem descontos, vence em 30/11. "
        "A segunda vence em 20/12, que em 2026 cai num domingo: por isso o pagamento deve sair até sexta, 18/12. "
        "Pagar tudo de uma vez só é permitido se for até 30/11.",
        faq=["Quem tem direito? Quem trabalha de carteira assinada, inclusive doméstica, rural e temporária.",
             "Trabalhei só parte do ano. Recebo? Sim, 1/12 por mês com 15 dias ou mais de trabalho.",
             "Os descontos de INSS e IR vêm quando? Na 2ª parcela."],
        fontes="Lei 4.090/1962; Lei 4.749/1965, arts. 1º e 2º.",
        convite="Salva pra conferir o contracheque e manda pra quem está contando com o 13º.",
        tags="#13Salário #DécimoTerceiro #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.749/1965, arts. 1º e 2º.\n💬 Você já sabe o que vai fazer com a 1ª parcela?")
t["frase"] = dict(
    html="O 13º não é bônus. <em>É salário que você já trabalhou para receber.</em>",
    legenda=legenda(t,
        "13º salário não é favor da empresa. Ele é calculado mês a mês, pelo trabalho que você já fez no ano.",
        "Cada mês com 15 dias ou mais de trabalho vale 1/12 do 13º. A 1ª parcela vence em 30/11 e a 2ª deve sair até 18/12 em 2026.",
        convite="Manda pra quem ainda acha que o 13º depende da boa vontade do patrão.",
        tags="#13Salário #DécimoTerceiro #DireitoTrabalhista #DireitosDoTrabalhador #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.090/1962, art. 1º; Lei 4.749/1965.\n💬 Marca aqui quem precisa lembrar desse prazo.")
t["carrossel"] = dict(
    tag="13º salário", area="Trabalhista",
    capa=("13º salário 2026", "5 regras", "para não perder dinheiro",
          'Prazos, cálculo e descontos: <span class="mt">confira antes de 30/11</span>.', "Lei 4.749/1965"),
    itens=[
        ("A 1ª parcela vence<br>em <em>30 de novembro</em>", 'Metade do salário, <span class="mt">sem desconto de INSS e IR</span>. Em 2026, cai numa segunda.', "Lei 4.749/1965, art. 2º"),
        ("A 2ª parcela sai<br>até <em>18 de dezembro</em>", 'O prazo é 20/12, um domingo em 2026: <span class="mt">o pagamento vem antes</span>. Os descontos ficam aqui.', "Lei 4.749/1965, art. 1º"),
        ("Mês com 15 dias<br>vale <em>1/12</em>", 'Cada mês com 15 dias ou mais de trabalho <span class="mt">conta inteiro no cálculo</span>.', "Lei 4.090/1962, art. 1º, § 2º"),
        ("Horas extras<br><em>entram</em> na conta", 'A média de horas extras habituais, adicional noturno e comissões <span class="mt">integra o 13º</span>.', "Súmula 45 do TST"),
        ("Atrasou? Confira<br>o <em>contracheque</em>", "A empresa que paga fora do prazo pode ser multada pela fiscalização. Confira:", "Lei 7.855/1989, art. 3º"),
    ],
    checklist=["Valor da 1ª parcela (metade do salário)", "Média de horas extras e adicionais", "Descontos só na 2ª parcela"],
    fecho=("O 13º <em>não é</em><br>presente de Natal.", "É salário garantido em lei.", "mande para quem está contando com ele."),
    objetos=["corte-calculadora.png", "corte-cofrinho.png", "corte-reais.png"], foto5=33629668,
    legenda=legenda(t,
        "13º salário 2026: a 1ª parcela vence em 30/11 e a 2ª deve sair até 18/12. Arrasta pro lado e confere as 5 regras. 💰",
        "Quem trabalha de carteira assinada recebe o 13º em duas parcelas. A primeira é metade do salário, sem descontos. "
        "A segunda traz os descontos de INSS e imposto de renda. Cada mês com 15 dias ou mais de trabalho vale 1/12, "
        "e a média de horas extras habituais entra na conta.",
        faq=["A empresa pode pagar tudo em dezembro? Não. A 1ª parcela tem prazo até 30/11.",
             "Fui demitida no meio do ano. Perco o 13º? Não. Você recebe o proporcional na rescisão, salvo justa causa.",
             "Hora extra entra no 13º? Entra a média das horas extras habituais."],
        fontes="Lei 4.090/1962; Lei 4.749/1965; Súmula 45 do TST; Lei 7.855/1989, art. 3º.",
        convite="Salva pra conferir o contracheque e manda pra uma colega de trabalho.",
        tags="#13Salário #DécimoTerceiro #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.090/1962; Lei 4.749/1965; Súmula 45 do TST.\n💬 Qual dessas regras você não conhecia?")

t = tema(chave="gestante-13-licenca", data="2026-11-05", area="Trabalhista", trabalhista=True, gestante=True,
         titulo="Gestante em licença-maternidade recebe o 13º inteiro?")
t["pergunta"] = dict(
    foto=31627496, pos="50% 50%", brilho=.92, area=TRAB,
    html="Estou de licença-maternidade. <em>Vou receber o 13º inteiro?</em>",
    legenda=legenda(t,
        "Quem está de licença-maternidade recebe o 13º inteiro? Recebe, sim. Os meses da licença contam como meses trabalhados. 👶",
        "Para a trabalhadora de carteira assinada, a licença-maternidade não reduz o 13º. "
        "A empresa paga o valor completo e depois compensa com o INSS a parte que corresponde aos meses de licença. "
        "Se o 13º veio menor por causa da licença, há erro no cálculo.",
        passos=["Confira o contracheque da 1ª parcela, que vence em 30/11", "Compare com metade do seu salário",
                "Peça ao RH o cálculo por escrito se o valor estiver menor"],
        faq=["Quem paga, a empresa ou o INSS? A empresa paga e compensa a parte da licença com o INSS.",
             "Sou MEI e recebo do INSS. E o 13º? O INSS paga o 13º proporcional ao salário-maternidade."],
        fontes="Lei 4.090/1962; Lei 8.213/1991, art. 72, § 1º.",
        convite="Salva e manda pra uma amiga que está de licença.",
        tags="#LicençaMaternidade #DireitosDaGestante #13Salário #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.090/1962; Lei 8.213/1991, art. 72, § 1º.\n💬 Você sabia que a licença não diminui o 13º?")
t["frase"] = dict(
    html="Cuidar do seu bebê <em>não tira nada do seu 13º.</em>",
    legenda=legenda(t,
        "Licença-maternidade não é falta. Os meses em casa com o bebê contam para o 13º como meses trabalhados.",
        "A empresa paga o 13º inteiro e compensa com o INSS a parte da licença. Valor menor por causa da licença é erro de cálculo.",
        convite="Manda pra uma mãe que está de licença agora.",
        tags="#LicençaMaternidade #DireitosDaGestante #13Salário #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.090/1962; Lei 8.213/1991, art. 72, § 1º.\n💬 Marca uma mãe que precisa saber disso.")
t["carrossel"] = dict(
    tag="Gestante e 13º", area="Trabalhista",
    capa=("Gestante e 13º salário", "13º inteiro", "mesmo na licença-maternidade",
          'A licença <span class="mt">não reduz</span> o seu 13º. Confira como é pago.', "Lei 4.090/1962"),
    itens=[
        ("A licença <em>conta</em><br>para o 13º", 'Os meses de licença-maternidade entram no cálculo <span class="mt">como meses trabalhados</span>.', "Lei 4.090/1962"),
        ("Quem paga é<br>a <em>empresa</em>", 'A empresa paga o 13º inteiro e <span class="mt">compensa com o INSS</span> a parte da licença.', "Lei 8.213/1991, art. 72, § 1º"),
        ("<em>Sem</em> desconto<br>pelos meses em casa", 'Estar de licença não diminui o 13º. <span class="mt">Valor menor é sinal de erro.</span>', "Lei 4.090/1962"),
        ("MEI e autônoma:<br>o <em>INSS</em> paga", 'Quem recebe o salário-maternidade direto do INSS <span class="mt">recebe dele o 13º proporcional</span>.', "INSS · abono anual"),
        ("Veio menor?<br><em>Confira</em>", "Antes de falar com o RH, separe:", ""),
    ],
    checklist=["Contracheques do ano", "Datas de início e fim da licença", "Recibos da 1ª e da 2ª parcela"],
    fecho=("Licença-maternidade<br><em>não é</em> falta.", "É tempo protegido pela lei.", "mande para uma amiga de licença."),
    objetos=["corte-sapatinho.png", "corte-calculadora.png", "corte-ursinho.png"], foto5=30699348,
    legenda=legenda(t,
        "Gestante de licença-maternidade recebe o 13º inteiro? Sim. Arrasta pro lado e confere quem paga e como conferir. 👶",
        "A licença-maternidade conta como tempo de trabalho para o 13º. Na carteira assinada, a empresa paga o valor completo "
        "e compensa com o INSS a parte dos meses de licença. Quem recebe o salário-maternidade direto do INSS, como a MEI, "
        "recebe do próprio INSS o 13º proporcional ao benefício.",
        faq=["A licença diminui o 13º? Não. Os meses contam como trabalhados.",
             "Quem paga o 13º da licença? A empresa, que compensa a parte da licença com o INSS.",
             "E a MEI? O INSS paga o 13º proporcional ao salário-maternidade."],
        fontes="Lei 4.090/1962; Lei 8.213/1991, art. 72, § 1º.",
        convite="Salva e manda pra uma amiga grávida ou de licença.",
        tags="#DireitosDaGestante #LicençaMaternidade #13Salário #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.090/1962; Lei 8.213/1991, art. 72, § 1º.\n💬 Você já tinha ouvido que a licença diminuía o 13º?")

t = tema(chave="pensao-13", data="2026-11-07", area="Família", titulo="Pensão alimentícia e 13º: quando entra no desconto")
t["pergunta"] = dict(
    foto=7680692, pos="50% 50%", brilho=.9, area=FAM,
    html="O pai do meu filho recebe 13º. <em>A pensão também vale sobre ele?</em>",
    legenda=legenda(t,
        "A pensão alimentícia incide sobre o 13º salário? Quando a pensão é um percentual do salário, sim. 🎄",
        "O STJ firmou que a pensão fixada em percentual dos rendimentos incide sobre o 13º e sobre o terço de férias. "
        "Quando a pensão é um valor fixo em reais, vale o que está escrito no acordo ou na decisão: o 13º só entra se estiver previsto.",
        passos=["Leia como a pensão foi fixada: percentual ou valor fixo", "Confira os depósitos de novembro e dezembro",
                "Guarde os extratos"],
        faq=["E as férias? O desconto também vale sobre o terço de férias.",
             "O genitor não paga o 13º da pensão. E agora? Com a decisão em mãos, é possível cobrar na Justiça."],
        fontes="STJ, Tema 192 (REsp 1.106.654).",
        convite="Salva pra conferir em dezembro e manda pra quem recebe pensão.",
        tags="#PensãoAlimentícia #13Salário #DireitoDeFamília #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: STJ, Tema 192 (REsp 1.106.654).\n💬 Você sabia que o percentual da pensão vale também no 13º?")
t["frase"] = dict(
    html="Pensão não é favor ao outro genitor. <em>É direito da criança.</em>",
    legenda=legenda(t,
        "Pensão alimentícia é da criança, e não de quem recebe em nome dela.",
        "No fim do ano, vale lembrar: quando a pensão é um percentual do salário, o desconto incide também sobre o 13º e o terço de férias.",
        convite="Manda pra quem cuida sozinha dos filhos.",
        tags="#PensãoAlimentícia #DireitoDeFamília #DireitosDaCriança #MãeSolo #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Civil, art. 1.694; STJ, Tema 192.\n💬 Deixa um 💛 se você cuida dos seus filhos sozinha.")
t["carrossel"] = dict(
    tag="Pensão alimentícia", area="Família",
    capa=("Pensão alimentícia", "E o 13º?", "5 respostas antes do fim do ano",
          'Percentual ou valor fixo: <span class="mt">a forma da pensão muda tudo</span>.', "STJ, Tema 192"),
    itens=[
        ("Pensão em percentual:<br>o 13º <em>entra</em>", 'Quando a pensão é um percentual do salário, <span class="mt">o desconto vale também no 13º</span>.', "STJ, Tema 192"),
        ("O terço de férias<br><em>também</em> entra", 'A mesma regra vale para o <span class="mt">terço constitucional de férias</span>.', "STJ, Tema 192"),
        ("Valor fixo: leia<br>a <em>decisão</em>", 'Pensão fixada em reais segue o que está escrito. <span class="mt">O 13º só entra se estiver previsto.</span>', "Acordo ou sentença"),
        ("Desconto em folha:<br>a <em>empresa</em> repassa", 'Com ofício do juiz, a empresa desconta <span class="mt">e deposita direto</span> na conta indicada.', "CPC, art. 529"),
        ("Não caiu?<br><em>Organize</em> as provas", "Se o valor do 13º não chegou, separe:", ""),
    ],
    checklist=["Decisão ou acordo da pensão", "Extratos com os depósitos", "Contracheque do genitor, se tiver"],
    fecho=("Pensão é <em>do filho</em>.", "E o 13º também conta.", "mande para quem recebe pensão."),
    objetos=["corte-cofrinho.png", "corte-pasta.png", "corte-martelo.png"], foto5=3171117,
    legenda=legenda(t,
        "Pensão alimentícia e 13º salário: quando o desconto vale também no fim do ano? Arrasta pro lado. 🎄",
        "A resposta depende de como a pensão foi fixada. Em percentual do salário, o STJ decidiu que o desconto incide sobre o 13º "
        "e o terço de férias. Em valor fixo, vale o texto do acordo ou da decisão. Com desconto em folha, a empresa repassa direto.",
        faq=["Pensão em percentual incide no 13º? Sim, conforme o STJ (Tema 192).",
             "E se a pensão é valor fixo? Só entra se o acordo ou a decisão previr.",
             "O 13º não foi repassado. Posso cobrar? Sim, com a decisão e os extratos."],
        fontes="STJ, Tema 192 (REsp 1.106.654); CPC, art. 529.",
        convite="Salva pra conferir em dezembro e manda pra quem recebe pensão.",
        tags="#PensãoAlimentícia #13Salário #DireitoDeFamília #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: STJ, Tema 192 (REsp 1.106.654); CPC, art. 529.\n💬 A sua pensão foi fixada em percentual ou valor fixo?")

# ─────────────────────── Semana 2: depois do parto, a mãe que volta ───────────────────────

t = tema(chave="amamentacao-trabalho", data="2026-11-10", area="Trabalhista", trabalhista=True, gestante=True,
         titulo="Amamentação no trabalho: 2 pausas de 30 minutos até 6 meses")
t["pergunta"] = dict(
    foto=7282634, pos="50% 40%", brilho=.95, area=TRAB,
    html="Voltei da licença e ainda amamento. <em>Posso sair do trabalho para amamentar?</em>",
    legenda=legenda(t,
        "Mãe que amamenta tem pausa no trabalho? Tem, sim: 2 descansos de meia hora por dia até o bebê completar 6 meses. 🍼",
        "A CLT garante à mãe que amamenta dois descansos especiais de 30 minutos cada, dentro do expediente, até o filho completar "
        "6 meses. Os horários são combinados com a empresa, e o prazo pode ser estendido quando a saúde do bebê exigir. "
        "A regra vale também para filho adotivo.",
        passos=["Peça as pausas por escrito ao RH", "Combine os horários", "Guarde o atestado se o médico pedir mais tempo"],
        faq=["Posso juntar as duas pausas? Os horários são definidos em acordo com a empresa.",
             "E se a empresa negar? A Justiça do Trabalho tem mandado pagar a pausa negada como hora extra."],
        fontes="CLT, art. 396, §§ 1º e 2º.",
        convite="Salva e manda pra uma mãe que está voltando ao trabalho.",
        tags="#Amamentação #DireitosDaGestante #MãeQueTrabalha #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 396.\n💬 Você sabia dessas 2 pausas?")
t["frase"] = dict(
    html="Voltar ao trabalho <em>não é deixar de ser mãe.</em>",
    legenda=legenda(t,
        "A volta da licença é um dos momentos mais difíceis para a mãe que trabalha. A lei sabe disso.",
        "Até o bebê completar 6 meses, a CLT garante 2 pausas de meia hora por dia para amamentar, dentro do expediente.",
        convite="Manda pra uma mãe que está voltando ao trabalho esta semana.",
        tags="#Amamentação #MãeQueTrabalha #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 396.\n💬 Deixa um 💛 para as mães que voltaram ao trabalho.")
t["carrossel"] = dict(
    tag="Amamentação", area="Trabalhista",
    capa=("Amamentação no trabalho", "2 pausas", "de meia hora por dia, até os 6 meses",
          'Um direito da mãe que volta da licença <span class="mt">e quase ninguém usa</span>.', "CLT, art. 396"),
    itens=[
        ("Até os 6 meses,<br><em>2 pausas</em> por dia", 'Dois descansos de <span class="mt">meia hora cada</span>, dentro do expediente.', "CLT, art. 396"),
        ("Os horários são<br><em>combinados</em>", 'Mãe e empresa definem os horários <span class="mt">em acordo individual</span>.', "CLT, art. 396, § 2º"),
        ("A saúde do bebê pede?<br>O prazo <em>aumenta</em>", 'Com indicação médica, <span class="mt">os 6 meses podem ser estendidos</span>.', "CLT, art. 396, § 1º"),
        ("Vale também<br>na <em>adoção</em>", 'A regra protege a mãe <span class="mt">de filho adotivo</span>.', "CLT, art. 396"),
        ("Pausa negada?<br><em>Registre</em>", "A Justiça tem mandado pagar a pausa negada como hora extra. Guarde:", "CLT, art. 396"),
    ],
    checklist=["Certidão de nascimento do bebê", "Pedido das pausas por escrito", "Registro de ponto dos dias"],
    fecho=("Amamentar <em>é direito</em><br>de quem trabalha.", "E do seu bebê também.", "mande para uma mãe que voltou ao trabalho."),
    objetos=["corte-ampulheta.png", "corte-ursinho.png", "corte-celular.png"], foto5=8430560,
    legenda=legenda(t,
        "Amamentação no trabalho: até os 6 meses, a mãe tem 2 pausas de meia hora por dia. Arrasta pro lado e confere. 🍼",
        "A CLT garante dois descansos especiais de 30 minutos para amamentar, dentro do expediente, até o bebê completar 6 meses. "
        "Os horários são combinados com a empresa, o prazo pode ser estendido por indicação médica e a regra vale para filho adotivo.",
        faq=["A pausa é dentro do expediente? Sim, são descansos especiais no horário de trabalho.",
             "Vale para mãe adotiva? Vale.",
             "Posso estender depois dos 6 meses? Sim, quando a saúde do bebê exigir."],
        fontes="CLT, art. 396, §§ 1º e 2º.",
        convite="Salva e manda pra uma mãe que está voltando da licença.",
        tags="#Amamentação #DireitosDaGestante #MãeQueTrabalha #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 396, §§ 1º e 2º.\n💬 A sua empresa respeitou essas pausas?")

t = tema(chave="creche-empresa", data="2026-11-12", area="Trabalhista", trabalhista=True, gestante=True,
         titulo="Creche ou auxílio-creche: quando a empresa é obrigada")
t["pergunta"] = dict(
    foto=6693300, pos="50% 50%", brilho=.92, area=TRAB,
    html="Na minha empresa trabalham 40 mulheres. <em>Ela é obrigada a ter creche?</em>",
    legenda=legenda(t,
        "Empresa com 30 mulheres ou mais é obrigada a ter creche? Precisa garantir um local para os bebês no período de amamentação. 🧸",
        "A CLT exige que o estabelecimento com pelo menos 30 mulheres acima de 16 anos tenha local apropriado para as mães deixarem "
        "os filhos durante a amamentação. A empresa pode cumprir por creche conveniada ou trocar o local pelo reembolso-creche, "
        "que vale para filhos de até 5 anos e 11 meses.",
        faq=["Reembolso-creche é salário? Não. O valor não tem natureza salarial.",
             "Minha empresa tem menos de 30 mulheres. Tenho algum direito? Confira a convenção coletiva: muitas garantem auxílio-creche."],
        fontes="CLT, art. 389, §§ 1º e 2º; Lei 14.457/2022.",
        convite="Salva e manda pra uma colega que vai voltar da licença.",
        tags="#AuxílioCreche #MãeQueTrabalha #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 389, §§ 1º e 2º; Lei 14.457/2022.\n💬 A sua empresa oferece creche ou reembolso?")
t["frase"] = dict(
    html="Nenhuma mãe deveria escolher <em>entre o emprego e o filho.</em>",
    legenda=legenda(t,
        "A volta da licença esbarra numa pergunta: com quem fica o bebê?",
        "Empresa com 30 mulheres ou mais precisa garantir local para os bebês no período de amamentação, por creche conveniada ou reembolso-creche.",
        convite="Manda pra uma mãe que está procurando creche agora.",
        tags="#MãeQueTrabalha #AuxílioCreche #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 389, § 1º.\n💬 Deixa um 💛 se você já viveu essa escolha.")
t["carrossel"] = dict(
    tag="Creche e trabalho", area="Trabalhista",
    capa=("Creche e trabalho", "30 mulheres", "e a empresa já tem obrigação",
          'Local para os bebês, creche conveniada <span class="mt">ou reembolso-creche</span>.', "CLT, art. 389"),
    itens=[
        ("30 mulheres:<br>a regra <em>muda</em>", 'Estabelecimento com <span class="mt">30 ou mais mulheres acima de 16 anos</span> precisa de local para os bebês.', "CLT, art. 389, § 1º"),
        ("Um lugar para<br>a <em>amamentação</em>", 'Espaço para a mãe deixar o filho <span class="mt">e amamentar no expediente</span>.', "CLT, art. 389, § 1º"),
        ("Pode ser creche<br><em>conveniada</em>", 'A empresa pode cumprir por <span class="mt">convênio com creche</span> pública ou privada.', "CLT, art. 389, § 2º"),
        ("Ou <em>reembolso</em>-creche", 'Para filhos até 5 anos e 11 meses. <span class="mt">Não tem natureza de salário.</span>', "Lei 14.457/2022"),
        ("Leia a<br><em>convenção</em>", "Muitas categorias garantem auxílio-creche maior. Confira:", ""),
    ],
    checklist=["Se existe auxílio-creche e o valor", "Até que idade do filho vale", "Como pedir o reembolso"],
    fecho=("Mãe que trabalha<br>precisa de <em>rede</em>.", "E a empresa faz parte dela.", "mande para uma colega que vai voltar da licença."),
    objetos=["obj-ursinho2.png", "corte-chaves.png", "corte-cafe.png"], foto5=6692931,
    legenda=legenda(t,
        "Creche e trabalho: empresa com 30 mulheres ou mais tem obrigação com os bebês das funcionárias. Arrasta pro lado. 🧸",
        "O estabelecimento com pelo menos 30 mulheres acima de 16 anos precisa de local para as mães deixarem os filhos no período de "
        "amamentação. Pode ser creche própria, conveniada ou o reembolso-creche, que vale para filhos de até 5 anos e 11 meses e não "
        "tem natureza salarial.",
        faq=["Toda empresa é obrigada? A obrigação legal começa em 30 mulheres acima de 16 anos.",
             "Reembolso-creche entra no salário? Não.",
             "A convenção pode garantir mais? Pode, e muitas garantem."],
        fontes="CLT, art. 389, §§ 1º e 2º; Lei 14.457/2022.",
        convite="Salva e manda pra uma colega que vai voltar da licença.",
        tags="#AuxílioCreche #MãeQueTrabalha #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 389, §§ 1º e 2º; Lei 14.457/2022.\n💬 Você sabia do reembolso-creche?")

t = tema(chave="gestante-insalubre", data="2026-11-14", area="Trabalhista", trabalhista=True, gestante=True,
         titulo="Grávida em local insalubre deve ser afastada")
t["pergunta"] = dict(
    foto=9628836, pos="50% 50%", brilho=.9, area=TRAB,
    html="Trabalho em local insalubre e estou grávida. <em>A empresa tem que me afastar?</em>",
    legenda=legenda(t,
        "Grávida pode trabalhar em local insalubre? Não. A gestante deve ser afastada da insalubridade em qualquer grau. 🧪",
        "A CLT manda afastar a gestante de atividades insalubres, sem prejuízo do salário e do adicional de insalubridade. "
        "O STF derrubou a exigência de atestado médico para isso. Se a empresa não tiver função segura, a gravidez é tratada "
        "como de risco e o INSS paga o salário-maternidade durante o afastamento.",
        passos=["Comunique a gravidez por escrito", "Peça a mudança de função ou o afastamento", "Guarde o laudo ou o PPP da insalubridade"],
        faq=["Perco o adicional de insalubridade? Não. Ele continua sendo pago.",
             "E depois do parto? A lactante também deve ficar longe da insalubridade."],
        fontes="CLT, art. 394-A; STF, ADI 5938.",
        convite="Salva e manda pra uma gestante que trabalha em hospital, laboratório ou indústria.",
        tags="#DireitosDaGestante #Insalubridade #GestanteCLT #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 394-A; STF, ADI 5938.\n💬 Você conhece alguma gestante que ainda trabalha em local insalubre?")
t["frase"] = dict(
    html="Nenhum salário vale <em>a saúde do seu bebê.</em>",
    legenda=legenda(t,
        "Gestante e lactante não podem trabalhar em local insalubre. E não precisam escolher entre a saúde e o adicional.",
        "O afastamento é obrigatório, em qualquer grau de insalubridade, com o salário e o adicional mantidos.",
        convite="Manda pra uma gestante que trabalha na saúde ou na indústria.",
        tags="#DireitosDaGestante #Insalubridade #GestanteCLT #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 394-A; STF, ADI 5938.\n💬 Marca uma gestante que precisa saber disso.")
t["carrossel"] = dict(
    tag="Gestante", area="Trabalhista",
    capa=("Gravidez e insalubridade", "Afastada", "sem perder o adicional",
          'Gestante e lactante <span class="mt">longe da insalubridade</span>, em qualquer grau.', "CLT, art. 394-A"),
    itens=[
        ("Insalubre em<br><em>qualquer grau</em>", 'Grau mínimo, médio ou máximo: <span class="mt">a gestante deve ser afastada</span>.', "CLT, art. 394-A; STF, ADI 5938"),
        ("<em>Sem</em> precisar<br>de atestado", 'O STF derrubou a exigência de atestado. <span class="mt">A proteção vale para todas.</span>', "STF, ADI 5938"),
        ("O adicional<br><em>continua</em>", 'O afastamento mantém a remuneração, <span class="mt">com o adicional de insalubridade</span>.', "CLT, art. 394-A"),
        ("Sem função segura?<br>O <em>INSS</em> paga", 'A gravidez é tratada como de risco e <span class="mt">o salário-maternidade cobre o afastamento</span>.', "CLT, art. 394-A, § 3º"),
        ("Amamentando?<br>A regra <em>segue</em>", "A lactante também fica longe da insalubridade. Separe:", "CLT, art. 394-A, III"),
    ],
    checklist=["Exame ou atestado da gravidez", "Laudo ou PPP da insalubridade", "Comunicado à empresa por escrito"],
    fecho=("Nenhum salário vale<br>a <em>saúde do bebê</em>.", "E a lei não pede essa escolha.", "mande para uma gestante que trabalha."),
    objetos=["corte-estetoscopio.png", "corte-ultrassom.png", "corte-prancheta.png"], foto5=16122138,
    legenda=legenda(t,
        "Grávida em local insalubre deve ser afastada, em qualquer grau e sem perder o adicional. Arrasta pro lado. 🧪",
        "A CLT protege gestante e lactante: o afastamento da insalubridade é obrigatório e mantém o salário e o adicional. "
        "Desde a decisão do STF na ADI 5938, não é preciso atestado. Se a empresa não tiver função segura, o INSS paga o "
        "salário-maternidade durante todo o afastamento.",
        faq=["Preciso de atestado para ser afastada? Não, segundo o STF.",
             "Perco o adicional? Não.",
             "A empresa não tem outra função. E agora? A gravidez é tratada como de risco e o INSS paga."],
        fontes="CLT, art. 394-A; STF, ADI 5938.",
        convite="Salva e manda pra uma gestante que trabalha em hospital, laboratório ou indústria.",
        tags="#DireitosDaGestante #Insalubridade #GestanteCLT #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 394-A; STF, ADI 5938.\n💬 Você sabia que não precisa de atestado?")

# ──────────────────── Semana 3: Consciência Negra e alimentos gravídicos ────────────────────

t = tema(chave="feriado-20-novembro", data="2026-11-17", area="Trabalhista", trabalhista=True,
         titulo="20/11 é feriado nacional: trabalho no feriado paga em dobro ou folga")
t["pergunta"] = dict(
    foto=29509527, pos="50% 50%", brilho=.95, area=TRAB,
    html="Vou trabalhar no feriado de 20 de novembro. <em>Recebo em dobro?</em>",
    legenda=legenda(t,
        "Trabalhar no feriado de 20 de novembro paga em dobro? Paga, se a empresa não der outra folga. 🗓️",
        "Desde 2024, o Dia Nacional de Zumbi e da Consciência Negra é feriado em todo o país. Em 2026, cai numa sexta. "
        "Quem trabalha no feriado recebe o dia em dobro, além do repouso, ou ganha outro dia de folga no lugar. "
        "No comércio, o trabalho em feriado depende de autorização em convenção coletiva.",
        passos=["Anote o horário trabalhado no dia 20", "Confira o contracheque de novembro ou dezembro",
                "Se houve troca, guarde a data da folga"],
        faq=["Feriado trabalhado é hora extra de 50%? Não. Sem folga, o pagamento é em dobro."],
        fontes="Lei 14.759/2023; Lei 605/1949, art. 9º; Súmula 146 do TST; Lei 10.101/2000, art. 6º-A.",
        convite="Salva e manda pra quem vai trabalhar na sexta, dia 20.",
        tags="#ConsciênciaNegra #Feriado #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 14.759/2023; Lei 605/1949, art. 9º; Súmula 146 do TST.\n💬 Você vai trabalhar no dia 20?")
t["frase"] = dict(
    html="Consciência Negra também é sobre <em>trabalho digno.</em>",
    legenda=legenda(t,
        "20 de novembro é feriado nacional, Dia de Zumbi e da Consciência Negra. E é também um dia para falar de trabalho com respeito.",
        "Quem trabalha no feriado recebe o dia em dobro ou ganha outra folga. E racismo no trabalho é crime, sem exceção.",
        convite="Manda pra quem vai trabalhar no dia 20.",
        tags="#ConsciênciaNegra #20DeNovembro #DireitoTrabalhista #TrabalhoDigno #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 14.759/2023; Lei 605/1949, art. 9º.\n💬 Deixa um ✊🏾 se esse dia é importante para você.")
t["carrossel"] = dict(
    tag="20 de novembro", area="Trabalhista",
    capa=("Feriado de 20 de novembro", "Em dobro", "ou folga: o feriado trabalhado",
          'Dia Nacional de Zumbi e da Consciência Negra: <span class="mt">feriado em todo o país</span>.', "Lei 14.759/2023"),
    itens=[
        ("20 de novembro<br>é feriado <em>nacional</em>", 'Vale em todo o país <span class="mt">desde 2024</span>. Em 2026, cai numa sexta.', "Lei 14.759/2023"),
        ("Trabalhou?<br>Recebe <em>em dobro</em>", 'O dia trabalhado é pago em dobro, <span class="mt">além do repouso</span>.', "Lei 605/1949, art. 9º; Súmula 146 do TST"),
        ("Ou ganha<br>outra <em>folga</em>", 'A empresa pode trocar o pagamento em dobro <span class="mt">por outro dia de descanso</span>.', "Lei 605/1949, art. 9º"),
        ("No comércio,<br>vale a <em>convenção</em>", 'Trabalho em feriado no comércio <span class="mt">precisa de autorização</span> em convenção coletiva.', "Lei 10.101/2000, art. 6º-A"),
        ("Anote o<br><em>ponto</em>", "Para conferir o pagamento depois, separe:", ""),
    ],
    checklist=["Registro de ponto do dia 20", "Contracheque do mês seguinte", "Data da folga, se houve troca"],
    fecho=("Feriado trabalhado<br>tem <em>preço</em>.", "E ele está na lei.", "mande para quem trabalha no dia 20."),
    objetos=["corte-cafe.png", "corte-reais.png", "corte-carimbo.png"], foto5=36703589,
    legenda=legenda(t,
        "20 de novembro é feriado nacional. Quem trabalha recebe em dobro ou ganha folga. Arrasta pro lado. 🗓️",
        "A Lei 14.759/2023 tornou o Dia Nacional de Zumbi e da Consciência Negra feriado em todo o país. "
        "Em 2026 ele cai numa sexta. O trabalho no feriado é pago em dobro, além do repouso, salvo se a empresa der "
        "outro dia de folga. No comércio, depende de autorização em convenção coletiva.",
        faq=["20/11 é feriado em todo o Brasil? Sim, desde a Lei 14.759/2023.",
             "Trabalhar no feriado é hora extra de 50%? Não. É em dobro, ou folga em outro dia.",
             "O comércio pode abrir? Só com autorização em convenção coletiva."],
        fontes="Lei 14.759/2023; Lei 605/1949, art. 9º; Súmula 146 do TST; Lei 10.101/2000, art. 6º-A.",
        convite="Salva e manda pra quem vai trabalhar na sexta, dia 20.",
        tags="#ConsciênciaNegra #Feriado #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 14.759/2023; Lei 605/1949, art. 9º; Súmula 146 do TST.\n💬 Na sua empresa, feriado trabalhado vira folga ou pagamento em dobro?")

t = tema(chave="racismo-trabalho", data="2026-11-19", area="Trabalhista", trabalhista=True,
         titulo="Racismo no trabalho: injúria racial e como reunir provas")
t["pergunta"] = dict(
    foto=12911213, pos="50% 45%", brilho=.92, area=TRAB,
    html="Um colega faz piadas sobre o meu cabelo. <em>Isso é crime?</em>",
    legenda=legenda(t,
        "Piada sobre cabelo crespo no trabalho é crime? Pode ser injúria racial, e o tom de brincadeira aumenta a pena. ✊🏾",
        "Ofender alguém por raça, cor ou etnia é injúria racial, com pena de 2 a 5 anos de reclusão. Quando a ofensa vem "
        "em tom de piada ou diversão, a lei aumenta a pena de um terço até a metade. A empresa que tolera esse ambiente "
        "pode ser condenada a indenizar.",
        passos=["Anote data, hora, local e o que foi dito", "Guarde prints, áudios e e-mails",
                "Liste quem presenciou", "Use o canal de denúncia da empresa"],
        faq=["Preciso registrar boletim de ocorrência? A injúria racial é crime e pode ser registrada na delegacia."],
        fontes="Lei 7.716/1989, arts. 2º-A e 20-A (Lei 14.532/2023); CLT, art. 223-B.",
        convite="Salva e manda pra quem já ouviu que era só brincadeira.",
        tags="#RacismoÉCrime #InjúriaRacial #ConsciênciaNegra #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 7.716/1989, arts. 2º-A e 20-A.\n💬 Você sabia que a \"piada\" aumenta a pena?")
t["frase"] = dict(
    html="Ninguém deveria <em>engolir calada</em> para manter o emprego.",
    legenda=legenda(t,
        "Racismo no trabalho não é coisa da sua cabeça. E não é algo que você tem que engolir calada.",
        "Injúria racial é crime, com pena de 2 a 5 anos, e o tom de piada aumenta a pena. A prova começa com anotações, prints e testemunhas.",
        convite="Manda pra quem precisa ouvir isso hoje.",
        tags="#RacismoÉCrime #InjúriaRacial #ConsciênciaNegra #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 7.716/1989, arts. 2º-A e 20-A.\n💬 Deixa um ✊🏾 em apoio.")
t["carrossel"] = dict(
    tag="Racismo no trabalho", area="Trabalhista",
    capa=("Racismo no trabalho", "Não é piada", "é crime: 5 passos para se proteger",
          'Injúria racial dá <span class="mt">2 a 5 anos de reclusão</span>.', "Lei 14.532/2023"),
    itens=[
        ("Injúria racial<br>é <em>crime</em>", 'Ofender alguém por raça, cor ou etnia <span class="mt">dá de 2 a 5 anos de reclusão</span>.', "Lei 7.716/1989, art. 2º-A"),
        ("Em tom de piada,<br>a pena <em>aumenta</em>", 'O "foi só brincadeira" <span class="mt">aumenta a pena de 1/3 até a metade</span>.', "Lei 7.716/1989, art. 20-A"),
        ("A empresa<br><em>responde</em>", 'Quem tolera a ofensa no ambiente de trabalho <span class="mt">pode ter que indenizar</span>.', "CLT, art. 223-B; CC, art. 932, III"),
        ("Use o canal<br>de <em>denúncia</em>", 'Empresas com CIPA devem ter canal para denúncias <span class="mt">de assédio e violência</span>.', "Lei 14.457/2022, art. 23"),
        ("A prova é<br>a parte <em>decisiva</em>", "Comece a reunir hoje:", ""),
    ],
    checklist=["Prints, áudios e e-mails", "Nomes de quem presenciou", "Datas e o que foi dito"],
    fecho=("Racismo <em>não é</em><br>brincadeira.", "É crime, inclusive no trabalho.", "mande para quem precisa ouvir isso."),
    objetos=["corte-celular.png", "corte-caneta.png", "corte-martelo.png"], foto5=5386496,
    legenda=legenda(t,
        "Racismo no trabalho: injúria racial é crime, e a piada aumenta a pena. Arrasta pro lado e confere como reunir provas. ✊🏾",
        "Desde a Lei 14.532/2023, a injúria racial tem pena de 2 a 5 anos de reclusão. Se a ofensa vem em tom de piada ou "
        "diversão, a pena aumenta de um terço até a metade. A empresa que tolera responde por indenização, e as empresas com "
        "CIPA devem manter canal de denúncia.",
        faq=["Piada racista é crime? Pode ser injúria racial, com pena aumentada.",
             "A empresa tem responsabilidade? Sim, pelo ambiente de trabalho que mantém.",
             "Como provo? Prints, áudios, e-mails, testemunhas e anotações com data."],
        fontes="Lei 7.716/1989, arts. 2º-A e 20-A; Lei 14.532/2023; CLT, art. 223-B; Lei 14.457/2022, art. 23.",
        convite="Salva e manda pra quem já ouviu que era só brincadeira.",
        tags="#RacismoÉCrime #InjúriaRacial #ConsciênciaNegra #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 7.716/1989, arts. 2º-A e 20-A; Lei 14.457/2022, art. 23.\n💬 A sua empresa tem canal de denúncia?")

t = tema(chave="alimentos-gravidicos", data="2026-11-21", area="Família", gestante=True,
         titulo="Alimentos gravídicos: pensão ao pai antes do bebê nascer")
t["pergunta"] = dict(
    foto=32592295, pos="50% 45%", brilho=.95, area=FAM,
    html="Estou grávida e o pai não quer ajudar. <em>Posso pedir pensão antes do bebê nascer?</em>",
    legenda=legenda(t,
        "Grávida pode pedir pensão antes do bebê nascer? Pode. São os alimentos gravídicos. 🤰",
        "A Lei 11.804/2008 permite que a gestante peça ao pai uma ajuda com as despesas da gravidez: consultas, exames, "
        "alimentação especial, remédios e parto. Não é preciso exame de DNA durante a gestação: bastam indícios da "
        "paternidade, como mensagens, fotos e testemunhas. Depois do parto, a pensão continua para o bebê.",
        passos=["Guarde os comprovantes das despesas da gravidez", "Salve conversas e fotos com o pai",
                "Reúna o que souber sobre a renda dele"],
        faq=["Precisa de DNA? Não na gravidez. Bastam indícios da paternidade.",
             "E depois que o bebê nascer? A pensão passa a ser do bebê, até alguém pedir revisão."],
        fontes="Lei 11.804/2008, arts. 2º e 6º.",
        convite="Salva e manda pra uma amiga grávida.",
        tags="#AlimentosGravídicos #PensãoAlimentícia #Gestante #DireitoDeFamília #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 11.804/2008, arts. 2º e 6º.\n💬 Você conhecia os alimentos gravídicos?")
t["frase"] = dict(
    html="Seu filho tem direitos <em>antes mesmo de nascer.</em>",
    legenda=legenda(t,
        "A gravidez tem custo, e ele não precisa ser só seu.",
        "Os alimentos gravídicos ajudam com consultas, exames, remédios e parto. Bastam indícios da paternidade, sem DNA na gestação.",
        convite="Manda pra uma amiga grávida que está passando por isso sozinha.",
        tags="#AlimentosGravídicos #Gestante #PensãoAlimentícia #DireitoDeFamília #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 11.804/2008.\n💬 Deixa um 💛 para as gestantes que estão seguindo sozinhas.")
t["carrossel"] = dict(
    tag="Gestante", area="Família",
    capa=("Alimentos gravídicos", "Pensão", "antes do bebê nascer",
          'A gestante pode pedir ajuda ao pai <span class="mt">já na gravidez</span>.', "Lei 11.804/2008"),
    itens=[
        ("A pensão começa<br><em>na gravidez</em>", 'A gestante pode pedir alimentos ao pai <span class="mt">antes do bebê nascer</span>.', "Lei 11.804/2008"),
        ("Cobre as despesas<br>da <em>gestação</em>", 'Consultas, exames, alimentação especial, <span class="mt">remédios e parto</span>.', "Lei 11.804/2008, art. 2º"),
        ("Bastam <em>indícios</em><br>da paternidade", 'Não precisa de DNA na gravidez. <span class="mt">Mensagens, fotos e testemunhas</span> ajudam.', "Lei 11.804/2008, art. 6º"),
        ("Cada um paga<br>na <em>proporção</em>", 'O valor considera os recursos <span class="mt">da gestante e do pai</span>.', "Lei 11.804/2008, art. 2º, par. único"),
        ("Depois do parto,<br><em>continua</em>", "Com o nascimento, vira pensão do bebê. Para pedir, separe:", "Lei 11.804/2008, art. 6º, par. único"),
    ],
    checklist=["Exames e comprovantes de gastos", "Conversas e fotos com o pai", "O que souber da renda dele"],
    fecho=("A pensão do seu filho<br>começa <em>na barriga</em>.", "A lei não espera o parto.", "mande para uma amiga grávida."),
    objetos=["corte-ultrassom.png", "corte-sapatinho-azul.png", "corte-martelo.png"], foto5=19785770,
    legenda=legenda(t,
        "Alimentos gravídicos: a gestante pode pedir pensão ao pai antes do bebê nascer. Arrasta pro lado. 🤰",
        "A Lei 11.804/2008 garante à gestante ajuda do pai com as despesas da gravidez, como consultas, exames, remédios e parto. "
        "O juiz decide com base em indícios da paternidade, sem DNA na gestação, e o valor considera os recursos dos dois. "
        "Com o nascimento, os alimentos viram pensão do bebê.",
        faq=["Precisa de DNA? Não. Bastam indícios.",
             "O que a pensão cobre? As despesas da gravidez até o parto.",
             "Depois do parto acaba? Não. Vira pensão alimentícia do bebê."],
        fontes="Lei 11.804/2008, arts. 2º e 6º.",
        convite="Salva e manda pra uma amiga grávida.",
        tags="#AlimentosGravídicos #PensãoAlimentícia #Gestante #DireitoDeFamília #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 11.804/2008, arts. 2º e 6º.\n💬 Você sabia que não precisa de DNA na gravidez?")

# ─────────────────────── Semana 4: Previdenciário da mulher ───────────────────────

t = tema(chave="aposentadoria-mulher-2026", data="2026-11-24", area="Previdenciário",
         titulo="Aposentadoria da mulher em 2026: 59 anos e 6 meses ou 93 pontos")
t["pergunta"] = dict(
    foto=11527706, pos="50% 50%", brilho=.9, area=PREV,
    html="Tenho 58 anos e 30 de contribuição. <em>Já posso me aposentar?</em>",
    legenda=legenda(t,
        "Mulher com 58 anos e 30 de contribuição já pode se aposentar em 2026? Talvez. Depende da regra de transição. 👵🏾",
        "Em 2026, a idade mínima progressiva pede 59 anos e 6 meses com 30 anos de contribuição, e a regra de pontos pede 93. "
        "Mas a regra do pedágio de 100% aceita 57 anos, desde que você cumpra também o tempo que faltava em novembro de 2019. "
        "Por isso a simulação no Meu INSS é o primeiro passo.",
        passos=["Baixe o extrato do CNIS no Meu INSS", "Confira se todos os vínculos aparecem", "Faça a simulação das regras"],
        faq=["Quantos pontos a mulher precisa em 2026? 93, com 30 anos de contribuição.",
             "E por idade? 62 anos e 15 anos de contribuição."],
        fontes="EC 103/2019, arts. 15, 16, 18 e 20.",
        convite="Salva e manda pra quem está perto de se aposentar.",
        tags="#Aposentadoria #INSS #AposentadoriaDaMulher #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: EC 103/2019, arts. 15, 16, 18 e 20.\n💬 Você já fez a simulação no Meu INSS?")
t["frase"] = dict(
    html="Uma vida inteira de trabalho <em>merece ser contada até o último mês.</em>",
    legenda=legenda(t,
        "Um vínculo que não aparece no CNIS pode atrasar a sua aposentadoria em anos.",
        "Antes de pedir, confira o extrato do INSS e compare com as carteiras de trabalho. Cada mês conta na regra de transição.",
        convite="Manda pra quem está perto de se aposentar.",
        tags="#Aposentadoria #INSS #AposentadoriaDaMulher #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: EC 103/2019.\n💬 Marca aqui quem está contando os meses para se aposentar.")
t["carrossel"] = dict(
    tag="Aposentadoria", area="Previdenciário",
    capa=("Aposentadoria da mulher", "5 regras", "para se aposentar em 2026",
          'Idade, pontos ou pedágio: <span class="mt">a regra certa muda o valor</span>.', "EC 103/2019"),
    itens=[
        ("Por idade:<br><em>62 anos</em>", 'Com <span class="mt">15 anos de contribuição</span>, para quem já contribuía antes da Reforma.', "EC 103/2019, art. 18"),
        ("Por pontos:<br><em>93</em> em 2026", 'Idade + tempo de contribuição, <span class="mt">com no mínimo 30 anos</span> de contribuição.', "EC 103/2019, art. 15"),
        ("Idade mínima:<br><em>59 anos e meio</em>", 'Com 30 anos de contribuição. <span class="mt">Sobe 6 meses por ano.</span>', "EC 103/2019, art. 16"),
        ("Pedágio:<br>a partir dos <em>57</em>", '57 anos, 30 de contribuição e <span class="mt">mais o tempo que faltava em 2019</span>.', "EC 103/2019, art. 20"),
        ("Antes de pedir,<br><em>simule</em>", "A regra mais vantajosa muda o valor. Separe:", ""),
    ],
    checklist=["Extrato do CNIS no Meu INSS", "Carteiras de trabalho antigas", "Carnês e períodos sem registro"],
    fecho=("Cada ano de trabalho<br><em>conta</em>.", "Confira se o INSS registrou todos.", "mande para quem está perto de se aposentar."),
    objetos=["corte-pasta.png", "corte-calculadora.png", "corte-ampulheta.png"], foto5=31005426,
    legenda=legenda(t,
        "Aposentadoria da mulher em 2026: 62 anos, 93 pontos, 59 anos e meio ou pedágio. Arrasta pro lado e confere as 5 regras. 👵🏾",
        "Depois da Reforma da Previdência, a mulher tem regras de transição. Em 2026: por idade, 62 anos e 15 de contribuição; "
        "por pontos, 93 com 30 de contribuição; pela idade mínima progressiva, 59 anos e 6 meses com 30 de contribuição; "
        "e pelo pedágio de 100%, 57 anos e 30 de contribuição mais o tempo que faltava em 2019.",
        faq=["Quantos pontos em 2026? 93 para a mulher.",
             "Qual a idade mínima? 59 anos e 6 meses na regra progressiva.",
             "Qual regra é melhor? A que der o maior valor, por isso a simulação."],
        fontes="EC 103/2019, arts. 15, 16, 18 e 20.",
        convite="Salva e manda pra quem está perto de se aposentar.",
        tags="#Aposentadoria #INSS #AposentadoriaDaMulher #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: EC 103/2019, arts. 15, 16, 18 e 20.\n💬 Qual dessas regras parece a sua?")

t = tema(chave="desempregada-gravida-inss", data="2026-11-26", area="Previdenciário", gestante=True,
         titulo="Desempregada e grávida: salário-maternidade pelo INSS")
t["pergunta"] = dict(
    foto=39462003, pos="50% 55%", brilho=.95, area=PREV,
    html="Estou sem emprego há 8 meses e grávida. <em>O INSS paga o salário-maternidade?</em>",
    legenda=legenda(t,
        "Desempregada grávida tem salário-maternidade? Tem, se o parto acontecer no período de graça. Quem paga é o INSS. 👶",
        "Quem para de contribuir continua segurada por um tempo, o chamado período de graça. A regra geral é de 12 meses "
        "depois da última contribuição, e o prazo pode chegar a 36 meses. Se o parto acontecer dentro desse prazo, "
        "o pedido do salário-maternidade vai direto ao INSS, pelo Meu INSS ou pelo 135.",
        passos=["Confira a data da última contribuição no CNIS", "Guarde a rescisão e a carteira de trabalho",
                "Faça o pedido pelo Meu INSS a partir do parto"],
        alerta="Se a gravidez começou antes da demissão, existe também a estabilidade da gestante. É outra proteção.",
        fontes="Lei 8.213/1991, art. 15; Decreto 3.048/1999, art. 97.",
        convite="Salva e manda pra uma amiga grávida e sem emprego.",
        tags="#SalárioMaternidade #INSS #Gestante #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 8.213/1991, art. 15; Decreto 3.048/1999, art. 97.\n💬 Você conhecia o período de graça?")
t["frase"] = dict(
    html="Perder o emprego <em>não é perder a proteção</em> da maternidade.",
    legenda=legenda(t,
        "Desemprego não apaga as contribuições que você fez.",
        "No período de graça, a desempregada continua segurada e o INSS paga o salário-maternidade direto a ela.",
        convite="Manda pra uma gestante que está sem emprego.",
        tags="#SalárioMaternidade #Gestante #INSS #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 8.213/1991, art. 15.\n💬 Marca uma amiga que precisa saber disso.")
t["carrossel"] = dict(
    tag="Gestante", area="Previdenciário",
    capa=("Desempregada e grávida", "O INSS paga", "o seu salário-maternidade",
          'No período de graça, <span class="mt">você continua segurada</span>.', "Lei 8.213/1991"),
    itens=[
        ("Sem emprego,<br><em>com</em> direito", 'Quem para de contribuir segue segurada <span class="mt">no período de graça</span>.', "Lei 8.213/1991, art. 15"),
        ("Regra geral:<br><em>12 meses</em>", 'O prazo conta <span class="mt">depois da última contribuição</span>.', "Lei 8.213/1991, art. 15, II"),
        ("Pode chegar<br>a <em>36 meses</em>", '+12 com mais de 120 contribuições e +12 <span class="mt">com o desemprego comprovado</span>.', "Lei 8.213/1991, art. 15, §§ 1º e 2º"),
        ("Quem paga é<br>o <em>INSS</em>", 'Sem empresa, o pedido vai <span class="mt">direto ao INSS</span>, pelo Meu INSS ou no 135.', "Decreto 3.048/1999, art. 97"),
        ("Engravidou antes<br>da <em>demissão</em>?", "Aí entra a estabilidade da gestante, que é outra proteção. Separe:", "ADCT, art. 10, II, b"),
    ],
    checklist=["Carteira de trabalho e rescisão", "Extrato do CNIS", "Certidão de nascimento ou atestado"],
    fecho=("Desemprego <em>não apaga</em><br>o que você contribuiu.", "O INSS ainda protege você.", "mande para uma amiga grávida e sem emprego."),
    objetos=["corte-sapatinho.png", "corte-pasta.png", "corte-celular.png"], foto5=28259754,
    legenda=legenda(t,
        "Desempregada e grávida: o INSS paga o salário-maternidade no período de graça. Arrasta pro lado. 👶",
        "Quem deixa de contribuir continua segurada por 12 meses depois da última contribuição, prazo que pode chegar a 36 meses "
        "com mais de 120 contribuições e desemprego comprovado. Se o parto acontecer nesse período, o pedido vai direto ao INSS. "
        "Se a gravidez começou antes da demissão, há também a estabilidade da gestante.",
        faq=["Quanto tempo dura o período de graça? Em regra, 12 meses. Pode chegar a 36.",
             "Quem paga? O INSS, direto para você.",
             "Fui demitida grávida. E agora? Existe a estabilidade da gestante, que é outra proteção."],
        fontes="Lei 8.213/1991, art. 15; Decreto 3.048/1999, art. 97; ADCT, art. 10, II, b.",
        convite="Salva e manda pra uma amiga grávida e sem emprego.",
        tags="#SalárioMaternidade #INSS #Gestante #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 8.213/1991, art. 15; Decreto 3.048/1999, art. 97.\n💬 Você sabia que o prazo pode chegar a 36 meses?")

t = tema(chave="dona-de-casa-inss", data="2026-11-28", area="Previdenciário",
         titulo="Mãe dona de casa pode contribuir e se aposentar")
t["pergunta"] = dict(
    foto=8055797, pos="50% 40%", brilho=.92, area=PREV,
    html="Sou dona de casa e nunca trabalhei de carteira. <em>Posso me aposentar?</em>",
    legenda=legenda(t,
        "Dona de casa pode se aposentar pelo INSS? Pode, contribuindo como facultativa. Na baixa renda, são R$ 81,05 por mês em 2026. 🏠",
        "Quem cuida da casa e não tem renda própria pode contribuir como segurada facultativa. Se a família é de baixa renda, "
        "inscrita no CadÚnico e com renda de até 2 salários mínimos, a contribuição é de 5% do salário mínimo. "
        "Ela garante a aposentadoria por idade e protege em doença e maternidade.",
        passos=["Atualize o CadÚnico no CRAS", "Pague a guia com o código 1929", "Confira no Meu INSS se as contribuições foram validadas"],
        alerta="Os 5% não valem para aposentadoria por tempo de contribuição sem complementar a diferença.",
        fontes="Lei 8.212/1991, art. 21, §§ 2º e 4º.",
        convite="Salva e manda pra uma mãe que cuida da casa.",
        tags="#DonaDeCasa #INSS #Aposentadoria #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 8.212/1991, art. 21, §§ 2º e 4º.\n💬 Você conhecia a contribuição de baixa renda?")
t["frase"] = dict(
    html="Quem cuida da casa <em>também merece se aposentar.</em>",
    legenda=legenda(t,
        "Trabalho de casa não tem carteira assinada, mas pode ter aposentadoria.",
        "A dona de casa de baixa renda, inscrita no CadÚnico, contribui com 5% do salário mínimo: R$ 81,05 por mês em 2026.",
        convite="Manda pra uma mãe que dedicou a vida à família.",
        tags="#DonaDeCasa #INSS #Aposentadoria #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 8.212/1991, art. 21, § 2º, II, b.\n💬 Marca uma mulher que merece ler isso.")
t["carrossel"] = dict(
    tag="Dona de casa", area="Previdenciário",
    capa=("Dona de casa e INSS", "R$ 81,05", "por mês para garantir a aposentadoria",
          'A contribuição de baixa renda <span class="mt">protege quem cuida da casa</span>.', "Lei 8.212/1991"),
    itens=[
        ("Dona de casa<br><em>pode</em> contribuir", 'Quem não tem renda própria contribui <span class="mt">como segurada facultativa</span>.', "Lei 8.212/1991, art. 21"),
        ("Baixa renda:<br>só <em>5%</em>", '5% do salário mínimo: <span class="mt">R$ 81,05 por mês em 2026</span>.', "Lei 8.212/1991, art. 21, § 2º, II, b"),
        ("Precisa estar<br>no <em>CadÚnico</em>", 'Cadastro atualizado nos últimos 2 anos e <span class="mt">renda da família até 2 salários mínimos</span>.', "Lei 8.212/1991, art. 21, § 4º"),
        ("Garante a aposentadoria<br>por <em>idade</em>", '62 anos e 15 de contribuição. <span class="mt">Protege também na doença e na maternidade.</span>', "EC 103/2019"),
        ("Pague <em>certo</em><br>desde o início", "Guia com código errado pode não contar. Separe:", "Código 1929"),
    ],
    checklist=["Folha resumo do CadÚnico", "Número do NIT ou PIS", "Guias pagas com o código 1929"],
    fecho=("Trabalho de casa<br><em>também</em> é trabalho.", "E pode virar aposentadoria.", "mande para uma mãe que cuida da casa."),
    objetos=["corte-cofrinho.png", "corte-chaves.png", "corte-cafe.png"], foto5=3807113,
    legenda=legenda(t,
        "Dona de casa e INSS: com R$ 81,05 por mês em 2026, a mulher de baixa renda garante a aposentadoria por idade. Arrasta pro lado. 🏠",
        "A dona de casa sem renda própria, de família inscrita no CadÚnico e com renda de até 2 salários mínimos, contribui "
        "com 5% do salário mínimo. A contribuição dá direito à aposentadoria por idade e protege em doença e maternidade. "
        "Para aposentadoria por tempo de contribuição, é preciso complementar a diferença.",
        faq=["Quanto custa por mês? R$ 81,05 em 2026, na baixa renda.",
             "Quem pode? Quem não tem renda própria e tem CadÚnico atualizado, com renda familiar até 2 salários mínimos.",
             "Qual o código da guia? 1929."],
        fontes="Lei 8.212/1991, art. 21, §§ 2º e 4º; EC 103/2019.",
        convite="Salva e manda pra uma mãe que cuida da casa.",
        tags="#DonaDeCasa #INSS #Aposentadoria #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 8.212/1991, art. 21, §§ 2º e 4º.\n💬 Você conhece alguém que poderia contribuir assim?")

# ─────────────────────── Semana 5: fim de ano na família ───────────────────────

t = tema(chave="guarda-natal-ferias", data="2026-12-01", area="Família", mes="dezembro de 2026",
         titulo="Guarda compartilhada no Natal e nas férias")
t["pergunta"] = dict(
    foto=12969126, pos="50% 55%", brilho=.95, area=FAM,
    html="Temos guarda compartilhada. <em>Com quem o meu filho passa o Natal?</em>",
    legenda=legenda(t,
        "Na guarda compartilhada, com quem a criança passa o Natal? Vale o que está no acordo ou na decisão do juiz. 🎄",
        "Na guarda compartilhada, o tempo com o pai e com a mãe deve ser dividido com equilíbrio. Natal, Ano Novo e férias "
        "seguem o acordo ou a decisão. Quando não há regra, o comum é alternar as datas a cada ano. Viagem para o exterior "
        "com só um dos pais exige autorização do outro.",
        passos=["Leia o acordo ou a decisão da guarda", "Combine as datas por escrito, com antecedência",
                "Para viagem ao exterior, providencie a autorização"],
        faq=["Atraso na pensão permite impedir a convivência? Não. Pensão e convivência são questões separadas."],
        fontes="Código Civil, arts. 1.583, § 2º, e 1.589; ECA, art. 84.",
        convite="Salva e manda pra quem vai dividir as festas este ano.",
        tags="#GuardaCompartilhada #DireitoDeFamília #Natal #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Civil, arts. 1.583, § 2º, e 1.589; ECA, art. 84.\n💬 Na sua família, como fica o Natal das crianças?")
t["frase"] = dict(
    html="O Natal do seu filho <em>não pode virar disputa.</em>",
    legenda=legenda(t,
        "Fim de ano é a época em que mais aparecem conflitos de guarda.",
        "Natal, Ano Novo e férias seguem o acordo ou a decisão. Combinar as datas por escrito, com antecedência, evita a briga.",
        convite="Manda pra quem vai dividir as festas este ano.",
        tags="#GuardaCompartilhada #DireitoDeFamília #Natal #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Civil, art. 1.583, § 2º.\n💬 Deixa um 🎄 se você já combinou as datas.")
t["carrossel"] = dict(
    tag="Guarda compartilhada", area="Família",
    capa=("Guarda compartilhada", "Natal e férias", "com quem o seu filho fica",
          'Datas, viagens e pensão: <span class="mt">5 respostas para o fim de ano</span>.', "Código Civil"),
    itens=[
        ("Vale o que está<br>no <em>acordo</em>", 'Datas festivas e férias seguem <span class="mt">o acordo ou a decisão do juiz</span>.', "CC, art. 1.589"),
        ("Tempo de convívio<br><em>equilibrado</em>", 'Na guarda compartilhada, o tempo com o pai e a mãe <span class="mt">é dividido com equilíbrio</span>.', "CC, art. 1.583, § 2º"),
        ("Sem regra? O comum<br>é <em>alternar</em>", 'Natal com um, Ano Novo com o outro, <span class="mt">invertendo no ano seguinte</span>.', "Prática dos acordos"),
        ("Exterior pede<br><em>autorização</em>", 'Viajar para fora do país com um dos pais <span class="mt">exige autorização do outro</span>.', "ECA, art. 84"),
        ("Pensão e convivência<br>são <em>separadas</em>", "Atraso na pensão não autoriza impedir a convivência. Para organizar, separe:", "CC, art. 1.589"),
    ],
    checklist=["O acordo ou a decisão da guarda", "Datas combinadas por escrito", "Autorização de viagem, se houver"],
    fecho=("O centro de tudo<br>é <em>a criança</em>.", "As datas se organizam em volta dela.", "mande para quem vai dividir as festas."),
    objetos=["obj-ursinho2.png", "corte-chaves.png", "corte-celular.png"], foto5=4546012,
    legenda=legenda(t,
        "Guarda compartilhada no Natal e nas férias: com quem o seu filho fica? Arrasta pro lado e confere. 🎄",
        "O Código Civil manda dividir o tempo de convívio com equilíbrio na guarda compartilhada. As festas e as férias seguem "
        "o acordo ou a decisão do juiz. Sem regra escrita, o comum é alternar Natal e Ano Novo a cada ano. Viagem ao exterior "
        "com um dos pais pede autorização do outro.",
        faq=["Quem decide onde a criança passa o Natal? O acordo ou a decisão da guarda.",
             "Posso viajar com meu filho nas férias? Para o exterior, precisa da autorização do outro genitor.",
             "Se a pensão atrasar, posso suspender as visitas? Não. São questões separadas."],
        fontes="Código Civil, arts. 1.583, § 2º, e 1.589; ECA, art. 84.",
        convite="Salva e manda pra quem vai dividir as festas este ano.",
        tags="#GuardaCompartilhada #DireitoDeFamília #Natal #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Civil, arts. 1.583, § 2º, e 1.589; ECA, art. 84.\n💬 Vocês já combinaram as datas deste ano?")


# ───────────────────────── Mito ou Lei (19h, dias pares) ─────────────────────────
# (dia, tema, afirmação, veredito, explicação, base legal, hashtags, gestante?, trabalhista?, convite, pergunta do 1º comentário)
MITO_OU_LEI = [
    ("2026-11-04", "13-salario-2026", "Quem foi demitido não recebe 13º.", "MITO",
     "Na demissão sem justa causa ou no pedido de demissão, você recebe o 13º proporcional aos meses trabalhados. Só a justa causa tira esse direito.",
     "Lei 4.090/1962, art. 3º; Súmula 157 do TST", "#13Salário #MitoOuLei #DireitoTrabalhista #Rescisão #AdvogadaVitóriaES", False, True,
     "manda pra quem saiu do emprego este ano", "Você sabia que até quem pede demissão recebe o proporcional?"),
    ("2026-11-06", "13-salario-2026", "Atestado médico reduz o 13º.", "MITO",
     "Falta justificada não desconta do 13º. Se o afastamento passar de 15 dias, o INSS paga a parte desse período.",
     "Decreto 57.155/1965, art. 2º; Lei 8.213/1991, art. 40", "#13Salário #MitoOuLei #DireitoTrabalhista #Atestado #AdvogadaVitóriaES", False, True,
     "manda pra quem teve atestado este ano", "Você achava que atestado diminuía o 13º?"),
    ("2026-11-08", "13-salario-2026", "O 13º pode ser pago numa parcela só, em dezembro.", "MITO",
     "A 1ª parcela vence em 30/11. Pagar tudo de uma vez só vale se for até essa data.",
     "Lei 4.749/1965, arts. 1º e 2º", "#13Salário #MitoOuLei #DireitoTrabalhista #CLT #AdvogadaVitóriaES", False, True,
     "manda pra quem vai conferir o contracheque", "Na sua empresa, o 13º vem em uma ou duas parcelas?"),
    ("2026-11-10", "amamentacao-trabalho", "Gestante com estabilidade pode pedir demissão sozinha.", "MITO",
     "O pedido de demissão de quem tem estabilidade só vale com assistência do sindicato ou da autoridade do trabalho. Sem isso, pode ser anulado.",
     "CLT, art. 500", "#DireitosDaGestante #MitoOuLei #EstabilidadeGestante #DireitoTrabalhista #AdvogadaVitóriaES", True, True,
     "manda pra uma gestante que está pensando em pedir demissão", "Você sabia que o pedido precisa da assistência do sindicato?"),
    ("2026-11-12", "creche-empresa", "Aborto espontâneo dá direito a repouso remunerado.", "LEI",
     "Com atestado médico, a trabalhadora tem 2 semanas de repouso remunerado e volta para a mesma função.",
     "CLT, art. 395", "#DireitosDaMulher #MitoOuLei #GestanteCLT #DireitoTrabalhista #AdvogadaVitóriaES", True, True,
     "manda com carinho para quem pode precisar", "Você conhecia esse direito?"),
    ("2026-11-14", "gestante-insalubre", "A licença-maternidade pode começar antes do parto.", "LEI",
     "Com atestado médico, a licença pode começar até 28 dias antes do parto.",
     "CLT, art. 392, § 1º", "#LicençaMaternidade #MitoOuLei #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES", True, True,
     "manda pra uma gestante na reta final", "Você sabia que a licença pode começar antes?"),
    ("2026-11-16", "gestante-insalubre", "Pai não tem licença no nascimento do filho.", "MITO",
     "A licença-paternidade é de 5 dias, ou 20 dias em empresa do programa Empresa Cidadã. A partir de 2027, o prazo começa a aumentar.",
     "ADCT, art. 10, § 1º; Lei 11.770/2008; Lei 15.371/2026", "#LicençaPaternidade #MitoOuLei #Paternidade #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra um futuro papai", "Quantos dias de licença o pai teve na sua família?"),
    ("2026-11-18", "feriado-20-novembro", "Trabalhar no feriado é sempre hora extra de 50%.", "MITO",
     "Feriado trabalhado sem folga em outro dia é pago em dobro, e não com 50%.",
     "Lei 605/1949, art. 9º; Súmula 146 do TST", "#Feriado #MitoOuLei #ConsciênciaNegra #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem trabalha no dia 20", "Você vai trabalhar no feriado?"),
    ("2026-11-20", "racismo-trabalho", "Piada racista no trabalho é só brincadeira.", "MITO",
     "Ofensa por raça ou cor é injúria racial, crime com pena de 2 a 5 anos. Em tom de piada, a pena aumenta de 1/3 até a metade.",
     "Lei 7.716/1989, arts. 2º-A e 20-A", "#RacismoÉCrime #MitoOuLei #ConsciênciaNegra #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem ainda chama isso de brincadeira", "Deixa um ✊🏾 neste 20 de novembro."),
    ("2026-11-22", "alimentos-gravidicos", "A pensão da gravidez vira pensão do bebê depois do parto.", "LEI",
     "Com o nascimento, os alimentos gravídicos viram pensão alimentícia da criança, até que alguém peça revisão.",
     "Lei 11.804/2008, art. 6º, parágrafo único", "#AlimentosGravídicos #MitoOuLei #PensãoAlimentícia #DireitoDeFamília #AdvogadaVitóriaES", True, False,
     "manda pra uma amiga grávida", "Você sabia que a pensão continua depois do parto?"),
    ("2026-11-24", "aposentadoria-mulher-2026", "Quem nunca contribuiu não recebe nada do INSS.", "MITO",
     "O BPC paga um salário mínimo ao idoso a partir de 65 anos e à pessoa com necessidades especiais de família de baixa renda, sem exigir contribuição.",
     "Lei 8.742/1993, art. 20", "#BPC #MitoOuLei #INSS #DireitoPrevidenciário #AdvogadaVitóriaES", False, False,
     "manda pra quem acha que não tem direito a nada", "Você conhecia o BPC?"),
    ("2026-11-26", "desempregada-gravida-inss", "MEI tem salário-maternidade.", "LEI",
     "A MEI em dia com o INSS recebe 120 dias de salário-maternidade, no valor de um salário mínimo.",
     "Lei 8.213/1991, art. 71; STF, ADI 2110", "#SalárioMaternidade #MitoOuLei #MEI #DireitoPrevidenciário #AdvogadaVitóriaES", True, False,
     "manda pra uma MEI que está grávida", "Você sabia que a MEI também tem esse direito?"),
    ("2026-11-28", "dona-de-casa-inss", "Aposentada perde a pensão por morte.", "MITO",
     "Dá para receber os dois. O benefício de maior valor vem inteiro e o outro é pago com redução por faixas.",
     "EC 103/2019, art. 24, § 2º", "#PensãoPorMorte #MitoOuLei #Aposentadoria #DireitoPrevidenciário #AdvogadaVitóriaES", False, False,
     "manda pra uma aposentada que tem essa dúvida", "Você achava que precisava escolher um dos dois?"),
    ("2026-11-30", "13-salario-2026", "Hoje vence a 1ª parcela do 13º.", "LEI",
     "A 1ª parcela do 13º tem que ser paga até 30 de novembro. Confira o seu extrato hoje.",
     "Lei 4.749/1965, art. 2º", "#13Salário #MitoOuLei #DireitoTrabalhista #CLT #AdvogadaVitóriaES", False, True,
     "manda pra quem ainda não conferiu o extrato", "A sua 1ª parcela já caiu?"),
    ("2026-12-02", "guarda-natal-ferias", "Quem paga pensão pode levar o filho quando quiser.", "MITO",
     "A convivência segue o que foi combinado ou decidido pelo juiz. Pagar pensão não dá direito a mudar as datas sozinho.",
     "Código Civil, art. 1.589", "#GuardaCompartilhada #MitoOuLei #PensãoAlimentícia #DireitoDeFamília #AdvogadaVitóriaES", False, False,
     "manda pra quem vai organizar as festas", "Vocês já combinaram as datas do fim de ano?"),
]


def legenda_mito(m) -> tuple[str, str]:
    dia, _k, af, ver, ex, ref, tags, gest, trab, convite, pergunta = m
    selo = "❌ MITO!" if ver == "MITO" else "✅ É LEI!"
    tema_fake = {"gestante": gest, "trabalhista": trab, "mes": "dezembro de 2026" if dia >= "2026-12" else "novembro de 2026"}
    texto = (f"{selo} {af}\n\n{ex}\n\n📚 Fonte: {ref}.\n\n"
             f"🔖 Toda semana tem Mito ou Lei por aqui. Salva e {convite}.\n\n" + fecho_legenda(tema_fake, tags))
    pc = f"📚 Base legal: {ref}.\n💬 {pergunta}"
    return texto, pc


# Fontes conferidas em 09/10/2026 (planalto.gov.br, STF, STJ, TST e notícias oficiais): Leis 4.090/1962 e 4.749/1965
# (13º); Súmulas 45, 146 e 157 do TST; Decreto 57.155/1965; CLT arts. 389, 392, 394-A, 395, 396, 500; STF ADI 5938 e
# ADI 2110; Lei 14.457/2022 (reembolso-creche até 5a11m, canal de denúncia art. 23); Lei 14.759/2023; Lei 605/1949;
# Lei 10.101/2000 art. 6º-A; Lei 7.716/1989 arts. 2º-A e 20-A (Lei 14.532/2023); Lei 11.804/2008; EC 103/2019 arts.
# 15, 16, 18, 20, 24; Lei 8.213/1991 art. 15 e 72; Decreto 3.048/1999 art. 97 (Portaria Conjunta 50/2021); Lei
# 8.212/1991 art. 21 (5% = R$ 81,05 com mínimo de R$ 1.621); Lei 8.742/1993 art. 20; CC arts. 1.583 e 1.589; ECA art. 84;
# STJ Tema 192; Lei 15.371/2026 (licença-paternidade a partir de 2027).
