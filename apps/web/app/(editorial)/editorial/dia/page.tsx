"use client";

import { ChevronLeft } from "lucide-react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { PecaCard } from "../../_components/peca-card";
import { PecaViewerSheet } from "../../_components/peca-viewer-sheet";
import { TabBar } from "../../_components/tab-bar";
import { listarPecas } from "../../_lib/editorial-api";
import type { ContentPieceEditorial } from "../../_lib/types";

function DiaDetalheContent() {
  const searchParams = useSearchParams();
  const pautaId = searchParams.get("id") ?? "";
  const [pecas, setPecas] = useState<ContentPieceEditorial[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [pecaAberta, setPecaAberta] = useState<ContentPieceEditorial | null>(null);

  useEffect(() => {
    if (!pautaId) {
      setCarregando(false);
      return;
    }
    async function carregar() {
      try {
        const lista = await listarPecas(pautaId);
        setPecas(lista);
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, [pautaId]);

  function atualizarPecaNaLista(atualizado: ContentPieceEditorial) {
    setPecas((atual) => atual.map((p) => (p.id === atualizado.id ? atualizado : p)));
    setPecaAberta(atualizado);
  }

  return (
    <>
      <header className="editorial-nav-bar">
        <Link
          href="/editorial"
          style={{ display: "flex", alignItems: "center", gap: 2, fontSize: 15, color: "var(--ios-accent)", marginBottom: 6 }}
        >
          <ChevronLeft size={18} />
          Dias
        </Link>
        <div className="editorial-nav-title">Peças do dia</div>
      </header>

      <main className="editorial-scroll-area">
        {carregando ? (
          <div className="editorial-empty">Carregando…</div>
        ) : pecas.length === 0 ? (
          <div className="editorial-empty">Nenhuma peça registrada para este dia.</div>
        ) : (
          <div className="editorial-list-section">
            <div className="editorial-list-header">Conteúdo</div>
            <div className="editorial-card-group">
              {pecas.map((peca) => (
                <PecaCard key={peca.id} peca={peca} onAbrir={() => setPecaAberta(peca)} />
              ))}
            </div>
          </div>
        )}
      </main>

      {pecaAberta && (
        <PecaViewerSheet
          peca={pecaAberta}
          onFechar={() => setPecaAberta(null)}
          onAtualizar={atualizarPecaNaLista}
        />
      )}

      <TabBar />
    </>
  );
}

export default function DiaDetalhePage() {
  return (
    <Suspense fallback={<div className="editorial-empty">Carregando…</div>}>
      <DiaDetalheContent />
    </Suspense>
  );
}
