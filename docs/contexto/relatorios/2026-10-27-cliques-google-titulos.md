# 27/10/2026 · Cliques no Google: títulos e descrições do site

## Pedido
Print da tela "Google e site": "o que devemos fazer para aumentar esses cliques?", depois "faça tudo que puder para
mim, vamos reverter isso, mais cliques, mais conversões" e, sobre a VPS, "você já tem acesso".

## Feito
- Auditoria pública das 71 páginas do sitemap (título, descrição, eventos de contato). Quase todo título passava de
  60 caracteres (sufixo `| Dra. Letícia Barros`), descrições de 160-220, três com termos vetados pela OAB, índice do blog
  com duas meta descriptions.
- Gerador de artigos (Orbit): `titulo_da_aba` (marca só quando cabe em 60) nos templates de artigo e jornal;
  `REGRAS_TITULO_GOOGLE` nos prompts de artigo e jornal.
- `blog_seo.trocar_titulo_e_descricao` (troca só `<title>` e meta description, junta metas repetidas em qualquer ordem
  de atributo) e `apps/api/scripts/aplicar_titulos_google.py` (simula por padrão, backup .tgz, IndexNow).
- 66 títulos/descrições novos em `producao/seo/2026-10-27-titulos-google.json`, com o motivo de cada um.
- Deploy da API na VPS (backup do banco `/root/orbit-backups/antes-titulos-google-20261027.sql.gz`, `git pull`, rebuild).
- Aplicados os 66 títulos/descrições no site (backup `/root/orbit-backups/site-titulos-20261027-1544.tgz`), IndexNow avisado.
- Lidas as consultas e páginas do Search Console no painel salvo; 2 títulos refeitos pelas buscas reais (180 dias e
  pensão atrasada), aplicados (backup `site-titulos-20261027-1546.tgz`).
- Contato nos artigos (pedido "faça o que precisa"): `producao/site/conversoes.js` faz o botão dos blocos de contato abrir o
  WhatsApp direto (antes levava à página de contato); `apps/api/scripts/publicar_conversoes.py`; templates e LPs com
  `?v=20261027`; commit `fcf1a16`, API recriada na VPS (backup `antes-conversoes-v20261027.sql.gz`).
- Artigos corrigidos (pedido "Corrija você!"): híbrida e carga horária reescritas, datas da EC 141 no 6x1; commit `8f9d4bf`,
  publicados com backup `/root/orbit-backups/site-artigos-20261028-0114.tgz` e IndexNow.
- Contexto em `docs/CONTEXTO_PROJETO.md` (seção "Cliques no Google" e pendência).

## Verificado
- Testes: 344 da API passaram após a mudança do template e do prompt; depois, 19 de `test_blog_seo` e
  `test_render_artigo_blog` (5 novos).
- Simulação nas cópias baixadas das 66 páginas: todas ficam com um `<title>` e uma meta description.
- Todos os títulos ≤ 60 caracteres; descrições entre 110 e 155; sem travessão nem termos vetados.
- Site público conferido de fora: as 66 páginas mostram o título e a descrição novos, com uma meta description só.
- API recriada na VPS (`f899d21`, que inclui `8408cba`).
- GA4 (pedido seguinte, depois de ela conferir que os 3 eventos já eram principais): marcados em 22/10 20h54 UTC; os 16
  contatos do painel são todos de 22/10 (instalação, antes da marcação); de 23 a 27/10, zero. Teste headless com envio
  bloqueado: o clique no WhatsApp dispara `contato_whatsapp` (artigo e home). O Orbit lê `keyEvents`, a métrica certa.
- Artigos corrigidos conferidos no site público: textos novos no ar, trechos errados ausentes, 1 meta description e
  FAQPage nos 3. Visual no celular conferido antes de publicar (Playwright).
- Não verificado: efeito no CTR (o Search Console leva de dias a semanas para refletir; conferir em 17/11/2026).

## Decisões e porquês
- Primeiro a correção que vale para todas as páginas (título que cabe no Google, descrição com a resposta); depois,
  com as consultas reais, o ajuste fino das páginas com mais aparições.
- Divórcio, plano de saúde e atestado falso aparecem na posição 30-90: título não resolve, precisa de conteúdo e links.
- H1 e og:title não mudam: o título da aba é para o Google; o H1 e o compartilhamento seguem com o texto da página.

## Pendente
- Publicar o `conversoes.js` novo: a simulação deu 85 páginas, mas o `--aplicar` foi barrado pela trava de segurança.
  Comando na VPS (pasta `deploy/vps`): `docker compose exec -T -e PYTHONPATH=/app api python /tmp/publicar_conversoes.py
  /tmp/conversoes.js 20261027 --aplicar` (os dois arquivos já estão no `/tmp` do container; se ele for recriado, copiar
  de novo) e depois copiar o .tgz do `/tmp` para `/root/orbit-backups/`.
- 17/11/2026: comparar o CTR das 5 páginas principais (ver CONTEXTO_PROJETO.md).
- Dra.: ler os dois artigos reescritos (híbrida e carga horária). Ponto aberto na híbrida: para homem filiado antes da
  Reforma, o INSS pede 20 anos (Decreto 3.048, art. 57 c/c art. 51); o texto diz que há argumento para 15 (art. 188-H).

## Próxima sessão
Ler o painel salvo (`social_metrics`, tipo `google_painel`, coluna `metricas` → `search_console.paginas/consultas`) e
comparar com os números deste relatório. Skill sugerida: `leticia-seo-local`.
