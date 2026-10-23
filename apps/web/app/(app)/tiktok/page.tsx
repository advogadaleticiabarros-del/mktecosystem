"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Check, Copy, Loader2, X } from "lucide-react";
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
type NaFila = { id: string; titulo: string; data: string; horario: string; video: string | null };
type EmProducao = {
  id: string;
  titulo: string;
  status: "para_gravar" | "para_editar";
  data_prevista: string | null;
  gancho: string | null;
  fala: string | null;
  fecho: string | null;
  palavra_chave: string | null;
  fonte: string | null;
  origem: string | null;
};
type Situacao = {
  conectado: boolean;
  nome: string | null;
  desde: string | null;
  fila: NaFila[];
  producao: EmProducao[];
  no_rascunho: Envio[];
  ultimos: Envio[];
};

const DIA_SEMANA = ["dom", "seg", "ter", "qua", "qui", "sex", "sáb"];

function diaCurto(iso: string) {
  const [a, m, d] = iso.split("-").map(Number);
  const dia = new Date(a, m - 1, d);
  return `${DIA_SEMANA[dia.getDay()]} ${String(d).padStart(2, "0")}/${String(m).padStart(2, "0")}`;
}

function ItemProducao({ p }: { p: EmProducao }) {
  const gravar = p.status === "para_gravar";
  return (
    <li className="py-2 text-sm">
      <details>
        <summary className="flex cursor-pointer flex-wrap items-center gap-2">
          <span className="w-24 shrink-0 font-medium tabular-nums">{p.data_prevista ? diaCurto(p.data_prevista) : "sem data"}</span>
          <span className="min-w-0 flex-1">{p.titulo}</span>
          <span className={`rounded-full px-2 py-0.5 text-xs ${gravar ? "bg-primary/15 text-primary" : "bg-muted"}`}>
            {gravar ? "Dra. grava" : "Corte (edição)"}
          </span>
        </summary>
        <div className="mt-2 space-y-1.5 rounded bg-muted/50 p-3">
          {p.gancho && <p><span className="font-medium">Gancho:</span> {p.gancho}</p>}
          {p.fala && <p><span className="font-medium">Fala:</span> {p.fala}</p>}
          {p.fecho && <p><span className="font-medium">Fecho:</span> {p.fecho}</p>}
          {p.origem && <p><span className="font-medium">Trecho:</span> {p.origem}</p>}
          {p.palavra_chave && <p className="text-xs text-muted-foreground">Palavra-chave: {p.palavra_chave}</p>}
          {p.fonte && <p className="text-xs text-muted-foreground">Fonte: {p.fonte}</p>}
        </div>
      </details>
    </li>
  );
}

function ItemFila({ f, aoMudar }: { f: NaFila; aoMudar: (vaga: { data: string | null; horario?: string }) => Promise<void> }) {
  const [editando, setEditando] = useState(false);
  const [data, setData] = useState(f.data);
  const [horario, setHorario] = useState(f.horario);
  const [ocupado, setOcupado] = useState(false);

  async function mudar(vaga: { data: string | null; horario?: string }) {
    setOcupado(true);
    await aoMudar(vaga);
    setOcupado(false);
    setEditando(false);
  }

  return (
    <li className="flex flex-wrap items-center gap-2 py-2 text-sm">
      <span className="w-28 shrink-0 font-medium tabular-nums">{diaCurto(f.data)} · {f.horario}</span>
      <span className="min-w-0 flex-1 truncate">{f.titulo}</span>
      {!editando && (
        <div className="flex gap-2">
          <Button size="xs" variant="outline" onClick={() => setEditando(true)}>Mudar data</Button>
          <Button size="xs" variant="ghost" disabled={ocupado} onClick={() => mudar({ data: null })}>
            <X /> Tirar do TikTok
          </Button>
        </div>
      )}
      {editando && (
        <div className="flex w-full flex-wrap items-center gap-2">
          <input type="date" value={data} onChange={(e) => setData(e.target.value)} className="rounded-md border bg-background px-2 py-1 text-sm" />
          <input type="time" value={horario} onChange={(e) => setHorario(e.target.value)} className="rounded-md border bg-background px-2 py-1 text-sm" />
          <Button size="xs" disabled={ocupado || !data || !horario} onClick={() => mudar({ data, horario })}>
            {ocupado ? <Loader2 className="animate-spin" /> : <Check />} Salvar
          </Button>
          <Button size="xs" variant="ghost" onClick={() => setEditando(false)}>Cancelar</Button>
        </div>
      )}
    </li>
  );
}

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
    <AppShell title="TikTok" description="Agenda própria do TikTok: 5 vídeos por semana, em horários escolhidos para o TikTok, sem esperar o Instagram.">
      {s && !s.conectado && (
        <Card className="mb-6 p-6 text-sm hover:translate-y-0">
          <p className="font-medium">O TikTok ainda não está conectado.</p>
          <p className="mt-1 text-muted-foreground">Conecte no card do TikTok da Visão Geral, entrando com a conta do TikTok da Dra.</p>
        </Card>
      )}
      {s?.conectado && (
        <p className="mb-6 text-sm text-muted-foreground">
          Conectado como <span className="font-medium text-foreground">{s.nome}</span>
        </p>
      )}
      <div className="space-y-6">
        <Secao
          titulo="Esperando publicar no app do TikTok"
          descricao="Enquanto o app do Orbit não passa pela auditoria da TikTok, o vídeo vai para a caixa de rascunhos do TikTok no horário da fila. No celular: abra a notificação, toque em Adicionar som → Sons comerciais → Em alta, escolha um som que combine, baixe o volume do som para 10% a 15% (a voz da Dra. fica em 100%), cole a legenda e publique."
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
        <Secao
          titulo="Fila do TikTok"
          descricao="Cada Reels aprovado entra sozinho na próxima vaga livre (dom 10h, seg 18h, ter 12h, qua 20h, qui 18h), na ordem das séries. Dá para mudar a data ou tirar um vídeo do TikTok."
        >
          {!s?.fila.length && <p className="text-sm text-muted-foreground">Fila vazia.</p>}
          <ul className="divide-y">
            {s?.fila.map((f) => (
              <ItemFila key={`${f.id}-${f.data}-${f.horario}`} f={f} aoMudar={async (vaga) => {
                await apiFetch(`/tiktok/${f.id}/agenda`, { method: "PUT", body: JSON.stringify(vaga) });
                await carregar();
              }} />
            ))}
          </ul>
        </Secao>
        <Secao
          titulo="Para gravar e editar (25/11 a 31/12)"
          descricao="Pauta do TikTok depois que os Reels prontos acabam. Roteiros para a Dra. gravar até 20/11 (na vertical, uns 30 segundos, começando direto na pergunta) e cortes de Reels prontos com gancho novo. Toque num item para ver o roteiro. Com o vídeo pronto e aprovado, ele entra na fila sozinho."
        >
          {!s?.producao?.length && <p className="text-sm text-muted-foreground">Nada em produção.</p>}
          <ul className="divide-y">
            {s?.producao?.map((p) => <ItemProducao key={p.id} p={p} />)}
          </ul>
        </Secao>
        <Secao titulo="Últimos envios" descricao="Cada vídeo vai uma única vez ao TikTok.">
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
