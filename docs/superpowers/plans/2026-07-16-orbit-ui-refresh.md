# Orbit UI Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the 4 Orbit frontend pages (Login, Planejamento, Resumo
Jurídico Diário, Aprovação) to match the approved high-fidelity mockup —
persistent sidebar navigation, cards, badges, a multi-step progress
indicator, and three layers of animation — with zero backend changes.

**Architecture:** A new `AppShell` component (sidebar + header) wraps the
three authenticated pages via a Next.js route group; Login keeps its own
full-bleed layout. Every page is rebuilt with Tailwind + shadcn/ui
components already installed and verified in commit `6694011`.

**Tech Stack:** Next.js 15 (App Router, static export), Tailwind CSS v4,
shadcn/ui (base-nova/base-ui style), lucide-react, Framer Motion.

## Global Constraints

- The design-system foundation (Tailwind v4, shadcn/ui init, 6 base
  components, lucide-react, framer-motion, fonts) is **already installed
  and verified** as of commit `6694011` — no task in this plan installs
  new UI dependencies.
- Brand colors are the ones already mapped into `app/globals.css`'s
  `:root`/`.dark` block (`--background: #231e1a`, `--primary: #c9a962`,
  etc.) — use the Tailwind semantic classes (`bg-background`,
  `text-primary`, `bg-card`, etc.), never hardcode a hex value in a
  component.
- Fonts: `font-display` (Space Grotesk) for headings/wordmark, `font-sans`
  (Inter, the default) for body text — both already wired in
  `app/layout.tsx`.
- Every route's URL must stay exactly the same as today (`/login`,
  `/planejamento`, `/resumo-diario`, `/aprovacao?pautaId=`) — moving files
  into a route group must not change any URL.
- No new backend calls, no new API endpoints. Reuse `apiFetch` from
  `apps/web/lib/api.ts` exactly as the pages already do.
- Elements with no functional backend yet ("Lembrar de mim", "Esqueci
  minha senha", multi-select on Resumo Diário, the "Publicado" progress
  step) are visually present but disabled — never wired to fake behavior
  that looks real.
- `npm run build` must succeed after every task (static export is the
  deploy artifact — this is the test gate for all UI tasks in this plan,
  same pattern as the original v1 frontend tasks).

---

## File Structure

```
apps/web/
  components/
    app-shell.tsx              NEW — sidebar + header, wraps authenticated pages
    ambient-glow.tsx            NEW — CSS-only animated background (login only)
    ui/                          (already exists: button, card, badge, input, avatar, separator)
  app/
    login/page.tsx                REWRITE — hero + form, uses AmbientGlow
    (app)/                          NEW route group — no URL impact
      layout.tsx                     NEW — wraps children in AppShell
      planejamento/page.tsx           MOVED + REWRITE
      resumo-diario/page.tsx           MOVED + REWRITE
      aprovacao/page.tsx                MOVED + REWRITE
```

---

### Task 1: AppShell component + route group restructuring

**Files:**
- Create: `apps/web/components/app-shell.tsx`
- Create: `apps/web/app/(app)/layout.tsx`
- Move: `apps/web/app/planejamento/page.tsx` → `apps/web/app/(app)/planejamento/page.tsx` (content unchanged in this task — Task 3 rewrites it)
- Move: `apps/web/app/resumo-diario/page.tsx` → `apps/web/app/(app)/resumo-diario/page.tsx` (content unchanged in this task — Task 4 rewrites it)
- Move: `apps/web/app/aprovacao/page.tsx` → `apps/web/app/(app)/aprovacao/page.tsx` (content unchanged in this task — Task 5 rewrites it)

**Interfaces:**
- Produces: `AppShell` component, props `{ title: string; description?: string; headerActions?: React.ReactNode; children: React.ReactNode }` — renders the sidebar nav (highlights the active route via `usePathname()`) plus a header row (title/description left, `headerActions` + notification bell + user avatar right), with `children` below.

No automated test for this task (UI-only, matches the pattern already used for the v1 frontend pages) — verification is `npm run build` succeeding and the three routes resolving to the exact same URLs as before.

- [ ] **Step 1: Move the three page files into the `(app)` route group**

