# 22/10/2026 — Google Business Profile API aprovada: correções antes de conectar

## Pedido
A Jessica colou o e-mail do Google aprovando o projeto 462973861302 (cota 300 consultas/min) e perguntou "e agora?".

## O que já existia
Integração completa no Orbit (julho/2026): OAuth (`/integracoes/google-business/iniciar` e `/callback`), botão
na Visão Geral, coleta diária de métricas (scheduler) e tela de Avaliações com triagem por IA.
`.env` da VPS (`/home/orbit-src/deploy/vps/.env`) já tem `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` e
`GOOGLE_REDIRECT_URI=https://api.orbit.advogadaleticiabarros.com.br/integracoes/google-business/callback`.

## Problemas encontrados e corrigidos (com teste antes)
1. **Avaliações** chamavam `mybusinessbusinessinformation.googleapis.com/v1/locations/{l}/reviews`, que não existe.
   Agora usam a API v4: `mybusiness.googleapis.com/v4/accounts/{a}/locations/{l}/reviews` e `.../reviews/{r}/reply`.
   O router passa a conta (`page_id`) e o local (`ig_user_id`).
2. **Métricas** mandavam só `dailyRange.start_date.year=2026` e o Google recusaria. Agora: últimos 30 dias até ontem,
   com início e fim completos.
3. **Visualizações** nunca eram preenchidas. Agora = `BUSINESS_IMPRESSIONS_DESKTOP_MAPS` + `MOBILE_MAPS`.

Arquivos: `apps/api/app/integrations/social/google_business_client.py`, `apps/api/app/routers/avaliacoes.py`,
`apps/api/tests/test_google_business_client.py`. Suíte da API: 279 testes passando.

## Falta (usuária)
1. Google Cloud Console → Biblioteca: ativar My Business Account Management API, My Business Business Information
   API e Business Profile Performance API.
2. Tela de consentimento OAuth em "Em produção" (em "Teste" o acesso expira a cada 7 dias).
3. Conferir que o URI de redirecionamento acima está cadastrado no cliente OAuth.
4. No Orbit: Visão Geral → Conectar Google Meu Negócio, com a conta Google dona do perfil.

## Observação
Se a conta tiver mais de um local, o callback usa o primeiro (`locais[0]`).
