# 20/10/2026 — Site da Letícia: schema, llms.txt e IndexNow (Bing)

## Pedido
Ela perguntou se dava para usar "prompt injection invisível" a nosso favor. A resposta foi não: texto oculto é spam no Google e é risco perante a OAB. Ofereci o caminho legítimo (GEO) e ela respondeu "sim, verifique". Depois aprovou as três correções ("SIM") e pediu: "Bing Webmaster Tools. O ChatGPT busca muito pelo Bing… veja se temos isso também, se não tiver faça de todas as páginas".

## Feito
- **No site, direto pelo SFTP da VPS** (o código do site não está no git), detalhes em `docs/CONTEXTO_PROJETO.md`, seção "Site da Letícia: descoberta por buscadores e IAs":
  - home sem `aggregateRating` e com `@id #escritorio`;
  - `sobre.html` com `ProfilePage` + `Person`;
  - as 7 `areas/*.html` com `Service`, `FAQPage` e `BreadcrumbList` (mais canonical nas duas páginas que não tinham);
  - `llms.txt` refeito, com 66 links;
  - arquivo da chave do IndexNow na raiz;
  - 69 URLs enviadas ao IndexNow.
- **No Orbit, commit `6bba6d2`:** novo `apps/api/app/services/site_descoberta.py` (`gerar_llms_txt`, `avisar_indexnow`), chamado em `blog_publisher._publicar_artigo`. Atualizados os testes e a skill `leticia-blog-artigo`. O commit também levou notas de contexto de 19/10 que estavam no working tree sem commit.

## Verificado
- Testes do blog: 24 passaram (`test_site_descoberta`, `test_blog_publisher`, `test_blog_seo`, `test_blog_index_editor`).
- JSON-LD de todas as páginas alteradas validado com `JSON.parse`.
- Conferido no ar por curl: home sem `aggregateRating` e com status 200, `Person` na "Sobre", Service/FAQ/Breadcrumb nas áreas, `llms.txt` com 66 links, chave acessível.
- IndexNow: `api.indexnow.org` respondeu 202. `www.bing.com/indexnow` respondeu 403, provavelmente porque a chave nova ainda não foi validada. Não verificado se o Bing já processou.
- **Não verificado:** a automação em produção, porque o deploy não foi feito (ver Pendente). Também não passei as páginas no Rich Results Test do Google.

## Decisões e porquês
- **`aggregateRating` removido** porque a página não mostra as avaliações. Isso viola a diretriz do Google e é zona cinzenta no Provimento 205.
- **Chave do IndexNow como constante no código**, porque ela é pública por definição; assim não foi preciso mexer no `.env` da VPS.
- **`llms.txt` gerado a partir do `blog/index.html`**, que tem todos os 47 artigos, para manter uma fonte única. Antes faltavam 14 artigos e havia links repetidos.
- **Na "Sobre", `worksFor` aponta para a Santiago Prado & Barros sem `@id`**, para não fundir essa entidade com a da home, que tem outro nome.
- **Bing Webmaster Tools:** o cadastro é com a conta dela, que disse que vai fazer. Importar do Google Search Console dispensa arquivo de verificação.

## Pendente
- **Push e deploy do `6bba6d2`.** O push foi recusado (403) para a conta ativa `alcancelegalmkt-collab`, que não tem acesso ao `advogadaleticiabarros-del/mktecosystem`. Usar a conta dona sem trocar a ativa foi bloqueado pelo modo automático. A Jessica decide: liberar o push pela conta `advogadaleticiabarros-del` ou dar acesso à conta colaboradora. Até o deploy, artigo novo publicado pelo Orbit **não** atualiza o `llms.txt` nem avisa o Bing.
- **Bing Webmaster Tools** (com a Jessica). Se o Bing pedir `BingSiteAuth.xml` ou a meta `msvalidate.01`, subir na raiz.
- **Opcional:** schema `Person` também em `escritorio.html` e nas LPs.

## Atualização (mesmo dia)
- Com autorização da Jessica, o push foi feito pela conta `advogadaleticiabarros-del` (a conta ativa continua `alcancelegalmkt-collab`). Deploy feito na VPS: o container `api` foi refeito e o import do publicador foi conferido.
- O pedido para dar acesso de escrita à `alcancelegalmkt-collab` foi bloqueado pelo modo automático, então não foi feito. Ela pode convidar em github.com/advogadaleticiabarros-del/mktecosystem/settings/access.
- `www.bing.com/indexnow` continua respondendo 403 depois do deploy. Provável causa: o Bing só aceita o envio direto depois que o site estiver no Bing Webmaster Tools.

## Próxima sessão
1. `git push origin main` com uma conta que tenha acesso.
2. Na VPS: `cd /home/orbit-src && git pull --ff-only && cd deploy/vps && docker compose up -d --build api`.
3. Conferir de novo `https://www.bing.com/indexnow`, que deve sair do 403.

Skills: `contexto-orbit`, `leticia-blog-artigo`, `leticia-seo-local`.
