"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpRight, Loader2, RefreshCw, Sparkles } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BarrasHorizontais, Colunas, LinhaAlcance, Participacao } from "./_components/graficos";
import { COR_FORMATO, dataCurta, numero, type Analise, type PostRanking } from "./_components/tipos";

const CRITERIOS = [
  { chave: "alcance", rotulo: "Alcance", unidade: "contas" },
  { chave: "interacoes", rotulo: "Interações", unidade: "interações" },
  { chave: "compartilhamentos", rotulo: "Compartilhamentos", unidade: "envios" },
  { chave: "seguidores", rotulo: "Novos seguidores", unidade: "seguidores" },
] as const;

const CAMPO_CRITERIO: Record<(typeof CRITERIOS)[number]["chave"], keyof PostRanking> = {
  alcance: "alcance",
  interacoes: "interacoes",
  compartilhamentos: "compartilhamentos",
  seguidores: "seguidores_ganhos",
};

function vezes(a: number, b: number) {
  return (a / b).toLocaleString("pt-BR", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
}

function quando(iso: string | null) {
  if (!iso) return null;
  return new Date(iso).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
}

/* Uma pergunta, o gráfico que a responde e a leitura em português ao lado. */
function Secao({
  pergunta,
  explicacao,
  children,
  extra,
}: {
  pergunta: string;
  explicacao: string;
  children: React.ReactNode;
  extra?: React.ReactNode;
}) {
  return (
    <Card className="p-0 hover:translate-y-0">
      <div className="grid lg:grid-cols-[minmax(0,1fr)_19rem]">
        <div className="min-w-0 p-6">
          <h2 className="font-display text-lg font-semibold tracking-tight">{pergunta}</h2>
          <div className="mt-5">{children}</div>
        </div>
        <aside className="border-t bg-accent/50 p-6 lg:border-l lg:border-t-0">
          <p className="text-xs font-semibold text-primary">O que isso quer dizer</p>
          <p className="mt-2 text-sm leading-relaxed text-foreground/85">{explicacao}</p>
          {extra && <div className="mt-4">{extra}</div>}
        </aside>
      </div>
    </Card>
  );
}

function Diagnostico({ analise }: { analise: Analise }) {
  const itens = analise.formatos.itens;
  const melhor = itens[0];
  const maisUsado = itens.length ? itens.reduce((a, b) => (b.posts > a.posts ? b : a)) : undefined;
  const titulo =
    melhor && maisUsado && melhor !== maisUsado && maisUsado.alcance_tipico > 0
      ? `${melhor.formato} alcança ${vezes(melhor.alcance_tipico, maisUsado.alcance_tipico)}× mais que ${maisUsado.formato.toLowerCase()}, o formato mais publicado.`
      : analise.resumo.texto;

  return (
    <Card className="relative overflow-hidden p-0 hover:translate-y-0">
      <div className="absolute inset-y-0 left-0 w-1 bg-primary" />
      <div className="grid gap-8 p-7 lg:grid-cols-[minmax(0,1.25fr)_minmax(0,1fr)] lg:p-9">
        <div>
          <p className="flex items-center gap-2 text-xs font-semibold text-primary">
            <Sparkles className="h-3.5 w-3.5" /> Diagnóstico do Orbit
          </p>
          <p className="mt-3 font-display text-2xl font-semibold leading-snug tracking-tight lg:text-[1.75rem]">{titulo}</p>
          <p className="mt-4 text-sm leading-relaxed text-muted-foreground">{analise.resumo.texto}</p>
        </div>
        <div>
          <p className="text-xs font-semibold text-muted-foreground">O que fazer agora</p>
          <ul className="mt-3 space-y-3">
            {analise.recomendacoes.map((r) => (
              <li key={r} className="flex gap-3 text-sm leading-relaxed">
                <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                {r}
              </li>
            ))}
            {!analise.recomendacoes.length && <li className="text-sm text-muted-foreground">Nada urgente: siga o ciclo editorial.</li>}
          </ul>
        </div>
      </div>
    </Card>
  );
}

function Numeros({ analise }: { analise: Analise }) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {analise.resumo.kpis.map((k) => (
        <div key={k.chave} className="rounded-xl bg-card p-4 ring-1 ring-foreground/10">
          <p className="text-xs text-muted-foreground">{k.rotulo}</p>
          <p className="mt-1 font-display text-3xl font-semibold tabular-nums">{numero(k.valor)}</p>
          <p className="mt-2 text-xs leading-relaxed text-muted-foreground">{k.explicacao}</p>
        </div>
      ))}
    </div>
  );
}

