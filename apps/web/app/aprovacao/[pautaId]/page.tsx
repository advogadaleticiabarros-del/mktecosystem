// apps/web/app/aprovacao/[pautaId]/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { apiFetch } from "@/lib/api";

type ContentPiece = {
  id: string;
  tipo: string;
  corpo: Record<string, unknown>;
  status: string;
};

export default function AprovacaoPage() {
  const { pautaId } = useParams<{ pautaId: string }>();
  const [pieces, setPieces] = useState<ContentPiece[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch("/content/gerar", {
      method: "POST",
      body: JSON.stringify({ pauta_id: pautaId }),
    })
      .then((r) => r.json())
      .then((data) => {
        setPieces(data);
        setLoading(false);
      });
  }, [pautaId]);

  async function atualizarStatus(pieceId: string, status: string) {
    const response = await apiFetch(`/content/${pieceId}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
    const updated = await response.json();
    setPieces((prev) => prev.map((p) => (p.id === pieceId ? updated : p)));
  }

  function editarCorpo(pieceId: string, novoCorpo: Record<string, unknown>) {
    setPieces((prev) => prev.map((p) => (p.id === pieceId ? { ...p, corpo: novoCorpo } : p)));
  }

  async function salvarEdicao(piece: ContentPiece) {
    await apiFetch(`/content/${piece.id}`, {
      method: "PATCH",
      body: JSON.stringify({ corpo: piece.corpo }),
    });
  }

  if (loading) {
    return <p style={{ margin: 40 }}>Gerando conteúdo...</p>;
  }

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ color: "var(--dourado)" }}>Revisar e aprovar</h1>
      {pieces.map((piece) => (
        <section key={piece.id} style={{ marginBottom: 32, borderBottom: "1px solid var(--areia)" }}>
          <h2 style={{ textTransform: "capitalize" }}>{piece.tipo}</h2>
          <textarea
            value={JSON.stringify(piece.corpo, null, 2)}
            onChange={(e) => {
              try {
                editarCorpo(piece.id, JSON.parse(e.target.value));
              } catch {
                // ignore invalid JSON while typing
              }
            }}
            onBlur={() => salvarEdicao(piece)}
            rows={8}
            style={{ width: "100%", fontFamily: "monospace" }}
          />
          <p>Status: {piece.status}</p>
          <button onClick={() => atualizarStatus(piece.id, "aprovado")}>Aprovar</button>
          <button onClick={() => atualizarStatus(piece.id, "rejeitado")} style={{ marginLeft: 8 }}>
            Rejeitar
          </button>
        </section>
      ))}
    </main>
  );
}
