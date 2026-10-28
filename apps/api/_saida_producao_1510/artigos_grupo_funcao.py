"""Grupo "O que a empresa pode exigir de você" (27/10/2026, pedido "rankear mais no Google e furar a bolha").

Por quê: a página do banheiro/desvio de função é a mais vista do site (2.583 aparições em 28 dias, posição 5,7) e
as buscas que caem nela são de trabalhador em geral, homem e mulher ("atendente pode lavar banheiro", "operador de
loja pode fazer limpeza"). Este grupo aproveita essa confiança do Google com 5 artigos ligados entre si, nas quintas
de 29/10 a 26/11 (as segundas seguem com o grupo Gestante já aprovado). Temas escolhidos pelos dados do Search
Console e pelos assuntos trabalhistas mais procurados em 2026 (FGTS, hora extra, jornada depois da EC 141).

Fatos conferidos em 27/10/2026: CLT arts. 58, 59, 59-B, 74, 456, 462, 483; CF art. 7º, XIII, XVI, XXIX; EC 141/2026
(planalto.gov.br); Lei 8.036/1990, art. 15 (depósito até o dia 20); TST Tema 70 (FGTS e rescisão indireta, sem
imediatidade, 24/02/2025); Súmulas 146, 338, 342 e 431 e OJ 125 da SDI-1 do TST; Lei 3.207/1957, art. 8º.
Valores em reais escritos por extenso ("2.200 reais") para não confundir com anúncio de preço (conformidade_oab).
"""

B = "https://advogadaleticiabarros.com.br/blog/"
PILAR = '<a href="empresa-pode-obrigar-limpar-banheiro.html">atendente pode ser obrigada a lavar banheiro?</a>'


def _cta(frase: str) -> str:
    return f"<h2>Se essa é a sua situação</h2>\n\n<p>{frase} Procure uma advogada de confiança.</p>"


