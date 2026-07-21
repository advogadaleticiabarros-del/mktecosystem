# Revolução Visual do Orbit — Fase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar ao Orbit uma fundação visual nova (tipografia, temas de cor trocáveis, vocabulário de movimento) e aplicá-la por completo no `AppShell`, na tela de Login e na tela de Visão Geral.

**Architecture:** Tokens de cor em CSS custom properties por tema (`[data-theme="..."]`), trocados via um `ThemeProvider` React que persiste em `localStorage` e aplica antes do primeiro paint via script inline. Movimento via `framer-motion` (já instalado), encapsulado em primitivos reutilizáveis (`StaggerList`, `CountUp`) para não duplicar configuração de easing/duration em cada tela.

**Tech Stack:** Next.js 15 (App Router, export estático), Tailwind v4, shadcn/ui, framer-motion, next/font/google.

## Global Constraints

- App é 100% export estático (`output: "export"`) — nada de mecanismo que dependa de servidor (sem cookies de sessão, sem API nova para tema).
- Fonte de destaque (`--font-display`) muda de Space Grotesk para **Chakra Petch** — decisão explícita da spec para fugir do "look de IA" (Space Grotesk é citada como escolha genérica demais).
- Fonte mono (`--font-mono`) nova: **JetBrains Mono**, usada em números/labels de dado.
- Inter continua como fonte de corpo/UI — sem mudança.
- 4 presets de tema nesta fase: **dourado** (default, = valores atuais), **esmeralda**, **azul**, **violeta**. Exatamente esses 4 — não adicionar mais nem menos.
- Toda animação deve respeitar `prefers-reduced-motion: reduce`.
- Sem suíte de testes automatizados de UI neste projeto — verificação é manual (dev server + build), documentada em cada task.
- Escopo desta fase: só `AppShell`, `app/login/page.tsx`, `app/(app)/visao-geral/page.tsx`, e os arquivos novos de fundação. Não mexer nas outras 6 telas (ficam para a Fase 2).

---

## File Structure

- `apps/web/app/globals.css` — reestruturado: 4 blocos de tokens por tema + `--font-mono` no `@theme inline`.
- `apps/web/app/layout.tsx` — troca de fonte (Chakra Petch + JetBrains Mono) + script inline anti-flash + `ThemeProvider`.
- `apps/web/components/theme-provider.tsx` (novo) — contexto + hook `useTheme()`.
- `apps/web/components/theme-switcher.tsx` (novo) — swatches de tema, usado no rodapé do `AppShell`.
- `apps/web/components/motion/stagger-list.tsx` (novo) — wrapper de entrada em stagger.
- `apps/web/components/motion/count-up.tsx` (novo) — número que incrementa ao aparecer.
- `apps/web/app/(app)/template.tsx` (novo) — transição de rota (fade/slide) para as telas do grupo `(app)`.
- `apps/web/components/ambient-glow.tsx` — modificado: blob maior, mais camadas, entrada animada.
- `apps/web/components/app-shell.tsx` — modificado: rodapé com `ThemeSwitcher`.
- `apps/web/app/login/page.tsx` — modificado: formulário animado, novo par tipográfico.
- `apps/web/app/(app)/visao-geral/page.tsx` — modificado: `StaggerList`, `CountUp`, barras crescendo.

---

### Task 1: Tokens de tema + tipografia nova

**Files:**
- Modify: `apps/web/app/globals.css`
- Modify: `apps/web/app/layout.tsx`

**Interfaces:**
- Produces: 4 blocos de tokens CSS selecionáveis via `[data-theme="dourado|esmeralda|azul|violeta"]` no elemento `<html>`; variável `--font-mono` disponível como utilitário `font-mono` (Tailwind v4 gera isso automaticamente a partir de `@theme inline`). Usado pelas Tasks 2, 3, 6, 7.

- [ ] **Step 1: Substituir o bloco de fontes em `layout.tsx`**

Conteúdo completo de `apps/web/app/layout.tsx`:

```tsx
import "./globals.css";
import { Chakra_Petch, Inter, JetBrains_Mono } from "next/font/google";
import { cn } from "@/lib/utils";
import { ThemeProvider } from "@/components/theme-provider";

const chakraPetch = Chakra_Petch({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["500", "600", "700"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500", "600"],
});

export const metadata = {
  title: "Orbit — The Marketing Operating System",
};

const THEME_SCRIPT = `
(function () {
  try {
    var tema = localStorage.getItem("orbit-theme") || "dourado";
    document.documentElement.setAttribute("data-theme", tema);
  } catch (e) {}
})();
`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="pt-BR"
      data-theme="dourado"
      className={cn("font-sans", chakraPetch.variable, inter.variable, jetbrainsMono.variable)}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_SCRIPT }} />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
```

Note: `data-theme="dourado"` no JSX é o fallback de build-time (evita FOUC antes do script inline rodar); o script inline sobrescreve com o valor salvo no `localStorage` assim que o `<head>` carrega, antes do primeiro paint do `<body>`. `ThemeProvider` (Task 2) ainda não existe — esse import vai quebrar o build até a Task 2 ser feita. Isso é esperado dentro desta task; a Task 2 é o próximo passo imediato do plano, então não rode `npm run build` como verificação final até completar a Task 2. Rode apenas `npm run lint` ou uma checagem de sintaxe se quiser confirmar o arquivo está bem formado antes de seguir.

