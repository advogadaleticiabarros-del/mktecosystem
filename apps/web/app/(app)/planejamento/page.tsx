"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Archive,
  ArrowRight,
  BadgeCheck,
  ExternalLink,
  Loader2,
  MapPin,
  Newspaper,
  Plus,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  Trash2,
} from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type Fonte = { nome: string; url: string; data: string | null };
type Apuracao = {
  gancho?: string;
  fatos?: string;
  o_que_muda?: string;
  prazo?: string | null;
  local_es?: boolean;
  formatos?: { carrossel?: string; frase?: string; pergunta?: string };
  fontes?: Fonte[];
  verificacao?: { nivel: "oficial" | "confirmada" | "fonte_unica"; texto: string };
  pedido?: string | null;
};
type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  origem: string;
  fonte: string;
  status: string;
  conteudo_bruto: string | null;
  data_editorial: string | null;
  criado_em: string;
  apuracao: Apuracao | null;
  relevancia: number | null;
  urgencia: "alta" | "media" | "baixa" | null;
};

const ETAPAS = [
  { chave: "sugerida", rotulo: "Novas" },
  { chave: "aprovada", rotulo: "Aprovadas" },
  { chave: "em_producao", rotulo: "Em produção" },
  { chave: "guardada", rotulo: "Guardadas" },
] as const;
const AREAS = ["Trabalhista", "Família", "Previdenciário", "Consumidor"];
const PASSOS_APURACAO = [
  "Buscando notícias no Google Notícias e na Tavily…",
  "Juntando matérias que falam do mesmo fato…",
  "Conferindo quantos veículos confirmam cada fato…",
  "Escrevendo as pautas na voz do escritório…",
];

function quando(iso: string) {
  return new Date(iso).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
}

