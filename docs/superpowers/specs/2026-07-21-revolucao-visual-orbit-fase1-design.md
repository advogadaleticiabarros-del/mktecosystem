# Revolução Visual do Orbit — Fase 1 (Fundação)

**Data:** 2026-07-21
**Status:** Aprovado para implementação

## Contexto

O frontend do Orbit (`apps/web`, Next.js + Tailwind v4 + shadcn/ui, export estático)
tem hoje: um único tema fixo (dourado/escuro) definido em `app/globals.css`, tipografia
só-Inter em todo lugar, e quase nenhuma animação real — `framer-motion` está instalado
mas só é usado no blob orbital (`components/ambient-glow.tsx`) que aparece no login e
na visão geral. O visual geral tem a "cara de IA": cards com cantos arredondados
genéricos, sem par tipográfico, sem movimento nas interações.

A usuária pediu uma revolução visual: tirar a cara de IA, adicionar movimento de
verdade, deixar moderno e tecnológico, e poder trocar o tema de cor. Também pediu
explicitamente para melhorar a tela de login — hoje só o lado esquerdo (o blob
orbital) tem alguma vida; o lado direito (formulário) é estático e genérico.

## Escopo da Fase 1

9 telas existem no total. Fazer todas de uma vez é grande demais para um plano só.
Fase 1 entrega a **fundação** (reutilizável em todas as telas futuras) e aplica ela
completamente em 3 lugares:
1. `AppShell` (sidebar + moldura, compartilhado por 8 das 9 telas)
2. Tela de **Login** (`app/login/page.tsx`) — vitrine + correção do pedido explícito
3. Tela de **Visão Geral** (`app/(app)/visao-geral/page.tsx`) — dashboard mais
   representativo, serve de modelo para as demais

Fase 2 (spec futuro, separado): replicar o padrão da Fase 1 nas 7 telas restantes
(Planejamento, Aprovação, Calendário, Criativos, E-mails, Configurações, Avaliações).

Fora de escopo: mudar a identidade visual do **blog público** (site separado, já
tratado em outro projeto) e o Estúdio de Criativos do Instagram (pendência à parte,
já registrada).

## Decisões de design

**Critério de bom gosto:** usar as skills `ui-ux-pro-max-skill` e
`taste-design`/`artifact-design` como referência de padrões e anti-padrões — não como
ferramentas de geração automática. Especificamente evitar: gradiente roxo-azul
genérico, cards `rounded-lg` uniformes com barra de destaque lateral, tipografia
só-Inter sem hierarquia, tudo centralizado, emoji como marcador de seção.

**Tipografia:** par intencional, carregado via `next/font/google` (self-hosted no
build, sem flash de fonte):
- **Chakra Petch** para `--font-display` (títulos, `h1`/`h2`, nome "ORBIT") — geométrica,
  com caráter técnico, mas não é a escolha "óbvia de IA" (evitando deliberadamente
  Space Grotesk, que o próprio critério de bom-gosto das skills de referência marca
  como escolha "segura" genérica demais)
- **Inter** permanece para corpo de texto e UI (labels, parágrafos, botões) — já
  instalada, sem mudança
- **JetBrains Mono** para `--font-mono`, usada em números de métrica, timestamps e
  badges de status (dá a leitura "painel técnico" nos dados do dashboard)

**Vocabulário de movimento (framer-motion, já instalado):**
- Entrada em stagger dos cards/seções ao carregar a página (não simultâneo)
- Micro-interação de hover em cards e botões (leve escala/glow, não bounce)
- Números de métrica contam/incrementam ao aparecer (Visão Geral)
- Barras do gráfico semanal crescem em vez de aparecer prontas
- Transição suave ao trocar de rota (fade/slide leve entre telas)
- Tudo respeita `prefers-reduced-motion: reduce` (motion reduz/desliga)

