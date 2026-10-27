# Orbit — Contexto Vivo do Projeto

> Este arquivo é a "consciência" do projeto: o que existe, o que está em andamento,
> o que falta. Deve ser atualizado ao final de toda mudança/implementação relevante
> (ver `.claude/skills/contexto-orbit/SKILL.md`). Última atualização: **2026-10-16**
> (6 artigos de atualidade + Stories + LP para empresas + plano até dezembro).

## O que é o Orbit

"The Marketing Operating System" — SaaS de marketing multi-tenant. Tenant 0 (único
cliente real hoje) é a **Advogada Letícia Barros** (Vitória/ES, direito trabalhista/
previdenciário/família). O sistema automatiza: pesquisa de pautas jurídicas → geração
de conteúdo (artigo de blog, carrossel, legenda, stories) via IA → aprovação humana →
agendamento automático → publicação automática (Instagram + blog real) → coleta de
métricas (Instagram, Google Meu Negócio) → e-mail marketing → "cérebro" que aprende
com edições anteriores.

## Stack

- **Backend** (`apps/api`): FastAPI + SQLAlchemy 2.0 async + Alembic + PostgreSQL.
  IA: Gemini 2.5 Flash (`google-genai`, geração de conteúdo) + Groq/Llama 3.3 70B
  (triagem rápida). Playwright renderiza imagens (criativos/capas) server-side.
  APScheduler roda jobs recorrentes in-process.
- **Frontend** (`apps/web`): Next.js 15 App Router, **export estático puro**
  (`output: "export"`, sem servidor Node rodando — é servido como arquivo estático
  via `npx serve`). Tailwind v4 + shadcn/ui. `framer-motion` para animação.
- **Deploy**: **VPS Hostinger** (migrado do Railway em 28/08/2026 — ver
  `deploy/vps/README.md` pro runbook completo). VPS `srv1921337.hstgr.cloud`
  (IP `179.199.128.68`, Ubuntu 24.04), a mesma máquina que já roda o CRM
  jurídico da Letícia (Node em `/home/crma`, porta 3001, MySQL local) —
  isolados via Docker, sem tocar no que já existia. Código em
  `/home/orbit-src` (git clone deste repo).
  - `db`: container `postgres:16`, volume próprio `vps_orbit_pgdata`.
  - `api`: container buildado de `apps/api/Dockerfile`, só `127.0.0.1:8010`
    (nunca exposto direto), atrás do nginx.
  - `web`: **sem container** — `apps/web` é buildado (`npm run build`, Node já
    presente na VPS pro CRM) e os arquivos estáticos de `out/` são copiados
    pra `/var/www/orbit-web`, servido direto pelo nginx.
  - nginx: dois server blocks novos em `/etc/nginx/sites-available/`
    (`orbit-web`, `orbit-api`), sem tocar no bloco existente do CRM (`crm`).
  - Domínios: `orbit.advogadaleticiabarros.com.br` (painel) e
    `api.orbit.advogadaleticiabarros.com.br` (API) — DNS gerenciado numa
    conta Hostinger **diferente** da conta dona da VPS (confuso à primeira
    vista: painel do domínio ≠ painel da VPS, apesar de ambos serem
    Hostinger).
  - Redeploy: `cd /home/orbit-src && git pull && cd deploy/vps && docker
    compose up -d --build`. Rebuild do web: `cd apps/web && npm run build &&
    cp -r out/* /var/www/orbit-web/`.
  - **Disco da VPS (16/10/2026):** cada `--build` deixa cache de build do Docker.
    Em 16/10 eram 55 GB, e o disco da VPS (que também roda o CRM jurídico)
    chegou a 81%. Foi limpo com `docker builder prune -f` (ficou em 27%).
    - **Prevenção:** o crontab do root roda `docker builder prune -f --filter
      until=168h` todo domingo às 4h (log em `/var/log/docker-builder-prune.log`),
      e o CRM avisa quando o disco passa de 85%.
    - **Depois da limpeza:** o primeiro `--build` refaz o cache e demora uns
      minutos a mais.
    - **Cuidado:** os `.tar` em `/tmp` (capas, reels, `pxv*`, `subir*`) são
      conteúdo copiado para o servidor, não pacotes de atualização. Foram
      mantidos (1,8 GB); só apagar com o ok da Jessica.
  - **Banco começou zerado, não migrado do Railway** — o Postgres do Railway
    (`Postgres-AXnQ`) estava fora do ar na hora da migração (conexão TCP
    abria mas o servidor fechava sem responder ao handshake do Postgres,
    junto com `orbit-api`/`orbit-web` mostrando "Service is offline" no
    painel — o ambiente inteiro do Railway parecia derrubado, possivelmente
    ligado a um "Security patch scheduled — CVE-2026-15741" que apareceu no
    card do Postgres). Decisão explícita da usuária: sem dado de produção
    relevante acumulado (app ainda recente), não valia a pena investigar o
    Railway só pra recuperar o dump — seed rodado do zero
    (`python -m app.seed.seed_leticia`, tenant `leticia-barros`, login
    `leticia@advogadaleticiabarros.com.br`).
  - **Pendência ativa: DNS não propagou** — os registros A criados apontam
    certo pro IP da VPS no painel, mas consultas externas (`dns.google`,
    `cloudflare-dns.com`) continuam voltando um pool de IPs de hospedagem
    compartilhada da Hostinger pra `orbit.advogadaleticiabarros.com.br`
    (TTL 60, IPs diferentes a cada consulta — cheira a algo sobrescrevendo,
    não só demora de propagação) e `NXDOMAIN` pra
    `api.orbit.advogadaleticiabarros.com.br`. Tudo já validado funcionando
    *dentro* da VPS via `curl -H "Host: ..." http://127.0.0.1/` (nginx→api e
    nginx→estático ambos OK) — só falta a internet enxergar o domínio certo.
    Sem isso, o `certbot` (HTTPS) também não roda, porque a validação dele
    depende do domínio resolver pro IP certo. Próximo passo: usuária abrir
    chamado com o suporte da Hostinger (conta do domínio) perguntando por
    que um registro A criado manualmente não sai do ar.
  - **Chaves a rotacionar quando der** (ficaram visíveis numa sessão de
    terminal/chat durante a migração): senha root da VPS (trocar em
    hPanel → VPS → "Redefinir senha"), e as chaves que estavam no `.env`
    antigo do Railway (`JWT_SECRET`, `GEMINI_API_KEY`, `ENCRYPTION_KEY`,
    `GOOGLE_CLIENT_SECRET`, `GROQ_API_KEY`, `META_APP_SECRET`,
    `RESEND_API_KEY`, `RESEND_WEBHOOK_SECRET`, `TAVILY_API_KEY`, senha do
    SFTP do blog) — não é urgente (baixo risco prático), mas fica registrado.
- **Blog público** (site separado, NÃO é o Orbit): `advogadaleticiabarros.com.br/blog/`,
  HTML estático hospedado na Hostinger, publicado via SFTP (host `147.93.38.211`,
  porta `65002`, usuário `u528898188`, caminho
  `/home/u528898188/domains/advogadaleticiabarros.com.br/public_html/blog/`).
  Credenciais salvas em `deploy/vps/.env` na VPS (antes: env vars do serviço
  `orbit-api` no Railway, hoje desativado).
- **Formulários do site principal corrigidos (04/09/2026)**: `index.html` e
  `contato.html` tinham `<form action="https://formspree.io/f/xrerejoa">` —
  nunca chegavam no CRM, e quando o Formspree falhava o lead se perdia sem
  nenhuma cópia. Os dois usam o mesmo `js/pages.js` compartilhado; trocado
  o `action` do Formspree por um `fetch()` direto pro
  `POST https://crm.advogadaleticiabarros.com.br/api/public/lead` (mesmo
  endpoint que as landing pages em `lp/` já usavam corretamente — CORS já
  liberado lá pra esse domínio). Publicado via SFTP (mesmas credenciais do
  blog acima, caminho `public_html/` em vez de `public_html/blog/`).
  Backups dos 3 arquivos originais ficaram só na sessão que fez a correção,
  não versionados aqui — se precisar reverter, puxar de novo via SFTP e
  comparar com o histórico do painel da Hostinger, se houver.

## O que está pronto e em produção

### Backend — módulos completos
- **Auth**: login, troca de senha, JWT.
- **Pautas**: Radar Jurídico automático diário (web search, ver seção própria) + geração manual, com IA.
- **Content**: geração de 4 tipos de peça por pauta (artigo, carrossel, legenda,
  stories) via Gemini, com "lições de edições anteriores" injetadas no prompt
  (o "cérebro" — `app/services/cerebro.py` / `MarketingMemory`).
- **Aprovação → Agendamento automático**: aprovar uma peça cria um `ScheduledPost`
  na próxima vaga livre do playbook (11:00/17:00, começando amanhã) — 
  `app/services/agenda.py`.
- **Publicador de Instagram**: hourly job publica carrosséis aprovados e agendados
  via Graph API (só `formato="carrossel"` — legenda/stories ainda não têm publicador
  próprio, ver Pendências). Conexão via OAuth **ou** token manual de System User
  (OAuth quebrado por exigir Business Verification do Meta sem atalho de dev-mode).
- **Publicador de Blog** (novo, 22/07): hourly job publica artigos aprovados e
  agendados no blog real via SFTP — gera HTML fiel ao design do site, capa simples
  dourado/preto (Playwright), atualiza `index.html` (2 grades) e `sitemap.xml` de
  forma idempotente. `app/services/blog_publisher.py` + `blog_slug.py` +
  `blog_index_editor.py` + `render_artigo_blog.py` +
  `app/integrations/publish/sftp_client.py`.
- **Instagram**: métricas diárias (seguidores, alcance), conexão OAuth + manual.
- **Google Meu Negócio**: métricas diárias (buscas, chamadas, rotas, visualizações),
  avaliações (listar + responder), triagem de urgência via Groq.
  **API aprovada pelo Google em 22/10/2026** (projeto Cloud 462973861302, cota 300/min).
  Na mesma data: avaliações passaram para a API v4 (`mybusiness.googleapis.com/v4/accounts/{a}/locations/{l}/reviews`;
  a v1 Business Information não tem avaliações), métricas passaram a enviar período completo (últimos 30 dias até
  ontem; antes só mandava o ano e o Google recusava) e "visualizações" = impressões no Maps (antes ficava sempre 0).
  `.env` da VPS já tem `GOOGLE_CLIENT_ID/SECRET` e `GOOGLE_REDIRECT_URI` de produção. Conectado em 22/10/2026
  (perfil `locations/12522032530123494694`, conta `accounts/107896560314349568974`).
