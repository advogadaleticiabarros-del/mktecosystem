import { apiFetch } from "@/lib/api";

// Regras de uma peça de conteúdo usadas pelo Editorial (celular) e pelo Estúdio de criativos:
// que mídia ela tem (vídeo do Reels ou imagens) e como aprovar ou pedir alteração.
// Aprovar agenda a peça (na data de corpo.programacao, se houver); pedir alteração guarda o
// pedido em corpo.pedido_alteracao e muda o status para "ajuste" (o Claude lê esses pedidos e
// devolve a peça refeita para "rascunho").

export type Programacao = { data?: string; hora?: string };
export type PedidoAlteracao = { texto?: string; em?: string };
export type Midia = { tipo: "video"; url: string } | { tipo: "imagens"; urls: string[] } | { tipo: "nenhuma" };

export const STATUS_PECA: Record<string, string> = {
  rascunho: "Para aprovar",
  ajuste: "Alteração pedida",
  aprovado: "Aprovado",
  publicado: "Publicado",
};

export function midiaDaPeca(corpo: Record<string, unknown>): Midia {
  if (typeof corpo.video === "string" && corpo.video) return { tipo: "video", url: corpo.video };
  if (Array.isArray(corpo.imagens) && corpo.imagens.length) return { tipo: "imagens", urls: corpo.imagens as string[] };
  if (typeof corpo.imagem === "string" && corpo.imagem) return { tipo: "imagens", urls: [corpo.imagem] };
  if (typeof corpo.imagem_capa === "string" && corpo.imagem_capa) return { tipo: "imagens", urls: [corpo.imagem_capa] };
  return { tipo: "nenhuma" };
}

export function quandoSai(prog: Programacao | undefined): string {
  if (!prog?.data) return "na próxima vaga do calendário";
  const [, mes, dia] = prog.data.split("-");
  return `em ${dia}/${mes}${prog.hora ? ` às ${prog.hora}` : ""}`;
}

async function patch<T>(id: string, payload: Record<string, unknown>): Promise<T> {
  const resp = await apiFetch(`/content/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
  if (!resp.ok) throw new Error("Não foi possível salvar a alteração");
  return resp.json();
}

export function aprovarPeca<T>(id: string): Promise<T> {
  return patch<T>(id, { status: "aprovado" });
}

export function pedirAlteracaoPeca<T>(id: string, corpo: Record<string, unknown>, texto: string): Promise<T> {
  const pedido: PedidoAlteracao = { texto: texto.trim(), em: new Date().toISOString() };
  return patch<T>(id, { status: "ajuste", corpo: { ...corpo, pedido_alteracao: pedido } });
}