- [ ] **Step 2: Reestruturar `globals.css` com os 4 temas**

Conteúdo completo de `apps/web/app/globals.css`:

```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";

@custom-variant dark (&:is(.dark *));

@theme {
  --color-fundo-escuro: #231e1a;
  --color-fundo-alt: #2e2720;
  --color-fundo-card: #352e26;
  --color-dourado: #c9a962;
  --color-dourado-dark: #b8943f;
  --color-dourado-light: #d4bc7d;
  --color-areia: #e8ded1;
  --color-areia-light: #f2ebe0;
  --color-branco: #faf6f0;
  --color-cafe: #3d2b1f;
  --color-whatsapp: #25d366;
}

body {
  background: var(--background);
  color: var(--foreground);
  font-family: "Inter", sans-serif;
  margin: 0;
}

@theme inline {
  --font-heading: var(--font-display);
  --font-display: var(--font-display);
  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);
  --color-sidebar-ring: var(--sidebar-ring);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar: var(--sidebar);
  --color-chart-5: var(--chart-5);
  --color-chart-4: var(--chart-4);
  --color-chart-3: var(--chart-3);
  --color-chart-2: var(--chart-2);
  --color-chart-1: var(--chart-1);
  --color-ring: var(--ring);
  --color-input: var(--input);
  --color-border: var(--border);
  --color-destructive: var(--destructive);
  --color-accent-foreground: var(--accent-foreground);
  --color-accent: var(--accent);
  --color-muted-foreground: var(--muted-foreground);
  --color-muted: var(--muted);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-secondary: var(--secondary);
  --color-primary-foreground: var(--primary-foreground);
  --color-primary: var(--primary);
  --color-popover-foreground: var(--popover-foreground);
  --color-popover: var(--popover);
  --color-card-foreground: var(--card-foreground);
  --color-card: var(--card);
  --color-foreground: var(--foreground);
  --color-background: var(--background);
  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) * 1.4);
  --radius-2xl: calc(var(--radius) * 1.8);
  --radius-3xl: calc(var(--radius) * 2.2);
  --radius-4xl: calc(var(--radius) * 2.6);
}

/* Orbit é sempre dark — 4 temas de cor trocáveis via [data-theme] no <html>,
   aplicado pelo ThemeProvider (persistido em localStorage). O bloco :root
   sem atributo é o fallback de build-time (= dourado) usado até o script
   inline do layout.tsx rodar. */
:root,
:root[data-theme="dourado"] {
  --background: #231e1a;
  --foreground: #e8ded1;
  --card: #352e26;
  --card-foreground: #e8ded1;
  --popover: #352e26;
  --popover-foreground: #e8ded1;
  --primary: #c9a962;
  --primary-foreground: #231e1a;
  --secondary: #2e2720;
  --secondary-foreground: #e8ded1;
  --muted: #2e2720;
  --muted-foreground: #cabfae;
  --accent: #352e26;
  --accent-foreground: #c9a962;
  --destructive: #e57373;
  --border: rgba(201, 169, 98, 0.25);
  --input: rgba(201, 169, 98, 0.25);
  --ring: #c9a962;
  --chart-1: #c9a962;
  --chart-2: #d4bc7d;
  --chart-3: #b8943f;
  --chart-4: #e8ded1;
  --chart-5: #2e2720;
  --radius: 0.75rem;
  --sidebar: #1c1712;
  --sidebar-foreground: #e8ded1;
  --sidebar-primary: #c9a962;
  --sidebar-primary-foreground: #231e1a;
  --sidebar-accent: #352e26;
  --sidebar-accent-foreground: #c9a962;
  --sidebar-border: rgba(201, 169, 98, 0.25);
  --sidebar-ring: #c9a962;
}

:root[data-theme="esmeralda"] {
  --background: #131b18;
  --foreground: #dcece3;
  --card: #1c2925;
  --card-foreground: #dcece3;
  --popover: #1c2925;
  --popover-foreground: #dcece3;
  --primary: #34c98a;
  --primary-foreground: #0d1a15;
  --secondary: #17211d;
  --secondary-foreground: #dcece3;
  --muted: #17211d;
  --muted-foreground: #a9c2b6;
  --accent: #1c2925;
  --accent-foreground: #34c98a;
  --destructive: #e57373;
  --border: rgba(52, 201, 138, 0.22);
  --input: rgba(52, 201, 138, 0.22);
  --ring: #34c98a;
  --chart-1: #34c98a;
  --chart-2: #5fd9a6;
  --chart-3: #22a36e;
  --chart-4: #dcece3;
  --chart-5: #17211d;
  --radius: 0.75rem;
  --sidebar: #0e1613;
  --sidebar-foreground: #dcece3;
  --sidebar-primary: #34c98a;
  --sidebar-primary-foreground: #0d1a15;
  --sidebar-accent: #1c2925;
  --sidebar-accent-foreground: #34c98a;
  --sidebar-border: rgba(52, 201, 138, 0.22);
  --sidebar-ring: #34c98a;
}

:root[data-theme="azul"] {
  --background: #10161f;
  --foreground: #dde6f2;
  --card: #182233;
  --card-foreground: #dde6f2;
  --popover: #182233;
  --popover-foreground: #dde6f2;
  --primary: #4d8fe0;
  --primary-foreground: #0a121c;
  --secondary: #16202e;
  --secondary-foreground: #dde6f2;
  --muted: #16202e;
  --muted-foreground: #a7b7cc;
  --accent: #182233;
  --accent-foreground: #4d8fe0;
  --destructive: #e57373;
  --border: rgba(77, 143, 224, 0.24);
  --input: rgba(77, 143, 224, 0.24);
  --ring: #4d8fe0;
  --chart-1: #4d8fe0;
  --chart-2: #7fb0ec;
  --chart-3: #3568b3;
  --chart-4: #dde6f2;
  --chart-5: #16202e;
  --radius: 0.75rem;
  --sidebar: #0b121b;
  --sidebar-foreground: #dde6f2;
  --sidebar-primary: #4d8fe0;
  --sidebar-primary-foreground: #0a121c;
  --sidebar-accent: #182233;
  --sidebar-accent-foreground: #4d8fe0;
  --sidebar-border: rgba(77, 143, 224, 0.24);
  --sidebar-ring: #4d8fe0;
}

:root[data-theme="violeta"] {
  --background: #181420;
  --foreground: #e6dff2;
  --card: #241d30;
  --card-foreground: #e6dff2;
  --popover: #241d30;
  --popover-foreground: #e6dff2;
  --primary: #a874e0;
  --primary-foreground: #180f24;
  --secondary: #211a2b;
  --secondary-foreground: #e6dff2;
  --muted: #211a2b;
  --muted-foreground: #c0b3cf;
  --accent: #241d30;
  --accent-foreground: #a874e0;
  --destructive: #e57373;
  --border: rgba(168, 116, 224, 0.24);
  --input: rgba(168, 116, 224, 0.24);
  --ring: #a874e0;
  --chart-1: #a874e0;
  --chart-2: #c29eea;
  --chart-3: #8a54c2;
  --chart-4: #e6dff2;
  --chart-5: #211a2b;
  --radius: 0.75rem;
  --sidebar: #120e19;
  --sidebar-foreground: #e6dff2;
  --sidebar-primary: #a874e0;
  --sidebar-primary-foreground: #180f24;
  --sidebar-accent: #241d30;
  --sidebar-accent-foreground: #a874e0;
  --sidebar-border: rgba(168, 116, 224, 0.24);
  --sidebar-ring: #a874e0;
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground;
  }
  html {
    @apply font-sans;
  }
}
```