- **Tela "Google e site" (`/presenca`, 22/10/2026)**: substitui a antiga tela Avaliações (que redireciona). Abas
  Resumo, Melhorias, Perfil, Avaliações, Posts, Buscas, Site e IAs. Backend em módulos fundos:
  `integrations/social/google_api.py` (HTTP + erros classificados: api_desativada/reconectar/sem_acesso),
  `services/presenca_google.py` (`coletar_painel`: cada seção falha sozinha), `services/checagem_site.py`
  (lê o site por **SFTP**: a hospedagem tem anti-robô que barra Python/httpx, mas deixa GPTBot/ClaudeBot/Googlebot
  passarem), `services/diagnostico_presenca.py` (regras puras → melhorias com `chave` estável; status em
  `recomendacoes_status`), `services/gestao_google.py` (escritas: post, resposta, perfil, foto, botão, sitemap;
  tudo passa por `services/conformidade_oab.py`), `services/central_google.py` (token + coleta + jobs).
  Painel salvo em `social_metrics` tipo `google_painel` (diário às 06h UTC junto das métricas, e pelo botão
  "Atualizar agora"). Posts do Google em `google_posts` (rascunho → aprovado → publicado pelo job de 5 em 5 min).
  OAuth pede `business.manage`, `analytics.readonly` e `webmasters` (sitemap reenviado a cada coleta).
  **APIs ativas no Cloud** (projeto 462973861302, "orbit-mkt"): Account Management, Business Information,
  Performance, My Business v4 (avaliações/posts/fotos), Verifications, Place Actions, Notifications, Analytics Data,
  Analytics Admin, Search Console, PageSpeed. Q&A foi descontinuada pelo Google (03/11/2025).
  Respostas a avaliações: IA escreve, ela aprova (sigilo profissional; decisão de 22/10/2026).
- **E-mail marketing**: campanhas com geração IA, captura pública de contatos,
  descadastro com token HMAC, worker de envio com cadência/teto diário/idempotência,
  webhook Resend (bounce/reclamação via Svix).
- **Dashboard**: `GET /dashboard/resumo` agrega tudo pra Visão Geral.
- **Dicas de desempenho**: IA cruza produção/aprovação/edição/e-mail e devolve
  recomendações (`app/services/insights.py`).

### Frontend — 9 telas do grupo `(app)` + login
`visao-geral`, `planejamento`, `aprovacao` (via query `?pautaId=`), `calendario`,
`criativos`, `emails`, `configuracoes`, `avaliacoes`. (`resumo-diario` foi removida
em 08/10/2026: só listava as pautas das últimas 24h, o que a aba "Novas" do
Planejamento já faz; a rota redireciona para `/planejamento`.) Layout comum via `AppShell` (`components/app-shell.tsx`).

**Revolução visual — Fase 1** (concluída e no ar em 22/07/2026):
- 4 temas de cor trocáveis: dourado (default), esmeralda, azul, violeta —
  via `[data-theme]` + `ThemeProvider` (`components/theme-provider.tsx`) +
  `localStorage`. Seletor temporário no rodapé da sidebar
  (`components/theme-switcher.tsx`) — o seletor definitivo vai pra tela de
  Configurações na Fase 2.
- Tipografia: Chakra Petch (display) + Inter (corpo, sem mudança) + JetBrains Mono
  (dados/timestamps) — trocado de Space Grotesk, considerado clichê de "cara de IA".
- Motion: `components/motion/stagger-list.tsx` (entrada em sequência),
  `components/motion/count-up.tsx` (números contando), `app/(app)/template.tsx`
  (transição de rota). Tudo respeita `prefers-reduced-motion`.
- `AmbientGlow` (blob orbital do login) ampliado — pedido explícito da usuária, que
  disse ser a única parte que gostava do visual antigo.
- Aplicado por completo em: `AppShell`, Login, Visão Geral. **As outras 7 telas
  ainda estão no estilo visual antigo** (isso é a Fase 2, ver Pendências).
- Logo novo (22/07): `public/logo/elemento-a.png` (anel orbital 3D dourado,
  fundo preto sólido sem alpha) substituindo o círculo+ponto simples no `AppShell`
  — usa `mix-blend-screen` via CSS pra dissolver o fundo preto contra o fundo escuro
  do app (confirmado com simulação de blend antes de aplicar). **Só funciona sobre
  fundo escuro** — `mix-blend-screen` lava a imagem inteira pra branco sobre fundo
  claro, por isso o Login (agora claro, ver abaixo) usa um mark SVG simples
  (`LogoMark` inline em `app/login/page.tsx`), não esse PNG.
