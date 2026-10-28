# Comparação com o 1º resultado do Google (28/10/2026)

## Pedido

Pedido da Jessica, repassado pela sessão do Instagram (`mktecosystem-ef`): seguir o método de um Reel. Pesquisar a
busca, abrir o 1º orgânico e perguntar "por que ele ranqueia?". Depois, comparar com a nossa página e dizer se
estamos no caminho certo. Em seguida a usuária escreveu: "Faça tudo o que for necessário para o sucesso".

## Feito

- **Análise das 3 buscas** ("atendente pode lavar banheiro", "licença maternidade 180 dias", "advogado trabalhista
  vitória es") e veredito: `docs/SEO_PLANO_GOOGLE_IA.md`, seção "Comparação com o 1º resultado, 28/10/2026".
- **Commit 7c7910e:**
  - `blog_seo.escolher_relacionados` passou a escolher por assunto e sem repetir artigo (testes em
    `tests/test_blog_seo.py`);
  - trocas `producao/seo/2026-10-28-trocas-site.py/.json`.
- **No ar** (backup `/root/orbit-backups/site-trocas-20261028-0929.tgz`):
  - licença 180 dias: tabela por situação, passo a passo do pedido, quem paga, pergunta nova no FAQ e no JSON-LD,
    links de gestante no lugar de pet, violência de gênero e Pix;
  - banheiro: "O que a Justiça já decidiu", com TRT-SC 2016 e TRT-MG 2023.

## Verificado

- 20 testes de `blog_seo` passaram.
- Simulação do "Continue lendo" com o índice real do blog:
  - hora extra → carga horária;
  - banco de horas → 6x1;
  - licença → paternidade e mãe adotante.
- Simulação na VPS e depois a aplicação: as 2 páginas mudaram.
- No ar, com Playwright:
  - largura de 390 px e nenhum erro de JavaScript;
  - os textos novos aparecem;
  - o JSON-LD do FAQ lê sem erro (7 perguntas na licença);
  - os 3 artigos indicados são de gestante.
- Verificador de OAB: nenhum alerta.
- **Não verificado:**
  - a posição real no Google: o Google bloqueia busca automatizada (captcha), e os líderes vieram da pesquisa web;
  - o mapa local.

## Decisões e porquês

- O Bing headless foi descartado como régua: devolveu dicionário para "licença" e Cachoeirinha-RS para "Vitória".
- O artigo da licença foi complementado, não reescrito, porque as 2.537 palavras e a explicação da ADI 7.495 estão
  certas. Faltava o formato "como conseguir".
- As decisões citadas são públicas, de outros processos, sem valores (OAB permite; caso próprio, não).

## Pendente

- **Deploy da API na VPS** (`git pull --ff-only` + `docker compose up -d --build api`), barrado pela trava de
  segurança; precisa da liberação da usuária. Sem ele, o artigo de 29/10 sai com o "Continue lendo" antigo.
- **Dra.:**
  - aprovar os 5 artigos do grupo novo e os posts do Google;
  - Jusbrasil completo, avaliações que citem área e cidade, Bing Webmaster Tools.

## Próxima sessão

1. Se o deploy foi liberado, rodar `cd /home/orbit-src && git pull --ff-only && cd deploy/vps && docker compose up -d
   --build api`.
2. Em 17/11, comparar a posição da licença e do banheiro com a seção de 28/10 do plano.
3. Aplicar a regra "posição 5-15 ganha passo a passo, tabela e decisão real" à pensão e ao aborto.

Skills: `contexto-orbit`, `leticia-seo-local`, `voz-leticia`.
