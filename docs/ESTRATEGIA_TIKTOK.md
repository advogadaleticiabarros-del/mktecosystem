# Estratégia de crescimento no TikTok (Letícia Barros Advocacia)

Versão de 23/10/2026. Pedido da Jessica: "manter independente do Instagram, editorial próprio, horários de maior
fluxo, crescimento a curto prazo e viralização". Vale até a revisão de 20/11/2026 (números de 4 semanas).

Ordem de prioridade quando houver conflito: **OAB > regras do TikTok > crescimento**. Tudo do
`MANUAL_CONTEUDO_REDES.md` (Provimento 205/2021) vale aqui também.

## 1. Como o TikTok distribui (e por que não dá para copiar o Instagram)

- **O que a TikTok diz oficialmente** (Newsroom, "How TikTok recommends videos #ForYou"): a recomendação usa
  (1) interações (assistir, rever, curtir, compartilhar, comentar, seguir), (2) informações do vídeo (legenda, som,
  hashtags) e (3) configurações do aparelho (idioma, país), estas com peso menor. **Terminar de assistir um vídeo
  longo é sinal forte.** Número de seguidores e vídeos que já viralizaram "não são fatores diretos".
- **Na prática:** cada vídeo é mostrado primeiro a um grupo pequeno de pessoas que **não** seguem a conta. Se esse
  grupo assiste até o fim, revê e compartilha, o vídeo vai para um grupo maior, e assim por diante. Conta nova pode
  viralizar no primeiro mês; no Instagram, o alcance começa pelos seguidores.
- **O sinal mais forte é a retenção** (quanto do vídeo a pessoa assiste e se assiste até o fim). Os blogs de
  marketing citam 50% a 70% de conclusão como o patamar para sair do primeiro grupo; a TikTok não publica o número.
  Tratamos como referência, não como regra.
- **O TikTok é buscador.** Ele lê a legenda, o texto escrito na tela e o que é falado (transcrição). Quem pesquisa
  "gestante demitida" ou "pensão 30 por cento" encontra o vídeo por semanas. A palavra-chave precisa estar **dita
  nos primeiros segundos, escrita na tela e no começo da legenda**.
- **O horário pesa menos que no Instagram**: o vídeo continua sendo distribuído por dias. O que pesa mais é a
  frequência e a regularidade.

| | Instagram (Reels) | TikTok |
|---|---|---|
| Quem vê primeiro | Seguidores | Desconhecidos com interesse no tema |
| Sinal principal | Envio por direct, salvamento | Retenção (assistir até o fim), rever, compartilhar |
| Frequência | 2 Reels por semana (terça e sexta 21h) | 5 vídeos por semana |
| Busca | Fraca | Forte (fala, texto na tela e legenda) |
| Vida útil do post | 1 a 2 dias | Dias ou semanas |

## 2. Agenda própria (no ar desde 23/10/2026)

O Orbit agora tem **fila própria do TikTok**, sem depender do horário do Instagram (`services/tiktok.py`,
`GRADE_TIKTOK`; tela `/tiktok` mostra a fila e permite mudar a data ou tirar um vídeo).

- **5 vídeos por semana**, em três faixas para testar:

  | Dia | Horário | Por quê |
  |---|---|---|
  | Domingo | 10h | Manhã de domingo aparece bem em vários levantamentos (Buffer 2026) |
  | Segunda | 18h | Fim da tarde, saída do trabalho (faixa 16h–21h é a mais citada) |
  | Terça | 12h | Almoço (testa a faixa do meio-dia) |
  | Quarta | 20h | Noite |
  | Quinta | 18h | Fim da tarde |

  Sexta e sábado ficam livres (sexta já é dia de Reels no Instagram; sábado tem a pior média nos levantamentos).
- **Base dos horários:** os estudos públicos não concordam entre si (Sprout Social, Buffer, listas de blogs
  brasileiros). O ponto em comum é dia útil, fim da tarde e começo da noite. Por isso a grade **testa** almoço,
  fim de tarde e noite. Em 20/11/2026, comparamos as visualizações das primeiras 24 h de cada faixa (TikTok Studio
  → Análises) e ficamos com as duas melhores. Se a conta passar de 100 seguidores, o TikTok mostra a "atividade dos
  seguidores" por hora, que passa a valer mais que os estudos.
