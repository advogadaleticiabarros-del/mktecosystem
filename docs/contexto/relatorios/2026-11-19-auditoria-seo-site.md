# Auditoria de SEO do site da Dra. (19/11/2026)

## Pedido
A Jessica mandou um Reels do @promptepipoca (instagram.com/reel/Df4ylFHDoKe) que mostra a skill claude-seo e o comando
`/seo audit seusite.com.br`, pedindo para "colocar para analisar no meu site". Depois pediu "instale" (o motor da skill).

## Feito
- Reels assistido pela skill `watch` (sem áudio transcrito; o conteúdo veio dos quadros e legendas na tela).
- Motor da claude-seo 2.5.0 instalado com `claude-seo setup` (ambiente isolado em `%LOCALAPPDATA%\claude-seo\.venv`,
  com Chromium). Fora do repositório.
- Auditoria de advogadaleticiabarros.com.br: `docs/seo/auditoria-2026-11-19/RELATORIO-AUDITORIA.md` (nota 76/100,
  15 problemas em ordem de prioridade e plano em 4 fases).
- Nenhuma mudança no site.

## Verificado
- 82 URLs do sitemap respondem 200; redirecionamentos http/www corretos; 404 real; `llms.txt` válido.
- Duplicatas `/lp-v3/` indexáveis, 5 LPs sem canonical, links internos para `index.html` e com UTM: conferidos no HTML.
- O "(27) 99999-9999" da home é só o placeholder do campo de telefone do formulário (não é erro).
- Não verificado: velocidade real (PageSpeed recusou por cota), Search Console, Analytics e backlinks.

## Decisões e porquês
- Auditoria feita na mesma sessão, sem abrir os vários agentes da skill: mesmo resultado com custo menor.
- Relatório salvo como Markdown no repositório (não publicado como página).

## Pendente
- Jessica decide se aplica as correções; a Fase 1 (imagens WebP, redirecionar `/lp-v3/` para `/lp/`, canonical/schema
  das LPs) é a de maior efeito.

## Próxima sessão
Se ela autorizar: começar pela Fase 1 do relatório; publicação via SFTP na VPS (ver `docs/CONTEXTO_PROJETO.md`, "Site
principal na VPS"). Skills: `claude-seo:seo-images`, `claude-seo:seo-schema`, `leticia-seo-local`. Medir antes e depois em
pagespeed.web.dev.