**Sistema de temas de cor:**
- Mecanismo: `data-theme="<nome>"` na tag `<html>`, tokens redefinidos via CSS custom
  properties (o app já usa esse padrão via shadcn — só passa a ter mais de um bloco de
  valores em vez de um só fixo em `:root`/`.dark`)
- Persistência: `localStorage` (app é export estático, sem backend por trás disso;
  não precisa de coluna nova no banco)
- Troca: um `ThemeProvider` (React context) aplica o `data-theme` no `<html>` no
  primeiro render (evita flash de tema errado) e expõe um hook `useTheme()` para
  trocar
- Interface: seletor de tema (swatches) na tela de Configurações — como Configurações
  é Fase 2, a Fase 1 só entrega o motor + os 4 presets; o seletor visual entra quando
  a tela de Configurações for refeita na Fase 2. Por enquanto, o tema ativo pode ser
  trocado via um pequeno seletor temporário no rodapé do `AppShell` (visível, mas
  discreto), para a usuária já poder experimentar os temas antes da Fase 2.
- Presets iniciais: **Dourado Clássico** (o atual, vira o default), **Esmeralda**,
  **Azul Profundo**, **Violeta** — cada um redefine o mesmo conjunto de tokens
  (`--background`, `--primary`, `--card`, `--accent`, `--border`, `--sidebar`, etc.),
  mantendo o mesmo fundo escuro denso como base (identidade "dark app" preservada,
  muda o acento/realce). Adicionar um 5º tema depois é só um novo bloco de tokens.

**Login — correção específica pedida pela usuária:**
- O lado esquerdo (blob orbital, `AmbientGlow`) fica mais evidente: maior, mais
  camadas de movimento, entra com uma animação de "montagem" na primeira carga em vez
  de já aparecer pronto
- O lado direito (formulário), hoje um card estático genérico, ganha: entrada
  animada (stagger nos campos), foco em input com glow sutil na cor do tema ativo,
  botão com micro-interação de hover/loading mais viva, e tipografia do novo par
  (título com a fonte de destaque)
- Mantém a mesma estrutura de 2 colunas (não é redesenho de layout, é
  aprofundamento visual + movimento em cima da estrutura que já existe)

**Visão Geral como modelo:** aplica o novo par tipográfico, o vocabulário de
movimento (stagger, contadores, barras crescendo) e os tokens de tema nos cards
existentes — sem mudar a informação/estrutura de dados exibida, só a apresentação.

## Arquitetura

- `app/globals.css`: reestruturar os tokens de cor em blocos por tema
  (`[data-theme="dourado"]`, `[data-theme="esmeralda"]`, etc.) em vez do único bloco
  `:root, .dark` fixo atual; adicionar `--font-display` real (fonte nova via
  `next/font`) e `--font-mono` para dados.
- `components/theme-provider.tsx` (novo): contexto React + hook `useTheme()`,
  aplica/lê `data-theme` do `<html>`, persiste em `localStorage`, com um script
  inline no `<head>` (via `app/layout.tsx`) para aplicar o tema salvo antes do
  primeiro paint (evita flash).
- `components/theme-switcher.tsx` (novo): seletor temporário de swatches, usado no
  rodapé do `AppShell` nesta fase.
- `components/motion/` (novo diretório): primitivos reutilizáveis de animação
  (`StaggerList`, `CountUp`, variantes de transição de rota) para não duplicar
  configuração de easing/duration em cada tela.
- `app/login/page.tsx`, `app/(app)/visao-geral/page.tsx`, `components/app-shell.tsx`,
  `components/ambient-glow.tsx`: atualizados para consumir os novos tokens e
  primitivos de movimento.

## Testes

Este é um projeto frontend visual — não há suíte de testes automatizados de UI hoje
no `apps/web` (confirmado: não há Jest/Playwright configurado no projeto). Verificação
será manual: rodar o dev server, navegar pelas 3 telas da Fase 1, confirmar troca de
tema sem flash/bug, confirmar `prefers-reduced-motion` desliga as animações, e
confirmar `npm run build` (export estático) continua passando sem erros.
