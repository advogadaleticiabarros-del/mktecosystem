# Onda 2 (parte 3) — Google Meu Negócio (Business Profile)

**Objetivo:** conectar o perfil do Google Meu Negócio da Letícia para (a) puxar métricas reais (buscas, ligações, pedidos de rota, visualizações) para a Visão Geral e as dicas da IA, e (b) permitir responder avaliações de clientes direto pelo Orbit.

**Pré-condição externa (fora do nosso controle):** a Google Business Profile API exige aprovação formal (perfil verificado há 60+ dias, site próprio, pedido de acesso com justificativa, 3–10 dias úteis de análise). O código fica pronto e testado com mocks antes da aprovação — igual fizemos com o Instagram — e conectamos de verdade assim que o Google liberar.

## Componentes

### 1. Conexão (OAuth Google, refresh token)
Reaproveita a tabela `social_connections` (já existe, `plataforma` distingue `"instagram"` de `"google_business"`). Diferença do fluxo Meta: o Google usa **refresh token** de longa duração — `access_token_encrypted` passa a guardar o refresh token criptografado; o access token (válido ~1h) é obtido sob demanda a cada chamada via `POST https://oauth2.googleapis.com/token` com `grant_type=refresh_token`, nunca persistido.

Campos reaproveitados com semântica por plataforma (documentado em comentário no modelo, sem migration nova):
- `page_id` → Google **Account ID** (`accounts/{accountId}`)
- `ig_user_id` → Google **Location ID** (`locations/{locationId}`)

- `GET /integracoes/google-business/iniciar` (autenticado): monta URL do consentimento OAuth do Google (`accounts.google.com/o/oauth2/v2/auth`) com scopes `https://www.googleapis.com/auth/business.manage`, `access_type=offline`, `prompt=consent` (força emissão de refresh token mesmo em reconexões).
- `GET /integracoes/google-business/callback` (pública, valida `state` assinado): troca `code` por `access_token`+`refresh_token`, lista contas (`GET /v1/accounts`) e locais (`GET /v1/accounts/{id}/locations`), salva a primeira conta+local encontrados.
- `DELETE /integracoes/google-business`: marca `status="desconectado"`.
- `GET /integracoes` (já existe, genérico): já retorna qualquer plataforma conectada — sem mudança.

### 2. Métricas diárias
Novo serviço `google_business_metrics.py`: para cada conexão ativa, renova o access token e chama a **Business Profile Performance API** (`GET .../locations/{id}:fetchMultiDailyMetricsTimeSeries`) pedindo `BUSINESS_IMPRESSIONS_DESKTOP_SEARCH`, `BUSINESS_IMPRESSIONS_MOBILE_SEARCH`, `CALL_CLICKS`, `BUSINESS_DIRECTION_REQUESTS` dos últimos 7 dias. Grava em `social_metrics` com `tipo="google_business"`.

`GET /dashboard/resumo` ganha um bloco `google_business` (buscas, ligações, pedidos de rota, visualizações) ao lado do bloco `instagram` já existente — mesmo formato, sem quebrar o payload atual.

Roda no mesmo scheduler diário do Instagram (`job_metricas_instagram` vira `job_metricas_fontes_externas`, chamando os dois coletores).

### 3. Responder avaliações
- `GET /avaliacoes`: busca ao vivo (`GET .../locations/{id}/reviews`) as avaliações do local conectado — sem cache/tabela nova, volume baixo o suficiente para buscar direto a cada visita à página.
- `POST /avaliacoes/{review_id}/responder`: envia a resposta (`PUT .../reviews/{reviewId}/reply`) com o texto escrito pela usuária. Sem geração automática por IA — sempre texto humano, dado o risco reputacional de resposta pública malcalibrada.
- Página nova `/avaliacoes`: lista com nome do cliente, nota, texto, campo de resposta e botão "Responder"; avaliações já respondidas mostram a resposta existente (sem novo campo).

### 4. Frontend
- Visão Geral: card "Google Meu Negócio" sai de `FONTES_FUTURAS` e vira card real com "Conectar" (mesmo componente/padrão do Instagram), mostrando buscas/ligações quando conectado.
- Nova entrada "Avaliações" na barra lateral (`AppShell`), ícone de estrela.

## Fora de escopo desta parte
Posts automáticos no perfil, gestão de horário/fotos/produtos, resposta a avaliação por IA, múltiplos locais por tenant (assume 1 local, como as outras integrações assumem 1 conta).

## Erros e conformidade
- Sem acesso aprovado pelo Google ainda: `/integracoes/google-business/iniciar` funciona normalmente (o OAuth em si não depende da aprovação da Performance API), mas as chamadas de métrica/avaliação retornam erro da API do Google — tratado como falha silenciosa no worker (loga e pula, mesmo padrão do Instagram) e mensagem de erro amigável nas páginas.
- Token expirado/revogado: mesmo tratamento do Instagram (`status="expirado"`, card avisa reconectar).

## Testes
- Unit: troca de refresh token por access token (mock httpx), parsing de métricas, seleção de conexões ativas.
- Integração: fluxo `/integracoes/google-business/callback` mockado, `/avaliacoes` GET e POST `/responder` mockados.