- [ ] **Step 3: Commit**

```bash
cd apps/web
git add app/globals.css app/layout.tsx
git commit -m "feat: 4 temas de cor trocáveis + tipografia Chakra Petch/JetBrains Mono"
```

(Este commit deixa o build quebrado até a Task 2 existir — `ThemeProvider` ainda não foi criado. Isso é esperado; a Task 2 é o próximo passo imediato.)

---

### Task 2: `ThemeProvider` e persistência

**Files:**
- Create: `apps/web/components/theme-provider.tsx`

**Interfaces:**
- Consumes: `data-theme` attribute setado no `<html>` pelo script inline da Task 1.
- Produces: `ThemeProvider` (componente, usado em `layout.tsx`, já referenciado pela Task 1), hook `useTheme(): { tema: Tema; setTema: (t: Tema) => void }`, tipo `Tema = "dourado" | "esmeralda" | "azul" | "violeta"`. Usado pela Task 3 (`ThemeSwitcher`).

- [ ] **Step 1: Criar o provider**

```tsx
// apps/web/components/theme-provider.tsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";

export type Tema = "dourado" | "esmeralda" | "azul" | "violeta";

const TEMAS: Tema[] = ["dourado", "esmeralda", "azul", "violeta"];
const STORAGE_KEY = "orbit-theme";

type ThemeContextValue = {
  tema: Tema;
  setTema: (tema: Tema) => void;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

function lerTemaSalvo(): Tema {
  if (typeof window === "undefined") return "dourado";
  const salvo = window.localStorage.getItem(STORAGE_KEY);
  return TEMAS.includes(salvo as Tema) ? (salvo as Tema) : "dourado";
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [tema, setTemaState] = useState<Tema>("dourado");

  useEffect(() => {
    setTemaState(lerTemaSalvo());
  }, []);

  function setTema(novoTema: Tema) {
    setTemaState(novoTema);
    document.documentElement.setAttribute("data-theme", novoTema);
    window.localStorage.setItem(STORAGE_KEY, novoTema);
  }

  return (
    <ThemeContext.Provider value={{ tema, setTema }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext);
  if (context === null) {
    throw new Error("useTheme deve ser usado dentro de um ThemeProvider");
  }
  return context;
}
```

