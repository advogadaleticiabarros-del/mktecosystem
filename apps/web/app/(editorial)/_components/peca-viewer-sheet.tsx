"use client";

import { Download, X } from "lucide-react";
import { atualizarPeca } from "../_lib/editorial-api";
import { TIPO_LABEL, imagensDaPeca, legendaDaPeca, type ContentPieceEditorial } from "../_lib/types";
import { ImageCarousel } from "./image-carousel";
import { LegendaEditor } from "./legenda-editor";
import { StatusToggle } from "./status-toggle";

export function PecaViewerSheet({
  peca,
  onFechar,
  onAtualizar,
}: {
  peca: ContentPieceEditorial;
  onFechar: () => void;
  onAtualizar: (peca: ContentPieceEditorial) => void;
}) {
  const imagens = imagensDaPeca(peca);
  const legendaAtual = legendaDaPeca(peca);

  async function salvarLegenda(novaLegenda: string) {
    // Peças do tipo "legenda" (legado) guardam o texto em `texto`; todas as
    // outras usam `legenda`. Preserva o restante do corpo (slides, imagens
    // etc.) já que o PATCH substitui o objeto inteiro.
    const chave = peca.tipo === "legenda" ? "texto" : "legenda";
    const corpoAtualizado = { ...peca.corpo, [chave]: novaLegenda } as Record<string, unknown>;
    const atualizado = await atualizarPeca(peca.id, { corpo: corpoAtualizado });
    onAtualizar(atualizado);
  }

  async function marcarPostado() {
    const atualizado = await atualizarPeca(peca.id, { status: "publicado" });
    onAtualizar(atualizado);
  }

  return (
    <div className="editorial-sheet-backdrop" onClick={onFechar}>
      <div className="editorial-sheet" onClick={(e) => e.stopPropagation()}>
        <div className="editorial-sheet-handle" />
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "4px 16px 8px",
          }}
        >
          <div style={{ fontSize: 17, fontWeight: 700 }}>{TIPO_LABEL[peca.tipo]}</div>
          <button
            type="button"
            onClick={onFechar}
            style={{
              width: 32,
              height: 32,
              borderRadius: "50%",
              background: "var(--ios-card-2)",
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--ios-label)",
            }}
            aria-label="Fechar"
          >
            <X size={16} />
          </button>
        </div>

        <div className="editorial-sheet-scroll">
          {imagens.length > 0 ? (
            <>
              <ImageCarousel imagens={imagens} alt={TIPO_LABEL[peca.tipo]} />
              <div className="editorial-action-row">
                <a
                  className="editorial-button"
                  data-variant="secondary"
                  href={imagens[0]}
                  download
                >
                  <Download size={16} />
                  Baixar imagem
                </a>
              </div>
            </>
          ) : (
            <div className="editorial-empty" style={{ padding: "24px 0" }}>
              Sem imagem gerada para esta peça ainda.
            </div>
          )}

          <LegendaEditor legendaInicial={legendaAtual} onSalvar={salvarLegenda} />

          <div className="editorial-action-row">
            <StatusToggle status={peca.status} onMarcarPostado={marcarPostado} />
          </div>
        </div>
      </div>
    </div>
  );
}