```bash
mkdir -p "apps/web/app/(app)/planejamento" "apps/web/app/(app)/resumo-diario" "apps/web/app/(app)/aprovacao"
git mv apps/web/app/planejamento/page.tsx "apps/web/app/(app)/planejamento/page.tsx"
git mv apps/web/app/resumo-diario/page.tsx "apps/web/app/(app)/resumo-diario/page.tsx"
git mv apps/web/app/aprovacao/page.tsx "apps/web/app/(app)/aprovacao/page.tsx"
rmdir apps/web/app/planejamento apps/web/app/resumo-diario apps/web/app/aprovacao 2>/dev/null || true
```

Route groups (folder names in parentheses) are excluded from the URL by
Next.js — `/planejamento` still resolves to `/planejamento`, not
`/(app)/planejamento`. Verify this assumption in Step 6.

- [ ] **Step 2: Write the AppShell component**

```tsx
// apps/web/components/app-shell.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, ClipboardList, Home, Newspaper, ShieldCheck } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/planejamento", label: "Início", icon: Home },
  { href: "/planejamento", label: "Planejamento", icon: ClipboardList },
  { href: "/resumo-diario", label: "Resumo Jurídico Diário", icon: Newspaper },
  // Aprovação requires a ?pautaId= query param to be meaningful — it isn't
  // a directly-navigable destination, but its nav icon still highlights
  // when the user is on that route. Clicking it from elsewhere sends them
  // to Planejamento, where they pick a pauta to generate content for.
  { href: "/planejamento", label: "Aprovação", icon: ShieldCheck, matchPrefix: "/aprovacao" },
] as const;

export function AppShell({
  title,
  description,
  headerActions,
  children,
}: {
  title: string;
  description?: string;
  headerActions?: React.ReactNode;
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <aside className="flex w-16 flex-col items-center gap-6 border-r border-border bg-sidebar py-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-full border border-primary/40">
          <div className="h-3 w-3 rounded-full bg-primary" />
        </div>
        <nav className="flex flex-col gap-2">
          {NAV_ITEMS.map((item) => {
            const isActive = item.matchPrefix
              ? pathname.startsWith(item.matchPrefix)
              : pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.label}
                href={item.href}
                title={item.label}
                className={cn(
                  "flex h-10 w-10 items-center justify-center rounded-lg transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                )}
              >
                <Icon className="h-5 w-5" />
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-border px-8 py-6">
          <div>
            <h1 className="font-display text-2xl font-semibold text-foreground">{title}</h1>
            {description && (
              <p className="mt-1 text-sm text-muted-foreground">{description}</p>
            )}
          </div>
          <div className="flex items-center gap-4">
            {headerActions}
            <button
              type="button"
              className="flex h-9 w-9 items-center justify-center rounded-full text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              aria-label="Notificações"
            >
              <Bell className="h-4 w-4" />
            </button>
            <Avatar className="h-9 w-9">
              <AvatarFallback className="bg-primary text-primary-foreground text-xs font-semibold">
                LB
              </AvatarFallback>
            </Avatar>
          </div>
        </header>
        <main className="flex-1 px-8 py-8">{children}</main>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Write the route group layout**

```tsx
// apps/web/app/(app)/layout.tsx
export default function AppGroupLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
```

This layout intentionally does nothing but pass children through — each
page calls `<AppShell>` itself with its own `title`/`description`/
`headerActions`, because those differ per page. A shared layout can't
express per-page header content without prop-drilling through Next.js's
layout system, so each page owning its own `AppShell` call is simpler.

- [ ] **Step 4: Confirm `avatar.tsx` exports `AvatarFallback`**

Run: `grep -n "export" apps/web/components/ui/avatar.tsx`
Expected: exports include `Avatar`, `AvatarFallback` (and likely
`AvatarImage`) — these were generated by `npx shadcn add avatar` in the
foundation commit. If `AvatarFallback` isn't exported, read the file and
adjust the import in Step 2 to match the real export names.

- [ ] **Step 5: Build to verify no import errors**

Run: `cd apps/web && npm run build`
Expected: build fails at this point with errors from the three moved
page files, because Task 1 didn't touch their content and they don't yet
import/use `AppShell` — that's expected and fixed in Tasks 3–5. Confirm
the *specific* failure is inside `planejamento/page.tsx`,
`resumo-diario/page.tsx`, or `aprovacao/page.tsx` (missing `AppShell`
usage is not required by Next.js — the actual likely failure is none,
since the moved pages are self-contained and don't reference AppShell
yet). If the build succeeds as-is, that's fine too — proceed to Step 6.

- [ ] **Step 6: Verify route URLs are unchanged**

Run: `ls apps/web/out/planejamento apps/web/out/resumo-diario apps/web/out/aprovacao`
Expected: each directory contains `index.html` (or the equivalent — check
`apps/web/out/` structure), confirming the route group didn't alter the
public URLs.

- [ ] **Step 7: Commit**

```bash
git add "apps/web/app/(app)" apps/web/components/app-shell.tsx
git commit -m "feat: add AppShell sidebar layout and (app) route group

