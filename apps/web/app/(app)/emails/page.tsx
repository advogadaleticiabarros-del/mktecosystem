"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { CheckCircle2, Mail, Sparkles, Users } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

type Campaign = {
  id: string;
  tipo: string;
  assunto: string;
  corpo_html: string;
  corpo_texto: string;
  status: string;
  criado_em: string;
};

type Contact = {
  id: string;
  nome: string;
  email: string;
  origem: string;
  status: string;
};

const TIPO_LABEL: Record<string, string> = {
  boas_vindas_1: "Boas-vindas · passo 1 (imediato)",
  boas_vindas_2: "Boas-vindas · passo 2 (dia 2)",
  boas_vindas_3: "Boas-vindas · passo 3 (dia 5)",
  newsletter: "Newsletter semanal",
};

const STATUS_STYLE: Record<string, string> = {
  rascunho: "bg-secondary text-secondary-foreground",
  aprovado: "bg-primary/15 text-primary",
  enviado: "bg-emerald-500/15 text-emerald-400",
};

export default function EmailsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [gerando, setGerando] = useState<"boas-vindas" | "newsletter" | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const router = useRouter();

  async function carregar() {
    const [respCampanhas, respContatos] = await Promise.all([
      apiFetch("/email/campaigns"),
      apiFetch("/email/contacts"),
    ]);
    if (respCampanhas.status === 401) {
      router.push("/login");
      return;
    }
    setCampaigns(await respCampanhas.json());
    setContacts(await respContatos.json());
  }

  useEffect(() => {
    carregar();
  }, []);

  async function gerar(tipo: "boas-vindas" | "newsletter") {
    setGerando(tipo);
    setErro(null);
    try {
      const resp = await apiFetch(`/email/campaigns/gerar-${tipo}`, { method: "POST" });
      if (!resp.ok) {
        const body = await resp.json().catch(() => null);
        setErro(body?.detail ?? "Erro ao gerar. Tente novamente.");
        return;
      }
      await carregar();
    } finally {
      setGerando(null);
    }
  }

  async function salvar(campaign: Campaign, patch: Partial<Campaign>) {
    const resp = await apiFetch(`/email/campaigns/${campaign.id}`, {
      method: "PATCH",
      body: JSON.stringify(patch),
    });
    const updated = await resp.json();
    setCampaigns((prev) => prev.map((c) => (c.id === campaign.id ? updated : c)));
  }

  const ativos = contacts.filter((c) => c.status === "ativo").length;

  return (
    <AppShell
      title="E-mail marketing"
      description="Sequência de boas-vindas e newsletter — nada sai sem a sua aprovação"
      headerActions={
        <div className="flex items-center gap-2 rounded-md border border-border px-3 py-1.5 text-sm text-muted-foreground">
          <Users className="h-4 w-4 text-primary" />
          {ativos} {ativos === 1 ? "contato ativo" : "contatos ativos"}
        </div>
      }
    >
      <div className="mb-6 flex flex-wrap items-center gap-3">
        <Button
          onClick={() => gerar("boas-vindas")}
          disabled={gerando !== null}
          variant="secondary"
        >
          <Sparkles className="h-4 w-4" />
          {gerando === "boas-vindas" ? "Gerando sequência..." : "Gerar sequência de boas-vindas"}
        </Button>
        <Button
          onClick={() => gerar("newsletter")}
          disabled={gerando !== null}
          variant="secondary"
        >
          <Mail className="h-4 w-4" />
          {gerando === "newsletter" ? "Montando newsletter..." : "Gerar newsletter da semana"}
        </Button>
        {erro && <p className="text-sm text-destructive">{erro}</p>}
      </div>

      {campaigns.length === 0 && (
        <Card className="flex flex-col items-center gap-3 p-12 text-center">
          <Mail className="h-8 w-8 text-primary" />
          <p className="font-display text-lg font-semibold">Nenhuma campanha ainda</p>
          <p className="max-w-sm text-sm text-muted-foreground">
            Gere a sequência de boas-vindas para receber bem quem chega pela landing page,
            ou monte a newsletter com os artigos da semana.
          </p>
        </Card>
      )}

      <div className="grid gap-5 lg:grid-cols-2">
        <AnimatePresence>
          {campaigns.map((campaign, i) => (
            <motion.div
              key={campaign.id}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Card className="flex h-full flex-col gap-4 p-5">
                <div className="flex items-start justify-between gap-3">
                  <p className="text-xs font-semibold uppercase tracking-wide text-primary">
                    {TIPO_LABEL[campaign.tipo] ?? campaign.tipo}
                  </p>
                  <Badge
                    className={cn(
                      "capitalize",
                      STATUS_STYLE[campaign.status] ?? "bg-secondary",
                    )}
                  >
                    {campaign.status}
                  </Badge>
                </div>

                <div>
                  <label className="mb-1.5 block text-xs text-muted-foreground">Assunto</label>
                  <Input
                    value={campaign.assunto}
                    disabled={campaign.status === "enviado"}
                    onChange={(e) =>
                      setCampaigns((prev) =>
                        prev.map((c) =>
                          c.id === campaign.id ? { ...c, assunto: e.target.value } : c,
                        ),
                      )
                    }
                    onBlur={() => salvar(campaign, { assunto: campaign.assunto })}
                  />
                </div>

                <div className="flex-1">
                  <label className="mb-1.5 block text-xs text-muted-foreground">Conteúdo</label>
                  <textarea
                    value={campaign.corpo_texto}
                    disabled={campaign.status === "enviado"}
                    rows={7}
                    className="w-full rounded-md border border-border bg-background p-3 text-sm leading-relaxed"
                    onChange={(e) =>
                      setCampaigns((prev) =>
                        prev.map((c) =>
                          c.id === campaign.id ? { ...c, corpo_texto: e.target.value } : c,
                        ),
                      )
                    }
                    onBlur={() => salvar(campaign, { corpo_texto: campaign.corpo_texto })}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <p className="text-xs text-muted-foreground">
                    {new Date(campaign.criado_em).toLocaleDateString("pt-BR")}
                  </p>
                  {campaign.status === "rascunho" && (
                    <Button size="sm" onClick={() => salvar(campaign, { status: "aprovado" })}>
                      <CheckCircle2 className="h-4 w-4" />
                      Aprovar
                    </Button>
                  )}
                  {campaign.status === "aprovado" && campaign.tipo === "newsletter" && (
                    <p className="flex items-center gap-1.5 text-xs text-primary">
                      <CheckCircle2 className="h-3.5 w-3.5" />
                      Na fila de envio
                    </p>
                  )}
                  {campaign.status === "aprovado" && campaign.tipo !== "newsletter" && (
                    <p className="flex items-center gap-1.5 text-xs text-primary">
                      <CheckCircle2 className="h-3.5 w-3.5" />
                      Ativo na sequência
                    </p>
                  )}
                </div>
              </Card>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </AppShell>
  );
}
