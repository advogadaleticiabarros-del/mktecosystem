export type Kpi = { chave: string; rotulo: string; valor: number; explicacao: string };
export type PostRanking = {
  media_id: string;
  data: string;
  formato: string;
  area: string;
  legenda: string;
  permalink: string | null;
  alcance: number;
  interacoes: number;
  compartilhamentos: number;
  salvamentos: number;
  seguidores_ganhos: number;
};
export type ItemFormato = {
  formato: string;
  posts: number;
  alcance_tipico: number;
  interacoes_tipicas: number;
  compartilhamentos: number;
  salvamentos: number;
  seguidores_ganhos: number;
};
export type ItemPublico = { rotulo: string; valor: number; pct: number };

export type Analise = {
  atualizado_em: string | null;
  total_posts: number;
  resumo: { kpis: Kpi[]; texto: string };
  alcance_diario: {
    serie: { data: string; valor: number }[];
    media: number;
    pico: { data: string; valor: number } | null;
    explicacao: string;
  };
  formatos: { itens: ItemFormato[]; explicacao: string; periodo?: string };
  areas: { itens: { area: string; posts: number; alcance_tipico: number }[]; explicacao: string };
  horarios: { itens: { hora: number; posts: number; alcance_tipico: number }[]; explicacao: string };
  dias_semana: { itens: { dia: string; posts: number; alcance_tipico: number }[]; explicacao: string };
  volume_mensal: { itens: { mes: string; rotulo: string; posts: number; alcance_medio: number }[]; explicacao: string };
  ranking: {
    alcance: PostRanking[];
    interacoes: PostRanking[];
    compartilhamentos: PostRanking[];
    seguidores: PostRanking[];
    explicacao: string;
  };
  publico: { genero: ItemPublico[]; idade: ItemPublico[]; cidades: ItemPublico[]; explicacao: string };
  recomendacoes: string[];
};

export const COR_FORMATO: Record<string, string> = {
  Reels: "var(--fmt-reels)",
  Carrossel: "var(--fmt-carrossel)",
  Imagem: "var(--fmt-imagem)",
};

export const numero = (n: number) => n.toLocaleString("pt-BR");

export function dataCurta(iso: string) {
  const [, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}`;
}
