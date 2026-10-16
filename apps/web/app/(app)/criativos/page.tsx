"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Check, ChevronLeft, ChevronRight, Download, Film, ImageIcon, Loader2, MessageSquareText } from "lucide-react";
import { STATUS_PECA, aprovarPeca, midiaDaPeca, pedirAlteracaoPeca, quandoSai } from "@/lib/pecas";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

// O Estúdio mostra as artes prontas que o Orbit guarda em cada peça
// (`corpo.imagens` no carrossel, `corpo.imagem` nas peças de imagem única, `corpo.video` no Reels),
// em qualquer status. Ao abrir uma peça, a Letícia aprova ou pede ajuste (lib/pecas.ts, as mesmas
// regras do Editorial do celular).
type ContentPiece = {
  id: string;
  tipo: string;
  status: string;
  criado_em: string;
  corpo: {
    imagens?: string[];
    imagem?: string;
    video?: string;
    legenda?: string;
    pedido_alteracao?: { texto?: string; em?: string };
    programacao?: { data?: string; hora?: string };
    reserva?: { desde?: string; motivo?: string };
  };
};

const TIPOS: Record<string, string> = {
  carrossel: "Carrossel",
  pergunta: "Pergunta",
  frase: "Frase",
  estatico: "Estático",
  stories: "Stories",
  reels: "Reels",
};

const STATUS = STATUS_PECA;

const FILTROS_STATUS = ["todos", "rascunho", "ajuste", "agenda", "reserva", "publicado"] as const;
const ROTULO_FILTRO: Record<string, string> = { ...STATUS_PECA, agenda: "Na agenda", reserva: "Reserva" };

function rotuloStatus(p: ContentPiece): string {
  if (p.status === "aprovado" && p.corpo.reserva) return "Reserva";
  return STATUS[p.status] ?? p.status;
}

// "Na agenda" = aprovada e com data; "Reserva" = aprovada mas fora da agenda de 1 post por dia.
function passaNoFiltro(p: ContentPiece, filtro: string): boolean {
  if (filtro === "todos") return true;
  if (filtro === "agenda") return p.status === "aprovado" && !!p.corpo.programacao?.data && !p.corpo.reserva;
  if (filtro === "reserva") return p.status === "aprovado" && !!p.corpo.reserva;
  return p.status === filtro;
}

function imagensDe(p: ContentPiece): string[] {
  const m = midiaDaPeca(p.corpo as Record<string, unknown>);
  return m.tipo === "imagens" ? m.urls : [];
}

function videoDe(p: ContentPiece): string | null {
  const m = midiaDaPeca(p.corpo as Record<string, unknown>);
  return m.tipo === "video" ? m.url : null;
}

// O card mostra quando a peça sai, nunca a data em que foi produzida (isso confundia: tudo aparecia "08/10").
function dataDe(p: ContentPiece): string {
  const d = p.corpo.programacao?.data;
  if (d) {
    const [ano, mes, dia] = d.split("-");
    const quando = `${dia}/${mes}/${ano}${p.corpo.programacao?.hora ? ` · ${p.corpo.programacao.hora}` : ""}`;
    return p.status === "publicado" ? `Publicado · ${quando}` : `Sai ${quando}`;
  }
  if (p.corpo.reserva) return p.corpo.reserva.motivo?.startsWith("pedido") ? "Fora do ar (a seu pedido)" : "Reserva · sem data";
  if (p.status === "publicado") return "Publicado";
  return "Sem data";
}