function Selo({ v }: { v?: Apuracao["verificacao"] }) {
  if (!v) return <span className="text-xs text-muted-foreground">Pauta manual</span>;
  const estilo = {
    oficial: { Icone: ShieldCheck, cls: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400", rotulo: "Fonte oficial" },
    confirmada: { Icone: BadgeCheck, cls: "bg-sky-500/10 text-sky-700 dark:text-sky-400", rotulo: "Confirmada" },
    fonte_unica: { Icone: ShieldAlert, cls: "bg-amber-500/15 text-amber-700 dark:text-amber-400", rotulo: "Fonte única" },
  }[v.nivel];
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-medium ${estilo.cls}`} title={v.texto}>
      <estilo.Icone className="h-3 w-3" /> {estilo.rotulo}
    </span>
  );
}

function Urgencia({ u }: { u: Pauta["urgencia"] }) {
  if (!u) return null;
  const cfg = {
    alta: ["bg-red-500", "Urgente"],
    media: ["bg-amber-400", "Esta semana"],
    baixa: ["bg-muted-foreground/40", "Sem pressa"],
  }[u];
  return (
    <span className="inline-flex items-center gap-1.5 text-[11px] text-muted-foreground">
      <span className={`h-2 w-2 rounded-full ${cfg[0]}`} /> {cfg[1]}
    </span>
  );
}

function Relevancia({ valor }: { valor: number | null }) {
  if (valor === null) return null;
  return (
    <span className="flex items-center gap-2" title={`Relevância ${valor} de 100`}>
      <span className="h-1.5 w-14 overflow-hidden rounded-full bg-muted">
        <span className="block h-full rounded-full bg-primary" style={{ width: `${valor}%` }} />
      </span>
      <span className="font-mono text-[11px] tabular-nums text-muted-foreground">{valor}</span>
    </span>
  );
}

function Jornalista({
  pautas,
  onApurar,
  apurando,
}: {
  pautas: Pauta[];
  onApurar: (foco?: string) => void;
  apurando: boolean;
}) {
  const [foco, setFoco] = useState("");
  const [passo, setPasso] = useState(0);
  useEffect(() => {
    if (!apurando) return setPasso(0);
    const t = setInterval(() => setPasso((p) => Math.min(p + 1, PASSOS_APURACAO.length - 1)), 9000);
    return () => clearInterval(t);
  }, [apurando]);

  const doJornalista = pautas.filter((p) => p.origem.startsWith("jornalista"));
  const ultima = doJornalista.reduce<string | null>((a, p) => (!a || p.criado_em > a ? p.criado_em : a), null);
  const novas = doJornalista.filter((p) => p.status === "sugerida");
  const urgentes = novas.filter((p) => p.urgencia === "alta").length;

  return (
    <Card className="relative overflow-hidden p-0 hover:translate-y-0">
      <div className="absolute inset-y-0 left-0 w-1 bg-primary" />
      <div className="grid gap-6 p-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)] lg:p-7">
        <div className="flex gap-4">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary/12 text-primary">
            <Newspaper className="h-5 w-5" />
          </div>
          <div>
            <p className="font-display text-lg font-semibold">Jornalista do Orbit</p>
            <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
              Todo dia às 7h40 ele lê as notícias das suas áreas, confere em quantos veículos cada fato saiu e entrega as pautas
              com fontes. Você só escolhe o que vira editorial.
            </p>
            <p className="mt-3 text-sm">
              {ultima ? (
                <>
                  Última ronda em <span className="font-medium">{quando(ultima)}</span> ·{" "}
                  <span className="font-medium">{novas.length}</span> pautas novas
                  {urgentes > 0 && (
                    <>
                      {" "}· <span className="font-medium text-red-600 dark:text-red-400">{urgentes} urgentes</span>
                    </>
                  )}
                </>
              ) : (
                "Ainda sem ronda. A primeira acontece amanhã às 7h40, ou agora mesmo pelo botão."
              )}
            </p>
          </div>
        </div>
        <div>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (foco.trim()) onApurar(foco.trim());
            }}
          >
            <label htmlFor="foco" className="text-xs font-medium text-muted-foreground">
              Peça uma pauta sobre um assunto
            </label>
            <div className="mt-1.5 flex gap-2">
              <div className="relative flex-1">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="foco"
                  value={foco}
                  onChange={(e) => setFoco(e.target.value)}
                  placeholder="Ex.: estabilidade da gestante, golpe do Pix, pensão em atraso"
                  className="h-10 pl-9"
                  disabled={apurando}
                />
              </div>
              <Button type="submit" className="h-10" disabled={apurando || !foco.trim()}>
                Apurar
              </Button>
            </div>
          </form>
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <Button variant="outline" size="sm" onClick={() => onApurar()} disabled={apurando}>
              {apurando ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RefreshCw className="h-3.5 w-3.5" />}
              Fazer a ronda agora
            </Button>
            {apurando && (
              <span className="text-xs text-muted-foreground" aria-live="polite">
                {PASSOS_APURACAO[passo]} (leva cerca de 1 minuto)
              </span>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
}

function Detalhe({
  pauta,
  onStatus,
  onGerar,
}: {
  pauta: Pauta;
  onStatus: (status: string) => void;
  onGerar: () => void;
}) {
  const a = pauta.apuracao;
  const formatos = a?.formatos ?? {};
  return (
    <Card className="gap-0 p-0 hover:translate-y-0">
      <div className="border-b p-6">
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="rounded-full bg-accent px-2 py-0.5 font-medium text-accent-foreground">{pauta.area || "Sem área"}</span>
          <span className="text-muted-foreground">{pauta.angulo === "sinceridade" ? "Ângulo: cautela" : "Ângulo: direitos"}</span>
          <Urgencia u={pauta.urgencia} />
          {a?.local_es && (
            <span className="inline-flex items-center gap-1 text-muted-foreground">
              <MapPin className="h-3 w-3" /> Espírito Santo
            </span>
          )}
        </div>
        <h2 className="mt-3 font-display text-2xl font-semibold leading-snug tracking-tight">{pauta.titulo}</h2>
        {a?.gancho && <p className="mt-2 text-sm text-muted-foreground">{a.gancho}</p>}
        {a?.prazo && (
          <p className="mt-3 inline-block rounded-md bg-red-500/10 px-2.5 py-1 text-xs font-medium text-red-700 dark:text-red-400">
            Prazo: {a.prazo}
          </p>
        )}
      </div>

      <div className="space-y-6 p-6">
        {a ? (
          <>
            <section>
              <h3 className="text-xs font-semibold text-primary">O que aconteceu</h3>
              <p className="mt-1.5 text-sm leading-relaxed">{a.fatos}</p>
            </section>
            <section>
              <h3 className="text-xs font-semibold text-primary">O que muda para a cliente</h3>
              <p className="mt-1.5 text-sm leading-relaxed">{a.o_que_muda}</p>
            </section>
            {(formatos.carrossel || formatos.frase || formatos.pergunta) && (
              <section>
                <h3 className="text-xs font-semibold text-primary">Como pode virar editorial</h3>
                <div className="mt-2 grid gap-2 sm:grid-cols-3">
                  {[
                    ["Pergunta", formatos.pergunta],
                    ["Frase", formatos.frase],
                    ["Carrossel", formatos.carrossel],
                  ].map(([rotulo, texto]) =>
                    texto ? (
                      <div key={rotulo} className="rounded-lg bg-muted/60 p-3">
                        <p className="text-[11px] font-medium text-muted-foreground">{rotulo}</p>
                        <p className="mt-1 text-sm leading-snug">{texto}</p>
                      </div>
                    ) : null,
                  )}
                </div>
              </section>
            )}
            <section>
              <div className="flex items-center justify-between gap-3">
                <h3 className="text-xs font-semibold text-primary">Fontes ({a.fontes?.length ?? 0})</h3>
                <Selo v={a.verificacao} />
              </div>
              <p className="mt-1 text-xs text-muted-foreground">{a.verificacao?.texto}</p>
              <ul className="mt-2 divide-y rounded-lg ring-1 ring-foreground/10">
                {a.fontes?.map((f) => (
                  <li key={f.url}>
                    <a
                      href={f.url}
                      target="_blank"
                      rel="noreferrer"
                      className="flex items-center justify-between gap-3 px-3 py-2.5 text-sm hover:bg-muted/50"
                    >
                      <span className="font-medium">{f.nome}</span>
                      <span className="flex items-center gap-2 text-xs text-muted-foreground">
                        {f.data && <span className="font-mono">{quando(f.data + "T12:00:00")}</span>}
                        <ExternalLink className="h-3.5 w-3.5" />
                      </span>
                    </a>
                  </li>
                ))}
              </ul>
            </section>
          </>
        ) : (
          <section>
            <h3 className="text-xs font-semibold text-primary">Material da pauta</h3>
            <p className="mt-1.5 whitespace-pre-line text-sm leading-relaxed text-muted-foreground">
              {pauta.conteudo_bruto || "Pauta criada à mão, sem material de apoio."}
            </p>
          </section>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2 border-t bg-accent/40 p-4">
        <Button onClick={onGerar}>
          {pauta.status === "em_producao" ? "Revisar conteúdo" : "Aprovar pauta e revisar"} <ArrowRight className="h-4 w-4" />
        </Button>
        {pauta.status !== "guardada" && (
          <Button variant="ghost" size="sm" onClick={() => onStatus("guardada")}>
            <Archive className="h-4 w-4" /> Guardar para depois
          </Button>
        )}
        {pauta.status === "guardada" && (
          <Button variant="ghost" size="sm" onClick={() => onStatus("sugerida")}>
            Voltar para novas
          </Button>
        )}
        <Button variant="ghost" size="sm" className="text-muted-foreground" onClick={() => onStatus("descartada")}>
          <Trash2 className="h-4 w-4" /> Descartar
        </Button>
      </div>
    </Card>
  );
}

function NovaPauta({ onCriada }: { onCriada: () => void }) {
  const [aberto, setAberto] = useState(false);
  const [titulo, setTitulo] = useState("");
  const [area, setArea] = useState("Trabalhista");
  const [angulo, setAngulo] = useState("direitos");
  if (!aberto) {
    return (
      <button
        onClick={() => setAberto(true)}
        className="flex w-full items-center justify-center gap-2 rounded-xl border border-dashed py-3 text-sm text-muted-foreground hover:border-primary hover:text-primary"
      >
        <Plus className="h-4 w-4" /> Criar pauta própria
      </button>
    );
  }
  return (
    <form
      className="space-y-3 rounded-xl bg-card p-4 ring-1 ring-foreground/10"
      onSubmit={async (e) => {
        e.preventDefault();
        await apiFetch("/pautas", { method: "POST", body: JSON.stringify({ titulo, area, angulo }) });
        setTitulo("");
        setAberto(false);
        onCriada();
      }}
    >
      <Input placeholder="Tema da pauta" value={titulo} onChange={(e) => setTitulo(e.target.value)} required autoFocus />
      <div className="flex flex-wrap gap-2">
        <select value={area} onChange={(e) => setArea(e.target.value)} className="h-9 rounded-md border bg-card px-3 text-sm">
          {AREAS.map((a) => (
            <option key={a}>{a}</option>
          ))}
        </select>
        <select value={angulo} onChange={(e) => setAngulo(e.target.value)} className="h-9 rounded-md border bg-card px-3 text-sm">
          <option value="direitos">Ângulo: direitos</option>
          <option value="sinceridade">Ângulo: cautela</option>
        </select>
        <Button type="submit" size="sm" className="h-9">
          Criar
        </Button>
        <Button type="button" variant="ghost" size="sm" className="h-9" onClick={() => setAberto(false)}>
          Cancelar
        </Button>
      </div>
    </form>
  );
}

export default function PlanejamentoPage() {
  const router = useRouter();
  const [pautas, setPautas] = useState<Pauta[] | null>(null);
  const [etapa, setEtapa] = useState<string>("sugerida");
  const [area, setArea] = useState<string | null>(null);
  const [selecionada, setSelecionada] = useState<string | null>(null);
  const [apurando, setApurando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    const r = await apiFetch("/pautas");
    if (r.status === 401) return router.push("/login");
    setPautas(await r.json());
  }, [router]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function apurar(foco?: string) {
    setApurando(true);
    setErro(null);
    try {
      const r = foco
        ? await apiFetch("/pautas/jornalista", { method: "POST", body: JSON.stringify({ foco }) })
        : await apiFetch("/pautas/buscar", { method: "POST" });
      if (!r.ok) throw new Error();
      const novas: Pauta[] = await r.json();
      await carregar();
      setEtapa("sugerida");
      setArea(null);
      setSelecionada(novas[0]?.id ?? null);
      if (!novas.length) setErro("O Jornalista não encontrou nada novo e confiável desta vez. Tente outro assunto ou mais tarde.");
    } catch {
      setErro("O Jornalista não conseguiu terminar a apuração. Tente de novo em alguns minutos.");
    } finally {
      setApurando(false);
    }
  }

  async function mudarStatus(id: string, status: string) {
    await apiFetch(`/pautas/${id}`, { method: "PATCH", body: JSON.stringify({ status }) });
    await carregar();
  }

  async function gerar(p: Pauta) {
    if (p.status === "sugerida" || p.status === "guardada") await mudarStatus(p.id, "aprovada");
    router.push(`/aprovacao?pautaId=${p.id}`);
  }

  const contagem = useMemo(() => {
    const c: Record<string, number> = {};
    for (const p of pautas ?? []) c[p.status] = (c[p.status] ?? 0) + 1;
    return c;
  }, [pautas]);

  const lista = useMemo(
    () =>
      (pautas ?? [])
        .filter((p) => p.status === etapa && (!area || p.area.toLowerCase().startsWith(area.toLowerCase().slice(0, 5))))
        .sort((a, b) => (b.relevancia ?? -1) - (a.relevancia ?? -1) || b.criado_em.localeCompare(a.criado_em)),
    [pautas, etapa, area],
  );
  const atual = lista.find((p) => p.id === selecionada) ?? lista[0];

  return (
    <AppShell title="Planejamento" description="A redação do Orbit: o Jornalista apura, você escolhe o que vira editorial.">
      <div className="space-y-6">
        <Jornalista pautas={pautas ?? []} onApurar={apurar} apurando={apurando} />
        {erro && <p className="rounded-lg bg-destructive/10 px-4 py-3 text-sm text-destructive">{erro}</p>}

        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap gap-1 rounded-lg bg-muted p-1" role="tablist">
            {ETAPAS.map((e) => (
              <button
                key={e.chave}
                role="tab"
                aria-selected={etapa === e.chave}
                onClick={() => {
                  setEtapa(e.chave);
                  setSelecionada(null);
                }}
                className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-primary ${
                  etapa === e.chave ? "bg-card text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {e.rotulo}
                <span className="ml-1.5 font-mono text-xs text-muted-foreground">{contagem[e.chave] ?? 0}</span>
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-1.5">
            {[null, ...AREAS].map((a) => (
              <button
                key={a ?? "todas"}
                onClick={() => setArea(a)}
                className={`rounded-full px-3 py-1 text-xs font-medium ring-1 transition-colors ${
                  area === a ? "bg-primary text-primary-foreground ring-primary" : "ring-foreground/10 hover:ring-primary/50"
                }`}
              >
                {a ?? "Todas as áreas"}
              </button>
            ))}
          </div>
        </div>

        {!pautas ? (
          <div className="flex justify-center py-20">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="grid gap-6 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
            <div className="space-y-2.5">
              {lista.map((p) => {
                const ativo = atual?.id === p.id;
                return (
                  <div key={p.id}>
                  <button
                    onClick={() => setSelecionada(p.id)}
                    className={`block w-full rounded-xl bg-card p-4 text-left ring-1 transition-all focus-visible:outline-2 focus-visible:outline-primary ${
                      ativo ? "ring-2 ring-primary" : "ring-foreground/10 hover:ring-primary/40"
                    }`}
                  >
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-xs font-medium text-primary">{p.area || "Sem área"}</span>
                      <Urgencia u={p.urgencia} />
                      <span className="ml-auto font-mono text-[11px] text-muted-foreground">{quando(p.criado_em)}</span>
                    </div>
                    <p className="mt-1.5 font-display text-[15px] font-semibold leading-snug">{p.titulo}</p>
                    {p.apuracao?.gancho && <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">{p.apuracao.gancho}</p>}
                    <div className="mt-3 flex flex-wrap items-center gap-3">
                      <Selo v={p.apuracao?.verificacao} />
                      {p.apuracao?.fontes && (
                        <span className="text-[11px] text-muted-foreground">
                          {p.apuracao.fontes.length} {p.apuracao.fontes.length === 1 ? "fonte" : "fontes"}
                        </span>
                      )}
                      <span className="ml-auto">
                        <Relevancia valor={p.relevancia} />
                      </span>
                    </div>
                  </button>
                  {/* No celular a apuração abre logo abaixo do card tocado */}
                  {selecionada === p.id && (
                    <div className="mt-2.5 lg:hidden">
                      <Detalhe pauta={p} onStatus={(st) => mudarStatus(p.id, st)} onGerar={() => gerar(p)} />
                    </div>
                  )}
                  </div>
                );
              })}
              {!lista.length && (
                <div className="rounded-xl border border-dashed p-8 text-center text-sm text-muted-foreground">
                  {etapa === "sugerida"
                    ? "Nenhuma pauta nova aqui. Peça uma ao Jornalista ou faça a ronda agora."
                    : "Nenhuma pauta nesta etapa."}
                </div>
              )}
              <NovaPauta onCriada={carregar} />
            </div>
            <div className="hidden lg:sticky lg:top-6 lg:block lg:self-start">
              {atual ? (
                <Detalhe pauta={atual} onStatus={(s) => mudarStatus(atual.id, s)} onGerar={() => gerar(atual)} />
              ) : (
                <div className="hidden rounded-xl border border-dashed p-10 text-center text-sm text-muted-foreground lg:block">
                  Escolha uma pauta para ver a apuração completa.
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
