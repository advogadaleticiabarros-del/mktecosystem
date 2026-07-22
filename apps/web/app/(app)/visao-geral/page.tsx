"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  BarChart3,
  CalendarClock,
  Camera,
  FileText,
  Lightbulb,
  Loader2,
  Mail,
  MapPin,
  Users,
} from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { StaggerList } from "@/components/motion/stagger-list";
import { CountUp } from "@/components/motion/count-up";

type Resumo = {
  instagram: { seguidores: number; alcance_7d: number } | null;
  google_business: { buscas: number; chamadas: number; pedidos_rota: number; visualizacoes: number } | null;
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
  const reduzirMovimento = useReducedMotion();

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
              {reduzirMovimento ? (
                <div
                  className="w-3 rounded-t"
                  style={{ background: COR_PAUTAS, height: Math.max(2, (d.pautas / teto) * alturaMax) }}
                />
              ) : (
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: Math.max(2, (d.pautas / teto) * alturaMax) }}
                  transition={{ delay: i * 0.04 }}
                  className="w-3 rounded-t"
                  style={{ background: COR_PAUTAS }}
                />
              )}
              {reduzirMovimento ? (
                <div
                  className="w-3 rounded-t"
                  style={{ background: COR_CONTEUDOS, height: Math.max(2, (d.conteudos / teto) * alturaMax) }}
                />
              ) : (
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: Math.max(2, (d.conteudos / teto) * alturaMax) }}
                  transition={{ delay: i * 0.04 + 0.02 }}
                  className="w-3 rounded-t"
                  style={{ background: COR_CONTEUDOS }}
                />
              )}
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
  { nome: "Google Analytics", icone: BarChart3, detalhe: "Tráfego e conversões do site" },
];

type Dica = { titulo: string; diagnostico: string; acao: string };
type Conexao = { id: string; plataforma: string; nome_conta: string; status: string };