- **Frequência:** o estudo da Buffer (mais de 11 milhões de posts) mostra que o maior salto de visualizações está em
  sair de 1 para 2 a 5 posts por semana; outro levantamento (1,9 milhão de vídeos) aponta 1 por dia como o melhor
  engajamento por post. Começamos com 5 e subimos para 7 se houver material com a mesma qualidade.
- **Como entra cada vídeo:** todo Reels aprovado com agendamento ativo no Instagram entra sozinho na próxima vaga
  livre, na ordem das datas do Instagram (as séries ficam em ordem). Os Reels já publicados no Instagram também
  entram: para o TikTok eles são novos. Versões antigas sem agendamento e Reels pausados não entram.
- **Enquanto a TikTok não aprovar o app (auditoria):** no horário da fila, o vídeo vai para a caixa de rascunhos do
  TikTok. Alguém da equipe abre a notificação no celular, põe o som, cola a legenda (a tela `/tiktok` mostra e tem
  o botão Copiar) e publica **na hora**. Depois clica "Já publiquei" no Orbit.

## 3. Música: sim, som em alta, mas da biblioteca comercial

- **Por que não qualquer som em alta:** o escritório é conta de empresa (publicidade de serviço). Pelas regras de
  música da TikTok, conta comercial só pode usar a **Biblioteca de Música Comercial** (sons liberados para uso por
  empresas). Os sons em alta da biblioteca geral são licenciados só para uso pessoal; em conta de empresa, o vídeo
  pode ser silenciado ou removido e o escritório fica exposto a reclamação de direito autoral. Para uma advogada,
  esse risco não compensa.
- **A boa notícia:** a biblioteca comercial tem uma aba **Em alta**. É de lá que escolhemos.
- **Como pôr (no celular, ao publicar o rascunho):** Adicionar som → Sons comerciais → Em alta → escolher um som
  calmo ou de tensão leve, sem letra cantada por cima da fala → Volume: **som em 10% a 15%, som original (voz da
  Dra.) em 100%**.
- **A voz da Dra. continua intocada** (padrão dos Reels de 21/10/2026): o som entra só no TikTok, no app, por baixo
  da fala. O arquivo do Orbit não muda e o Instagram continua sem música.
- **Quando a auditoria sair:** a API de vídeo não põe som. Se quisermos manter o som em alta, os vídeos continuam
  indo para a caixa de rascunhos (decidir na hora: som em alta × publicação automática).
- **Conferir uma vez:** a conta do TikTok precisa estar como **Conta comercial** (Configurações → Conta → Mudar para
  Conta comercial, categoria "Serviços jurídicos"). Ela também libera as análises e o link na bio.

## 4. Editorial próprio do TikTok

Os pilares são os mesmos do Instagram (Mulher que trabalha, Família, Seus direitos no dia a dia, Jornada e trabalho
2026-2027, Empresa em dia), mas a embalagem muda.

### Formatos que mais funcionam no TikTok (em ordem de prioridade)

1. **Séries numeradas ("Parte 1, 2, 3") em dias seguidos.** Quem gosta da parte 1 entra no perfil para ver a 2, e a
   visita ao perfil vira seguidor. Texto na tela no fim: "Parte 2 amanhã". Já temos 6 séries prontas (gestante,
   guarda, 13º, insalubridade, hora extra, limbo previdenciário). Se a conta tiver a opção, criar uma **playlist** por
   série no perfil.
2. **Resposta a comentário em vídeo** (o TikTok mostra o comentário em cima do vídeo). É o formato que mais puxa
   comentário novo. Sempre **em tese**: a Dra. explica a regra e fecha com "cada caso precisa ser avaliado"; nunca
   analisa o caso da pessoa em público (CED art. 42 I).
3. **Mito ou verdade / "3 coisas que..."**: lista curta, número na tela desde o primeiro segundo.
4. **Notícia com tela verde** (efeito Tela Verde do TikTok, a Dra. falando na frente da manchete ou da decisão do
   TST/STF): para o pilar Jornada 2026-2027 (6x1, EC 141, decisões novas). Fonte e data na tela.
