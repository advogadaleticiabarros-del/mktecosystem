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
  const [erro, setErro] = useState(false);
  const router = useRouter();

  async function carregar() {
    setCarregando(true);
    setErro(false);
    try {
      const lista = await listarPautasEditorial(dataISO(-30), dataISO(14));
      setPautas(lista);
      const entradas = await Promise.all(
        lista.map(async (pauta) => [pauta.id, await listarPecas(pauta.id)] as const),
      );
      setPecasPorPauta(Object.fromEntries(entradas));
    } catch {
      setErro(true);
    } finally {
      setCarregando(false);
    }
  }

  useEffect(() => {
    carregar();
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
        ) : erro ? (
          <div className="editorial-empty">
            Não foi possível carregar o conteúdo. Verifique sua conexão.
            <div className="editorial-action-row" style={{ maxWidth: 220, margin: "16px auto 0" }}>
              <button type="button" className="editorial-button" data-variant="secondary" onClick={carregar}>
                Tentar de novo
              </button>
            </div>
          </div>
        ) : (
          <DiaList pautas={pautas} pecasPorPauta={pecasPorPauta} />
        )}
      </main>

      <TabBar />
    </>
  );
}
