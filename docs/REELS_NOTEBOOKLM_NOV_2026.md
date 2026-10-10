# Reels de novembro/2026: comandos para gerar o áudio no NotebookLM

Para a Letícia gerar a narração das 4 séries do plano (`docs/PLANO_CONTEUDO_NOV_2026.md`). O vídeo é
produzido por nós a partir do áudio, no padrão motion (skill `leticia-reels-motion`).

Página para ela (celular, com botões de copiar e roteiro falado da série 1): https://claude.ai/artifact/Uxj3u5dK7TA2YQbQYFgjTe

## Como gerar (igual para as 4 séries)

1. No NotebookLM, crie **um caderno por série** (ex.: "Reels 13º sem susto").
2. **Adicionar fonte → Texto copiado**: cole o bloco "FONTE" da série. Use só essa fonte (sem PDFs
   ou sites extras), para a IA não puxar informação de fora.
3. Em **Visão geral em áudio → Personalizar**:
   - Formato: **Conversa aprofundada** · Duração: **Mais curta** · Idioma: **Português (Brasil)**.
   - Cole o bloco "INSTRUÇÃO" da série no campo "Em que os apresentadores de IA devem se concentrar?".
4. Gere, ouça uma vez e baixe o áudio (.wav ou .m4a). Me envie com o nome da série.
5. Se algum fato sair diferente da fonte, me avise: eu corto o trecho na edição (os fatos são
   conferidos de novo antes de montar).

Meta: áudio de **2 a 3 minutos**, dividido em 3 blocos claros. Cada bloco vira um Reels de 30 a 45 s.

---

## Série 1 · "13º sem susto" (ter 03/11, qui 05/11, sáb 07/11 · 20h30)

**FONTE**

```
13º SALÁRIO EM 2026: O QUE A TRABALHADORA PRECISA SABER (lei brasileira)

Parte 1. Prazos do 13º em 2026
- O 13º é pago em duas parcelas (Lei 4.749/1965).
- 1ª parcela: até 30 de novembro de 2026 (segunda-feira). É metade do salário, SEM desconto de INSS e de imposto de renda.
- 2ª parcela: o prazo legal é 20 de dezembro. Em 2026, 20/12 cai num domingo, então o pagamento deve sair até sexta, 18 de dezembro. Os descontos de INSS e IR ficam na 2ª parcela.
- Pagar tudo de uma vez só é permitido se for até 30 de novembro. Pagar tudo só em dezembro é irregular.
- Empresa que atrasa pode ser multada pela fiscalização (Lei 7.855/1989, art. 3º).

Parte 2. Quem tem direito e como é calculado
- Tem direito quem trabalha de carteira assinada, inclusive doméstica, rural e temporária.
- Cada mês com 15 dias ou mais de trabalho vale 1/12 do 13º (Lei 4.090/1962).
- Falta justificada por atestado médico não reduz o 13º (Decreto 57.155/1965, art. 2º).
- A média das horas extras habituais, adicional noturno e comissões entra no cálculo (Súmula 45 do TST).
- Quem pede demissão ou é demitida sem justa causa recebe o 13º proporcional na rescisão (Súmula 157 do TST). Só a justa causa tira esse direito.

Parte 3. A gestante e o 13º
- A licença-maternidade NÃO reduz o 13º. Os meses de licença contam como meses trabalhados.
- Na carteira assinada, a empresa paga o 13º inteiro e compensa com o INSS a parte da licença (Lei 8.213/1991, art. 72, § 1º).
- Quem recebe o salário-maternidade direto do INSS (MEI, autônoma, desempregada no período de graça, doméstica) recebe do INSS o 13º proporcional ao benefício.
- Se o 13º veio menor por causa da licença, há erro de cálculo: guarde os contracheques e peça o cálculo por escrito ao RH.
```

**INSTRUÇÃO**

```
Público: trabalhadoras brasileiras, principalmente gestantes e mães, que assistem no Instagram. Fale em português do Brasil, com linguagem simples, calorosa e direta, sem juridiquês.
Organize a conversa em 3 blocos bem separados, na ordem da fonte (Parte 1, Parte 2, Parte 3). Cada bloco deve abrir com uma pergunta-gancho forte que pare quem está rolando o feed (ex.: "A empresa pode pagar o seu 13º só em dezembro?") e durar entre 40 e 50 segundos.
Use SOMENTE as informações da fonte. Não invente números, datas, valores ou exemplos de casos. Cite as datas exatamente como estão.
Nunca use as palavras "especialista", "ex" ou "deficiência". Não ofereça serviços, não diga "fale comigo", "me chama" ou "conte seu caso".
Termine a conversa com: "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança."
```

