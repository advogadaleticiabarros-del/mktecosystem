import { apiFetch } from "@/lib/api";
import type { ContentPieceEditorial, PautaEditorial } from "./types";

export async function listarPautasEditorial(
  dataInicio: string,
  dataFim: string,
): Promise<PautaEditorial[]> {
  const resp = await apiFetch(`/pautas?data_inicio=${dataInicio}&data_fim=${dataFim}`);
  if (!resp.ok) throw new Error("Não foi possível carregar os dias do editorial");
  return resp.json();
}

export async function listarPecas(pautaId: string): Promise<ContentPieceEditorial[]> {
  const resp = await apiFetch(`/content?pauta_id=${pautaId}`);
  if (!resp.ok) throw new Error("Não foi possível carregar as peças deste dia");
  return resp.json();
}

export async function atualizarPeca(
  pieceId: string,
  payload: { corpo?: Record<string, unknown>; status?: string },
): Promise<ContentPieceEditorial> {
  const resp = await apiFetch(`/content/${pieceId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  if (!resp.ok) throw new Error("Não foi possível salvar a alteração");
  return resp.json();
}

export async function uploadMidia(arquivo: File): Promise<{ url: string; arquivo: string }> {
  const form = new FormData();
  form.append("arquivo", arquivo);
  // Não usar apiFetch aqui: ele força Content-Type: application/json quando
  // há body, o que quebraria o multipart/form-data (o browser precisa
  // definir o boundary sozinho). Repetimos só a parte de auth do apiFetch.
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const resp = await fetch(`${apiUrl}/media/upload`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: form,
  });
  if (!resp.ok) throw new Error("Não foi possível enviar a imagem");
  return resp.json();
}
