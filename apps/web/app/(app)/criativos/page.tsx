"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, ChevronRight, Download, ImageIcon, Loader2 } from "lucide-react";
import { toPng } from "html-to-image";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

type ContentPiece = {
  id: string;
  tipo: string;
  corpo: { slides?: string[]; texto?: string };
  status: string;
  criado_em: string;
};

const MARCA = {
  fundo: "#231E1A",
  fundoAlt: "#2E2720",
  dourado: "#C9A962",
  douradoLight: "#D4BC7D",
  areia: "#E8DED1",
  branco: "#FAF6F0",
  instagram: "@adv.leticiabarros2",
  oab: "OAB/ES 39.948",
  nome: "Letícia Barros",
};

function Slide({
  texto,
  indice,
  total,
}: {
  texto: string;
  indice: number;
  total: number;
}) {
  const capa = indice === 0;
  const final = indice === total - 1;
  return (
    <div
      style={{
        boxSizing: "border-box",
        width: 1080,
        height: 1350,
        background: capa
          ? `radial-gradient(ellipse at 30% 20%, ${MARCA.fundoAlt}, ${MARCA.fundo} 70%)`
          : MARCA.fundo,
        color: MARCA.areia,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: 96,
        fontFamily: "Inter, sans-serif",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          right: -180,
          top: -180,
          width: 480,
          height: 480,
          borderRadius: "50%",
          border: `1px solid ${MARCA.dourado}33`,
        }}
      />
      <div
        style={{
          position: "absolute",
          right: -120,
          top: -120,
          width: 360,
          height: 360,
          borderRadius: "50%",
          border: `1px solid ${MARCA.dourado}22`,
        }}
      />

      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div
          style={{
            width: 40,
            height: 40,
            borderRadius: "50%",
            border: `2px solid ${MARCA.dourado}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: "50%",
              background: MARCA.dourado,
            }}
          />
        </div>
        <span style={{ fontSize: 26, letterSpacing: 2, color: MARCA.douradoLight }}>
          {MARCA.nome.toUpperCase()}
        </span>
      </div>

      <div style={{ flex: 1, display: "flex", alignItems: "center" }}>
        <p
          style={{
            fontSize: capa ? 72 : final ? 60 : 52,
            lineHeight: 1.25,
            fontWeight: capa || final ? 700 : 500,
            color: capa ? MARCA.branco : MARCA.areia,
            margin: 0,
            minWidth: 0,
          }}
        >
          {texto}
        </p>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderTop: `1px solid ${MARCA.dourado}44`,
          paddingTop: 32,
        }}
      >
        <span style={{ fontSize: 24, color: MARCA.dourado }}>{MARCA.instagram}</span>
        <span style={{ fontSize: 22, color: `${MARCA.areia}99` }}>
          {final ? MARCA.oab : `${indice + 1} / ${total}`}
        </span>
      </div>
    </div>
  );
}

export default function CriativosPage() {
  const [pieces, setPieces] = useState<ContentPiece[]>([]);
  const [selecionado, setSelecionado] = useState<ContentPiece | null>(null);
  const [slideAtual, setSlideAtual] = useState(0);
  const [exportando, setExportando] = useState(false);
  const slideRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    apiFetch("/content?tipo=carrossel&status=aprovado").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      const data: ContentPiece[] = await resp.json();
      setPieces(data.filter((p) => Array.isArray(p.corpo.slides)));
    });
  }, [router]);

  const slides = selecionado?.corpo.slides ?? [];

  async function exportarTodas() {
    if (!selecionado || !slideRef.current) return;
    setExportando(true);
    try {
      const original = slideAtual;
      for (let i = 0; i < slides.length; i++) {
        setSlideAtual(i);
        await new Promise((r) => setTimeout(r, 150));
        const dataUrl = await toPng(slideRef.current, {
          width: 1080,
          height: 1350,
          pixelRatio: 1,
        });
        const link = document.createElement("a");
        link.download = `carrossel-slide-${i + 1}.png`;
        link.href = dataUrl;
        link.click();
        await new Promise((r) => setTimeout(r, 300));
      }
      setSlideAtual(original);
    } finally {
      setExportando(false);
    }
  }

  return (
    <AppShell
      title="Estúdio de criativos"
      description="Artes geradas automaticamente do conteúdo aprovado, na identidade da marca"
    >
      {pieces.length === 0 && !selecionado && (
        <Card className="flex flex-col items-center gap-3 p-12 text-center">
          <ImageIcon className="h-8 w-8 text-primary" />
          <p className="font-display text-lg font-semibold">Nenhum carrossel aprovado ainda</p>
          <p className="max-w-md text-sm text-muted-foreground">
            Aprove um carrossel na tela de Aprovação e ele aparece aqui pronto para virar
            arte — capa, slides e CTA final com a identidade visual completa.
          </p>
        </Card>
      )}

      {!selecionado && pieces.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {pieces.map((piece) => (
            <Card
              key={piece.id}
              className="cursor-pointer p-5 transition-colors hover:border-primary/50"
              onClick={() => {
                setSelecionado(piece);
                setSlideAtual(0);
              }}
            >
              <Badge variant="secondary" className="mb-3">
                {piece.corpo.slides?.length ?? 0} slides
              </Badge>
              <p className="line-clamp-3 text-sm">{piece.corpo.slides?.[0]}</p>
              <p className="mt-3 text-xs text-muted-foreground">
                {new Date(piece.criado_em).toLocaleDateString("pt-BR")}
              </p>
            </Card>
          ))}
        </div>
      )}

      {selecionado && (
        <div className="flex flex-col items-center gap-5">
          <div className="flex w-full max-w-2xl items-center justify-between">
            <Button variant="outline" size="sm" onClick={() => setSelecionado(null)}>
              <ChevronLeft className="h-4 w-4" />
              Voltar
            </Button>
            <Button onClick={exportarTodas} disabled={exportando}>
              {exportando ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Download className="h-4 w-4" />
              )}
              {exportando ? "Exportando..." : "Baixar todas (PNG)"}
            </Button>
          </div>

          <div
            className="overflow-hidden rounded-xl border border-border"
            style={{ width: 432, height: 540 }}
          >
            <div style={{ transform: "scale(0.4)", transformOrigin: "top left" }}>
              <div ref={slideRef}>
                <Slide texto={slides[slideAtual] ?? ""} indice={slideAtual} total={slides.length} />
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              disabled={slideAtual === 0}
              onClick={() => setSlideAtual((s) => s - 1)}
              aria-label="Slide anterior"
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            {slides.map((_, i) => (
              <button
                key={i}
                type="button"
                onClick={() => setSlideAtual(i)}
                aria-label={`Slide ${i + 1}`}
                className={cn(
                  "h-2 w-2 rounded-full transition-colors",
                  i === slideAtual ? "bg-primary" : "bg-border",
                )}
              />
            ))}
            <Button
              variant="outline"
              size="sm"
              disabled={slideAtual === slides.length - 1}
              onClick={() => setSlideAtual((s) => s + 1)}
              aria-label="Próximo slide"
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </AppShell>
  );
}
