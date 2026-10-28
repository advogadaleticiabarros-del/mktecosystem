# Google: furar a bolha (27-28/10/2026)

## Pedido

"preciso rankear mais no google, meu conteudo tem que furar a bolha" e, depois, "faça o que for necessario, pesquise
os temas mais falados no direito trabalhista, revise o site, a aparencia, se engaja, se encanta tudo".

## Feito

- **Análise com dados reais** do Search Console (banco do Orbit, `social_metrics` tipo `google_painel`) e pesquisa
  dos temas trabalhistas de 2026: registrada em `docs/SEO_PLANO_GOOGLE_IA.md`, seção "27/10/2026".
- **Revisão no ar** (commit 084992b): `apps/api/scripts/aplicar_trocas_site.py` + `blog_seo.aplicar_trocas` (a função e
  os testes entraram no commit 8f9d4bf da outra sessão, que dividia o repositório). Trocas em
  `producao/seo/2026-10-27-trocas-site.py/.json`:
  - pensão: o "caso real" com valor recuperado foi retirado (OAB) e foram corrigidos a prescrição, o Juizado Especial,
    o SISBAJUD e a prisão; entrou uma resposta rápida;
  - aborto espontâneo: estabilidade e quem paga o salário-maternidade;
  - banheiro: saíram os valores de dano moral e o "garante"; entraram leituras do mesmo assunto;
  - home: tela de carregamento e rolagem lateral no celular.
- **5 artigos novos em rascunho** (grupo "O que a empresa pode exigir de você", quintas de 29/10 a 26/11) e **5 posts
  do Perfil da Empresa em rascunho**: `apps/api/_saida_producao_1510/artigos_grupo_funcao.py`,
  `posts_google_grupo_funcao.py` e `subir_grupo_funcao.py`; capas em `pecas/`, fotos e créditos em `_fotos_pexels/`.
- `docs/CONTEXTO_PROJETO.md`: seção "Google: furar a bolha" e pendência nova.

## Verificado

- Testes de `blog_seo`: 17 passaram.
- Simulação na VPS: as 41 trocas conferiram nas 4 páginas. Aplicado com backup em
  `/root/orbit-backups/site-trocas-20261028-0118.tgz`.
- Site público com Playwright, no celular:
  - a tela de carregamento sai em 0,9 s;
  - a largura é de 390 px na home e nos 3 artigos;
  - não há erro de JavaScript;
  - os textos novos estão no ar e os antigos sumiram.
- `verificar_texto_oab` nos 5 artigos: nenhum alerta.
- Carga no Orbit: criou 5 artigos e 5 posts; a 2ª execução não criou nada (idempotente). As capas respondem 200 no
  endereço público da mídia.
- **Não verificado:**
  - os 5 artigos renderizados no modelo do blog (só serão gerados na publicação);
  - a causa do 403 do IndexNow.

## Decisões e porquês

- As LPs com "Enviar meu caso para análise" **não** foram mudadas. O texto está nas 10 páginas, no mesmo modelo, e
  não é "análise gratuita". Ficou como decisão da Dra.
- O 6x1, a carga horária, a híbrida e o `conversoes.js` ficaram com a outra sessão (`mktecosystem-78`). Isso foi
  combinado por mensagem.
- Grupo novo nas quintas: as pautas de gestante dessas datas não tinham texto e continuam lá; as segundas seguem
  com gestante. Assim o grupo fala com trabalhador em geral sem tirar o que ela já aprovou.
- Foto do desconto no salário trocada: a primeira tinha placas em russo.
- Valores em reais escritos por extenso e "em dobro" no lugar de "100%", para passar no verificador de OAB do Orbit.

## Pendente

- **Dra. Letícia / Jessica:**
  - aprovar os 5 artigos (o primeiro sai quinta, 29/10, às 9h) e os 5 posts do Google (tela "Google e site");
  - cadastrar o site no Bing Webmaster Tools (IndexNow deu 403);
  - decidir o texto das LPs, o selo "5.0 no Google" e o "© 2025".
- **Sessão do `conversoes.js`:** caixa de contato duplicada nos artigos (`.article-cta` + `.contato-meio`). Já
  avisada.

## Próxima sessão

Em 17/11/2026, ler o `google_painel` mais recente e comparar a posição das buscas de função e limpeza, da pensão e do
aborto com a seção 27/10 de `docs/SEO_PLANO_GOOGLE_IA.md`. Depois, escrever o próximo grupo ("Jornada depois da
6x1"). Skills: `contexto-orbit`, `leticia-seo-local`, `voz-leticia`, `leticia-blog-artigo`.
