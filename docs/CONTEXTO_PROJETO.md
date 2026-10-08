# Orbit — Contexto Vivo do Projeto

> Este arquivo é a "consciência" do projeto: o que existe, o que está em andamento,
> o que falta. Deve ser atualizado ao final de toda mudança/implementação relevante
> (ver `.claude/skills/contexto-orbit/SKILL.md`). Última atualização: **2026-10-08**
> (migração de deploy Railway → VPS Hostinger, DNS ainda pendente).

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
- **E-mail marketing**: campanhas com geração IA, captura pública de contatos,
  descadastro com token HMAC, worker de envio com cadência/teto diário/idempotência,
  webhook Resend (bounce/reclamação via Svix).
- **Dashboard**: `GET /dashboard/resumo` agrega tudo pra Visão Geral.
- **Dicas de desempenho**: IA cruza produção/aprovação/edição/e-mail e devolve
  recomendações (`app/services/insights.py`).

### Frontend — 9 telas do grupo `(app)` + login
`visao-geral`, `planejamento`, `aprovacao` (via query `?pautaId=`), `calendario`,
`criativos`, `emails`, `configuracoes`, `avaliacoes`, `resumo-diario` (usado na
Visão Geral também). Layout comum via `AppShell` (`components/app-shell.tsx`).

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
- **Agenda** (`agenda.py`): Instagram segue o ciclo — dias de tema alternam a
  partir de `CICLO_ANCORA = 2026-10-09`; pergunta 12h, frase 15h, carrossel 20h
  da mesma pauta no mesmo dia (uma pauta por dia de tema); estático 19h no dia
  de respiro seguinte ao tema da sua pauta. Artigo/jornal/legenda/stories/reels
  seguem o playbook antigo (11h/17h).
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

## Pendências conhecidas (por ordem de "quão perto de virar trabalho ativo")

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
