"use client";

import { Check, MessageSquareText } from "lucide-react";
import { useState } from "react";
import { atualizarPeca } from "../_lib/editorial-api";
import type { ContentPieceEditorial } from "../_lib/types";

type Programacao = { data?: string; hora?: string };
type PedidoAlteracao = { texto?: string; em?: string };

function quandoSai(prog: Programacao | undefined): string {
  if (!prog?.data) return "na próxima vaga do calendário";
  const [, mes, dia] = prog.data.split("-");
  return `em ${dia}/${mes}${prog.hora ? ` às ${prog.hora}` : ""}`;
}

// Aprovar agenda a peça (na data combinada em corpo.programacao, se houver);
// pedir alteração guarda o pedido na peça e tira do calendário até ser aprovada de novo.
export function AprovacaoAcoes({
  peca,
  onAtualizar,
}: {
  peca: ContentPieceEditorial;
  onAtualizar: (peca: ContentPieceEditorial) => void;
}) {
  const corpo = peca.corpo as Record<string, unknown>;
  const programacao = corpo.programacao as Programacao | undefined;
  const pedido = corpo.pedido_alteracao as PedidoAlteracao | undefined;
  const [escrevendo, setEscrevendo] = useState(false);
  const [texto, setTexto] = useState("");
  const [pendente, setPendente] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  if (peca.status === "publicado") return null;

  async function enviar(payload: { status: string; corpo?: Record<string, unknown> }, falha: string) {
    setPendente(true);
    setErro(null);
    try {
      onAtualizar(await atualizarPeca(peca.id, payload));
      setEscrevendo(false);
      setTexto("");
    } catch {
      setErro(falha);
    } finally {
      setPendente(false);
    }
  }

  const aprovar = () => enviar({ status: "aprovado" }, "Não foi possível aprovar. Tente de novo.");
  const pedirAlteracao = () =>
    enviar(
      { status: "ajuste", corpo: { ...corpo, pedido_alteracao: { texto: texto.trim(), em: new Date().toISOString() } } },
      "Não foi possível enviar o pedido. Tente de novo.",
    );

  return (
    <div style={{ marginTop: 20, display: "flex", flexDirection: "column", gap: 10 }}>
      {peca.status === "aprovado" && (
        <div className="editorial-status-line" style={{ color: "var(--primary)" }}>
          <Check size={14} style={{ verticalAlign: "-2px" }} /> Aprovada. Sai {quandoSai(programacao)}.
        </div>
      )}
      {peca.status === "ajuste" && pedido?.texto && (
        <div className="editorial-status-line">Alteração pedida: “{pedido.texto}”</div>
      )}

      {escrevendo ? (
        <>
          <textarea
            className="editorial-textarea"
            rows={4}
            autoFocus
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="O que você quer mudar? Ex.: trocar a foto da capa, mudar o título…"
          />
          <div className="editorial-action-row" style={{ margin: 0 }}>
            <button type="button" className="editorial-button" data-variant="secondary"
              onClick={() => setEscrevendo(false)} disabled={pendente} style={{ flex: 1 }}>
              Cancelar
            </button>
            <button type="button" className="editorial-button" data-variant="primary"
              onClick={pedirAlteracao} disabled={pendente || !texto.trim()} style={{ flex: 1 }}>
              {pendente ? "Enviando…" : "Enviar pedido"}
            </button>
          </div>
        </>
      ) : (
        <div className="editorial-action-row" style={{ margin: 0 }}>
          <button type="button" className="editorial-button" data-variant="secondary"
            onClick={() => setEscrevendo(true)} disabled={pendente} style={{ flex: 1 }}>
            <MessageSquareText size={16} />
            Pedir alteração
          </button>
          {peca.status !== "aprovado" && (
            <button type="button" className="editorial-button" data-variant="primary"
              onClick={aprovar} disabled={pendente} style={{ flex: 1 }}>
              <Check size={16} />
              {pendente ? "Aprovando…" : "Aprovar e agendar"}
            </button>
          )}
        </div>
      )}
      {erro && (
        <div className="editorial-status-line" style={{ color: "var(--destructive)" }}>{erro}</div>
      )}
    </div>
  );
}
