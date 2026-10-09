"use client";

// Revisar e aprovar (09/10/2026): esta tela NÃO gera conteúdo. Mostra o que já foi
// produzido e ainda não foi aprovado (rascunho ou alteração pedida), com as artes, a
// legenda e o primeiro comentário, e os botões "Aprovar e agendar" / "Pedir alteração".
// Aprovar agenda na data de corpo.programacao; pedir alteração tira do calendário.

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Check, CheckCircle2, ChevronLeft, MessageSquareText } from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type ContentPiece = {
  id: string;
  pauta_id: string;
  tipo: string;
  corpo: Record<string, unknown>;
  status: string;
};
type Pauta = { id: string; titulo: string; area: string };

const TIPO: Record<string, string> = {
  carrossel: "Carrossel", pergunta: "Me faça uma pergunta", frase: "Frase", estatico: "Estático",
  stories: "Story", artigo: "Artigo do blog", legenda: "Legenda", reels: "Reels", jornal: "Jornal",
};

const STEPS = [
  { key: "planejamento", label: "Planejamento", detail: "Pauta criada" },
  { key: "pesquisa", label: "Pesquisa", detail: "Fontes verificadas" },
  { key: "conteudo", label: "Conteúdo", detail: "Conteúdo que produzimos" },
  { key: "revisao", label: "Revisão", detail: "Aguardando aprovação" },
  { key: "publicado", label: "Publicado", detail: "Em breve" },
] as const;