5. **Carrossel de fotos (modo foto)** com os carrosséis já aprovados (1080×1440): teste de 1 por semana a partir da
   semana 3. Os estudos se contradizem (2025 a favor das fotos, 2026 a favor do vídeo), então testamos na conta.
   Publicação manual pelo app no começo (a API de fotos exige verificar o domínio de mídia).

### Regras de edição para o TikTok (somam ao padrão premium dos Reels)

- **Gancho nos primeiros 2 segundos**: a pergunta ou a frase mais forte, falada e escrita. Nada de abertura com
  logo, nome ou "oi, gente".
- **Palavra-chave dita, escrita na tela e no começo da legenda** (busca do TikTok).
- **Duração:** 20 a 45 s para crescer (retenção alta). Vídeo acima de 60 s só quando o tema segurar.
- **Fim que puxa para o próximo**: "Parte 2 amanhã", ou um final que emenda no começo (o vídeo recomeça e a pessoa
  revê, o que conta como "rever").
- **Texto na tela dentro da área segura** (nada nos 20% de baixo nem na faixa da direita, onde ficam os botões do
  TikTok).
- **Cortes curtos (a partir da semana 3):** de cada gravação longa sai 1 corte de 15 a 25 s com outro gancho
  (o melhor momento da fala). Edição pela skill `leticia-reels-premium`, sempre **arquivo e peça novos**
  (`tipo="tiktok"` no Orbit, entra na fila sozinho). Material pronto não é sobrescrito.

### Legenda no TikTok

