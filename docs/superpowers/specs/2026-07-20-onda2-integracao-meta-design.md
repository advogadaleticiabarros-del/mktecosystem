# Onda 2 (parte 1) — Integração Instagram/Facebook (Meta Graph API)

**Objetivo:** conectar a conta real do Instagram/Facebook da Letícia ao Orbit para (a) publicar automaticamente o que está aprovado e agendado no Calendário, e (b) puxar métricas reais (alcance, curtidas, comentários, seguidores) para a Visão Geral e as dicas da IA.

**Pré-requisitos já resolvidos (2026-07-20):** app Meta `orbit.mkt` criado (App ID `4422857141191476`), caso de uso "Facebook Login for Business", redirect URI configurado. Instagram `@adv.leticiabarros2` é conta Business vinculada a uma Página do Facebook administrada pela própria Letícia — conexão funciona em modo de desenvolvimento, sem precisar de App Review da Meta (só seria necessário se conectássemos contas de terceiros fora do app).

## Componentes

### 1. `social_connections` (nova tabela)
`id, tenant_id, plataforma ("instagram"), page_id, ig_user_id, nome_conta, access_token_encrypted, expira_em, status ("ativo"|"expirado"|"desconectado"), conectado_em`. Um registro por tenant+plataforma (unique).

Token **sempre criptografado em repouso** com Fernet (`ENCRYPTION_KEY`, já gerada e configurada no Railway). Nunca retorna o token em nenhum endpoint da API — só usado internamente pelos workers/serviços.

### 2. Fluxo de conexão (OAuth)
- `GET /integracoes/instagram/iniciar` (autenticado): monta a URL de autorização da Meta (`dialog/oauth`) com os scopes `pages_show_list, pages_read_engagement, instagram_basic, instagram_content_publish, business_management` e redireciona.
- `GET /integracoes/instagram/callback` (rota pública, valida `state` assinado contra CSRF): troca o `code` por um token de usuário de curta duração, troca por token de longa duração (60 dias), busca `/me/accounts` para achar a Página administrada, busca `instagram_business_account` associado a ela. Salva/atualiza `social_connections` criptografado. Redireciona de volta para `/visao-geral?conectado=instagram`.
- `DELETE /integracoes/instagram`: marca `status="desconectado"` (não deleta o histórico de métricas).
- `GET /integracoes`: lista conexões do tenant com status (sem token) — alimenta os cards da Visão Geral.

### 3. Renderização server-side dos criativos
- Novo módulo `app/services/render_criativo.py`: usa Playwright (headless Chromium) para renderizar o mesmo HTML/CSS do Estúdio de Criativos (portado para um template Jinja2 no backend) e tirar screenshot 1080×1350 em PNG.
- Endpoint público `GET /media/{arquivo}` serve os PNGs gerados (salvos em `apps/api/media/`, montado como volume persistente no Railway — mesmo padrão do volume do Postgres).
- Reuso: o Estúdio de Criativos no frontend continua existindo para download manual; a rota de publicação automática usa a versão server-side (mesmo template visual, fonte de verdade única documentada, sem duplicar design).

### 4. Publicação automática (worker)
- `app/services/instagram_publisher.py`: `publicar_agendamentos_prontos(db)` — seleciona `scheduled_posts` com `canal="instagram"`, `status="pronto"`, `data_agendada+horario <= agora`, cujo `content_piece` está aprovado.
- Para `formato="carrossel"`: renderiza todos os slides, cria um container de mídia por imagem (`is_carousel_item=true`), cria o container pai (`media_type=CAROUSEL`), publica.
- Para `formato="post"`/`"story"`: renderiza uma imagem única, cria container, publica (stories usa `media_type=STORIES`).
- Sucesso: grava `platform_post_id` em `scheduled_posts`, `status="publicado"`. Falha: `status` permanece `"pronto"`, loga erro, tenta de novo na próxima passada (idempotente — Graph API não duplica se reenviado o mesmo container, mas por segurança marcamos `tentativas` e paramos após 3 falhas, status vira `"erro"`).
- Sem conexão ativa do tenant: pula silenciosamente (log informativo, não erro).
- Roda no mesmo scheduler do e-mail, a cada hora.

### 5. Métricas (worker diário)
- `app/services/instagram_metrics.py`: para cada conexão ativa, busca `/{ig_user_id}/insights` (conta: alcance, seguidores) e `/{media_id}/insights` dos posts publicados nos últimos 30 dias.
- Nova tabela `social_metrics`: `id, tenant_id, tipo ("conta"|"post"), referencia_id (scheduled_post_id ou null), metricas (JSON), coletado_em`.
- `GET /dashboard/resumo` passa a incluir um bloco `instagram` (seguidores atuais, alcance da semana, top 3 posts) quando há conexão ativa — mantém o resto do payload igual.
- `app/services/insights.py` (dicas automáticas) passa a incluir essas métricas reais na coleta de dados quando disponíveis — sem mudar a interface do endpoint.

### 6. Frontend
- Visão Geral: os 3 cards "Em breve" ganham um botão **Conectar** funcional para Instagram (GA4/GMB continuam "Em breve" — fora desta parte da Onda 2). Card conectado mostra nome da conta + botão "Desconectar".
- Calendário: item com `canal="instagram"` e `status="publicado"` ganha um pequeno indicador de link para o post real (usa `platform_post_id` para montar a URL `instagram.com/p/...` — best-effort, não crítico se a Meta não retornar o shortcode).

## Fora de escopo desta parte
GA4 e Google Meu Negócio (sub-projetos próprios da Onda 2), App Review da Meta (só necessário para multi-tenant com contas de terceiros), Stories com elementos interativos (enquete, link) — só imagem estática por enquanto.

## Erros e conformidade
- Token expirado/révogado: `status="expirado"`, card na Visão Geral avisa para reconectar, worker pula e loga.
- Rate limit da Meta: publisher respeita `retry-after` se retornado; se não, backoff simples (pula essa passada).
- LGPD/segurança: token nunca aparece em log nem em resposta de API; `ENCRYPTION_KEY` já provisionada.

## Testes
- Unit: criptografia do token (roundtrip), seleção de agendamentos prontos para publicar, montagem do container de carrossel (mock da API da Meta via httpx), parsing de métricas.
- Integração: fluxo completo `/integracoes/instagram/callback` com Graph API mockada; publisher fim-a-fim com render mockado (sem depender de Playwright real nos testes, usar uma imagem fixture).
