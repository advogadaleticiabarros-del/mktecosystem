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