Nota de design: o `useState` inicial é sempre `"dourado"` (não lê `localStorage` na inicialização) porque o componente roda tanto no server (build do export estático) quanto no client, e `localStorage` não existe no server — ler direto na inicialização causaria erro de hidratação (server renderiza "dourado", client renderizaria outro valor na mesma passada). Em vez disso, o `useEffect` sincroniza o estado React com o que o script inline do `layout.tsx` já aplicou visualmente no DOM (via atributo) assim que o componente monta no client — não há flash porque o CSS já reflete o tema certo antes do React hidratar; o estado React só precisa alcançar a realidade do DOM para o `ThemeSwitcher` (Task 3) saber qual swatch marcar como ativo.

- [ ] **Step 2: Verificação manual**

Run: `cd apps/web && npm run dev`
Abra `http://localhost:3000/login` no navegador. Expected: a página carrega normalmente, sem erro no console sobre `ThemeProvider`/`useTheme`, tema visual permanece o dourado atual (nada mudou ainda visualmente nesta task).

- [ ] **Step 3: Commit**

```bash
cd apps/web
git add components/theme-provider.tsx
git commit -m "feat: ThemeProvider com persistência em localStorage"
```

---

### Task 3: `ThemeSwitcher` no rodapé do `AppShell`

**Files:**
- Create: `apps/web/components/theme-switcher.tsx`
- Modify: `apps/web/components/app-shell.tsx`

**Interfaces:**
- Consumes: `useTheme()`, tipo `Tema` (Task 2).
- Produces: componente `ThemeSwitcher` usado dentro do `AppShell`.

- [ ] **Step 1: Criar o seletor de temas**

```tsx
// apps/web/components/theme-switcher.tsx
"use client";

import { useTheme, type Tema } from "@/components/theme-provider";
import { cn } from "@/lib/utils";

const OPCOES: { tema: Tema; label: string; cor: string }[] = [
  { tema: "dourado", label: "Dourado Clássico", cor: "#c9a962" },
  { tema: "esmeralda", label: "Esmeralda", cor: "#34c98a" },
  { tema: "azul", label: "Azul Profundo", cor: "#4d8fe0" },
  { tema: "violeta", label: "Violeta", cor: "#a874e0" },
];

export function ThemeSwitcher() {
  const { tema, setTema } = useTheme();

  return (
    <div className="flex flex-col items-center gap-2">
      {OPCOES.map((opcao) => (
        <button
          key={opcao.tema}
          type="button"
          title={opcao.label}
          aria-label={`Tema ${opcao.label}`}
          aria-pressed={tema === opcao.tema}
          onClick={() => setTema(opcao.tema)}
          className={cn(
            "h-4 w-4 rounded-full border transition-transform hover:scale-110",
            tema === opcao.tema
              ? "border-foreground ring-2 ring-offset-2 ring-offset-sidebar ring-foreground/40"
              : "border-foreground/20",
          )}
          style={{ backgroundColor: opcao.cor }}
        />
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Adicionar ao rodapé do `AppShell`**

Em `apps/web/components/app-shell.tsx`, adicione o import no topo:

```tsx
import { ThemeSwitcher } from "@/components/theme-switcher";
```

Localize a `<aside>` da sidebar (o bloco que começa com `<aside className="flex w-16 flex-col items-center gap-6 border-r border-border bg-sidebar py-6">` e contém o `<nav>` de ícones). Adicione o `ThemeSwitcher` como último filho da `<aside>`, empurrado para o final via `mt-auto`:

```tsx
      <aside className="flex w-16 flex-col items-center gap-6 border-r border-border bg-sidebar py-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-full border border-primary/40">
          <div className="h-3 w-3 rounded-full bg-primary" />
        </div>
        <nav className="flex flex-col gap-2">
          {/* ... conteúdo existente do nav, não mudar ... */}
        </nav>
        <div className="mt-auto">
          <ThemeSwitcher />
        </div>
      </aside>
```

(Só adicione o `<div className="mt-auto"><ThemeSwitcher /></div>` logo após o `</nav>` de fechamento — não reescreva o conteúdo do `<nav>`.)

- [ ] **Step 3: Verificação manual**

Run: `cd apps/web && npm run dev`
Abra `http://localhost:3000/visao-geral` (ou qualquer tela do grupo `(app)`). Expected: 4 bolinhas de cor aparecem no rodapé da sidebar; clicar em cada uma troca instantaneamente as cores de toda a interface (fundo, cards, botões, bordas), sem reload de página; recarregar a página (F5) mantém o tema escolhido.

- [ ] **Step 4: Commit**

```bash
cd apps/web
git add components/theme-switcher.tsx components/app-shell.tsx
git commit -m "feat: seletor de tema no rodapé da sidebar"
```

---

### Task 4: Primitivos de movimento (`StaggerList`, `CountUp`) e transição de rota

**Files:**
- Create: `apps/web/components/motion/stagger-list.tsx`
- Create: `apps/web/components/motion/count-up.tsx`
- Create: `apps/web/app/(app)/template.tsx`

**Interfaces:**
- Produces:
  - `StaggerList({ children, className }: { children: React.ReactNode[]; className?: string })` — anima os filhos em sequência ao montar.
  - `CountUp({ valor, duracaoMs }: { valor: number; duracaoMs?: number })` — número que incrementa de 0 até `valor`.
  - `app/(app)/template.tsx` — aplica fade/slide leve em toda navegação dentro do grupo `(app)`.
  - Usados pela Task 7 (Visão Geral). `StaggerList`/`CountUp` também ficam disponíveis para a Fase 2.

