"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { DiaList } from "../_components/dia-list";
import { TabBar } from "../_components/tab-bar";
import { listarPautasEditorial, listarPecas } from "../_lib/editorial-api";
import type { ContentPieceEditorial, PautaEditorial } from "../_lib/types";

function dataISO(offsetDias: number): string {
  const d = new Date();
  d.setDate(d.getDate() + offsetDias);
  return d.toISOString().slice(0, 10);
}

export default function EditorialPage() {
  const [pautas, setPautas] = useState<PautaEditorial[]>([]);
  const [pecasPorPauta, setPecasPorPauta] = useState<Record<string, ContentPieceEditorial[]>>({});
  const [carregando, setCarregando] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function carregar() {
      try {
        const lista = await listarPautasEditorial(dataISO(-30), dataISO(14));
        setPautas(lista);
        const entradas = await Promise.all(
          lista.map(async (pauta) => [pauta.id, await listarPecas(pauta.id)] as const),
        );
        setPecasPorPauta(Object.fromEntries(entradas));
      } catch {
        // Se o token expirou, a próxima navegação normal do usuário já vai
        // cair no /login via apiFetch nas outras telas; aqui só evita
        // travar a tela em estado de carregando infinito.
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, [router]);

  return (
    <>
      <header className="editorial-nav-bar">
        <div className="editorial-nav-title">Editorial</div>
        <div className="editorial-nav-subtitle">Conteúdo diário pronto pra postar</div>
      </header>

      <main className="editorial-scroll-area">
        {carregando ? (
          <div className="editorial-empty">Carregando…</div>
        ) : (
          <DiaList pautas={pautas} pecasPorPauta={pecasPorPauta} />
        )}
      </main>

      <TabBar />
    </>
  );
}
