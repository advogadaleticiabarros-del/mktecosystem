export type PautaEditorial = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  data_editorial: string | null;
  criado_em: string;
};

export type TipoContentPiece =
  | "artigo"
  | "carrossel"
  | "legenda"
  | "stories"
  | "pergunta"
  | "frase"
  | "estatico"
  | "reels";

export type CorpoCarrossel = { slides?: string[]; imagens?: string[]; legenda?: string };
export type CorpoPergunta = { pergunta?: string; imagem?: string; legenda?: string };
export type CorpoStories = { roteiro?: string[]; imagem?: string; legenda?: string };
export type CorpoArtigo = {
  titulo?: string;
  html?: string;
  meta_description?: string;
  resumo?: string;
  imagem_capa?: string;
};
export type CorpoLegenda = { texto?: string };

export type CorpoContentPiece =
  | CorpoCarrossel
  | CorpoPergunta
  | CorpoStories
  | CorpoArtigo
  | CorpoLegenda;

export type ContentPieceEditorial = {
  id: string;
  pauta_id: string;
  tipo: TipoContentPiece;
  corpo: CorpoContentPiece;
  status: string;
  versao: number;
  criado_em: string;
};

export const TIPO_LABEL: Record<TipoContentPiece, string> = {
  carrossel: "Carrossel",
  pergunta: "Me faça uma pergunta",
  stories: "Story",
  artigo: "Blog",
  legenda: "Legenda",
  frase: "Frase",
  estatico: "Estático",
  reels: "Reels",
};

export function imagensDaPeca(piece: ContentPieceEditorial): string[] {
  const corpo = piece.corpo as Record<string, unknown>;
  if (Array.isArray(corpo.imagens)) return corpo.imagens as string[];
  if (typeof corpo.imagem === "string") return [corpo.imagem];
  if (typeof corpo.imagem_capa === "string") return [corpo.imagem_capa];
  return [];
}

export function legendaDaPeca(piece: ContentPieceEditorial): string {
  const corpo = piece.corpo as Record<string, unknown>;
  if (typeof corpo.legenda === "string") return corpo.legenda;
  if (typeof corpo.texto === "string") return corpo.texto;
  return "";
}
