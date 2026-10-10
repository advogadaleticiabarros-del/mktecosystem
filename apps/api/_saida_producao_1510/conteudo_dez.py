"""Conteúdo do plano 03/12 a 31/12/2026 (docs/PLANO_CONTEUDO_DEZ_2026.md), aprovado pela Letícia em 10/10/2026.

Mesmo padrão de novembro (conteudo_nov.py): pergunta v6 12h, frase v2 15h, carrossel v5 Ouro editorial 18h nos
dias de tema; Mito ou Lei v3 19h nos dias pares. Regras de 10/10: mais pessoas negras nas fotos e cada objeto
ligado ao item do slide (1º objeto = item 01, 2º = item 02, 3º = item 03). Fatos conferidos em 10/10/2026.
"""
from conteudo_nov import FAM, PREV, TRAB, legenda, legenda_mito  # noqa: F401

DEZ = "dezembro de 2026"
TEMAS = []


def tema(**t):
    t.setdefault("mes", DEZ)
    TEMAS.append(t)
    return t


# ─────────────────────────── 03/12 · Dezembro Vermelho ───────────────────────────
t = tema(chave="hiv-trabalho", data="2026-12-03", area="Trabalhista", trabalhista=True,
         titulo="Dezembro Vermelho: HIV no trabalho (sigilo, demissão discriminatória, FGTS)")
