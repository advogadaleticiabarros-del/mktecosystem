"""Os 9 artigos de blog de dezembro/2026 (segundas e quintas, 9h), plano docs/PLANO_CONTEUDO_DEZ_2026.md.
Voz da Letícia; modelo de HTML igual aos publicados; fatos conferidos em 10/10/2026 (ver conteudo_dez.py).
`post_google` = texto pronto para o Perfil da Empresa (sem telefone, sem link no texto)."""

B = "https://advogadaleticiabarros.com.br/blog/"


def _cta(frase: str) -> str:
    return f"<h2>Se essa é a sua situação</h2>\n\n<p>{frase} Procure uma advogada de confiança.</p>"


ARTIGOS = [
    {
        "data": "2026-12-03", "pauta": "Blog: HIV no trabalho: sigilo, exames e demissão discriminatória", "foto": "original-hiv-trabalho.jpg", "cy": 0.32,
        "titulo": "HIV no trabalho: sigilo, exames e demissão discriminatória",
        "slug": "hiv-no-trabalho-sigilo-exames-demissao",
        "meta": "Quem vive com HIV não precisa contar para a empresa, não pode ser testado na admissão e não pode ser demitido por isso. Veja os direitos.",
        "resumo": "Sigilo, teste proibido na admissão, demissão discriminatória e saque do FGTS: os direitos de quem vive com HIV no trabalho.",
        "post_google": "Dezembro Vermelho: quem vive com HIV não é obrigado a contar para a empresa, não pode ser testado na admissão e não pode ser demitido por isso. Explicamos os direitos no blog.",
        "html": """<p>Você recebeu o diagnóstico e, junto com o cuidado com a saúde, veio o medo: e se descobrirem no trabalho? E se eu for demitida?</p>

<p>Esse medo tem razão de existir, porque o preconceito ainda existe. Mas a lei brasileira é clara do seu lado.</p>

<p>Neste artigo eu explico, sem juridiquês, os direitos de quem vive com HIV no trabalho. Vamos juntas.</p>

<h2>Preciso contar para a empresa que vivo com HIV?</h2>

<p>Não. Revelar a condição é uma escolha sua. Ninguém é obrigado a contar para a empresa, para o RH ou para os colegas. A informação de saúde é íntima e protegida.</p>

<h2>A empresa pode pedir teste de HIV?</h2>

<p>Não pode. A Portaria MTE 1.246/2010 proíbe, de forma direta ou indireta, o teste de HIV nos exames de <strong>admissão, mudança de função, periódicos, retorno e demissão</strong>. O TST já condenou empresas a indenizar trabalhadores que foram obrigados a fazer o teste para serem contratados.</p>

<h2>Demitir por causa do HIV é crime</h2>

<p>A Lei 12.984/2014 tornou crime, com pena de 1 a 4 anos de reclusão, <strong>negar emprego ou demitir</strong> alguém por viver com HIV. E a Justiça do Trabalho presume discriminatória a demissão de quem tem doença que gera estigma (Súmula 443 do TST). Na prática, é a empresa que precisa provar que demitiu por outro motivo.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Demissão presumida discriminatória dá direito à <strong>reintegração</strong> no emprego ou a indenização, conforme o caso (Lei 9.029/1995).</p>
</div>

<h2>Posso sacar o FGTS?</h2>

<p>Pode. Quem vive com HIV, ou tem dependente que vive com HIV, pode movimentar o FGTS <strong>sem precisar sair do emprego</strong> (Lei 8.036/1990, art. 20, XIII). O pedido é feito na Caixa, com o atestado médico.</p>

<h2>Como provar a discriminação (essa é a parte decisiva)</h2>

<table class="prova-table">
<tr><th>Guarde</th><th>Para quê</th></tr>
<tr><td>Pedidos de exame ou de informação de saúde</td><td>Mostram a exigência proibida.</td></tr>
<tr><td>Mensagens e comentários</td><td>Revelam quem sabia e como passou a tratar você.</td></tr>
<tr><td>Datas</td><td>Quando a empresa soube e quando veio a demissão.</td></tr>
<tr><td>Testemunhas</td><td>Colegas que presenciaram comentários ou mudanças de tratamento.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Sou obrigada a contar que vivo com HIV?</h3>
<p>Não. Revelar é uma escolha sua.</p>

<h3>A empresa pode exigir teste de HIV na admissão?</h3>
<p>Não. A Portaria MTE 1.246/2010 proíbe o teste em qualquer exame ligado ao trabalho.</p>

<h3>Fui demitida depois que souberam. O que posso fazer?</h3>
<p>A demissão é presumida discriminatória e pode gerar reintegração ou indenização. Além disso, demitir por HIV é crime.</p>

<h3>Posso sacar o FGTS por viver com HIV?</h3>
<p>Pode, sem precisar sair do emprego.</p>

""" + _cta("Viver com HIV não tira direitos. Se você foi discriminada no trabalho,"),
    },
    {
        "data": "2026-12-07", "pauta": "Blog: Burnout é doença do trabalho? Afastamento, INSS e estabilidade", "foto": "original-burnout-trabalho.jpg", "cy": 0.6,
        "titulo": "Burnout é doença do trabalho? Afastamento, INSS e estabilidade",
        "slug": "burnout-doenca-do-trabalho-afastamento-inss-estabilidade",
        "meta": "Burnout está na lista de doenças do trabalho desde 2023. Veja como funciona o afastamento pelo INSS, a CAT e a estabilidade de 12 meses.",
        "resumo": "Burnout é doença do trabalho: afastamento pelo INSS, CAT e 12 meses de estabilidade, e como provar a relação com o emprego.",
        "post_google": "Burnout é doença do trabalho desde 2023. No blog, explicamos o afastamento pelo INSS, a CAT, a estabilidade de 12 meses e como provar a relação com o emprego.",
        "html": """<p>Você acorda cansada, chega ao trabalho com o coração acelerado e, no fim do dia, não sobra nada. Até que o corpo para.</p>

<p>Muita gente acha que é fraqueza. Não é. O burnout é reconhecido como doença relacionada ao trabalho, e isso gera direitos.</p>

<p>Neste artigo eu explico, sem juridiquês, o que muda quando o burnout é ligado ao emprego. Vamos juntas.</p>

<h2>Burnout é doença do trabalho?</h2>

<p>Desde 2023, a síndrome de burnout está na <strong>Lista de Doenças Relacionadas ao Trabalho</strong> do Ministério da Saúde (Portaria GM/MS 1.999/2023). A lista não decide sozinha o seu caso: é preciso mostrar que, para você, o adoecimento veio do trabalho. Mas ela facilita muito esse reconhecimento.</p>

<h2>Como funciona o afastamento</h2>

<ul>
<li><strong>Até 15 dias</strong>: a empresa paga o salário normalmente.</li>
<li><strong>A partir do 16º dia</strong>: o INSS paga o benefício por incapacidade temporária, depois da perícia (Lei 8.213/1991, art. 60).</li>
</ul>

<h2>A CAT e o benefício acidentário</h2>

<p>A CAT (Comunicação de Acidente de Trabalho) liga a doença ao emprego. A empresa deve emitir; se ela se recusar, <strong>o médico, o sindicato ou a própria trabalhadora</strong> podem emitir (Lei 8.213/1991, art. 22). Com a relação reconhecida, o benefício é acidentário.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Depois do benefício acidentário, você tem <strong>12 meses de estabilidade</strong> na volta ao trabalho (Lei 8.213/1991, art. 118). E a empresa continua depositando o FGTS durante o afastamento.</p>
</div>

<h2>Como provar a relação com o trabalho (essa é a parte decisiva)</h2>

<table class="prova-table">
<tr><th>Guarde</th><th>Por quê</th></tr>
<tr><td>Laudo do psiquiatra ou do psicólogo</td><td>Descreve a doença e a ligação com o trabalho.</td></tr>
<tr><td>Mensagens de cobrança fora do horário</td><td>Mostram a pressão e a jornada real.</td></tr>
<tr><td>Metas e registros de ponto</td><td>Mostram sobrecarga e horas extras.</td></tr>
<tr><td>Testemunhas</td><td>Colegas que viveram o mesmo ambiente.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Burnout dá afastamento pelo INSS?</h3>
<p>Dá, quando a incapacidade passa de 15 dias e é confirmada na perícia.</p>

<h3>Quem emite a CAT se a empresa se recusar?</h3>
<p>O médico, o sindicato ou a própria trabalhadora.</p>

<h3>Tenho estabilidade depois do afastamento?</h3>
<p>Sim, 12 meses depois do fim do benefício acidentário.</p>

""" + _cta("Adoecer pelo trabalho não é fraqueza. Se o seu afastamento foi negado ou a empresa não reconhece a relação com o trabalho,"),
    },
    {
        "data": "2026-12-10", "pauta": "Blog: Assédio moral no trabalho: exemplos e como provar", "foto": "original-assedio-moral.jpg", "cy": 0.32,
        "titulo": "Assédio moral no trabalho: exemplos e como provar",
        "slug": "assedio-moral-no-trabalho-exemplos-e-como-provar",
        "meta": "Gritos, humilhação, isolamento e metas para constranger: veja exemplos de assédio moral no trabalho, seus direitos e como reunir provas.",
        "resumo": "Exemplos de assédio moral no trabalho, o que você pode pedir e como reunir provas sem se expor.",
        "post_google": "Dia dos Direitos Humanos: dignidade também vale no trabalho. No blog, mostramos exemplos de assédio moral, os direitos de quem passa por isso e como reunir provas.",
        "html": """<p>O chefe grita na frente de todo mundo. Tiram suas tarefas e passam a fingir que você não existe. Cada reunião vira um momento de humilhação.</p>

<p>Isso não é coisa da sua cabeça. E não é algo que você tem que engolir calada.</p>

<p>Neste artigo eu explico, sem juridiquês, o que é assédio moral, quais são seus direitos e como provar. Vamos juntas.</p>

<h2>O que é assédio moral no trabalho?</h2>

<p>É a exposição da trabalhadora a situações humilhantes e constrangedoras, de forma a atingir a dignidade dela. Costuma se repetir e pode vir de um chefe, de colegas ou até da forma como a empresa organiza o trabalho.</p>

<h2>Exemplos de assédio moral</h2>

<ul>
<li>Gritos, xingamentos e humilhação em público.</li>
<li>Isolar a pessoa, excluir de reuniões, ignorar.</li>
<li>Tirar tarefas para "esvaziar" a função, ou dar tarefas impossíveis.</li>
<li>Expor metas e resultados para constranger.</li>
<li>Piadas sobre aparência, gravidez, origem ou cor.</li>
</ul>

<h2>Quais são os seus direitos</h2>

<ul>
<li><strong>Indenização por dano moral</strong>, a ser decidida pela Justiça do Trabalho (CLT, art. 223-B).</li>
<li><strong>Rescisão indireta</strong> nos casos graves: você sai e recebe as verbas como se tivesse sido demitida sem justa causa (CLT, art. 483).</li>
<li>A empresa <strong>responde</strong> pelos atos dos chefes e colegas (Código Civil, art. 932, III).</li>
</ul>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Empresas com CIPA são obrigadas a manter canal de denúncia e medidas contra o assédio (Lei 14.457/2022, art. 23). Usar esse canal também gera prova.</p>
</div>

<h2>Como provar o assédio moral (essa é a parte decisiva)</h2>

<table class="prova-table">
<tr><th>Prova</th><th>Como guardar</th></tr>
<tr><td>Diário dos fatos</td><td>Anote data, hora, local, o que foi dito e quem viu.</td></tr>
<tr><td>Mensagens e e-mails</td><td>Faça prints com data e o nome de quem enviou.</td></tr>
<tr><td>Áudios</td><td>Gravar a conversa da qual você participa é aceito como prova pela Justiça.</td></tr>
<tr><td>Testemunhas</td><td>Colegas que presenciaram os episódios.</td></tr>
<tr><td>Laudos médicos</td><td>Se o assédio te adoeceu, eles mostram o dano.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Um grito do chefe já é assédio moral?</h3>
<p>Depende do caso. Humilhação e exposição, principalmente quando se repetem, caracterizam assédio.</p>

<h3>Posso pedir demissão e receber tudo?</h3>
<p>Nos casos graves, pela rescisão indireta, você sai com as verbas de uma demissão sem justa causa.</p>

<h3>Posso gravar o chefe?</h3>
<p>Gravar uma conversa da qual você participa é aceito como prova pela Justiça.</p>

""" + _cta("Respeito não é favor. Se você está passando por isso,"),
    },
    {
        "data": "2026-12-14", "pauta": "Blog: 13º salário: como calcular a 2ª parcela e os descontos", "foto": "original-13-segunda-parcela.jpg", "cy": 0.32,
        "titulo": "13º salário: como calcular a 2ª parcela e os descontos",
        "slug": "13-salario-como-calcular-segunda-parcela-descontos",
        "meta": "A 2ª parcela do 13º sai até 18/12 em 2026 e traz todos os descontos. Veja como calcular, o que entra na conta e o que fazer se não pagarem.",
        "resumo": "Como calcular a 2ª parcela do 13º, por que ela vem menor e o que fazer se a empresa não pagar até 18/12.",
        "post_google": "A 2ª parcela do 13º sai até 18 de dezembro em 2026 e traz todos os descontos. No blog, mostramos como calcular e o que fazer se a empresa não pagar.",
        "html": """<p>A 1ª parcela do 13º caiu em novembro e foi um alívio. Agora chega a 2ª e o valor parece errado: bem menor do que você esperava.</p>

<p>Na maioria das vezes não é erro. Mas vale conferir, porque às vezes é.</p>

<p>Neste artigo eu explico, sem juridiquês, como a 2ª parcela é calculada e o que fazer se ela não vier. Vamos juntas.</p>

<h2>Qual é o prazo da 2ª parcela em 2026?</h2>

<p>O prazo legal é 20 de dezembro (Lei 4.749/1965, art. 1º). Em 2026, o dia 20 cai num domingo, então o pagamento precisa sair <strong>até sexta-feira, 18 de dezembro</strong>.</p>

<h2>Por que a 2ª parcela vem menor?</h2>

<p>Porque <strong>todos os descontos ficam nela</strong>. A 1ª parcela é metade do salário, sem desconto. Na 2ª, a empresa calcula o INSS e o imposto de renda sobre o 13º inteiro e desconta tudo de uma vez.</p>

<h2>Como calcular, passo a passo</h2>

<ol>
<li>Calcule o 13º total: salário dividido por 12, vezes o número de meses com 15 dias ou mais de trabalho.</li>
<li>Some a média das horas extras habituais, do adicional noturno e das comissões (Súmula 45 do TST).</li>
<li>Subtraia o que você recebeu na 1ª parcela.</li>
<li>Subtraia o INSS e o imposto de renda calculados sobre o 13º total.</li>
</ol>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Se a pensão alimentícia é um percentual do salário, ela também incide sobre o 13º (STJ, Tema 192). Esse desconto pode aparecer na 2ª parcela.</p>
</div>

<h2>E se a empresa não pagar?</h2>

<p>O atraso pode gerar multa administrativa para a empresa (Lei 7.855/1989, art. 3º), e o valor pode ser cobrado na Justiça do Trabalho. Antes disso, peça o cálculo por escrito ao RH.</p>

<h2>Como conferir (a parte que mais importa)</h2>

<table class="prova-table">
<tr><th>Separe</th><th>Para quê</th></tr>
<tr><td>Contracheques de novembro e dezembro</td><td>Mostram as duas parcelas e os descontos.</td></tr>
<tr><td>Registros de horas extras do ano</td><td>Conferir se a média entrou.</td></tr>
<tr><td>Extrato bancário</td><td>Comprova a data do depósito.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Quando cai a 2ª parcela do 13º em 2026?</h3>
<p>Até 18 de dezembro, porque o dia 20 é domingo.</p>

<h3>Por que a 2ª parcela é menor que a 1ª?</h3>
<p>Porque o INSS e o imposto de renda do 13º inteiro são descontados nela.</p>

<h3>Hora extra entra no 13º?</h3>
<p>Entra a média das horas extras habituais.</p>

""" + _cta("Conferir o 13º é direito seu. Se o valor não fecha e a empresa não explica,"),
    },
    {
        "data": "2026-12-17", "pauta": "Blog: Trabalho temporário de fim de ano: direitos e gestante", "foto": "original-temporaria-fim-de-ano.jpg", "cy": 0.35,
        "titulo": "Trabalho temporário de fim de ano: direitos e gestante",
        "slug": "trabalho-temporario-fim-de-ano-direitos-gestante",
        "meta": "Contratada para o fim de ano? Veja os direitos do trabalho temporário: salário igual, FGTS, 13º, férias proporcionais e estabilidade da gestante.",
        "resumo": "Salário igual, FGTS, 13º e férias proporcionais, e a estabilidade da gestante reconhecida pelo TST em 2026.",
        "post_google": "Contratada só para o fim de ano? O trabalho temporário tem salário igual ao da equipe, FGTS, 13º e férias proporcionais, e desde 2026 a gestante tem estabilidade. Leia no blog.",
        "html": """<p>Dezembro chegou e com ele a vaga temporária no comércio. É uma renda extra importante, mas vem a dúvida: temporária tem os mesmos direitos?</p>

<p>Tem muito mais do que se imagina. E, em 2026, a gestante ganhou uma proteção que não tinha.</p>

<p>Neste artigo eu explico, sem juridiquês, os direitos de quem trabalha no temporário de fim de ano. Vamos juntas.</p>

<h2>O que é trabalho temporário</h2>

<p>É a contratação feita por uma <strong>empresa de trabalho temporário</strong> (a agência) para atender a uma demanda extra, como o fim de ano. É regido pela Lei 6.019/1974. O contrato pode durar até 180 dias, prorrogáveis por mais 90 (art. 10).</p>

<h2>Quais são os direitos do temporário</h2>

<ul>
<li><strong>Salário equivalente</strong> ao de quem faz a mesma função na empresa (art. 12).</li>
<li><strong>Jornada de 8 horas</strong>, com hora extra paga com adicional.</li>
<li><strong>FGTS</strong> depositado todo mês.</li>
<li><strong>13º e férias proporcionais</strong>, com o terço.</li>
<li>Descanso semanal remunerado e adicional noturno.</li>
</ul>

<h2>Grávida no temporário tem estabilidade?</h2>

<p>Desde março de 2026, sim. O Pleno do TST mudou o entendimento que vinha desde 2019 e passou a reconhecer a <strong>estabilidade da gestante também no trabalho temporário</strong> (processo 1000059-12.2020.5.02.0382), com regras de transição para casos antigos.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Se a gravidez começou durante o contrato temporário, guarde o ultrassom com a idade gestacional: ele mostra que a proteção existe.</p>
</div>

<p>Para entender a estabilidade em detalhe, leia: <a href="estabilidade-gestante-contrato-de-experiencia-e-temporario.html">estabilidade da gestante no contrato de experiência e no trabalho temporário</a>.</p>

<h2>O que guardar (a parte decisiva)</h2>

<table class="prova-table">
<tr><th>Guarde</th><th>Por quê</th></tr>
<tr><td>Contrato com a agência</td><td>Mostra a função, as datas e o salário.</td></tr>
<tr><td>Recibos de pagamento</td><td>Para comparar com o salário da equipe.</td></tr>
<tr><td>Extrato do FGTS</td><td>Confere os depósitos.</td></tr>
<tr><td>Registro de ponto</td><td>Mostra as horas extras do fim de ano.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Temporário tem FGTS?</h3>
<p>Tem, depositado todo mês.</p>

<h3>Temporário recebe 13º?</h3>
<p>Recebe o 13º proporcional aos meses trabalhados.</p>

<h3>Gestante temporária tem estabilidade?</h3>
<p>Desde março de 2026, o TST reconhece a estabilidade também no trabalho temporário.</p>

""" + _cta("Contrato curto não diminui direitos. Se os seus não foram respeitados,"),
    },
    {
        "data": "2026-12-21", "pauta": "Blog: Trabalhar no Natal e no Ano Novo: o que diz a lei", "foto": "original-natal-ano-novo-feriado.jpg", "cy": 0.3,
        "titulo": "Trabalhar no Natal e no Ano Novo: o que diz a lei",
        "slug": "trabalhar-no-natal-e-ano-novo-o-que-diz-a-lei",
        "meta": "25/12 e 01/01 são feriados nacionais. Veja quando o trabalho é pago em dobro, como fica a escala 12x36 e se 24 e 31 de dezembro são feriados.",
        "resumo": "Natal e Ano Novo trabalhados: dobro ou folga, a regra da 12x36 e por que 24 e 31 não são feriados nacionais.",
        "post_google": "Vai trabalhar no Natal ou no Ano Novo? Explicamos no blog quando o feriado é pago em dobro, como fica a escala 12x36 e se 24 e 31 de dezembro são feriados.",
        "html": """<p>Enquanto a família se reúne, você está de plantão, no caixa ou na portaria. Trabalhar no Natal e no Ano Novo faz parte da vida de muita gente.</p>

<p>E tem regra. Saber qual é evita surpresa no contracheque de janeiro.</p>

<p>Neste artigo eu explico, sem juridiquês, o que a lei diz sobre trabalhar nas festas de fim de ano. Vamos juntas.</p>

<h2>Natal e Ano Novo são feriados?</h2>

<p>Sim. <strong>25 de dezembro e 1º de janeiro</strong> são feriados nacionais (Lei 662/1949). Já <strong>24 e 31 de dezembro não são</strong> feriados nacionais: são dias normais de trabalho, salvo lei municipal, estadual ou convenção coletiva que diga o contrário.</p>

<h2>Trabalhei no feriado. Recebo em dobro?</h2>

<p>Recebe, se a empresa não der outro dia de folga. O trabalho em feriado é pago <strong>em dobro</strong>, além do repouso (Lei 605/1949, art. 9º; Súmula 146 do TST). Se a empresa der uma folga em outro dia, o dobro não é devido.</p>

<h2>E na escala 12x36?</h2>

<p>Na escala 12x36, a lei considera que o salário mensal já inclui os feriados trabalhados (CLT, art. 59-A, parágrafo único). Por isso, em regra, não há pagamento em dobro. Confira a convenção coletiva da sua categoria: algumas garantem mais.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>No comércio, trabalhar em feriado depende de autorização em convenção coletiva (Lei 10.101/2000, art. 6º-A). Vale ler a da sua categoria.</p>
</div>

<h2>Como conferir (a parte que mais importa)</h2>

<table class="prova-table">
<tr><th>Separe</th><th>Para quê</th></tr>
<tr><td>Registro de ponto de 25/12 e 01/01</td><td>Prova que você trabalhou no feriado.</td></tr>
<tr><td>Escala de dezembro</td><td>Mostra se houve folga compensatória.</td></tr>
<tr><td>Contracheque de janeiro</td><td>Confere se o dobro foi pago.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Trabalhar no Natal paga em dobro?</h3>
<p>Paga, se a empresa não der outro dia de folga.</p>

<h3>24 de dezembro é feriado?</h3>
<p>Não é feriado nacional. Pode ser por lei local ou convenção.</p>

<h3>Quem trabalha 12x36 recebe o feriado em dobro?</h3>
<p>Em regra, não: a lei considera o feriado compensado na escala.</p>

""" + _cta("Feriado trabalhado tem regra. Se o seu não foi pago,"),
    },
    {
        "data": "2026-12-24", "pauta": "Blog: Viagem com filhos nas férias: autorização de viagem", "foto": "original-viagem-com-filhos.jpg", "cy": 0.4,
        "titulo": "Viagem com filhos nas férias: quando precisa de autorização",
        "slug": "viagem-com-filhos-nas-ferias-autorizacao",
        "meta": "Pais separados podem viajar com os filhos? Veja quando precisa de autorização para viagem nacional e internacional e o que levar.",
        "resumo": "Viagem nacional, internacional e com terceiros: quando precisa de autorização do outro genitor ou do juiz.",
        "post_google": "Vai viajar com os filhos nas férias? Dentro do Brasil, com o pai ou a mãe, não precisa de autorização do outro; para o exterior, precisa. Explicamos tudo no blog.",
        "html": """<p>As malas estão quase prontas, as crianças contando os dias. Aí vem a dúvida: como sou separada, preciso da autorização do pai para viajar com meu filho?</p>

<p>Depende do destino e de com quem a criança vai.</p>

<p>Neste artigo eu explico, sem juridiquês, quando a viagem precisa de autorização. Vamos juntas.</p>

<h2>Viagem dentro do Brasil com o pai ou a mãe</h2>

<p>Criança ou adolescente com até 16 anos que viaja <strong>dentro do Brasil acompanhado do pai ou da mãe</strong> não precisa de autorização do outro genitor (ECA, art. 83). Basta levar documento com foto e, de preferência, a certidão de nascimento.</p>

<h2>Viagem sem os pais</h2>

<p>Menor de 16 anos que viaja para fora da comarca <strong>sem os pais</strong> precisa de autorização: dos pais (com firma reconhecida) ou do juiz (ECA, art. 83; Resolução CNJ 295/2019). Se for com parente até o terceiro grau, como avós e tios, basta comprovar o parentesco.</p>

<h2>Viagem para o exterior</h2>

<p>Para viajar ao exterior com só um dos pais, é preciso <strong>autorização do outro genitor</strong>, por escrito e com firma reconhecida, ou autorização do juiz (ECA, art. 84; Resolução CNJ 131/2011). A autorização também pode constar no passaporte.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Mesmo sem precisar de autorização, a viagem deve respeitar as datas de convivência combinadas ou decididas pelo juiz (Código Civil, art. 1.589). Viajar no período do outro genitor exige acordo.</p>
</div>

<h2>O que levar (a parte prática)</h2>

<table class="prova-table">
<tr><th>Documento</th><th>Quando</th></tr>
<tr><td>Documento com foto da criança</td><td>Sempre.</td></tr>
<tr><td>Certidão de nascimento</td><td>Comprova a filiação.</td></tr>
<tr><td>Autorização com firma reconhecida</td><td>Exterior com um só genitor, ou viagem sem os pais.</td></tr>
<tr><td>Acordo ou decisão da guarda</td><td>Para mostrar as datas combinadas, se houver conflito.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Preciso de autorização do pai para viajar com meu filho no Brasil?</h3>
<p>Não, se você estiver acompanhando a criança.</p>

<h3>E para o exterior?</h3>
<p>Precisa da autorização do outro genitor, com firma reconhecida, ou do juiz.</p>

<h3>O pai não autoriza a viagem ao exterior. E agora?</h3>
<p>É possível pedir a autorização ao juiz.</p>

""" + _cta("Férias boas começam combinadas. Se a viagem virou conflito,"),
    },
    {
        "data": "2026-12-28", "pauta": "Blog: Pensão alimentícia em 2027: reajuste pelo salário mínimo", "foto": "original-pensao-reajuste.jpg", "cy": 0.32,
        "titulo": "Pensão alimentícia em 2027: reajuste pelo salário mínimo",
        "slug": "pensao-alimenticia-2027-reajuste-salario-minimo",
        "meta": "A pensão fixada em salário mínimo sobe sozinha em janeiro. Veja como fica cada tipo de pensão em 2027 e o que fazer se pagarem o valor antigo.",
        "resumo": "Como fica o reajuste da pensão em janeiro de 2027: salário mínimo, percentual do salário ou valor fixo.",
        "post_google": "A pensão fixada em salário mínimo sobe sozinha em janeiro. No blog, explicamos como fica cada tipo de pensão em 2027 e o que fazer se pagarem o valor antigo.",
        "html": """<p>Janeiro chega, o salário mínimo muda e o depósito da pensão do seu filho continua igual. Está certo?</p>

<p>Depende de como a pensão foi fixada. Em muitos casos, o valor deveria ter subido sozinho.</p>

<p>Neste artigo eu explico, sem juridiquês, como funciona o reajuste da pensão em 2027. Vamos juntas.</p>

<h2>Pensão em percentual do salário mínimo</h2>

<p>É a forma mais comum quando quem paga não tem emprego formal. Nesse caso, a pensão <strong>acompanha o reajuste do salário mínimo automaticamente</strong>, a partir de janeiro, sem precisar de novo processo. A jurisprudência do STF e do STJ admite essa forma de fixação justamente por isso.</p>

<h2>Pensão em percentual do salário de quem paga</h2>

<p>Acompanha o salário: se ele aumenta, a pensão aumenta. E o desconto vale também sobre o 13º e o terço de férias (STJ, Tema 192).</p>

<h2>Pensão em valor fixo</h2>

<p>Só muda pelo índice de correção previsto no acordo ou na decisão. Sem índice, o caminho é o pedido de revisão, quando muda a necessidade de quem recebe ou a possibilidade de quem paga (Código Civil, art. 1.699).</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Se a pensão é em salário mínimo e continuou sendo paga pelo valor antigo, a <strong>diferença pode ser cobrada</strong> na Justiça (CPC, art. 528).</p>
</div>

<h2>Como conferir (a parte que mais importa)</h2>

<table class="prova-table">
<tr><th>Separe</th><th>Para quê</th></tr>
<tr><td>A decisão ou o acordo da pensão</td><td>Mostra a forma de fixação.</td></tr>
<tr><td>Extratos dos depósitos</td><td>Mostram o valor pago a cada mês.</td></tr>
<tr><td>O valor do novo salário mínimo</td><td>Base para calcular a diferença.</td></tr>
</table>

<p>Para entender a revisão em detalhe, leia: <a href="revisao-de-pensao-alimenticia-quando-o-valor-pode-mudar.html">revisão de pensão alimentícia: quando o valor pode mudar</a>.</p>

<h2>Perguntas frequentes</h2>

<h3>A pensão em salário mínimo aumenta em janeiro?</h3>
<p>Aumenta automaticamente, junto com o novo salário mínimo.</p>

<h3>Pensão em valor fixo aumenta?</h3>
<p>Só pelo índice previsto ou com pedido de revisão.</p>

<h3>Continuaram pagando o valor antigo. Posso cobrar?</h3>
<p>Pode cobrar a diferença na Justiça.</p>

""" + _cta("A pensão é do seu filho, com reajuste. Se o depósito veio errado,"),
    },
    {
        "data": "2026-12-31", "pauta": "Blog: O que muda em 2027 para quem trabalha e para as mães", "foto": "original-licenca-paternidade-2027.jpg", "cy": 0.62,
        "titulo": "O que muda em 2027 para quem trabalha e para as mães",
        "slug": "o-que-muda-em-2027-trabalhadores-e-maes",
        "meta": "Licença-paternidade de 10 dias, novas regras da aposentadoria da mulher e o reajuste da pensão: o que muda em 2027 para quem trabalha e para as mães.",
        "resumo": "Licença-paternidade maior, aposentadoria da mulher com novas regras e pensão reajustada: o que muda em 2027.",
        "post_google": "2027 começa com mudanças: licença-paternidade de 10 dias, novas regras na aposentadoria da mulher e pensão reajustada. Resumimos tudo no blog.",
        "html": """<p>Ano novo, regras novas. Algumas mudanças de 2027 mexem direto com a vida de quem trabalha e de quem cuida dos filhos.</p>

<p>Separei as principais para você começar o ano informada.</p>

<p>Neste artigo eu explico, sem juridiquês, o que muda em 2027. Vamos juntas.</p>

<h2>Licença-paternidade passa para 10 dias</h2>

<p>A Lei 15.371/2026 amplia a licença-paternidade aos poucos: <strong>10 dias a partir de 1º de janeiro de 2027</strong>, 15 dias em 2028 e 20 dias em 2029, se cumpridas as metas fiscais. A lei também cria o <strong>salário-paternidade</strong>: a empresa paga e é reembolsada pelo INSS. Vale para nascimento, adoção e guarda para adoção.</p>

<h2>Aposentadoria da mulher: regras de transição sobem</h2>

<ul>
<li><strong>Pontos</strong>: 94 em 2027 (idade + tempo de contribuição), com 30 anos de contribuição (EC 103/2019, art. 15).</li>
<li><strong>Idade mínima progressiva</strong>: 60 anos, com 30 anos de contribuição (art. 16).</li>
<li><strong>Por idade</strong>: continua 62 anos e 15 de contribuição (art. 18).</li>
</ul>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Quem completou os requisitos de alguma regra em 2026 <strong>mantém o direito</strong>, mesmo que peça a aposentadoria depois. Vale fazer a simulação no Meu INSS.</p>
</div>

<h2>Pensão em salário mínimo sobe em janeiro</h2>

<p>Quando a pensão foi fixada em percentual do salário mínimo, ela acompanha o novo mínimo automaticamente. Detalhes em: <a href="pensao-alimenticia-2027-reajuste-salario-minimo.html">pensão alimentícia em 2027</a>.</p>

<h2>O que continua igual para a gestante</h2>

<p>A estabilidade da gestante, a licença-maternidade de 120 dias (ou 180 na Empresa Cidadã) e as pausas para amamentar continuam valendo. O guia completo está em: <a href="direitos-da-gestante-clt-guia-completo.html">direitos da gestante CLT</a>.</p>

<h2>Organize-se para 2027 (a parte prática)</h2>

<table class="prova-table">
<tr><th>Tarefa</th><th>Por quê</th></tr>
<tr><td>Baixar o extrato do CNIS</td><td>Conferir o tempo de contribuição antes de pedir aposentadoria.</td></tr>
<tr><td>Avisar o RH sobre o nascimento</td><td>Garantir a licença-paternidade de 10 dias.</td></tr>
<tr><td>Conferir o depósito da pensão de janeiro</td><td>Ver se o reajuste foi aplicado.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Quantos dias de licença-paternidade em 2027?</h3>
<p>10 dias, a partir de 1º de janeiro.</p>

<h3>Quantos pontos a mulher precisa em 2027?</h3>
<p>94, com 30 anos de contribuição.</p>

<h3>Completei os requisitos em 2026. Perco o direito?</h3>
<p>Não. É direito adquirido.</p>

""" + _cta("Feliz 2027. Se alguma dessas mudanças mexe com o seu caso,"),
    },
]

# Seções extras (erros comuns, prazos, exemplos) antes de "Perguntas frequentes".
from artigos_dez_extras import EXTRAS  # noqa: E402

for _a in ARTIGOS:
    if _a["slug"] in EXTRAS:
        _a["html"] = _a["html"].replace("<h2>Perguntas frequentes</h2>", EXTRAS[_a["slug"]] + "<h2>Perguntas frequentes</h2>", 1)