// Agendadas primeiro, por data; depois as publicadas; a reserva e o resto no fim.
function ordem(p: ContentPiece): string {
  if (p.corpo.programacao?.data) return `1 ${p.corpo.programacao.data} ${p.corpo.programacao.hora ?? ""}`;
  if (p.status === "publicado") return `2 ${p.criado_em}`;
  return `3 ${p.criado_em}`;
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
  const [escrevendo, setEscrevendo] = useState(false);
  const [pedido, setPedido] = useState("");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const router = useRouter();

  function abrir(p: ContentPiece | null) {
    setSelecionado(p);
    setAtual(0);
    setEscrevendo(false);
    setPedido("");
    setErro(null);
  }

  async function decidir(acao: () => Promise<ContentPiece>, falha: string) {
    setSalvando(true);
    setErro(null);
    try {
      const atualizado = await acao();
      setSelecionado(atualizado);
      setPieces((lista) => (lista ?? []).map((x) => (x.id === atualizado.id ? atualizado : x)));
      setEscrevendo(false);
      setPedido("");
    } catch {
      setErro(falha);
    } finally {
      setSalvando(false);
    }
  }

  useEffect(() => {
    apiFetch("/content").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      const data: ContentPiece[] = await resp.json();
      setPieces(
        data
          .filter((p) => p.tipo in TIPOS && (imagensDe(p).length > 0 || videoDe(p) !== null))
          .sort((a, b) => ordem(a).localeCompare(ordem(b))),
      );
    });
  }, [router]);

  const visiveis = useMemo(
    () =>
      (pieces ?? []).filter(
        (p) => passaNoFiltro(p, filtroStatus) && (filtroTipo === "todos" || p.tipo === filtroTipo),
      ),
    [pieces, filtroStatus, filtroTipo],
  );

  const imagens = selecionado ? imagensDe(selecionado) : [];
  const video = selecionado ? videoDe(selecionado) : null;

  async function baixarTodas() {
    if (!selecionado) return;
    setBaixando(true);
    try {
      if (video) {
        await baixar(video, `reels-${selecionado.id.slice(0, 8)}.mp4`);
        return;
      }
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
              {s === "todos" ? "Todos" : ROTULO_FILTRO[s]}
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
            const filme = videoDe(piece);
            return (
              <Card
                key={piece.id}
                className="cursor-pointer overflow-hidden p-0 transition-colors hover:border-primary/50"
                onClick={() => abrir(piece)}
              >
                {filme ? (
                  <div className="relative">
                    <video src={`${filme}#t=1`} muted playsInline preload="metadata" className="aspect-[4/5] w-full bg-black object-cover" />
                    <Film className="absolute right-2 top-2 h-5 w-5 text-white drop-shadow" />
                  </div>
                ) : (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={capa} alt={TIPOS[piece.tipo]} loading="lazy" className="aspect-[4/5] w-full bg-muted object-contain" />
                )}
                <div className="flex flex-col gap-1.5 p-3">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <Badge variant="secondary">{TIPOS[piece.tipo]}</Badge>
                    <Badge variant={piece.status === "rascunho" || piece.status === "ajuste" ? "outline" : "default"}>
                      {rotuloStatus(piece)}
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
            <Button variant="outline" size="sm" onClick={() => abrir(null)}>
              <ChevronLeft className="h-4 w-4" />
              Voltar
            </Button>
            <div className="flex items-center gap-1.5">
              <Badge variant="secondary">{TIPOS[selecionado.tipo]}</Badge>
              <Badge>{rotuloStatus(selecionado)}</Badge>
            </div>
            <Button size="sm" onClick={baixarTodas} disabled={baixando}>
              {baixando ? <Loader2 className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4" />}
              {video ? "Baixar vídeo" : imagens.length > 1 ? "Baixar todas" : "Baixar"}
            </Button>
          </div>

          {video ? (
            <video
              src={video}
              controls
              playsInline
              preload="metadata"
              className="w-full max-w-sm rounded-xl border border-border bg-black"
              style={{ aspectRatio: "9 / 16" }}
            />
          ) : (
            // eslint-disable-next-line @next/next/no-img-element
            <img
            src={imagens[atual]}
            alt={`${TIPOS[selecionado.tipo]} ${atual + 1}`}
            className="w-full max-w-xl rounded-xl border border-border bg-muted object-contain"
            style={{ aspectRatio: "4 / 5" }}
          />
          )}

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

          {selecionado.status !== "publicado" && (
            <Card className="flex w-full max-w-xl flex-col gap-3 p-4">
              {selecionado.status === "aprovado" && (
                <p className="text-sm text-primary">
                  <Check className="mr-1 inline h-4 w-4" />
                  Aprovado. Sai {quandoSai(selecionado.corpo.programacao)}.
                </p>
              )}
              {selecionado.status === "ajuste" && selecionado.corpo.pedido_alteracao?.texto && (
                <p className="text-sm">Ajuste pedido: {selecionado.corpo.pedido_alteracao.texto}</p>
              )}
              {escrevendo ? (
                <>
                  <textarea
                    autoFocus
                    rows={4}
                    value={pedido}
                    onChange={(e) => setPedido(e.target.value)}
                    placeholder="O que você quer ajustar? Ex.: trocar a foto, mudar o título, cortar um trecho do vídeo."
                    className="w-full rounded-md border border-border bg-background p-3 text-sm outline-none focus:border-primary"
                  />
                  <div className="flex gap-2">
                    <Button variant="outline" className="flex-1" disabled={salvando} onClick={() => setEscrevendo(false)}>
                      Cancelar
                    </Button>
                    <Button
                      className="flex-1"
                      disabled={salvando || !pedido.trim()}
                      onClick={() =>
                        decidir(
                          () => pedirAlteracaoPeca<ContentPiece>(selecionado.id, selecionado.corpo as Record<string, unknown>, pedido),
                          "Não foi possível enviar o pedido. Tente de novo.",
                        )
                      }
                    >
                      {salvando ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                      Enviar pedido de ajuste
                    </Button>
                  </div>
                </>
              ) : (
                <div className="flex gap-2">
                  <Button variant="outline" className="flex-1" disabled={salvando} onClick={() => setEscrevendo(true)}>
                    <MessageSquareText className="h-4 w-4" />
                    Pedir ajuste
                  </Button>
                  {selecionado.status !== "aprovado" && (
                    <Button
                      className="flex-1"
                      disabled={salvando}
                      onClick={() => decidir(() => aprovarPeca<ContentPiece>(selecionado.id), "Não foi possível aprovar. Tente de novo.")}
                    >
                      {salvando ? <Loader2 className="h-4 w-4 animate-spin" /> : <Check className="h-4 w-4" />}
                      Aprovar
                    </Button>
                  )}
                </div>
              )}
              {erro && <p className="text-sm text-destructive">{erro}</p>}
            </Card>
          )}
          {selecionado.corpo.legenda && (
            <Card className="w-full max-w-xl whitespace-pre-line p-4 text-sm">{selecionado.corpo.legenda}</Card>
          )}
        </div>
      )}
    </AppShell>
  );
}
