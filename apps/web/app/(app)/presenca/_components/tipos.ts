export type ErroSecao = { tipo: string; mensagem: string; ativar_em: string | null };

export type Servico = { nome: string; descricao: string };

export type Perfil = {
  titulo: string;
  descricao: string;
  categoria_principal: string;
  categorias_adicionais: string[];
  telefone: string;
  telefones_extras: string[];
  site: string;
  endereco: string;
  cidade: string;
  area_atendimento: string[];
  horarios: { dia: string; abre: string; fecha: string }[];
  servicos: Servico[];
  servicos_padrao?: string[];
  maps_uri: string | null;
  link_avaliar: string | null;
  status: string | null;
  aberto_desde: string | null;
};

export type PontoDesempenho = {
  data: string;
  buscas: number;
  maps: number;
  ligacoes: number;
  rotas: number;
  cliques_site: number;
  conversas: number;
  agendamentos: number;
};
export type TotaisDesempenho = Omit<PontoDesempenho, "data">;

export type Avaliacao = {
  name: string;
  autor: string;
  foto_autor: string | null;
  nota: number;
  comentario: string;
  criada_em: string | null;
  resposta: string | null;
  respondida_em: string | null;
};

export type PostGoogle = {
  name: string;
  tipo: string;
  texto: string;
  criado_em: string | null;
  estado: string | null;
  link: string | null;
  imagem: string | null;
};

export type Consulta = { termo: string; cliques: number; impressoes: number; ctr: number; posicao: number };
export type PaginaGsc = { pagina: string; cliques: number; impressoes: number; ctr: number; posicao: number };

export type Painel = {
  coletado_em: string;
  dominio: string | null;
  erros: Record<string, ErroSecao>;
  perfil: Perfil | null;
  atributos: Record<string, unknown> | null;
  desempenho: { serie: PontoDesempenho[]; totais_30d: TotaisDesempenho; totais_30d_anterior: TotaisDesempenho } | null;
  palavras_chave: { termo: string; valor: number | null; abaixo_de: number | null }[] | null;
  avaliacoes: { media: number | null; total: number; sem_resposta: number; ultimos_30d: number; lista: Avaliacao[] } | null;
  posts: { total: number; ultimo_em: string | null; ultimos_30d: number; lista: PostGoogle[] } | null;
  midia: {
    total: number;
    fotos: number;
    videos: number;
    ultima_em: string | null;
    por_categoria: Record<string, number>;
    recentes: { name: string; url: string; criada_em: string }[];
  } | null;
  verificacao: Record<string, unknown> | null;
  botoes: { name: string; tipo: string; url: string }[] | null;
  analytics: {
    propriedade: string;
    nome: string;
    serie: { data: string; sessoes: number; usuarios: number; conversoes: number }[];
    totais_30d: { sessoes: number; usuarios: number; conversoes: number };
    totais_30d_anterior: { sessoes: number; usuarios: number; conversoes: number };
    paginas: { host: string; caminho: string; secao: string; visualizacoes: number; sessoes: number }[];
    por_secao: Record<string, number>;
    origens: { origem: string; meio: string; sessoes: number }[];
    ia: { total_90d: number; por_fonte: { fonte: string; sessoes: number }[] };
  } | null;
  search_console: {
    site: string;
    serie: { data: string; cliques: number; impressoes: number; posicao: number }[];
    totais_28d: { cliques: number; impressoes: number; ctr: number; posicao: number };
    totais_28d_anterior: { cliques: number; impressoes: number; ctr: number; posicao: number };
    consultas: Consulta[];
    paginas: PaginaGsc[];
  } | null;
  site?: {
    dominio: string;
    home: { titulo: string | null; descricao: string | null; schemas: string[]; tem_analytics: boolean };
    robots_txt: boolean;
    robos_ia_bloqueados: string[];
    llms_txt: boolean;
    sitemap: { ok: boolean; paginas: number };
    paginas_html: number;
    paginas_sem_analytics: string[];
    paginas_sem_descricao: string[];
  } | null;
  sitemap_enviado?: boolean;
};

export type Recomendacao = {
  chave: string;
  area: string;
  prioridade: "alta" | "media" | "baixa";
  titulo: string;
  motivo: string;
  acao: string;
  itens: string[];
  link: string | null;
  aplicar: "editar_perfil" | "responder_avaliacoes" | "criar_post" | "enviar_fotos" | null;
  status: "pendente" | "feita" | "ignorada";
};

export type RespostaPainel = { painel: Painel | null; coletado_em: string | null; recomendacoes: Recomendacao[] };

export type ProblemaOab = { trecho: string; motivo: string; nivel: "bloqueia" | "atencao" };

export type PostOrbit = {
  id: string;
  texto: string;
  botao: string | null;
  link: string | null;
  imagem_url: string | null;
  publicar_em: string;
  status: "rascunho" | "aprovado" | "publicado" | "erro";
  link_publicado: string | null;
  erro: string | null;
  criado_em: string;
  problemas: ProblemaOab[];
};

export type Aba = "resumo" | "melhorias" | "perfil" | "avaliacoes" | "posts" | "buscas" | "site";

export const numero = (n: number | null | undefined) => (n ?? 0).toLocaleString("pt-BR");

export function dataCurta(iso: string | null | undefined) {
  if (!iso) return "—";
  const [a, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${a}`;
}

export function variacao(atual: number, anterior: number): number | null {
  if (!anterior) return null;
  return Math.round((atual / anterior - 1) * 100);
}

/* Lê o detalhe de erro da API (texto, ou objeto com mensagem e problemas da OAB). */
export async function lerErro(resp: Response): Promise<{ mensagem: string; problemas: ProblemaOab[] }> {
  const corpo = await resp.json().catch(() => null);
  const detalhe = corpo?.detail;
  if (typeof detalhe === "string") return { mensagem: detalhe, problemas: [] };
  if (detalhe?.mensagem) return { mensagem: detalhe.mensagem, problemas: detalhe.problemas ?? [] };
  return { mensagem: "Não foi possível concluir. Tente de novo.", problemas: [] };
}
