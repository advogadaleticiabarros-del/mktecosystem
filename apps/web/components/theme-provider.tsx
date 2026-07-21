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