---

## Série 2 · "Depois do parto" (ter 10/11, qui 12/11, sáb 14/11 · 20h30)

**FONTE**

```
DEPOIS DO PARTO: OS DIREITOS DA MÃE QUE VOLTA AO TRABALHO (lei brasileira)

Parte 1. Amamentação no trabalho
- Até o bebê completar 6 meses, a mãe tem direito a 2 descansos especiais de meia hora cada, dentro do horário de trabalho, para amamentar (CLT, art. 396).
- Os horários são combinados entre a mãe e a empresa (CLT, art. 396, § 2º).
- Quando a saúde do bebê exigir, com indicação médica, os 6 meses podem ser estendidos (CLT, art. 396, § 1º).
- Vale também para filho adotivo.
- A licença-maternidade pode começar até 28 dias antes do parto, com atestado médico (CLT, art. 392, § 1º).

Parte 2. Creche
- Estabelecimento com pelo menos 30 mulheres com mais de 16 anos precisa ter local para as mães deixarem os filhos no período de amamentação (CLT, art. 389, § 1º).
- A empresa pode cumprir com creche conveniada, pública ou privada (CLT, art. 389, § 2º).
- Ou com o reembolso-creche, para filhos de até 5 anos e 11 meses. O reembolso não tem natureza de salário (Lei 14.457/2022).
- Muitas convenções coletivas garantem auxílio-creche maior. Vale conferir a da sua categoria.

Parte 3. Gravidez e insalubridade
- A gestante deve ser afastada de atividades insalubres em qualquer grau: mínimo, médio ou máximo (CLT, art. 394-A).
- O STF derrubou a exigência de atestado médico para isso (ADI 5938). A proteção vale para todas.
- O afastamento mantém o salário e o adicional de insalubridade.
- Se a empresa não tiver função segura, a gravidez é tratada como de risco e o INSS paga o salário-maternidade durante o afastamento (CLT, art. 394-A, § 3º).
- A lactante (mãe que amamenta) também deve ficar longe da insalubridade.
```

**INSTRUÇÃO**

```
Público: gestantes e mães que trabalham de carteira assinada no Brasil e assistem no Instagram. Fale em português do Brasil, com acolhimento e linguagem simples, sem juridiquês.
Organize a conversa em 3 blocos bem separados, na ordem da fonte (Parte 1, Parte 2, Parte 3). Cada bloco abre com uma pergunta-gancho (ex.: "Você sabia que a mãe que amamenta tem 2 pausas por dia no trabalho?") e dura entre 40 e 50 segundos.
Use SOMENTE as informações da fonte. Não invente números, prazos, valores ou casos.
Nunca use as palavras "especialista", "ex" ou "deficiência". Não ofereça serviços, não diga "fale comigo", "me chama" ou "conte seu caso".
Termine com: "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança."
```

---

## Série 3 · "Pensão desde a barriga" (ter 17/11, qui 19/11, sáb 21/11 · 20h30)

**FONTE**

```
PENSÃO DESDE A BARRIGA: ALIMENTOS GRAVÍDICOS (lei brasileira)

Parte 1. A grávida pode pedir pensão antes do bebê nascer
- A gestante pode pedir ao pai uma ajuda com as despesas da gravidez: são os alimentos gravídicos (Lei 11.804/2008).
- Cobrem as despesas da concepção ao parto: alimentação especial, assistência médica e psicológica, exames, internações, parto e remédios (art. 2º).
- O valor é dividido na proporção dos recursos da gestante e do pai (art. 2º, parágrafo único).

Parte 2. Como provar a paternidade na gravidez
- Não é preciso exame de DNA durante a gravidez. O juiz decide com base em indícios da paternidade (art. 6º).
- Indícios: conversas de WhatsApp e redes sociais, fotos juntos, testemunhas que conheciam o relacionamento.
- Guarde também os recibos das despesas da gravidez e o que souber da renda do pai.

Parte 3. Depois do parto
- Com o nascimento, os alimentos gravídicos viram pensão alimentícia do bebê, até que alguém peça revisão (art. 6º, parágrafo único).
- Quando a pensão é um percentual do salário do pai, o desconto vale também sobre o 13º e o terço de férias (STJ, Tema 192).
- Atraso na pensão não autoriza impedir a convivência com a criança, e pagar pensão não dá direito a mudar sozinho as datas de convivência. São questões separadas.
```

