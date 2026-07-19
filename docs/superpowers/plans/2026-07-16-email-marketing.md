# E-mail Marketing (Resend) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base de contatos própria + sequência de boas-vindas + newsletter semanal, entregues via Resend (free tier), com aprovação humana obrigatória.

**Architecture:** Orbit/Postgres é dono dos contatos; Resend só entrega (API transacional). Worker APScheduler in-process. Aprovação via tela `/emails`.

**Tech Stack:** FastAPI + SQLAlchemy async + Alembic + APScheduler + httpx + Resend REST API; Next.js static export no frontend.

## Global Constraints
- Nenhum e-mail sai de campanha com status ≠ `aprovado`.
- Teto de envio: 90/dia (margem sob o limite 100/dia do Resend Free).
- Todo e-mail: link de descadastro próprio + rodapé OAB do TenantConfig.
- Multi-tenant: toda query filtra por `tenant_id`.
- Novas env vars: `RESEND_API_KEY`, `EMAIL_FROM`, `RESEND_WEBHOOK_SECRET` (vazias em dev ⇒ envio vira no-op logado).

---

### Mapa Task 1: Modelos + migration
**Files:** Create `apps/api/app/models/contact.py`, `apps/api/app/models/email_campaign.py`, `apps/api/app/models/email_send.py`; nova revision Alembic.
**Produces:** `Contact(tenant_id, nome, email, origem, consentimento_em, status, welcome_step, criado_em)` com unique (tenant_id, email); `EmailCampaign(tenant_id, tipo, assunto, corpo_html, corpo_texto, status, criado_em, aprovado_em, enviado_em)`; `EmailSend(tenant_id, campaign_id, contact_id, resend_id, status, criado_em)` com unique (campaign_id, contact_id).
**Steps:** modelos → importar em `models/__init__.py` → `alembic revision --autogenerate` → revisar migration → commit.

### Mapa Task 2: Token de descadastro + captura pública
**Files:** Create `apps/api/app/core/unsubscribe.py`, `apps/api/app/routers/public.py`, `apps/api/app/schemas/contact.py`; Test `apps/api/tests/test_public_contacts.py`.
**Produces:** `make_unsubscribe_token(contact_id) -> str`, `verify_unsubscribe_token(token) -> uuid | None` (HMAC-SHA256 com JWT_SECRET, formato `hex_id.assinatura`); `POST /public/contacts` (payload: tenant_slug, nome, email, origem, website honeypot); `GET /public/unsubscribe?token=`.
**Steps:** testes do token (válido/adulterado) → implementar → testes do endpoint (honeypot descarta, duplicado idempotente, consentimento gravado) → implementar → registrar router no main → commit.

### Mapa Task 3: Cliente Resend + config
**Files:** Create `apps/api/app/integrations/email/__init__.py`, `apps/api/app/integrations/email/resend_client.py`; Modify `apps/api/app/config.py`; Test `apps/api/tests/test_resend_client.py`.
**Produces:** `ResendClient(api_key, sender).send(to, subject, html, text) -> str | None` (retorna resend_id; sem api_key ⇒ loga e retorna None); função `montar_rodape(tenant_config, unsubscribe_url) -> str`.
**Steps:** teste com httpx MockTransport → implementar cliente → config novas vars → commit.

### Mapa Task 4: Campanhas + geração IA + API autenticada
**Files:** Create `apps/api/app/routers/email.py`, `apps/api/app/schemas/email_campaign.py`, `apps/api/app/services/email_campaigns.py`; Modify `apps/api/app/main.py`.
**Produces:** service `gerar_boas_vindas(db, tenant_id, ai)` (3 rascunhos na voz do tenant), `gerar_rascunho_newsletter(db, tenant_id, ai)` (artigos ≤7 dias; sem artigos ⇒ None); rotas `GET/PATCH /email/campaigns`, `POST /email/campaigns/gerar-boas-vindas`, `POST /email/campaigns/gerar-newsletter`, `GET /email/contacts`. PATCH aceita `assunto`, `corpo_html`, `corpo_texto`, `status` (aprovar grava `aprovado_em`).
**Steps:** schemas → service com prompts (voz + OAB, tom educativo) → rotas → registrar router → commit.

### Mapa Task 5: Worker de envio (APScheduler)
**Files:** Create `apps/api/app/services/email_sender.py`, `apps/api/app/scheduler.py`; Modify `apps/api/app/main.py` (lifespan); Test `apps/api/tests/test_email_sender.py`.
**Produces:** `processar_boas_vindas(db)` (cadência 0/2/5 dias por `welcome_step` + `criado_em`/último send; só templates aprovados; incrementa passo), `processar_fila_newsletter(db)` (campanha aprovada → contatos ativos sem send, corte 90/dia global), `contar_envios_hoje(db)`. Scheduler: horário para os dois processadores; cron segunda 11:00 UTC para rascunho de newsletter.
**Steps:** testes de seleção/cadência/corte com sqlite in-memory → implementar services → scheduler no lifespan (flag `ENABLE_SCHEDULER`, default true em prod, false em testes) → commit.

### Mapa Task 6: Webhook Resend
**Files:** Modify `apps/api/app/routers/public.py`; Test `apps/api/tests/test_resend_webhook.py`.
**Produces:** `POST /public/webhooks/resend` com verificação Svix (HMAC base64 sobre `{id}.{timestamp}.{payload}` com `RESEND_WEBHOOK_SECRET`); `email.bounced` ⇒ contato bounce; `email.complained` ⇒ descadastrado; atualiza `email_sends` pelo `resend_id`.
**Steps:** teste assinatura válida/ inválida + efeitos → implementar → commit.

### Mapa Task 7: Frontend `/emails`
**Files:** Create `apps/web/app/(app)/emails/page.tsx`; Modify `apps/web/components/app-shell.tsx` (item de menu "E-mails").
**Produces:** lista de campanhas (badge por status), editor assunto/corpo (textarea), botões Gerar boas-vindas / Gerar newsletter / Aprovar; contador de contatos ativos.
**Steps:** página seguindo padrão das existentes → menu → `npm run build` verde → commit.

### Mapa Task 8: Deploy + setup externo (com o usuário)
**Steps:** rodar suite completa → push (Railway aplica migration via deploy) → guiar criação da API key no Resend + verificação do domínio (2 registros DNS na Hostinger) + webhook endpoint → setar env vars no Railway → teste real de envio para e-mail da Letícia.
