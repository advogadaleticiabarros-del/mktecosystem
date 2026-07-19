"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  BarChart3,
  CalendarClock,
  Camera,
  FileText,
  Mail,
  MapPin,
  Users,
} from "lucide-react";
import { motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

type Resumo = {
  conteudos_por_status: Record<string, number>;
  contatos_por_origem: Record<string, number>;
  contatos_ativos: number;
  emails_enviados: number;
  pautas_total: number;
  producao_semanal: { semana: string; pautas: number; conteudos: number }[];
  proximos_agendamentos: {
    id: string;
    titulo: string;
    canal: string;
    data_agendada: string;
    horario: string;
    status: string;
  }[];
};

// Paleta categórica validada (dataviz, modo dark, superfície #352E26):
// todas as 5 verificações passam — não trocar sem revalidar.
const COR_CONTEUDOS = "#B8862B";
const COR_PAUTAS = "#2E8FD1";

function BarrasSemanais({ dados }: { dados: Resumo["producao_semanal"] }) {
  const [hover, setHover] = useState<number | null>(null);
  const alturaMax = 120;
  const teto = Math.max(1, ...dados.map((d) => Math.max(d.pautas, d.conteudos)));

  return (
    <div>
      <div className="mb-3 flex items-center gap-4 text-xs text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-sm" style={{ background: COR_PAUTAS }} />
          Pautas
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2.5 w-2.5 rounded-sm" style={{ background: COR_CONTEUDOS }} />
          Conteúdos
        </span>
      </div>
      <div className="flex items-end gap-3" style={{ height: alturaMax + 24 }}>
        {dados.map((d, i) => (
          <div
            key={d.semana}
            className="relative flex flex-1 cursor-default flex-col items-center gap-1"
            onMouseEnter={() => setHover(i)}
            onMouseLeave={() => setHover(null)}
          >
            {hover === i && (
              <div className="absolute -top-12 z-10 whitespace-nowrap rounded-md border border-border bg-popover px-2.5 py-1.5 text-xs">
                <span className="text-muted-foreground">
                  {new Date(d.semana + "T00:00:00").toLocaleDateString("pt-BR", {
                    day: "2-digit",
                    month: "short",
                  })}
                  :
                </span>{" "}
                {d.pautas} pautas · {d.conteudos} conteúdos
              </div>
            )}
            <div className="flex w-full items-end justify-center gap-0.5" style={{ height: alturaMax }}>
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: Math.max(2, (d.pautas / teto) * alturaMax) }}
                transition={{ delay: i * 0.04 }}
                className="w-3 rounded-t"
                style={{ background: COR_PAUTAS }}
              />
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: Math.max(2, (d.conteudos / teto) * alturaMax) }}
                transition={{ delay: i * 0.04 + 0.02 }}
                className="w-3 rounded-t"
                style={{ background: COR_CONTEUDOS }}
              />
            </div>
            <span className="text-[10px] text-muted-foreground">
              {new Date(d.semana + "T00:00:00").toLocaleDateString("pt-BR", {
                day: "2-digit",
                month: "2-digit",
              })}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

const FONTES_FUTURAS = [
  { nome: "Instagram", icone: Camera, detalhe: "Alcance, seguidores, melhores posts" },
  { nome: "Google Analytics", icone: BarChart3, detalhe: "Tráfego e conversões do site" },
  { nome: "Google Meu Negócio", icone: MapPin, detalhe: "Buscas locais, ligações, rotas" },
];

export default function VisaoGeralPage() {
  const [resumo, setResumo] = useState<Resumo | null>(null);
  const router = useRouter();

  useEffect(() => {
    apiFetch("/dashboard/resumo").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      setResumo(await resp.json());
    });
  }, [router]);

  if (!resumo) {
    return (
      <AppShell title="Visão geral" description="O desempenho de todo o ecossistema num lugar só">
        <p className="text-sm text-muted-foreground">Carregando...</p>
      </AppShell>
    );
  }

  const aprovados = resumo.conteudos_por_status["aprovado"] ?? 0;
  const totalConteudos = Object.values(resumo.conteudos_por_status).reduce((a, b) => a + b, 0);

  const tiles = [
    { label: "Pautas pesquisadas", valor: resumo.pautas_total, icone: FileText },
    { label: "Conteúdos produzidos", valor: totalConteudos, icone: BarChart3, extra: `${aprovados} aprovados` },
    { label: "Contatos ativos", valor: resumo.contatos_ativos, icone: Users },
    { label: "E-mails entregues", valor: resumo.emails_enviados, icone: Mail },
  ];

  return (
    <AppShell
      title="Visão geral"
      description="O desempenho de todo o ecossistema num lugar só"
    >
      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {tiles.map((tile, i) => (
          <motion.div
            key={tile.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06 }}
          >
            <Card className="p-5">
              <div className="flex items-center justify-between">
                <p className="text-xs text-muted-foreground">{tile.label}</p>
                <tile.icone className="h-4 w-4 text-primary" />
              </div>
              <p className="mt-2 font-display text-3xl font-semibold tabular-nums">
                {tile.valor}
              </p>
              {"extra" in tile && tile.extra && (
                <p className="mt-1 text-xs text-primary">{tile.extra}</p>
              )}
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-5 lg:grid-cols-[1.6fr_1fr]">
        <Card className="p-5">
          <h2 className="mb-4 font-display text-base font-semibold">
            Produção nas últimas 8 semanas
          </h2>
          <BarrasSemanais dados={resumo.producao_semanal} />
        </Card>

        <Card className="p-5">
          <h2 className="mb-4 flex items-center gap-2 font-display text-base font-semibold">
            <CalendarClock className="h-4 w-4 text-primary" />
            Próximas publicações
          </h2>
          {resumo.proximos_agendamentos.length === 0 && (
            <p className="text-sm text-muted-foreground">
              Nada agendado — aprove conteúdos e eles entram aqui sozinhos.
            </p>
          )}
          <div className="space-y-3">
            {resumo.proximos_agendamentos.map((a) => (
              <div key={a.id} className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <p className="truncate text-sm">{a.titulo}</p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(a.data_agendada + "T00:00:00").toLocaleDateString("pt-BR", {
                      day: "2-digit",
                      month: "short",
                    })}{" "}
                    às {a.horario}
                  </p>
                </div>
                <Badge variant="secondary" className="capitalize">
                  {a.canal}
                </Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <h2 className="mb-3 mt-8 font-display text-base font-semibold text-muted-foreground">
        Conectar fontes de desempenho
      </h2>
      <div className="grid gap-4 sm:grid-cols-3">
        {FONTES_FUTURAS.map((fonte) => (
          <Card key={fonte.nome} className="p-5 opacity-70">
            <div className="flex items-center justify-between">
              <fonte.icone className="h-5 w-5 text-primary" />
              <Badge variant="secondary">Em breve</Badge>
            </div>
            <p className="mt-3 text-sm font-medium">{fonte.nome}</p>
            <p className="mt-1 text-xs text-muted-foreground">{fonte.detalhe}</p>
          </Card>
        ))}
      </div>
    </AppShell>
  );
}