**INSTRUÇÃO**

```
Público: mulheres grávidas no Brasil, muitas criando o filho sozinhas, que assistem no Instagram. Fale em português do Brasil, com acolhimento, sem julgamento e sem juridiquês.
Organize a conversa em 3 blocos bem separados, na ordem da fonte (Parte 1, Parte 2, Parte 3). Cada bloco abre com uma pergunta-gancho (ex.: "Dá para pedir pensão antes do bebê nascer?") e dura entre 40 e 50 segundos.
Use SOMENTE as informações da fonte. Não invente valores, prazos ou casos.
Chame o pai de "pai" ou "genitor". Nunca use as palavras "ex", "especialista" ou "deficiência". Não ofereça serviços, não diga "fale comigo", "me chama" ou "conte seu caso".
Termine com: "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança."
```

---

## Série 4 · "INSS da mulher" (ter 24/11, qui 26/11, sáb 28/11 · 20h30)

**FONTE**

```
INSS DA MULHER EM 2026 (lei brasileira)

Parte 1. Aposentadoria da mulher em 2026 (regras de transição da Reforma, EC 103/2019)
- Por idade: 62 anos e 15 anos de contribuição, para quem já contribuía antes da Reforma (art. 18).
- Por pontos: 93 pontos em 2026 (idade + tempo de contribuição), com no mínimo 30 anos de contribuição (art. 15).
- Idade mínima progressiva: 59 anos e 6 meses em 2026, com 30 anos de contribuição. Sobe 6 meses por ano (art. 16).
- Pedágio de 100%: 57 anos, 30 anos de contribuição e mais o tempo que faltava em novembro de 2019 (art. 20).
- Antes de pedir, confira o extrato do CNIS no Meu INSS: vínculo que não aparece atrasa a aposentadoria.

Parte 2. Desempregada e grávida
- Quem para de contribuir continua segurada por um tempo: o período de graça (Lei 8.213/1991, art. 15).
- Regra geral: 12 meses depois da última contribuição. +12 meses com mais de 120 contribuições e +12 meses com o desemprego comprovado: pode chegar a 36 meses.
- Se o parto acontecer dentro desse período, o INSS paga o salário-maternidade direto, pedido pelo Meu INSS ou pelo 135.
- A MEI em dia com o INSS também recebe 120 dias de salário-maternidade, no valor de um salário mínimo (R$ 1.621 em 2026). O STF derrubou a exigência de carência (ADI 2110).

Parte 3. Dona de casa pode se aposentar
- Quem cuida da casa e não tem renda própria pode contribuir como segurada facultativa.
- Na baixa renda, a contribuição é de 5% do salário mínimo: R$ 81,05 por mês em 2026 (Lei 8.212/1991, art. 21).
- Requisitos: família inscrita no CadÚnico, com cadastro atualizado nos últimos 2 anos, e renda familiar de até 2 salários mínimos. Guia com o código 1929.
- Garante a aposentadoria por idade e protege em doença e maternidade. Para aposentadoria por tempo de contribuição, é preciso complementar a diferença.
- Aposentada não perde a pensão por morte: dá para receber os dois; o maior vem inteiro e o outro com redução por faixas (EC 103/2019, art. 24).
```

**INSTRUÇÃO**

```
Público: mulheres brasileiras de 30 a 65 anos, donas de casa, mães e trabalhadoras, que assistem no Instagram. Fale em português do Brasil, com linguagem simples e respeitosa, sem juridiquês.
Organize a conversa em 3 blocos bem separados, na ordem da fonte (Parte 1, Parte 2, Parte 3). Cada bloco abre com uma pergunta-gancho (ex.: "Dona de casa pode se aposentar pagando 81 reais por mês?") e dura entre 40 e 50 segundos.
Use SOMENTE as informações da fonte. Não invente números, idades, valores ou casos; cite os valores exatamente como estão.
Nunca use as palavras "especialista", "ex" ou "deficiência" (se precisar, diga "necessidades especiais"). Não ofereça serviços, não diga "fale comigo", "me chama" ou "conte seu caso".
Termine com: "Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança."
```