Moves planejamento/resumo-diario/aprovacao into a route group so they
share the new sidebar navigation without changing their public URLs.
Page content is rewritten in the next three tasks."
```

---

### Task 2: Login page rebuild

**Files:**
- Create: `apps/web/components/ambient-glow.tsx`
- Rewrite: `apps/web/app/login/page.tsx`

**Interfaces:**
- Consumes: `login` and `apiFetch` from `apps/web/lib/api.ts` (unchanged
  signatures: `login(email, password) -> Promise<void>`, throws on
  non-2xx).
- Produces: `AmbientGlow` component, no props, renders a fixed-position
  decorative background (CSS-only rotating/pulsing radial shapes).

No automated test — verification is `npm run build` + manual comparison
to the mockup.

- [ ] **Step 1: Write the ambient background component**

```tsx
// apps/web/components/ambient-glow.tsx
export function AmbientGlow() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
      <div className="absolute -left-24 top-1/4 h-[420px] w-[420px] animate-[spin_40s_linear_infinite] rounded-full border border-primary/20" />
      <div className="absolute -left-40 top-1/3 h-[560px] w-[560px] animate-[spin_60s_linear_infinite_reverse] rounded-full border border-primary/10" />
      <div className="absolute left-10 top-1/2 h-2 w-2 animate-pulse rounded-full bg-primary shadow-[0_0_20px_6px_var(--primary)]" />
      <div className="absolute left-52 top-1/4 h-1.5 w-1.5 animate-pulse rounded-full bg-primary shadow-[0_0_16px_4px_var(--primary)] [animation-delay:0.6s]" />
    </div>
  );
}
```

`animate-[spin_40s_linear_infinite]` is Tailwind's arbitrary-value syntax
for a custom-duration spin — no extra `@keyframes` needed since `spin`
and `pulse` are Tailwind v4 built-ins; the arbitrary value just overrides
the default duration/timing.

- [ ] **Step 2: Rewrite the login page**

```tsx
// apps/web/app/login/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck } from "lucide-react";
import { login } from "@/lib/api";
import { AmbientGlow } from "@/components/ambient-glow";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

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
    <main className="relative flex min-h-screen bg-background text-foreground">
      <section className="relative hidden flex-1 flex-col justify-center overflow-hidden px-16 md:flex">
        <AmbientGlow />
        <div className="relative z-10 max-w-md">
          <div className="mb-10 flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full border border-primary/40">
              <div className="h-2.5 w-2.5 rounded-full bg-primary" />
            </div>
            <div>
              <p className="font-display text-lg font-semibold tracking-wide">ORBIT</p>
              <p className="text-xs text-muted-foreground">The Marketing Operating System.</p>
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
        </div>
        <p className="relative z-10 mt-16 text-xs text-muted-foreground">
          © 2026 Orbit. Todos os direitos reservados.
        </p>
      </section>

      <section className="flex flex-1 items-center justify-center px-6 py-16">
        <div className="w-full max-w-sm rounded-2xl border border-border bg-card p-8">
          <h2 className="font-display text-xl font-semibold">Bem-vinda de volta!</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Faça login para acessar sua plataforma
          </p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div>
              <label className="mb-1.5 block text-xs text-muted-foreground">E-mail</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="mb-1.5 block text-xs text-muted-foreground">Senha</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="flex items-center justify-between text-xs text-muted-foreground">
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
            </div>

            {error && <p className="text-sm text-destructive">{error}</p>}

            <Button type="submit" disabled={loading} className="w-full">
              {loading ? "Entrando..." : "Entrar na plataforma"}
            </Button>
          </form>

          <div className="mt-6 flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
            <ShieldCheck className="h-3.5 w-3.5" />
            Segurança de nível empresarial
          </div>
        </div>
      </section>
    </main>
  );
}
```

"Lembrar de mim" and "Esqueci minha senha" are rendered `disabled` — per
the spec, these have no backend counterpart yet (documented in the spec's
pending-elements table).

- [ ] **Step 3: Build and manually verify**

Run: `cd apps/web && echo "NEXT_PUBLIC_API_URL=https://mktecosystem-production.up.railway.app" > .env.local && npm run build && rm -f .env.local`
Expected: build succeeds, `/login/index.html` generated. Open
`apps/web/out/login/index.html` in a browser (or `npm run dev` and visit
`/login`) — confirm the dark hero panel with rotating gold rings on the
left, form card on the right, disabled "Lembrar de mim"/"Esqueci minha
senha" don't respond to clicks.

- [ ] **Step 4: Commit**

```bash
git add apps/web/app/login/page.tsx apps/web/components/ambient-glow.tsx
git commit -m "feat: rebuild login page to match Orbit mockup

