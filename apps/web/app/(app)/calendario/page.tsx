"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, Plus, Trash2, X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

type Agendamento = {
  id: string;
  content_piece_id: string | null;
  titulo: string;
  canal: string;
  formato: string;
  data_agendada: string;
  horario: string;
  status: string;
};

const CANAL_COR: Record<string, string> = {
  instagram: "border-l-primary bg-primary/10",
  blog: "border-l-sky-400 bg-sky-400/10",
  email: "border-l-emerald-400 bg-emerald-400/10",
};

const STATUS_DOT: Record<string, string> = {
  planejado: "bg-muted-foreground",
  pronto: "bg-primary",
  publicado: "bg-emerald-400",
};

const DIAS_SEMANA = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

function mesLabel(ano: number, mes: number) {
  return new Intl.DateTimeFormat("pt-BR", { month: "long", year: "numeric" }).format(
    new Date(ano, mes - 1, 1),
  );
}

export default function CalendarioPage() {
  const hoje = new Date();
  const [ano, setAno] = useState(hoje.getFullYear());
  const [mes, setMes] = useState(hoje.getMonth() + 1);
  const [itens, setItens] = useState<Agendamento[]>([]);
  const [editando, setEditando] = useState<Agendamento | null>(null);
  const [novoDia, setNovoDia] = useState<string | null>(null);
  const [novoTitulo, setNovoTitulo] = useState("");
  const router = useRouter();

  const mesParam = `${ano}-${String(mes).padStart(2, "0")}`;

  const carregar = useCallback(async () => {
    const resp = await apiFetch(`/calendario?mes=${mesParam}`);
    if (resp.status === 401) {
      router.push("/login");
      return;
    }
    setItens(await resp.json());
  }, [mesParam, router]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  function navegar(delta: number) {
    let novoMes = mes + delta;
    let novoAno = ano;
    if (novoMes < 1) {
      novoMes = 12;
      novoAno -= 1;
    } else if (novoMes > 12) {
      novoMes = 1;
      novoAno += 1;
    }
    setMes(novoMes);
    setAno(novoAno);
  }

  async function criarRapido(dia: string) {
    if (!novoTitulo.trim()) return;
    await apiFetch("/calendario", {
      method: "POST",
      body: JSON.stringify({ titulo: novoTitulo, data_agendada: dia }),
    });
    setNovoTitulo("");
    setNovoDia(null);
    await carregar();
  }

  async function salvarEdicao() {
    if (!editando) return;
    await apiFetch(`/calendario/${editando.id}`, {
      method: "PATCH",
      body: JSON.stringify({
        titulo: editando.titulo,
        canal: editando.canal,
        formato: editando.formato,
        data_agendada: editando.data_agendada,
        horario: editando.horario,
        status: editando.status,
      }),
    });
    setEditando(null);
    await carregar();
  }

  async function remover(id: string) {
    await apiFetch(`/calendario/${id}`, { method: "DELETE" });
    setEditando(null);
    await carregar();
  }

  const primeiroDia = new Date(ano, mes - 1, 1);
  const diasNoMes = new Date(ano, mes, 0).getDate();
  const offset = primeiroDia.getDay();
  const celulas: (string | null)[] = [
    ...Array.from({ length: offset }, () => null),
    ...Array.from({ length: diasNoMes }, (_, i) => {
      const d = String(i + 1).padStart(2, "0");
      return `${mesParam}-${d}`;
    }),
  ];

  const porDia = itens.reduce<Record<string, Agendamento[]>>((acc, item) => {
    (acc[item.data_agendada] ??= []).push(item);
    return acc;
  }, {});

  const hojeISO = new Date().toISOString().slice(0, 10);

  return (
    <AppShell
      title="Calendário editorial"
      description="Tudo que está planejado, pronto e publicado — conteúdo aprovado entra aqui sozinho"
      headerActions={
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => navegar(-1)} aria-label="Mês anterior">
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <span className="min-w-40 text-center font-display text-sm font-semibold capitalize">
            {mesLabel(ano, mes)}
          </span>
          <Button variant="outline" size="sm" onClick={() => navegar(1)} aria-label="Próximo mês">
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      }
    >
      <div className="mb-4 flex items-center gap-5 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-primary" /> Instagram
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-sky-400" /> Blog
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-emerald-400" /> E-mail
        </span>
      </div>

      <div className="grid grid-cols-7 gap-px overflow-hidden rounded-xl border border-border bg-border">
        {DIAS_SEMANA.map((d) => (
          <div
            key={d}
            className="bg-card px-2 py-2 text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground"
          >
            {d}
          </div>
        ))}
        {celulas.map((dia, i) => (
          <div
            key={i}
            className={cn(
              "group min-h-28 bg-background p-1.5",
              dia === hojeISO && "bg-accent/40",
            )}
          >
            {dia && (
              <>
                <div className="mb-1 flex items-center justify-between">
                  <span
                    className={cn(
                      "text-xs",
                      dia === hojeISO
                        ? "flex h-5 w-5 items-center justify-center rounded-full bg-primary font-semibold text-primary-foreground"
                        : "text-muted-foreground",
                    )}
                  >
                    {Number(dia.slice(8))}
                  </span>
                  <button
                    type="button"
                    onClick={() => {
                      setNovoDia(novoDia === dia ? null : dia);
                      setNovoTitulo("");
                    }}
                    className="rounded p-0.5 text-muted-foreground opacity-0 transition-opacity hover:bg-accent hover:text-foreground group-hover:opacity-100"
                    aria-label={`Adicionar em ${dia}`}
                  >
                    <Plus className="h-3.5 w-3.5" />
                  </button>
                </div>

                {novoDia === dia && (
                  <div className="mb-1">
                    <Input
                      autoFocus
                      value={novoTitulo}
                      placeholder="Título..."
                      className="h-7 text-xs"
                      onChange={(e) => setNovoTitulo(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") criarRapido(dia);
                        if (e.key === "Escape") setNovoDia(null);
                      }}
                    />
                  </div>
                )}

                <div className="space-y-1">
                  {(porDia[dia] ?? []).map((item) => (
                    <motion.button
                      key={item.id}
                      layout
                      type="button"
                      onClick={() => setEditando({ ...item })}
                      className={cn(
                        "block w-full rounded border-l-2 px-1.5 py-1 text-left text-[11px] leading-tight transition-transform hover:scale-[1.02]",
                        CANAL_COR[item.canal] ?? "border-l-muted bg-muted/20",
                      )}
                    >
                      <span className="flex items-center gap-1">
                        <span
                          className={cn(
                            "h-1.5 w-1.5 shrink-0 rounded-full",
                            STATUS_DOT[item.status],
                          )}
                        />
                        <span className="text-muted-foreground">{item.horario}</span>
                      </span>
                      <span className="line-clamp-2">{item.titulo}</span>
                    </motion.button>
                  ))}
                </div>
              </>
            )}
          </div>
        ))}
      </div>

      <AnimatePresence>
        {editando && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
            onClick={() => setEditando(null)}
          >
            <motion.div
              initial={{ scale: 0.95, y: 8 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.95, y: 8 }}
              className="w-full max-w-md rounded-2xl border border-border bg-card p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="mb-4 flex items-center justify-between">
                <h2 className="font-display text-lg font-semibold">Editar agendamento</h2>
                <button
                  type="button"
                  onClick={() => setEditando(null)}
                  className="rounded p-1 text-muted-foreground hover:bg-accent"
                  aria-label="Fechar"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="mb-1 block text-xs text-muted-foreground">Título</label>
                  <Input
                    value={editando.titulo}
                    onChange={(e) => setEditando({ ...editando, titulo: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="mb-1 block text-xs text-muted-foreground">Data</label>
                    <Input
                      type="date"
                      value={editando.data_agendada}
                      onChange={(e) =>
                        setEditando({ ...editando, data_agendada: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-muted-foreground">Horário</label>
                    <Input
                      type="time"
                      value={editando.horario}
                      onChange={(e) => setEditando({ ...editando, horario: e.target.value })}
                    />
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {(
                    [
                      ["canal", ["instagram", "blog", "email"]],
                      ["formato", ["carrossel", "post", "story", "artigo", "newsletter"]],
                      ["status", ["planejado", "pronto", "publicado"]],
                    ] as const
                  ).map(([campo, opcoes]) => (
                    <div key={campo}>
                      <label className="mb-1 block text-xs capitalize text-muted-foreground">
                        {campo}
                      </label>
                      <select
                        value={editando[campo]}
                        onChange={(e) => setEditando({ ...editando, [campo]: e.target.value })}
                        className="h-9 w-full rounded-md border border-border bg-background px-2 text-sm capitalize"
                      >
                        {opcoes.map((o) => (
                          <option key={o} value={o}>
                            {o}
                          </option>
                        ))}
                      </select>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-5 flex items-center justify-between">
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => remover(editando.id)}
                >
                  <Trash2 className="h-4 w-4" />
                  Remover
                </Button>
                <Button onClick={salvarEdicao}>Salvar</Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </AppShell>
  );
}
