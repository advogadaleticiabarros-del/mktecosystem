"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Newspaper, Plus, Scale, Sparkles } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";

type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  origem: string;
  fonte: string;
};

const AREA_ICON = { Previdenciário: Scale, Trabalhista: Newspaper } as const;

export default function PlanejamentoPage() {
  const [pautas, setPautas] = useState<Pauta[]>([]);
  const [loading, setLoading] = useState(false);
  const [manualTitulo, setManualTitulo] = useState("");
  const [manualAngulo, setManualAngulo] = useState("direitos");
  const [manualArea, setManualArea] = useState("Trabalhista");
  const router = useRouter();

  async function carregarSugestoes() {
    const response = await apiFetch("/pautas?relevante_para_conteudo=true");
    if (response.status === 401) {
      router.push("/login");
      return;
    }
    setPautas(await response.json());
  }

  useEffect(() => {
    carregarSugestoes();
  }, []);

  async function buscarNovasSugestoes() {
    setLoading(true);
    try {
      await apiFetch("/pautas/buscar", { method: "POST" });
      await carregarSugestoes();
    } finally {
      setLoading(false);
    }
  }

  async function criarPautaManual(event: React.FormEvent) {
    event.preventDefault();
    await apiFetch("/pautas", {
      method: "POST",
      body: JSON.stringify({ titulo: manualTitulo, angulo: manualAngulo, area: manualArea }),
    });
    setManualTitulo("");
    await carregarSugestoes();
  }

  function escolherPauta(pautaId: string) {
    router.push(`/aprovacao?pautaId=${pautaId}`);
  }

  return (
    <AppShell
      title="Planejamento"
      description="Escolha um tema ou deixe o Orbit sugerir para você"
      headerActions={
        <Button variant="outline" size="sm" onClick={() => router.push("/resumo-diario")}>
          Resumo Jurídico Diário
        </Button>
      }
    >
      <div className="mb-4 flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-primary" />
        <p className="text-sm font-medium text-primary">Sugestões para hoje</p>
      </div>

      <div className="mb-4">
        <Button onClick={buscarNovasSugestoes} disabled={loading} variant="secondary">
          {loading ? "Buscando..." : "Buscar sugestões de hoje"}
        </Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {pautas.map((pauta) => {
          const Icon = AREA_ICON[pauta.area as keyof typeof AREA_ICON] ?? Newspaper;
          return (
            <Card key={pauta.id} className="flex flex-col gap-4 p-5">
              <div className="flex items-start justify-between">
                <h3 className="font-display text-base font-semibold leading-snug">
                  {pauta.titulo}
                </h3>
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent text-primary">
                  <Icon className="h-4 w-4" />
                </div>
              </div>
              <div>
                <Badge variant="secondary" className="uppercase tracking-wide">
                  {pauta.area} ({pauta.angulo})
                </Badge>
                <p className="mt-2 text-xs text-muted-foreground">Fonte: {pauta.fonte}</p>
              </div>
              <Button onClick={() => escolherPauta(pauta.id)} className="mt-auto">
                Gerar conteúdo →
              </Button>
            </Card>
          );
        })}
      </div>

      <h2 className="mb-3 mt-8 font-display text-lg font-semibold text-primary">
        Ou digite um tema livre
      </h2>
      <form onSubmit={criarPautaManual} className="flex flex-wrap items-center gap-3">
        <Input
          placeholder="Ex: Estabilidade da gestante em contrato temporário"
          value={manualTitulo}
          onChange={(e) => setManualTitulo(e.target.value)}
          required
          className="max-w-md flex-1"
        />
        <select
          value={manualAngulo}
          onChange={(e) => setManualAngulo(e.target.value)}
          className="h-9 rounded-md border border-border bg-card px-3 text-sm"
        >
          <option value="direitos">Direitos</option>
          <option value="sinceridade">Sinceridade</option>
        </select>
        <select
          value={manualArea}
          onChange={(e) => setManualArea(e.target.value)}
          className="h-9 rounded-md border border-border bg-card px-3 text-sm"
        >
          <option>Trabalhista</option>
          <option>Previdenciário</option>
          <option>Família</option>
          <option>Consumidor</option>
        </select>
        <Button type="submit" variant="secondary">
          <Plus className="h-4 w-4" />
          Adicionar pauta
        </Button>
      </form>
    </AppShell>
  );
}