- Primeira linha: a palavra-chave e o gancho ("Grávida pode ser demitida no contrato de experiência?").
- 2 a 4 linhas de contexto, em tese.
- Fechamento impessoal: "Procure uma advogada de confiança." Nada de "me chama", "link na bio para agendar".
- **3 a 5 hashtags**: 1 ou 2 do tema (#direitotrabalhista, #pensaoalimenticia), 1 de nicho (#gestante, #clt) e
  no máximo 1 ampla. Nada de #fyp / #viral (não ajudam e parecem spam).
- Rótulo de conteúdo de IA quando houver imagem ou voz gerada (o Orbit já marca quando a peça tem `rotulo_ia`).

## 5. Táticas de curto prazo (primeiros 30 dias)

1. **Fila cheia desde domingo (25/10):** 23 vídeos prontos cobrem até 24/11 (ver seção 7).
2. **Primeira hora de cada vídeo:** responder todos os comentários na primeira hora (sinal de conversa). Os
   comentários com pergunta boa viram resposta em vídeo na semana seguinte.
3. **Perfil arrumado antes de crescer:**
   - nome com palavra-chave ("Letícia Barros | Advogada Trabalhista");
   - bio com assunto e região ("Direito do trabalho, família e INSS · Vitória/ES · conteúdo informativo");
   - foto de rosto;
   - fixar no perfil os 3 vídeos com melhor retenção, revendo toda semana.
4. **Não apagar vídeo fraco** e não repostar o mesmo vídeo (o TikTok trata como duplicado). Vídeo que foi mal pode
   voltar como **corte novo com outro gancho**.
5. **Seguir a frequência por 4 semanas antes de julgar.** Conta nova costuma oscilar muito nos primeiros 15 a 20
   vídeos.
6. **Proibido (OAB e TikTok):** comprar seguidores ou visualizações, grupo de engajamento, sorteio para seguir
   (Provimento 205/2021 veda influenciar o alcance de forma fraudulenta); dancinha, trend que tire a sobriedade,
   valores, promessa de resultado, caso concreto.

### Sobre viralizar (com honestidade)

Não dá para garantir que um vídeo viralize; a TikTok decide vídeo a vídeo. O que dá para controlar é o que aumenta a
chance: **volume** (5 por semana), **gancho forte**, **retenção**, **séries** e **resposta a comentário**. Na
prática, perfis jurídicos que crescem rápido no TikTok têm 1 ou 2 vídeos que estouram a cada 15 ou 20 publicados.
Por isso a meta é de volume e de aprendizado, não de "um viral por semana".

Ponto de atenção da OAB: em 2021, a Comissão de Publicidade do TED da OAB/MG chegou a recomendar que advogados não
usassem o TikTok. Não é regra do Provimento 205/2021 nem da OAB/ES, mas mostra que a fiscalização olha esse canal
com mais rigor. Mais um motivo para manter tom informativo e sóbrio em tudo.

## 6. Métricas e metas (revisão em 20/11/2026)

Por enquanto os números vêm do **TikTok Studio → Análises** no celular (o Orbit ainda não lê métricas do TikTok;
isso pede os escopos `video.list` e `user.info.stats` numa reconexão futura).

| Métrica | Onde ver | Meta das 4 primeiras semanas |
|---|---|---|
| Vídeos publicados | `/tiktok` | 20 (5 por semana, sem falhar) |
| Retenção média (% do vídeo assistido) | Análises do vídeo | 40% ou mais nos vídeos de até 45 s |
| Visualizações de "Para você" | Fontes de tráfego | 70% ou mais das visualizações |
| Visualizações vindas da busca | Fontes de tráfego | Subindo semana a semana |
| Vídeos acima de 2× a mediana | Lista de vídeos | 2 ou mais (são os que viram série ou corte novo) |
| Seguidores ganhos | Visão geral | Base para a meta de dezembro |

**Em 20/11:** escolher as 2 melhores faixas de horário, os 3 formatos que mais seguraram e decidir se sobe para 7
vídeos por semana. Registrar aqui e no `CONTEXTO_PROJETO.md`.

## 7. Fila inicial (montada pelo Orbit em 23/10/2026)

Séries agrupadas em dias seguidos. A partir de 25/11 a fila só recebe os 2 Reels novos por semana do Instagram;
para manter 5 por semana, os **cortes curtos e as respostas a comentário** precisam começar a ser produzidos na
semana de 09/11.

| Data | Vídeo |
|---|---|
| dom 25/10 10h | 5 coisas que a empresa não pode fazer com a gestante |
| seg 26/10 18h | Gestante 1/3 |
| ter 27/10 12h | Gestante 2/3 |
| qua 28/10 20h | Gestante 3/3 |
| qui 29/10 18h | Guarda dos filhos 1/3 |
| dom 01/11 10h | Guarda dos filhos 2/3 |
| seg 02/11 18h | Guarda dos filhos 3/3 |
| ter 03/11 a seg 09/11 | 13º sem susto 1/3, 2/3, 3/3, 13º proporcional, 13º: as 4 regras (época certa: 1ª parcela até 30/11) |
| ter 10/11 a qui 12/11 | Gestante e insalubridade 1/3, 2/3, 3/3 |
| dom 15/11 e seg 16/11 | Multa do 477 no pedido de demissão; Pensão: mito dos 30% |
| ter 17/11 a qui 19/11 | Hora extra 1/3, 2/3, 3/3 |
| dom 22/11 a ter 24/11 | Conselhos da advogada; Limbo previdenciário 1/2 e 2/2 |

## Fontes

- TikTok Newsroom, "How TikTok recommends videos #ForYou": https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- TikTok for Developers, Content Posting API (rascunho e foto): https://developers.tiktok.com/doc/content-posting-api-get-started-upload-content/ e https://developers.tiktok.com/doc/content-posting-api-reference-photo-post
- Buffer, frequência de posts no TikTok (11 milhões+ de posts): https://buffer.com/resources/how-often-should-you-post-on-tiktok/
- Buffer, melhor formato por rede (45 milhões+ de posts): https://buffer.com/resources/data-best-content-format-social-media/
- Metricool, sons no TikTok e biblioteca comercial: https://metricool.com/tiktok-sounds e https://metricool.com/pt/melhor-horario-postar-tiktok/
- Soundstripe, biblioteca de música do TikTok: https://www.soundstripe.com/blogs/tiktok-music-library-explained
- Loggi e Shopify Brasil, horários no TikTok: https://www.loggi.com/conteudos/empreendedorismo/melhores-horarios-postar-no-tiktok/ e https://www.shopify.com/br/blog/melhores-horarios-para-postar-no-tiktok
- Migalhas, posição do TED da OAB/MG sobre o TikTok: https://www.migalhas.com.br/quentes/338524/tiktok-nao-e-ferramenta-adequada-para-advogados-diz-ted-da-oabmg-em-manual
- Provimento 205/2021: https://www.conjur.com.br/dl/pr/provimento-2052021.pdf
