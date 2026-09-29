"use client";

import { ChevronRight } from "lucide-react";
import Link from "next/link";
import type { PautaEditorial } from "../_lib/types";

function formatarData(iso: string | null): string {
  if (!iso) return "Sem data";
  const [ano, mes, dia] = iso.split("-");
  return `${dia}/${mes}/${ano}`;
}

export function DiaCard({
  pauta,
  totalPecas,
  pecasPostadas,
}: {
  pauta: PautaEditorial;
  totalPecas: number;
  pecasPostadas: number;
}) {
  const tudoPostado = totalPecas > 0 && pecasPostadas === totalPecas;

  return (
    <Link
      href={`/editorial/dia?id=${pauta.id}`}
      className="editorial-card-row"
      data-pressable="true"
    >
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 2 }}>
          {formatarData(pauta.data_editorial)}
        </div>
        <div
          style={{
            fontSize: 14,
            color: "var(--muted-foreground)",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {pauta.titulo}
        </div>
      </div>
      {totalPecas > 0 && (
        <span
          className="editorial-badge"
          data-tone={tudoPostado ? "done" : "progress"}
        >
          {pecasPostadas}/{totalPecas}
        </span>
      )}
      <ChevronRight size={18} color="var(--muted-foreground)" />
    </Link>
  );
}