ARTIGOS = [
    {
        "data": "2026-10-29", "pauta": "Blog: Acúmulo de função: tenho direito a aumento de salário?",
        "foto": "original-acumulo-de-funcao.jpg", "cy": 0.45, "kicker": "Seus direitos no trabalho",
        "titulo": "Acúmulo de função: tenho direito a aumento de salário?",
        "slug": "acumulo-de-funcao-tenho-direito-a-aumento",
        "meta": "Faz o trabalho de dois e ganha por um? Veja quando o acúmulo de função dá direito a diferença salarial, o que diz o TST e como provar.",
        "resumo": "Quando fazer tarefas de outro cargo dá direito a receber mais, quando não dá, e como provar o acúmulo de função.",
        "post_google": "Faz o trabalho de dois e recebe por um? Explicamos no blog quando o acúmulo de função dá direito a diferença salarial, a diferença para o desvio de função e como guardar as provas.",
        "html": """<p>Você foi contratado como vendedor. Hoje também abre a loja, faz o caixa, recebe mercadoria e ainda cuida do estoque. A colega que fazia isso saiu e ninguém foi contratado no lugar.</p>

<p>O salário? O mesmo de quando você só vendia.</p>

<p>Essa é uma das dúvidas que mais chegam ao escritório: "estou fazendo o trabalho de dois, tenho direito a ganhar mais?". Neste artigo eu explico, sem juridiquês, quando a resposta é sim, quando é não, e o que fazer para não perder esse direito. Vamos juntos.</p>

<div class="callout-box">
<h4>Resposta rápida</h4>
<p>Nem todo acúmulo de função dá direito a aumento. A CLT diz que o empregado faz todo serviço compatível com o cargo (art. 456, parágrafo único). O direito a receber mais aparece quando a convenção coletiva ou uma lei da sua profissão prevê adicional, quando você assume tarefas de um cargo mais bem pago ou de complexidade maior, ou quando, na prática, você passou a ocupar outra função.</p>
</div>

<h2>Acúmulo de função e desvio de função não são a mesma coisa</h2>

<p>É aqui que muita gente se confunde, então vou explicar por contraste.</p>

<ul>
<li><strong>Desvio de função</strong>: você deixa de fazer o seu trabalho e passa a fazer o de outro cargo. Foi contratada como recepcionista e virou, na prática, auxiliar administrativa. O TST reconhece o direito às <strong>diferenças salariais</strong> do período (Orientação Jurisprudencial 125 da SDI-1), mesmo sem mudar o cargo na carteira.</li>
<li><strong>Acúmulo de função</strong>: você continua fazendo o seu trabalho e <strong>soma</strong> tarefas de outro cargo, na mesma jornada.</li>
</ul>

<p>O caso mais comum de desvio é o que eu explico no artigo sobre <a href="empresa-pode-obrigar-limpar-banheiro.html">quando a empresa obriga a lavar banheiro</a>. Aqui o assunto é o acúmulo.</p>

<h2>O que diz a CLT</h2>

<p>A CLT não tem uma regra geral de "plus salarial" para quem acumula funções. O artigo 456, parágrafo único, diz que, se o contrato não fala nada, o empregado se obriga a todo serviço <strong>compatível com a sua condição pessoal</strong>.</p>

<p>Traduzindo: tarefas parecidas, do mesmo nível, feitas dentro do horário, em regra não geram salário extra. O vendedor que arruma a vitrine, a atendente que repõe o balcão, o motorista que confere a nota da entrega.</p>

<h2>Quando o acúmulo dá direito a receber mais</h2>

<h3>1. A convenção coletiva ou uma lei da profissão prevê adicional</h3>
<p>Muitas convenções coletivas preveem um percentual para quem acumula funções. Algumas profissões têm lei própria: o vendedor que também faz inspeção ou fiscalização tem direito a um acréscimo de 10% da remuneração (Lei 3.207/1957, art. 8º), e os radialistas também têm adicional por acúmulo em lei específica. Por isso, a primeira coisa a conferir é a convenção da sua categoria.</p>

<h3>2. A tarefa somada é de um cargo mais bem pago ou mais complexo</h3>
<p>Quando você assume responsabilidades de outro nível (por exemplo, passa a responder pelo caixa e pela abertura e fechamento da loja, com chave e valores), a Justiça do Trabalho tem reconhecido diferenças salariais, porque a tarefa não é "compatível" com o cargo de origem.</p>

<h3>3. Na prática, você ocupa dois cargos</h3>
<p>Se a empresa extinguiu um cargo e passou tudo para você, de forma fixa, o caso fica mais perto do desvio de função, e o pedido é pela diferença entre o seu salário e o do cargo que você assumiu.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>O que decide não é o nome do cargo na carteira. É o que você faz <strong>todo dia</strong>, comparado com o que foi combinado na contratação e com o que a convenção coletiva diz.</p>
</div>

<h2>Como provar o acúmulo (essa é a parte que mais importa)</h2>

<p>É na prova que muita gente desiste, e eu não quero que você desista. Comece hoje:</p>

<table class="prova-table">
<tr><th>Guarde</th><th>Para quê</th></tr>
<tr><td>Mensagens e e-mails com as ordens</td><td>Mostram quem mandou fazer a tarefa e desde quando.</td></tr>
<tr><td>Escalas, checklists e relatórios com o seu nome</td><td>Provam que a tarefa era sua de forma fixa, não um favor de um dia.</td></tr>
<tr><td>Descrição do cargo, anúncio da vaga ou contrato</td><td>Mostram o que foi combinado na contratação.</td></tr>
<tr><td>Convenção coletiva da categoria</td><td>Diz se existe adicional por acúmulo e qual o piso de cada função.</td></tr>
<tr><td>Nome de colegas que viram</td><td>Testemunhas costumam ser a prova mais forte nesse tema.</td></tr>
</table>

<h2>Até quando dá para cobrar</h2>

<p>Enquanto trabalha na empresa, você pode cobrar os últimos <strong>5 anos</strong>. Depois que sai, o prazo para entrar com a ação é de <strong>2 anos</strong> (Constituição, art. 7º, XXIX). Passou disso, o direito se perde.</p>

<h2>Perguntas frequentes</h2>

<h3>Acúmulo de função dá direito a quanto de aumento?</h3>
<p>Não existe percentual fixo na CLT. Quando há direito, o valor vem da convenção coletiva, da lei da profissão ou da diferença para o salário do cargo assumido. Cada caso precisa ser avaliado.</p>

<h3>Posso me recusar a fazer a tarefa de outro cargo?</h3>
<p>Recusar sem orientação pode gerar advertência. O caminho mais seguro é registrar por escrito, perguntar ao RH quais são as suas atribuições e guardar a resposta.</p>

<h3>Caixa que também repõe mercadoria tem direito a mais?</h3>
<p>Depende da convenção coletiva do comércio da sua cidade e de quanto do seu dia vai para a outra tarefa. Repor o próprio posto, em regra, não. Assumir o estoque da loja de forma fixa pode mudar a resposta.</p>

<h3>Acúmulo de função dá rescisão indireta?</h3>
<p>Exigir serviços alheios ao contrato está entre as faltas da empresa que permitem a <a href="rescisao-indireta-o-que-e-quando-tenho-direito.html">rescisão indireta</a> (CLT, art. 483, "a"). Mas é um passo sério, que precisa de prova e de orientação antes.</p>

<p>Leia também: <a href="funcoes-da-recepcionista-o-que-pode-ser-exigido.html">funções da recepcionista: o que a empresa pode exigir</a>.</p>

""" + _cta("Fazer o trabalho de dois não é \"vestir a camisa\" sem limite. Se a sua rotina mudou e o salário ficou igual,"),
    },
    {
        "data": "2026-11-05", "pauta": "Blog: FGTS não depositado: como consultar e o que fazer",
        "foto": "original-fgts-nao-depositado.jpg", "cy": 0.4, "kicker": "FGTS",
        "titulo": "FGTS não depositado: como consultar e o que fazer",
        "slug": "fgts-nao-depositado-como-consultar-e-o-que-fazer",
        "meta": "Abriu o app e o FGTS não caiu? Veja como consultar os depósitos, o prazo da empresa, o que o TST decidiu e como cobrar os valores atrasados.",
        "resumo": "Como conferir os depósitos do FGTS no aplicativo, o que fazer quando a empresa não deposita e quando isso permite a rescisão indireta.",
        "post_google": "A empresa desconta, mas o FGTS não aparece no aplicativo? Explicamos no blog como consultar os depósitos, o prazo da empresa e o que a lei permite fazer quando ela não deposita.",
        "html": """<p>Você abriu o aplicativo do FGTS para ver o saldo e levou um susto: há meses sem depósito. O contracheque mostra tudo certinho, mas o dinheiro não está lá.</p>

<p>Muita gente só descobre isso na hora de sacar, quando é demitida ou vai comprar a casa própria. E aí vem a pergunta: e agora, perdi esse dinheiro?</p>

<p>Não perdeu. Neste artigo eu explico, sem juridiquês, como conferir os depósitos, qual é o prazo da empresa e o que a lei permite fazer. Vamos juntas.</p>

<div class="callout-box">
<h4>Resposta rápida</h4>
<p>A empresa precisa depositar <strong>8% do seu salário</strong> todo mês na conta do FGTS, até o dia 20 do mês seguinte (Lei 8.036/1990, art. 15). Você confere no aplicativo FGTS, da Caixa. Se faltar depósito, dá para cobrar na Justiça do Trabalho os últimos 5 anos e, segundo tese do TST de 2025, a falta de depósito já é motivo suficiente para a rescisão indireta.</p>
</div>

<h2>Como consultar se o FGTS foi depositado</h2>

<ol>
<li>Baixe o aplicativo <strong>FGTS</strong> (da Caixa) e entre com a sua conta gov.br.</li>
<li>Abra "Meus FGTS" e escolha a conta da empresa atual.</li>
<li>Veja o <strong>extrato</strong>: cada mês precisa ter um depósito, perto de 8% do salário bruto.</li>
<li>Compare com os contracheques. Faltou mês? Anote quais.</li>
</ol>

<p>Faça isso a cada três meses. Quanto antes você percebe, menor a dívida e mais fácil a cobrança.</p>

<h2>Quanto a empresa precisa depositar</h2>

<ul>
<li><strong>8% da remuneração</strong> por mês, incluindo horas extras, adicionais e comissões, e também sobre o 13º.</li>
<li><strong>2%</strong> para o jovem aprendiz.</li>
<li>Para a empregada doméstica, 8% mais 3,2% de uma reserva para a multa de demissão.</li>
</ul>

<p>Esse dinheiro é seu. Ele não sai do seu salário: é um custo da empresa, depositado por fora.</p>

<h2>O que fazer quando o FGTS não foi depositado</h2>

<h3>1. Guarde a prova</h3>
<p>Tire print do extrato do aplicativo e guarde os contracheques do mesmo período.</p>

<h3>2. Pergunte por escrito</h3>
<p>Mande um e-mail ou mensagem ao RH pedindo a regularização. Às vezes é erro. Se não for, a resposta (ou o silêncio) também vira prova.</p>

<h3>3. Denuncie, se quiser</h3>
<p>Você pode registrar uma denúncia trabalhista no gov.br, para a fiscalização do Ministério do Trabalho cobrar a empresa. A denúncia não depende de processo.</p>

<h3>4. Cobre na Justiça do Trabalho</h3>
<p>A ação pede que a empresa deposite tudo o que ficou para trás, com correção. O TST também já firmou que um parcelamento da dívida da empresa com a Caixa não impede o trabalhador de cobrar os valores dele.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Em fevereiro de 2025, o TST fixou tese vinculante (Tema 70): deixar de depositar o FGTS é falta grave da empresa e basta para a <a href="rescisao-indireta-o-que-e-quando-tenho-direito.html">rescisão indireta</a>, a "justa causa da empresa". E o trabalhador <strong>NÃO PRECISA</strong> ter reclamado na hora: pode agir mesmo depois de meses de atraso.</p>
</div>

<h2>Rescisão indireta: o que você recebe</h2>

<p>Se a rescisão indireta for reconhecida, você sai como se tivesse sido demitida sem justa causa: aviso prévio, férias e 13º proporcionais, saque do FGTS com a multa de 40% e acesso ao seguro-desemprego. A multa é calculada sobre tudo o que <strong>deveria</strong> estar depositado, não só sobre o que está na conta.</p>

<p>É um passo sério. Antes de sair do emprego, busque orientação: sair por conta própria sem a prova certa pode virar pedido de demissão.</p>

<h2>Até quando dá para cobrar</h2>

<p>Os depósitos dos últimos <strong>5 anos</strong>, e até <strong>2 anos</strong> depois de sair da empresa (STF, ARE 709.212, e Constituição, art. 7º, XXIX).</p>

<h2>Como provar (a parte que mais importa)</h2>

<table class="prova-table">
<tr><th>Guarde</th><th>Para quê</th></tr>
<tr><td>Extrato do aplicativo FGTS</td><td>Mostra mês a mês o que foi e o que não foi depositado.</td></tr>
<tr><td>Contracheques</td><td>Mostram o salário de cada mês e a base do cálculo.</td></tr>
<tr><td>Mensagens com o RH</td><td>Mostram que você pediu e a empresa não resolveu.</td></tr>
</table>

<h2>Perguntas frequentes</h2>

<h3>Como saber se a empresa está depositando o meu FGTS?</h3>
<p>Pelo aplicativo FGTS, da Caixa, no extrato da conta da empresa atual. Cada mês trabalhado precisa ter um depósito.</p>

<h3>A empresa pode parcelar o FGTS atrasado e eu esperar?</h3>
<p>A empresa pode negociar com a Caixa, mas isso não impede você de cobrar na Justiça do Trabalho.</p>

<h3>FGTS não depositado dá direito a rescisão indireta?</h3>
<p>Sim. O TST decidiu em 2025, em tese vinculante, que a falta ou irregularidade dos depósitos basta para a rescisão indireta, sem exigir reação imediata.</p>

<h3>Perdi o FGTS se a empresa fechou?</h3>
<p>Não necessariamente. A dívida pode ser cobrada da empresa e, em alguns casos, dos sócios. Cada caso precisa ser avaliado.</p>

<p>Leia também: <a href="fgts-trabalhador-temporario-direitos-e-como-cobrar.html">FGTS do trabalhador temporário</a> e <a href="multa-artigo-477-clt-um-salario-a-mais.html">multa do art. 477 por atraso na rescisão</a>.</p>

""" + _cta("O FGTS é seu, e a falta de depósito não é detalhe. Se o extrato não bate com os seus contracheques,"),
    },
    {
        "data": "2026-11-12", "pauta": "Blog: Hora extra não paga: como calcular e como provar",
        "foto": "original-hora-extra-nao-paga.jpg", "cy": 0.45, "kicker": "Jornada de trabalho",
        "titulo": "Hora extra não paga: como calcular e como provar",
        "slug": "hora-extra-nao-paga-como-calcular-e-provar",
        "meta": "Trabalha além do horário e não recebe? Veja como calcular a hora extra, o adicional de 50% ou em dobro, os reflexos e as provas que valem.",
        "resumo": "Como calcular a hora extra, quanto vale o adicional, o que entra nos reflexos e como provar a jornada que não está no ponto.",
        "post_google": "Trabalha além do horário e a hora extra não aparece no contracheque? Explicamos no blog como calcular, quanto vale o adicional e quais provas a Justiça aceita.",
        "html": """<p>O expediente acaba às 18h. Mas você sai às 19h30, quase todo dia. Às vezes o chefe pede para bater o ponto e "terminar só aquilo". No fim do mês, a hora extra não aparece no contracheque.</p>

<p>Parece pouco, uma hora aqui, meia hora ali. Em um ano, vira um salário inteiro que ficou para trás.</p>

<p>Neste artigo eu explico, sem juridiquês, como calcular a hora extra, o que entra na conta e, principalmente, como provar. Vamos juntos.</p>

<div class="callout-box">
<h4>Resposta rápida</h4>
<p>Hora extra é todo tempo trabalhado além da sua jornada (em regra, 8 horas por dia e 44 por semana, limite que cai para 42 em 16/12/2026 com a Emenda Constitucional 141). Ela vale <strong>no mínimo 50% a mais</strong> que a hora normal, e em dobro em domingos e feriados não compensados. Se a empresa não paga, dá para cobrar os últimos 5 anos, com reflexos em férias, 13º e FGTS.</p>
</div>

<h2>Como calcular a sua hora extra</h2>

<ol>
<li><strong>Valor da hora normal</strong>: divida o salário pelo divisor da sua jornada. Para 44 horas semanais, o divisor é 220. Para 40 horas, é 200 (Súmula 431 do TST).</li>
<li><strong>Valor da hora extra</strong>: some o adicional. Com 50%, multiplique por 1,5.</li>
<li><strong>Total do mês</strong>: multiplique pelo número de horas extras.</li>
</ol>

<div class="callout-box">
<h4>Exemplo prático</h4>
<p>Salário de 2.200 reais, jornada de 44 horas: a hora normal vale 10 reais (2.200 ÷ 220). A hora extra com 50% vale 15 reais. Uma hora e meia a mais por dia, em 22 dias, são 33 horas extras: 495 reais no mês, fora os reflexos.</p>
</div>

<h2>Adicional de 50% ou em dobro?</h2>

<ul>
<li><strong>50%, no mínimo</strong>, em dias úteis (Constituição, art. 7º, XVI). A convenção coletiva pode prever mais.</li>
<li><strong>Em dobro</strong> no domingo e no feriado trabalhados sem folga compensatória (Súmula 146 do TST).</li>
<li>O limite é de <strong>2 horas extras por dia</strong> (CLT, art. 59). Passar disso não tira o seu direito de receber: só mostra que a empresa descumpriu a lei.</li>
</ul>

<h2>Os reflexos: o que mais entra na conta</h2>

<p>Quem faz hora extra com frequência recebe também a diferença em:</p>

<ul>
<li>descanso semanal remunerado;</li>
<li>férias com o terço;</li>
<li>13º salário;</li>
<li>FGTS (e a multa de 40%, se você for demitido sem justa causa);</li>
<li>aviso prévio.</li>
</ul>

<p>Por isso o valor final costuma ser bem maior do que a soma das horas.</p>

<h2>O que muda com o fim da escala 6x1</h2>

<p>Com a <a href="fim-da-escala-6x1-o-que-muda-e-quando-comeca.html">Emenda Constitucional 141</a>, a jornada máxima cai para 42 horas em 16 de dezembro de 2026 e para 40 horas um ano depois, sem redução de salário. O que passar do novo limite é hora extra. Se a empresa mantiver o horário antigo depois dessas datas, as horas a mais precisam ser pagas ou compensadas de forma válida. Veja também a <a href="carga-horaria-maxima-clt.html">carga horária máxima na CLT</a>.</p>

<h2>Como provar a hora extra (essa é a parte decisiva)</h2>

<p>A empresa com mais de 20 empregados é obrigada a controlar o ponto (CLT, art. 74, § 2º). Se ela não apresentar os cartões no processo sem justificativa, a Justiça presume verdadeira a jornada que você contou, até prova em contrário (Súmula 338 do TST). E ponto com horário igual todo dia, "certinho demais", não vale como prova.</p>

<p>Mesmo assim, não dependa só do ponto. Guarde:</p>

<table class="prova-table">
<tr><th>Guarde</th><th>Para quê</th></tr>
<tr><td>Mensagens e e-mails enviados depois do horário</td><td>Têm data e hora, e mostram que você estava trabalhando.</td></tr>
<tr><td>Anotação diária da hora de entrada e saída</td><td>Feita na hora, num caderno ou no celular, ajuda a reconstruir a jornada.</td></tr>
<tr><td>Registros de sistema, login e entregas</td><td>Mostram atividade fora do horário oficial.</td></tr>
<tr><td>Nome de colegas que saíam junto</td><td>Testemunhas confirmam a rotina.</td></tr>
</table>

<h2>Quem não recebe hora extra</h2>

<p>A CLT exclui do controle de jornada quem tem cargo de gestão de verdade, com poder de decisão e gratificação de pelo menos 40% (art. 62, II), e algumas atividades externas sem como controlar o horário (art. 62, I). Mas o nome "gerente" no crachá não basta: o que vale é o poder real.</p>

<h2>Se você é empresa</h2>

<p>Ajuste o controle de ponto antes de 16/12/2026, revise escalas e acordos de compensação para a nova jornada e não mude salários. Hora extra habitual não registrada é um dos pedidos mais comuns nas ações trabalhistas.</p>

<h2>Perguntas frequentes</h2>

<h3>Como calcular hora extra de 50%?</h3>
<p>Divida o salário por 220 (jornada de 44 horas) para achar a hora normal e multiplique por 1,5. Depois, multiplique pelo número de horas extras.</p>

<h3>Até quando posso cobrar hora extra?</h3>
<p>Os últimos 5 anos, com ação proposta em até 2 anos depois de sair da empresa (Constituição, art. 7º, XXIX).</p>

<h3>A empresa pode pagar hora extra com folga?</h3>
<p>Pode, se houver acordo de compensação ou banco de horas válido, dentro dos prazos da lei. Sem isso, as horas precisam ser pagas.</p>

<h3>Mensagem de WhatsApp fora do horário conta como hora extra?</h3>
<p>Pode contar, se você precisava responder e ficava à disposição. Veja <a href="assedio-moral-digital-cobranca-fora-do-horario-de-trabalho.html">cobrança fora do horário pelo WhatsApp</a>.</p>

<p>Leia também: <a href="acumulo-de-funcao-tenho-direito-a-aumento.html">acúmulo de função: tenho direito a aumento?</a></p>

""" + _cta("Hora extra não paga é salário que ficou com a empresa. Se o seu ponto não mostra a jornada que você faz,"),
    },
    {
        "data": "2026-11-19", "pauta": "Blog: Desconto no salário: o que a empresa pode e não pode descontar",
        "foto": "original-descontos-no-salario.jpg", "cy": 0.45, "kicker": "Salário",
        "titulo": "Desconto no salário: o que a empresa pode descontar?",
        "slug": "desconto-no-salario-o-que-a-empresa-pode-descontar",
        "meta": "Quebra de caixa, uniforme, produto avariado: veja quais descontos no salário a CLT permite, quais são proibidos e como pedir a devolução.",
        "resumo": "Os descontos que a CLT permite, os que são proibidos (uniforme, EPI, prejuízo sem culpa) e como recuperar o que foi descontado indevidamente.",
        "post_google": "Descontaram do seu salário a diferença do caixa, o uniforme ou um produto quebrado? Explicamos no blog o que a CLT permite descontar e o que é proibido.",
        "html": """<p>Faltou dinheiro no caixa no fim do dia, e o valor saiu do seu salário. Quebrou uma peça na entrega, e veio o desconto. O uniforme? Também foi cobrado.</p>

<p>No fim do mês, o contracheque chega menor, e você fica sem saber se a empresa pode fazer isso.</p>

<p>Neste artigo eu explico, sem juridiquês, quais descontos a lei permite, quais são proibidos e como pedir de volta o que foi tirado sem motivo. Vamos juntas.</p>

<div class="callout-box">
<h4>Resposta rápida</h4>
<p>A regra é que a empresa <strong>não pode</strong> descontar do salário, salvo adiantamentos, descontos previstos em lei (INSS, imposto de renda, vale-transporte, pensão alimentícia) e os previstos em convenção coletiva (CLT, art. 462). Prejuízo causado pelo empregado só pode ser descontado se houver dolo (intenção) ou se o desconto estiver combinado no contrato. Equipamento de proteção nunca pode ser cobrado.</p>
</div>

<h2>Os descontos que a lei permite</h2>

<ul>
<li><strong>INSS e imposto de renda</strong>, nas faixas da lei.</li>
<li><strong>Vale-transporte</strong>: até 6% do salário básico.</li>
<li><strong>Pensão alimentícia</strong> determinada pelo juiz.</li>
<li><strong>Adiantamentos</strong> (o "vale" do meio do mês).</li>
<li><strong>Faltas sem justificativa</strong>, que podem levar junto o descanso semanal da semana. Falta com atestado ou nas hipóteses da lei (art. 473 da CLT) não pode ser descontada.</li>
<li><strong>Empréstimo consignado</strong> que você contratou, dentro do limite da lei.</li>
</ul>

<p>Descontos para plano de saúde, odontológico, seguro, previdência privada ou associação valem se você autorizou <strong>por escrito</strong> e não foi pressionado a assinar (Súmula 342 do TST).</p>

<h2>Prejuízo, avaria e quebra de caixa</h2>

<p>Aqui está a dúvida que mais chega. A CLT diz que, se o empregado causar dano, o desconto só é lícito em dois casos (art. 462, § 1º):</p>

<ol>
<li>se houver <strong>dolo</strong>, ou seja, se você causou o prejuízo de propósito; ou</li>
<li>se a possibilidade de desconto por culpa (descuido) estiver <strong>combinada no contrato</strong>, e mesmo assim a empresa precisa mostrar que houve culpa sua.</li>
</ol>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>O risco do negócio é da empresa. Diferença de caixa sem prova de culpa, produto que quebrou no transporte, assalto, cliente que não pagou: <strong>NADA DISSO</strong> pode ser descontado automaticamente do seu salário.</p>
</div>

<p>Mesmo quem recebe gratificação de quebra de caixa não dá à empresa um "cheque em branco": a diferença precisa ser apurada, e a culpa, demonstrada.</p>

<h2>Uniforme e equipamento de proteção</h2>

<ul>
<li><strong>EPI</strong> (luva, bota, capacete, protetor) é entregue de graça, por lei (CLT, art. 166).</li>
<li><strong>Uniforme exigido pela empresa</strong> é custo do negócio e não deve ser cobrado de quem trabalha. A lavagem comum fica com o empregado, salvo quando exige produto ou cuidado especial (CLT, art. 456-A).</li>
</ul>

<h2>Como provar e pedir a devolução (a parte que mais importa)</h2>

<table class="prova-table">
<tr><th>Guarde</th><th>Para quê</th></tr>
<tr><td>Contracheques com o desconto</td><td>Mostram o valor, o mês e o nome que a empresa deu ao desconto.</td></tr>
<tr><td>Documentos que mandaram você assinar</td><td>Mostram se houve autorização e se ela foi livre.</td></tr>
<tr><td>Mensagens sobre o prejuízo</td><td>Mostram como a empresa apurou (ou não) a sua culpa.</td></tr>
<tr><td>Relatório ou conferência do caixa</td><td>Mostra se a diferença foi conferida com você presente.</td></tr>
</table>

<p>Primeiro, peça a devolução por escrito ao RH. Se não resolver, os descontos indevidos podem ser cobrados na Justiça do Trabalho, com correção, dos últimos 5 anos e em até 2 anos depois de sair da empresa.</p>

<h2>Perguntas frequentes</h2>

<h3>A empresa pode descontar falta de dinheiro no caixa?</h3>
<p>Só se houver dolo ou se o contrato previr o desconto por culpa e a empresa provar que a diferença foi culpa sua. Desconto automático, sem apuração, é indevido.</p>

<h3>Podem descontar o uniforme do meu salário?</h3>
<p>Não deve. Uniforme exigido pela empresa é custo do negócio, e EPI nunca pode ser cobrado.</p>

<h3>Qual o limite de desconto no salário?</h3>
<p>Não há um percentual único para todos os descontos. Cada um segue sua regra: vale-transporte até 6% do salário básico, consignado dentro do limite da lei, pensão no valor fixado pelo juiz.</p>

<h3>Assinei autorização de desconto. Perdi o direito?</h3>
<p>Não necessariamente. Se você foi obrigado a assinar para ser contratado ou para continuar no emprego, a autorização pode ser anulada.</p>

<p>Leia também: <a href="acumulo-de-funcao-tenho-direito-a-aumento.html">acúmulo de função</a>, <a href="hora-extra-nao-paga-como-calcular-e-provar.html">hora extra não paga</a> e <a href="fgts-nao-depositado-como-consultar-e-o-que-fazer.html">FGTS não depositado</a>.</p>

""" + _cta("Salário é a base do seu sustento, e a lei protege cada real dele. Se o seu contracheque vem com descontos que você não entende,"),
    },
    {
        "data": "2026-11-26", "pauta": "Blog: Banco de horas: regras, prazos e o que muda com o fim da 6x1",
        "foto": "original-banco-de-horas.jpg", "cy": 0.5, "kicker": "Jornada de trabalho",
        "titulo": "Banco de horas: regras, prazos e o que muda com o fim da 6x1",
        "slug": "banco-de-horas-regras-e-fim-da-6x1",
        "meta": "Banco de horas precisa de acordo, tem prazo para compensar e limite de 10 horas por dia. Veja as regras da CLT e o que muda com a EC 141.",
        "resumo": "As três formas de banco de horas na CLT, os prazos para compensar, o que acontece na demissão e o que muda com a nova jornada da EC 141.",
        "post_google": "Suas horas vão para o banco e nunca viram folga? Explicamos no blog as regras do banco de horas na CLT, os prazos para compensar e o que muda com o fim da escala 6x1.",
        "html": """<p>Você ficou até mais tarde a semana inteira. Na hora de receber, a resposta foi: "foi para o banco". Os meses passam, o saldo só cresce, e a folga nunca chega.</p>

<p>Banco de horas é permitido por lei. Mas ele tem regras, e quando a empresa não cumpre, as horas viram hora extra a pagar.</p>

<p>Neste artigo eu explico, sem juridiquês, como o banco de horas funciona, os prazos para compensar e o que muda com o fim da escala 6x1. Vamos juntos.</p>

<div class="callout-box">
<h4>Resposta rápida</h4>
<p>O banco de horas troca hora extra por folga, mas precisa de acordo. Por convenção ou acordo coletivo, a compensação pode levar até 1 ano; por acordo individual escrito, até 6 meses; e dentro do mesmo mês, até por acordo tácito (CLT, art. 59). O limite é de 10 horas trabalhadas por dia. Horas não compensadas no prazo, ou no fim do contrato, são pagas como extras.</p>
</div>

<h2>As três formas de banco de horas</h2>

<table class="prova-table">
<tr><th>Como foi combinado</th><th>Prazo para compensar</th></tr>
<tr><td>Convenção ou acordo coletivo (com o sindicato)</td><td>Até 1 ano (art. 59, § 2º)</td></tr>
<tr><td>Acordo individual escrito</td><td>Até 6 meses (art. 59, § 5º)</td></tr>
<tr><td>Acordo individual, escrito ou tácito</td><td>Dentro do mesmo mês (art. 59, § 6º)</td></tr>
</table>

<p>Em qualquer caso, a jornada não pode passar de <strong>10 horas por dia</strong>.</p>

<h2>O que acontece se a empresa descumprir</h2>

<ul>
<li><strong>Passou o prazo e não compensou?</strong> As horas que sobraram são pagas como extras, com o adicional de pelo menos 50%.</li>
<li><strong>Não existe acordo nenhum?</strong> Não há banco de horas válido: o tempo além da jornada é hora extra.</li>
<li><strong>Foi demitido com saldo positivo?</strong> As horas não compensadas são pagas na rescisão, calculadas pelo salário da data da saída (art. 59, § 3º).</li>
</ul>

<p>Um detalhe que pouca gente conhece: a CLT diz que fazer hora extra com frequência, por si só, não anula o banco de horas (art. 59-B, parágrafo único). Por isso, o que costuma decidir o caso é se o acordo existe, se os prazos foram respeitados e se você tinha como acompanhar o saldo.</p>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Você tem direito de saber o seu saldo. Peça o extrato do banco de horas por escrito. Banco de horas que só a empresa conhece, sem controle, é difícil de defender.</p>
</div>

<h2>O que muda com o fim da escala 6x1</h2>

<p>A <a href="fim-da-escala-6x1-o-que-muda-e-quando-comeca.html">Emenda Constitucional 141</a> manteve a possibilidade de compensação de horários por acordo ou convenção coletiva. O que muda é a régua:</p>

<ul>
<li>a partir de <strong>16/12/2026</strong>, a jornada máxima cai para 42 horas por semana, com dois dias de descanso;</li>
<li>um ano depois, cai para 40 horas.</li>
</ul>

<p>Na prática, o que passar do novo limite semanal é hora extra: entra no banco de horas, se houver acordo válido, ou é paga. E o segundo dia de descanso é <strong>remunerado</strong>: ele não se confunde com a folga que você ganha compensando horas do banco.</p>

<p>Na transição para 42 horas, a convenção ou o acordo coletivo pode ampliar a jornada diária para distribuir a semana (EC 141, art. 7º). Vale conferir o que o sindicato da sua categoria assinar.</p>

<h2>Como provar (a parte que mais importa)</h2>

<table class="prova-table">
<tr><th>Guarde</th><th>Para quê</th></tr>
<tr><td>O acordo de banco de horas (ou a convenção coletiva)</td><td>Mostra se ele existe e qual é o prazo.</td></tr>
<tr><td>Extratos do saldo</td><td>Mostram quantas horas entraram e quantas viraram folga.</td></tr>
<tr><td>Espelho de ponto</td><td>Mostra a jornada real de cada dia.</td></tr>
<tr><td>Pedidos de folga negados</td><td>Mostram que a compensação não foi oferecida.</td></tr>
</table>

<h2>Se você é empresa</h2>

<p>Revise os acordos de compensação antes de 16/12/2026: limites, prazos e controle de saldo precisam bater com a nova jornada. Cláusulas coletivas incompatíveis com a EC 141 perdem efeito dois meses depois da publicação.</p>

<h2>Perguntas frequentes</h2>

<h3>A empresa pode me obrigar a fazer banco de horas?</h3>
<p>O banco de horas precisa de acordo: coletivo, individual escrito ou, para compensar no mesmo mês, até tácito. Sem nenhum acordo, as horas a mais são extras.</p>

<h3>Qual o prazo para compensar o banco de horas?</h3>
<p>Até 1 ano, se combinado com o sindicato; até 6 meses, por acordo individual escrito; no mesmo mês, por acordo tácito.</p>

<h3>Fui demitido com horas no banco. Recebo?</h3>
<p>Sim. As horas não compensadas são pagas como extras na rescisão.</p>

<h3>O banco de horas acaba com o fim da 6x1?</h3>
<p>Não. A Emenda 141 manteve a compensação de horários. Muda o limite da jornada, e o que passar dele precisa ser compensado ou pago.</p>

<p>Leia também: <a href="hora-extra-nao-paga-como-calcular-e-provar.html">hora extra não paga: como calcular e provar</a> e <a href="carga-horaria-maxima-clt.html">carga horária máxima na CLT</a>.</p>

""" + _cta("Banco de horas que nunca vira folga é hora extra que ficou sem pagamento. Se o seu saldo só cresce,"),
    },
]