Hero panel with animated gold rings (CSS-only, AmbientGlow component)
and headline, form card with shadcn Input/Button. 'Lembrar de mim' and
'Esqueci minha senha' are rendered disabled — no backend support yet,
documented in the design spec's pending-elements table."
```

---

### Task 3: Planejamento page rebuild

**Files:**
- Rewrite: `apps/web/app/(app)/planejamento/page.tsx`

**Interfaces:**
- Consumes: `AppShell` from Task 1, `apiFetch` from `apps/web/lib/api.ts`
  (unchanged: `GET /pautas?relevante_para_conteudo=true`,
  `POST /pautas/buscar`, `POST /pautas`), `Button`/`Card`/`Badge`/`Input`
  from `components/ui/`.

No automated test — verification is `npm run build` + manual check that
searching/creating pautas and navigating to Aprovação still work exactly
as before (only the visuals change).

- [ ] **Step 1: Rewrite the page**

```tsx
// apps/web/app/(app)/planejamento/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Newspaper, Plus, Scale, Sparkles } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";

type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  origem: string;
  fonte: string;
};

const AREA_ICON = { Previdenciário: Scale, Trabalhista: Newspaper } as const;

export default function PlanejamentoPage() {
  const [pautas, setPautas] = useState<Pauta[]>([]);
  const [loading, setLoading] = useState(false);
  const [manualTitulo, setManualTitulo] = useState("");
  const [manualAngulo, setManualAngulo] = useState("direitos");
  const [manualArea, setManualArea] = useState("Trabalhista");
  const router = useRouter();

  async function carregarSugestoes() {
    const response = await apiFetch("/pautas?relevante_para_conteudo=true");
    if (response.status === 401) {
      router.push("/login");
      return;
    }
    setPautas(await response.json());
  }

  useEffect(() => {
    carregarSugestoes();
  }, []);

  async function buscarNovasSugestoes() {
    setLoading(true);
    try {
      await apiFetch("/pautas/buscar", { method: "POST" });
      await carregarSugestoes();
    } finally {
      setLoading(false);
    }
  }

  async function criarPautaManual(event: React.FormEvent) {
    event.preventDefault();
    await apiFetch("/pautas", {
      method: "POST",
      body: JSON.stringify({ titulo: manualTitulo, angulo: manualAngulo, area: manualArea }),
    });
    setManualTitulo("");
    await carregarSugestoes();
  }

  function escolherPauta(pautaId: string) {
    router.push(`/aprovacao?pautaId=${pautaId}`);
  }

  return (
    <AppShell
      title="Planejamento"
      description="Escolha um tema ou deixe o Orbit sugerir para você"
      headerActions={
        <Button variant="outline" size="sm" onClick={() => router.push("/resumo-diario")}>
          Resumo Jurídico Diário
        </Button>
      }
    >
      <div className="mb-4 flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-primary" />
        <p className="text-sm font-medium text-primary">Sugestões para hoje</p>
      </div>

      <div className="mb-4">
        <Button onClick={buscarNovasSugestoes} disabled={loading} variant="secondary">
          {loading ? "Buscando..." : "Buscar sugestões de hoje"}
        </Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {pautas.map((pauta) => {
          const Icon = AREA_ICON[pauta.area as keyof typeof AREA_ICON] ?? Newspaper;
          return (
            <Card key={pauta.id} className="flex flex-col gap-4 p-5">
              <div className="flex items-start justify-between">
                <h3 className="font-display text-base font-semibold leading-snug">
                  {pauta.titulo}
                </h3>
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent text-primary">
                  <Icon className="h-4 w-4" />
                </div>
              </div>
              <div>
                <Badge variant="secondary" className="uppercase tracking-wide">
                  {pauta.area} ({pauta.angulo})
                </Badge>
                <p className="mt-2 text-xs text-muted-foreground">Fonte: {pauta.fonte}</p>
              </div>
              <Button onClick={() => escolherPauta(pauta.id)} className="mt-auto">
                Gerar conteúdo →
              </Button>
            </Card>
          );
        })}
      </div>

      <h2 className="mb-3 mt-8 font-display text-lg font-semibold text-primary">
        Ou digite um tema livre
      </h2>
      <form onSubmit={criarPautaManual} className="flex flex-wrap items-center gap-3">
        <Input
          placeholder="Ex: Estabilidade da gestante em contrato temporário"
          value={manualTitulo}
          onChange={(e) => setManualTitulo(e.target.value)}
          required
          className="max-w-md flex-1"
        />
        <select
          value={manualAngulo}
          onChange={(e) => setManualAngulo(e.target.value)}
          className="h-9 rounded-md border border-border bg-card px-3 text-sm"
        >
          <option value="direitos">Direitos</option>
          <option value="sinceridade">Sinceridade</option>
        </select>
        <select
          value={manualArea}
          onChange={(e) => setManualArea(e.target.value)}
          className="h-9 rounded-md border border-border bg-card px-3 text-sm"
        >
          <option>Trabalhista</option>
          <option>Previdenciário</option>
          <option>Família</option>
          <option>Consumidor</option>
        </select>
        <Button type="submit" variant="secondary">
          <Plus className="h-4 w-4" />
          Adicionar pauta
        </Button>
      </form>
    </AppShell>
  );
}
```

- [ ] **Step 2: Build and manually verify**

Run: `cd apps/web && echo "NEXT_PUBLIC_API_URL=https://mktecosystem-production.up.railway.app" > .env.local && npm run build && rm -f .env.local`
Expected: build succeeds. With the API running (or against production),
confirm the sidebar shows with Planejamento highlighted, suggestion cards
render, "Gerar conteúdo" still navigates to `/aprovacao?pautaId=...`.

- [ ] **Step 3: Commit**

```bash
git add "apps/web/app/(app)/planejamento/page.tsx"
git commit -m "feat: rebuild planejamento page with AppShell and card layout

