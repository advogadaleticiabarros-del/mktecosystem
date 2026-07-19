# Módulo E-mail Marketing (Resend) — Design

**Objetivo:** nutrir leads da LP e enviar newsletter semanal dos artigos, com aprovação humana obrigatória, custo zero (Resend Free: 3.000 e-mails/mês, 100/dia, 1 domínio).

**Decisão de arquitetura:** o Orbit é o dono da base de contatos (Postgres, multi-tenant). O Resend é usado apenas como API transacional de entrega — não usamos Audiences/Broadcasts (teto de 1.000 contatos e base presa na conta deles). Descadastro, supressão e métricas ficam no Orbit.

## Componentes

### 1. Base de contatos
- Tabela `contacts`: `id`, `tenant_id`, `nome`, `email` (único por tenant), `origem` (`lp` | `blog`), `consentimento_em` (timestamp — LGPD), `status` (`ativo` | `descadastrado` | `bounce`), `welcome_step` (0–3, próximo passo da sequência), `criado_em`.
- Endpoint público `POST /public/contacts` (sem auth): valida e-mail, campo honeypot `website` (preenchido ⇒ descarta silenciosamente com 200), grava consentimento com timestamp. Idempotente: e-mail repetido no mesmo tenant retorna 200 sem duplicar.
- Endpoint público `GET /public/unsubscribe?token=...`: token HMAC-SHA256 (`contact_id`, assinado com `JWT_SECRET`), marca `status=descadastrado`, responde página simples de confirmação.

### 2. Campanhas de e-mail (aprovação obrigatória)
- Tabela `email_campaigns`: `id`, `tenant_id`, `tipo` (`boas_vindas_1` | `boas_vindas_2` | `boas_vindas_3` | `newsletter`), `assunto`, `corpo_html`, `corpo_texto`, `status` (`rascunho` | `aprovado` | `enviado` | `arquivado`), `criado_em`, `aprovado_em`, `enviado_em`.
- Sequência de boas-vindas: 3 templates gerados pela IA (voz do tenant via `TenantConfig.voz`) **uma única vez**, aprovados no Orbit, reutilizados por lead. Cadência: passo 1 imediato, passo 2 no dia 2, passo 3 no dia 5.
- Newsletter: rascunho gerado automaticamente toda segunda 08:00 UTC-3 com artigos da semana; só envia após `status=aprovado`. Aprovação dispara envio para toda a base ativa (respeitando 100/dia — batch com corte diário).
- Regra invariante: **nenhum e-mail sai com campanha fora de `aprovado`**.

### 3. Entrega (Resend)
- `app/integrations/email/resend_client.py`: cliente httpx para `POST https://api.resend.com/emails`. Config nova: `RESEND_API_KEY`, `EMAIL_FROM` (ex.: `Letícia Barros <contato@advogadaleticiabarros.com.br>`).
- Todo e-mail inclui: link de descadastro (endpoint próprio) e rodapé com identificação profissional (OAB) vindo de `TenantConfig`.
- Tabela `email_sends` (log): `id`, `tenant_id`, `campaign_id`, `contact_id`, `resend_id`, `status` (`enviado` | `erro` | `bounce` | `reclamacao`), `criado_em`. Única por (`campaign_id`, `contact_id`) — impede reenvio duplicado.
- Webhook `POST /public/webhooks/resend`: verifica assinatura Svix (HMAC, `RESEND_WEBHOOK_SECRET`); `email.bounced` ⇒ contato `status=bounce`; `email.complained` ⇒ `descadastrado`. Atualiza `email_sends.status`.

### 4. Worker (APScheduler, in-process no FastAPI)
- Job horário `processar_boas_vindas`: seleciona contatos ativos com passo pendente e tempo decorrido; envia o template aprovado do passo; incrementa `welcome_step`. Se o template do passo não está aprovado, pula (sem erro).
- Job semanal `gerar_rascunho_newsletter` (segunda): monta rascunho com artigos dos últimos 7 dias (fonte: `content_pieces` tipo blog aprovados na semana; fallback: sem artigos ⇒ não cria rascunho).
- Job horário `processar_fila_newsletter`: envia campanha newsletter `aprovado` para contatos ativos ainda sem `email_send` dela, até o teto diário (margem: 90/dia).

### 5. API autenticada (`/email/*`)
- `GET /email/contacts` — lista contatos do tenant (com status).
- `POST /email/campaigns/gerar-boas-vindas` — IA gera os 3 rascunhos da sequência.
- `POST /email/campaigns/gerar-newsletter` — força geração do rascunho da semana (mesmo código do job).
- `GET /email/campaigns` / `PATCH /email/campaigns/{id}` — listar, editar corpo/assunto, aprovar (`status=aprovado` grava `aprovado_em`).

### 6. Frontend (mínimo)
- Página `/emails`: lista campanhas com status, editor simples (assunto + corpo), botão Aprovar; contador de contatos. Segue AppShell/design system atuais. (Obs.: publicação do frontend depende do destravamento do docroot Hostinger — o código fica pronto e commitado.)

## Fora de escopo (YAGNI)
- Audiences/Broadcasts do Resend; segmentação; A/B; templates React Email; importação de listas; e-mails transacionais de outros fluxos.

## Erros e conformidade
- Falha no Resend ⇒ `email_sends.status=erro`, retry na próxima passada do job (idempotência pela unicidade campaign+contact: só re-tenta quando status=erro).
- LGPD: consentimento com timestamp na captura; descadastro 1 clique; supressão automática de bounce/reclamação.
- OAB: conteúdo educativo, sem captação ativa; rodapé identificado; aprovação humana sempre.

## Testes
- Unit: token de descadastro (gera/valida/rejeita adulterado); honeypot; idempotência de contato; seleção de contatos por passo/tempo; corte diário.
- Integração (httpx mock): envio marca `email_sends`; webhook bounce marca contato.
