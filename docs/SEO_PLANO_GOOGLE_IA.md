# Plano de SEO: aparecer mais no Google e nas IAs (10/10/2026)

Pedido da Letícia: "precisamos aparecer em mais pesquisas orgânicas no Google... acho que poderíamos ter
2 artigos por semana". Este documento junta o diagnóstico do site, o que a pesquisa mostra sobre 2026 e
o plano proposto.

## 1. Diagnóstico do site (advogadaleticiabarros.com.br, 10/10/2026)

O que está bom:
- `robots.txt` libera tudo e aponta o sitemap; sitemap com 49 URLs (24 artigos, 7 áreas, 5 LPs).
- Artigos têm título com a pergunta da pessoa, meta description, canonical, H1 único, vários H2 e
  schema `BlogPosting` com autora "Dra. Letícia Barros". Home tem schema `Attorney`/`LegalService`.
- Publicação automática pelo Orbit funcionando (artigo do pet saiu sozinho em 09/10).

O que está atrapalhando:
1. **Capas pesadas**: cada capa do blog é PNG de 0,4 a 1,1 MB; a página `/blog/` carrega mais de 10 MB
   de imagem. Lento no celular (e a busca jurídica é quase toda no celular). Converter para WebP/JPG
   (~80–150 KB).
2. **Artigos ilhados**: cada artigo tem 1 link para outro artigo; a home e as páginas de área têm
   **0 links** para o blog. O Google mede autoridade por assunto (cluster), e sem links entre as páginas
   ele não enxerga que o site cobre bem "direitos da gestante".
3. **Sem schema de FAQ**: os artigos já têm "Perguntas frequentes", mas sem `FAQPage`; falta também
   `dateModified` nos novos e a autora como `Person` com OAB. Isso ajuda as IAs (ChatGPT, Perplexity,
   Gemini) a extrair e citar.
4. **Textos da home e das áreas**:
   - A meta description da home diz "Advogada especialista": isso é risco com a OAB e precisa sair.
   - A página trabalhista diz "envie o seu caso para análise": tom de captação, rever.
   - Os títulos das áreas não têm "advogada trabalhista em Vitória-ES" (busca local real).
   - O H1 da home não tem palavra-chave.
5. **`/blog/` sem meta description e sem canonical.**
6. **Sem `llms.txt`** (arquivo-guia para IAs; o Google não exige, mas ChatGPT e Perplexity leem).
7. **URL com palavra vetada**: o artigo do BPC tem "deficiencia" no endereço. Trocar com redirecionamento 301.
8. **Sem medição**: não temos os números do Search Console (consultas, impressões, posição) no Orbit.

## 2. O que pesa em 2026 (pesquisa)

- Conteúdo jurídico é YMYL ("seu dinheiro ou sua vida"): o Google exige mais **E-E-A-T** (experiência,
  conhecimento, autoridade e confiança).
  - Os updates de março e maio de 2026 subiram essa régua.
  - Autora identificada, com credencial e histórico no tema, ganha.
  - Texto de IA em escala, sem revisão humana e sem informação nova, perde.
  - A confiança passou a ser avaliada **por grupo de páginas do mesmo assunto**, não só por página.
- **AI Overviews/AI Mode** derrubam cliques no 1º resultado. Por outro lado, quem é **citado** na
  resposta da IA ganha. Para ser citado, o texto precisa de:
  - resposta direta logo no início (40–60 palavras);
  - perguntas frequentes;
  - fonte legal citada;
  - data de atualização.
- **Frequência**: não há estudo mostrando que mais posts por semana ganha de menos posts melhores.
  O consenso é que o ritmo precisa ser **constante por meses**, organizado em **clusters**: uma página
  pilar + 8 a 15 artigos ligados entre si. O efeito aparece em 2 a 6 meses.
- **Busca local** ("advogada trabalhista Vitória ES" aparece no autocompletar): pesam o Perfil da
  Empresa no Google completo, o endereço igual em todo lugar e as avaliações. Avaliações pedem cuidado
  com a OAB: nada de usar depoimento como propaganda.

