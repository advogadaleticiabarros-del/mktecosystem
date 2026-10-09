"use client";

import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, ExternalLink, Layers, Loader2, X } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

// Grade do Instagram: o perfil como vai ficar. Cada post aparece recortado em 3:4, como o
// perfil mostra, com data e hora acima; tocar abre a arte inteira, legenda e comentário.
type PostGrade = {
  data: string;
  hora: string;
  tipo: string;
  status: "rascunho" | "agendado" | "publicado";
  imagens: string[];
  legenda: string;
  primeiro_comentario: string;
  permalink: string | null;
};

const TIPO: Record<string, string> = {
  carrossel: "Carrossel",
  pergunta: "Pergunta",
  frase: "Frase",
  estatico: "Estático",
  post: "Post",
  reels: "Reels",
};
const STATUS: Record<string, { rotulo: string; cor: string }> = {
  rascunho: { rotulo: "Para aprovar", cor: "bg-amber-400" },
  agendado: { rotulo: "Agendado", cor: "bg-primary" },
  publicado: { rotulo: "Publicado", cor: "bg-emerald-500" },
};
const SEMANA = ["dom", "seg", "ter", "qua", "qui", "sex", "sáb"];

function quando(p: PostGrade) {
  const [a, m, d] = p.data.split("-").map(Number);
  const dia = SEMANA[new Date(a, m - 1, d).getDay()];
  return `${dia} ${String(d).padStart(2, "0")}/${String(m).padStart(2, "0")} · ${p.hora}`;
}

export function GradeInstagram() {
  const [posts, setPosts] = useState<PostGrade[] | null>(null);
  const [aberto, setAberto] = useState<PostGrade | null>(null);
  const [slide, setSlide] = useState(0);

  useEffect(() => {
    apiFetch("/calendario/grade").then(async (r) => setPosts(r.ok ? await r.json() : []));
  }, []);

  if (posts === null) {
    return (
      <div className="flex justify-center p-12">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-4 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
        {Object.values(STATUS).map((s) => (
          <span key={s.rotulo} className="flex items-center gap-1.5">
            <span className={cn("h-2 w-2 rounded-full", s.cor)} /> {s.rotulo}
          </span>
        ))}
        <span>Mais novo no topo, como no perfil. Toque para ver a arte inteira.</span>
      </div>

      <div className="grid grid-cols-3 gap-x-1 gap-y-3">
        {posts.map((p, i) => (
          <button
            key={`${p.data}-${p.hora}-${i}`}
            type="button"
            className="text-left"
            onClick={() => {
              setAberto(p);
              setSlide(0);
            }}
          >
            <div className="mb-1 flex items-center gap-1.5 px-0.5 text-[11px] font-medium sm:text-xs">
              <span className={cn("h-1.5 w-1.5 shrink-0 rounded-full", STATUS[p.status].cor)} />
              <span className="truncate">{quando(p)}</span>
            </div>
            <div className="relative overflow-hidden bg-muted" style={{ aspectRatio: "3 / 4" }}>
              {p.imagens[0] ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={p.imagens[0]} alt={TIPO[p.tipo] ?? p.tipo} loading="lazy" className="h-full w-full object-cover" />
              ) : (
                <div className="flex h-full items-center justify-center text-xs text-muted-foreground">sem arte</div>
              )}
              {p.imagens.length > 1 && <Layers className="absolute right-1.5 top-1.5 h-4 w-4 text-white drop-shadow" />}
            </div>
          </button>
        ))}
      </div>

      {aberto && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/60 sm:items-center" onClick={() => setAberto(null)}>
          <div
            className="max-h-[92vh] w-full max-w-lg overflow-y-auto rounded-t-2xl bg-card p-4 sm:rounded-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-3 flex items-center justify-between gap-2">
              <div className="flex flex-wrap items-center gap-1.5">
                <Badge variant="secondary">{TIPO[aberto.tipo] ?? aberto.tipo}</Badge>
                <Badge>{STATUS[aberto.status].rotulo}</Badge>
                <span className="text-sm font-medium">{quando(aberto)}</span>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setAberto(null)} aria-label="Fechar">
                <X className="h-4 w-4" />
              </Button>
            </div>

            {aberto.imagens[slide] && (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={aberto.imagens[slide]}
                alt={`slide ${slide + 1}`}
                className="w-full rounded-lg bg-muted object-contain"
                style={{ aspectRatio: "4 / 5" }}
              />
            )}
            {aberto.imagens.length > 1 && (
              <div className="mt-2 flex items-center justify-center gap-3">
                <Button variant="outline" size="sm" disabled={slide === 0} onClick={() => setSlide((s) => s - 1)} aria-label="Anterior">
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <span className="text-xs text-muted-foreground">
                  {slide + 1} / {aberto.imagens.length}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={slide === aberto.imagens.length - 1}
                  onClick={() => setSlide((s) => s + 1)}
                  aria-label="Próximo"
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            )}

            {aberto.legenda && (
              <div className="mt-4">
                <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Legenda</p>
                <p className="whitespace-pre-line text-sm">{aberto.legenda}</p>
              </div>
            )}
            {aberto.primeiro_comentario && (
              <div className="mt-4">
                <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Primeiro comentário</p>
                <p className="whitespace-pre-line text-sm">{aberto.primeiro_comentario}</p>
              </div>
            )}
            {aberto.permalink && (
              <a href={aberto.permalink} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-primary">
                Ver no Instagram <ExternalLink className="h-3.5 w-3.5" />
              </a>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