function ProgressStepper({ activeIndex }: { activeIndex: number }) {
  return (
    <div className="flex flex-col gap-6">
      {STEPS.map((step, i) => {
        const isDone = i < activeIndex;
        const isActive = i === activeIndex;
        const isFuture = i > activeIndex;
        return (
          <div key={step.key} className="flex items-start gap-3">
            <motion.div
              initial={false}
              animate={isActive ? { scale: [1, 1.15, 1] } : {}}
              transition={{ duration: 1.4, repeat: isActive ? Infinity : 0 }}
              className={cn(
                "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2",
                isDone && "border-primary bg-primary text-primary-foreground",
                isActive && "border-primary text-primary",
                isFuture && "border-border text-muted-foreground",
              )}
            >
              {isDone ? <CheckCircle2 className="h-4 w-4" /> : i + 1}
            </motion.div>
            <div>
              <p className={cn("text-sm font-medium", isFuture ? "text-muted-foreground" : "text-foreground")}>{step.label}</p>
              <p className="text-xs text-muted-foreground">{step.detail}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function imagens(p: ContentPiece): string[] {
  const c = p.corpo;
  if (Array.isArray(c.imagens)) return c.imagens as string[];
  if (typeof c.imagem === "string") return [c.imagem];
  if (typeof c.imagem_capa === "string") return [c.imagem_capa];
  return [];
}

function quando(p: ContentPiece): string {
  const prog = p.corpo.programacao as { data?: string; hora?: string } | undefined;
  if (!prog?.data) return "Sem data combinada";
  const [, m, d] = prog.data.split("-");
  return `Sai em ${d}/${m}${prog.hora ? ` às ${prog.hora}` : ""}`;
}

function PecaRevisao({ peca, pauta, onAtualizar }: { peca: ContentPiece; pauta?: Pauta; onAtualizar: (p: ContentPiece) => void }) {
  const [escrevendo, setEscrevendo] = useState(false);
  const [texto, setTexto] = useState("");
  const [pendente, setPendente] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const imgs = imagens(peca);
  const legenda = String(peca.corpo.legenda ?? peca.corpo.texto ?? "");
  const comentario = String(peca.corpo.primeiro_comentario ?? "");
  const pedido = peca.corpo.pedido_alteracao as { texto?: string } | undefined;

  async function enviar(payload: Record<string, unknown>, falha: string) {
    setPendente(true);
    setErro(null);
    try {
      const r = await apiFetch(`/content/${peca.id}`, { method: "PATCH", body: JSON.stringify(payload) });
      if (!r.ok) throw new Error();
      onAtualizar(await r.json());
      setEscrevendo(false);
      setTexto("");
    } catch {
      setErro(falha);
    } finally {
      setPendente(false);
    }
  }

  return (
    <Card className="gap-4 p-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-primary">{TIPO[peca.tipo] ?? peca.tipo}</p>
          <h3 className="font-display text-base font-semibold">{pauta?.titulo ?? "Conteúdo"}</h3>
        </div>
        <p className="text-xs text-muted-foreground">{quando(peca)}</p>
      </div>

      {imgs.length > 0 && (
        <div className="flex gap-3 overflow-x-auto pb-1">
          {imgs.map((src) => (
            // eslint-disable-next-line @next/next/no-img-element
            <a key={src} href={src} target="_blank" rel="noreferrer" className="shrink-0">
              <img src={src} alt="" className="h-64 w-auto rounded-lg ring-1 ring-foreground/10" loading="lazy" />
            </a>
          ))}
        </div>
      )}

      {legenda && (
        <details className="rounded-lg bg-muted/40 p-3">
          <summary className="cursor-pointer text-xs font-semibold text-foreground">Legenda</summary>
          <p className="mt-2 whitespace-pre-line text-sm text-muted-foreground">{legenda}</p>
        </details>
      )}
      {comentario && (
        <details className="rounded-lg bg-muted/40 p-3">
          <summary className="cursor-pointer text-xs font-semibold text-foreground">Primeiro comentário</summary>
          <p className="mt-2 whitespace-pre-line text-sm text-muted-foreground">{comentario}</p>
        </details>
      )}

      {peca.status === "ajuste" && pedido?.texto && (
        <p className="rounded-lg border border-primary/40 bg-primary/5 p-3 text-sm">
          <span className="font-semibold">Alteração pedida:</span> “{pedido.texto}”
        </p>
      )}

      {escrevendo ? (
        <div className="flex flex-col gap-2">
          <textarea
            autoFocus
            rows={3}
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="O que você quer mudar? Ex.: trocar a foto da capa, mudar o título…"
            className="w-full rounded-md border border-border bg-background p-3 text-sm"
          />
          <div className="flex justify-end gap-2">
            <Button size="sm" variant="outline" onClick={() => setEscrevendo(false)} disabled={pendente}>Cancelar</Button>
            <Button
              size="sm"
              disabled={pendente || !texto.trim()}
              onClick={() =>
                enviar(
                  { status: "ajuste", corpo: { ...peca.corpo, pedido_alteracao: { texto: texto.trim(), em: new Date().toISOString() } } },
                  "Não foi possível enviar o pedido. Tente de novo.",
                )
              }
            >
              {pendente ? "Enviando…" : "Enviar pedido"}
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex justify-end gap-2">
          <Button size="sm" variant="outline" onClick={() => setEscrevendo(true)} disabled={pendente}>
            <MessageSquareText className="h-4 w-4" /> Pedir alteração
          </Button>
          <Button size="sm" onClick={() => enviar({ status: "aprovado" }, "Não foi possível aprovar. Tente de novo.")} disabled={pendente}>
            <Check className="h-4 w-4" /> {pendente ? "Aprovando…" : "Aprovar e agendar"}
          </Button>
        </div>
      )}
      {erro && <p className="text-sm text-destructive">{erro}</p>}
    </Card>
  );
}

function AprovacaoContent() {
  const searchParams = useSearchParams();
  const pautaId = searchParams.get("pautaId");
  const router = useRouter();
  const [pecas, setPecas] = useState<ContentPiece[]>([]);
  const [pautas, setPautas] = useState<Record<string, Pauta>>({});
  const [aba, setAba] = useState<"rascunho" | "ajuste">("rascunho");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    try {
      const filtro = pautaId ? `&pauta_id=${pautaId}` : "";
      const [r1, r2, r3] = await Promise.all([
        apiFetch(`/content?status=rascunho${filtro}`),
        apiFetch(`/content?status=ajuste${filtro}`),
        apiFetch("/pautas"),
      ]);
      if (r1.status === 401) return router.push("/login");
      if (!r1.ok || !r2.ok || !r3.ok) throw new Error();
      setPecas([...(await r1.json()), ...(await r2.json())]);
      const lista: Pauta[] = await r3.json();
      setPautas(Object.fromEntries(lista.map((p) => [p.id, p])));
    } catch {
      setError("Não foi possível carregar o conteúdo. Tente de novo.");
    } finally {
      setLoading(false);
    }
  }, [pautaId, router]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const ordenadas = useMemo(() => {
    const chave = (p: ContentPiece) => {
      const prog = p.corpo.programacao as { data?: string; hora?: string } | undefined;
      return prog?.data ? `${prog.data} ${prog.hora ?? ""}` : "9999";
    };
    return pecas.filter((p) => p.status === aba).sort((a, b) => chave(a).localeCompare(chave(b)));
  }, [pecas, aba]);
  const n = (s: string) => pecas.filter((p) => p.status === s).length;

  function atualizar(p: ContentPiece) {
    setPecas((prev) => prev.map((x) => (x.id === p.id ? p : x)));
  }

  return (
    <AppShell
      title="Revisar e aprovar"
      description="O conteúdo que produzimos e ainda espera a sua aprovação"
      headerActions={
        <Button variant="outline" size="sm" onClick={() => router.push("/planejamento")}>
          <ChevronLeft className="h-4 w-4" />
          Voltar ao planejamento
        </Button>
      }
    >
      <div className="grid gap-8 lg:grid-cols-[1fr_260px]">
        <div className="space-y-5">
          <div className="flex gap-2">
            {(["rascunho", "ajuste"] as const).map((s) => (
              <Button key={s} size="sm" variant={aba === s ? "default" : "outline"} onClick={() => setAba(s)}>
                {s === "rascunho" ? "Aguardando você" : "Alteração pedida"} ({n(s)})
              </Button>
            ))}
          </div>
          {loading && <p className="text-sm text-muted-foreground">Carregando o conteúdo…</p>}
          {error && <p className="text-sm text-destructive">{error}</p>}
          {!loading && !error && ordenadas.length === 0 && (
            <p className="text-sm text-muted-foreground">
              {aba === "rascunho" ? "Nada esperando aprovação por aqui." : "Nenhuma alteração pendente."}
            </p>
          )}
          {ordenadas.map((p) => (
            <PecaRevisao key={p.id} peca={p} pauta={pautas[p.pauta_id]} onAtualizar={atualizar} />
          ))}
        </div>

        <div className="h-fit rounded-xl border border-border bg-card p-5">
          <ProgressStepper activeIndex={3} />
        </div>
      </div>
    </AppShell>
  );
}

export default function AprovacaoPage() {
  return (
    <Suspense fallback={<p className="p-8 text-sm text-muted-foreground">Carregando...</p>}>
      <AprovacaoContent />
    </Suspense>
  );
}
