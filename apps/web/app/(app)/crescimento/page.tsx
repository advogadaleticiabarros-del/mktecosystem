"use client";

import { useEffect, useState } from "react";
import {
  Loader2,
  Eye,
  Clock,
  UserPlus,
  MessageCircle,
  AtSign,
  ThumbsUp,
  Film,
  Image as ImageIcon,
  Flame,
  Users,
} from "lucide-react";
import { useReducedMotion, motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

type Metricas = Record<string, number | string | undefined>;
type Registro = { id: string; coletado_em: string; metricas: Metricas };

// Mesma paleta categórica validada em visao-geral/page.tsx (dataviz, modo
// dark, superfície #352E26) — não trocar sem revalidar.
const COR_LINHA = "#B8862B";
const COR_LINHA_SECUNDARIA = "#2E8FD1";
const COR_INSTAGRAM = "#D1477A";
const COR_FACEBOOK = "#2E8FD1";

function formatarData(iso: string): string {
  return new Date(iso).toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
}

function formatarPeriodo(m: Metricas): string | null {
  if (!m.periodo_inicio || !m.periodo_fim) return null;
  const ini = new Date(String(m.periodo_inicio) + "T00:00:00").toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
  });
  const fim = new Date(String(m.periodo_fim) + "T00:00:00").toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
  });
  return `${ini} – ${fim}`;
}

function numero(v: number | string | undefined): number {
  if (typeof v === "number") return v;
  if (typeof v === "string") {
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  }
  return 0;
}

function texto(v: number | string | undefined): string {
  return v === undefined ? "—" : String(v);
}

function formatarValor(v: number, sufixo?: string): string {
  if (sufixo) return `${v}${sufixo}`;
  if (v >= 1000) return v.toLocaleString("pt-BR");
  return String(v);
}

