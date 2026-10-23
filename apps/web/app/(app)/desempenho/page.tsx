"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AlertTriangle, ArrowDownRight, ArrowRight, ArrowUpRight, ChevronDown, Loader2, RefreshCw } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type Kpi = { rotulo: string; valor: number | null; anterior: number | null; formato: "numero" | "percentual" | "posicao" | "nota"; explicacao: string };
type Lista = { titulo: string; colunas: string[]; linhas: (string | number)[][]; links?: (string | null)[] };
type Secao = {
  chave: string;
  titulo: string;
  link: string;
  situacao: "ok" | "sem_dados" | "sem_conexao";
  resumo: string;
  kpis: Kpi[];
  listas: Lista[];
  atualizado_em: string | null;
};
type Desempenho = { avisos: { texto: string; link: string }[]; secoes: Secao[] };

function formatar(v: number | null, formato: Kpi["formato"]) {
  if (v === null || v === undefined) return "—";
  if (formato === "percentual") return `${v.toLocaleString("pt-BR")}%`;
  if (formato === "nota") return v.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  if (formato === "posicao") return v.toLocaleString("pt-BR", { maximumFractionDigits: 1 });
  return v.toLocaleString("pt-BR");
}

function Variacao({ k }: { k: Kpi }) {
  if (k.valor === null || k.anterior === null || k.anterior === undefined || k.anterior === 0) return null;
  const melhorou = k.formato === "posicao" ? k.valor < k.anterior : k.valor > k.anterior;
  const igual = k.valor === k.anterior;
  const pct = k.formato === "posicao" ? null : Math.round(((k.valor - k.anterior) / k.anterior) * 100);
  const Icone = igual ? ArrowRight : melhorou ? ArrowUpRight : ArrowDownRight;
  return (
    <span className={`inline-flex items-center gap-0.5 text-xs ${igual ? "text-muted-foreground" : melhorou ? "text-emerald-600 dark:text-emerald-400" : "text-destructive"}`}
      title={`Mês anterior: ${formatar(k.anterior, k.formato)}`}>
      <Icone className="h-3.5 w-3.5" />
      {pct !== null ? `${pct > 0 ? "+" : ""}${pct}%` : `antes ${formatar(k.anterior, k.formato)}`}
    </span>
  );
}

function Tabela({ l }: { l: Lista }) {
  const [aberta, setAberta] = useState(false);
  if (!l.linhas.length) return null;
  return (
    <div className="rounded-md border">
      <button type="button" onClick={() => setAberta((a) => !a)} className="flex w-full items-center justify-between px-3 py-2 text-left text-sm font-medium">
        {l.titulo} <span className="flex items-center gap-1 text-xs text-muted-foreground">{l.linhas.length}<ChevronDown className={`h-4 w-4 transition-transform ${aberta ? "rotate-180" : ""}`} /></span>
      </button>
      {aberta && (
        <div className="overflow-x-auto border-t">
          <table className="w-full text-sm">
            <thead><tr className="text-left text-xs text-muted-foreground">{l.colunas.map((c, i) => <th key={c} className={`px-3 py-1.5 font-medium ${i > 0 && typeof l.linhas[0][i] === "number" ? "text-right" : ""}`}>{c}</th>)}</tr></thead>
            <tbody>
              {l.linhas.map((linha, i) => (
                <tr key={i} className="border-t">
                  {linha.map((celula, j) => (
                    <td key={j} className={`px-3 py-1.5 ${typeof celula === "number" ? "text-right tabular-nums" : "max-w-96 truncate"}`} title={String(celula)}>
                      {j === 0 && l.links?.[i] ? <a href={l.links[i]!} target="_blank" rel="noreferrer" className="text-primary hover:underline">{celula}</a>
                        : typeof celula === "number" ? celula.toLocaleString("pt-BR") : celula}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function BlocoCanal({ s }: { s: Secao }) {
  const router = useRouter();
  return (
    <Card className="p-5 hover:translate-y-0">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="min-w-0">
          <h2 className="font-display text-base font-semibold">{s.titulo}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{s.resumo}</p>
        </div>
        <Button size="sm" variant="outline" onClick={() => router.push(s.link)}>Detalhes</Button>
      </div>
      {s.kpis.length > 0 && (
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {s.kpis.map((k) => (
            <div key={k.rotulo} className="rounded-md border p-3" title={k.explicacao}>
              <p className="text-xs text-muted-foreground">{k.rotulo}</p>
              <div className="mt-1 flex flex-wrap items-baseline gap-2">
                <span className="text-xl font-semibold tabular-nums">{formatar(k.valor, k.formato)}</span>
                <Variacao k={k} />
              </div>
              {k.explicacao && <p className="mt-1 text-[11px] leading-snug text-muted-foreground">{k.explicacao}</p>}
            </div>
          ))}
        </div>
      )}
      {s.listas.some((l) => l.linhas.length) && <div className="mt-4 space-y-2">{s.listas.map((l) => <Tabela key={l.titulo} l={l} />)}</div>}
      {s.atualizado_em && <p className="mt-3 text-[11px] text-muted-foreground">Dados de {new Date(s.atualizado_em).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}</p>}
    </Card>
  );
}

export default function DesempenhoPage() {
  const router = useRouter();
  const [dados, setDados] = useState<Desempenho | null>(null);
  const [atualizando, setAtualizando] = useState(false);

  const carregar = useCallback(async () => {
    const r = await apiFetch("/desempenho");
    if (r.status === 401) return router.push("/login");
    if (r.ok) setDados(await r.json());
  }, [router]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function atualizarAgora() {
    setAtualizando(true);
    await Promise.allSettled([apiFetch("/presenca/atualizar", { method: "POST" }), apiFetch("/analise/instagram/atualizar", { method: "POST" })]);
    await carregar();
    setAtualizando(false);
  }

  return (
    <AppShell title="Desempenho" description="Site, Google, Instagram, LinkedIn, TikTok e blog numa tela só. As setas comparam com o mês anterior.">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-muted-foreground">Os números são atualizados sozinhos todo dia de manhã.</p>
        <Button variant="outline" size="sm" disabled={atualizando} onClick={atualizarAgora}>
          {atualizando ? <Loader2 className="animate-spin" /> : <RefreshCw />} {atualizando ? "Buscando dados (até 1 minuto)…" : "Atualizar agora"}
        </Button>
      </div>
      {!dados && <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />}
      {dados && dados.avisos.length > 0 && (
        <Card className="mb-6 border-amber-500/40 p-4 hover:translate-y-0">
          <p className="flex items-center gap-2 text-sm font-medium"><AlertTriangle className="h-4 w-4 text-amber-600" /> Precisa de atenção</p>
          <ul className="mt-2 space-y-1 text-sm">
            {dados.avisos.map((a) => (
              <li key={a.texto}><button type="button" onClick={() => router.push(a.link)} className="text-left hover:underline">{a.texto}</button></li>
            ))}
          </ul>
        </Card>
      )}
      <div className="space-y-6">{dados?.secoes.map((s) => <BlocoCanal key={s.chave} s={s} />)}</div>
    </AppShell>
  );
}