- [ ] **Step 1: Criar `StaggerList`**

```tsx
// apps/web/components/motion/stagger-list.tsx
"use client";

import { motion, useReducedMotion } from "framer-motion";

const CONTAINER_VARIANTS = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.08 },
  },
};

const ITEM_VARIANTS = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" } },
};

export function StaggerList({
  children,
  className,
}: {
  children: React.ReactNode[];
  className?: string;
}) {
  const reduzirMovimento = useReducedMotion();

  if (reduzirMovimento) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      className={className}
      variants={CONTAINER_VARIANTS}
      initial="hidden"
      animate="show"
    >
      {children.map((child, indice) => (
        <motion.div key={indice} variants={ITEM_VARIANTS}>
          {child}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

- [ ] **Step 2: Criar `CountUp`**

```tsx
// apps/web/components/motion/count-up.tsx
"use client";

import { useEffect, useState } from "react";
import { useReducedMotion } from "framer-motion";

export function CountUp({
  valor,
  duracaoMs = 800,
}: {
  valor: number;
  duracaoMs?: number;
}) {
  const reduzirMovimento = useReducedMotion();
  const [exibido, setExibido] = useState(reduzirMovimento ? valor : 0);

  useEffect(() => {
    if (reduzirMovimento) {
      setExibido(valor);
      return;
    }

    let frameId: number;
    const inicio = performance.now();

    function passo(agora: number) {
      const progresso = Math.min(1, (agora - inicio) / duracaoMs);
      setExibido(Math.round(progresso * valor));
      if (progresso < 1) {
        frameId = requestAnimationFrame(passo);
      }
    }

    frameId = requestAnimationFrame(passo);
    return () => cancelAnimationFrame(frameId);
  }, [valor, duracaoMs, reduzirMovimento]);

  return <span className="font-mono tabular-nums">{exibido.toLocaleString("pt-BR")}</span>;
}
```

- [ ] **Step 3: Criar a transição de rota**

```tsx
// apps/web/app/(app)/template.tsx
"use client";

import { motion, useReducedMotion } from "framer-motion";

