"use client";

import { ChevronRight } from "lucide-react";
import { TIPO_LABEL, imagensDaPeca, type ContentPieceEditorial } from "../_lib/types";

const SELO_STATUS: Record<string, { rotulo: string; tom: "done" | "pending" | "progress" }> = {
  publicado: { rotulo: "Postado", tom: "done" },
  aprovado: { rotulo: "Aprovado", tom: "done" },
  ajuste: { rotulo: "Alteração pedida", tom: "progress" },
  rascunho: { rotulo: "Aguardando você", tom: "pending" },
};

export function PecaCard({
  peca,
  onAbrir,
}: {
  peca: ContentPieceEditorial;
  onAbrir: () => void;
}) {
  const imagens = imagensDaPeca(peca);
  const selo = SELO_STATUS[peca.status] ?? SELO_STATUS.rascunho;

  return (
    <button type="button" className="editorial-card-row" data-pressable="true" onClick={onAbrir}>
      <div
        style={{
          width: 44,
          height: 44,
          borderRadius: 10,
          overflow: "hidden",
          background: "var(--editorial-card-2)",
          flexShrink: 0,
        }}
      >
        {imagens[0] && (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={imagens[0]}
            alt=""
            style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "center" }}
          />
        )}
      </div>
      <div style={{ flex: 1, textAlign: "left" }}>
        <div style={{ fontSize: 15, fontWeight: 600 }}>{TIPO_LABEL[peca.tipo]}</div>
      </div>
      <span className="editorial-badge" data-tone={selo.tom}>
        {selo.rotulo}
      </span>
      <ChevronRight size={18} color="var(--muted-foreground)" />
    </button>
  );
}