## 3. O que as pessoas digitam (autocompletar do Google, 10/10/2026)

Gestante (nosso nicho principal), buscas que ainda **não** têm artigo nosso:
- estabilidade gestante: contrato de experiência; contrato temporário; quanto tempo; como contar; após a licença
- grávida pode ser demitida: por justa causa; por faltas; abandono de emprego
- gestante demitida: reintegração ou indenização; tem direito ao seguro-desemprego
- licença-maternidade: quem paga; conta a partir de quando; como dar entrada; MEI; para o pai
- salário-maternidade: urbano ou rural; quantas parcelas; como saber se tenho direito

Outros temas com muita busca:
- **Trabalhista**: rescisão indireta (recebe seguro? demora quanto?); pedi demissão (o que recebo, FGTS,
  aviso prévio, empréstimo consignado); acordo trabalhista; assédio moral (como provar, é crime?); horas extras.
- **Família**: pensão alimentícia (valor 2026, líquido ou bruto, 1 e 2 filhos, depositada a menor);
  guarda compartilhada paga pensão?; divórcio no cartório.
- **Previdenciário**: auxílio-doença negado; aposentadoria da mulher (quantos pontos, sem contribuição);
  BPC/LOAS (autismo, empréstimo, 13º).

## 4. Plano proposto

**Frente A: arrumar a base técnica (1 a 2 semanas, uma vez só, feito por nós)**
1. Capas em WebP/JPG leves, com `loading="lazy"` no índice do blog.
2. Template do artigo:
   - `FAQPage` montado das "Perguntas frequentes";
   - `dateModified`;
   - autora como `Person` (OAB/ES 39.948);
   - breadcrumb;
   - bloco "Leia também" com 3 artigos do mesmo cluster.
3. Home e páginas de área com links para os artigos do tema.
4. Títulos locais nas áreas ("Advogada trabalhista em Vitória-ES").
5. Tirar "especialista" e o convite de "envie o seu caso".
6. `llms.txt`, meta e canonical do `/blog/`, e redirecionamento da URL do BPC.
7. Republicar os 24 artigos antigos com o template novo.

**Frente B: clusters (o coração da estratégia)**
- **Cluster 1, Gestante CLT (prioridade)**:
  - página pilar "Direitos da gestante CLT: guia completo 2026";
  - artigos da lista da seção 3, todos ligando para a pilar e entre si.
- **Cluster 2, Pensão e guarda.**
- **Cluster 3, Rescisão e demissão.**
- **Cluster 4, INSS da mulher.**

**Frente C: 2 artigos por semana**
- **Segunda**: artigo do cluster, sobre uma busca "sempre procurada" da lista.
- **Quinta**: artigo de atualidade (lei nova, decisão do STF/TST, prazo do mês) ligado a um cluster.
- Cada artigo continua passando pela aprovação dela.
- Precisa ter algo que só ela pode dar: um "caso típico do escritório" sem identificar ninguém, a
  experiência prática, a dúvida que mais chega. É isso que o Google chama de experiência e o que evita
  parecer texto de IA em escala.
- Revisar e atualizar os artigos antigos que começarem a aparecer (com "Atualizado em").

**Frente D: presença fora do site**
- Perfil da Empresa no Google: serviços, posts semanais com link para o artigo e fotos reais
  (pendência antiga dela).
- Endereço igual em todo lugar.
- Instagram e Reels apontando para os artigos.