t["pergunta"] = dict(foto=8680265, pos="50% 50%", brilho=.92, area=TRAB,
    html="Vivo com HIV. <em>Sou obrigada a contar para a empresa?</em>",
    legenda=legenda(t,
        "Quem vive com HIV precisa contar para a empresa? Não. Contar é uma escolha sua, e a lei protege o seu sigilo. 🎗️",
        "Ninguém é obrigado a revelar a condição no trabalho. A empresa não pode exigir teste de HIV na admissão, nos exames "
        "periódicos ou na demissão. Demitir alguém por viver com HIV é crime, e a Justiça do Trabalho presume que essa "
        "demissão é discriminatória.",
        faq=["Posso sacar o FGTS? Sim. Quem vive com HIV pode movimentar o FGTS sem sair do emprego.",
             "Fui demitida depois que souberam. E agora? A demissão é presumida discriminatória e pode gerar reintegração."],
        fontes="Lei 12.984/2014; Portaria MTE 1.246/2010; Súmula 443 do TST; Lei 8.036/1990, art. 20, XIII.",
        convite="Salva e manda pra quem precisa saber disso neste Dezembro Vermelho.",
        tags="#DezembroVermelho #HIV #Discriminação #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 12.984/2014; Portaria MTE 1.246/2010; Súmula 443 do TST.\n💬 Você sabia que o teste de HIV na admissão é proibido?")
t["frase"] = dict(html="Viver com HIV não tira direitos. <em>O preconceito é que é crime.</em>",
    legenda=legenda(t,
        "Dezembro Vermelho é o mês de lembrar que viver com HIV não muda os seus direitos no trabalho.",
        "Sigilo garantido, teste proibido na admissão e demissão discriminatória punida como crime: está na lei.",
        convite="Manda pra quem precisa ouvir isso hoje.",
        tags="#DezembroVermelho #HIV #Respeito #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 12.984/2014.\n💬 Deixa um ❤️ pelo Dezembro Vermelho.")
t["carrossel"] = dict(tag="Dezembro Vermelho", area="Trabalhista",
    capa=("HIV no trabalho", "Sigilo", "e respeito: 5 direitos",
          'A lei protege quem vive com HIV <span class="mt">do primeiro ao último dia</span> de trabalho.', "Lei 12.984/2014"),
    itens=[
        ("Contar é <em>escolha</em><br>sua", 'Ninguém é obrigado a revelar a condição <span class="mt">para a empresa ou para colegas</span>.', "Lei 12.984/2014"),
        ("Teste de HIV<br>é <em>proibido</em>", 'A empresa não pode exigir o teste na admissão, <span class="mt">nos exames periódicos ou na demissão</span>.', "Portaria MTE 1.246/2010"),
        ("Demitir por HIV<br>é <em>crime</em>", 'Pena de 1 a 4 anos. E a Justiça <span class="mt">presume discriminatória</span> essa demissão.', "Lei 12.984/2014; Súmula 443 do TST"),
        ("O FGTS pode<br>ser <em>sacado</em>", 'Quem vive com HIV pode movimentar o FGTS <span class="mt">sem precisar sair do emprego</span>.', "Lei 8.036/1990, art. 20, XIII"),
        ("Sofreu discriminação?<br><em>Registre</em>", "Guarde tudo e separe:", ""),
    ],
    checklist=["Mensagens e comentários recebidos", "Datas, nomes e testemunhas", "Documentos da demissão"],
    fecho=("Viver com HIV<br><em>não tira</em> direitos.", "O preconceito é que é crime.", "mande para quem precisa saber disso."),
    objetos=["obj-envelope.png", "corte-estetoscopio.png", "corte-martelo.png"], foto5=8385158,
    legenda=legenda(t,
        "Dezembro Vermelho: quem vive com HIV tem direito ao sigilo no trabalho, e demitir por isso é crime. Arrasta pro lado. 🎗️",
        "A Lei 12.984/2014 tornou crime negar emprego ou demitir alguém por viver com HIV. A empresa não pode exigir o teste em "
        "nenhum exame do trabalho, a Justiça presume discriminatória a demissão e o FGTS pode ser sacado sem sair do emprego.",
        faq=["Preciso contar que tenho HIV? Não. É uma escolha sua.",
             "A empresa pode pedir o teste? Não, em nenhum exame ocupacional.",
             "Posso sacar o FGTS? Sim, sem precisar sair do emprego."],
        fontes="Lei 12.984/2014; Portaria MTE 1.246/2010; Súmula 443 do TST; Lei 8.036/1990, art. 20, XIII.",
        convite="Salva e manda pra quem precisa saber disso.",
        tags="#DezembroVermelho #HIV #Discriminação #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 12.984/2014; Portaria MTE 1.246/2010; Súmula 443 do TST; Lei 8.036/1990, art. 20, XIII.\n💬 Qual desses direitos você não conhecia?")

# ─────────────────────────── 05/12 · Abolição da Escravidão (02/12) ───────────────────────────
t = tema(chave="trabalho-escravo", data="2026-12-05", area="Trabalhista", trabalhista=True,
         titulo="Trabalho escravo hoje: jornada exaustiva, dívida e o caso das domésticas")
t["pergunta"] = dict(foto=6196566, pos="50% 55%", brilho=.9, area=TRAB,
    html="Trabalho numa casa de família sem folga e sem salário certo. <em>Isso é trabalho escravo?</em>",
    legenda=legenda(t,
        "Trabalhar sem folga, sem salário e sem poder sair é trabalho escravo? Pode ser, e é crime. ⛓️",
        "O Código Penal chama de trabalho análogo à escravidão o trabalho forçado, a jornada exaustiva, as condições degradantes "
        "ou a dívida que prende a pessoa ao emprego. O trabalho doméstico é um dos setores com mais casos. A empregada doméstica "
        "tem direito a salário mínimo, jornada de 44 horas, folga semanal, férias e FGTS.",
        faq=["Como denunciar? Pelo Sistema Ipê, na internet, de forma sigilosa, ou pelo Disque 100.",
             "Qual é a pena? De 2 a 8 anos de reclusão, além de multa."],
        fontes="Código Penal, art. 149; Lei Complementar 150/2015.",
        convite="Salva e manda pra quem pode precisar de ajuda.",
        tags="#TrabalhoEscravo #TrabalhoDoméstico #DireitosHumanos #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Penal, art. 149; Lei Complementar 150/2015.\n💬 Você sabia que a denúncia pode ser feita em sigilo?")
t["frase"] = dict(html="Trabalho sem liberdade <em>tem nome: é crime.</em>",
    legenda=legenda(t,
        "A escravidão foi abolida em 1888, mas o trabalho escravo ainda aparece, inclusive dentro de casas de família.",
        "Jornada exaustiva, condições degradantes ou dívida que prende a pessoa ao emprego são crime, com pena de 2 a 8 anos.",
        convite="Manda pra quem precisa saber que dá pra denunciar em sigilo.",
        tags="#TrabalhoEscravo #DireitosHumanos #TrabalhoDoméstico #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Penal, art. 149.\n💬 Denúncia sigilosa: Sistema Ipê ou Disque 100.")
t["carrossel"] = dict(tag="Trabalho escravo", area="Trabalhista",
    capa=("Trabalho escravo hoje", "Não acabou", "os sinais e como denunciar",
          'É crime, com pena de <span class="mt">2 a 8 anos de reclusão</span>.', "Código Penal, art. 149"),
    itens=[
        ("Trabalho <em>forçado</em>", 'Trabalhar sob ameaça, sem poder sair <span class="mt">ou com documentos retidos</span>.', "Código Penal, art. 149"),
        ("Jornada<br><em>exaustiva</em>", 'Horas que tiram a saúde, o descanso <span class="mt">e o convívio com a família</span>.', "Código Penal, art. 149"),
        ("Dívida que<br><em>prende</em>", 'Cobrar "dívidas" para impedir a pessoa <span class="mt">de ir embora</span>.', "Código Penal, art. 149"),
        ("Condições<br><em>degradantes</em>", 'Sem salário, sem comida adequada, <span class="mt">sem lugar digno para dormir</span>.', "Código Penal, art. 149"),
        ("Denuncie<br>em <em>sigilo</em>", "Não precisa dizer seu nome. Canais:", ""),
    ],
    checklist=["Sistema Ipê (internet, sigiloso)", "Disque 100", "Ministério Público do Trabalho"],
    fecho=("A escravidão foi<br><em>abolida</em>.", "Quem explora responde por crime.", "mande para quem precisa de ajuda."),
    objetos=["corte-chaves.png", "corte-ampulheta.png", "corte-reais.png"], foto5=6197042,
    legenda=legenda(t,
        "Trabalho escravo hoje: jornada exaustiva, dívida que prende e condições degradantes são crime. Arrasta pro lado. ⛓️",
        "O art. 149 do Código Penal pune com 2 a 8 anos de reclusão quem reduz alguém a condição análoga à de escravo. "
        "Basta uma das situações: trabalho forçado, jornada exaustiva, condições degradantes ou restrição de ir embora por dívida. "
        "No trabalho doméstico, os casos cresceram nos últimos anos.",
        faq=["Precisa de corrente para ser trabalho escravo? Não. Jornada exaustiva ou condições degradantes já bastam.",
             "Como denuncio? Sistema Ipê, Disque 100 ou Ministério Público do Trabalho, com sigilo.",
             "Doméstica que dorme no emprego tem folga? Tem: descanso semanal e jornada de 44 horas."],
        fontes="Código Penal, art. 149; Lei Complementar 150/2015.",
        convite="Salva e manda pra quem pode precisar de ajuda.",
        tags="#TrabalhoEscravo #TrabalhoDoméstico #DireitosHumanos #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Penal, art. 149; Lei Complementar 150/2015.\n💬 Você sabia que jornada exaustiva também caracteriza o crime?")

# ─────────────────────────── 08/12 · Burnout ───────────────────────────
t = tema(chave="burnout-trabalho", data="2026-12-08", area="Trabalhista", trabalhista=True,
         titulo="Burnout é doença do trabalho: afastamento e 12 meses de estabilidade")
t["pergunta"] = dict(foto=30149853, pos="50% 50%", brilho=.95, area=TRAB,
    html="O médico disse que estou com burnout. <em>Posso me afastar pelo INSS?</em>",
    legenda=legenda(t,
        "Burnout dá direito a afastamento pelo INSS? Dá, quando a incapacidade passa de 15 dias. E pode gerar estabilidade. 🔋",
        "Desde 2023, o burnout está na lista oficial de doenças relacionadas ao trabalho. Os primeiros 15 dias de afastamento são "
        "pagos pela empresa; depois, pelo INSS. Se ficar provada a relação com o trabalho, o benefício é acidentário e, na volta, "
        "você tem 12 meses de estabilidade.",
        faq=["O que é a CAT? A Comunicação de Acidente de Trabalho. Se a empresa não emitir, o médico ou o sindicato podem.",
             "A lista basta? Não. É preciso provar a relação com o trabalho no seu caso."],
        fontes="Portaria GM/MS 1.999/2023; Lei 8.213/1991, arts. 22, 60 e 118.",
        convite="Salva e manda pra quem está no limite.",
        tags="#Burnout #SaúdeMental #INSS #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Portaria GM/MS 1.999/2023; Lei 8.213/1991, art. 118.\n💬 Você sabia que o burnout está na lista de doenças do trabalho?")
t["frase"] = dict(html="Adoecer pelo trabalho <em>não é fraqueza.</em>",
    legenda=legenda(t,
        "Fim de ano é quando muita gente chega ao limite. O burnout é doença, e doença do trabalho gera direitos.",
        "Afastamento pelo INSS depois de 15 dias e, com a relação provada, 12 meses de estabilidade na volta.",
        convite="Manda pra quem está precisando ouvir isso.",
        tags="#Burnout #SaúdeMental #DireitoTrabalhista #INSS #AdvogadaVitóriaES"),
    pc="📚 Base legal: Portaria GM/MS 1.999/2023.\n💬 Deixa um 💛 para quem está cansada demais.")
t["carrossel"] = dict(tag="Saúde mental", area="Trabalhista",
    capa=("Burnout", "É doença", "do trabalho: 5 direitos",
          'Afastamento, INSS e <span class="mt">12 meses de estabilidade</span>.', "Portaria GM/MS 1.999/2023"),
    itens=[
        ("Está na lista<br>de doenças <em>do trabalho</em>", 'O Ministério da Saúde incluiu o burnout em 2023. <span class="mt">O caso ainda precisa de prova.</span>', "Portaria GM/MS 1.999/2023"),
        ("Depois de 15 dias,<br>paga o <em>INSS</em>", 'Os primeiros 15 dias são da empresa; <span class="mt">depois, o INSS paga o benefício</span>.', "Lei 8.213/1991, art. 60"),
        ("Peça a <em>CAT</em>", 'Ela liga a doença ao emprego. <span class="mt">Se a empresa negar, o médico ou o sindicato emitem.</span>', "Lei 8.213/1991, art. 22"),
        ("<em>12 meses</em><br>de estabilidade", 'Depois do benefício acidentário, <span class="mt">não pode haver demissão sem justa causa</span> por 12 meses.', "Lei 8.213/1991, art. 118"),
        ("Prove a <em>ligação</em><br>com o trabalho", "É a parte decisiva. Separe:", ""),
    ],
    checklist=["Laudo do psiquiatra ou psicólogo", "Mensagens de cobrança fora de hora", "Registro de jornada e metas"],
    fecho=("Descanso <em>não é</em><br>fraqueza.", "Adoecer pelo trabalho gera direitos.", "mande para quem está no limite."),
    objetos=["corte-estetoscopio.png", "corte-ampulheta.png", "corte-prancheta.png"], foto5=8374457,
    legenda=legenda(t,
        "Burnout é doença do trabalho: afastamento pelo INSS e 12 meses de estabilidade. Arrasta pro lado. 🔋",
        "A Portaria GM/MS 1.999/2023 incluiu a síndrome de burnout na lista de doenças relacionadas ao trabalho. Com afastamento "
        "acima de 15 dias, o INSS paga o benefício; provada a relação com o trabalho e emitida a CAT, o benefício é acidentário "
        "e garante 12 meses de estabilidade depois da volta.",
        faq=["Burnout é doença do trabalho? Está na lista oficial, mas cada caso precisa de prova.",
             "Quem emite a CAT? A empresa; se ela não emitir, o médico, o sindicato ou a própria trabalhadora.",
             "Tenho estabilidade? 12 meses depois do fim do benefício acidentário."],
        fontes="Portaria GM/MS 1.999/2023; Lei 8.213/1991, arts. 22, 60 e 118.",
        convite="Salva e manda pra quem está no limite.",
        tags="#Burnout #SaúdeMental #INSS #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Portaria GM/MS 1.999/2023; Lei 8.213/1991, arts. 22, 60 e 118.\n💬 Sua empresa fala de saúde mental?")

# ─────────────────────────── 10/12 · Direitos Humanos ───────────────────────────
t = tema(chave="assedio-moral", data="2026-12-10", area="Trabalhista", trabalhista=True,
         titulo="Direitos Humanos no trabalho: assédio moral, exemplos e como provar")
t["pergunta"] = dict(foto=9301304, pos="50% 40%", brilho=.92, area=TRAB,
    html="Meu chefe me humilha na frente da equipe. <em>Isso é assédio moral?</em>",
    legenda=legenda(t,
        "Chefe que humilha na frente da equipe pratica assédio moral? Pode praticar, e a empresa responde por isso. 🕊️",
        "Assédio moral é a exposição a situações humilhantes no trabalho: gritos, xingamentos, isolamento, cobranças para "
        "constranger. Ele gera indenização por dano moral e, nos casos graves, permite a rescisão indireta, em que você sai "
        "com todas as verbas. A empresa responde pelos atos dos chefes.",
        passos=["Anote cada episódio com data e quem viu", "Guarde prints, áudios e e-mails", "Use o canal de denúncia da empresa"],
        fontes="CLT, art. 483; Código Civil, art. 932, III.",
        convite="Salva e manda pra quem está passando por isso.",
        tags="#AssédioMoral #DireitosHumanos #SaúdeMental #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 483; Código Civil, art. 932, III.\n💬 Você já viu alguém ser humilhado no trabalho?")
t["frase"] = dict(html="Humilhação <em>não faz parte do salário.</em>",
    legenda=legenda(t,
        "No Dia Internacional dos Direitos Humanos, um lembrete: dignidade também vale no trabalho.",
        "Gritos, xingamentos e exposição podem ser assédio moral e geram indenização. A empresa responde pelos chefes.",
        convite="Manda pra quem precisa ouvir isso hoje.",
        tags="#DireitosHumanos #AssédioMoral #DireitoTrabalhista #Respeito #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 483.\n💬 Deixa um 🕊️ pelo Dia dos Direitos Humanos.")
t["carrossel"] = dict(tag="Direitos Humanos", area="Trabalhista",
    capa=("Assédio moral no trabalho", "Dignidade", "também no trabalho: 5 respostas",
          'Humilhação, isolamento e gritos <span class="mt">têm consequência</span>.', "CLT, art. 483"),
    itens=[
        ("Humilhar em público<br><em>não é</em> jeito do chefe", 'Gritos, xingamentos e exposição <span class="mt">podem caracterizar assédio moral</span>.', "CLT, art. 483"),
        ("Isolar e<br><em>esvaziar</em> a função", 'Tirar tarefas, ignorar e excluir de reuniões <span class="mt">também é forma de assédio</span>.', "CLT, art. 483"),
        ("A empresa<br><em>responde</em>", 'O empregador responde pelos atos <span class="mt">dos chefes e dos colegas</span>.', "Código Civil, art. 932, III"),
        ("Pode sair<br>com <em>tudo</em>", 'Assédio grave permite a rescisão indireta, <span class="mt">com as verbas da demissão sem justa causa</span>.', "CLT, art. 483"),
        ("Prove com<br><em>calma</em>", "Anote tudo, com datas. Separe:", ""),
    ],
    checklist=["Prints, áudios e e-mails", "Nomes de quem presenciou", "Atestados e laudos, se adoeceu"],
    fecho=("Trabalho é <em>lugar</em><br>de respeito.", "Humilhação não faz parte do salário.", "mande para quem está passando por isso."),
    objetos=["corte-celular.png", "obj-cadeira.png", "corte-martelo.png"], foto5=6632537,
    legenda=legenda(t,
        "Assédio moral no trabalho: humilhação, isolamento e gritos têm consequência. Arrasta pro lado e veja como provar. 🕊️",
        "Assédio moral é expor a trabalhadora a situações humilhantes e constrangedoras. Pode gerar indenização, permite a rescisão "
        "indireta nos casos graves e a empresa responde pelos atos dos chefes e colegas. A prova se faz com anotações, prints, "
        "áudios e testemunhas.",
        faq=["Grito do chefe é assédio? Humilhação e exposição podem ser.",
             "Posso sair e receber tudo? Nos casos graves, pela rescisão indireta.",
             "Como provo? Anotações com data, prints, áudios e testemunhas."],
        fontes="CLT, art. 483; Código Civil, art. 932, III; Lei 14.457/2022.",
        convite="Salva e manda pra quem está passando por isso.",
        tags="#AssédioMoral #DireitosHumanos #SaúdeMental #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, art. 483; Código Civil, art. 932, III.\n💬 Qual desses sinais você já viu acontecer?")

# ─────────────────────────── 12/12 · Festa da firma ───────────────────────────
t = tema(chave="festa-da-firma", data="2026-12-12", area="Trabalhista", trabalhista=True,
         titulo="Festa da firma: assédio sexual é crime, inclusive na confraternização")
t["pergunta"] = dict(foto=5834736, pos="50% 45%", brilho=.9, area=TRAB,
    html="Na festa da empresa, um colega passou a mão em mim. <em>O que eu faço?</em>",
    legenda=legenda(t,
        "Colega que passa a mão em você na festa da empresa comete crime? Sim. Toque sem consentimento é importunação sexual. 🥂",
        "Tocar alguém com conotação sexual sem consentimento é importunação sexual, com pena de 1 a 5 anos. Se quem constrange usa "
        "o cargo para obter favor sexual, é assédio sexual. A empresa responde pelo que acontece nos eventos que ela promove e "
        "precisa ter canal de denúncia.",
        passos=["Registre um boletim de ocorrência", "Anote nomes de quem viu", "Denuncie no canal da empresa"],
        fontes="Código Penal, arts. 215-A e 216-A; Lei 14.457/2022, art. 23.",
        convite="Salva e manda pras colegas antes da festa.",
        tags="#AssédioSexual #FestaDaFirma #DireitosDaMulher #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Penal, arts. 215-A e 216-A; Lei 14.457/2022.\n💬 Sua empresa tem canal de denúncia?")
t["frase"] = dict(html="Festa da firma <em>não é passe livre.</em>",
    legenda=legenda(t,
        "Confraternização de fim de ano não suspende o respeito.",
        "Toque sem consentimento é importunação sexual, e usar o cargo para constranger é assédio sexual. Os dois são crime.",
        convite="Manda pras colegas antes da festa.",
        tags="#AssédioSexual #FestaDaFirma #DireitosDaMulher #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Penal, arts. 215-A e 216-A.\n💬 Marca uma colega que vai à festa.")
t["carrossel"] = dict(tag="Festa da firma", area="Trabalhista",
    capa=("Festa da firma", "Limite", "assédio na confraternização é crime",
          'Respeito vale <span class="mt">também depois do expediente</span>.', "Código Penal, art. 216-A"),
    itens=[
        ("Na festa,<br>a regra <em>continua</em>", 'O que acontece no evento da empresa <span class="mt">pode gerar responsabilidade dela</span>.', "Código Civil, art. 932, III"),
        ("Toque sem<br>consentimento é <em>crime</em>", 'Importunação sexual: <span class="mt">pena de 1 a 5 anos de reclusão</span>.', "Código Penal, art. 215-A"),
        ("Chefe que cobra<br>favor é <em>assédio</em>", 'Usar o cargo para constranger com fins sexuais <span class="mt">é assédio sexual</span>.', "Código Penal, art. 216-A"),
        ("A empresa tem<br><em>dever</em> de agir", 'Empresas com CIPA precisam de canal de denúncia <span class="mt">e de medidas contra o assédio</span>.', "Lei 14.457/2022, art. 23"),
        ("Aconteceu?<br><em>Registre</em>", "Você não precisa resolver sozinha. Separe:", ""),
    ],
    checklist=["Boletim de ocorrência", "Nomes de quem viu", "Denúncia no canal da empresa"],
    fecho=("Festa <em>não é</em><br>passe livre.", "Respeito vale o ano inteiro.", "mande para as colegas antes da festa."),
    objetos=["obj-declaracao.png", "corte-martelo.png", "corte-pasta.png"], foto5=6518876,
    legenda=legenda(t,
        "Festa da firma: assédio e importunação sexual na confraternização são crime. Arrasta pro lado. 🥂",
        "Tocar alguém com conotação sexual sem consentimento é importunação sexual (1 a 5 anos). Usar o cargo para constranger "
        "com fins sexuais é assédio sexual. A empresa responde pelo que acontece nos eventos que promove e, se tem CIPA, precisa "
        "manter canal de denúncia.",
        faq=["Na festa vale a mesma regra? Vale. E a empresa pode responder.",
             "Qual a diferença entre importunação e assédio? Assédio envolve o uso do cargo.",
             "O que fazer? Boletim de ocorrência, testemunhas e o canal da empresa."],
        fontes="Código Penal, arts. 215-A e 216-A; Código Civil, art. 932, III; Lei 14.457/2022, art. 23.",
        convite="Salva e manda pras colegas antes da festa.",
        tags="#AssédioSexual #FestaDaFirma #DireitosDaMulher #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Penal, arts. 215-A e 216-A; Lei 14.457/2022.\n💬 Sua empresa já falou sobre isso antes da festa?")

# ─────────────────────────── 15/12 · 2ª parcela do 13º ───────────────────────────
t = tema(chave="13-segunda-parcela", data="2026-12-15", area="Trabalhista", trabalhista=True,
         titulo="2ª parcela do 13º: prazo 18/12, descontos e o que fazer se não pagarem")
t["pergunta"] = dict(foto=30005563, pos="50% 50%", brilho=.92, area=TRAB,
    html="A 2ª parcela do meu 13º veio bem menor. <em>Está certo?</em>",
    legenda=legenda(t,
        "Por que a 2ª parcela do 13º vem menor? Porque todos os descontos de INSS e imposto de renda ficam nela. 🎁",
        "A 2ª parcela é o 13º inteiro, menos o que você já recebeu na 1ª parcela, menos o INSS e o imposto de renda calculados "
        "sobre o valor total. Por isso ela costuma ser menor que a 1ª. Em 2026, o prazo é sexta, 18 de dezembro, porque o dia 20 "
        "cai num domingo.",
        faq=["Pensão desconta do 13º? Se for percentual do salário, sim.",
             "E se não pagarem até 18/12? A empresa pode ser multada, e o valor pode ser cobrado."],
        fontes="Lei 4.749/1965; Lei 7.855/1989, art. 3º; STJ, Tema 192.",
        convite="Salva pra conferir o contracheque e manda pra quem estranhou o valor.",
        tags="#13Salário #DécimoTerceiro #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.749/1965.\n💬 A sua 2ª parcela já caiu?")
t["frase"] = dict(html="Entender o contracheque <em>também é proteger o seu dinheiro.</em>",
    legenda=legenda(t,
        "A 2ª parcela do 13º sai até 18/12 e vem com os descontos. Conferir é direito seu.",
        "13º total, menos a 1ª parcela, menos INSS e imposto de renda: essa é a conta. Se não fechar, pergunte ao RH por escrito.",
        convite="Manda pra quem ainda não entendeu o desconto.",
        tags="#13Salário #DécimoTerceiro #DireitoTrabalhista #FinançasPessoais #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.749/1965.\n💬 Marca quem precisa conferir o contracheque.")
t["carrossel"] = dict(tag="13º salário", area="Trabalhista",
    capa=("13º salário", "2ª parcela", "por que ela vem menor",
          'Prazo em 2026: <span class="mt">sexta, 18 de dezembro</span>.', "Lei 4.749/1965"),
    itens=[
        ("Prazo:<br>até <em>18/12</em>", 'O limite legal é 20/12, um domingo em 2026: <span class="mt">o pagamento vem antes</span>.', "Lei 4.749/1965, art. 1º"),
        ("Os descontos<br>vêm <em>todos</em> aqui", 'INSS e IR são calculados sobre o 13º inteiro <span class="mt">e descontados só na 2ª parcela</span>.', "Lei 4.749/1965"),
        ("A conta<br>é <em>simples</em>", '13º total, menos a 1ª parcela, <span class="mt">menos INSS e IR</span>.', "Lei 4.749/1965"),
        ("Pensão também<br><em>pode</em> descontar", 'Se a pensão é percentual do salário, <span class="mt">ela incide sobre o 13º</span>.', "STJ, Tema 192"),
        ("Não pagaram?<br><em>Confira</em>", "Atraso pode gerar multa à empresa. Separe:", "Lei 7.855/1989, art. 3º"),
    ],
    checklist=["Contracheques de novembro e dezembro", "Média de horas extras e adicionais", "Extrato com a data do depósito"],
    fecho=("Conferir o 13º<br><em>é direito</em>.", "Pergunte ao RH por escrito.", "mande para quem estranhou o desconto."),
    objetos=["corte-ampulheta.png", "corte-calculadora.png", "corte-reais.png"], foto5=35725804,
    legenda=legenda(t,
        "2ª parcela do 13º: prazo até 18/12 e todos os descontos ficam nela. Arrasta pro lado. 🎁",
        "A 2ª parcela é o 13º total menos a 1ª parcela, menos INSS e imposto de renda calculados sobre o 13º inteiro. "
        "Em 2026 o prazo é sexta, 18/12, porque o dia 20 cai num domingo. Pensão em percentual do salário também incide.",
        faq=["Por que a 2ª parcela é menor? Porque os descontos ficam todos nela.",
             "Qual o prazo? 18/12 em 2026.",
             "A empresa atrasou. E agora? Pode ser multada, e o valor pode ser cobrado."],
        fontes="Lei 4.749/1965; Lei 7.855/1989, art. 3º; STJ, Tema 192.",
        convite="Salva pra conferir o contracheque e manda pra uma colega.",
        tags="#13Salário #DécimoTerceiro #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 4.749/1965; Lei 7.855/1989, art. 3º.\n💬 Sua 2ª parcela veio do jeito que você esperava?")

# ─────────────────────────── 17/12 · Temporária de fim de ano ───────────────────────────
t = tema(chave="temporaria-fim-de-ano", data="2026-12-17", area="Trabalhista", trabalhista=True, gestante=True,
         titulo="Temporária de fim de ano: direitos e estabilidade da gestante (TST 2026)")
t["pergunta"] = dict(foto=5868733, pos="50% 50%", brilho=.92, area=TRAB,
    html="Fui contratada só para o fim de ano. <em>Tenho os mesmos direitos?</em>",
    legenda=legenda(t,
        "Temporária de fim de ano tem os mesmos direitos? Tem salário igual ao da equipe, FGTS, 13º e férias proporcionais. 🛍️",
        "O trabalho temporário, contratado por agência, é regido pela Lei 6.019/1974. Ele garante salário equivalente ao de quem "
        "faz a mesma função, jornada de 8 horas com hora extra paga, FGTS, 13º e férias proporcionais. E desde março de 2026 o "
        "TST reconhece a estabilidade da gestante também no temporário.",
        faq=["Quanto tempo pode durar? Até 180 dias, prorrogáveis por mais 90.",
             "Engravidei durante o contrato. E agora? O TST passou a reconhecer a estabilidade no temporário em 2026."],
        fontes="Lei 6.019/1974, arts. 10 e 12; TST Pleno, processo 1000059-12.2020.5.02.0382.",
        convite="Salva e manda pra quem pegou vaga de fim de ano.",
        tags="#TrabalhoTemporário #FimDeAno #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 6.019/1974, arts. 10 e 12.\n💬 Você já trabalhou como temporária no fim de ano?")
t["frase"] = dict(html="Contrato curto <em>não diminui direitos.</em>",
    legenda=legenda(t,
        "Vaga de fim de ano também tem lei.",
        "Salário igual ao da equipe, FGTS, 13º e férias proporcionais. E a gestante temporária tem estabilidade desde março de 2026.",
        convite="Manda pra quem começou num temporário este mês.",
        tags="#TrabalhoTemporário #FimDeAno #DireitoTrabalhista #DireitosDaGestante #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 6.019/1974.\n💬 Marca quem está trabalhando no comércio este fim de ano.")
t["carrossel"] = dict(tag="Fim de ano", area="Trabalhista",
    capa=("Temporária de fim de ano", "5 direitos", "de quem foi contratada para o Natal",
          'Do salário ao FGTS, <span class="mt">e a gestante tem estabilidade</span>.', "Lei 6.019/1974"),
    itens=[
        ("Salário <em>igual</em><br>ao da equipe", 'Remuneração equivalente à de quem faz <span class="mt">a mesma função na empresa</span>.', "Lei 6.019/1974, art. 12"),
        ("<em>FGTS</em> e<br>13º proporcional", 'O temporário tem FGTS depositado <span class="mt">e 13º proporcional aos meses</span>.', "Lei 6.019/1974; Lei 8.036/1990"),
        ("Hora extra<br><em>é paga</em>", 'Jornada de 8 horas; o que passar <span class="mt">é hora extra com adicional</span>.', "Lei 6.019/1974, art. 12"),
        ("Grávida no temporário<br><em>tem estabilidade</em>", 'Desde março de 2026, o TST reconhece <span class="mt">a estabilidade também no temporário</span>.', "TST Pleno, mar/2026"),
        ("Guarde o<br><em>contrato</em>", "No fim do contrato, confira:", "Lei 6.019/1974, art. 10"),
    ],
    checklist=["Contrato com a agência", "Recibos de pagamento", "Extrato do FGTS"],
    fecho=("Temporário <em>não é</em><br>sem direito.", "A lei vale do primeiro ao último dia.", "mande para quem pegou vaga de fim de ano."),
    objetos=["corte-reais.png", "corte-cofrinho.png", "corte-ampulheta.png"], foto5=5832580,
    legenda=legenda(t,
        "Temporária de fim de ano: salário igual, FGTS, 13º e férias proporcionais, e estabilidade da gestante. Arrasta pro lado. 🛍️",
        "A Lei 6.019/1974 garante ao temporário salário equivalente ao dos empregados da mesma função, jornada de 8 horas, hora "
        "extra, FGTS e direitos proporcionais. O contrato vai até 180 dias, prorrogáveis por mais 90. Em março de 2026, o TST "
        "passou a reconhecer a estabilidade da gestante também no trabalho temporário.",
        faq=["Temporário tem FGTS? Tem.",
             "Recebo 13º? Proporcional aos meses trabalhados.",
             "Grávida no temporário tem estabilidade? Desde março de 2026, o TST reconhece."],
        fontes="Lei 6.019/1974, arts. 10 e 12; Lei 8.036/1990; TST Pleno, mar/2026.",
        convite="Salva e manda pra quem pegou vaga de fim de ano.",
        tags="#TrabalhoTemporário #FimDeAno #DireitosDaGestante #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 6.019/1974, arts. 10 e 12; TST Pleno, mar/2026.\n💬 Qual desses direitos você não conhecia?")

# ─────────────────────────── 19/12 · Férias coletivas ───────────────────────────
t = tema(chave="ferias-coletivas", data="2026-12-19", area="Trabalhista", trabalhista=True,
         titulo="Férias coletivas de fim de ano: as regras")
t["pergunta"] = dict(foto=8185804, pos="50% 50%", brilho=.95, area=TRAB,
    html="A empresa deu férias coletivas e eu tenho só 6 meses de casa. <em>Como fica?</em>",
    legenda=legenda(t,
        "Férias coletivas com menos de 1 ano de empresa? Você tira férias proporcionais e começa um novo período. 🏖️",
        "Quem tem menos de 12 meses de casa entra nas férias coletivas recebendo férias proporcionais aos meses trabalhados, com "
        "o terço constitucional, e a partir daí começa a contar um novo período aquisitivo. As férias coletivas podem ser em até "
        "2 períodos no ano, nenhum com menos de 10 dias.",
        faq=["A empresa precisa avisar? Sim: Ministério do Trabalho e sindicato, com 15 dias de antecedência.",
             "Quando recebo? Até 2 dias antes do início das férias."],
        fontes="CLT, arts. 139, 140 e 145; Constituição, art. 7º, XVII.",
        convite="Salva e manda pra quem vai entrar de férias coletivas.",
        tags="#FériasColetivas #Férias #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, arts. 139, 140 e 145.\n💬 Sua empresa dá férias coletivas no fim do ano?")
t["frase"] = dict(html="Descansar é direito. <em>Com as regras certas.</em>",
    legenda=legenda(t,
        "Férias coletivas de fim de ano têm regras, e o pagamento vem antes de você sair.",
        "Até 2 períodos no ano, nenhum menor que 10 dias, pagamento com 1/3 até 2 dias antes do início.",
        convite="Manda pra quem vai entrar de férias coletivas.",
        tags="#FériasColetivas #Férias #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, arts. 139 e 145.\n💬 Já está contando os dias para as férias?")
t["carrossel"] = dict(tag="Férias coletivas", area="Trabalhista",
    capa=("Férias coletivas", "Fim de ano", "as regras das férias coletivas",
          'Prazos, pagamento e <span class="mt">quem tem pouco tempo de casa</span>.', "CLT, art. 139"),
    itens=[
        ("Até 2 períodos<br>de <em>10 dias</em> ou mais", 'As férias coletivas podem ser divididas em 2, <span class="mt">nenhum com menos de 10 dias</span>.', "CLT, art. 139, § 1º"),
        ("Aviso com<br><em>15 dias</em>", 'A empresa comunica o Ministério do Trabalho e o sindicato <span class="mt">com 15 dias de antecedência</span>.', "CLT, art. 139, §§ 2º e 3º"),
        ("Pouco tempo<br>de casa? <em>Proporcional</em>", 'Menos de 12 meses: férias proporcionais <span class="mt">e um novo período começa</span>.', "CLT, art. 140"),
        ("O <em>1/3</em><br>vem junto", 'Férias coletivas também têm o terço constitucional, <span class="mt">pago até 2 dias antes</span>.', "Constituição, art. 7º, XVII; CLT, art. 145"),
        ("Confira o<br><em>recibo</em>", "Antes de sair de férias, confira:", ""),
    ],
    checklist=["Datas de início e fim", "Valor das férias com 1/3", "Pagamento até 2 dias antes"],
    fecho=("Descansar <em>é</em><br>direito.", "Com as regras certas.", "mande para quem vai entrar de férias coletivas."),
    objetos=["corte-ampulheta.png", "obj-envelope.png", "corte-calculadora.png"], foto5=35129503,
    legenda=legenda(t,
        "Férias coletivas de fim de ano: até 2 períodos, aviso com 15 dias e pagamento com 1/3 antes. Arrasta pro lado. 🏖️",
        "A CLT permite férias coletivas em até 2 períodos anuais, nenhum menor que 10 dias, com aviso ao Ministério do Trabalho e "
        "ao sindicato 15 dias antes. Quem tem menos de 12 meses de casa tira férias proporcionais e começa um novo período. O "
        "pagamento, com o terço, sai até 2 dias antes.",
        faq=["Podem ser em 3 partes? Não. No máximo 2.",
             "Tenho 6 meses de casa. Como fica? Férias proporcionais e novo período aquisitivo.",
             "Quando recebo? Até 2 dias antes do início."],
        fontes="CLT, arts. 139, 140 e 145; Constituição, art. 7º, XVII.",
        convite="Salva e manda pra quem vai entrar de férias coletivas.",
        tags="#FériasColetivas #Férias #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: CLT, arts. 139, 140 e 145.\n💬 Você já tirou férias coletivas?")

# ─────────────────────────── 22/12 · Natal e Ano Novo ───────────────────────────
t = tema(chave="natal-ano-novo-feriado", data="2026-12-22", area="Trabalhista", trabalhista=True,
         titulo="Trabalhar no Natal e no Ano Novo: dobro ou folga")
t["pergunta"] = dict(foto=19663614, pos="50% 50%", brilho=.9, area=TRAB,
    html="Vou trabalhar no Natal e no Ano Novo. <em>Recebo em dobro?</em>",
    legenda=legenda(t,
        "Trabalhar no Natal e no Ano Novo paga em dobro? Paga, se a empresa não der outro dia de folga. 🎄",
        "25 de dezembro e 1º de janeiro são feriados nacionais. O trabalho no feriado é pago em dobro, além do repouso, salvo se "
        "a empresa conceder outro dia de folga. Na escala 12x36, a lei considera os feriados já compensados no salário. As "
        "vésperas, 24 e 31, não são feriados nacionais.",
        faq=["24 e 31 de dezembro são feriados? Não nacionais. Podem ser por lei local ou convenção.",
             "Trabalho na 12x36. Recebo em dobro? Em regra não: a lei considera o feriado compensado na escala."],
        fontes="Lei 662/1949; Lei 605/1949, art. 9º; Súmula 146 do TST; CLT, art. 59-A.",
        convite="Salva e manda pra quem vai trabalhar nas festas.",
        tags="#Natal #Feriado #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 662/1949; Lei 605/1949, art. 9º; CLT, art. 59-A.\n💬 Você vai trabalhar no Natal ou no Ano Novo?")
t["frase"] = dict(html="Quem trabalha no Natal <em>merece cada direito do feriado.</em>",
    legenda=legenda(t,
        "Enquanto muita gente celebra, enfermeiras, comerciárias, vigilantes e tantas outras estão trabalhando.",
        "Feriado trabalhado é pago em dobro ou compensado com outra folga. Na 12x36, a lei considera compensado.",
        convite="Manda pra quem vai estar de plantão.",
        tags="#Natal #Feriado #DireitoTrabalhista #Plantão #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 605/1949, art. 9º.\n💬 Deixa um 🎄 para quem trabalha nas festas.")
t["carrossel"] = dict(tag="Natal e Ano Novo", area="Trabalhista",
    capa=("Trabalho nas festas", "25/12 e 01/01", "trabalhou no feriado? veja o que vale",
          'Dobro, folga ou escala 12x36: <span class="mt">cada caso tem sua regra</span>.', "Lei 605/1949"),
    itens=[
        ("Natal e Ano Novo<br>são <em>feriados</em>", '25/12 e 01/01 são feriados nacionais, <span class="mt">em todo o país</span>.', "Lei 662/1949"),
        ("<em>24 e 31</em><br>não são", 'As vésperas são dias normais, <span class="mt">salvo lei local ou convenção</span>.', "Lei 662/1949"),
        ("Trabalhou?<br><em>Dobro</em> ou folga", 'Sem outro dia de folga, o feriado trabalhado <span class="mt">é pago em dobro</span>.', "Lei 605/1949, art. 9º; Súmula 146 do TST"),
        ("Na <em>12x36</em>,<br>já está compensado", 'A lei considera os feriados <span class="mt">incluídos no salário da escala</span>.', "CLT, art. 59-A"),
        ("Anote<br>o <em>ponto</em>", "Para conferir no contracheque, separe:", ""),
    ],
    checklist=["Ponto de 25/12 e 01/01", "Escala de dezembro", "Data da folga, se houve troca"],
    fecho=("Feriado trabalhado<br><em>tem regra</em>.", "Confira antes de assinar a escala.", "mande para quem trabalha nas festas."),
    objetos=["obj-declaracao.png", "corte-cafe.png", "corte-reais.png"], foto5=35724805,
    legenda=legenda(t,
        "Trabalhar no Natal e no Ano Novo: dobro ou folga, e na 12x36 a regra é outra. Arrasta pro lado. 🎄",
        "25/12 e 01/01 são feriados nacionais. O trabalho no feriado é pago em dobro, além do repouso, salvo se houver outro dia "
        "de folga. Na escala 12x36, a CLT considera os feriados compensados. As vésperas, 24 e 31, não são feriados nacionais.",
        faq=["Natal trabalhado paga em dobro? Paga, se não houver outra folga.",
             "E na 12x36? Em regra, o feriado já está compensado na escala.",
             "24/12 é feriado? Não nacional."],
        fontes="Lei 662/1949; Lei 605/1949, art. 9º; Súmula 146 do TST; CLT, art. 59-A.",
        convite="Salva e manda pra quem vai trabalhar nas festas.",
        tags="#Natal #Feriado #DireitoTrabalhista #CLT #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 662/1949; Lei 605/1949, art. 9º; CLT, art. 59-A.\n💬 Você trabalha em escala 12x36?")

# ─────────────────────────── 24/12 · Viagem com os filhos ───────────────────────────
t = tema(chave="viagem-com-filhos", data="2026-12-24", area="Família",
         titulo="Viagem de férias com os filhos: quando precisa de autorização")
t["pergunta"] = dict(foto=7368186, pos="50% 55%", brilho=.95, area=FAM,
    html="Sou separada e quero viajar com meu filho nas férias. <em>Preciso de autorização do pai?</em>",
    legenda=legenda(t,
        "Mãe separada precisa de autorização do pai para viajar com o filho? Dentro do Brasil, não. Para o exterior, sim. ✈️",
        "Criança ou adolescente até 16 anos que viaja dentro do Brasil com o pai ou com a mãe não precisa de autorização do outro "
        "genitor. Para viajar ao exterior com só um dos pais, é preciso autorização do outro, por escrito e com firma reconhecida, "
        "ou autorização do juiz. E a viagem precisa respeitar as datas de convivência combinadas.",
        faq=["E se o pai não autorizar a viagem ao exterior? É possível pedir a autorização ao juiz.",
             "Meu filho vai viajar com a avó. Precisa? Parente até o terceiro grau, com documento que prove o parentesco, pode levar."],
        fontes="ECA, arts. 83 e 84; CNJ, Resoluções 131/2011 e 295/2019; Código Civil, art. 1.589.",
        convite="Salva e manda pra quem vai viajar com os filhos.",
        tags="#ViagemComFilhos #GuardaCompartilhada #Férias #DireitoDeFamília #AdvogadaVitóriaES"),
    pc="📚 Base legal: ECA, arts. 83 e 84.\n💬 Vai viajar com as crianças nestas férias?")
t["frase"] = dict(html="Férias boas <em>começam combinadas.</em>",
    legenda=legenda(t,
        "Viagem de fim de ano com os filhos é ótima. Com as datas combinadas e os documentos em ordem, melhor ainda.",
        "Dentro do Brasil, com o pai ou a mãe, não precisa de autorização do outro. Para o exterior, precisa.",
        convite="Manda pra quem vai viajar com os filhos.",
        tags="#ViagemComFilhos #Férias #DireitoDeFamília #GuardaCompartilhada #AdvogadaVitóriaES"),
    pc="📚 Base legal: ECA, arts. 83 e 84.\n💬 Praia ou interior nestas férias?")
t["carrossel"] = dict(tag="Férias com os filhos", area="Família",
    capa=("Férias com os filhos", "Viagem", "quando precisa de autorização",
          'Brasil, exterior e <span class="mt">as datas da guarda</span>.', "ECA, arts. 83 e 84"),
    itens=[
        ("No Brasil, com<br>o pai ou a mãe: <em>livre</em>", 'Até 16 anos, com um dos pais, <span class="mt">não precisa de autorização do outro</span>.', "ECA, art. 83"),
        ("Sem os pais?<br><em>Autorização</em>", 'Menor de 16 anos sem os pais precisa de autorização <span class="mt">dos pais ou do juiz</span>.', "ECA, art. 83; CNJ, Res. 295/2019"),
        ("Exterior com um<br>dos pais: <em>autorização</em>", 'O outro genitor autoriza por escrito, <span class="mt">com firma reconhecida</span>, ou o juiz autoriza.', "ECA, art. 84; CNJ, Res. 131/2011"),
        ("Respeite as<br>datas da <em>guarda</em>", 'A viagem não pode atropelar a convivência <span class="mt">combinada ou decidida</span>.', "Código Civil, art. 1.589"),
        ("Antes de<br><em>embarcar</em>", "Leve na bolsa:", ""),
    ],
    checklist=["Documento com foto da criança", "Certidão de nascimento", "Autorização, se for o caso"],
    fecho=("Férias boas<br>começam <em>combinadas</em>.", "Com os documentos em ordem.", "mande para quem vai viajar com os filhos."),
    objetos=["obj-ursinho2.png", "obj-envelope.png", "corte-pasta.png"], foto5=11668208,
    legenda=legenda(t,
        "Viagem de férias com os filhos: no Brasil, com o pai ou a mãe, não precisa de autorização; para o exterior, precisa. Arrasta pro lado. ✈️",
        "Pelo ECA, criança ou adolescente até 16 anos viajando no Brasil com um dos pais não precisa de autorização do outro. "
        "Sem os pais, precisa. Para o exterior com só um dos pais, o outro genitor autoriza por escrito, com firma reconhecida, "
        "ou o juiz autoriza. E as datas de convivência devem ser respeitadas.",
        faq=["Viagem nacional com a mãe precisa de autorização do pai? Não.",
             "E para o exterior? Precisa da autorização do outro genitor ou do juiz.",
             "Posso viajar no período do outro genitor? Só com acordo."],
        fontes="ECA, arts. 83 e 84; CNJ, Resoluções 131/2011 e 295/2019; Código Civil, art. 1.589.",
        convite="Salva e manda pra quem vai viajar com os filhos.",
        tags="#ViagemComFilhos #GuardaCompartilhada #Férias #DireitoDeFamília #AdvogadaVitóriaES"),
    pc="📚 Base legal: ECA, arts. 83 e 84; CNJ, Resoluções 131/2011 e 295/2019.\n💬 Vocês já combinaram as férias das crianças?")

# ─────────────────────────── 26/12 · Pensão: reajuste de janeiro ───────────────────────────
t = tema(chave="pensao-reajuste", data="2026-12-26", area="Família",
         titulo="Pensão em salário mínimo: o reajuste de janeiro é automático")
t["pergunta"] = dict(foto=11114830, pos="50% 50%", brilho=.92, area=FAM,
    html="A pensão do meu filho é 30% do salário mínimo. <em>Ela aumenta em janeiro?</em>",
    legenda=legenda(t,
        "Pensão em salário mínimo aumenta em janeiro? Aumenta. Ela acompanha o novo mínimo sem precisar de processo. 👧🏾",
        "Quando a pensão foi fixada em percentual do salário mínimo, o valor sobe junto com o reajuste do mínimo, a partir de "
        "janeiro, automaticamente. Se foi fixada em percentual do salário de quem paga, acompanha esse salário. Se foi em valor "
        "fixo, só muda pelo índice previsto ou com pedido de revisão.",
        faq=["E se continuarem pagando o valor antigo? A diferença pode ser cobrada na Justiça."],
        fontes="Jurisprudência do STF e do STJ; Código Civil, art. 1.699; CPC, art. 528.",
        convite="Salva pra conferir o depósito de janeiro e manda pra quem recebe pensão.",
        tags="#PensãoAlimentícia #SalárioMínimo #DireitoDeFamília #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Civil, art. 1.699; CPC, art. 528.\n💬 A pensão do seu filho é em salário mínimo ou em valor fixo?")
t["frase"] = dict(html="A pensão do seu filho <em>também ganha reajuste.</em>",
    legenda=legenda(t,
        "Janeiro tem salário mínimo novo. E a pensão fixada em salário mínimo sobe junto.",
        "Não precisa de processo: o valor acompanha o reajuste. Se o depósito vier com o valor antigo, a diferença pode ser cobrada.",
        convite="Manda pra quem recebe pensão.",
        tags="#PensãoAlimentícia #SalárioMínimo #DireitoDeFamília #MãeSolo #AdvogadaVitóriaES"),
    pc="📚 Base legal: Código Civil, art. 1.699.\n💬 Marca uma mãe que precisa conferir o depósito de janeiro.")
t["carrossel"] = dict(tag="Pensão alimentícia", area="Família",
    capa=("Pensão em 2027", "Reajuste", "quando ele é automático em janeiro",
          'Salário mínimo, salário ou valor fixo: <span class="mt">cada forma tem uma regra</span>.', "Código Civil, art. 1.699"),
    itens=[
        ("Em salário mínimo:<br><em>automático</em>", 'A pensão acompanha o novo mínimo <span class="mt">sem precisar de processo</span>.', "STF e STJ"),
        ("Em percentual<br>do <em>salário</em>", 'Acompanha o salário de quem paga, <span class="mt">inclusive aumentos e 13º</span>.', "STJ, Tema 192"),
        ("Em valor fixo:<br>leia a <em>decisão</em>", 'Só muda pelo índice previsto no acordo <span class="mt">ou com pedido de revisão</span>.', "Código Civil, art. 1.699"),
        ("Pagou o valor<br><em>antigo</em>?", 'A diferença pode ser cobrada <span class="mt">na Justiça</span>.', "CPC, art. 528"),
        ("Para conferir,<br><em>separe</em>", "Antes de cobrar a diferença:", ""),
    ],
    checklist=["A decisão ou o acordo da pensão", "Extratos dos depósitos", "O novo valor do salário mínimo"],
    fecho=("Pensão é do filho,<br><em>com reajuste</em>.", "Confira o depósito de janeiro.", "mande para quem recebe pensão."),
    objetos=["corte-cofrinho.png", "corte-calculadora.png", "corte-martelo.png"], foto5=6603412,
    legenda=legenda(t,
        "Pensão em salário mínimo sobe sozinha em janeiro. Arrasta pro lado e confira como fica a sua. 👧🏾",
        "A forma como a pensão foi fixada decide o reajuste. Em percentual do salário mínimo, acompanha o novo mínimo "
        "automaticamente. Em percentual do salário, acompanha o salário de quem paga. Em valor fixo, segue o índice previsto ou "
        "depende de revisão. Pagamento com valor antigo gera diferença que pode ser cobrada.",
        faq=["Pensão em salário mínimo aumenta em janeiro? Sim, automaticamente.",
             "Valor fixo aumenta? Só pelo índice previsto ou com revisão.",
             "Pagaram menos. Posso cobrar? Pode."],
        fontes="Jurisprudência do STF e do STJ; STJ, Tema 192; Código Civil, art. 1.699; CPC, art. 528.",
        convite="Salva pra conferir o depósito de janeiro e manda pra quem recebe pensão.",
        tags="#PensãoAlimentícia #SalárioMínimo #DireitoDeFamília #DireitosDaCriança #AdvogadaVitóriaES"),
    pc="📚 Base legal: STJ, Tema 192; Código Civil, art. 1.699; CPC, art. 528.\n💬 Você sabia que o reajuste pode ser automático?")

# ─────────────────────────── 29/12 · Aposentadoria 2027 ───────────────────────────
t = tema(chave="aposentadoria-2027", data="2026-12-29", area="Previdenciário",
         titulo="Aposentadoria da mulher em 2027: 94 pontos e 60 anos")
t["pergunta"] = dict(foto=7012265, pos="50% 50%", brilho=.92, area=PREV,
    html="Vou completar 30 anos de contribuição em 2027. <em>O que muda para mim?</em>",
    legenda=legenda(t,
        "O que muda na aposentadoria da mulher em 2027? Os pontos sobem para 94 e a idade mínima progressiva para 60 anos. 👵🏾",
        "Em 2027, a regra de pontos pede 94 (idade + tempo de contribuição), com 30 anos de contribuição, e a idade mínima "
        "progressiva sobe para 60 anos. A aposentadoria por idade continua com 62 anos e 15 de contribuição. Quem completou "
        "algum requisito em 2026 mantém o direito, mesmo pedindo depois.",
        passos=["Baixe o extrato do CNIS no Meu INSS", "Faça a simulação das regras", "Confira se faltam vínculos antigos"],
        fontes="EC 103/2019, arts. 15, 16, 18 e 20.",
        convite="Salva e manda pra quem pensa em se aposentar.",
        tags="#Aposentadoria #INSS #AposentadoriaDaMulher #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: EC 103/2019, arts. 15, 16 e 18.\n💬 Você já fez a simulação no Meu INSS?")
t["frase"] = dict(html="Planejar a aposentadoria <em>é um presente para o seu futuro.</em>",
    legenda=legenda(t,
        "Virada de ano é um bom momento para olhar para a aposentadoria.",
        "Em 2027 as regras de transição da mulher sobem: 94 pontos e idade mínima de 60 anos. Simular antes evita surpresa.",
        convite="Manda pra quem está perto de se aposentar.",
        tags="#Aposentadoria #INSS #AposentadoriaDaMulher #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: EC 103/2019.\n💬 Marca quem está contando os anos para se aposentar.")
t["carrossel"] = dict(tag="Aposentadoria", area="Previdenciário",
    capa=("Aposentadoria da mulher", "2027", "o que muda nas regras",
          'Pontos e idade mínima sobem: <span class="mt">confira antes de pedir</span>.', "EC 103/2019"),
    itens=[
        ("Pontos:<br><em>94</em> em 2027", 'Idade + contribuição, <span class="mt">com 30 anos de contribuição</span>. Sobe 1 por ano até 100.', "EC 103/2019, art. 15"),
        ("Idade mínima:<br><em>60 anos</em>", 'Com 30 anos de contribuição. <span class="mt">Sobe 6 meses por ano até 62.</span>', "EC 103/2019, art. 16"),
        ("Por idade:<br><em>62 anos</em>", 'Com 15 anos de contribuição. <span class="mt">Essa regra não muda.</span>', "EC 103/2019, art. 18"),
        ("Pedágio de 100%:<br>a partir dos <em>57</em>", '30 de contribuição e mais o tempo <span class="mt">que faltava em 2019</span>.', "EC 103/2019, art. 20"),
        ("Completou em 2026?<br><em>Está garantido</em>", "O direito adquirido não se perde. Separe:", ""),
    ],
    checklist=["Extrato do CNIS", "Simulação no Meu INSS", "Carteiras e carnês antigos"],
    fecho=("Planejar a<br>aposentadoria <em>conta</em>.", "Cada regra dá um valor diferente.", "mande para quem pensa em se aposentar."),
    objetos=["corte-calculadora.png", "corte-ampulheta.png", "corte-pasta.png"], foto5=36810448,
    legenda=legenda(t,
        "Aposentadoria da mulher em 2027: 94 pontos e idade mínima de 60 anos. Arrasta pro lado e confira as regras. 👵🏾",
        "Pelas regras de transição da Reforma, em 2027 a mulher precisa de 94 pontos com 30 anos de contribuição, ou de 60 anos "
        "de idade com 30 de contribuição. A aposentadoria por idade segue com 62 anos e 15 de contribuição. Quem completou os "
        "requisitos de alguma regra em 2026 mantém o direito.",
        faq=["Quantos pontos em 2027? 94.",
             "Qual a idade mínima em 2027? 60 anos, com 30 de contribuição.",
             "Completei os requisitos em 2026. Perco? Não. É direito adquirido."],
        fontes="EC 103/2019, arts. 15, 16, 18 e 20.",
        convite="Salva e manda pra quem pensa em se aposentar.",
        tags="#Aposentadoria #INSS #AposentadoriaDaMulher #DireitoPrevidenciário #AdvogadaVitóriaES"),
    pc="📚 Base legal: EC 103/2019, arts. 15, 16, 18 e 20.\n💬 Qual regra parece a sua?")

# ─────────────────────────── 31/12 · Licença-paternidade 2027 ───────────────────────────
t = tema(chave="licenca-paternidade-2027", data="2026-12-31", area="Trabalhista", trabalhista=True,
         titulo="2027 começa com licença-paternidade de 10 dias")
t["pergunta"] = dict(foto=15797916, pos="50% 50%", brilho=.95, area=TRAB,
    html="Meu bebê nasce em janeiro de 2027. <em>Quantos dias de licença o pai terá?</em>",
    legenda=legenda(t,
        "Licença-paternidade em 2027: quantos dias? A partir de 1º de janeiro, passa de 5 para 10 dias. 👶🏾",
        "A Lei 15.371/2026 amplia a licença-paternidade aos poucos: 10 dias a partir de 1º de janeiro de 2027, 15 dias em 2028 e "
        "20 dias em 2029, se cumpridas as metas fiscais. A lei também cria o salário-paternidade: a empresa paga e é reembolsada "
        "pelo INSS. Vale para nascimento, adoção e guarda para adoção.",
        faq=["Empresa Cidadã muda alguma coisa? Confira com o RH como a empresa aplica a nova regra.",
             "Quem paga? A empresa, com reembolso do INSS."],
        fontes="Lei 15.371/2026.",
        convite="Salva e manda pra um futuro papai.",
        tags="#LicençaPaternidade #Paternidade #Pai #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 15.371/2026.\n💬 Quantos dias de licença o pai teve na sua família?")
t["frase"] = dict(html="Um pai presente <em>começa nos primeiros dias.</em>",
    legenda=legenda(t,
        "2027 começa com uma mudança para as famílias: a licença-paternidade dobra.",
        "São 10 dias a partir de janeiro, 15 em 2028 e 20 em 2029, conforme as metas fiscais.",
        convite="Manda pra um futuro papai.",
        tags="#LicençaPaternidade #Paternidade #Pai #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 15.371/2026.\n💬 Feliz 2027! Deixa um 💛 para os pais presentes.")
t["carrossel"] = dict(tag="Licença-paternidade", area="Trabalhista",
    capa=("Licença-paternidade", "10 dias", "a partir de janeiro de 2027",
          'A licença do pai aumenta <span class="mt">aos poucos até 2029</span>.', "Lei 15.371/2026"),
    itens=[
        ("<em>10 dias</em><br>em 2027", 'A licença-paternidade passa de 5 <span class="mt">para 10 dias</span>.', "Lei 15.371/2026"),
        ("<em>15 dias</em><br>em 2028", 'E 20 dias em 2029, <span class="mt">se cumpridas as metas fiscais</span>.', "Lei 15.371/2026"),
        ("Nasce o<br><em>salário-paternidade</em>", 'A empresa paga <span class="mt">e é reembolsada pelo INSS</span>.', "Lei 15.371/2026"),
        ("Vale também<br>na <em>adoção</em>", 'A licença é garantida na adoção <span class="mt">e na guarda para adoção</span>.', "Lei 15.371/2026"),
        ("Combine com<br>o <em>RH</em>", "Avise com antecedência e separe:", ""),
    ],
    checklist=["Certidão de nascimento ou termo de guarda", "Pedido da licença por escrito", "Datas de início e fim"],
    fecho=("Pai presente<br><em>desde o início</em>.", "2027 começa com mais tempo em casa.", "mande para um futuro papai."),
    objetos=["corte-sapatinho-azul.png", "corte-ampulheta.png", "corte-reais.png"], foto5=29513145,
    legenda=legenda(t,
        "Licença-paternidade de 10 dias a partir de janeiro de 2027. Arrasta pro lado e confira o que muda. 👶🏾",
        "A Lei 15.371/2026 amplia a licença-paternidade de forma gradual: 10 dias em 2027, 15 em 2028 e 20 em 2029, conforme as "
        "metas fiscais. Cria o salário-paternidade, pago pela empresa com reembolso do INSS, e vale também na adoção.",
        faq=["Quantos dias em 2027? 10.",
             "Quem paga? A empresa, com reembolso do INSS.",
             "Vale na adoção? Vale."],
        fontes="Lei 15.371/2026.",
        convite="Salva e manda pra um futuro papai.",
        tags="#LicençaPaternidade #Paternidade #Pai #DireitoTrabalhista #AdvogadaVitóriaES"),
    pc="📚 Base legal: Lei 15.371/2026.\n💬 O que você acha da licença maior para os pais?")


# ───────────────────────── Mito ou Lei (19h, dias pares) ─────────────────────────
MITO_OU_LEI = [
    ("2026-12-04", "hiv-trabalho", "Quem vive com HIV precisa contar para a empresa.", "MITO",
     "Revelar é escolha da pessoa. A empresa não pode exigir teste de HIV, e demitir por causa da condição é crime.",
     "Lei 12.984/2014; Portaria MTE 1.246/2010", "#DezembroVermelho #MitoOuLei #HIV #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem precisa saber", "Você sabia que o teste de HIV na admissão é proibido?"),
    ("2026-12-06", "trabalho-escravo", "Empresa com 100 funcionários precisa ter cota de inclusão.", "LEI",
     "De 2% a 5% das vagas, conforme o tamanho da empresa, são de pessoas com necessidades especiais ou reabilitadas pelo INSS.",
     "Lei 8.213/1991, art. 93", "#Inclusão #MitoOuLei #Acessibilidade #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem procura uma vaga", "A empresa onde você trabalha cumpre a cota?"),
    ("2026-12-08", "burnout-trabalho", "Burnout não é doença do trabalho.", "MITO",
     "Desde 2023, o burnout está na lista oficial de doenças relacionadas ao trabalho. Com a relação provada, gera afastamento e estabilidade.",
     "Portaria GM/MS 1.999/2023; Lei 8.213/1991, art. 118", "#Burnout #MitoOuLei #SaúdeMental #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem está no limite", "Você conhece alguém que se afastou por burnout?"),
    ("2026-12-10", "assedio-moral", "Gritar com funcionário na frente de todos é só jeito do chefe.", "MITO",
     "Humilhação e exposição podem ser assédio moral e gerar indenização. A empresa responde pelos atos do chefe.",
     "CLT, art. 483; Código Civil, art. 932, III", "#AssédioMoral #MitoOuLei #DireitosHumanos #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem passa por isso", "Você já viu alguém ser humilhado no trabalho?"),
    ("2026-12-12", "festa-da-firma", "Assédio sexual no trabalho é crime.", "LEI",
     "Usar o cargo para constranger alguém com fins sexuais dá de 1 a 2 anos de detenção.",
     "Código Penal, art. 216-A", "#AssédioSexual #MitoOuLei #DireitosDaMulher #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pras colegas antes da festa", "Sua empresa tem canal de denúncia?"),
    ("2026-12-14", "13-segunda-parcela", "A 2ª parcela do 13º vem sem descontos.", "MITO",
     "É na 2ª parcela que entram os descontos de INSS e imposto de renda, calculados sobre o 13º inteiro.",
     "Lei 4.749/1965", "#13Salário #MitoOuLei #DireitoTrabalhista #CLT #AdvogadaVitóriaES", False, True,
     "manda pra quem vai conferir o contracheque", "Sua 2ª parcela já tem data?"),
    ("2026-12-16", "aposentadoria-2027", "BPC dá direito a 13º.", "MITO",
     "O BPC paga 12 parcelas de um salário mínimo por ano, sem abono anual. Aposentados e pensionistas do INSS recebem; o BPC não.",
     "Lei 8.742/1993", "#BPC #MitoOuLei #INSS #DireitoPrevidenciário #AdvogadaVitóriaES", False, False,
     "manda pra quem recebe o BPC", "Você achava que o BPC tinha 13º?"),
    ("2026-12-18", "13-segunda-parcela", "Hoje é o prazo da 2ª parcela do 13º.", "LEI",
     "O prazo legal é 20/12, um domingo em 2026. Por isso, o pagamento deve sair até hoje, sexta-feira.",
     "Lei 4.749/1965, art. 1º", "#13Salário #MitoOuLei #DireitoTrabalhista #CLT #AdvogadaVitóriaES", False, True,
     "manda pra quem ainda não conferiu o extrato", "A sua 2ª parcela já caiu?"),
    ("2026-12-20", "temporaria-fim-de-ano", "Contrato temporário de fim de ano não tem FGTS.", "MITO",
     "O temporário tem FGTS depositado, além de 13º e férias proporcionais.",
     "Lei 6.019/1974; Lei 8.036/1990", "#TrabalhoTemporário #MitoOuLei #FGTS #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem pegou vaga de fim de ano", "Você já conferiu o FGTS do temporário?"),
    ("2026-12-22", "natal-ano-novo-feriado", "24 e 31 de dezembro são feriados nacionais.", "MITO",
     "Os feriados nacionais são 25/12 e 01/01. As vésperas são dias normais, salvo lei local ou convenção coletiva.",
     "Lei 662/1949", "#Natal #MitoOuLei #Feriado #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem vai trabalhar nas festas", "Você trabalha na véspera de Natal?"),
    ("2026-12-24", "viagem-com-filhos", "Para viajar com o filho dentro do Brasil, sempre precisa de autorização do outro genitor.", "MITO",
     "Com o pai ou a mãe, a viagem nacional não precisa de autorização do outro. Para o exterior, precisa.",
     "ECA, arts. 83 e 84", "#ViagemComFilhos #MitoOuLei #Férias #DireitoDeFamília #AdvogadaVitóriaES", False, False,
     "manda pra quem vai viajar com os filhos", "Feliz Natal! Vai viajar com as crianças?"),
    ("2026-12-26", "pensao-reajuste", "Pensão fixada em salário mínimo aumenta sozinha em janeiro.", "LEI",
     "O valor acompanha o reajuste do salário mínimo, sem precisar de novo processo.",
     "Jurisprudência do STF e do STJ", "#PensãoAlimentícia #MitoOuLei #SalárioMínimo #DireitoDeFamília #AdvogadaVitóriaES", False, False,
     "manda pra quem recebe pensão", "Você vai conferir o depósito de janeiro?"),
    ("2026-12-28", "natal-ano-novo-feriado", "Os prazos do processo trabalhista param no fim do ano.", "LEI",
     "De 20 de dezembro a 20 de janeiro, os prazos processuais ficam suspensos na Justiça do Trabalho.",
     "CLT, art. 775-A", "#JustiçaDoTrabalho #MitoOuLei #Recesso #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem tem processo em andamento", "Você sabia do recesso de fim de ano?"),
    ("2026-12-30", "ferias-coletivas", "Férias coletivas podem ser divididas em 3 partes.", "MITO",
     "São no máximo 2 períodos por ano, e nenhum pode ter menos de 10 dias.",
     "CLT, art. 139, § 1º", "#FériasColetivas #MitoOuLei #Férias #DireitoTrabalhista #AdvogadaVitóriaES", False, True,
     "manda pra quem vai entrar de férias", "Feliz Ano Novo! Já está de férias?"),
]

# Fontes conferidas em 10/10/2026: Lei 12.984/2014; Portaria MTE 1.246/2010; Súmula 443 do TST; Lei 8.036/1990, art. 20,
# XIII; Código Penal, arts. 149, 215-A e 216-A; LC 150/2015; Portaria GM/MS 1.999/2023; Lei 8.213/1991, arts. 22, 60, 93
# e 118; CLT, arts. 59-A, 139, 140, 145, 483 e 775-A; Lei 4.749/1965; Lei 7.855/1989; Lei 6.019/1974, arts. 10 e 12;
# TST Pleno mar/2026 (1000059-12.2020.5.02.0382); Lei 662/1949; Lei 605/1949, art. 9º; Súmula 146 do TST; ECA, arts. 83 e
# 84; CNJ, Res. 131/2011 e 295/2019; Lei 8.742/1993 (BPC sem abono anual); EC 103/2019; Lei 15.371/2026 (10 dias em 2027).
