"use client";

import { useEffect, useState } from "react";
import { Calendar, ChevronRight, Users } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";

type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  fonte: string;
  relevante_para_conteudo: boolean;
};

export default function ResumoDiarioPage() {
  const [pautas, setPautas] = useState<Pauta[]>([]);

  useEffect(() => {
    apiFetch("/pautas/resumo-diario")
      .then((r) => r.json())
      .then(setPautas);
  }, []);

  const porArea = pautas.reduce<Record<string, Pauta[]>>((acc, p) => {
    (acc[p.area] ??= []).push(p);
    return acc;
  }, {});

  const candidatas = pautas.filter((p) => p.relevante_para_conteudo);

  return (
    <AppShell
      title="Resumo Jurídico Diário"
      description="Fique por dentro do que mais importa no direito hoje"
      headerActions={
        <div className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-sm text-muted-foreground">
          <Calendar className="h-4 w-4" />
          {new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "long", year: "numeric" }).format(
            new Date(),
          )}
        </div>
      }
    >
      <div className="space-y-8">
        {Object.entries(porArea).map(([area, itens]) => (
          <section key={area}>
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-primary">
              {area}
            </h2>
            <div className="divide-y divide-border rounded-xl border border-border bg-card">
              {itens.map((p) => (
                <div key={p.id} className="flex items-center justify-between px-4 py-3">
                  <p className="text-sm">
                    {p.titulo} — <span className="text-muted-foreground">fonte: {p.fonte}</span>
                  </p>
                  <div className="flex items-center gap-3">
                    {p.relevante_para_conteudo && (
                      <Badge className="bg-primary/15 text-primary hover:bg-primary/15">
                        candidato a conteúdo
                      </Badge>
                    )}
                    <ChevronRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>

      {candidatas.length > 0 && (
        <div
          className="mt-8 flex items-center justify-between rounded-xl border border-primary/30 bg-accent/40 px-5 py-4 opacity-60"
          title="Seleção múltipla ainda não é funcional — vá para Planejamento e escolha uma pauta por vez."
        >
          <div className="flex items-center gap-3">
            <Users className="h-5 w-5 text-primary" />
            <div>
              <p className="text-sm font-medium">
                {candidatas.length} {candidatas.length === 1 ? "pauta" : "pautas"} candidatas a
                conteúdo
              </p>
              <p className="text-xs text-muted-foreground">
                Acesse o planejamento para gerar conteúdo a partir delas
              </p>
            </div>
          </div>
          <span className="cursor-not-allowed rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground">
            Ir para planejamento
          </span>
        </div>
      )}
    </AppShell>
  );
}
