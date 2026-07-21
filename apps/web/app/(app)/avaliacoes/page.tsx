"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Star } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Card } from "@/components/ui/card";

type Avaliacao = {
  name: string;
  reviewer: { displayName: string };
  starRating: string;
  comment?: string;
  reviewReply?: { comment: string };
  urgencia: "urgente" | "normal" | null;
};

const ESTRELAS: Record<string, number> = {
  ONE: 1,
  TWO: 2,
  THREE: 3,
  FOUR: 4,
  FIVE: 5,
};

export default function AvaliacoesPage() {
  const [avaliacoes, setAvaliacoes] = useState<Avaliacao[] | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [respostas, setRespostas] = useState<Record<string, string>>({});
  const [enviando, setEnviando] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    apiFetch("/avaliacoes").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      if (!resp.ok) {
        const body = await resp.json().catch(() => null);
        setErro(body?.detail ?? "Não foi possível carregar as avaliações.");
        return;
      }
      setAvaliacoes(await resp.json());
    });
  }, [router]);

  async function responder(reviewName: string) {
    const texto = respostas[reviewName]?.trim();
    if (!texto) return;
    setEnviando(reviewName);
    try {
      const resp = await apiFetch(`/avaliacoes/${encodeURIComponent(reviewName)}/responder`, {
        method: "POST",
        body: JSON.stringify({ texto }),
      });
      if (resp.ok) {
        setAvaliacoes((prev) =>
          prev
            ? prev.map((a) =>
                a.name === reviewName ? { ...a, reviewReply: { comment: texto } } : a,
              )
            : prev,
        );
      }
    } finally {
      setEnviando(null);
    }
  }

  return (
    <AppShell title="Avaliações" description="Responda avaliações do Google Meu Negócio">
      {erro && <Card className="p-6 text-sm text-muted-foreground">{erro}</Card>}
      {!erro && !avaliacoes && <p className="text-sm text-muted-foreground">Carregando...</p>}
      {avaliacoes && avaliacoes.length === 0 && (
        <Card className="p-6 text-sm text-muted-foreground">Nenhuma avaliação ainda.</Card>
      )}
      <div className="space-y-4">
        {avaliacoes?.map((a) => (
          <Card
            key={a.name}
            className={a.urgencia === "urgente" ? "border-l-2 border-destructive p-5" : "p-5"}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium">{a.reviewer.displayName}</p>
                {a.urgencia === "urgente" && (
                  <span className="rounded-full bg-destructive/15 px-2 py-0.5 text-[10px] font-medium text-destructive">
                    Urgente
                  </span>
                )}
              </div>
              <div className="flex items-center gap-0.5">
                {Array.from({ length: ESTRELAS[a.starRating] ?? 0 }).map((_, i) => (
                  <Star key={i} className="h-3.5 w-3.5 fill-primary text-primary" />
                ))}
              </div>
            </div>
            {a.comment && <p className="mt-2 text-sm text-muted-foreground">{a.comment}</p>}

            {a.reviewReply ? (
              <p className="mt-3 rounded-md bg-accent/40 p-3 text-xs text-muted-foreground">
                <span className="font-medium text-foreground">Sua resposta: </span>
                {a.reviewReply.comment}
              </p>
            ) : (
              <div className="mt-3 space-y-2">
                <textarea
                  value={respostas[a.name] ?? ""}
                  onChange={(e) =>
                    setRespostas((prev) => ({ ...prev, [a.name]: e.target.value }))
                  }
                  rows={2}
                  placeholder="Escreva sua resposta..."
                  className="w-full rounded-md border border-border bg-background p-2 text-xs"
                />
                <button
                  type="button"
                  onClick={() => responder(a.name)}
                  disabled={enviando === a.name || !respostas[a.name]?.trim()}
                  className="flex items-center gap-1.5 rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground disabled:opacity-60"
                >
                  {enviando === a.name && <Loader2 className="h-3 w-3 animate-spin" />}
                  Responder
                </button>
              </div>
            )}
          </Card>
        ))}
      </div>
    </AppShell>
  );
}
