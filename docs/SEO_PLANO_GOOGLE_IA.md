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
