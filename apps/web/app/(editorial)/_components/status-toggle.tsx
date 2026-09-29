"use client";

import { Check } from "lucide-react";
import { useState } from "react";

export function StatusToggle({
  status,
  onMarcarPostado,
}: {
  status: string;
  onMarcarPostado: () => Promise<void>;
}) {
  const [pendente, setPendente] = useState(false);
  const [erro, setErro] = useState(false);
  const postado = status === "publicado";

  async function marcar() {
    if (postado || pendente) return;
    setPendente(true);
    setErro(false);
    try {
      await onMarcarPostado();
    } catch {
      setErro(true);
    } finally {
      setPendente(false);
    }
  }

  return (
    <div style={{ flex: 1 }}>
      <button
        type="button"
        className="editorial-button"
        data-variant={postado ? "success" : "primary"}
        onClick={marcar}
        disabled={postado || pendente}
        style={{ width: "100%" }}
      >
        <Check size={16} />
        {postado ? "Postado" : pendente ? "Marcando…" : "Marcar como postado"}
      </button>
      {erro && (
        <div className="editorial-status-line" style={{ color: "var(--destructive)" }}>
          Não foi possível marcar como postado. Tente de novo.
        </div>
      )}
    </div>
  );
}