export default function Template({ children }: { children: React.ReactNode }) {
  const reduzirMovimento = useReducedMotion();

  if (reduzirMovimento) {
    return <>{children}</>;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

Nota: `template.tsx` é uma convenção do Next.js App Router — ao contrário de `layout.tsx`, ele remonta a cada navegação, então serve exatamente para animar a entrada de cada troca de rota dentro do grupo `(app)`.

- [ ] **Step 4: Verificação manual**

Run: `cd apps/web && npm run dev`
Navegue entre duas telas do grupo `(app)` (ex.: Visão Geral → Planejamento). Expected: cada troca de rota tem um fade/slide sutil de entrada, sem flash ou salto de layout.

No DevTools do navegador, ative "Emulate CSS prefers-reduced-motion: reduce" (Rendering tab). Expected: a transição de rota para de acontecer (troca instantânea).

- [ ] **Step 5: Commit**

```bash
cd apps/web
git add components/motion/ "app/(app)/template.tsx"
git commit -m "feat: primitivos de movimento (StaggerList, CountUp) e transição de rota"
```

---

### Task 5: `AmbientGlow` mais evidente

**Files:**
- Modify: `apps/web/components/ambient-glow.tsx`

**Interfaces:**
- Consumes: nada de tasks anteriores.
- Produces: mesmo componente `AmbientGlow` (sem mudança de assinatura — continua sendo usado sem props em `app/login/page.tsx`, Task 6 só ajusta o layout ao redor dele).

- [ ] **Step 1: Reescrever com mais presença e entrada animada**

Substitua o conteúdo completo de `apps/web/components/ambient-glow.tsx`:

```tsx
"use client";

import { motion, useReducedMotion } from "framer-motion";

type OrbitNodeProps = {
  ring: number;
  size: number;
  duration: number;
  reverse?: boolean;
  offset?: number;
  tether?: boolean;
};

function OrbitNode({ ring, size, duration, reverse, offset = 0, tether }: OrbitNodeProps) {
  return (
    <div
      className="absolute left-1/2 top-1/2"
      style={{ width: ring, height: ring, marginLeft: -ring / 2, marginTop: -ring / 2, transform: `rotate(${offset}deg)` }}
    >
      <div
        className="absolute inset-0"
        style={{ animation: `orbit-spin ${duration}s linear infinite${reverse ? " reverse" : ""}` }}
      >
        <div
          className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary"
          style={{ width: size, height: size, boxShadow: `0 0 ${size * 4}px ${size}px var(--primary)` }}
        >
          {tether && (
            <span
              className="absolute left-1/2 top-full -translate-x-1/2 bg-gradient-to-b from-primary/50 to-transparent"
              style={{ width: 1, height: size * 3 }}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export function AmbientGlow() {
  const reduzirMovimento = useReducedMotion();

  return (
    <motion.div
      className="pointer-events-none absolute inset-0 overflow-hidden"
      aria-hidden="true"
      initial={reduzirMovimento ? false : { opacity: 0, scale: 0.85 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.9, ease: "easeOut" }}
    >
      <style>{`
        @keyframes orbit-spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>

      <div className="absolute left-[38%] top-1/2 -translate-x-1/2 -translate-y-1/2">
        <div
          className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
          style={{
            width: 64,
            height: 64,
            background: "radial-gradient(circle at 35% 30%, color-mix(in srgb, var(--primary) 70%, white), var(--primary) 60%, color-mix(in srgb, var(--primary) 70%, black) 100%)",
            boxShadow: "0 0 90px 22px color-mix(in srgb, var(--primary) 50%, transparent)",
          }}
        />

        <div
          className="absolute left-1/2 top-1/2 h-[260px] w-[260px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/30"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/20"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[580px] w-[580px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/12"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[720px] w-[720px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/8"
        />

        <OrbitNode ring={260} size={9} duration={20} offset={20} tether />
        <OrbitNode ring={260} size={5} duration={24} offset={190} reverse />
        <OrbitNode ring={420} size={6} duration={34} offset={80} reverse />
        <OrbitNode ring={420} size={4} duration={30} offset={250} />
        <OrbitNode ring={580} size={7} duration={48} offset={140} tether />
        <OrbitNode ring={580} size={4} duration={42} offset={320} reverse />
        <OrbitNode ring={720} size={5} duration={64} offset={60} />
        <OrbitNode ring={720} size={3.5} duration={58} offset={210} reverse tether />
      </div>
    </motion.div>
  );
}
```

Mudanças em relação ao original: núcleo central maior (46px → 64px) e com glow mais forte, 4 anéis em vez de 3 (novo anel externo de 720px), 8 nós orbitando em vez de 6, cores do núcleo/nós usando `color-mix` com `var(--primary)` (acompanha o tema ativo automaticamente, não fica preso ao dourado), e uma entrada animada (fade + scale) na primeira montagem via `framer-motion`, desligada quando `prefers-reduced-motion: reduce`.

- [ ] **Step 2: Verificação manual**

Run: `cd apps/web && npm run dev`
Abra `http://localhost:3000/login`. Expected: o blob orbital é visivelmente maior e mais denso que antes, com uma entrada suave (não aparece já "pronto"), e a cor do núcleo acompanha o tema selecionado no `ThemeSwitcher` (teste trocando de tema em outra aba logada e recarregando o login, ou temporariamente ajustando `data-theme` no DevTools).

- [ ] **Step 3: Commit**

```bash
cd apps/web
git add components/ambient-glow.tsx
git commit -m "feat: AmbientGlow mais evidente, com entrada animada e cor por tema"
```

---

### Task 6: Reforma da tela de Login

**Files:**
- Modify: `apps/web/app/login/page.tsx`

**Interfaces:**
- Consumes: `AmbientGlow` (Task 5, sem mudança de uso), tipografia `--font-display`/`--font-mono` (Task 1).
- Produces: nada consumido por outras tasks (tela-folha).

- [ ] **Step 1: Reescrever a tela**

Substitua o conteúdo completo de `apps/web/app/login/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import { login } from "@/lib/api";
import { AmbientGlow } from "@/components/ambient-glow";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const CAMPO_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" } },
};

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const reduzirMovimento = useReducedMotion();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      router.push("/planejamento");
    } catch {
      setError("E-mail ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen grid-cols-1 bg-background text-foreground md:grid-cols-2">
      <section className="relative hidden flex-col items-center justify-center overflow-hidden p-10 md:flex">
        <AmbientGlow />
        <div className="relative z-10 flex w-full max-w-md flex-col">
          <div className="mb-10 flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full border border-primary/40">
              <div className="h-2.5 w-2.5 rounded-full bg-primary" />
            </div>
            <div>
              <p className="font-display text-lg font-semibold tracking-wide">ORBIT</p>
              <p className="font-mono text-xs text-muted-foreground">The Marketing Operating System.</p>
            </div>
          </div>
          <h1 className="font-display text-4xl font-semibold leading-tight">
            O centro de <br />
            todo o seu <span className="text-primary">marketing.</span>
          </h1>
          <p className="mt-4 text-muted-foreground">
            Inteligência, estratégia e automação trabalhando juntas para gerar
            resultados enquanto você foca no que importa.
          </p>
          <p className="relative z-10 mt-16 font-mono text-xs text-muted-foreground">
            © 2026 Orbit. Todos os direitos reservados.
          </p>
        </div>
      </section>

      <section className="flex items-center justify-center p-6 py-16">
        <motion.div
          className="w-full max-w-sm rounded-2xl border border-border bg-card p-8"
          initial={reduzirMovimento ? false : "hidden"}
          animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.07, delayChildren: 0.1 } } }}
        >
          <motion.h2 variants={CAMPO_VARIANTS} className="font-display text-xl font-semibold">
            Bem-vinda de volta!
          </motion.h2>
          <motion.p variants={CAMPO_VARIANTS} className="mt-1 text-sm text-muted-foreground">
            Faça login para acessar sua plataforma
          </motion.p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <motion.div variants={CAMPO_VARIANTS}>
              <label className="mb-1.5 block text-xs text-muted-foreground">E-mail</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="transition-shadow focus-visible:shadow-[0_0_0_4px_color-mix(in_srgb,var(--primary)_25%,transparent)]"
              />
            </motion.div>
            <motion.div variants={CAMPO_VARIANTS}>
              <label className="mb-1.5 block text-xs text-muted-foreground">Senha</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="transition-shadow focus-visible:shadow-[0_0_0_4px_color-mix(in_srgb,var(--primary)_25%,transparent)]"
              />
            </motion.div>

            <motion.div variants={CAMPO_VARIANTS} className="flex items-center justify-between text-xs text-muted-foreground">
              <label className="flex items-center gap-2 opacity-50">
                <input type="checkbox" disabled className="h-3.5 w-3.5" />
                Lembrar de mim
              </label>
              <button
                type="button"
                disabled
                className="cursor-not-allowed text-primary/50"
                title="Em breve"
              >
                Esqueci minha senha
              </button>
            </motion.div>

            {error && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-sm text-destructive"
              >
                {error}
              </motion.p>
            )}

            <motion.div variants={CAMPO_VARIANTS}>
              <Button type="submit" disabled={loading} className="w-full transition-transform active:scale-[0.98]">
                {loading ? "Entrando..." : "Entrar na plataforma"}
              </Button>
            </motion.div>
          </form>

          <motion.div
            variants={CAMPO_VARIANTS}
            className="mt-6 flex items-center justify-center gap-1.5 font-mono text-xs text-muted-foreground"
          >
            <ShieldCheck className="h-3.5 w-3.5" />
            Segurança de nível empresarial
          </motion.div>
        </motion.div>
      </section>
    </main>
  );
}
```

Mudanças principais em relação ao original: título "ORBIT"/tagline e rodapé de copyright passam a usar `font-mono` (reforça a leitura "painel técnico"); o card do formulário inteiro entra em stagger (título, subtítulo, cada campo, opções, botão, selo de segurança aparecem em sequência, não todos de uma vez); os dois `Input` ganham um glow sutil na cor do tema ativo (`var(--primary)`) ao receber foco; o botão de submit ganha uma leve compressão (`active:scale-[0.98]`) ao ser clicado.

- [ ] **Step 2: Verificação manual**

Run: `cd apps/web && npm run dev`
Abra `http://localhost:3000/login` em uma aba anônima/recarregada (para ver a animação de entrada do zero). Expected: o card do formulário monta em sequência visível (não tudo de uma vez), clicar em um campo de input mostra um glow na cor do tema, o botão "Entrar na plataforma" comprime levemente ao ser clicado. Ative "Emulate prefers-reduced-motion: reduce" no DevTools e recarregue — Expected: o card aparece direto, sem sequência de entrada.

- [ ] **Step 3: Commit**

```bash
cd apps/web
git add app/login/page.tsx
git commit -m "feat: reforma visual da tela de login (movimento, tipografia, glow de foco)"
```

---

### Task 7: Reforma da tela de Visão Geral

**Files:**
- Modify: `apps/web/app/(app)/visao-geral/page.tsx`

**Interfaces:**
- Consumes: `StaggerList`, `CountUp` (Task 4), tipografia `--font-mono` (Task 1).
- Produces: nada consumido por outras tasks (tela-folha).

- [ ] **Step 1: Ler o arquivo atual antes de editar**

Leia `apps/web/app/(app)/visao-geral/page.tsx` por completo (438 linhas) antes de fazer qualquer alteração — este arquivo já tem lógica de fetch de dados (`Resumo` type, `apiFetch`), um componente `BarrasSemanais` customizado, e vários cards de métricas. As mudanças abaixo são cirúrgicas em cima dessa estrutura existente, não uma reescrita.

- [ ] **Step 2: Envolver a grade de cards principais em `StaggerList`**

Localize o(s) trecho(s) onde os cards de métrica (`<Card>...</Card>`) são renderizados dentro de um contêiner `<div className="grid ...">` (a grade principal de métricas da página, tipicamente logo abaixo do cabeçalho). Envolva os elementos `<Card>` desse grid com `StaggerList` no lugar da `<div>` de grid pura — mova as classes de grid (`grid grid-cols-...gap-...`) do `<div>` original para a prop `className` do `StaggerList`, e passe os `<Card>` como um array de filhos (`.map(...)` já deve estar retornando isso naturalmente se a grade é gerada a partir de uma lista; se os cards forem literais fixos no JSX, envolva-os em um array explícito `{[<Card key="a">...</Card>, <Card key="b">...</Card>, ...]}`).

Adicione o import no topo do arquivo:

```tsx
import { StaggerList } from "@/components/motion/stagger-list";
import { CountUp } from "@/components/motion/count-up";
```

- [ ] **Step 3: Trocar números de métrica estáticos por `CountUp`**

Onde a página hoje renderiza um número bruto de métrica como texto (ex.: `{resumo.contatos_ativos}`, `{resumo.emails_enviados}`, `{resumo.pautas_total}`, contadores de `conteudos_por_status`/`contatos_por_origem`, e os valores de `instagram`/`google_business` quando não-nulos), troque a interpolação direta pelo componente:

```tsx
<CountUp valor={resumo.contatos_ativos} />
```

(mesma troca para cada número de métrica exibido na página — sempre `<CountUp valor={numeroExistente} />` no lugar de `{numeroExistente}`, mantendo o texto/label ao redor exatamente como está).

- [ ] **Step 4: Animar as barras do gráfico semanal para crescerem**

Dentro do componente `BarrasSemanais` (já existente no arquivo, usa `alturaMax`/`teto` para calcular a altura de cada barra em pixels), localize onde a altura calculada é aplicada como `style={{ height: ... }}` (ou `style={{ height: alturaPx }}`) no elemento da barra. Envolva esse elemento com `motion.div` (import `motion` de `"framer-motion"` no topo do arquivo) e anime a altura de `0` até o valor calculado:

```tsx
<motion.div
  initial={{ height: 0 }}
  animate={{ height: alturaPx }}
  transition={{ duration: 0.5, ease: "easeOut" }}
  // ... manter todas as outras props/classes que já existiam no elemento original
/>
```

(Substitua `alturaPx` pelo nome real da variável de altura já usada no arquivo — não invente um novo nome, use o que `BarrasSemanais` já calcula.) `framer-motion` respeita `prefers-reduced-motion` automaticamente para animações de layout como essa quando `useReducedMotion()` está em uso em outros componentes da árvore, mas para garantir aqui especificamente, adicione a mesma guarda usada nas tasks anteriores: se `useReducedMotion()` retornar `true`, renderize a barra com `<div style={{ height: alturaPx }}>` (sem `motion`) em vez do `motion.div` animado.

- [ ] **Step 5: Aplicar `font-mono` em timestamps e badges de status**

Onde a página renderiza datas/horários (`data_agendada`, `horario` dos `proximos_agendamentos`) ou badges de status (`<Badge>`), adicione a classe `font-mono` a esses elementos de texto especificamente (não ao texto de prosa/labels ao redor) — reforça a leitura "painel de dados" pedida na spec.

- [ ] **Step 5.1: Micro-interação de hover nos cards de métrica**

Nos `<Card>` do grid principal de métricas (os mesmos envolvidos pelo `StaggerList` no Step 2), adicione classes de transição de hover diretamente no `className` de cada `<Card>`:

```tsx
className="transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_0_0_1px_var(--primary),0_8px_24px_-8px_color-mix(in_srgb,var(--primary)_35%,transparent)]"
```

(Combine com as classes que o `<Card>` já tiver — não substitua, concatene. Se algum `<Card>` já tiver uma prop `className` com outras classes, mantenha-as e apenas acrescente estas.) Isso dá a leve elevação + glow na cor do tema ativo pedida na spec ("leve escala/glow, não bounce") sem precisar alterar o componente `Card` compartilhado (`components/ui/card.tsx`), que outras telas ainda não revisadas na Fase 2 também usam.

- [ ] **Step 6: Verificação manual**

Run: `cd apps/web && npm run dev`
Abra `http://localhost:3000/visao-geral` logado. Expected: os cards de métrica aparecem em sequência (stagger) ao carregar a página, não todos de uma vez; os números de métrica contam de 0 até o valor final; as barras do gráfico semanal crescem de baixo para cima ao carregar, em vez de aparecerem já no tamanho final; datas/badges de status usam a fonte mono; passar o mouse sobre um card de métrica eleva ele levemente com um glow na cor do tema ativo.

- [ ] **Step 7: Commit**

```bash
cd apps/web
git add "app/(app)/visao-geral/page.tsx"
git commit -m "feat: reforma visual da Visão Geral (stagger, contadores, barras animadas)"
```

---

### Task 8: Verificação final e build

**Files:** nenhum arquivo novo — esta task só verifica o resultado acumulado das Tasks 1-7.

- [ ] **Step 1: Build de produção (export estático)**

Run: `cd apps/web && npm run build`
Expected: build completa sem erros, gera a pasta `out/` normalmente (o projeto já usa `output: "export"` — confirme que não há erro relacionado a `next/font` ou aos novos componentes client-only).

- [ ] **Step 2: Checklist visual manual dos 4 temas**

Run: `cd apps/web && npm run dev`, abra `/login` e `/visao-geral`.
Para cada um dos 4 temas (clicar em cada swatch do `ThemeSwitcher` na Visão Geral, e checar o Login recarregando a página depois de trocar):
- [ ] Contraste de texto continua legível (nenhum texto quase invisível sobre o fundo)
- [ ] `AmbientGlow` no login reflete a cor do tema ativo
- [ ] Recarregar a página (F5) mantém o tema escolhido

- [ ] **Step 3: Checklist de `prefers-reduced-motion`**

No DevTools, ative "Emulate CSS prefers-reduced-motion: reduce" e repita a navegação por `/login` → `/visao-geral` → outra tela do grupo `(app)`.
Expected: nenhuma animação de entrada/stagger/contagem/crescimento de barra acontece; a interface aparece direto no estado final, mas continua funcional (nada quebra, nada fica invisível por depender de uma animação que não rodou).

- [ ] **Step 4: Reportar findings, se houver**

Se qualquer item dos checklists acima falhar, corrija antes de considerar a Fase 1 completa — não há próxima task depois desta; esta é a última verificação antes da revisão final da branch.
