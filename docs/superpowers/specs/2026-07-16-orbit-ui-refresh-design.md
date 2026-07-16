# Orbit UI Refresh — Design

## Contexto e visão

A v1 do Marketing OS (marca de produto: **Orbit — "The Marketing Operating
System"**) está em produção, funcionando de ponta a ponta (pesquisa de pautas,
geração de conteúdo com IA, aprovação, publicação estática). O frontend hoje é
funcional mas visualmente cru: quatro páginas com estilo inline (`style={{}}`),
sem sistema de design, sem menu de navegação persistente.

A tenant recebeu (ou produziu) um mockup de alta fidelidade das quatro telas —
Login, Planejamento, Resumo Jurídico Diário, Aprovação — com identidade visual
de produto de tecnologia: menu lateral persistente, cards, badges, indicador de
progresso multi-etapa, e animações ambiente. Este documento cobre a reforma
visual completa para bater com esse mockup, mantendo a plataforma funcionalmente
onde está (nenhuma mudança de backend).

## Escopo

**Dentro do escopo:**
1. Introdução de Tailwind CSS + shadcn/ui + lucide-react + Framer Motion no
   `apps/web`, com fontes novas via `next/font/google`.
2. Um componente de shell compartilhado (menu lateral + topo) envolvendo as
   três páginas autenticadas (Planejamento, Resumo Diário, Aprovação).
3. Reconstrução visual das 4 páginas para bater com o mockup.
4. Animações: brilho ambiente contínuo (CSS), reações de hover/transição
   (Framer Motion), indicador de progresso animado na tela de Aprovação.
5. Elementos do mockup sem contraparte funcional hoje (recuperação de senha,
   "lembrar-me", seleção múltipla no Resumo Diário com handoff pro
   Planejamento, etapa "Publicado" do indicador de progresso) — **implementados
   visualmente, mas desabilitados**, com o que falta no backend documentado no
   Bloco 4 abaixo.

**Fora do escopo:**
- Qualquer mudança de comportamento do backend (nenhuma rota nova, nenhuma
  migração).
- Tornar funcionais os elementos desabilitados listados acima — isso é
  trabalho futuro, só documentado aqui.
- Testes automatizados de UI (fora do padrão já estabelecido no projeto —
  validação manual, como as demais páginas).

## Arquitetura

**Novas dependências em `apps/web`:**
- `tailwindcss` + `postcss` + `autoprefixer` — configuração padrão Next.js App
  Router.
- `shadcn/ui` (via `npx shadcn@latest init`) — componentes copiados para
  `apps/web/components/ui/`, não é dependência de runtime.
- `lucide-react` — ícones.
- `framer-motion` — animações de interação.
- Fontes: `next/font/google` importando **Space Grotesk** (títulos, wordmark
  "ORBIT") e **Inter** (corpo — já em uso hoje). Decidido, não é placeholder —
  ambas self-hospedadas via `next/font/google`, sem chamada externa em
  produção.

Todas essas dependências são compatíveis com `output: "export"` (confirmado:
Tailwind processa em build time, shadcn é código copiado, lucide-react e
framer-motion são bibliotecas client-side puras, `next/font/google` baixa e
self-hospeda as fontes no build) — nenhuma quebra o deploy estático existente
pro Hostinger.

**Tokens de cor:** os já verificados contra o CSS real do site
(`--fundo-escuro #231E1A`, `--dourado #C9A962`, `--areia #E8DED1`, etc.,
documentados em `apps/api/app/seed/seed_leticia.py` e no spec da v1) viram a
base do tema Tailwind (`tailwind.config.ts` → `theme.extend.colors`), não
valores novos inventados.

## Estrutura compartilhada — AppShell

Novo componente `apps/web/components/app-shell.tsx`: barra lateral fixa
(logotipo Orbit, ícones de navegação — Home/Planejamento/Resumo
Diário/Aprovação — sino de notificação e avatar do usuário no topo). Item de
navegação ativo destacado com pílula dourada, igual ao mockup.

Aplicado via layout de grupo de rotas: `app/(app)/layout.tsx` envolvendo
`planejamento/`, `resumo-diario/`, `aprovacao/`. A página `login/` fica **fora**
desse grupo, com layout próprio (painel hero + card de formulário, tela
cheia, sem menu lateral).

## Páginas

**Login** (`app/login/page.tsx`): painel esquerdo com headline ("O centro de
todo o seu marketing."), tagline, linhas douradas com brilho/rotação contínua
em CSS puro; painel direito com card de formulário (e-mail, senha com ícone de
mostrar/ocultar, "Lembrar de mim" e "Esqueci minha senha" **desabilitados**,
botão "Entrar na plataforma", selo "Segurança de nível empresarial").

**Planejamento**: cards de sugestão (ícone por área, título, badge
área/ângulo, "Fonte: X", botão "Gerar conteúdo →"), campo de tema livre, botão
"Resumo Jurídico Diário" no topo — tudo já funcional hoje, só reestilizado.

**Resumo Jurídico Diário**: agrupado por área (títulos em dourado), itens com
badge "candidato a conteúdo" nos relevantes, seletor de data no topo (mostra a
data atual, sem navegação entre datas — isso não existe no backend). Barra
inferior de seleção múltipla + "Ir para planejamento" — **desabilitada**,
visual apenas.

**Aprovação**: indicador de progresso vertical (Planejamento → Pesquisa →
Conteúdo → Revisão → Publicado) — as quatro primeiras etapas refletem o estado
real da peça (pauta escolhida → fontes buscadas → conteúdo gerado → aguardando
aprovação); "Publicado" **sempre inativo/cinza**, sem lógica de estado (não
existe módulo de publicação). Conteúdo (artigo/carrossel/etc.) em cards com
preview estilizado do JSON, botões Aprovar/Rejeitar, indicador "Salvo
automaticamente".

## Elementos desabilitados — o que falta pra ficarem reais

Documentado aqui para orientar módulos futuros, não implementado agora:

| Elemento | O que falta no backend |
|---|---|
| "Lembrar de mim" | Sessão de longa duração — hoje o JWT tem expiração fixa (`JWT_EXPIRE_MINUTES`), precisaria de um token de refresh ou expiração configurável por login. |
| "Esqueci minha senha" | Endpoint de recuperação (gera token de reset, envia e-mail — precisa de serviço de e-mail, hoje inexistente), + tela de redefinição. |
| Seleção múltipla no Resumo Diário → Planejamento | `POST /content/gerar` já aceita um `pauta_id` por vez; precisaria aceitar lista, ou o frontend chamar em sequência. Endpoint de "marcar pautas selecionadas" não existe (hoje pautas não têm esse estado). |
| Etapa "Publicado" | Todo o módulo de publicação automática — primeiro item do roadmap pós-v1 já documentado no spec original. |

## Testes

Validação manual, mesmo padrão já usado nas páginas atuais: `npm run build`
continua gerando `apps/web/out/` corretamente, deploy automático (GitHub
Actions → Hostinger) continua funcionando sem alteração, cada tela comparada
visualmente ao mockup fornecido.
