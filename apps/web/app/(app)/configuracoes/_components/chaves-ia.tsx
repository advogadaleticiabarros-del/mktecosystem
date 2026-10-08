"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, Eye, EyeOff, Loader2, Lock, Sparkles } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type StatusChave = {
  provedor: string;
  nome: string;
  uso: string;
  configurada: boolean;
  final: string | null;
  validada_em: string | null;
  origem: "painel" | "servidor" | null;
};

function ChaveServico({ status, onMudou }: { status: StatusChave; onMudou: () => void }) {
  const [editando, setEditando] = useState(!status.configurada);
  const [chave, setChave] = useState("");
  const [mostrar, setMostrar] = useState(false);
  const [validando, setValidando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState(false);

  async function salvar(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setOk(false);
    setValidando(true);
    try {
      const r = await apiFetch(`/chaves/${status.provedor}`, { method: "PUT", body: JSON.stringify({ chave }) });
      if (!r.ok) {
        const corpo = await r.json().catch(() => null);
        setErro(corpo?.detail ?? "Não foi possível validar a chave agora. Tente de novo em alguns minutos.");
        return;
      }
      setChave("");
      setEditando(false);
      setOk(true);
      onMudou();
    } finally {
      setValidando(false);
    }
  }

  async function remover() {
    if (!confirm(`Remover a chave da ${status.nome}? O Jornalista para de usar essa fonte.`)) return;
    await apiFetch(`/chaves/${status.provedor}`, { method: "DELETE" });
    setEditando(true);
    onMudou();
  }

  return (
    <div className="rounded-xl p-4 ring-1 ring-foreground/10">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="font-medium">{status.nome}</p>
          <p className="mt-0.5 text-xs text-muted-foreground">{status.uso}</p>
        </div>
        {status.configurada ? (
          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-700 dark:text-emerald-400">
            <CheckCircle2 className="h-3 w-3" /> Conectada
          </span>
        ) : (
          <span className="rounded-full bg-muted px-2 py-0.5 text-[11px] text-muted-foreground">Não conectada</span>
        )}
      </div>

      {status.configurada && !editando && (
        <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
          <span className="font-mono text-muted-foreground">
            {status.final ? `sk-…${status.final}` : "guardada no servidor"}
          </span>
          {status.validada_em && (
            <span className="text-xs text-muted-foreground">
              validada em {new Date(status.validada_em).toLocaleDateString("pt-BR")}
            </span>
          )}
          <span className="ml-auto flex gap-1">
            <Button variant="ghost" size="sm" onClick={() => setEditando(true)}>
              Trocar chave
            </Button>
            {status.origem === "painel" && (
              <Button variant="ghost" size="sm" className="text-muted-foreground" onClick={remover}>
                Remover
              </Button>
            )}
          </span>
        </div>
      )}

      {editando && (
        <form onSubmit={salvar} className="mt-3 space-y-2">
          <div className="relative">
            <Input
              type={mostrar ? "text" : "password"}
              autoComplete="off"
              spellCheck={false}
              placeholder="Cole aqui a chave (começa com sk-)"
              value={chave}
              onChange={(e) => setChave(e.target.value)}
              className="pr-10 font-mono"
              required
            />
            <button
              type="button"
              onClick={() => setMostrar((m) => !m)}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-muted-foreground hover:text-foreground"
              aria-label={mostrar ? "Esconder a chave" : "Mostrar a chave"}
            >
              {mostrar ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Button type="submit" size="sm" disabled={validando || chave.trim().length < 8}>
              {validando && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
              {validando ? "Testando com a OpenAI…" : "Validar e salvar"}
            </Button>
            {status.configurada && (
              <Button type="button" variant="ghost" size="sm" onClick={() => setEditando(false)}>
                Cancelar
              </Button>
            )}
          </div>
        </form>
      )}

      {erro && <p className="mt-2 text-sm text-destructive">{erro}</p>}
      {ok && (
        <p className="mt-2 flex items-center gap-1.5 text-sm text-emerald-700 dark:text-emerald-400">
          <CheckCircle2 className="h-4 w-4" /> Chave aceita e salva. O Jornalista já usa essa fonte na próxima ronda.
        </p>
      )}
    </div>
  );
}

export function ChavesIA() {
  const [lista, setLista] = useState<StatusChave[] | null>(null);
  const carregar = () =>
    apiFetch("/chaves")
      .then((r) => (r.ok ? r.json() : []))
      .then(setLista)
      .catch(() => setLista([]));

  useEffect(() => {
    carregar();
  }, []);

  return (
    <Card className="p-6 hover:translate-y-0">
      <div className="flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-primary" />
        <h2 className="font-display text-base font-semibold">Chaves de IA</h2>
      </div>
      <p className="mt-1.5 flex items-start gap-1.5 text-xs leading-relaxed text-muted-foreground">
        <Lock className="mt-0.5 h-3 w-3 shrink-0" />
        A chave é testada na hora e guardada criptografada. Depois de salva, nem esta tela mostra o valor, só o final para
        você reconhecer.
      </p>
      <div className="mt-4 space-y-3">
        {lista === null && <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />}
        {lista?.map((s) => (
          <ChaveServico key={s.provedor} status={s} onMudou={carregar} />
        ))}
      </div>
    </Card>
  );
}
