"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, ArrowDownRight, ArrowUpRight, ExternalLink, ShieldAlert } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { numero, variacao, type ErroSecao, type ProblemaOab } from "./tipos";

export function Kpi({
  rotulo,
  valor,
  anterior,
  sufixo,
  ajuda,
}: {
  rotulo: string;
  valor: number | string;
  anterior?: number;
  sufixo?: string;
  ajuda?: string;
}) {
  const v = typeof valor === "number" && anterior !== undefined ? variacao(valor, anterior) : null;
  return (
    <Card className="p-4 hover:translate-y-0" title={ajuda}>
      <p className="text-xs text-muted-foreground">{rotulo}</p>
      <p className="mt-1 font-display text-2xl font-semibold tracking-tight">
        {typeof valor === "number" ? numero(valor) : valor}
        {sufixo && <span className="ml-1 text-sm font-normal text-muted-foreground">{sufixo}</span>}
      </p>
      {v !== null && (
        <p className={`mt-1 flex items-center gap-0.5 text-xs ${v >= 0 ? "text-emerald-500" : "text-destructive"}`}>
          {v >= 0 ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
          {v > 0 ? "+" : ""}
          {v}% vs. período anterior
        </p>
      )}
    </Card>
  );
}

const TEXTO_ERRO: Record<string, string> = {
  api_desativada: "A API dessa parte não está ativada no Google Cloud.",
  reconectar: "A conexão do Google não tem permissão para essa parte. Reconecte na Visão Geral marcando todas as caixas.",
  sem_acesso: "A conta Google conectada não tem acesso a isso.",
  nao_encontrado: "O Google não encontrou esse recurso.",
  falha: "O Google não respondeu como esperado.",
};

export function AvisoSecao({ erro, nome }: { erro?: ErroSecao; nome: string }) {
  if (!erro) return null;
  return (
    <Card className="border-l-2 border-amber-500 p-4 text-sm hover:translate-y-0">
      <p className="flex items-center gap-2 font-medium">
        <AlertTriangle className="h-4 w-4 text-amber-500" /> {nome}: dados indisponíveis
      </p>
      <p className="mt-1 text-muted-foreground">{TEXTO_ERRO[erro.tipo] ?? erro.mensagem}</p>
      {erro.ativar_em && (
        <a href={erro.ativar_em} target="_blank" rel="noreferrer" className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline">
          Ativar no Google Cloud <ExternalLink className="h-3 w-3" />
        </a>
      )}
      {erro.tipo !== "api_desativada" && erro.tipo !== "reconectar" && (
        <p className="mt-1 text-xs text-muted-foreground/80">{erro.mensagem}</p>
      )}
    </Card>
  );
}

export function ListaOab({ problemas }: { problemas: ProblemaOab[] }) {
  if (!problemas.length) return null;
  return (
    <ul className="space-y-1 rounded-md border border-amber-500/40 bg-amber-500/5 p-3 text-xs">
      {problemas.map((p, i) => (
        <li key={i} className="flex gap-2">
          <ShieldAlert className={`mt-0.5 h-3.5 w-3.5 shrink-0 ${p.nivel === "bloqueia" ? "text-destructive" : "text-amber-500"}`} />
          <span>
            <strong>&ldquo;{p.trecho}&rdquo;</strong> {p.motivo}
            {p.nivel === "bloqueia" && <span className="ml-1 text-destructive">(impede publicar)</span>}
          </span>
        </li>
      ))}
    </ul>
  );
}

/* Caixa de texto que confere as regras da OAB enquanto a usuária digita. */
export function TextoComOab({
  valor,
  aoMudar,
  linhas = 5,
  limite,
  contexto = "geral",
  placeholder,
  aoConferir,
}: {
  valor: string;
  aoMudar: (v: string) => void;
  linhas?: number;
  limite?: number;
  contexto?: "geral" | "resposta_avaliacao";
  placeholder?: string;
  aoConferir?: (problemas: ProblemaOab[]) => void;
}) {
  const [problemas, setProblemas] = useState<ProblemaOab[]>([]);

  useEffect(() => {
    if (!valor.trim()) {
      setProblemas([]);
      aoConferir?.([]);
      return;
    }
    const t = setTimeout(async () => {
      const resp = await apiFetch("/presenca/conferir-oab", {
        method: "POST",
        body: JSON.stringify({ texto: valor, contexto }),
      });
      if (resp.ok) {
        const dados = (await resp.json()).problemas as ProblemaOab[];
        setProblemas(dados);
        aoConferir?.(dados);
      }
    }, 500);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [valor, contexto]);

  return (
    <div className="space-y-2">
      <textarea
        value={valor}
        onChange={(e) => aoMudar(e.target.value)}
        rows={linhas}
        placeholder={placeholder}
        className="w-full rounded-md border border-border bg-background p-3 text-sm leading-relaxed"
      />
      {limite && (
        <p className={`text-right text-xs ${valor.length > limite ? "text-destructive" : "text-muted-foreground"}`}>
          {valor.length}/{limite}
        </p>
      )}
      <ListaOab problemas={problemas} />
    </div>
  );
}

export function Tabela({
  colunas,
  linhas,
  vazio = "Sem dados ainda.",
}: {
  colunas: { rotulo: string; alinhar?: "direita" }[];
  linhas: React.ReactNode[][];
  vazio?: string;
}) {
  if (!linhas.length) return <p className="text-sm text-muted-foreground">{vazio}</p>;
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left text-xs text-muted-foreground">
            {colunas.map((c) => (
              <th key={c.rotulo} className={`py-2 pr-3 font-medium ${c.alinhar === "direita" ? "text-right" : ""}`}>
                {c.rotulo}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {linhas.map((l, i) => (
            <tr key={i} className="border-b border-border/50 last:border-0">
              {l.map((celula, j) => (
                <td key={j} className={`py-2 pr-3 align-top ${colunas[j]?.alinhar === "direita" ? "text-right tabular-nums" : ""}`}>
                  {celula}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function Secao({ titulo, descricao, children, acoes }: { titulo: string; descricao?: string; children: React.ReactNode; acoes?: React.ReactNode }) {
  return (
    <Card className="p-6 hover:translate-y-0">
      <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="font-display text-lg font-semibold tracking-tight">{titulo}</h2>
          {descricao && <p className="mt-1 text-sm text-muted-foreground">{descricao}</p>}
        </div>
        {acoes}
      </div>
      {children}
    </Card>
  );
}
