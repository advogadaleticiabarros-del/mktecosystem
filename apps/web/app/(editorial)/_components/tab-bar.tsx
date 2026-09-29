"use client";

import { CalendarDays, Settings2 } from "lucide-react";
import { usePathname } from "next/navigation";
import Link from "next/link";

const TABS = [{ href: "/editorial", label: "Dias", icon: CalendarDays }] as const;

export function TabBar() {
  const pathname = usePathname();

  return (
    <nav className="editorial-tab-bar">
      {TABS.map((tab) => {
        const Icon = tab.icon;
        const active = pathname === tab.href || pathname.startsWith(`${tab.href}/`);
        return (
          <Link key={tab.href} href={tab.href} className="editorial-tab-item" data-active={active}>
            <Icon size={22} strokeWidth={active ? 2.4 : 1.8} />
            <span>{tab.label}</span>
          </Link>
        );
      })}
      <div className="editorial-tab-item" data-active="false">
        <Settings2 size={22} strokeWidth={1.8} />
        <span>Ajustes</span>
      </div>
    </nav>
  );
}
