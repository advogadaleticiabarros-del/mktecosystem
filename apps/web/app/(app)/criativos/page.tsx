"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, Download, ImageIcon, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

// O Estúdio mostra as artes prontas que o Orbit guarda em cada peça
// (`corpo.imagens` no carrossel, `corpo.imagem` nas peças de imagem única),
// em qualquer status: rascunho para aprovar, aprovado/agendado e publicado.
type ContentPiece = {
  id: string;
  tipo: string;
  status: string;
  criado_em: string;
  corpo: {
    imagens?: string[];
    imagem?: string;
    legenda?: string;
    programacao?: { data?: string; hora?: string };
  };
};

const TIPOS: Record<string, string> = {
  carrossel: "Carrossel",
  pergunta: "Pergunta",
  frase: "Frase",
  estatico: "Estático",
  stories: "Stories",
};

const STATUS: Record<string, string> = {
  rascunho: "Para aprovar",
  aprovado: "Aprovado",
  publicado: "Publicado",
};

const FILTROS_STATUS = ["todos", "rascunho", "aprovado", "publicado"] as const;

function imagensDe(p: ContentPiece): string[] {
  if (Array.isArray(p.corpo.imagens)) return p.corpo.imagens;
  if (typeof p.corpo.imagem === "string") return [p.corpo.imagem];
  return [];
}

function dataDe(p: ContentPiece): string {
  const d = p.corpo.programacao?.data;
  if (d) {
    const [ano, mes, dia] = d.split("-");
    return `${dia}/${mes}/${ano}${p.corpo.programacao?.hora ? ` · ${p.corpo.programacao.hora}` : ""}`;
  }
  return new Date(p.criado_em).toLocaleDateString("pt-BR");
}

function ordem(p: ContentPiece): string {
  return p.corpo.programacao?.data ? `${p.corpo.programacao.data} ${p.corpo.programacao.hora ?? ""}` : p.criado_em;
}

async function baixar(url: string, nome: string) {
  try {
    const resp = await fetch(url);
    const blob = await resp.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = nome;
    link.click();
    URL.revokeObjectURL(link.href);
  } catch {
    window.open(url, "_blank");
  }
}

