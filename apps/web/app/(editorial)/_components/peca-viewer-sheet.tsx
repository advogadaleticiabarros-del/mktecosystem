"use client";

import { Download, X } from "lucide-react";
import { atualizarPeca } from "../_lib/editorial-api";
import { TIPO_LABEL, imagensDaPeca, legendaDaPeca, type ContentPieceEditorial } from "../_lib/types";
import { ArtigoLeitura } from "./artigo-leitura";
import { ImageCarousel } from "./image-carousel";
import { LegendaEditor } from "./legenda-editor";
import { StatusToggle } from "./status-toggle";

const TIPOS_COM_PRIMEIRO_COMENTARIO = ["carrossel", "frase", "pergunta", "estatico"];

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
  const ehArtigo = peca.tipo === "artigo";
  // Peças que viram post no feed levam o primeiro comentário do próprio perfil,
  // publicado junto pelo Orbit (docs/MANUAL_CONTEUDO_REDES.md).
  const temPrimeiroComentario = TIPOS_COM_PRIMEIRO_COMENTARIO.includes(peca.tipo);
  const primeiroComentario = String((peca.corpo as Record<string, unknown>).primeiro_comentario ?? "");
  const corpoArtigo = ehArtigo ? (peca.corpo as { html?: string; titulo?: string }) : null;

  async function salvarLegenda(novaLegenda: string) {
    // Peças do tipo "legenda" (legado) guardam o texto em `texto`; todas as
    // outras usam `legenda`. Preserva o restante do corpo (slides, imagens
    // etc.) já que o PATCH substitui o objeto inteiro.
    const chave = peca.tipo === "legenda" ? "texto" : "legenda";
    const corpoAtualizado = { ...peca.corpo, [chave]: novaLegenda } as Record<string, unknown>;
    const atualizado = await atualizarPeca(peca.id, { corpo: corpoAtualizado });
    onAtualizar(atualizado);
  }

  async function salvarPrimeiroComentario(texto: string) {
    const corpoAtualizado = { ...peca.corpo, primeiro_comentario: texto } as Record<string, unknown>;
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
              background: "var(--editorial-card-2)",
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--foreground)",
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

          {ehArtigo ? (
            <ArtigoLeitura html={corpoArtigo?.html ?? ""} titulo={corpoArtigo?.titulo} />
          ) : (
            <LegendaEditor legendaInicial={legendaAtual} onSalvar={salvarLegenda} />
          )}

          {temPrimeiroComentario && (
            <div style={{ marginTop: 16 }}>
              <div style={{ fontSize: 15, fontWeight: 700, padding: "0 0 6px" }}>Primeiro comentário</div>
              <LegendaEditor
                legendaInicial={primeiroComentario}
                onSalvar={salvarPrimeiroComentario}
                placeholder="Base legal + pergunta de conversa. O Orbit publica logo depois do post."
                rotuloCopiar="Copiar comentário"
              />
            </div>
          )}

          <div className="editorial-action-row">
            <StatusToggle status={peca.status} onMarcarPostado={marcarPostado} />
          </div>
        </div>
      </div>
    </div>
  );
}