function GraficoLinha({
  registros,
  campo,
  campoSecundario,
  labelPrincipal,
  labelSecundario,
  sufixo,
  corPrincipal = COR_LINHA,
  corSecundaria = COR_LINHA_SECUNDARIA,
}: {
  registros: Registro[];
  campo: string;
  campoSecundario?: string;
  labelPrincipal: string;
  labelSecundario?: string;
  sufixo?: string;
  corPrincipal?: string;
  corSecundaria?: string;
}) {
  const [hover, setHover] = useState<number | null>(null);
  const reduzirMovimento = useReducedMotion();
  const alturaMax = 128;

  const valores = registros.map((r) => numero(r.metricas[campo]));
  const valoresSecundarios = campoSecundario
    ? registros.map((r) => numero(r.metricas[campoSecundario]))
    : [];
  const teto = Math.max(1, ...valores, ...valoresSecundarios);
  // Arredonda o teto do eixo para um número "redondo" (não o valor bruto máximo),
  // assim as linhas de grade mostram marcos legíveis (ex.: 0/250/500/750/1000).
  const magnitude = Math.pow(10, Math.floor(Math.log10(teto || 1)));
  const tetoEixo = Math.ceil((teto * 1.15) / (magnitude / 2)) * (magnitude / 2) || 1;
  const marcos = [1, 0.75, 0.5, 0.25, 0];

  if (registros.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-2 py-10 text-center">
        <p className="text-xs text-muted-foreground">
          Sem registros ainda. Envie o primeiro print para começar a série histórica.
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 flex items-center gap-4 text-xs">
        <span className="flex items-center gap-1.5 font-medium text-foreground">
          <span className="h-2 w-2 rounded-full" style={{ background: corPrincipal }} />
          {labelPrincipal}
        </span>
        {campoSecundario && (
          <span className="flex items-center gap-1.5 font-medium text-foreground">
            <span className="h-2 w-2 rounded-full" style={{ background: corSecundaria }} />
            {labelSecundario}
          </span>
        )}
      </div>
      <div className="flex gap-2">
        {/* Eixo Y */}
        <div
          className="flex shrink-0 flex-col justify-between text-right text-[10px] text-muted-foreground"
          style={{ height: alturaMax }}
        >
          {marcos.map((m) => (
            <span key={m}>{formatarValor(Math.round(tetoEixo * m), sufixo)}</span>
          ))}
        </div>
        {/* Área do gráfico com grade de referência */}
        <div className="relative flex-1">
          <div
            className="absolute inset-x-0 top-0 flex flex-col justify-between"
            style={{ height: alturaMax }}
            aria-hidden
          >
            {marcos.map((m) => (
              <div key={m} className="border-t border-border/60" />
            ))}
          </div>
          <div className="relative flex items-end gap-3" style={{ height: alturaMax + 24 }}>
            {registros.map((r, i) => {
              const v = numero(r.metricas[campo]);
              const vSec = campoSecundario ? numero(r.metricas[campoSecundario]) : null;
              const emFoco = hover === i;
              return (
                <div
                  key={r.id}
                  className="group relative flex flex-1 cursor-default flex-col items-center gap-1.5"
                  onMouseEnter={() => setHover(i)}
                  onMouseLeave={() => setHover(null)}
                >
                  {emFoco && (
                    <div className="pointer-events-none absolute -top-3 left-1/2 z-10 w-max -translate-x-1/2 -translate-y-full rounded-lg border border-border bg-popover px-3 py-2 text-xs shadow-lg">
                      <p className="font-medium text-foreground">{formatarData(r.coletado_em)}</p>
                      <p className="mt-0.5 flex items-center gap-1.5 text-muted-foreground">
                        <span className="h-1.5 w-1.5 rounded-full" style={{ background: corPrincipal }} />
                        {labelPrincipal}: <span className="font-medium text-foreground">{formatarValor(v, sufixo)}</span>
                      </p>
                      {vSec !== null && (
                        <p className="flex items-center gap-1.5 text-muted-foreground">
                          <span className="h-1.5 w-1.5 rounded-full" style={{ background: corSecundaria }} />
                          {labelSecundario}: <span className="font-medium text-foreground">{formatarValor(vSec, sufixo)}</span>
                        </p>
                      )}
                    </div>
                  )}
                  <div
                    className="flex w-full items-end justify-center gap-1"
                    style={{ height: alturaMax }}
                  >
                    {reduzirMovimento ? (
                      <div
                        className={`w-3.5 rounded-t-sm transition-opacity ${emFoco ? "opacity-100" : "opacity-90 group-hover:opacity-100"}`}
                        style={{
                          background: corPrincipal,
                          height: Math.max(2, (v / tetoEixo) * alturaMax),
                        }}
                      />
                    ) : (
                      <motion.div
                        initial={{ height: 0 }}
                        animate={{ height: Math.max(2, (v / tetoEixo) * alturaMax) }}
                        transition={{ delay: i * 0.04, type: "spring", stiffness: 220, damping: 24 }}
                        className={`w-3.5 rounded-t-sm transition-opacity ${emFoco ? "opacity-100" : "opacity-90 group-hover:opacity-100"}`}
                        style={{ background: corPrincipal }}
                      />
                    )}
                    {campoSecundario &&
                      (reduzirMovimento ? (
                        <div
                          className={`w-3.5 rounded-t-sm transition-opacity ${emFoco ? "opacity-100" : "opacity-90 group-hover:opacity-100"}`}
                          style={{
                            background: corSecundaria,
                            height: Math.max(2, ((vSec ?? 0) / tetoEixo) * alturaMax),
                          }}
                        />
                      ) : (
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: Math.max(2, ((vSec ?? 0) / tetoEixo) * alturaMax) }}
                          transition={{ delay: i * 0.04 + 0.03, type: "spring", stiffness: 220, damping: 24 }}
                          className={`w-3.5 rounded-t-sm transition-opacity ${emFoco ? "opacity-100" : "opacity-90 group-hover:opacity-100"}`}
                          style={{ background: corSecundaria }}
                        />
                      ))}
                  </div>
                  <span
                    className={`text-[10px] tabular-nums transition-colors ${emFoco ? "font-medium text-foreground" : "text-muted-foreground"}`}
                  >
                    {formatarData(r.coletado_em)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

function BarraComparativa({
  label,
  itens,
}: {
  label: string;
  itens: { nome: string; valor: number; cor: string }[];
}) {
  const reduzirMovimento = useReducedMotion();
  const teto = Math.max(1, ...itens.map((i) => i.valor));
  return (
    <div>
      <p className="mb-3 text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</p>
      <div className="space-y-2.5">
        {itens.map((item, i) => (
          <div key={item.nome} className="flex items-center gap-3">
            <span className="w-24 shrink-0 truncate text-xs text-muted-foreground" title={item.nome}>
              {item.nome}
            </span>
            <div className="h-2 flex-1 overflow-hidden rounded-full bg-muted">
              {reduzirMovimento ? (
                <div
                  className="h-full rounded-full"
                  style={{ width: `${(item.valor / teto) * 100}%`, background: item.cor }}
                />
              ) : (
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(item.valor / teto) * 100}%` }}
                  transition={{ delay: i * 0.05, type: "spring", stiffness: 200, damping: 26 }}
                  className="h-full rounded-full"
                  style={{ background: item.cor }}
                />
              )}
            </div>
            <span className="w-12 shrink-0 text-right text-xs font-medium tabular-nums">
              {item.valor}
              {item.valor <= 100 ? "%" : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Ultimo(registros: Registro[], campo: string): number | string | undefined {
  if (registros.length === 0) return undefined;
  return registros[registros.length - 1].metricas[campo];
}

function Variacao(registros: Registro[], campo: string): number | undefined {
  if (registros.length < 2) return undefined;
  const atual = numero(registros[registros.length - 1].metricas[campo]);
  const anterior = numero(registros[registros.length - 2].metricas[campo]);
  if (anterior === 0) return undefined;
  return ((atual - anterior) / anterior) * 100;
}

function IndicadorVariacao({ valor, compacto = false }: { valor: number | undefined; compacto?: boolean }) {
  if (valor === undefined || !Number.isFinite(valor)) return null;
  const positivo = valor >= 0;
  return (
    <Badge
      variant="secondary"
      className={`mt-1 gap-1 font-mono text-[11px] ${
        positivo
          ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
          : "bg-red-500/10 text-red-600 dark:text-red-400"
      }`}
    >
      {positivo ? "↑" : "↓"} {Math.abs(valor).toFixed(1)}%{!compacto && " vs. semana anterior"}
    </Badge>
  );
}

export default function CrescimentoPage() {
  const [registros, setRegistros] = useState<Registro[] | null>(null);

  useEffect(() => {
    apiFetch("/dashboard/instagram-historico")
      .then((resp) => resp.json())
      .then((data) => setRegistros(data.registros))
      .catch(() => setRegistros([]));
  }, []);

  if (!registros) {
    return (
      <AppShell title="Crescimento" description="Aparecer, manter, reter, converter.">
        <div className="flex items-center justify-center py-24">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      </AppShell>
    );
  }

  const ultimo = registros.length > 0 ? registros[registros.length - 1].metricas : {};
  const periodo = formatarPeriodo(ultimo);

  return (
    <AppShell
      title="Crescimento"
      description="Acompanhamento semanal das redes sociais: aparecer, manter, reter e converter."
    >
      {periodo && (
        <p className="mb-4 text-xs text-muted-foreground">
          Último registro: período {periodo} · fonte: {texto(ultimo.fonte)}
        </p>
      )}

      {/* Funil principal */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="border-l-2 p-5" style={{ borderLeftColor: COR_LINHA }}>
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <Eye className="h-3.5 w-3.5" />
            Aparecer
          </div>
          <p className="mt-2 text-3xl font-semibold tabular-nums">
            {numero(Ultimo(registros, "alcance_nao_seguidores")).toLocaleString("pt-BR")}
          </p>
          <p className="text-xs text-muted-foreground">Alcance de não seguidores</p>
          <IndicadorVariacao compacto valor={Variacao(registros, "alcance_nao_seguidores")} />
        </Card>

        <Card className="border-l-2 p-5" style={{ borderLeftColor: COR_LINHA_SECUNDARIA }}>
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <Clock className="h-3.5 w-3.5" />
            Manter
          </div>
          <p className="mt-2 text-3xl font-semibold tabular-nums">
            {numero(Ultimo(registros, "interacoes_nao_seguidores_pct"))}%
          </p>
          <p className="text-xs text-muted-foreground">Interação de não seguidores</p>
          <IndicadorVariacao compacto valor={Variacao(registros, "interacoes_nao_seguidores_pct")} />
        </Card>

        <Card className="border-l-2 p-5" style={{ borderLeftColor: COR_INSTAGRAM }}>
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <UserPlus className="h-3.5 w-3.5" />
            Reter
          </div>
          <p className="mt-2 text-3xl font-semibold tabular-nums">
            {numero(Ultimo(registros, "seguidores_novos"))}
          </p>
          <p className="text-xs text-muted-foreground">
            Seguidores novos · {numero(Ultimo(registros, "cancelamentos_seguimento"))} cancelaram
          </p>
          <IndicadorVariacao compacto valor={Variacao(registros, "seguidores_novos")} />
        </Card>

        <Card className="border-l-2 p-5" style={{ borderLeftColor: "#22C55E" }}>
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <MessageCircle className="h-3.5 w-3.5" />
            Converter
          </div>
          <p className="mt-2 text-3xl font-semibold tabular-nums">
            {numero(Ultimo(registros, "conversas_iniciadas"))}
          </p>
          <p className="text-xs text-muted-foreground">Conversas iniciadas</p>
          <IndicadorVariacao compacto valor={Variacao(registros, "conversas_iniciadas")} />
        </Card>
      </div>

      {/* Gráficos do funil */}
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card className="p-5">
          <h3 className="mb-1 font-display text-sm font-semibold">Aparecer — Alcance</h3>
          <p className="mb-4 text-xs text-muted-foreground">
            Seguidores vs. não seguidores por semana. O objetivo é crescer a barra azul (fora da bolha).
          </p>
          <GraficoLinha
            registros={registros}
            campo="alcance_seguidores"
            campoSecundario="alcance_nao_seguidores"
            labelPrincipal="Seguidores"
            labelSecundario="Não seguidores"
          />
        </Card>

        <Card className="p-5">
          <h3 className="mb-1 font-display text-sm font-semibold">Manter — Interação de quem chega de fora</h3>
          <p className="mb-4 text-xs text-muted-foreground">
            % das interações vindas de não seguidores. Se está baixo, o gancho não está prendendo.
          </p>
          <GraficoLinha
            registros={registros}
            campo="interacoes_nao_seguidores_pct"
            labelPrincipal="Interação de não seguidores"
            sufixo="%"
          />
        </Card>

        <Card className="p-5">
          <h3 className="mb-1 font-display text-sm font-semibold">Reter — Seguidores</h3>
          <p className="mb-4 text-xs text-muted-foreground">
            Seguidores novos vs. cancelamentos por semana.
          </p>
          <GraficoLinha
            registros={registros}
            campo="seguidores_novos"
            campoSecundario="cancelamentos_seguimento"
            labelPrincipal="Novos"
            labelSecundario="Cancelamentos"
          />
        </Card>

        <Card className="p-5">
          <h3 className="mb-1 font-display text-sm font-semibold">Converter — Conversas e contactos</h3>
          <p className="mb-4 text-xs text-muted-foreground">
            Conversas iniciadas por semana — o sinal mais próximo de virar cliente.
          </p>
          <GraficoLinha
            registros={registros}
            campo="conversas_iniciadas"
            campoSecundario="novos_contactos"
            labelPrincipal="Conversas iniciadas"
            labelSecundario="Novos contactos"
          />
        </Card>
      </div>

      {/* Destaque: top post */}
      {ultimo.top_post_titulo && (
        <Card
          className="mt-6 overflow-hidden p-5"
          style={{
            background: `linear-gradient(135deg, ${COR_LINHA}12, transparent 60%)`,
          }}
        >
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide" style={{ color: COR_LINHA }}>
            <Flame className="h-3.5 w-3.5" />
            Conteúdo em destaque da semana
          </div>
          <p className="mt-2 font-display text-lg font-semibold">{texto(ultimo.top_post_titulo)}</p>
          <Separator className="my-3" />
          <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm">
            <span className="text-muted-foreground">{texto(ultimo.top_post_data)}</span>
            <span className="flex items-center gap-1.5 font-medium">
              👁️ {numero(ultimo.top_post_visualizacoes).toLocaleString("pt-BR")}
              <span className="font-normal text-muted-foreground">visualizações</span>
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              ❤️ {numero(ultimo.top_post_curtidas)}
              <span className="font-normal text-muted-foreground">curtidas</span>
            </span>
          </div>
        </Card>
      )}

      {/* Instagram vs Facebook lado a lado */}
      <h2 className="mb-3 mt-8 font-display text-base font-semibold text-muted-foreground">
        Instagram vs. Facebook
      </h2>
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="p-5">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <AtSign className="h-3.5 w-3.5" style={{ color: COR_INSTAGRAM }} />
            Instagram
          </div>
          <div className="mt-3 grid grid-cols-2 gap-3">
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.visualizacoes_total)}</p>
              <p className="text-xs text-muted-foreground">Visualizações totais</p>
            </div>
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.seguidores_total)}</p>
              <p className="text-xs text-muted-foreground">Seguidores totais</p>
            </div>
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.instagram_historias_visualizacoes_total)}</p>
              <p className="text-xs text-muted-foreground">Visualizações de Stories</p>
            </div>
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.instagram_historias_alcance)}</p>
              <p className="text-xs text-muted-foreground">Alcance de Stories</p>
            </div>
          </div>
          <div className="mt-4">
            <BarraComparativa
              label="Interação por tipo de mídia"
              itens={[
                { nome: "Foto", valor: numero(ultimo.instagram_interacoes_por_midia_foto), cor: COR_INSTAGRAM },
                { nome: "Reels", valor: numero(ultimo.instagram_interacoes_por_midia_reels), cor: COR_LINHA },
              ]}
            />
          </div>
        </Card>

        <Card className="p-5">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <ThumbsUp className="h-3.5 w-3.5" style={{ color: COR_FACEBOOK }} />
            Facebook
          </div>
          <div className="mt-3 grid grid-cols-2 gap-3">
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.facebook_publicacoes_visualizacoes)}</p>
              <p className="text-xs text-muted-foreground">Visualizações de publicações</p>
              <IndicadorVariacao compacto valor={numero(ultimo.facebook_publicacoes_visualizacoes_variacao_pct)} />
            </div>
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.facebook_publicacoes_interacoes)}</p>
              <p className="text-xs text-muted-foreground">Interações em publicações</p>
            </div>
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.facebook_reels_visualizacoes)}</p>
              <p className="text-xs text-muted-foreground">Visualizações de Reels</p>
              <IndicadorVariacao compacto valor={numero(ultimo.facebook_reels_visualizacoes_variacao_pct)} />
            </div>
            <div>
              <p className="text-lg font-semibold">{texto(ultimo.facebook_reels_tempo_visualizacao)}</p>
              <p className="text-xs text-muted-foreground">Tempo médio de visualização</p>
            </div>
          </div>
          <div className="mt-4">
            <BarraComparativa
              label="Conteúdos publicados no período"
              itens={[
                { nome: "Histórias", valor: numero(ultimo.facebook_conteudos_publicados_historias), cor: COR_FACEBOOK },
                { nome: "Fotos", valor: numero(ultimo.facebook_conteudos_publicados_fotos), cor: COR_LINHA },
                { nome: "Reels", valor: numero(ultimo.facebook_conteudos_publicados_reels), cor: COR_LINHA_SECUNDARIA },
              ]}
            />
          </div>
        </Card>
      </div>

      {/* Formatos de conteúdo */}
      <h2 className="mb-3 mt-8 font-display text-base font-semibold text-muted-foreground">
        Formatos de conteúdo
      </h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <Card className="p-5">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <Film className="h-3.5 w-3.5" />
            Publicações · interação
          </div>
          <p className="mt-2 text-2xl font-semibold">
            {numero(ultimo.instagram_publicacoes_interacoes)}
          </p>
          <p className="text-xs text-muted-foreground">
            {texto(ultimo.instagram_publicacoes_interacoes_periodo_anterior)}
          </p>
          <IndicadorVariacao valor={numero(ultimo.instagram_publicacoes_interacoes_variacao_pct)} />
        </Card>

        <Card className="p-5">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <ImageIcon className="h-3.5 w-3.5" />
            Volume publicado
          </div>
          <div className="mt-2 flex gap-6">
            <div>
              <p className="text-2xl font-semibold">{numero(ultimo.conteudo_stories_qtd)}</p>
              <p className="text-xs text-muted-foreground">Stories</p>
            </div>
            <div>
              <p className="text-2xl font-semibold">{numero(ultimo.conteudo_publicacoes_qtd)}</p>
              <p className="text-xs text-muted-foreground">Publicações</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Público-alvo: quem já segue vs. quem poderia seguir (a bolha a furar) */}
      <h2 className="mb-3 mt-8 font-display text-base font-semibold text-muted-foreground">
        Público-alvo
      </h2>
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="p-5">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <Users className="h-3.5 w-3.5" />
            Quem já segue hoje
          </div>
          <div className="mt-3 flex items-center gap-6">
            <div>
              <p className="text-2xl font-semibold">{numero(ultimo.publico_seguidores_mulheres_pct)}%</p>
              <p className="text-xs text-muted-foreground">Mulheres</p>
            </div>
            <div>
              <p className="text-2xl font-semibold">{numero(ultimo.publico_seguidores_homens_pct)}%</p>
              <p className="text-xs text-muted-foreground">Homens</p>
            </div>
            <div>
              <p className="text-2xl font-semibold">{texto(ultimo.publico_faixa_etaria_predominante)}</p>
              <p className="text-xs text-muted-foreground">Faixa etária predominante</p>
            </div>
          </div>
          {Array.isArray(ultimo.publico_cidades) && (
            <div className="mt-4">
              <BarraComparativa
                label="Principais cidades"
                itens={(ultimo.publico_cidades as unknown as { nome: string; pct: number }[])
                  .slice(0, 6)
                  .map((c) => ({ nome: c.nome, valor: c.pct, cor: COR_LINHA }))}
              />
            </div>
          )}
        </Card>

        <Card className="p-5">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
            <Flame className="h-3.5 w-3.5" />
            Público potencial — a bolha a furar
          </div>
          <p className="mt-2 text-2xl font-semibold">
            {ultimo.publico_potencial_min && ultimo.publico_potencial_max
              ? `${(numero(ultimo.publico_potencial_min) / 1_000_000).toFixed(0)} mi – ${(
                  numero(ultimo.publico_potencial_max) / 1_000_000
                ).toFixed(0)} mi`
              : "—"}
          </p>
          <p className="text-xs text-muted-foreground">
            Pessoas com o perfil certo, ainda fora do alcance atual (847/semana)
          </p>
          <div className="mt-3 flex gap-6">
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.publico_potencial_mulheres_pct)}%</p>
              <p className="text-xs text-muted-foreground">Mulheres</p>
            </div>
            <div>
              <p className="text-lg font-semibold">{numero(ultimo.publico_potencial_homens_pct)}%</p>
              <p className="text-xs text-muted-foreground">Homens</p>
            </div>
          </div>
          {Array.isArray(ultimo.publico_potencial_paginas_afins) && (
            <div className="mt-4">
              <BarraComparativa
                label="Páginas que esse público também segue"
                itens={(ultimo.publico_potencial_paginas_afins as unknown as { nome: string; pct: number }[])
                  .slice(0, 5)
                  .map((c) => ({ nome: c.nome, valor: c.pct, cor: COR_INSTAGRAM }))}
              />
            </div>
          )}
        </Card>
      </div>

      <p className="mt-6 text-xs text-muted-foreground">
        {registros.length} registro{registros.length === 1 ? "" : "s"} desde{" "}
        {registros.length > 0 ? formatarData(registros[0].coletado_em) : "—"}. Envie um print novo
        toda semana (visão geral, Reels, Stories, Facebook e público) para manter a série completa.
      </p>
    </AppShell>
  );
}