export default function CriativosPage() {
  const [pieces, setPieces] = useState<ContentPiece[] | null>(null);
  const [filtroStatus, setFiltroStatus] = useState<(typeof FILTROS_STATUS)[number]>("todos");
  const [filtroTipo, setFiltroTipo] = useState<string>("todos");
  const [selecionado, setSelecionado] = useState<ContentPiece | null>(null);
  const [atual, setAtual] = useState(0);
  const [baixando, setBaixando] = useState(false);
  const router = useRouter();

  useEffect(() => {
    apiFetch("/content").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      const data: ContentPiece[] = await resp.json();
      setPieces(
        data
          .filter((p) => p.tipo in TIPOS && imagensDe(p).length > 0)
          .sort((a, b) => ordem(a).localeCompare(ordem(b))),
      );
    });
  }, [router]);

  const visiveis = useMemo(
    () =>
      (pieces ?? []).filter(
        (p) => (filtroStatus === "todos" || p.status === filtroStatus) && (filtroTipo === "todos" || p.tipo === filtroTipo),
      ),
    [pieces, filtroStatus, filtroTipo],
  );

  const imagens = selecionado ? imagensDe(selecionado) : [];

  async function baixarTodas() {
    if (!selecionado) return;
    setBaixando(true);
    try {
      for (let i = 0; i < imagens.length; i++) {
        await baixar(imagens[i], `${selecionado.tipo}-${i + 1}.jpg`);
        await new Promise((r) => setTimeout(r, 300));
      }
    } finally {
      setBaixando(false);
    }
  }

  return (
    <AppShell
      title="Estúdio de criativos"
      description="As artes prontas do Orbit: para aprovar, agendadas e publicadas"
    >
      {!selecionado && (
        <div className="mb-5 flex flex-wrap gap-2">
          {FILTROS_STATUS.map((s) => (
            <Button key={s} size="sm" variant={filtroStatus === s ? "default" : "outline"} onClick={() => setFiltroStatus(s)}>
              {s === "todos" ? "Todos" : STATUS[s]}
            </Button>
          ))}
          <span className="mx-1 w-px self-stretch bg-border" />
          {["todos", ...Object.keys(TIPOS)].map((t) => (
            <Button key={t} size="sm" variant={filtroTipo === t ? "default" : "outline"} onClick={() => setFiltroTipo(t)}>
              {t === "todos" ? "Todos os formatos" : TIPOS[t]}
            </Button>
          ))}
        </div>
      )}

      {pieces === null && (
        <div className="flex justify-center p-12">
          <Loader2 className="h-6 w-6 animate-spin text-primary" />
        </div>
      )}

      {pieces !== null && visiveis.length === 0 && !selecionado && (
        <Card className="flex flex-col items-center gap-3 p-12 text-center">
          <ImageIcon className="h-8 w-8 text-primary" />
          <p className="font-display text-lg font-semibold">Nenhum criativo neste filtro</p>
          <p className="max-w-md text-sm text-muted-foreground">
            Quando o Orbit gera uma peça com arte, ela aparece aqui: para aprovar, agendada ou já publicada.
          </p>
        </Card>
      )}

      {!selecionado && visiveis.length > 0 && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {visiveis.map((piece) => {
            const capa = imagensDe(piece)[0];
            return (
              <Card
                key={piece.id}
                className="cursor-pointer overflow-hidden p-0 transition-colors hover:border-primary/50"
                onClick={() => {
                  setSelecionado(piece);
                  setAtual(0);
                }}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={capa} alt={TIPOS[piece.tipo]} loading="lazy" className="aspect-[4/5] w-full bg-muted object-contain" />
                <div className="flex flex-col gap-1.5 p-3">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <Badge variant="secondary">{TIPOS[piece.tipo]}</Badge>
                    <Badge variant={piece.status === "rascunho" ? "outline" : "default"}>
                      {STATUS[piece.status] ?? piece.status}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {dataDe(piece)}
                    {piece.tipo === "carrossel" ? ` · ${imagensDe(piece).length} slides` : ""}
                  </p>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {selecionado && (
        <div className="flex flex-col items-center gap-5">
          <div className="flex w-full max-w-xl items-center justify-between gap-2">
            <Button variant="outline" size="sm" onClick={() => setSelecionado(null)}>
              <ChevronLeft className="h-4 w-4" />
              Voltar
            </Button>
            <div className="flex items-center gap-1.5">
              <Badge variant="secondary">{TIPOS[selecionado.tipo]}</Badge>
              <Badge>{STATUS[selecionado.status] ?? selecionado.status}</Badge>
            </div>
            <Button size="sm" onClick={baixarTodas} disabled={baixando}>
              {baixando ? <Loader2 className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4" />}
              {imagens.length > 1 ? "Baixar todas" : "Baixar"}
            </Button>
          </div>

          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={imagens[atual]}
            alt={`${TIPOS[selecionado.tipo]} ${atual + 1}`}
            className="w-full max-w-xl rounded-xl border border-border bg-muted object-contain"
            style={{ aspectRatio: "4 / 5" }}
          />

          {imagens.length > 1 && (
            <div className="flex items-center gap-3">
              <Button variant="outline" size="sm" disabled={atual === 0} onClick={() => setAtual((s) => s - 1)} aria-label="Anterior">
                <ChevronLeft className="h-4 w-4" />
              </Button>
              {imagens.map((_, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setAtual(i)}
                  aria-label={`Slide ${i + 1}`}
                  className={cn("h-2 w-2 rounded-full transition-colors", i === atual ? "bg-primary" : "bg-border")}
                />
              ))}
              <Button
                variant="outline"
                size="sm"
                disabled={atual === imagens.length - 1}
                onClick={() => setAtual((s) => s + 1)}
                aria-label="Próximo"
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          )}

          <p className="text-sm text-muted-foreground">{dataDe(selecionado)}</p>
          {selecionado.corpo.legenda && (
            <Card className="w-full max-w-xl whitespace-pre-line p-4 text-sm">{selecionado.corpo.legenda}</Card>
          )}
        </div>
      )}
    </AppShell>
  );
}
