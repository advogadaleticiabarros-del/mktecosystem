"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bell,
  CalendarDays,
  ClipboardList,
  Home,
  ImageIcon,
  Mail,
  Newspaper,
  ShieldCheck,
} from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/visao-geral", label: "Visão geral", icon: Home },
  { href: "/planejamento", label: "Planejamento", icon: ClipboardList },
  { href: "/resumo-diario", label: "Resumo Jurídico Diário", icon: Newspaper },
  // Aprovação requires a ?pautaId= query param to be meaningful — it isn't
  // a directly-navigable destination, but its nav icon still highlights
  // when the user is on that route. Clicking it from elsewhere sends them
  // to Planejamento, where they pick a pauta to generate content for.
  { href: "/planejamento", label: "Aprovação", icon: ShieldCheck, matchPrefix: "/aprovacao" },
  { href: "/calendario", label: "Calendário editorial", icon: CalendarDays },
  { href: "/criativos", label: "Estúdio de criativos", icon: ImageIcon },
  { href: "/emails", label: "E-mails", icon: Mail },
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
            const matchPrefix = "matchPrefix" in item ? item.matchPrefix : undefined;
            const isActive = matchPrefix
              ? pathname.startsWith(matchPrefix)
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
