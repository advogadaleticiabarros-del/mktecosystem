# Orbit — Contexto Vivo do Projeto

> Este arquivo é a "consciência" do projeto: o que existe, o que está em andamento,
> o que falta. Deve ser atualizado ao final de toda mudança/implementação relevante
> (ver `.claude/skills/contexto-orbit/SKILL.md`). Última atualização: **2026-07-22**
> (órbita do login sem corte + estrelas cadentes + glow que segue o cursor).

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
- **Deploy**: **Railway** (migrado da Hostinger em 21/07/2026). Projeto
  `orbit-marketing-os`, conta `alcancelegalmkt-collab`. Dois serviços:
  - `orbit-api` → `https://orbit-api-production-0029.up.railway.app`
  - `orbit-web` → `https://orbit-web-production-0a39.up.railway.app`
  - Convenção deste projeto: **commit direto na `main`**, sem branch de feature —
    confirmado repetidamente ao longo da sessão, é assim que o time trabalha aqui.
  - Deploy manual: `railway up ./apps/<api|web> --path-as-root --service orbit-<api|web> --detach`
    (o `railway up` sem `--path-as-root` builda a partir da raiz do monorepo e falha).
  - **Gotcha resolvido 22/07**: build do `orbit-web` falhava sempre (~23s, sem log
    nenhum) por colisão de mount do BuildKit em `/app/tsconfig.tsbuildinfo` (TS
    incremental grava esse arquivo na raiz por padrão). Corrigido apontando
    `tsBuildInfoFile` pra dentro de `.next/cache` no `tsconfig.json`. Se o deploy do
    `orbit-web` voltar a falhar sem log nenhum logo após o build, comece por aqui.
- **Blog público** (site separado, NÃO é o Orbit): `advogadaleticiabarros.com.br/blog/`,
  HTML estático hospedado na Hostinger, publicado via SFTP (host `147.93.38.211`,
  porta `65002`, usuário `u528898188`, caminho
  `/home/u528898188/domains/advogadaleticiabarros.com.br/public_html/blog/`).
  Credenciais salvas como env vars `BLOG_SFTP_*` no serviço `orbit-api` do Railway.

## O que está pronto e em produção

### Backend — módulos completos
- **Auth**: login, troca de senha, JWT.
- **Pautas**: pesquisa automática (STF/TST/CNJ) + geração manual, com IA.
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

## Pendências conhecidas (por ordem de "quão perto de virar trabalho ativo")

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
4. **Instagram — token do sistema**: usuária precisa gerar um token de System User
   no Gerenciador de Negócios da Meta (permissões `pages_show_list`,
   `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`,
   `business_management`) e colar no botão "Colar token" da Visão Geral — OAuth
   direto está bloqueado por exigência de Business Verification sem atalho de teste.
5. **Publicador do Instagram só cobre carrossel**: legenda (`formato="post"`) e
   stories ainda não têm publicador — são explicitamente ignorados pela query de
   seleção (`instagram_publisher.py`) pra não tentar montar carrossel vazio.
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
