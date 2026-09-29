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
  const postado = status === "publicado";

  async function marcar() {
    if (postado || pendente) return;
    setPendente(true);
    try {
      await onMarcarPostado();
    } finally {
      setPendente(false);
    }
  }

  return (
    <button
      type="button"
      className="editorial-button"
      data-variant={postado ? "success" : "primary"}
      onClick={marcar}
      disabled={postado || pendente}
    >
      <Check size={16} />
      {postado ? "Postado" : pendente ? "Marcando…" : "Marcar como postado"}
    </button>
  );
}