- **Tema claro é agora o padrão de TODO o app (22/07)**, não só o login — a usuária
  pediu explicitamente ("quero o SaaS inteiro mudado com esse tema, faça isso
  agora"). Implementado como um **5º preset no sistema de tokens** já existente
  (`[data-theme="claro"]` em `globals.css`, promovido a default no `ThemeProvider`,
  no script anti-flash do `layout.tsx`, e no fallback do `<html>`) — os 4 temas
  escuros (dourado/esmeralda/azul/violeta) continuam existindo e selecionáveis no
  `ThemeSwitcher` (5 bolinhas agora), só não são mais o default. Como todo
  componente compartilhado (`Card`, `Button`, `Input`, `AppShell`) já consumia os
  tokens CSS (`var(--background)`, `var(--card)`, etc.) em vez de cor fixa, as 9
  telas herdaram o tema claro automaticamente — **não foi necessário reescrever
  cada página individualmente**, só o `globals.css` + provider + switcher.
  Confirmado visualmente (Playwright) em login, visão geral e configurações.
  - O logo do `AppShell` (PNG `elemento-a.png` com `mix-blend-screen`, que só
    funciona sobre fundo escuro — vira invisível/lavado sobre fundo claro) foi
    trocado pelo mesmo mark em SVG do login (`components/logo-mark.tsx`,
    compartilhado). O PNG `public/logo/elemento-a.png` ficou sem uso no momento;
    pode servir pra algo mais no futuro (ex.: favicon, splash) mas hoje não é
    referenciado em nenhum lugar do código.
  - Micromovimento padrão adicionado ao componente `Card` compartilhado
    (`components/ui/card.tsx`): leve elevação + glow na cor do tema ativo no
    hover. Aplica em todas as telas automaticamente, sem editar página por página
    — foi a resposta ao pedido de "inclua micromovimentos, tire a cara de IA" na
    escala de tempo disponível.
  - **`AmbientGlow` (blob orbital) precisou sair de dentro de uma seção com
    `overflow-hidden`** — os anéis externos (até 720px de diâmetro) eram cortados
    numa linha reta na borda da coluna esquerda do login. Corrigido movendo o
    componente pra ser filho direto de `<main>` (cobre as duas colunas, anéis
    sangram livremente atrás do card). **Gotcha a lembrar**: qualquer elemento
    decorativo grande/animado precisa verificar se algum ancestral tem
    `overflow-hidden` menor que a área que ele realmente ocupa.
  - `AmbientGlow` ganhou: 5 "estrelas cadentes" (partículas com rastro, CSS
    keyframes, posições/tempos escalonados) e paralaxe sutil que segue o mouse
    (framer-motion `useSpring`, rastreado via listener em `window` — o overlay
    continua `pointer-events-none` pra nunca bloquear cliques no formulário
    embaixo). Ambos desligados em `prefers-reduced-motion`.
  - Login ainda usa paleta clara **hardcoded** (não os tokens) — foi construído
    antes dessa decisão virar "o app inteiro". As cores foram escolhidas pra bater
    com o tema "claro" recém-criado, mas não são literalmente a mesma fonte; se o
    tema "claro" for recalibrado no futuro, o login precisa ser ajustado à mão
    também (candidato a refactor: migrar o login pra consumir os tokens).
- **Como validei visualmente sem navegador interativo**: usei o Playwright já
  instalado no `apps/api` (Python) pra tirar screenshot real do build estático
  servido localmente (`npx serve out` + `page.goto(...).screenshot(...)`) e ler a
  imagem antes de commitar. Vale usar essa técnica sempre que uma mudança visual for
  significativa — resolve a lacuna de "nenhum agente tem navegador" que apareceu
  repetidamente nas revisões da Fase 1.
- **Sem suíte de testes automatizados no frontend** — verificação é `tsc --noEmit` +
  `npm run build`, complementado (a partir de 22/07) por screenshot real via
  Playwright quando a mudança for visual.

### Radar Jurídico → Jornal do site (28/08/2026)

A advogada já pesquisa/cura um "Radar Jurídico" semanal no ChatGPT (fora do
Orbit, por escolha dela). Em vez de reconstruir essa pesquisa dentro do Orbit,
o material entra via CLI e passa a andar pelo pipeline existente (Pauta →
ContentPiece → Aprovação → Agendamento → SFTP):

- **Import**: `apps/api/scripts/import_radar.py` (`python scripts/import_radar.py
  arquivo.md --titulo "..." --area ... --origem radar_juridico_manchete|
  radar_juridico_satelite`) loga como o owner e chama `POST /pautas` (agora
  aceitando `origem`/`conteudo_bruto`, campos que `criar_pauta_manual` não
  hardcoda mais — ver `app/schemas/pauta.py`, `app/routers/pautas.py`).
  `Pauta.conteudo_bruto` (Text, nullable) é coluna nova
  (`alembic/versions/e7a2c4f6b891_pauta_conteudo_bruto.py`).
- **Geração**: `POST /content/gerar` (`app/routers/content.py`) injeta
  `pauta.conteudo_bruto` (quando existe) em todos os prompts como "material já
  pesquisado — não invente além disso", em vez de deixar a IA repesquisar. Se
  `pauta.origem == "radar_juridico_manchete"`, gera também um `ContentPiece`
  extra `tipo="jornal"` (a edição semanal), além do conjunto padrão
  (artigo/carrossel/legenda/stories). Pautas satélite (`radar_juridico_satelite`)
  geram só o conjunto padrão — viram matéria de blog normal.
- **Agendamento**: `app/services/agenda.py` mapeia `tipo="jornal"` →
  `canal="blog"`, `formato="newsletter"` — dando uso real ao `formato`
  `"newsletter"` que já existia em `FORMATOS` (`calendario.py`) mas nunca era
  produzido por nada.
- **Publicação**: `app/services/blog_publisher.py` ramifica por
  `agendamento.formato`: `"artigo"` segue o caminho de sempre (slug novo por
  artigo); `"newsletter"` cai em `_publicar_jornal`, que sobe sempre para a
  mesma URL fixa `jornal.html` (sobrescreve, não cria slug novo a cada
  edição) via novo template `app/templates/jornal.html` +
  `render_artigo_blog.py::renderizar_jornal_html`. O card no `index.html` do
  blog é inserido uma única vez (idempotente por URL, como já era
  `inserir_card`); o `sitemap.xml` agora atualiza o `<lastmod>` de uma URL já
  existente em vez de só ignorar (`blog_index_editor.py::inserir_sitemap_entry`)
  — necessário porque a URL do Jornal não muda, só o conteúdo.
- **Dois bugs de produção corrigidos no mesmo trabalho** (pré-existentes,
  bloqueavam captação mesmo antes do Jornal existir):
  1. O formulário "Jornal da Semana" (`blog_artigo.html`) e os dois formulários
     de lead dos guias (`lp/guia-gestante-clt.html`,
     `lp/guia-direitos-gestante-trabalhadora.html`) enviavam para
     `crm.advogadaleticiabarros.com.br/api/public/*` — domínio inexistente.
     Corrigidos para `https://orbit-api-production-0029.up.railway.app/public/contacts`
     com o payload real de `ContactCreate` (`tenant_slug: "leticia-barros"`,
     `nome`, `email`, `origem`, `website`). **Efeito colateral aceito**: os
     guias coletavam telefone e uma mensagem com UTM/contexto; `Contact` não
     tem esses campos, então phone/mensagem deixaram de ser persistidos —
     só nome/e-mail/origem. Se telefone for importante para esses leads,
     precisa de campo novo em `Contact` (fora de escopo deste trabalho).
  2. `email_campaigns.py::gerar_rascunho_newsletter` filtrava
     `ContentPiece.tipo == "blog"`, tipo que a geração real nunca produz
     (produz `"artigo"`) — a newsletter semanal por e-mail estava sempre
     vazia mesmo com artigos aprovados. Filtro corrigido para
     `tipo.in_(["artigo", "jornal"])`.
- **Pendência operacional (não é código)**: confirmar no Railway que
  `CORS_ORIGINS` do serviço `orbit-api` inclui a origem real de onde o
  formulário roda no navegador (`https://advogadaleticiabarros.com.br`) —
  sem isso, o `fetch` do formulário corrigido é bloqueado por CORS mesmo com
  o endpoint certo. Não verificado nesta sessão (sem acesso às env vars do
  Railway).
- Rodar `alembic upgrade head` em produção antes do próximo deploy do
  `orbit-api` (nova coluna `pautas.conteudo_bruto`).

### Reels e estático no gerador automático (28/08/2026)

`POST /content/gerar` (`app/routers/content.py`) agora produz **6 peças por
pauta** (era 4): `artigo`, `carrossel`, `legenda`, `stories`, e dois tipos
novos — `reels` (roteiro de Reels/TikTok, estrutura Problema-Solução com
timestamps, regra dos 3 segundos, sugestão de *tom* de áudio de tendência —
nunca nome de música real, sem acesso ao catálogo da plataforma) e `estatico`
(briefing de arte única: conceito visual + texto de overlay + legenda). O
prompt do `carrossel` também foi reescrito pra estrutura Value-Stack (capa
declara quantidade exata de itens, sem slide de enchimento) — isso mudou o
número de slides de fixo em 5 para variável (6-10); `instagram_publisher.py`
já lia `len(slides)` dinamicamente, então nenhuma mudança foi necessária lá.

Mapeamento novo em `agenda.py`: `reels` → canal `instagram`/formato `reels`
(`reels` virou valor novo em `FORMATOS`, `calendario.py`); `estatico` → canal
`instagram`/formato `post` (reaproveita o mesmo bucket de `legenda`).
**Nenhum dos dois tem publicador automático ainda** — só `carrossel` publica
de verdade hoje (`instagram_publisher.py` filtra
`ScheduledPost.formato == "carrossel"` explicitamente); `reels`/`estatico`
ficam agendados como `pronto` e exigem publicação manual, mesmo padrão já
existente pra `legenda`/`stories`.

Isso roda pra **toda pauta**, não só as do Radar — decisão explícita da
usuária ("coloque tudo que dá pra usarmos aqui em produção"), então o custo/
latência de geração por pauta subiu de 4 para 6 chamadas de IA (mais 1 pro
`jornal`, quando aplicável).

Origem do conteúdo dos prompts: skills do plugin `marketing-skills` (ver
próxima seção) — a estrutura de carrossel Value-Stack e o roteiro de vídeo
curto vieram de lá, adaptados à voz/regras OAB do tenant.

### Plugin de skills de marketing instalado (28/08/2026)

`claude plugin install marketing-skills@marketingskills --scope local` — 50
skills de marketing (SEO, copywriting, vídeo, imagem, social/Reels/TikTok,
carrossel, ads, e-mail, etc.), fonte `github.com/coreyhaines31/marketingskills`.
Escopo `local` (`.claude/settings.local.json`, gitignorado) — só disponível
neste repositório, não é global nem versionado. Usado como referência de
conteúdo ao escrever/revisar os prompts do Orbit (ver seção acima), não é
algo que o backend do Orbit chama em runtime — skills são um recurso do
Claude Code, o Orbit gera conteúdo via API do Gemini diretamente, sem relação
com esse sistema de skills.

### Radar Jurídico automático (29/09/2026)

Substitui o ChatGPT rodado à mão e as fontes fixas STF/TST/CNJ (que buscavam
sempre a mesma página → temas repetidos). Módulo profundo
`app/services/radar_juridico.py`: interface `rodar_radar(db, tenant_id,
pesquisador, hoje)`; por dentro lê áreas do `TenantConfig.voz`, manda os
títulos dos últimos 30 dias como "evitar" e **também** filtra depois por
similaridade (`difflib`, ≥0,85, sem acento/pontuação), limita a 8, grava
`conteudo_bruto` = resumo + link, `data_editorial` = hoje. Às **segundas** o
1º achado relevante vira `radar_juridico_manchete` (alimenta o Jornal
semanal); o resto é `radar_juridico_satelite`.

- **Seam `Pesquisador`**, dois adapters em `app/integrations/radar/`:
  `OpenAIPesquisador` (Responses API + tool `web_search`, modelo em
  `OPENAI_RADAR_MODEL`, default `gpt-4.1-mini`) — preferido quando há
  `OPENAI_API_KEY`; `TavilyGeminiPesquisador` (Tavily `topic=news`, 7 dias,
  1 consulta por área + 1 geral de tribunais superiores → Gemini seleciona)
  — reserva com chaves já existentes. `criar_pesquisador()` escolhe; `None`
  = radar desligado (job loga aviso, `/pautas/buscar` responde 503).
- **Agendador**: `job_radar_juridico` diário 10:40 UTC (07:40 Brasília).
- **`POST /pautas/buscar`** agora roda o mesmo radar na hora.
  `app/integrations/sources/` (STF/TST/CNJ) removido.
- **Bug corrigido**: `pautas.origem` era `String(20)` e as origens do radar
  têm 23 chars — o Postgres rejeitaria (SQLite dos testes não valida).
  Migração `f1b3d5a7c9e2_pauta_origem_40.py`.
- `scripts/import_radar.py` continua existindo para importar texto manual.

### Ciclo editorial de 2 dias + publicador de imagem única (08/10/2026)

Estratégia aprovada pela usuária e documentada no doc "Estratégia Editorial
Orbit" (https://claude.ai/code/artifact/f49e795f-5a37-4d7a-a6f7-c31235e86e5d),
com o raio-X real do Instagram (309 posts via Graph API): Reels alcançam ~4x
o carrossel, 0 salvamentos/30 dias, +15 seguidores/30 dias, 73% mulheres,
74% ES. Fase 1 da refatoração implementada:

- **Instagram conectado** (08/10) com token de System User que não expira
  (app "Orbit Leticia Barros"). Escopos: pages_show_list, pages_read_engagement,
  business_management, instagram_basic/content_publish/manage_insights/
  manage_comments/manage_messages/manage_contents. **Faltam** read_insights,
  pages_read_user_content, pages_manage_posts, ads_read, leads_retrieval
  (Facebook e anúncios) — dependem de adicionar produtos ao app da Meta.
- **`app/services/midia_instagram.py`** (módulo profundo): `montar_midia(piece,
  ...) -> Midia(imagens, legenda)` transforma carrossel, frase, pergunta e
  estático em imagens + legenda; usa `corpo.imagem`/`corpo.imagens` (arte
  enviada à mão) quando existe, senão renderiza. Renderizador injetável
  (`RenderizadorPlaywright` em produção, `tests/fakes.py` nos testes).
  `publicavel(tipo)` filtra o que tem imagem.
- **Publicador** (`instagram_publisher.py`) agora publica `formato in
  (carrossel, post)` cujo tipo é publicável: 1 imagem → `publicar_imagem_unica`,
  várias → carrossel. **Bug corrigido**: carrossel saía sem legenda (caption
  não era enviada ao container pai). Peça sem texto de imagem
  (`PecaSemConteudo`) vai direto pra `erro`, sem gastar tentativas.
- **Gerador**: 8 peças por pauta (+`frase`, +`pergunta`); carrossel agora pede
  `legenda` no JSON. Card novo `templates/pergunta_card.html` +
  `render_criativo.renderizar_pergunta`.
- **Agenda** (`agenda.py`, regra de 16/10/2026, substitui o ciclo de 2 dias): **1 publicação por dia no
  Instagram**. Peça aprovada vai para o primeiro dia sem post do Instagram (Stories não contam); em dia de Reels,
  só o Reels. Horários pelo alcance real do perfil em 12 meses: Reels 21h (melhor hora, 196 contas), feed 14h
  (seg a sex) e 11h (sáb e dom); 12h e manhãs eram fracos. `corpo.programacao` continua mandando.
  Artigo/jornal/stories seguem o playbook (11h/17h).
- **Próximas fases** (no doc): 2 = arte com foto + calendário montado sozinho
  pelo Radar/rodízio de áreas; 3 = métricas por post + ranking + relatório
  semanal; 4 = ajuste automático de horários/formatos, Reels, Facebook.
- **Deployado em 08/10/2026** (commit 3bb9fc7), junto com o Radar automático
  e a análise do Instagram. A VPS estava travada em 963611a porque o
  `docker-compose.yml` tinha um volume `orbit_media:/app/media` adicionado à
  mão (bloqueava o `git pull`); agora está no repositório.
- **Acesso do Claude à VPS**: chave dedicada `~/.ssh/orbit_vps` (máquina da
  usuária) autorizada em `/root/.ssh/authorized_keys` (comentário
  `claude-orbit-deploy`), com regra de permissão no Claude Code
  `Bash(ssh -i ~/.ssh/orbit_vps root@179.199.128.68:*)`. Deploy = backup
  (`/root/orbit-backups/`), `git pull --ff-only`, `docker compose up -d
  --build api` (roda alembic), build do web e `cp -r out/*
  /var/www/orbit-web/`.

### Tela Crescimento = análise automática do Instagram (08/10/2026)

A tela `/crescimento` antiga dependia de prints enviados à mão (vivia vazia).
Foi reescrita como painel de análise alimentado sozinho pela Graph API:

- **Coleta** (`app/services/coleta_instagram.py`, `coletar_instagram(db,
  tenant_id=None, criar_api=...)`): grava/atualiza cada publicação em
  `instagram_posts` (modelo `InstagramPost`, migração `a3c5e7f9b1d2`) com
  alcance, visualizações, curtidas, comentários, compartilhamentos,
  salvamentos, interações, seguidores ganhos e visitas ao perfil; stories
  ficam de fora. Guarda o retrato da conta (perfil, alcance diário 90 dias,
  novos seguidores 30 dias, totais 30 dias, demografia) em
  `SocialMetric(tipo="ig_raio_x")`. Roda no `job_metricas_fontes_externas`
  (06h UTC) e sob demanda pelo botão "Atualizar dados".
- **API Meta** (`InstagramAPI.listar_publicacoes` com paginação + insights
  por post em paralelo, limite 8; `buscar_raio_x`). Insight recusado vira {}
  sem derrubar a coleta.
- **Análise** (`app/services/analise_instagram.py`): `analisar(posts, raio_x,
  hoje)` é pura e devolve cada seção com dados + `explicacao` em português
  (formatos, áreas, horário e dia em horário de Brasília, volume × alcance
  por mês, ranking top 10 em 4 critérios, público) e `recomendacoes`.
  "Típico" = mediana. Área do post = `classificar_area(legenda)` por
  contagem de palavras-chave (empate: Previdenciário > Família > Consumidor
  > Trabalhista; sem palavra = "Institucional").
- **Rotas**: `GET /analise/instagram`, `POST /analise/instagram/atualizar`.
- **Front** (`app/(app)/crescimento/page.tsx` + `_components/`): diagnóstico
  no topo, 8 números do mês com explicação, cada gráfico com o painel "O que
  isso quer dizer"; gráficos SVG feitos à mão (linha com cursor, barras,
  colunas, participação). Cores dos formatos `--fmt-reels/carrossel/imagem`
  em `globals.css`, validadas com o script da skill `dataviz` no claro e no
  escuro. Conferido em screenshot real (desktop 1440 e celular 390).