Same data flow as before (GET/POST /pautas, POST /pautas/buscar) —
only the visuals change: suggestion cards with per-area icons and
badges, AppShell sidebar, shadcn Button/Input."
```

---

### Task 4: Resumo Jurídico Diário page rebuild

**Files:**
- Rewrite: `apps/web/app/(app)/resumo-diario/page.tsx`

**Interfaces:**
- Consumes: `AppShell` from Task 1, `apiFetch` (unchanged:
  `GET /pautas/resumo-diario`).

No automated test — verification is `npm run build` + manual check that
the digest still loads and groups by area correctly.

- [ ] **Step 1: Rewrite the page**

```tsx
// apps/web/app/(app)/resumo-diario/page.tsx
"use client";

import { useEffect, useState } from "react";
import { Calendar, ChevronRight, Users } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";

type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  fonte: string;
  relevante_para_conteudo: boolean;
};

export default function ResumoDiarioPage() {
  const [pautas, setPautas] = useState<Pauta[]>([]);

  useEffect(() => {
    apiFetch("/pautas/resumo-diario")
      .then((r) => r.json())
      .then(setPautas);
  }, []);

  const porArea = pautas.reduce<Record<string, Pauta[]>>((acc, p) => {
    (acc[p.area] ??= []).push(p);
    return acc;
  }, {});

  const candidatas = pautas.filter((p) => p.relevante_para_conteudo);

  return (
    <AppShell
      title="Resumo Jurídico Diário"
      description="Fique por dentro do que mais importa no direito hoje"
      headerActions={
        <div className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-sm text-muted-foreground">
          <Calendar className="h-4 w-4" />
          {new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "long", year: "numeric" }).format(
            new Date(),
          )}
        </div>
      }
    >
      <div className="space-y-8">
        {Object.entries(porArea).map(([area, itens]) => (
          <section key={area}>
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-primary">
              {area}
            </h2>
            <div className="divide-y divide-border rounded-xl border border-border bg-card">
              {itens.map((p) => (
                <div key={p.id} className="flex items-center justify-between px-4 py-3">
                  <p className="text-sm">
                    {p.titulo} — <span className="text-muted-foreground">fonte: {p.fonte}</span>
                  </p>
                  <div className="flex items-center gap-3">
                    {p.relevante_para_conteudo && (
                      <Badge className="bg-primary/15 text-primary hover:bg-primary/15">
                        candidato a conteúdo
                      </Badge>
                    )}
                    <ChevronRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>

      {candidatas.length > 0 && (
        <div
          className="mt-8 flex items-center justify-between rounded-xl border border-primary/30 bg-accent/40 px-5 py-4 opacity-60"
          title="Seleção múltipla ainda não é funcional — vá para Planejamento e escolha uma pauta por vez."
        >
          <div className="flex items-center gap-3">
            <Users className="h-5 w-5 text-primary" />
            <div>
              <p className="text-sm font-medium">
                {candidatas.length} {candidatas.length === 1 ? "pauta" : "pautas"} candidatas a
                conteúdo
              </p>
              <p className="text-xs text-muted-foreground">
                Acesse o planejamento para gerar conteúdo a partir delas
              </p>
            </div>
          </div>
          <span className="cursor-not-allowed rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground">
            Ir para planejamento
          </span>
        </div>
      )}
    </AppShell>
  );
}
```

The bottom banner is rendered but not interactive (`cursor-not-allowed`,
no `onClick`, wrapped in a `title` tooltip explaining why) — per the
spec, multi-select handoff to Planejamento has no backend support yet.

- [ ] **Step 2: Build and manually verify**

Run: `cd apps/web && echo "NEXT_PUBLIC_API_URL=https://mktecosystem-production.up.railway.app" > .env.local && npm run build && rm -f .env.local`
Expected: build succeeds. Confirm grouping by area still works, badge
shows only on `relevante_para_conteudo: true` items, bottom banner
appears when there's at least one candidate and doesn't navigate
anywhere when clicked.

- [ ] **Step 3: Commit**

```bash
git add "apps/web/app/(app)/resumo-diario/page.tsx"
git commit -m "feat: rebuild resumo diario page with AppShell and area grouping

Same GET /pautas/resumo-diario call as before. Adds the mockup's
multi-select summary banner as a disabled visual element — no backend
support for batch pauta selection yet."
```

---

### Task 5: Aprovação page rebuild

**Files:**
- Rewrite: `apps/web/app/(app)/aprovacao/page.tsx`

**Interfaces:**
- Consumes: `AppShell` from Task 1, `apiFetch` (unchanged:
  `POST /content/gerar`, `PATCH /content/{id}`).

No automated test — verification is `npm run build` + manual check that
generation/edit/approve/reject still work exactly as before.

- [ ] **Step 1: Rewrite the page**

```tsx
// apps/web/app/(app)/aprovacao/page.tsx
"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { CheckCircle2, ChevronLeft } from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type ContentPiece = {
  id: string;
  tipo: string;
  corpo: Record<string, unknown>;
  status: string;
};

const STEPS = [
  { key: "planejamento", label: "Planejamento", detail: "Pauta criada" },
  { key: "pesquisa", label: "Pesquisa", detail: "Fontes verificadas" },
  { key: "conteudo", label: "Conteúdo", detail: "Gerado com IA" },
  { key: "revisao", label: "Revisão", detail: "Aguardando aprovação" },
  { key: "publicado", label: "Publicado", detail: "Em breve" },
] as const;

function ProgressStepper({ activeIndex }: { activeIndex: number }) {
  return (
    <div className="flex flex-col gap-6">
      {STEPS.map((step, i) => {
        const isDone = i < activeIndex;
        const isActive = i === activeIndex;
        const isFuture = i > activeIndex;
        return (
          <div key={step.key} className="flex items-start gap-3">
            <motion.div
              initial={false}
              animate={isActive ? { scale: [1, 1.15, 1] } : {}}
              transition={{ duration: 1.4, repeat: isActive ? Infinity : 0 }}
              className={cn(
                "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2",
                isDone && "border-primary bg-primary text-primary-foreground",
                isActive && "border-primary text-primary",
                isFuture && "border-border text-muted-foreground",
              )}
            >
              {isDone ? <CheckCircle2 className="h-4 w-4" /> : i + 1}
            </motion.div>
            <div>
              <p
                className={cn(
                  "text-sm font-medium",
                  isFuture ? "text-muted-foreground" : "text-foreground",
                )}
              >
                {step.label}
              </p>
              <p className="text-xs text-muted-foreground">{step.detail}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function AprovacaoContent() {
  const searchParams = useSearchParams();
  const pautaId = searchParams.get("pautaId");
  const router = useRouter();
  const [pieces, setPieces] = useState<ContentPiece[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!pautaId) {
      setLoading(false);
      setError("Nenhuma pauta selecionada.");
      return;
    }

    apiFetch("/content/gerar", {
      method: "POST",
      body: JSON.stringify({ pauta_id: pautaId }),
    })
      .then(async (response) => {
        if (response.status === 401) {
          router.push("/login");
          return;
        }
        if (!response.ok) {
          setLoading(false);
          setError("Erro ao gerar conteúdo. Tente novamente.");
          return;
        }
        const data = await response.json();
        setPieces(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
        setError("Erro ao gerar conteúdo. Tente novamente.");
      });
  }, [pautaId, router]);

  async function atualizarStatus(pieceId: string, status: string) {
    const response = await apiFetch(`/content/${pieceId}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
    const updated = await response.json();
    setPieces((prev) => prev.map((p) => (p.id === pieceId ? updated : p)));
  }

  function editarCorpo(pieceId: string, novoCorpo: Record<string, unknown>) {
    setPieces((prev) => prev.map((p) => (p.id === pieceId ? { ...p, corpo: novoCorpo } : p)));
  }

  async function salvarEdicao(piece: ContentPiece) {
    await apiFetch(`/content/${piece.id}`, {
      method: "PATCH",
      body: JSON.stringify({ corpo: piece.corpo }),
    });
  }

  const activeIndex = loading ? 2 : error ? 1 : 3;

  return (
    <AppShell
      title="Revisar e aprovar"
      description="Confira e edite o conteúdo antes da publicação"
      headerActions={
        <Button variant="outline" size="sm" onClick={() => router.push("/planejamento")}>
          <ChevronLeft className="h-4 w-4" />
          Voltar ao planejamento
        </Button>
      }
    >
      <div className="grid gap-8 lg:grid-cols-[1fr_260px]">
        <div className="space-y-6">
          {loading && <p className="text-sm text-muted-foreground">Gerando conteúdo...</p>}
          {error && <p className="text-sm text-destructive">{error}</p>}

          {pieces.map((piece) => (
            <Card key={piece.id} className="p-5">
              <h3 className="mb-3 font-display text-base font-semibold capitalize">
                {piece.tipo}
              </h3>
              <textarea
                value={JSON.stringify(piece.corpo, null, 2)}
                onChange={(e) => {
                  try {
                    editarCorpo(piece.id, JSON.parse(e.target.value));
                  } catch {
                    // ignore invalid JSON while typing
                  }
                }}
                onBlur={() => salvarEdicao(piece)}
                rows={8}
                className="w-full rounded-md border border-border bg-background p-3 font-mono text-xs"
              />
              <div className="mt-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <p className="text-xs text-muted-foreground">Status: {piece.status}</p>
                  {piece.status !== "rascunho" && (
                    <span className="flex items-center gap-1 text-xs text-primary">
                      <CheckCircle2 className="h-3 w-3" /> Salvo automaticamente
                    </span>
                  )}
                </div>
                <div className="flex gap-2">
                  <Button size="sm" onClick={() => atualizarStatus(piece.id, "aprovado")}>
                    Aprovar
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => atualizarStatus(piece.id, "rejeitado")}
                  >
                    Rejeitar
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="rounded-xl border border-border bg-card p-5">
          <ProgressStepper activeIndex={activeIndex} />
        </div>
      </div>
    </AppShell>
  );
}

export default function AprovacaoPage() {
  return (
    <Suspense fallback={<p className="p-8 text-sm text-muted-foreground">Carregando...</p>}>
      <AprovacaoContent />
    </Suspense>
  );
}
```

The "Publicado" step (index 4) never becomes active or done — there is no
publishing module yet, so `activeIndex` only ever reaches 3 (Revisão).

- [ ] **Step 2: Build and manually verify**

Run: `cd apps/web && echo "NEXT_PUBLIC_API_URL=https://mktecosystem-production.up.railway.app" > .env.local && npm run build && rm -f .env.local`
Expected: build succeeds. With the API running, confirm generation still
triggers on load, edit/blur still saves, Aprovar/Rejeitar still update
status, the progress stepper animates its active step and never lights up
"Publicado".

- [ ] **Step 3: Commit**

```bash
git add "apps/web/app/(app)/aprovacao/page.tsx"
git commit -m "feat: rebuild aprovacao page with progress stepper and AppShell

Same generation/edit/approve/reject flow as before. Adds the 5-step
progress indicator from the mockup (Framer Motion pulse on the active
step) — 'Publicado' never activates, no publishing module exists yet."
```

---

### Task 6: Final verification pass

**Files:** none created — this task only runs checks.

- [ ] **Step 1: Full clean build**

Run: `cd apps/web && rm -rf .next out && echo "NEXT_PUBLIC_API_URL=https://mktecosystem-production.up.railway.app" > .env.local && npm run build && rm -f .env.local`
Expected: succeeds, `out/` contains `login/`, `planejamento/`,
`resumo-diario/`, `aprovacao/`, `_next/`, matching the routes that
existed before this plan.

- [ ] **Step 2: Confirm no leftover empty route folders**

Run: `ls apps/web/app/`
Expected: `login/`, `(app)/`, `layout.tsx`, `globals.css`, `page.tsx` (the
root redirect from the earlier plan) — no stray top-level
`planejamento/`, `resumo-diario/`, or `aprovacao/` folders left behind
from Task 1's `git mv`.

- [ ] **Step 3: Push and confirm the Hostinger deploy automation runs**

```bash
git push origin main
```

Then check the GitHub Actions run (`Deploy frontend to Hostinger`
workflow) completes successfully and the live site at
`https://orbit.advogadaleticiabarros.com.br/login/` shows the new design.

---

## Self-Review Notes

**Spec coverage:** all 5 blocks from `2026-07-16-orbit-ui-refresh-design.md`
map to tasks — setup/architecture (already done in commit `6694011`,
referenced as a Global Constraint), AppShell (Task 1), all 4 pages (Tasks
2–5), and the disabled-elements documentation table is honored inline in
each page's code (Task 2's login footer note, Task 4's banner tooltip,
Task 5's stepper that never reaches "Publicado") rather than a separate
file — the spec's table itself already serves as that documentation.

**Placeholder scan:** no TBD/TODO; every step has complete, real code.

**Type consistency:** `Pauta` and `ContentPiece` types are declared
per-page (matching the existing pattern in the pre-refresh pages, which
also declared local types rather than a shared `types.ts` — not
introducing a new shared-types file keeps this plan's blast radius to
exactly the 4 pages plus 2 new components). Field names (`titulo`,
`angulo`, `area`, `fonte`, `relevante_para_conteudo`, `tipo`, `corpo`,
`status`) match the API responses documented in the v1 backend plan and
already used by the pre-refresh pages — no renames.