function Ranking({ analise }: { analise: Analise }) {
  const [criterio, setCriterio] = useState<(typeof CRITERIOS)[number]>(CRITERIOS[0]);
  const lista = analise.ranking[criterio.chave];
  const campo = CAMPO_CRITERIO[criterio.chave];
  return (
    <Card className="p-0 hover:translate-y-0">
      <div className="p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="font-display text-lg font-semibold tracking-tight">Quais posts mais se destacaram?</h2>
            <p className="mt-1 max-w-2xl text-sm text-muted-foreground">{analise.ranking.explicacao}</p>
          </div>
          <div className="flex flex-wrap gap-1 rounded-lg bg-muted p-1" role="tablist">
            {CRITERIOS.map((c) => (
              <button
                key={c.chave}
                role="tab"
                aria-selected={c.chave === criterio.chave}
                onClick={() => setCriterio(c)}
                className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-primary ${
                  c.chave === criterio.chave ? "bg-card text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {c.rotulo}
              </button>
            ))}
          </div>
        </div>
        <ol className="mt-6 divide-y">
          {lista.map((p, i) => (
            <li key={p.media_id} className="grid grid-cols-[2rem_minmax(0,1fr)_auto] items-start gap-4 py-3.5">
              <span className="pt-0.5 font-mono text-sm text-muted-foreground">{i + 1}</span>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5 font-medium text-foreground">
                    <span className="h-2 w-2 rounded-full" style={{ background: COR_FORMATO[p.formato] }} />
                    {p.formato}
                  </span>
                  <span>{p.area}</span>
                  <span className="font-mono">{dataCurta(p.data)}/{p.data.slice(2, 4)}</span>
                </div>
                <p className="mt-1 line-clamp-2 text-sm">{p.legenda || "Post sem legenda"}</p>
              </div>
              <div className="text-right">
                <p className="font-display text-lg font-semibold tabular-nums">{numero(Number(p[campo]))}</p>
                <p className="text-[11px] text-muted-foreground">{criterio.unidade}</p>
                {p.permalink && (
                  <a
                    href={p.permalink}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-1 inline-flex items-center gap-0.5 text-[11px] font-medium text-primary hover:underline"
                  >
                    ver post <ArrowUpRight className="h-3 w-3" />
                  </a>
                )}
              </div>
            </li>
          ))}
          {!lista.length && <li className="py-6 text-sm text-muted-foreground">Ainda não há posts com esse dado.</li>}
        </ol>
      </div>
    </Card>
  );
}

export default function CrescimentoPage() {
  const router = useRouter();
  const [analise, setAnalise] = useState<Analise | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [atualizando, setAtualizando] = useState(false);

  useEffect(() => {
    apiFetch("/analise/instagram")
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then(setAnalise)
      .catch(() => setErro("Não foi possível carregar a análise. Confira a conexão e recarregue a página."));
  }, []);

  const atualizar = useCallback(async () => {
    setAtualizando(true);
    setErro(null);
    try {
      const r = await apiFetch("/analise/instagram/atualizar", { method: "POST" });
      if (!r.ok) throw new Error();
      setAnalise(await r.json());
    } catch {
      setErro("O Instagram não respondeu. Tente de novo em alguns minutos; se continuar, reconecte o Instagram na Visão geral.");
    } finally {
      setAtualizando(false);
    }
  }, []);

  const acoes = (
    <div className="flex items-center gap-3">
      {analise?.atualizado_em && (
        <span className="hidden text-xs text-muted-foreground sm:inline">Atualizado em {quando(analise.atualizado_em)}</span>
      )}
      <Button size="sm" variant="outline" onClick={() => router.push("/crescimento/auditoria")}>
        Auditoria do perfil
      </Button>
      <Button size="sm" variant="outline" onClick={atualizar} disabled={atualizando}>
        {atualizando ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RefreshCw className="h-3.5 w-3.5" />}
        {atualizando ? "Buscando no Instagram…" : "Atualizar dados"}
      </Button>
    </div>
  );

  const shell = (conteudo: React.ReactNode) => (
    <AppShell
      title="Crescimento"
      description="Como o Instagram está crescendo, o que funciona e o que fazer agora. Atualiza sozinho todo dia."
      headerActions={acoes}
    >
      {erro && <p className="mb-4 rounded-lg bg-destructive/10 px-4 py-3 text-sm text-destructive">{erro}</p>}
      {conteudo}
    </AppShell>
  );

  if (!analise) {
    return shell(
      !erro && (
        <div className="flex items-center justify-center py-24">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      ),
    );
  }

  if (!analise.total_posts) {
    return shell(
      <Card className="items-center p-12 text-center hover:translate-y-0">
        <p className="font-display text-xl font-semibold">Ainda não há dados do Instagram aqui</p>
        <p className="mt-2 max-w-md text-sm text-muted-foreground">
          O Orbit busca as publicações e as métricas todo dia às 6h. Para ver agora, busque os dados uma primeira vez.
        </p>
        <Button className="mt-6" onClick={atualizar} disabled={atualizando}>
          {atualizando ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
          Buscar dados do Instagram
        </Button>
      </Card>,
    );
  }

  const { formatos, areas, horarios, dias_semana, volume_mensal, publico, alcance_diario } = analise;
  const porHora = new Map(horarios.itens.map((h) => [h.hora, h]));
  const melhorHora = horarios.itens.filter((h) => h.posts >= 3).reduce((a, b) => (b.alcance_tipico > (a?.alcance_tipico ?? -1) ? b : a), undefined as (typeof horarios.itens)[number] | undefined);
  const melhorDia = dias_semana.itens.reduce((a, b) => (b.alcance_tipico > (a?.alcance_tipico ?? -1) ? b : a), undefined as (typeof dias_semana.itens)[number] | undefined);
  const corGenero = ["var(--fmt-imagem)", "var(--fmt-carrossel)", "var(--muted-foreground)"];

  return shell(
    <div className="space-y-6">
      <Diagnostico analise={analise} />
      <Numeros analise={analise} />

      {alcance_diario.serie.length > 0 && (
        <Secao pergunta="Quantas pessoas o perfil alcança por dia?" explicacao={alcance_diario.explicacao}>
          <LinhaAlcance serie={alcance_diario.serie} media={alcance_diario.media} pico={alcance_diario.pico} />
          <p className="mt-2 text-xs text-muted-foreground">Passe o mouse no gráfico para ver cada dia.</p>
        </Secao>
      )}

      <Secao
        pergunta="Qual formato chega a mais gente?"
        explicacao={formatos.explicacao}
        extra={<p className="text-xs leading-relaxed text-muted-foreground">Alcance típico = o meio da fila dos posts. Um post que viralizou não distorce a comparação.</p>}
      >
        <BarrasHorizontais
          sufixo=" contas"
          itens={formatos.itens.map((f) => ({
            rotulo: f.formato,
            valor: f.alcance_tipico,
            cor: COR_FORMATO[f.formato],
            detalhe: `${f.posts} posts`,
          }))}
        />
        <div className="mt-6 overflow-x-auto">
          <table className="w-full min-w-[560px] text-sm">
            <thead>
              <tr className="text-left text-xs text-muted-foreground">
                <th className="pb-2 font-medium">Formato</th>
                <th className="pb-2 text-right font-medium">Posts</th>
                <th className="pb-2 text-right font-medium">Interações típicas</th>
                <th className="pb-2 text-right font-medium">Compartilhamentos</th>
                <th className="pb-2 text-right font-medium">Salvamentos</th>
                <th className="pb-2 text-right font-medium">Seguidores trazidos</th>
              </tr>
            </thead>
            <tbody className="divide-y font-mono tabular-nums">
              {formatos.itens.map((f) => (
                <tr key={f.formato}>
                  <td className="py-2 font-sans">
                    <span className="flex items-center gap-2">
                      <span className="h-2.5 w-2.5 rounded-sm" style={{ background: COR_FORMATO[f.formato] }} />
                      {f.formato}
                    </span>
                  </td>
                  <td className="py-2 text-right">{numero(f.posts)}</td>
                  <td className="py-2 text-right">{numero(f.interacoes_tipicas)}</td>
                  <td className="py-2 text-right">{numero(f.compartilhamentos)}</td>
                  <td className="py-2 text-right">{numero(f.salvamentos)}</td>
                  <td className="py-2 text-right">{f.formato === "Reels" ? "—" : numero(f.seguidores_ganhos)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Secao>

      <Secao pergunta="Postar mais aumenta o alcance?" explicacao={volume_mensal.explicacao}>
        <p className="text-xs font-medium text-muted-foreground">Posts publicados por mês</p>
        <Colunas
          altura={130}
          itens={volume_mensal.itens.map((v) => ({ rotulo: v.rotulo, valor: v.posts, detalhe: `${v.rotulo}: ${v.posts} posts` }))}
        />
        <p className="mt-5 text-xs font-medium text-muted-foreground">Alcance médio de cada post no mês</p>
        <Colunas
          altura={150}
          cor="var(--primary)"
          itens={volume_mensal.itens.map((v) => ({
            rotulo: v.rotulo,
            valor: v.alcance_medio,
            detalhe: `${v.rotulo}: ${numero(v.alcance_medio)} contas por post`,
          }))}
        />
      </Secao>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card className="p-6 hover:translate-y-0">
          <h2 className="font-display text-lg font-semibold tracking-tight">Em que horário postar?</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            {melhorHora ? `Melhor horário até aqui: ${melhorHora.hora}h.` : "Ainda sem horários suficientes."} Barras claras têm menos de 3 posts.
          </p>
          <div className="mt-5">
            <Colunas
              itens={Array.from({ length: 24 }, (_, hora) => {
                const h = porHora.get(hora);
                return {
                  rotulo: `${hora}h`,
                  valor: h?.alcance_tipico ?? 0,
                  fraco: !h || h.posts < 3,
                  destaque: h === melhorHora,
                  detalhe: h ? `${hora}h: ${numero(h.alcance_tipico)} contas por post (${h.posts} posts)` : `${hora}h: nenhum post`,
                };
              })}
            />
          </div>
          <p className="mt-4 text-sm leading-relaxed text-foreground/85">{horarios.explicacao}</p>
        </Card>
        <Card className="p-6 hover:translate-y-0">
          <h2 className="font-display text-lg font-semibold tracking-tight">E em que dia da semana?</h2>
          <p className="mt-1 text-sm text-muted-foreground">{melhorDia ? `Melhor dia até aqui: ${melhorDia.dia}.` : ""}</p>
          <div className="mt-5">
            <Colunas
              itens={dias_semana.itens.map((d) => ({
                rotulo: d.dia.slice(0, 3),
                valor: d.alcance_tipico,
                destaque: d === melhorDia,
                detalhe: `${d.dia}: ${numero(d.alcance_tipico)} contas por post (${d.posts} posts)`,
              }))}
            />
          </div>
          <p className="mt-4 text-sm leading-relaxed text-foreground/85">{dias_semana.explicacao}</p>
        </Card>
      </div>

      <Secao pergunta="Quais áreas rendem mais?" explicacao={areas.explicacao}>
        <BarrasHorizontais
          sufixo=" contas"
          itens={[...areas.itens]
            .sort((a, b) => b.alcance_tipico - a.alcance_tipico)
            .map((a, i) => ({
              rotulo: `${a.area} (${a.posts})`,
              valor: a.alcance_tipico,
              destaque: i === 0,
              detalhe: `${a.posts} posts`,
            }))}
        />
        <p className="mt-3 text-xs text-muted-foreground">Entre parênteses, quantos posts de cada área. As barras mostram o alcance típico de cada post.</p>
      </Secao>

      <Ranking analise={analise} />

      {publico.genero.length > 0 && (
        <Secao pergunta="Quem acompanha o perfil?" explicacao={publico.explicacao}>
          <Participacao itens={publico.genero.map((g, i) => ({ rotulo: g.rotulo, pct: g.pct, cor: corGenero[i] ?? "var(--muted)" }))} />
          <div className="mt-8 grid gap-8 md:grid-cols-2">
            <div>
              <p className="mb-3 text-xs font-medium text-muted-foreground">Faixa de idade</p>
              <BarrasHorizontais
                sufixo="%"
                itens={publico.idade.map((i) => ({
                  rotulo: `${i.rotulo} anos`,
                  valor: i.pct,
                  destaque: i.valor === Math.max(...publico.idade.map((x) => x.valor)),
                }))}
              />
            </div>
            <div>
              <p className="mb-3 text-xs font-medium text-muted-foreground">Cidades com mais seguidores</p>
              <BarrasHorizontais
                itens={publico.cidades.map((c, i) => ({ rotulo: c.rotulo, valor: c.valor, destaque: i === 0, detalhe: `${c.pct}%` }))}
              />
            </div>
          </div>
        </Secao>
      )}

      <Card className="p-6 hover:translate-y-0">
        <h2 className="font-display text-base font-semibold">Facebook</h2>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          Os números da Página do Facebook entram aqui assim que a permissão de leitura da Página for liberada no app da Meta.
          Até lá, o Facebook não aparece nesta análise.
        </p>
      </Card>
    </div>,
  );
}