- Facebook: card explicando que entra quando a permissão de leitura da
  Página for liberada.

### Jornalista do Orbit + Planejamento como redação (08/10/2026)

O Radar Jurídico (`radar_juridico.py`, `integrations/radar/`) foi **removido** e
substituído pelo Jornalista (`app/services/jornalista.py`, interface
`apurar(db, tenant_id, buscador, redator, hoje, foco=None)`):

- **Fontes** (`app/integrations/noticias/`, seam `Buscador`): Google Notícias
  RSS (sem chave), Tavily (topic=news) e pesquisa web da OpenAI (só quando
  houver `OPENAI_API_KEY`; só ficam links que a busca citou em
  `url_citation`; até 8 buscas por ronda). `BuscadorMultiplo` junta tudo.
- **Método** (inspirado nas skills de jornalismo jamditis/claude-skills-journalism:
  story-pitch, source-verification, editorial-workflow): coleta → agrupa matérias
  do mesmo fato (Jaccard de palavras ≥ 0,5) → Gemini redige citando NÚMEROS de
  grupo (links nunca vêm da IA; aceita a chave traduzida "groups") → selo por
  regra fixa pelo DOMÍNIO (`.jus/.gov/.leg/.mp.br` = oficial; 2+ domínios =
  confirmada; senão fonte única) → dedup 30 dias → máx. 8 (5 num pedido).
  Segunda-feira: a mais relevante vira `jornalista_manchete` (Jornal semanal).
- `Pauta` ganhou `apuracao` (JSON: gancho, fatos, o_que_muda, prazo, local_es,
  formatos {pergunta, frase, carrossel}, fontes, verificacao, pedido),
  `relevancia`, `urgencia` (migração `b4d6f8a0c2e3`). Etapas: sugerida →
  aprovada → em_producao (automático ao gerar conteúdo) → publicada; ou
  guardada / descartada (`PATCH /pautas/{id}`).
- Rotas: `POST /pautas/buscar` (ronda), `POST /pautas/jornalista {foco}`.
  Agendador: `job_jornalista` 10:40 UTC.
- Primeira ronda real (08/10): 7 pautas, fontes reais (Agência Brasil, Folha,
  TST, TJSC…). Ajustes feitos após ler o resultado: manchete sem "!",
  notas distribuídas, mesmo veículo conta uma vez.
- Tela `/planejamento` reescrita: painel do Jornalista (pedido por assunto +
  ronda agora), abas por etapa, filtro por área, lista com selo/urgência/
  relevância e apuração completa ao lado (no celular, abaixo do card).

### Painel de chaves de IA (08/10/2026)

`Configurações → Chaves de IA`: a usuária cola a chave, o Orbit testa no
serviço (OpenAI: `GET /v1/models`) e guarda criptografada com Fernet em
`chaves_api` (migração `c5e7a9b1d3f4`); a tela só mostra os 4 últimos
caracteres. `app/services/chaves_api.py` (`salvar_chave`, `status_chaves`,
`obter_chave` com fallback para a variável de ambiente, `remover_chave`) e
rotas `GET/PUT/DELETE /chaves/{provedor}`. O Jornalista recebe a chave via
`criar_jornalista(openai_key=...)` (rota e agendador leem com `obter_chave`).
A chave da OpenAI atual foi colocada pela usuária no `.env` da VPS em 08/10
(veio colada 3x pelo `read -s`; corrigida para uma cópia, validada: 200).

### IA com reserva: Gemini + OpenAI (08/10/2026)

**A chave do Gemini é do plano GRATUITO**: 20 pedidos/dia no gemini-2.5-flash
(descoberto com um 429 RESOURCE_EXHAUSTED). Cada geração de pauta gasta 8.
`app/integrations/ai/fabrica.py::criar_ia(openai_key)` agora é o ponto único:
Gemini principal + `OpenAIClient` (Chat Completions, gpt-4.1-mini) de reserva
automática (`IAComReserva`: qualquer falha da principal → mesma pergunta na
reserva, com log de aviso). Usado por content, dashboard, email, scheduler e
Jornalista. A pesquisa web da OpenAI entra só em pedidos sob encomenda e
descarta matéria antiga pela data (na ronda diária trazia notícias de meses
atrás); resposta pedida em texto com citações (JSON não traz `url_citation`).
Pendência: decidir se vale ativar o faturamento do Gemini.

### Primeira programação automática (08/10/2026)

Peças prontas do Editorial (Desktop\Editorial 28/09–04/10) + artes novas
(frases de pet/abandono/CLT, pergunta CLT no padrão creme da usuária via
`_saida_programacao_0810/_gerar_pergunta_clt.py`) + 3 frases de violência de
gênero como estáticos de respiro. Tudo em JPEG (a Graph API só aceita JPEG)
no volume `/app/media`, programado por `_saida_programacao_0810/_programar.py`
(pauta por tema, peça aprovada com `imagem`/`imagens` + `legenda`, agendamento
no ciclo). 13 posts Instagram 08–14/10 + artigos de pet (09/10 10h) e abandono
afetivo (11/10 10h) no blog com capa pronta (`corpo.capa_arquivo` + `slug`).
Ajustes para a 1ª publicação automática: `InstagramAPI._aguardar` espera o
container ficar FINISHED antes de `media_publish`; `job_envios` a cada 5 min.
Teste seco: container criado com `pergunta-pet.jpg` → FINISHED (sem publicar).

### Manual de Conteúdo para Instagram e Facebook (08/10/2026)

- `docs/MANUAL_CONTEUDO_REDES.md` = regras obrigatórias de toda peça de rede social
  (OAB Prov. 205/2021, políticas da Meta, specs, design system aplicado, copy,
  checklist). Referenciado no `CLAUDE.md` e nas skills `leticia-*`/`fabrica-de-conteudo`.
  Versão comentada com fontes: https://claude.ai/code/artifact/3927cd5d-9428-4056-a928-2c779b46ea2b
- Prompt `legenda` pedia 7 hashtags; o Instagram limita a 5 desde 18/12/2025. Corrigido
  e travado por `test_nenhum_prompt_pede_mais_de_5_hashtags`.
- **Pendente**: templates de render ainda geram 1080×1350; padrão novo do manual é
  1080×1440 (grid 3:4) com conteúdo crítico na faixa central 1350. Subtítulo da marca
  em `carrossel_slide.html` está em 12 px (mínimo do manual: 22 px).
- **Primeiro comentário automático**: prompts de carrossel/estático/frase/pergunta
  pedem `primeiro_comentario` (constante `PRIMEIRO_COMENTARIO` em `content.py`);
  `Midia.primeiro_comentario` (`midia_instagram.py`); o publicador chama
  `InstagramAPI.comentar(post_id, texto)` depois de publicar, e falha ali só loga
  (post já está no ar). Editável no Editorial (sheet da peça). Peças geradas antes
  disso não têm o campo e publicam sem comentário. Facebook ainda manual (falta
  `pages_manage_engagement`). Ainda não validado contra a Meta em produção: conferir
  no log do primeiro post publicado se o comentário entrou.

### Editorial reflete o que foi postado (08/10/2026)

- Publicadores (Instagram e blog) agora marcam a `ContentPiece` como `publicado`
  junto com o agendamento: o contador "x/y" do Editorial (`dia-list.tsx` conta
  `status == "publicado"`) passa a refletir o que foi ao ar.
