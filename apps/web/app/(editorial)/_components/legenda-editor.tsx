"use client";

import { Check, Copy } from "lucide-react";
import { useEffect, useRef, useState } from "react";

export function LegendaEditor({
  legendaInicial,
  onSalvar,
}: {
  legendaInicial: string;
  onSalvar: (legenda: string) => Promise<void>;
}) {
  const [legenda, setLegenda] = useState(legendaInicial);
  const [salvando, setSalvando] = useState(false);
  const [salvo, setSalvo] = useState(false);
  const [copiado, setCopiado] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    setLegenda(legendaInicial);
  }, [legendaInicial]);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  async function salvar() {
    if (legenda === legendaInicial) return;
    setSalvando(true);
    try {
      await onSalvar(legenda);
      setSalvo(true);
      setTimeout(() => setSalvo(false), 1800);
    } finally {
      setSalvando(false);
    }
  }

  async function copiar() {
    try {
      await navigator.clipboard.writeText(legenda);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 1500);
    } catch {
      // Clipboard API pode falhar fora de contexto seguro; sem fallback
      // necessário aqui pois o app roda sempre em HTTPS.
    }
  }

  return (
    <div>
      <textarea
        className="editorial-textarea"
        value={legenda}
        onChange={(e) => setLegenda(e.target.value)}
        onBlur={salvar}
        placeholder="Legenda ainda não escrita"
      />
      <div className="editorial-action-row">
        <button
          type="button"
          className="editorial-button"
          data-variant="secondary"
          onClick={copiar}
          disabled={!legenda}
        >
          {copiado ? <Check size={16} /> : <Copy size={16} />}
          {copiado ? "Copiado" : "Copiar legenda"}
        </button>
      </div>
      <div className="editorial-status-line">
        {salvando ? "Salvando…" : salvo ? "Salvo" : ""}
      </div>
    </div>
  );
}
