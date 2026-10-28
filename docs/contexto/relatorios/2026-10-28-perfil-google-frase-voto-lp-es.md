# 28/10/2026: Perfil na Pesquisa do Google, frase "demitido pela posição política", LP do ES e post do Google

## Pedido
1. Analisar um Reel (Plinio Ventavoli) sobre o "Perfil na Pesquisa" do Google e dar o passo a passo. Depois: "vamos fazer
   as demais coisas, já que ainda não cheguei em 10000 seguidores, vamos trabalhar para isso" e "estamos muito parados".
2. Post imediato "igual a esse": frase da @draraqueladvogadadelas ("Se você for demitido por sua posição política,
   nosso escritório vai te atender gratuitamente!"), com legenda "com a nossa cara, que chame a atenção".
3. "Um post para o Google, uma LP nova para o site com esse assunto especificamente, pesquise como está a procura".

## Feito
- **Perfil na Pesquisa (creators.google/profile):** exige 10 mil seguidores em uma rede (Instagram, TikTok, YouTube ou X)
  e só existe nos EUA, no Canadá e na Índia (Ajuda do Google, 28/10). A Dra. tem cerca de 415 no Instagram. Equivalente
  hoje: Perfil da Empresa com as redes + `sameAs` no site + reivindicar o painel de informações.
- **Site/blog:** `sobre.html` e `index.html` já tinham `sameAs` com Instagram, LinkedIn e Facebook (no ar). Os artigos
  novos agora ligam a autora ao `@id` do Person de `sobre.html` e às 3 redes: `apps/api/app/services/blog_seo.py`
  (`ID_DRA`, `REDES_DRA`) + teste em `tests/test_blog_seo.py`. Os artigos já publicados não foram reprocessados.
- **Frase (feed):** `producao/frases/2026-10-28-demitido-posicao-politica/frase-demitido-posicao-politica-1080x1440.png`
  (texto igual ao de referência, League Spartan 800, fundo escuro, "gratuitamente!" em dourado, assinatura OAB).
  Script de render: só no scratchpad da sessão (HTML simples, fácil de refazer). Legenda e primeiro comentário: na
  conversa (não salvos em arquivo).
- **LP nova do ES:** `lp/assedio-eleitoral-es.html`, gerada por
  `producao/campanhas/2026-10-assedio-eleitoral/blog-lp/gerar_lp_es.py` a partir de `lp/demissao-por-voto.html`
  (mesmo visual e formulário; marca `[LP assedio-eleitoral-es]`, campanha `assedio-eleitoral-es-2026`). Conteúdo local:
  47 denúncias no MPT-ES até 27/10 (+57% em uma semana), 19 TACs e 3 ações, denúncia na PRT 17ª Região
  (prt17.mpt.mp.br), TRT-17, FAQ local. O guia de provas fica só na LP nacional (link), para não duplicar.
  Publicador: `blog-lp/publicar_lp_es.py` (roda dentro do container da API, recusa sobrescrever).
- **Post do Google:** `producao/campanhas/2026-10-assedio-eleitoral/google-post-es/` (imagem 1200×900, texto e botão
  com UTM em `post-google.md`, gerador `gerar_imagem.py`).

## Verificado
- `pytest tests/test_blog_seo.py`: 23 passaram (o teste novo falhou antes da mudança).
- LP do ES aberta no Chromium (390 px e 1280 px): sem erro de JS, sem rolagem lateral. Formulário não foi enviado de teste.
- Números do ES conferidos em A Gazeta (balanço do MPT-ES de 27/10). Nacionais: O Povo, ConJur, Brasil de Fato.
- **Não verificado:** volume de busca (o Google Trends não aparece nas buscas; não há dado de volume). LP do ES e post do
  Google **não estão no ar** (o modo automático bloqueou o envio para a VPS e a leitura do banco de produção).

## Decisões e porquês
- A Jessica pediu para manter o texto da frase mesmo com o alerta (CED art. 30 §3º e manual: proibido "consulta
  gratuita"/oferta de serviço): "pule a ética, eu me responsabilizo". A frase foi feita igual e **não foi agendada**:
  quem publica é ela. O risco disciplinar é da inscrição da Dra.
- LP nova com ângulo **Espírito Santo** em vez de uma segunda LP nacional (as duas iam disputar as mesmas buscas).
- A LP nacional diz "~10x mais denúncias que em 2022", mas o MPT (via A Gazeta) dá 3.373 em 2022 contra 2.364 em 2026
  até 27/10. A comparação não foi repetida na LP do ES. A LP nacional **não foi corrigida** (esperando a Jessica).
- Plano de crescimento: a Jessica pediu "o ideal" e "os dois por igual" (Instagram e TikTok). Recomendação: ligar as 4
  mudanças de `docs/ANALISE_INSTAGRAM_2026-10-27.md` §4 (Trial Reels 2/semana, legenda pedindo envio, 1 Reels/semana
  com rosto, teste sexta 15h por 4 semanas). **Ainda não implementado**: a sessão parou para o post imediato.

## Pendente
- Publicar a LP do ES: liberar o comando ou rodar `scp` da LP e do `publicar_lp_es.py` para `/tmp` da VPS,
  `docker cp` no container da API e `docker exec -w /app <api> python /tmp/publicar_lp_es.py`. Depois, incluir no
  `sitemap.xml` e avisar o IndexNow. (Jessica libera.)
- Post do Google: cadastrar no Orbit (`google_posts`) ou direto no Perfil da Empresa, com a imagem e o texto da pasta.
- Corrigir ou tirar o "~10x" da LP nacional (Jessica decide).
- `@` do TikTok da Dra. para o `sameAs` do site; @ da página do escritório no LinkedIn no `sameAs` do LegalService.
- Perfil da Empresa: conferir links das redes (Editar perfil > Perfis de mídia social), feito pela conta dela.
- Ligar as 4 mudanças do plano de crescimento (acima) e redeploy da API para o `blog_seo.py` valer.

## Próxima sessão
Publicar a LP do ES (comando acima), cadastrar o post do Google e então ligar o plano de crescimento em
`app/services/agenda.py` e nos prompts de `app/routers/content.py`. Skills: `contexto-orbit`, `leticia-seo-local`,
`codebase-design` + `tdd`.

## Atualização (mesmo dia): LP do ES juntada à nacional
- Pedido: "junta com essa lp, e deixa mais completa". `lp/assedio-eleitoral-es.html` e o gerador saíram (ficam no
  histórico do git); `lp/demissao-por-voto.html` ganhou a seção `#espirito-santo`, o atalho no topo, MPT-ES no passo 1
  da denúncia, "sem prova o MPT ainda investiga", 4 perguntas novas (FAQ e schema: 11) e números corrigidos
  (2.364 no ano, +500 depois do 2º turno, 47 no ES; sem "recorde" nem "~10x 2022").
- Verificado: JSON-LD válido, sem erro de JS e sem rolagem lateral a 390 px. A versão no ar só diferia na versão do
  `conversoes.js` (a do git é a mais nova).
- Publicar: copiar `lp/demissao-por-voto.html` e `blog-lp/publicar_lp_v2.py` para `/tmp` da VPS, `docker cp` no
  container da API e `docker exec -w /app <api> python /tmp/publicar_lp_v2.py` (faz backup antes). **Não publicado.**
- Post do Google agora aponta para `demissao-por-voto.html#espirito-santo`.
- Ainda com o número antigo ("quase dez vezes 2022", "recorde"): o artigo do blog no ar e as peças já publicadas
  (carrossel, Stories, legendas). Peças publicadas não se mexe; o artigo espera o ok da Jessica.
- Frases novas sugeridas na conversa (variações mais suaves e com gancho de números), sem arte ainda.
- Frases escolhidas pela Jessica viraram arte no mesmo estilo (a primeira ficou intacta), em
  `producao/frases/2026-10-28-demitido-posicao-politica/` (gerador `gerar_frases.py`): `frase-escritorio-orientar`,
  `frase-500-denuncias-ilegal`, `frase-eleicao-acabou`, `frase-2364-denuncias-es` (as 3 com número têm a linha da fonte
  do MPT). Nenhuma foi agendada.
- **No Orbit (rascunho), pedido "coloque no orbit":** pauta `d7b867af`, 5 peças `tipo="frase"` com legenda, primeiro
  comentário, alt e `programacao`: 28/10 19h (gratuitamente), 29/10 12h (eleição acabou), 30/10 12h (2.364/ES), 31/10
  12h (500 ilegal), 01/11 12h (orientar). Imagens em `/app/media/voto-frase-*.jpg` (HTTP 200). Script
  `producao/frases/2026-10-28-demitido-posicao-politica/subir_orbit.py` (idempotente). Conflito com a regra de 1 feed
  por dia: 29/10, 31/10 e 01/11 já têm carrossel/post "pronto"; a Jessica decide a troca de datas ao aprovar.
- **Postadas à mão (Jessica, 28/10):** as 5 frases foram para `status="publicado"`, sem `programacao` (guardada em
  `corpo.postado_manualmente`). A "eleição acabou" já tinha 1 agendamento (aprovada no Orbit), que também foi para
  "publicado", para o publicador não postar de novo. Script: `marcar_postadas.py` na pasta das frases. O conflito de
  datas deixou de existir.
- **LP publicada (28/10, "Publica a LP"):** `publicar_lp_v2.py` no container; backup da versão anterior em
  `/tmp/bkp_lp_voto_v1.html` (dentro do container da API, some se ele for recriado; a v1 também está no git em
  `cf014b6`). Conferido: a página no ar é idêntica à de `lp/demissao-por-voto.html`, com `#espirito-santo` e 2.364.
- **Artigo corrigido no ar (28/10, "corrije"):** `blog-lp/corrigir_artigo_numeros.py` trocou o parágrafo do "1.939,
  recorde, quase dez vezes 2022" pelos números de 27/10 (2.364 no ano, +500 depois do 2º turno, 47 no ES, com link
  para `#espirito-santo`), tirou a comparação com o pico de 2022 (não conferida) e pôs `dateModified` 28/10. Backup em
  `/tmp/bkp_artigo_voto_v1.html` no container. Conferido no ar: sem "1.939", "recorde" ou "dez vezes".
- **IndexNow respondeu 403** ("UserForbiddedToAccessSite") ao avisar o artigo, mas a chave
  `/6bc7d2f33225bd1d3c4af27b891f2ac6.txt` responde 200. Antes dava 202. Investigar no Bing Webmaster (pendente).
- **Post do Google publicado (28/10, "leve para o orbit e já publique"):** `google_posts` f9fe7650 (aprovado →
  `publicar_post` na hora), botão Saiba mais → LP `#espirito-santo` com UTM google/gbp-post. Link do post:
  local.google.com (id do lugar 5130877975844596468). Script: `google-post-es/publicar_post_google.py`.