- Por isso newsletter semanal (`email_campaigns.py`) e insights aceitam
  `aprovado` OU `publicado`; filtrar só `aprovado` faria o artigo publicado sumir
  da newsletter.
- Prompt `pergunta` não termina mais com "Me conta nos comentários" (CED art. 42 I);
  travado por teste.
- Editorial agrupa por `Pauta.data_editorial` = data em que vai ao ar. A
  programação de 08/10 criou pautas-cópia sem data; corrigido: assédio (pergunta)
  em 08/10, pet em 09/10 (com o story), duplicatas em rascunho das pautas de 28/09
  e 30/09 removidas (backup `pre-editorial-datas-*` em /root/orbit-backups).

### Produção 15/10 a 02/11/2026 (rascunho, aguardando aprovação)

- 39 posts (10 dias de tema + 9 "Mito ou Lei" nos dias de respiro) em
  `apps/api/_saida_producao_1510/`: `conteudo.py` (textos, fatos conferidos),
  `produzir.py` (artes: carrossel capa/itens/final, pergunta creme sem selo de
  verificado e com logo no avatar, frase, Mito ou Lei; JPEG 1080×1350), `plano.json`,
  `subir_rascunhos.py` (roda no container). Peças `rascunho` com
  `corpo.programacao = {data, hora}`; cada dia numa pauta com `data_editorial` = data
  de postagem. **Nada agendado**: após aprovação da Letícia (doc
  https://claude.ai/code/artifact/2f39add3-ba5e-4eb5-bc0e-47fae877428d, coluna
  Aprovação), criar `ScheduledPost` a partir de `corpo.programacao` e marcar `aprovado`.
- Pautas do Jornalista fundidas (04d86f1b, 2dede71c, dccbb606) ficaram `guardada`,
  sem data. Programação de 10–14/10 ajustada (5 hashtags, primeiro comentário, CTA).
- 08/10 19h: primeira publicação automática real + primeiro comentário confirmados
  via Graph API (post 18095711492653597).
- `produzir.py` usa `indice_fotos.json` (número da foto → arquivo do BANCO IMAGENS).

### Radar de referências do Instagram (08/10/2026)

- `app/services/radar_referencias.py`: `vigiar(db, tenant_id, leitor, perfis, agora)`.
  Lê perfis públicos via business discovery (`InstagramAPI.posts_de_perfil_publico`),
  e post dos últimos 3 dias com engajamento ≥ 2× a mediana do perfil vira pauta
  `sugerida` (origem `referencia_instagram`, fonte `@perfil`, sem data editorial,
  link no `apuracao`, nunca repete). Máx. 3 por perfil. Job `job_referencias` 07h10.
- Perfis em `TenantConfig.canais["referencias_instagram"]` (hoje: diariojustica,
  atualizacao_trabalhista, trtespiritosanto). Só funciona com conta comercial/criador.
- Capas de carrossel v2 (`_saida_producao_1510/capa_v2.py`, recorte com rembg
  `u2net_human_seg`) e cartão de pergunta refinado (`pergunta_refinada.py`).

### Pergunta v6 = padrão oficial (09/10/2026)

- Aprovado pela Letícia: foto inteira com um objeto do tema (sem recorte), caixa de vidro
  centralizada, destaque em itálico dourado. Gerador oficial reescrito
  (`templates/pergunta_card.html`, `render_criativo.html_pergunta/renderizar_pergunta`
  com `foto_path`, `area`, `foto_posicao`, `brilho`, `desce`); `_fotografar` agora espera
  fontes carregarem. 13 perguntas agendadas às 12h de 09/10 a 02/11. Resto do lote
  15/10–02/11 continua rascunho por pedido dela. Ver `docs/PASSAGEM_DE_CONTEXTO.md`.

### Mito ou Lei v3 = padrão oficial (09/10/2026)

- Aprovado pela Letícia: selo encaixado no topo do cartão de vidro (afirmação + explicação
  no mesmo cartão), escolhido por sobreviver ao corte 3:4 da grade e pela leitura em linha
  reta. Gerador oficial `templates/mito_card.html` + `render_criativo.html_mito_ou_lei /
  renderizar_mito_ou_lei` (valida veredito MITO/LEI, abrevia referência longa), com testes.
  9 peças agendadas às 19h de 16/10 a 01/11. Ver `docs/PASSAGEM_DE_CONTEXTO.md`.

### Reels: publicação automática e padrão de produção (09/10/2026)

- `InstagramAPI.publicar_reels` (container REELS com video_url, espera FINISHED, publica);
  `montar_midia` aceita `tipo="reels"` com `corpo.video`; o publicador busca `formato="reels"`.
  Vídeo: 1080×1920, H.264, AAC 128 kbps (192 é recusado). Teste real sem publicar: container
  da série gestante FINISHED em ~30 s.
- A API não liga o rótulo "Informações de IA": a legenda leva "🔊 Narração produzida com
  inteligência artificial.".
- Produção: skill `leticia-reels-motion` + motor congelado em `C:\tmp\videos-reels\_padrao-motion`.
  Série gestante agendada: 15, 17 e 19/10 às 20h30.

### Editorial: aprovar ou pedir alteração (09/10/2026)

- Pedido da Letícia ("preciso de um botão de alteração ou aprovação"). No Editorial (celular),
  cada peça tem "Aprovar e agendar" e "Pedir alteração" (`_components/aprovacao-acoes.tsx`).
- Aprovar (`PATCH status=aprovado`) agenda na data/hora de `corpo.programacao` quando existe
  (`agenda._programacao_combinada`); sem ela, segue o ciclo de vagas.
- Pedir alteração grava `corpo.pedido_alteracao {texto, em}`, status `ajuste`, e
  `cancelar_agendamento_pendente` tira do calendário (post já publicado fica). Ao ver
  peças em `ajuste`, o Claude lê o pedido, refaz a peça e devolve para `rascunho`.

### Produção de novembro/2026 em rascunho (09/10/2026)

- Plano `docs/PLANO_CONTEUDO_NOV_2026.md` aprovado e produzido no padrão: 13 dias de tema
  (pergunta v6 12h, frase v2 15h, carrossel v5 Ouro editorial 18h), 15 Mito ou Lei v3 (19h) e
  4 artigos de blog (segundas 9h), todos em rascunho com `corpo.programacao`, nas pautas de
  novembro. Dados: `_saida_producao_1510/conteudo_nov.py` e `artigos_nov.py`. Reels esperam os
  áudios (`docs/REELS_NOTEBOOKLM_NOV_2026.md`).
- "Revisar e aprovar" agora mostra o texto do artigo ("Ler o artigo"), para ela aprovar sem sair
  do Orbit; o aviso dos Reels diz que o Orbit publica sozinho.

### Narração dos Reels com a voz da Letícia (ElevenLabs, 14/10/2026)

- A Letícia já tem a voz clonada no ElevenLabs. `C:\tmp\videos-reels\_padrao-motion\narrar.py` (+ `test_narrar.py`)
  transforma um roteiro (uma parte por Reels, `## Parte N`) em `narracao.wav` + `transcricao.json` no formato do
  Whisper, com o tempo de cada palavra vindo do endpoint `/with-timestamps`. O motor motion consome sem mudança.
- Substitui o NotebookLM como padrão: o texto falado é o nosso roteiro, com fatos conferidos antes; acaba a
  correção de transcrição e a fala truncada. `--checar` avisa números/siglas a escrever por extenso, termos vetados
  pela OAB e duração fora de 20–45 s.
- Boas práticas vindas do OpenMontage (só ideias; o código dele é AGPL e não entra no Orbit): `previous_text`/
  `next_text` entre partes, `seed` fixa, cache por conteúdo (`cache_voz/`, não cobra duas vezes). Chave e voice_id
  em variáveis de ambiente ou `C:\Users\prosy\.elevenlabs-leticia.json` (fora do git). A legenda continua com o
  aviso de narração por IA.
- Atenção: o motor motion vive em `C:\tmp` e não está versionado.

### Atualidades de 15/10/2026, Stories e frente B2B

- 6 artigos (`_saida_producao_1510/artigos_out.py` + `artigos_out_extras.py`), fatos conferidos em fonte primária
  no mesmo dia (docstring lista as fontes): fim da 6x1 (PEC 221/2019 aprovada no Senado em 14/10, ainda sem
  promulgação), licença-paternidade (Lei 15.371/2026), Lei 15.377/2026 + NR-1 (multas suspensas na ADPF 1.316),
  TST Tema 215, pejotização (Tema 1.389), pensão para pais idosos no ES (33.560 processos, CNJ via Tribuna 12/10).
  Formato novo: bloco "Resposta rápida" de 40–60 palavras logo após a abertura (alvo de citação em IA),
  "Atualizado em", seção "Se você é empresa" nos trabalhistas.
- Subidos em rascunho por `subir_out.py` (pautas do dia criadas pelo script; backup
  `/root/orbit-backups/pre-out15-*.sql.gz`): artigos das 10h às 15h, 6 peças `stories` (xxh30, link + passo a passo
  na legenda; o Orbit não publica Stories e o adesivo de link só existe no app) e a frase v2 do Dia dos Professores (10h).
- **Padrão de Story "Leia o artigo no link"** (`producao_out.html_story`): a capa Ouro editorial do carrossel v5
  (`capa_fecho.CSS_OURO`) em 1080×1920, com 250 px livres em cima e embaixo e espaço para o adesivo acima da base.
  O template antigo `story_artigo_no_ar.html` (Playfair) ficou fora do padrão e não é mais usado.
- LP nova `lp/empresas-adequacao-trabalhista-2026.html` (gerador `lp/_gerar_lp_empresas.py`, design da LP
  assessoria-empresarial): **rascunho, ainda não publicada**. Botão "Solicitar contato" (sem "envie o seu caso").
- Plano `docs/PLANO_CRESCIMENTO_OUT_DEZ_2026.md`: pilares 4 (Jornada 2026-2027) e 5 (Empresa em dia, B2B),
  gatilho de 24 h na promulgação da 6x1, LinkedIn, contadores, grupos de SEO novos e metas.
- Pendente: a página de artefato do Perfil da Empresa (posts do Google) não respondeu ao `ArtifactData` nesta
  sessão; imagens e textos dos 6 posts estão em `pecas/google-post-*.jpg` e `pecas/posts_google_out.json`.

### Estúdio de criativos com Reels e decisão (15/10/2026)

