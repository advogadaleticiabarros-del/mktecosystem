"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { CheckCircle2, ChevronLeft } from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type ContentPiece = {
  id: string;
  tipo: string;
  corpo: Record<string, unknown>;
  status: string;
};

const STEPS = [
  { key: "planejamento", label: "Planejamento", detail: "Pauta criada" },
  { key: "pesquisa", label: "Pesquisa", detail: "Fontes verificadas" },
  { key: "conteudo", label: "Conteúdo", detail: "Gerado com IA" },
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
              <p
                className={cn(
                  "text-sm font-medium",
                  isFuture ? "text-muted-foreground" : "text-foreground",
                )}
              >
                {step.label}
              </p>
              <p className="text-xs text-muted-foreground">{step.detail}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function AprovacaoContent() {
  const searchParams = useSearchParams();
  const pautaId = searchParams.get("pautaId");
  const router = useRouter();
  const [pieces, setPieces] = useState<ContentPiece[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!pautaId) {
      setLoading(false);
      setError("Nenhuma pauta selecionada.");
      return;
    }

    apiFetch("/content/gerar", {
      method: "POST",
      body: JSON.stringify({ pauta_id: pautaId }),
    })
      .then(async (response) => {
        if (response.status === 401) {
          router.push("/login");
          return;
        }
        if (!response.ok) {
          setLoading(false);
          setError("Erro ao gerar conteúdo. Tente novamente.");
          return;
        }
        const data = await response.json();
        setPieces(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
        setError("Erro ao gerar conteúdo. Tente novamente.");
      });
  }, [pautaId, router]);

  async function atualizarStatus(pieceId: string, status: string) {
    const response = await apiFetch(`/content/${pieceId}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
    const updated = await response.json();
    setPieces((prev) => prev.map((p) => (p.id === pieceId ? updated : p)));
  }

  function editarCorpo(pieceId: string, novoCorpo: Record<string, unknown>) {
    setPieces((prev) => prev.map((p) => (p.id === pieceId ? { ...p, corpo: novoCorpo } : p)));
  }

  async function salvarEdicao(piece: ContentPiece) {
    await apiFetch(`/content/${piece.id}`, {
      method: "PATCH",
      body: JSON.stringify({ corpo: piece.corpo }),
    });
  }

  const activeIndex = loading ? 2 : error ? 1 : 3;

  return (
    <AppShell
      title="Revisar e aprovar"
      description="Confira e edite o conteúdo antes da publicação"
      headerActions={
        <Button variant="outline" size="sm" onClick={() => router.push("/planejamento")}>
          <ChevronLeft className="h-4 w-4" />
          Voltar ao planejamento
        </Button>
      }
    >
      <div className="grid gap-8 lg:grid-cols-[1fr_260px]">
        <div className="space-y-6">
          {loading && <p className="text-sm text-muted-foreground">Gerando conteúdo...</p>}
          {error && <p className="text-sm text-destructive">{error}</p>}

          {pieces.map((piece) => (
            <Card key={piece.id} className="p-5">
              <h3 className="mb-3 font-display text-base font-semibold capitalize">
                {piece.tipo}
              </h3>
              <textarea
                value={JSON.stringify(piece.corpo, null, 2)}
                onChange={(e) => {
                  try {
                    editarCorpo(piece.id, JSON.parse(e.target.value));
                  } catch {
                    // ignore invalid JSON while typing
                  }
                }}
                onBlur={() => salvarEdicao(piece)}
                rows={8}
                className="w-full rounded-md border border-border bg-background p-3 font-mono text-xs"
              />
              <div className="mt-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <p className="text-xs text-muted-foreground">Status: {piece.status}</p>
                  {piece.status !== "rascunho" && (
                    <span className="flex items-center gap-1 text-xs text-primary">
                      <CheckCircle2 className="h-3 w-3" /> Salvo automaticamente
                    </span>
                  )}
                </div>
                <div className="flex gap-2">
                  <Button size="sm" onClick={() => atualizarStatus(piece.id, "aprovado")}>
                    Aprovar
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => atualizarStatus(piece.id, "rejeitado")}
                  >
                    Rejeitar
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="rounded-xl border border-border bg-card p-5">
          <ProgressStepper activeIndex={activeIndex} />
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
