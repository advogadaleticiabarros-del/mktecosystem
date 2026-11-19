# 19/11/2026: carrossel e artigo do decreto da escala 5x2

## Pedido
A Jessica mandou o carrossel do TST (instagram.com/p/Df7ZFwQhh2r) e pediu "Faça um desse", depois "Aplicando a Dra
Letícia é claro". Depois: "pode postar agora" (assunto viral, postar hoje) e "faça um artigo com as maiores dúvidas e publique, para aumentarmos os cliques no blog e ranquear no google e IAs".

## Feito
- Carrossel de 8 páginas (1080×1440) em `producao/estilos/escala-5x2/` (ver o `README.md` da pasta): capa-manchete,
  as duas etapas (16/12/2026 e 16/12/2027), 14,8 milhões na 6x1, mulheres com 6,8 h a mais de tarefas da casa,
  jornada longa = salário menor (café, sem "R$", barras), descanso e produtividade, "Guarde desde já" (salvável) e
  fecho com o retrato real da Dra.
- Legenda e primeiro comentário em `editorial.json`; página de conferência publicada:
  https://claude.ai/artifact/Dgf7zpuSyUWP78B452Chh5.

- Artigo publicado: https://advogadaleticiabarros.com.br/blog/escala-5x2-decreto-duvidas.html ("Escala 5x2: as 12 maiores
  dúvidas sobre o decreto, respondidas"). Fonte em `producao/blog/novos-2026-11-19/` (rascunho `.md`, `montar_spec.py`
  com bloco FAQPage, `publicar.py`, `faq_no_head.py`). Rodado no `vps-api-1`; backup do índice, sitemap e llms.txt em
  `/tmp/bkp_blog_20261119-220826` dentro do contêiner.
- O publicador tira `<script>` do corpo; o FAQPage foi posto no `<head>` da página publicada por `faq_no_head.py`
  (cópia do HTML anterior em `/tmp/bkp_escala-5x2-decreto-duvidas_*.html` no contêiner).

## Verificado
- Decreto assinado em 19/11/2026: notícias do Planalto e do MTE. 14,8 milhões: MTE/eSocial (março de 2026).
- As 8 artes foram vistas uma a uma depois do render (sem marca de terceiro nem texto estrangeiro visível).
- O artigo do blog "escala-42-horas-16-de-dezembro…" ainda dá 404, por isso o link saiu do comentário.
- Artigo no ar (curl): `article-hero` presente, zero `blog-grid`, card no índice, no sitemap e no llms.txt, capa 200,
  JSON-LD BlogPosting + BreadcrumbList + FAQPage com 12 perguntas. Decreto nº 13.173 (DOU extra de 19/11): Band, O Povo,
  Gazeta do Povo e HoraMS.
- IndexNow (Bing) respondeu 403 "UserForbiddedToAccessSite", pelo Orbit e direto em bing.com/indexnow, com o arquivo
  de chave no ar (200). O Bing NÃO foi avisado.
- Não verificado por conta própria: PNAD 2022 (6,8 h), Ipea/RAIS 2023 e OIT (citados como o TST cita).

## Decisões e porquês
- Estrutura da referência com a identidade da marca (regra das referências de 18/11), mais as duas páginas padrão da
  Dra. (salvável e fecho com retrato). 8 páginas em vez de 7 do v5.
- Fotos novas do Pexels baixadas por link direto: a busca pela chave do Orbit na VPS foi bloqueada pelo modo automático,
  e as candidatas do banco local já tinham sido usadas em outras peças.
- Página de salário em café: é o acento escuro do carrossel (feed claro).

## Pendente
- Jessica: postar o carrossel hoje pelo app (não há publicação automática de carrossel daqui; a VPS também foi
  bloqueada para a busca de fotos). Depois, registrar a peça no Orbit como publicada.
- Jessica: pedir indexação do artigo no Google Search Console ("Inspecionar URL" → "Solicitar indexação") e enviar a
  URL no Bing Webmaster Tools; investigar o 403 do IndexNow (provável reverificação do site no Bing depois da mudança
  para a VPS em 16/11).
- Dra.: conferir o artigo (texto novo, publicado a pedido da Jessica sem revisão dela).
- Dra.: conferir os textos (seção "Textos novos" da conferência).
- Antes de publicar: reconferir a liminar do STF (ADIs 8.041 e 8.042), que vai ao Plenário.

## Próxima sessão
Com a aprovação, subir as 8 artes ao Orbit e trocar a peça de 22/11 na agenda (ver `referencias-1811/agendar.py` como
modelo). Skills: `leticia-carrossel`, `contexto-orbit`.