- Pedido da Letícia: ver o Reels no Estúdio e dar o veredito ali. `apps/web/lib/pecas.ts` concentra mídia da
  peça (vídeo ou imagens) + aprovar + pedir alteração, usado pelo Estúdio (`/criativos`) e pelo Editorial
  (`aprovacao-acoes.tsx`). Estúdio: Reels no grid e player; botões Aprovar e Pedir ajuste; filtro "Alteração pedida".
  Editorial: player do Reels no visualizador. Sem testes de frontend no projeto (validado por `tsc` + `next build`).
- Pedidos de ajuste chegam ao Claude por verificação periódica na sessão (`apps/api/scripts/pedidos_ajuste.py`,
  cópia em `/root/orbit-tools/` na VPS): lista peças em `ajuste` com o texto do pedido. O agendamento vive só
  na sessão do Claude aberta (some ao fechar; expira em 7 dias). Fora dela, ao começar uma sessão, rodar o script.

### Motor 3D, série Guarda dos filhos e acervo de Reels (15/10/2026)

- **Motor 3D** (`producao/reels/motor3d/`): mundo em miniatura three.js (argila + ouro sobre café), câmera
  contínua por chaves, camada 2D (cabeçalho, capítulos, etiquetas com fio, selos, números em ouro, legenda palavra a
  palavra, fechamento), render quadro a quadro no Chromium com WebGL por software (`--use-angle=swiftshader`),
  verificador da área limpa (`window.checar`). Inspirado num Reels de referência (@explicandodireito.br, 6x1).
  Primeiro roteiro: `reel_6x1.py`, com tempos estimados; **espera a gravação da Letícia**
  (`Desktop\PROJETOS\ecosystemmkt\GRAVAR - Reels fim da 6x1.txt`). Gotcha: em three.js `position` é somente
  leitura (usar `.position.set`, helper `em()`).
- **Série Guarda dos filhos** (pedido de ajuste no acervo 04): 3 Reels com o rosto real dela (gravações 4K de
  15/08/2025 em `Desktop\Leticia conteudos\novos videos\Guarda compartilhada x unilateral`) no motor v2: cenas de
  rosto (pílulas no peito, `dy` para subir o vídeo na tomada longa) + cenas de corte com o vídeo desfocado. Fontes em
  `producao/reels/series/15-guarda-compartilhada/`. No Orbit em rascunho, 21/23/25-10 às 20h30. A versão vertical
  de outubro/2025 desse vídeo tem selo de verificado falso: não usar.
- **Acervo**: Reels 01–11 antigos subidos como rascunho, sem data (`subir_acervo_reels.py`), com aviso para conferir
  se já foram postados.
- **Dia dos Professores**: v3 (sala vista do fundo, quadro com inglês desfocado) após pedido de ajuste.
- Verificação de pedidos de ajuste: só quando a usuária avisar (ela pediu para parar a verificação periódica).

## Série 18: Limbo previdenciário (20/10/2026)

- 2 Reels de cerca de 55 s a partir da gravação `Downloads\IMG_0330.MOV` (tomada única de 3 min 07 s): 1 "O que é
  limbo previdenciário", 2 "Quem paga o salário" (a empresa, pela jurisprudência majoritária). Motor v2 no padrão
  da série 17 (rosto + vídeos do Pexels), sem correção de cor (luz boa), `DY -200` e zoom 1.12 (com 1.22 a testa
  saía cortada).
- Cortados da fala, com aprovação da Jessica: "auxílio-acidente" (nome errado do benefício), "o contrato fica
  suspenso" (tecnicamente errado) e o caso de 10 meses do escritório (OAB). Detalhes em
  `producao/reels/series/18-limbo-previdenciario/montar_falas.py`.
- No Orbit: peças novas em **rascunho, sem data** (`limbo-previdenciario-{1,2}-v1.mp4`). Backup do banco antes:
  `/root/orbit-backups/antes-serie18-2026-10-20.sql.gz`. Mídia pesada em `C:\tmp\videos-reels\18-limbo-previdenciario\`.
- **v2 (mesmo dia, pedido "falas mais limpas, sem pausas e repetições, mais dinâmico; o segundo está travando")**:
  - travamento da v1: a cena "Mas ele não trabalhou" (11,9 s) usava um vídeo do banco de 10 s, e a imagem congelava
    aos 33,6 s. Na v2, `corte()` em `serie_v2.py` recusa cena maior que o clipe.
  - falas: pausas reais medidas com `silencedetect` (-44 dB, ≥ 0,25 s; com -36 dB comia sílabas) e encurtadas para
    0,18 s; repetições cortadas ("fica nesse", "vindo do INSS", "segundo a jurisprudência", "nem, nem", "né?"); 5% mais
    rápida. A ponta de cada trecho encosta na pausa real mais próxima (`encostar`), porque o Whisper erra alguns décimos.
  - Ficaram com 46,5 s e 39,6 s (eram 55 s e 54 s). O vídeo do banco "empresa" (o mesmo da série 17) foi trocado
    por "chefe" (Yan Krukau).
  - No Orbit: peças novas `versao=2` nas mesmas pautas (`limbo-previdenciario-{1,2}-v2.mp4`); a v1 continua lá.
    Backup: `/root/orbit-backups/antes-serie18-v2-2026-10-20.sql.gz`.
- Pendente: ela aprovar (a v2) e escolher os dias (21h, dia sem outro post; a parte 2 logo depois da 1).

## Reels premium: ferramentas e motor (21/10/2026)

- Passo 1 da skill `leticia-reels-premium` feito em `producao/reels/motor/` (39 testes: `py -m pytest`):
  - `fala.py` (`transcrever` / `montar <falas.py>`): pontas na pausa real, pausas internas a 0,18 s, fusão de 20 ms,
    pontas alinhadas aos quadros, retranscrição de cada trecho. Decisões não óbvias:
    - pausa partida por estalo (dois silêncios curtos e um estalo no meio) só é cortada se, medida a -40 dB, for ≥ 60%
      silêncio a -44 dB. Juntar silêncios "próximos" comia a consoante dentro da palavra ("atestado" virou "ato está");
    - aviso de texto só vale se aparecer no trecho isolado **e** na fala inteira (o Whisper chuta em trecho < 1 s);
      troca ou palavra comida onde o corte só tirou silêncio (pico < -38 dB) vira "nota", não reprova;
    - Whisper medium precisa de ~3 GB livres; sem memória, cai para o small com AVISO.
  - `conferir.py <mp4> [cfg]`: congelamento (fora do fechamento), volume, formato, cena maior que o clipe, folha de 10 quadros.
  - Motor: sem trilha (1 entrega), mix cravado em -14 LUFS por ganho + limitador (o loudnorm linear parava em -15
    por causa dos picos de consoante da voz), CBR 11 Mbps (taxa média dava 4 a 9 Mbps em motion graphics, nem 2
    passadas resolvem), 3-4 variações por efeito sorteadas com semente fixa, efeitos abaixados sob a voz
    (sidechain), punch-in alternado (1,0/1,12, centrado no rosto) nas emendas das cenas com
    `"rosto": True`, `fim_da_fala()` (a última cena de rosto congelava antes do fechamento na v2), e `codificar`
    recusa sobrescrever.
- Validação com a série 18 (`IMG_0330.MOV`, mesmos trechos da v2): "fala ok" nos dois; `conferir.py` sem avisos
  (45,0 s e 37,9 s; 11,0 Mbps; -14,1 e -14,2 LUFS; pico -1,9 dBTP). A ferramenta achou defeitos que a v2 tinha:
  4 pausas de 0,27 a 0,49 s por Reel e a cena final congelada. Arquivos: `series/18-limbo-previdenciario/
  falas_premium.py` e `serie_premium.py`; vídeos em `C:\tmp\videos-reels\18-limbo-previdenciario\validacao-premium\`
  (`limbo-previdenciario-premium-c-{1,2}.mp4` são os bons; `-` e `-b-` ficaram como registro). **Nada foi ao Orbit.**
- Retorno dela sobre a validação (21/10): chiado de fundo abafando a voz (era a ambiência: -34 dB constante, no
  nível da fala baixa; **tirada do motor**, teste garante pausa < -55 dB); faltou 3D e ficou menos dinâmico (a
  validação usou o roteiro de cenas da v2, sem 3D; nos próximos, 3D obrigatório em 1 ou 2 momentos via `motor3d`);
  e **uma versão só por vídeo** (sem versões de teste).
- Terceiro retorno (21/10): a amostra da voz tratada ficou "péssima, estragou o áudio; é melhor não mexer e manter o
  original". **Cadeia de tratamento removida**: a voz entra como foi gravada, só com ganho (pico a -3 dBTP); final
  a -14 LUFS só com ganho + limitador que corta no máximo 2 dB (escolha dela: som intacto > volume). O IMG_0330, com
  picos fortes, sai a -18,2 LUFS. `conferir.py` avisa só acima de -13 ou abaixo de -20. Amostras apagadas.
- Segundo retorno (21/10, substituído pelo terceiro): "vídeo amador, baixo, voz abafada". Medido: o IMG_0330 vem sem agudos (AAC mono 84 kbps:
  4-8 kHz a -46 dB; voz limpa fica perto de -20) e o vídeo de 15/08/2025 tem fundo constante a -40 dB. Voz refeita
  em `cadeia_voz` (analisa a gravação; `aexciter` só quando abafada; RNNoise inteiro + afftdn; corte 250/500 Hz;
  presença 3 kHz; de-esser; compressor; portão): fala 59 dB (IMG_0330) e 62 dB (vídeo novo) acima do fundo. Voz
  nivelada a -14 LUFS antes da mistura (sem isso os efeitos passaram por cima da voz). Volume final **-11 LUFS**
  (compressão suave + limitador a 192 kHz; sai -11,5 a -11,7). Amostras antes/depois para ela ouvir em
  `C:\tmp\videos-reels\amostras-som\`.
- Pixabay (efeitos sonoros): a página abre pela leitura web, mas download por linha de comando dá 403 e a API não
  tem áudio. Para usar, ela baixa à mão e conferimos a licença antes.

## Site da Letícia: descoberta por buscadores e IAs (20/10/2026)

- Pedido dela depois de perguntar sobre "prompt injection invisível" (resposta: não; texto oculto é spam no Google
  e risco na OAB). O caminho legítimo foi feito:
  - Home: removido `aggregateRating` 5,0/30 do JSON-LD (nota declarada sem avaliações visíveis na página; viola
    diretriz do Google). A entidade do escritório ganhou `@id` `https://advogadaleticiabarros.com.br/#escritorio`.
  - `sobre.html`: `ProfilePage` + `Person` (Letícia Elias Barros, OAB/ES 39.948, sócia da Santiago Prado & Barros).
  - `areas/*.html` (7): `Service` (provider = `#escritorio`) + `FAQPage` das `<details>` visíveis + `BreadcrumbList`;
    `direito-familia` e `direito-previdenciario` ganharam canonical.
  - `llms.txt` refeito: 66 links sem repetição (páginas, 7 áreas, 6 guias/LPs, 47 artigos por área com resumo).
  - **IndexNow** (Bing e outros; o ChatGPT busca pelo índice do Bing): chave em `/6bc7d2f33225bd1d3c4af27b891f2ac6.txt`
    (pública por definição, constante em `app/services/site_descoberta.py`). Em 20/10 as 68 URLs do sitemap + llms.txt
    foram enviadas (`api.indexnow.org` respondeu 202).
