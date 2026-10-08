"use client";

import { useEffect, useRef, useState } from "react";
import { dataCurta, numero } from "./tipos";

function useLargura<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  const [largura, setLargura] = useState(0);
  useEffect(() => {
    if (!ref.current) return;
    const ro = new ResizeObserver(([e]) => setLargura(e.contentRect.width));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  return [ref, largura] as const;
}

function teto(v: number) {
  if (v <= 0) return 1;
  const ordem = 10 ** Math.floor(Math.log10(v));
  const passo = [1, 2, 2.5, 5, 10].find((p) => p * ordem >= v / 4)! * ordem;
  return Math.ceil(v / passo) * passo;
}

/* ------------------------------------------------------------------ */
/* Linha de alcance diário: área suave, média tracejada, pico marcado,  */
/* cursor que mostra o valor do dia.                                    */
/* ------------------------------------------------------------------ */
export function LinhaAlcance({
  serie,
  media,
  pico,
}: {
  serie: { data: string; valor: number }[];
  media: number;
  pico: { data: string; valor: number } | null;
}) {
  const [ref, largura] = useLargura<HTMLDivElement>();
  const [foco, setFoco] = useState<number | null>(null);
  const altura = 240;
  const m = { esq: 44, dir: 16, topo: 20, base: 30 };
  const w = Math.max(largura - m.esq - m.dir, 10);
  const h = altura - m.topo - m.base;
  const max = teto(Math.max(...serie.map((p) => p.valor), media));
  const x = (i: number) => m.esq + (serie.length > 1 ? (i / (serie.length - 1)) * w : w / 2);
  const y = (v: number) => m.topo + h - (v / max) * h;
  const caminho = serie.map((p, i) => `${i ? "L" : "M"}${x(i)},${y(p.valor)}`).join("");
  const area = `${caminho}L${x(serie.length - 1)},${y(0)}L${x(0)},${y(0)}Z`;
  const ticksY = [0, max / 2, max];
  const passoX = Math.max(1, Math.round(serie.length / Math.max(2, Math.floor(w / 90))));
  const iPico = pico ? serie.findIndex((p) => p.data === pico.data) : -1;
  const atual = foco !== null ? serie[foco] : null;

  function mover(e: React.PointerEvent<SVGRectElement>) {
    const caixa = e.currentTarget.getBoundingClientRect();
    const rel = (e.clientX - caixa.left) / caixa.width;
    setFoco(Math.min(serie.length - 1, Math.max(0, Math.round(rel * (serie.length - 1)))));
  }

  return (
    <div ref={ref} className="relative w-full">
      {largura > 0 && (
        <svg width={largura} height={altura} role="img" aria-label="Contas alcançadas por dia">
          <defs>
            <linearGradient id="grad-alcance" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="var(--primary)" stopOpacity="0.22" />
              <stop offset="100%" stopColor="var(--primary)" stopOpacity="0" />
            </linearGradient>
          </defs>
          {ticksY.map((t) => (
            <g key={t}>
              <line x1={m.esq} x2={m.esq + w} y1={y(t)} y2={y(t)} stroke="var(--border)" />
              <text x={m.esq - 8} y={y(t) + 4} textAnchor="end" className="fill-muted-foreground font-mono text-[10px]">
                {numero(t)}
              </text>
            </g>
          ))}
          {serie.map((p, i) =>
            i % passoX === 0 ? (
              <text key={p.data} x={x(i)} y={altura - 8} textAnchor="middle" className="fill-muted-foreground font-mono text-[10px]">
                {dataCurta(p.data)}
              </text>
            ) : null,
          )}
          <path d={area} fill="url(#grad-alcance)" />
          <path d={caminho} fill="none" stroke="var(--primary)" strokeWidth={2} strokeLinejoin="round" />
          <line
            x1={m.esq}
            x2={m.esq + w}
            y1={y(media)}
            y2={y(media)}
            stroke="var(--muted-foreground)"
            strokeDasharray="4 4"
            strokeOpacity={0.7}
          />
          <text x={m.esq + w} y={y(media) - 6} textAnchor="end" className="fill-muted-foreground text-[11px]">
            média {numero(media)}/dia
          </text>
          {iPico >= 0 && pico && (
            <g>
              <circle cx={x(iPico)} cy={y(pico.valor)} r={5} fill="var(--primary)" stroke="var(--card)" strokeWidth={2} />
              <text
                x={x(iPico)}
                y={y(pico.valor) - 10}
                textAnchor={x(iPico) > m.esq + w - 80 ? "end" : "middle"}
                className="fill-foreground text-[11px] font-semibold"
              >
                pico {dataCurta(pico.data)} · {numero(pico.valor)}
              </text>
            </g>
          )}
          {atual && foco !== null && (
            <g pointerEvents="none">
              <line x1={x(foco)} x2={x(foco)} y1={m.topo} y2={m.topo + h} stroke="var(--foreground)" strokeOpacity={0.25} />
              <circle cx={x(foco)} cy={y(atual.valor)} r={4} fill="var(--primary)" stroke="var(--card)" strokeWidth={2} />
            </g>
          )}
          <rect
            x={m.esq}
            y={m.topo}
            width={w}
            height={h}
            fill="transparent"
            onPointerMove={mover}
            onPointerLeave={() => setFoco(null)}
          />
        </svg>
      )}
      {atual && foco !== null && (
        <div
          className="pointer-events-none absolute -translate-x-1/2 rounded-lg border bg-popover px-3 py-2 text-xs shadow-lg"
          style={{ left: Math.min(Math.max(x(foco), 70), largura - 70), top: 0 }}
        >
          <div className="font-mono text-muted-foreground">{dataCurta(atual.data)}</div>
          <div className="font-semibold">{numero(atual.valor)} contas</div>
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Barras horizontais com rótulo e valor direto.                       */
/* ------------------------------------------------------------------ */
export type ItemBarra = { rotulo: string; valor: number; cor?: string; detalhe?: string; destaque?: boolean };

export function BarrasHorizontais({ itens, sufixo = "" }: { itens: ItemBarra[]; sufixo?: string }) {
  const max = Math.max(...itens.map((i) => i.valor), 1);
  return (
    <ul className="space-y-2.5">
      {itens.map((item) => (
        <li key={item.rotulo} className="group grid grid-cols-[7.5rem_1fr_auto] items-center gap-3" title={item.detalhe}>
          <span className="truncate text-sm" title={item.rotulo}>
            {item.rotulo}
          </span>
          <span className="h-3 rounded-full bg-muted">
            <span
              className="block h-3 rounded-full transition-[filter] group-hover:brightness-110"
              style={{
                width: `${Math.max((item.valor / max) * 100, 2)}%`,
                background: item.cor ?? (item.destaque ? "var(--primary)" : "var(--muted-foreground)"),
                opacity: item.cor || item.destaque ? 1 : 0.45,
              }}
            />
          </span>
          <span className="min-w-14 text-right font-mono text-sm tabular-nums">
            {numero(item.valor)}
            {sufixo}
          </span>
        </li>
      ))}
    </ul>
  );
}

/* ------------------------------------------------------------------ */
/* Colunas verticais (horas, dias, meses). `fraco` = amostra pequena.   */
/* ------------------------------------------------------------------ */
export type ItemColuna = { rotulo: string; valor: number; detalhe: string; fraco?: boolean; destaque?: boolean };

export function Colunas({
  itens,
  altura = 180,
  cor = "var(--muted-foreground)",
  rotuloValor,
}: {
  itens: ItemColuna[];
  altura?: number;
  cor?: string;
  rotuloValor?: (v: number) => string;
}) {
  const [ref, largura] = useLargura<HTMLDivElement>();
  const [foco, setFoco] = useState<number | null>(null);
  const m = { topo: 22, base: 22 };
  const h = altura - m.topo - m.base;
  const max = Math.max(...itens.map((i) => i.valor), 1);
  const banda = largura / Math.max(itens.length, 1);
  const larguraBarra = Math.max(Math.min(banda * 0.62, 36), 3);
  const passoRotulo = Math.max(1, Math.ceil(52 / banda));
  const formatar = rotuloValor ?? numero;

  return (
    <div ref={ref} className="relative w-full">
      {largura > 0 && (
        <svg width={largura} height={altura} role="img" aria-label="Gráfico de colunas">
          <line x1={0} x2={largura} y1={m.topo + h} y2={m.topo + h} stroke="var(--border)" />
          {itens.map((item, i) => {
            const bh = Math.max((item.valor / max) * h, item.valor > 0 ? 2 : 0);
            const cx = i * banda + banda / 2;
            const realce = item.destaque || foco === i;
            return (
              <g key={item.rotulo} onPointerEnter={() => setFoco(i)} onPointerLeave={() => setFoco(null)}>
                <rect x={i * banda} y={m.topo} width={banda} height={h} fill="transparent" />
                <rect
                  x={cx - larguraBarra / 2}
                  y={m.topo + h - bh}
                  width={larguraBarra}
                  height={bh}
                  rx={Math.min(4, larguraBarra / 2)}
                  fill={item.destaque ? "var(--primary)" : cor}
                  fillOpacity={item.fraco ? 0.25 : item.destaque ? 1 : 0.55}
                  stroke={foco === i ? "var(--foreground)" : "none"}
                  strokeOpacity={0.3}
                />
                {realce && (
                  <text x={cx} y={m.topo + h - bh - 6} textAnchor="middle" className="fill-foreground font-mono text-[11px] font-semibold">
                    {formatar(item.valor)}
                  </text>
                )}
                {i % passoRotulo === 0 && (
                  <text
                    x={i === 0 ? Math.max(cx - banda / 2, 0) : i === itens.length - 1 ? Math.min(cx + banda / 2, largura) : cx}
                    y={altura - 6}
                    textAnchor={i === 0 ? "start" : i === itens.length - 1 ? "end" : "middle"}
                    className="fill-muted-foreground font-mono text-[10px]"
                  >
                    {item.rotulo}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
      )}
      {foco !== null && itens[foco] && (
        <div
          className="pointer-events-none absolute -translate-x-1/2 rounded-lg border bg-popover px-3 py-2 text-xs shadow-lg"
          style={{ left: Math.min(Math.max(foco * banda + banda / 2, 90), largura - 90), top: -8 }}
        >
          {itens[foco].detalhe}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Barra única de participação (100%), com legenda direta.             */
/* ------------------------------------------------------------------ */
export function Participacao({ itens }: { itens: { rotulo: string; pct: number; cor: string }[] }) {
  return (
    <div>
      <div className="flex h-4 w-full gap-0.5 overflow-hidden rounded-full">
        {itens.map((i) => (
          <span key={i.rotulo} style={{ width: `${i.pct}%`, background: i.cor }} title={`${i.rotulo}: ${i.pct}%`} />
        ))}
      </div>
      <div className="mt-3 flex flex-wrap gap-x-5 gap-y-1.5">
        {itens.map((i) => (
          <span key={i.rotulo} className="flex items-center gap-2 text-sm">
            <span className="h-2.5 w-2.5 rounded-sm" style={{ background: i.cor }} />
            {i.rotulo}
            <span className="font-mono font-semibold tabular-nums">{i.pct}%</span>
          </span>
        ))}
      </div>
    </div>
  );
}
