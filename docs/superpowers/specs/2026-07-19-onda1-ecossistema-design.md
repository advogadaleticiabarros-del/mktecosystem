# Onda 1 do Ecossistema — Calendário, Criativos, Dashboard, Cérebro

**Contexto:** a v1 provou o motor (pauta → IA → aprovação → e-mail), mas a usuária precisa do ecossistema visível e operante: planejamento, produção de criativos, medição e aprendizado. Esta onda entrega tudo que não depende de integrações externas (Meta/Google ficam para a Onda 2 — exigem cadastros e app review).

## 1. Calendário editorial
- Tabela `scheduled_posts`: `id`, `tenant_id`, `content_piece_id?`, `titulo`, `canal` (`instagram` | `blog` | `email`), `formato` (`carrossel` | `post` | `story` | `artigo` | `newsletter`), `data_agendada` (date), `horario` (str "HH:MM"), `status` (`planejado` | `pronto` | `publicado`), `criado_em`.
- API `/calendario`: CRUD + `GET /calendario?mes=YYYY-MM` (lista do mês).
- **Auto-agendamento:** ao aprovar um `content_piece` (PATCH status=aprovado em /content), o backend cria `scheduled_post` "pronto" na próxima vaga livre do playbook do tenant (2 posts/dia: 11:00 e 17:00, começando amanhã). Nunca duplica (unique por content_piece_id).
- Página `/calendario`: grade mensal (7 colunas), cards por dia com canal/formato/status (cores por canal), clique abre editor (título, data, hora, canal, status), botão "+ novo" por dia. Navegação mês anterior/próximo.

## 2. Estúdio de criativos (client-side, custo zero)
- Página `/criativos`: seleciona um conteúdo aprovado tipo carrossel (ou legenda) → renderiza slides 4:5 (1080×1350) em HTML com a identidade visual do tenant (`TenantConfig.identidade_visual`: fundo escuro #231E1A, dourado #C9A962, fontes) → preview navegável → botão "Baixar todas" exporta PNGs via `html-to-image` (sem servidor de render; funciona no static export).
- Template v1: capa (gancho grande + marca), slides de conteúdo (título + corpo), slide final (CTA + @instagram + OAB). Mesma linguagem do template carrossel-4x5 já validado no blog.
- Dependência nova no web: `html-to-image` (leve, sem backend).

## 3. Dashboard `/visao-geral`
- API `GET /dashboard/resumo`: contagens e séries do próprio banco — pautas geradas/semana, conteúdos por status, e-mails enviados/abertos (email_sends), contatos por origem, próximos agendamentos.
- Página com stat-tiles + gráficos (barras/linhas SVG próprios, sem lib pesada) + seção "Conectar fontes" com cards Instagram/GA4/Google Meu Negócio marcados "Onda 2 — em breve" (deixa o destino visível).

## 4. Cérebro (marketing_memory ativo)
- Ao aprovar conteúdo: grava memória `{tipo: "aprovacao", area, angulo, formato}`.
- Ao editar antes de aprovar (corpo mudou da versão gerada): grava `{tipo: "edicao", campo, resumo_diff}` — sinal do que a IA erra para este tenant.
- Geração de conteúdo passa a injetar no prompt as últimas N memórias de edição ("evite estes padrões que a cliente corrige").

## Fora desta onda
- Publicação automática em redes (Onda 2: Meta Graph API), GA4/GMB (Onda 2), recomendações automáticas e campanhas pagas (Onda 3 — precisam de dados das integrações para não serem chute).

## Critério de pronto
- Fluxo demonstrável de ponta a ponta local: aprovar conteúdo → aparece no calendário → gerar criativo → baixar PNGs → dashboard reflete tudo.