- **Daqui pra frente é automático:** `blog_publisher._publicar_artigo` sobe o `llms.txt` regerado do índice do blog
  (`gerar_llms_txt`) e chama `avisar_indexnow([url_artigo, blog/])`; falha de rede só vira log.
- Backup da raiz do site antes da mudança: `/root/orbit-backups/site-leticia-raiz-2026-10-20.tgz` na VPS.
- **Pendente com ela:** criar a conta no Bing Webmaster Tools e adicionar o site (o jeito mais rápido é "Importar do
  Google Search Console", que já está verificado). Se o Bing pedir arquivo `BingSiteAuth.xml` ou meta `msvalidate.01`,
  ela manda o código e a gente sobe na raiz.

## LinkedIn B2B, Reels 2 por semana e TikTok (23/10/2026)

- **Tela Desempenho** (`/desempenho`, commit `c5d951e`): todos os canais numa tela (site/GA4, Search Console, Perfil
  da Empresa, Instagram, LinkedIn, TikTok, blog), com comparação com o mês anterior, listas (páginas, buscas, posts)
  e avisos. Módulo `services/desempenho.py`: `consolidar(fontes, hoje)` é pura; `montar_desempenho` só lê o banco
  (as coletas diárias das 06h). "Atualizar agora" chama `/presenca/atualizar` e `/analise/instagram/atualizar`.

- **LinkedIn** (estratégia em `docs/ESTRATEGIA_LINKEDIN_PME.md`, até 31/01/2027): perfil da Dra. conectado (token
  de 60 dias, vence 22/12/2026; o Orbit avisa 7 dias antes). Tela `/linkedin`: card **Resultados** (visitas e
  contatos vindos do LinkedIn, do GA4 em `painel.analytics.linkedin`, porque a API do LinkedIn não dá números),
  edição de post na fila, "Aprovar todos os rascunhos" e fila em ordem de data. Links do site saem com UTM
  (`link_com_utm`). Texto aceita menção `@[Nome](urn:li:organization:ID)`. **39 posts aprovados** (27/10 a
  28/01; terça, quarta e quinta às 8h). Os 4 que levam à LP de empresas esperam a LP ir ao ar.
- **Página da empresa** criada (0 seguidores). Capa em `producao/linkedin/capa-pagina-linkedin@2x.png`. Publicar na
  página e ler números depende da Community Management API (app separado, análise do LinkedIn).
- **LP de empresas** regerada (EC 141 promulgada em 16/10, seção e formulário do Checklist 2027) e **Checklist 2027**
  (`lp/checklist-2027-empresas.pdf`, gerador `lp/_gerar_pdf_checklist_empresas.py`): esperando a aprovação para
  subir (LP em `lp/`, PDF em `assets/downloads/`).
- **Reels: 2 por semana, terça e sexta 21h** (`DIAS_REELS` em `agenda.py`; feed nos outros cinco dias; Reels com
  data combinada fora desses dias vai para a próxima terça ou sexta). Calendário existente remarcado em 23/10
  (log em `/root/orbit-backups/remarcacao_reels_2026-10-23.json` na VPS). Em dezembro alguns dias de Reels também
  têm o carrossel das 14h já marcado (datas temáticas não foram mexidas).
- **TikTok (commit `0e93966`, no ar):** card na Visão Geral (Conectar), tela `/tiktok`, job `job_tiktok` a cada 10 min.
  Cada Reels do Instagram vai uma vez ao TikTok depois do horário do Instagram, a partir do dia da conexão
  (`conectado_em`), com envio do arquivo em partes (FILE_UPLOAD; não precisa verificar domínio). Com o app auditado
  pela TikTok sai direto e público; sem auditoria a TikTok só aceitaria privado, então o Orbit manda para a **caixa
  de rascunhos** do TikTok (`status="no_rascunho"`): a pessoa publica pelo app colando a legenda que a tela
  `/tiktok` mostra e clica "Já publiquei". Escopos: `user.info.basic,video.upload,video.publish`. Redirect que
  precisa estar no app da TikTok: `https://api.orbit.advogadaleticiabarros.com.br/integracoes/tiktok/callback`.
- **TikTok com agenda própria (23/10/2026, pedido "editorial próprio, horários de maior fluxo, viralização"):**
  estratégia em `docs/ESTRATEGIA_TIKTOK.md` (algoritmo, grade, música, formatos, metas, revisão em 20/11).
  `services/tiktok.py` agora tem **fila própria**: `publicar_fila_tiktok` (job a cada 10 min) põe cada Reels aprovado
  com agendamento ativo do Instagram (e peças `tipo="tiktok"`, para cortes só do TikTok) na próxima vaga livre de
  `GRADE_TIKTOK` (dom 10h, seg 18h, ter 12h, qua 20h, qui 18h), na ordem das datas do Instagram, e envia quando o
  horário do TikTok chega. Vaga em `corpo["tiktok"]` (`data`, `horario`; `fora=True` tira do TikTok).
  `PUT /tiktok/{id}/agenda` remarca/tira; a tela `/tiktok` mostra a fila. A regra antiga "só Reels depois da
  conexão" caiu: Reels já publicados no Instagram também vão (para o TikTok são novos). Música: som **comercial**
  "Em alta" posto no app ao publicar o rascunho, 10-15% sob a voz (a voz do arquivo não muda). A fila inicial
  (23 vídeos, séries em dias seguidos) vai até 24/11; depois disso precisa de cortes curtos e respostas a
  comentário para manter 5 por semana.
- 6 Stories de 16/10 ficaram como "pronto" e não saíram (o Orbit não publica Stories).

## Série 19: Contrato intermitente e teste de dois estilos (26/10/2026)

- Gravação `Desktop\NOVOS REELS\VIDEO 1` (IMG_0384 + IMG_0385, 4K HEVC 10 bits). Trabalho em
  `C:\tmp\videos-reels\19-video1\` (`fontes/bruto-1080.mp4` é a cópia 1080 usada pelo `fala.py`: o 4K estourava a
  memória). Textos em `producao/reels/series/19-contrato-intermitente/` (falas com fatos e cortes, roteiros dos dois
  estilos, créditos Pexels, legenda). Cortes jurídicos: "24 horas para recusar" (lei: 1 dia útil, CLT 452-A §2º) e
  FGTS "no valor do dia" (é depositado, §8º); a tela mostra o certo.
- **Dois estilos de Reels (pedido da Jessica: "deixe o motor antigo intacto", "sempre me pergunte"):** inteiro com banco
  de imagens (`producao/reels/motor/`, intocado) e **tela dividida** (`producao/reels/motor-dividida/`: `engine.html`
  com cena `"painel"`, `fx.js` com o verificador da legenda invertido, `diagramas.py` com título, relógio recorrente,
  calendário, recibo, dezembro, comparação, balão, meses e balança). Referências: dois Reels do
  @viniciusguimaraes.ia (diagrama no alto, pessoa embaixo). A skill `leticia-reels-premium` já manda perguntar.
- **3D como clipe de fundo:** `producao/reels/motor3d/clip3d.py <destino> semana cofre` grava `stock-3d-<nome>.mp4`
  (mundo da 6x1 sem a camada 2D). Usado no R1 inteiro (convocação e FGTS).
- **R1 pronto nos dois estilos** (`contrato-intermitente-{inteiro,dividida}-1.mp4`, 50,5 s, conferir sem avisos,
  -19,9 LUFS por causa dos picos), cópias em `Desktop\NOVOS REELS\VIDEO 1\PRONTOS`. Plano: os dois como **Trial Reels**
  (só não seguidores), mesma legenda; o vencedor vai aos seguidores e o R2 sai nesse estilo. **Ainda não foram ao Orbit.**
- R2 ("Quando vira problema"): fala montada mas ainda com 3 emendas a acertar (trechos 9, 10 e 15 de `falas.py`).
- Ferramentas novas na conta do Claude (fora do git): skills `watch` (vídeo por link, modo local), `impeccable` e
  `hallmark` (este só para site novo: proíbe itálico em título e caixa-alta espaçada, que são da identidade).

## Pendências conhecidas (por ordem de "quão perto de virar trabalho ativo")

- **Crescimento orgânico (19/10/2026, pedido "faça tudo")**:
  - Feito no Orbit: capa do Reels no quadro do gancho (`thumb_offset`, padrão 1200 ms, `corpo.capa_ms`); Trial
    Reels ligado (`corpo.trial_reels` + agendamento `formato="trial"`, que não ocupa o dia dos seguidores; a Meta
    aceitou `trial_params` na v21). Rotina: 1 Trial por semana com o gancho B de um Reels da semana. Primeiro
    teste: "5 coisas" (gancho B) em 20/10 12h.
  - Localização pronta no código (`INSTAGRAM_LOCATION_ID`), mas a Meta recusa a página da Dra. porque ela não tem
    endereço. Ligar quando ela cadastrar o endereço de Vitória/ES na página (id 688466407676130).
  - Pendente com ela: campo Nome do perfil com palavra-chave; endereço na página do Facebook; republicar no
    Facebook exige reconectar com `pages_manage_posts`; YouTube Shorts exige conexão Google nova (uploads de app não
    verificado ficam privados). Hora extra 3/3: versão de até 45 s em produção (`fala-r6`).

- **PENDENTE (pedido de 18/10/2026, esperar ela liberar)**: limpeza do disco C (temporários do Windows com mais de 2
  dias, cerca de 13 GB, e cache do npm, 3,5 GB; Downloads é dela e não se toca) e instalação do **VoiceStudio**
  (debpalash/VoiceStudio, AGPL, app local de clonagem de voz; CPU-only precisa de cerca de 5 GB). Ela vai avisar.

- **Reels até 15/11 (16/10/2026)**: 16 Reels em dia útil às 21h (`reels_ate_1511.py`), séries em dias alternados, 13º
  entre 4 e 12/11 (pico de busca 6-12/11). Base: dados do perfil (terça melhor; sábado/domingo fracos; 21h) e pesquisa.
  Reels novo "5 coisas que a empresa não pode fazer com a gestante" (gravação da Dra., série 16) em 19/10.
- **Acervo de Reels (01-11) NÃO está no padrão**: texto fora da margem em 7, selo de verificado falso no 05 e 08,
  visual antigo e legenda provisória. Precisa ser refeito no motor atual antes de agendar. O 03 tinha sido aprovado
  e auto-agendado para 02/01/2027: agendamento pausado (nada apagado).

- **REGRA (16/10/2026): material pronto nunca some.** Versão nova é peça nova e arquivo novo (nome com versão); não
  reaproveitar peça de material pronto, não trocar vídeo sem guardar o anterior, não esconder material por
  ordenação. O Reels 04 do acervo (guarda, original da Dra.) tinha sido reaproveitado como Parte 1 da série Guarda e
  foi restaurado como peça própria (`restaurar_acervo04_1610.py`). Antes e depois de qualquer script que mexe em
  peças, contar por tipo e conferir que nada sumiu.

- **Reels: área segura nova (15/10/2026)**. A gestante 1/3 saiu com texto cortado nas bordas no iPhone (tela
  cheia corta ~98 px por lado) e foi excluída. Regra nova: laterais **150 px**, topo 270, base 672 (y ≤ 1248),
  legenda falada com no máximo 700 px de largura, centralizada (x 190–890) e longe da coluna de ícones da
  direita. No motor v2 (`producao/reels/motor`), a camada gráfica de cada cena é encolhida para o centro
  (`ZONA` = 0,83 em engine.html). Assim, o que é desenhado em x=90 cai em x≈155, já contando o push-in de
  1,03. O pó de ouro e as explosões passam pela mesma conta. O cabeçalho virou só "Letícia Barros" + série.
  O `.kick` ficou com 27 px, para continuar ≥22 px depois da escala. `checar()` (fx.js) agora usa 150/930
  e mede também o cabeçalho e a legenda. Motor v1 (série gestante, pasta 12): mesma ideia com `ZONA` 0,78,
  porque lá os elementos nascem em x=70 e a câmera chega a 1,06. Também ganhou `--checar`. O motor 3D
  (`pagina.html`) usa os mesmos limites. O verificador confere também durante as animações, a cada 0,1 s:
  carimbos que ficam ~1 s na tela escapavam da regra antiga de "só depois de assentar". Ele mede a moldura
  de carimbos e pílulas. O carimbo não quebra linha, encolhe a fonte sozinho até caber, e a batida inicial
  (até 2,4x) é limitada à área segura. Pílula "pop" cresce a partir da borda esquerda. Os 15 reels foram
  re-renderizados em 16/10, passaram no verificador e a folha de prova foi enviada a ela.
  Depois: mostrar amostras, subir com `?v=` novo e reagendar (todos os reels estão "pausado"; a gestante 1/3
  precisa de data nova).
- **Calendário de 1 post por dia (16/10/2026)**. Ela pediu: "uma publicação por dia" e "reels quando for dia de reels
  a noite". Aplicado por `_saida_producao_1510/aplicar_calendario_1610.py` (backup
  `/root/orbit-backups/pre-calendario-1por-dia-202610160841.sql.gz`). 16/10 a 31/12: 74 dias com 1 post, mais 3 Reels
  da Guarda (rascunho, `programacao` 23, 25 e 27/10, entram quando ela aprovar no Estúdio). Prioridade: Reels a cada
  2 dias nas séries, conteúdo de data marcada (eleição, 13º, 20/11, Natal) no prazo, carrossel, Mito ou Lei, e
  **frase aos domingos 11h**. **81 peças aprovadas ficaram na reserva**: sem agendamento, com
  `corpo.reserva {desde, motivo, programacao_antiga}`, prontas para usar em 2027 ou para tapar buraco. Os 15 Reels
  apontam para os vídeos da área segura nova (`?v=sz1`); a Gestante 1/3 voltou para 17/10 às 21h.
- **Revisão das frases do feed (pedido de 15/10/2026)**. Rodada 1 (16/10): 17 aprovadas. Destas, 12 mudaram de
  texto, receberam imagem nova (`frases_revisao_1610.py`, `?v=rev1610`) e guardam `corpo.frase_antiga`. 3 ela
  mandou manter a antiga. A de medida protetiva foi retirada ("não coloque nada sobre esse assunto"); só a frase
  saiu, o carrossel ficou. Rodada 2: 14 reescritas estão "Para avaliar" na página, com o pedido dela ao lado.
  Pedidos para não esquecer: evitar "também" e "combinado", ser direta e popular, dar nome às coisas
  (temporário, mãe/pai/filho), nunca soar como cobrança ao trabalhador. Ao aprovar, aplicar em `corpo.frase` e
  refazer a imagem.
- Histórico da revisão das frases. Ela achou "não" demais e leitura pouco fluida, inclusive
  nas aprovadas. Página de aprovação: https://claude.ai/artifact/VJaiy4ECR8aWKaVt3xqMP2 (db `frases/<id da
  peça>`: antiga, nova, status pendente/aprovada/refazer, pedido). Tem as 35 frases aprovadas de 17/10 a 31/12.
  **Nada muda no Orbit antes de ela aprovar.** Depois: aplicar as aprovadas em `corpo.frase`, refazer as imagens
  e reescrever as que ela pedir de novo. A regra vale daqui pra frente: menos negação, frase afirmativa e curta.

0. **Chave da OpenAI para o Jornalista** (opcional — terceira fonte):
   `OPENAI_API_KEY` no `.env` da API na VPS + `docker compose up -d api`.
   DNS/HTTPS da VPS: resolvidos (verificado 29/09/2026, cert até 28/11/2026).

1. **Redesenho visual — polimento por página ainda falta**: o tema claro já é o
   padrão de todo o app (22/07, ver "O que está pronto") — isso resolveu a cor/fundo/
   cards de todas as 9 telas de uma vez, via tokens. O que **ainda não** foi feito é
   o polimento bespoke que Login e Visão Geral receberam (ícones nos campos, stagger
   de entrada próprio da tela, contadores animados, hover glow específico) — as
   outras 6 telas (Planejamento, Aprovação, Calendário, Criativos, E-mails,
   Avaliações; Configurações já foi conferida visualmente e está OK mas simples)
   herdam só o básico (cores corretas + hover genérico do Card + transição de rota).
   Se a usuária pedir mais polimento visual, é apply o mesmo tratamento página a
   página, não mexer nos tokens de novo. Skills de design pra usar: `shadcn-ui`,
   `taste-design`, `ui-ux-pro-max-skill`, `stitch-design` (`~/.claude/skills/`).
2. **Estilo real dos criativos do Instagram**: Estúdio de Criativos hoje só gera
   texto-dourado-sobre-fundo-escuro; usuária quer o estilo real que ela usa (fotos de
   banco de imagens, formato "Me faça uma pergunta", formato "Segunda Jurídica",
   selo circular da marca). Ver `app/services/render_criativo.py`. Referência:
   repo `advogadaleticiabarros-del/blogautomaticoleticia` →
   `squads/@squad-design/criativos-estaticos/templates/`.
3. **Variantes de legenda via Groq**: teste A/B de 2-3 legendas alternativas na tela
   de Aprovação, gerado por Groq. Design aprovado, não construído ainda.
4. **Instagram — token do sistema**: RESOLVIDO em 08/10/2026 (ver "Ciclo
   editorial de 2 dias"). Falta só o produto da Meta para dados do Facebook.
5. **Publicador do Instagram**: cobre carrossel + imagem única (frase, pergunta,
   estático) desde 08/10/2026. Stories e Reels ainda sem publicador.
6. **`known_hosts=None` no SFTP do blog**: verificação de host key desabilitada
   (`app/integrations/publish/sftp_client.py`) — risco aceito por falta de acesso à
   fingerprint real do host; documentado, não resolvido.
7. **Fase 1 do redesenho — nunca vista num navegador real**: nenhum agente neste
   projeto teve acesso interativo a browser. Toda a Fase 1 (temas, motion, login,
   visão geral) foi verificada só via `tsc`/`build`. Recomendo checagem visual manual
   nos 4 temas + `prefers-reduced-motion` antes de assumir que está 100% correto.

## Decisões e observações que não são óbvias lendo o código

- **Groq é só pra triagem** (urgência de avaliações), não fallback nem geração de
  conteúdo principal — decisão explícita da usuária, não uma limitação técnica.
- **Categoria do blog vem sempre de `Pauta.area`**, sem mapeamento — decisão de
  design pra manter simples.
- **Capa do artigo de blog é intencionalmente simples** (dourado/preto via
  Playwright), não fotográfica — o estilo fotográfico é exclusivo do Estúdio de
  Criativos do Instagram (pendência 2 acima), fora de escopo pro publicador de blog.
- **`ScheduledPost.canal="blog"` só virou publicação de verdade em 22/07/2026** —
  antes disso era só uma categorização visual no calendário, sem nada publicando.
- **Railway CLI perde login entre sessões** — se `railway status`/`railway up`
  falhar com "Unauthorized", gerar um token novo em railway.app → Project Settings →
  Tokens e usar como `RAILWAY_TOKEN=... railway ...` (funciona sem `railway login`
  interativo). No Git Bash do Windows, prefixar `MSYS_NO_PATHCONV=1` em comandos que
  passem paths Unix-style como valor de variável (senão o Git Bash reescreve
  `/home/...` pra um path do Windows).
- **Todo o histórico de decisão de design/plano de implementação** fica versionado
  em `docs/superpowers/specs/` e `docs/superpowers/plans/` — vale checar antes de
  redesenhar algo já decidido.

## Como continuar uma sessão neste projeto

1. Leia este arquivo primeiro.
2. Se for mexer em algo que tem uma spec/plano recente em `docs/superpowers/`, leia
   o mais recente relacionado antes de propor mudanças.
3. Ao terminar uma implementação/mudança relevante (feature nova, bugfix não-trivial,
   decisão de design), **atualize este arquivo** — seções "O que está pronto",
   "Pendências" e "Decisões" são as que mais mudam.
