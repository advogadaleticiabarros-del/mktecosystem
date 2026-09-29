"use client";

import type { ContentPieceEditorial, PautaEditorial } from "../_lib/types";
import { DiaCard } from "./dia-card";

export function DiaList({
  pautas,
  pecasPorPauta,
}: {
  pautas: PautaEditorial[];
  pecasPorPauta: Record<string, ContentPieceEditorial[]>;
}) {
  if (pautas.length === 0) {
    return (
      <div className="editorial-empty">
        Nenhum dia de editorial encontrado nesse período.
      </div>
    );
  }

  return (
    <div className="editorial-list-section">
      <div className="editorial-list-header">Editorial da semana</div>
      <div className="editorial-card-group">
        {pautas.map((pauta) => {
          const pecas = pecasPorPauta[pauta.id] ?? [];
          const postadas = pecas.filter((p) => p.status === "publicado").length;
          return (
            <DiaCard
              key={pauta.id}
              pauta={pauta}
              totalPecas={pecas.length}
              pecasPostadas={postadas}
            />
          );
        })}
      </div>
    </div>
  );
}