**Medição**
- Search Console mensal: consultas, impressões, cliques e posição por cluster.
- Precisamos de acesso (adicionar o e-mail do Orbit como usuário da propriedade) ou de um print mensal.
- Meta de 90 dias: aparecer nas buscas longas do cluster gestante (ex.: "estabilidade gestante
  contrato de experiência") e ser citado no AI Overview em pelo menos algumas delas.

## Fontes

- [Google May 2026 Core Update (The Publive)](https://www.thepublive.com/blog/google/google-may-2026-core-update-11872595)
- [Core Update May 2026: rankings e visibilidade em IA (Relevant Audience)](https://www.relevantaudience.com/seo/google-core-update-may-2026-what-you-need-to-know/)
- [March 2026 core update (Launchcodex)](https://launchcodex.com/blog/seo-geo-ai/google-march-2026-core-update/)
- [May 2026 Core Update: quem foi atingido (TechSEO)](https://www.techseo.es/en/blog/google-may-2026-core-update)
- [Topic clusters 2026 (Digital Applied)](https://www.digitalapplied.com/blog/seo-content-clusters-2026-topic-authority-guide)
- [Topic clusters para pequenas empresas (Verlua)](https://www.verlua.com/blog/topic-cluster-strategy-small-business)
- [Com que frequência publicar (Quillly, dados 2026)](https://quillly.com/blogs/how-often-publish-blog-posts-2026)
- [Frequência de blog para pequenas empresas (MJW Media)](https://www.mjwmedia.com/how-often-small-business-blog-2026/)
- [SEO para advogados (Migalhas)](https://www.migalhas.com.br/depeso/461561/seo-para-advogados-como-aparecer-na-primeira-pagina-do-google)
- [Google Meu Negócio para advogados (Desmistificando)](https://desmistificando.com.br/google-meu-negocio-advogados/)
- [Provimento 205/2021 e marketing jurídico (Projuris)](https://www.projuris.com.br/blog/provimento-205-2021/)
- [Site da OAB sobre marketing jurídico](https://www.oab.org.br/noticia/60188/oab-lanca-site-para-esclarecer-duvidas-sobre-o-marketing-juridico)
- Google, guia oficial de recursos de IA na busca (skill `ai-seo`): sem marcação especial; conteúdo útil
  e organizado; não escrever separado "para IA".

## Execução

### 10/10/2026: Frente A feita e conteúdo iniciado

- **Site no ar** (`apps/api/_saida_producao_1510/seo_site.py`; backup dos textos em
  `/root/orbit-backups/site-textos-antes-seo-20261010.tgz`): 65 arquivos e 127 trocas.
  - Saíram "especialista", "Fale comigo", "envie o seu caso", "análise gratuita" e "sem compromisso".
  - "Deficiência" virou "necessidades especiais" e "ex" virou "genitor"/"pai".
  - O valor do BPC foi atualizado para R$ 1.621.
  - 2 endereços novos, com 301: `pai-nao-paga-pensao-o-que-fazer` e `bpc-para-crianca-com-necessidades-especiais-...`.
  - Schema completo em 38 artigos (FAQPage em 32).
  - "Continue lendo" por assunto em todos os artigos; links do blog na home e nas áreas; títulos locais nas áreas.
  - Mapa do site de 24 para 59 URLs (9 artigos estavam fora); `llms.txt` publicado.
  - Capas em JPG (de 12,8 MB para 1,3 MB).
  - A pasta `.claude` exposta foi removida e os arquivos ocultos agora dão 404.
- **Orbit**: `app/services/blog_seo.py` aplica schema, FAQ, breadcrumb, "Continue lendo" e capa JPG em
  todo artigo publicado automaticamente (testes em `tests/test_blog_seo.py`).
- **Grupo Gestante CLT**:
  - 10 pautas criadas, segundas e quintas às 9h, de 12/10 a 26/11.
  - Prontos em rascunho: o guia completo (12/10) e o de contrato de experiência/temporário (15/10), cada um com o
    texto do post para o Perfil da Empresa em `corpo.legenda`.
  - Fonte: `_saida_producao_1510/artigos_cluster_gestante.py`.
- **Pendências dela** (artefato com campos que salvam para o Claude):
  https://claude.ai/artifact/2Y8ZraLYmWB49cMST554Kr. Ele guarda casos típicos, endereço oficial,
  áudios dos Reels, Search Console, Perfil da Empresa, avaliações e o selo "5.0 no Google". Ler as
  respostas com `ArtifactData` nas coleções `casos`, `dados/nap` e `tarefas`.

### 10/10/2026: Perfil da Empresa no Google

- Manual com checklist para ela: https://claude.ai/artifact/JETQMCUpDvMJSqfN5L42mz. Tem acesso, como
  completar o perfil (descrição e serviços prontos), como publicar pelo celular e pelo computador, regras
  e problemas comuns.
- **Posts prontos**: ficam no banco do artefato (coleção `posts`; doc = slug, com `data`, `titulo`,
  `texto`, `link` e `imagem` em data URI de 1200×900). Gerados por `_saida_producao_1510/posts_google.py`.
  A cada artigo novo, acrescentar o post com `ArtifactData`. A marcação "Publiquei" dela fica em
  `publicados`.
- Os 2 artigos do grupo Gestante (12 e 15/10) foram aprovados e agendados em 10/10.

### 27/10/2026: "rankear mais e furar a bolha" (revisão com os dados do Search Console)

**Dados (28 dias até 24/10, `social_metrics` tipo `google_painel`):** 5.665 aparições (+62% sobre os 28 dias
anteriores, 3.503) e 51 cliques (eram 48). O site é mostrado mais, mas fica no fim da 1ª página e não convence o
clique. 80% das aparições vêm de 5 páginas. O Google só mostra 132 das buscas (o resto é anônimo). Leitura:

- **A porta fora da bolha já existe:** as buscas que caem na página do banheiro são de trabalhador em geral
  ("atendente pode lavar banheiro" 18, "atendente pode fazer limpeza de banheiro" 16, "recepcionista pode fazer
  limpeza" 13, "lavar banheiro é desvio de função" 12, "operador de loja pode fazer limpeza", "funcionário pode
  lavar banheiro da empresa"), posição 5 a 10, quase sem clique. A da recepcionista está na posição 2 a 4.
- **Na beira da 1ª página (posição 8 a 11):** licença-maternidade 180 dias (1.336), pai não paga pensão (328; busca
  com "pai" e com "genitor"), aborto espontâneo/dias de atestado (191), fim da 6x1 (177).
- **Perdidas (posição 20 a 95):** divórcio, atestado falso, plano de saúde. Não investir agora.
- **Busca pelo nome:** "advogada letícia" na posição 5,8 e "leticia barros" na 11. Melhora com autoridade de fora
  (Perfil da Empresa, Jusbrasil, OAB/ES, imprensa), não com texto.
- Busca local ("advogado trabalhista vitória") tem 1 a 2 aparições por mês: não é a alavanca principal.

**Temas trabalhistas mais procurados em 2026 (pesquisa de 27/10):** fim da 6x1 (EC 141, 42 h em 16/12/2026 e 40 h
um ano depois); pejotização (STF Tema 1.389); saúde mental e NR-1; jornada, banco de horas e hora extra; FGTS não
depositado e rescisão indireta (TST Tema 70, fev/2025: basta a falta de depósito, sem imediatidade); teletrabalho;
exames preventivos (Lei 15.377/2026); assédio eleitoral (TST: 79% de acordo ou procedência em 2026). Fontes:
[Âmbito Jurídico](https://ambitojuridico.com.br/guia-completo-de-direitos-trabalhistas-em-2026-para-trabalhadores-brasileiros/),
[Lefosse](https://lefosse.com/newsletter/temas-trabalhistas-a-serem-julgados-no-stf-e-tst-em-2026/),
[EC 141 no Planalto](https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc141.htm),
[Conjur sobre a EC 141](https://conjur.com.br/2026-out-23/a-emenda-constitucional-no-141-da-reducao-da-jornada-e-da-dobra-do-descanso/),
[Contábeis sobre o Tema 70](https://www.contabeis.com.br/artigos/69843/falta-de-fgts-pode-levar-a-rescisao-indireta-alerta-tst/),
[ICL/Folhapress sobre assédio eleitoral](https://iclnoticias.com.br/economia/justica-do-trabalho-fecha-acordo-ou/).

**Feito em 27-28/10:**
- **Grupo novo "O que a empresa pode exigir de você"** (trabalhador em geral, homem e mulher), página principal =
  artigo do banheiro. 5 artigos em rascunho no Orbit, quintas 9h: acúmulo de função (29/10), FGTS não depositado
  (05/11), hora extra não paga (12/11), desconto no salário (19/11), banco de horas e 6x1 (26/11). Cada um com post
  do Perfil da Empresa em rascunho (mesmo dia, 10h). Fonte: `apps/api/_saida_producao_1510/artigos_grupo_funcao.py`
  (+ `posts_google_grupo_funcao.py` e `subir_grupo_funcao.py`). As pautas de gestante das mesmas quintas, sem texto,
  ficaram como estavam: as segundas seguem com o grupo Gestante já aprovado.
- **Revisão de conteúdo no ar** (`producao/seo/2026-10-27-trocas-site.py` → `apps/api/scripts/aplicar_trocas_site.py`):
  - pensão: "caso real do escritório" com valor recuperado (OAB), prescrição errada (não corre contra filho menor,
    CC 197, II), Juizado Especial (não cabe pensão, Lei 9.099, art. 3º, § 2º), BACENJUD → SISBAJUD, prisão (CPC 528),
    resposta rápida;
  - aborto espontâneo: estabilidade errada (TST: gravidez + 2 semanas do art. 395; a partir da 23ª semana é parto),
    quem paga o salário-maternidade, resposta rápida;
  - banheiro: sem valores de dano moral nem "garante", leituras do mesmo assunto;
  - home: tela de carregamento sai em 0,9 s (antes: `load` + 1,4 s) e sem rolagem lateral no celular.
- O 6x1, a carga horária e a aposentadoria híbrida foram corrigidos na mesma noite por outra sessão (commit 8f9d4bf).

**Próximos grupos sugeridos (na ordem):** (1) "Jornada depois da 6x1" (12x36, domingos no comércio, doméstica);
(2) "Saúde e afastamento" (burnout em dez, NR-1, atestado e INSS); (3) "Saída do emprego" (rescisão indireta,
pedido de demissão, acordo, seguro-desemprego), ligando ao artigo da rescisão indireta que já existe.

### Comparação com o 1º resultado, 28/10/2026

Pedido da Jessica (via sessão do Instagram), a partir do método de um Reel: abrir o 1º orgânico da busca,
entender por que ele ranqueia e comparar com a nossa página. **Limite do estudo:** o Google bloqueou a busca
automatizada (captcha) e o Bing devolveu resultados sem relação; os líderes foram identificados pela pesquisa web
em português (próxima do Google, não idêntica). Comparação só para estudo: nada disso vai para conteúdo publicado
(OAB). Densidade de palavra-chave foi ignorada (o Google não usa).

**Busca 1: "atendente pode lavar banheiro"** (nossa página: banheiro, posição 5,7, 2.583 aparições, 0 cliques).
Quem aparece em cima: notícias de tribunal (TRT-SC, garçom, 2016), imprensa (O Tempo, atendente de fast-food,
2023), Jus.com.br (fórum de 2016, ~200 palavras, título com erro) e escritórios com texto genérico.

| Eles têm e nós não | Nós temos e eles não |
| --- | --- |
| Domínio forte (Jus, tribunal, jornal) | Resposta direta na 1ª frase, por função (atendente, recepcionista, operador) |
| Decisão real com tribunal e data | Perguntas frequentes com schema, autora com OAB, data de atualização |
| Formato de notícia ("Justiça concede...") | Exemplo prático, passo a passo de prova, links do mesmo assunto |

Leitura: a página já é melhor que a dos concorrentes; perde em autoridade do domínio e o Google provavelmente
responde a pergunta no próprio resultado. **Feito hoje:** seção "O que a Justiça já decidiu" (TRT-SC 2016 e TRT-MG
2023, sem valores).

**Busca 2: "licença maternidade 180 dias"** (nossa página: licença 180 dias, posição 8,7, 1.336 aparições).
Quem lidera: Serasa e C6 Bank (marcas fortes, guias longos de 4-6 mil palavras), Marra CLT e Direitos da Mamãe
("Como conseguir em 2026": resposta rápida, tabela por situação, passo a passo, prazo, quem paga, 6 perguntas
frequentes, advogada com OAB e data de atualização).

| Eles têm e nós não (antes de hoje) | Nós temos e eles não |
| --- | --- |
| A intenção "como conseguir": passo a passo e prazo destacados | Explicação correta da ADI 7.495 (muita gente erra) |
| Tabela "quem tem 120, quem tem 180" | Autora advogada com OAB, voz própria |
| Quem paga os 60 dias e a dedução do IR | Perguntas frequentes com schema |
| Links para salário-maternidade, estabilidade, retorno | |

Leitura: o nosso artigo era notícia ("o que o STF decidiu de verdade") e a busca quer o guia prático; os links do
fim levavam para pet no divórcio, violência de gênero e Pix da pensão. **Feito hoje:** tabela por situação, "Como
pedir (passo a passo)", "Quem paga os 60 dias", pergunta nova (texto e schema), links para o guia da gestante, mãe
adotante e paternidade.

**Busca 3: "advogado trabalhista vitória es"** (nossa página: área trabalhista, posição 13-18).
O que decide é o mapa (Perfil da Empresa: avaliações, distância, categoria), que não deu para ver (captcha). Os
sites orgânicos de concorrentes são fracos: H1 "BLOG", sem endereço, sem mapa, sem OAB, sem perguntas locais; um
mostra 8 avaliações do Google na página; o Jusbrasil aparece com o diretório de advogados de Vitória.

| Eles têm e nós não | Nós temos e eles não |
| --- | --- |
| Página antiga e "advogado trabalhista em Vitória" repetido no texto | Título certo ("Advogada Trabalhista em Vitória-ES"), schema LegalService e FAQPage |
| Perfil no diretório do Jusbrasil por cidade | OAB, endereço no rodapé, Grande Vitória citada, links para 6 artigos |

Leitura: a busca local se ganha no Perfil da Empresa e em citações (Jusbrasil, OAB/ES, diretórios), não no texto.

**Mudança no código (vale para todo artigo publicado daqui em diante):** o "Continue lendo" escolhia os 3 artigos
mais recentes da área; agora escolhe pelo assunto (`blog_seo.escolher_relacionados`, commit 7c7910e). Precisa de
deploy da API (barrado pela trava de segurança em 28/10; pendente).

**Ações em ordem de impacto**
1. **Responder a intenção da busca, não a notícia**: nas páginas na posição 5-15, abrir com a resposta, ter
   "como fazer/pedir" em passo a passo e tabela "quem tem direito". Feito na licença; próximas: pensão (já tem
   resposta rápida), aborto (feito), 6x1 (feito por outra sessão).
2. **Links do mesmo assunto** em todo artigo (código feito; deploy pendente) e grupos de artigos ligados entre si
   (grupo "O que a empresa pode exigir" em rascunho).
3. **Autoridade de fora**: perfil completo no Jusbrasil (aparece no diretório de Vitória), OAB/ES com o site,
   imprensa local (TV Tribuna, A Gazeta) com link, Bing Webmaster Tools.
4. **Perfil da Empresa**: avaliações que citem área e cidade, 1 post por semana com link de artigo (os 5 do grupo
   novo já estão em rascunho), categoria "Advogado trabalhista".
5. **Decisões públicas citadas** (tribunal, turma, ano) nos artigos de dúvida prática: é o que os jornais e
   tribunais têm e dá confiança (E-E-A-T).

**Veredito:** o plano está no caminho certo (grupos de artigos, revisão dos mais vistos, Perfil da Empresa); a
comparação confirmou que o conteúdo já é melhor que o da maioria dos concorrentes. O que faltava era **formato de
"como fazer" nas páginas que estão na beira da 1ª página** e **links do mesmo assunto**, que foram corrigidos hoje,
e **autoridade de fora do site**, que depende da Dra. (Jusbrasil, avaliações, imprensa). Não trocar a estratégia;
acrescentar a regra "toda página na posição 5-15 ganha passo a passo, tabela e decisão real" e medir em 17/11.
