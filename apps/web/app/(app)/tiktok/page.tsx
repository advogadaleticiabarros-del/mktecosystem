"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Check, Copy, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Secao } from "../presenca/_components/comuns";

type Envio = {
  id: string;
  titulo: string;
  status: "publicado" | "no_rascunho" | "tentando" | "erro";
  modo: "publico" | "rascunho" | null;
  em: string | null;
  motivo: string | null;
  legenda: string;
  video: string | null;
};
type Situacao = { conectado: boolean; nome: string | null; desde: string | null; no_rascunho: Envio[]; ultimos: Envio[] };

const NOME_STATUS: Record<Envio["status"], string> = {
  publicado: "Publicado",
  no_rascunho: "Na caixa do TikTok",
  tentando: "Tentando de novo",
  erro: "Erro",
};

function quando(iso: string | null) {
  return iso ? new Date(iso).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "";
}

function Rascunho({ e, aoPublicar }: { e: Envio; aoPublicar: () => Promise<void> }) {
  const [copiado, setCopiado] = useState(false);
  const [ocupado, setOcupado] = useState(false);

  async function copiar() {
    try {
      await navigator.clipboard.writeText(e.legenda);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 2500);
    } catch {
      setCopiado(false);
    }
  }

  return (
    <li className="rounded-md border p-3">
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
        <span className="font-medium">{e.titulo}</span>
        <span className="text-muted-foreground">enviado em {quando(e.em)}</span>
      </div>
      <p className="mt-2 max-h-40 overflow-y-auto whitespace-pre-line rounded bg-muted/50 p-2 text-sm">{e.legenda}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        <Button size="xs" variant="outline" onClick={copiar}>{copiado ? <Check /> : <Copy />} {copiado ? "Copiada" : "Copiar legenda"}</Button>
        <Button size="xs" disabled={ocupado} onClick={async () => { setOcupado(true); await aoPublicar(); setOcupado(false); }}>
          {ocupado ? <Loader2 className="animate-spin" /> : <Check />} Já publiquei no TikTok
        </Button>
      </div>
    </li>
  );
}

export default function TiktokPage() {
  const router = useRouter();
  const [s, setS] = useState<Situacao | null>(null);

  const carregar = useCallback(async () => {
    const r = await apiFetch("/tiktok");
    if (r.status === 401) return router.push("/login");
    if (r.ok) setS(await r.json());
  }, [router]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return (
    <AppShell title="TikTok" description="Os Reels do Instagram vão também para o TikTok, no mesmo dia e com a mesma legenda.">
      {s && !s.conectado && (
        <Card className="mb-6 p-6 text-sm hover:translate-y-0">
          <p className="font-medium">O TikTok ainda não está conectado.</p>
          <p className="mt-1 text-muted-foreground">Conecte no card do TikTok da Visão Geral, entrando com a conta do TikTok da Dra.</p>
        </Card>
      )}
      {s?.conectado && (
        <p className="mb-6 text-sm text-muted-foreground">
          Conectado como <span className="font-medium text-foreground">{s.nome}</span>
          {s.desde && <> · envia os Reels do Instagram a partir de {new Date(s.desde).toLocaleDateString("pt-BR")}</>}
        </p>
      )}
      <div className="space-y-6">
        <Secao
          titulo="Esperando publicar no app do TikTok"
          descricao="Enquanto o app do Orbit não passa pela auditoria da TikTok, ela não deixa publicar público direto pela API. O Orbit manda o vídeo para a caixa de rascunhos do TikTok: abra a notificação no celular, cole a legenda e publique. Depois da auditoria, sai sozinho."
        >
          {!s?.no_rascunho.length && <p className="text-sm text-muted-foreground">Nada esperando agora.</p>}
          <ul className="space-y-3">
            {s?.no_rascunho.map((e) => (
              <Rascunho key={e.id} e={e} aoPublicar={async () => {
                await apiFetch(`/tiktok/${e.id}/publicado`, { method: "POST" });
                await carregar();
              }} />
            ))}
          </ul>
        </Secao>
        <Secao titulo="Últimos envios" descricao="Cada Reels vai uma única vez, depois do horário do Instagram.">
          {!s?.ultimos.length && <p className="text-sm text-muted-foreground">Nenhum envio ainda.</p>}
          <ul className="divide-y text-sm">
            {s?.ultimos.map((e) => (
              <li key={e.id} className="flex flex-wrap items-center justify-between gap-2 py-2">
                <span className="min-w-0 flex-1 truncate">{e.titulo}</span>
                <span className={`rounded-full px-2 py-0.5 text-xs ${e.status === "erro" ? "bg-destructive/15 text-destructive" : "bg-muted"}`}>{NOME_STATUS[e.status]}</span>
                <span className="text-xs text-muted-foreground">{quando(e.em)}</span>
                {e.motivo && e.status !== "publicado" && <span className="w-full text-xs text-destructive">{e.motivo}</span>}
              </li>
            ))}
          </ul>
        </Secao>
      </div>
    </AppShell>
  );
}