export default function VisaoGeralPage() {
  const [resumo, setResumo] = useState<Resumo | null>(null);
  const [dicas, setDicas] = useState<Dica[] | null>(null);
  const [gerandoDicas, setGerandoDicas] = useState(false);
  const [conexoes, setConexoes] = useState<Conexao[]>([]);
  const [mostrarCampoToken, setMostrarCampoToken] = useState(false);
  const [tokenManual, setTokenManual] = useState("");
  const [conectando, setConectando] = useState(false);
  const [erroConexao, setErroConexao] = useState<string | null>(null);
  const router = useRouter();

  async function analisar() {
    setGerandoDicas(true);
    try {
      const resp = await apiFetch("/dashboard/insights", { method: "POST" });
      if (resp.ok) setDicas((await resp.json()).dicas);
    } finally {
      setGerandoDicas(false);
    }
  }

  const instagramConectado = conexoes.find(
    (c) => c.plataforma === "instagram" && c.status === "ativo",
  );

  function conectarInstagram() {
    const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const token = localStorage.getItem("token") ?? "";
    window.location.href = `${base}/integracoes/instagram/iniciar?token=${encodeURIComponent(token)}`;
  }

  async function desconectarInstagram() {
    await apiFetch("/integracoes/instagram", { method: "DELETE" });
    setConexoes((prev) => prev.filter((c) => c.plataforma !== "instagram"));
  }

  const googleBusinessConectado = conexoes.find(
    (c) => c.plataforma === "google_business" && c.status === "ativo",
  );

  function conectarGoogleBusiness() {
    const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    const token = localStorage.getItem("token") ?? "";
    window.location.href = `${base}/integracoes/google-business/iniciar?token=${encodeURIComponent(token)}`;
  }

  async function desconectarGoogleBusiness() {
    await apiFetch("/integracoes/google-business", { method: "DELETE" });
    setConexoes((prev) => prev.filter((c) => c.plataforma !== "google_business"));
  }

  async function conectarComTokenManual() {
    setConectando(true);
    setErroConexao(null);
    try {
      const resp = await apiFetch("/integracoes/instagram/token", {
        method: "POST",
        body: JSON.stringify({ access_token: tokenManual.trim() }),
      });
      if (!resp.ok) {
        const body = await resp.json().catch(() => null);
        setErroConexao(body?.detail ?? "Não foi possível conectar com esse token.");
        return;
      }
      const nova = await resp.json();
      setConexoes((prev) => [...prev.filter((c) => c.plataforma !== "instagram"), nova]);
      setMostrarCampoToken(false);
      setTokenManual("");
    } finally {
      setConectando(false);
    }
  }

  useEffect(() => {
    apiFetch("/dashboard/resumo").then(async (resp) => {
      if (resp.status === 401) {
        router.push("/login");
        return;
      }
      setResumo(await resp.json());
    });
    apiFetch("/integracoes").then(async (resp) => {
      if (resp.ok) setConexoes(await resp.json());
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
    { label: "Conteúdos produzidos", valor: totalConteudos, icone: BarChart3, extraValor: aprovados },
    { label: "Contatos ativos", valor: resumo.contatos_ativos, icone: Users },
    { label: "E-mails entregues", valor: resumo.emails_enviados, icone: Mail },
  ];

  return (
    <AppShell
      title="Visão geral"
      description="O desempenho de todo o ecossistema num lugar só"
    >
      <StaggerList className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {tiles.map((tile) => (
          <Card
            key={tile.label}
            className="p-5 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_0_0_1px_var(--primary),0_8px_24px_-8px_color-mix(in_srgb,var(--primary)_35%,transparent)]"
          >
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">{tile.label}</p>
              <tile.icone className="h-4 w-4 text-primary" />
            </div>
            <p className="mt-2 font-display text-3xl font-semibold tabular-nums">
              <CountUp valor={tile.valor} />
            </p>
            {"extraValor" in tile && tile.extraValor !== undefined && (
              <p className="mt-1 text-xs text-primary">
                <CountUp valor={tile.extraValor} /> aprovados
              </p>
            )}
          </Card>
        ))}
      </StaggerList>

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
                  <p className="font-mono text-xs text-muted-foreground">
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

      <Card className="mt-8 p-5">
        <div className="flex items-center justify-between">
          <h2 className="flex items-center gap-2 font-display text-base font-semibold">
            <Lightbulb className="h-4 w-4 text-primary" />
            Dicas para melhorar o desempenho
          </h2>
          <button
            type="button"
            onClick={analisar}
            disabled={gerandoDicas}
            className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground disabled:opacity-60"
          >
            {gerandoDicas && <Loader2 className="h-4 w-4 animate-spin" />}
            {gerandoDicas ? "Analisando..." : dicas ? "Analisar de novo" : "Analisar agora"}
          </button>
        </div>
        {!dicas && !gerandoDicas && (
          <p className="mt-3 text-sm text-muted-foreground">
            A IA cruza produção, aprovações, edições e e-mail das últimas 4 semanas e
            devolve o que fazer para melhorar — em ordem de impacto.
          </p>
        )}
        {dicas && (
          <div className="mt-4 space-y-4">
            {dicas.map((dica, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.08 }}
                className="border-l-2 border-primary/60 pl-4"
              >
                <p className="text-sm font-medium">{dica.titulo}</p>
                <p className="mt-0.5 text-xs text-muted-foreground">{dica.diagnostico}</p>
                <p className="mt-1 text-xs text-primary">→ {dica.acao}</p>
              </motion.div>
            ))}
          </div>
        )}
      </Card>

      <h2 className="mb-3 mt-8 font-display text-base font-semibold text-muted-foreground">
        Conectar fontes de desempenho
      </h2>
      <div className="grid gap-4 sm:grid-cols-3">
        <Card className="p-5">
          <div className="flex items-center justify-between">
            <Camera className="h-5 w-5 text-primary" />
            <Badge
              className={
                instagramConectado ? "font-mono bg-primary/15 text-primary" : "font-mono"
              }
              variant={instagramConectado ? undefined : "secondary"}
            >
              {instagramConectado ? "Conectado" : "Não conectado"}
            </Badge>
          </div>
          <p className="mt-3 text-sm font-medium">Instagram</p>
          <p className="mt-1 text-xs text-muted-foreground">
            {instagramConectado ? (
              <>
                @{instagramConectado.nome_conta}
                {resumo.instagram && (
                  <>
                    {" · "}
                    <CountUp valor={resumo.instagram.seguidores} /> seguidores
                  </>
                )}
              </>
            ) : (
              "Alcance, seguidores, melhores posts"
            )}
          </p>
          {!instagramConectado && (
            <div className="mt-3 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={conectarInstagram}
                className="text-xs font-medium text-primary hover:underline"
              >
                Conectar
              </button>
              <button
                type="button"
                onClick={() => setMostrarCampoToken((v) => !v)}
                className="text-xs text-muted-foreground hover:underline"
              >
                {mostrarCampoToken ? "Cancelar" : "Colar token"}
              </button>
            </div>
          )}
          {instagramConectado && (
            <button
              type="button"
              onClick={desconectarInstagram}
              className="mt-3 text-xs font-medium text-primary hover:underline"
            >
              Desconectar
            </button>
          )}
          {mostrarCampoToken && !instagramConectado && (
            <div className="mt-3 space-y-2">
              <Input
                placeholder="Token do usuário do sistema (EAA...)"
                value={tokenManual}
                onChange={(e) => setTokenManual(e.target.value)}
                className="h-8 text-xs"
              />
              <button
                type="button"
                onClick={conectarComTokenManual}
                disabled={conectando || !tokenManual.trim()}
                className="flex items-center gap-1.5 rounded-md bg-primary px-2.5 py-1 text-xs font-medium text-primary-foreground disabled:opacity-60"
              >
                {conectando && <Loader2 className="h-3 w-3 animate-spin" />}
                {conectando ? "Conectando..." : "Confirmar"}
              </button>
              {erroConexao && <p className="text-xs text-destructive">{erroConexao}</p>}
            </div>
          )}
        </Card>
        <Card className="p-5">
          <div className="flex items-center justify-between">
            <MapPin className="h-5 w-5 text-primary" />
            <Badge
              className={
                googleBusinessConectado ? "font-mono bg-primary/15 text-primary" : "font-mono"
              }
              variant={googleBusinessConectado ? undefined : "secondary"}
            >
              {googleBusinessConectado ? "Conectado" : "Não conectado"}
            </Badge>
          </div>
          <p className="mt-3 text-sm font-medium">Google Meu Negócio</p>
          <p className="mt-1 text-xs text-muted-foreground">
            {googleBusinessConectado ? (
              resumo.google_business ? (
                <>
                  <CountUp valor={resumo.google_business.chamadas} /> ligações ·{" "}
                  <CountUp valor={resumo.google_business.pedidos_rota} /> rotas (7d)
                </>
              ) : (
                googleBusinessConectado.nome_conta
              )
            ) : (
              "Buscas locais, ligações, rotas"
            )}
          </p>
          <button
            type="button"
            onClick={googleBusinessConectado ? desconectarGoogleBusiness : conectarGoogleBusiness}
            className="mt-3 text-xs font-medium text-primary hover:underline"
          >
            {googleBusinessConectado ? "Desconectar" : "Conectar"}
          </button>
        </Card>
        {FONTES_FUTURAS.map((fonte) => (
          <Card key={fonte.nome} className="p-5 opacity-70">
            <div className="flex items-center justify-between">
              <fonte.icone className="h-5 w-5 text-primary" />
              <Badge variant="secondary" className="font-mono">Em breve</Badge>
            </div>
            <p className="mt-3 text-sm font-medium">{fonte.nome}</p>
            <p className="mt-1 text-xs text-muted-foreground">{fonte.detalhe}</p>
          </Card>
        ))}
      </div>
    </AppShell>
  );
}
