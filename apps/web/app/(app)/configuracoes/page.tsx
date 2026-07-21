"use client";

import { useState } from "react";
import { CheckCircle2, KeyRound, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function ConfiguracoesPage() {
  const [senhaAtual, setSenhaAtual] = useState("");
  const [senhaNova, setSenhaNova] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [sucesso, setSucesso] = useState(false);

  async function trocarSenha(event: React.FormEvent) {
    event.preventDefault();
    setErro(null);
    setSucesso(false);

    if (senhaNova.length < 8) {
      setErro("A nova senha precisa ter pelo menos 8 caracteres.");
      return;
    }
    if (senhaNova !== confirmarSenha) {
      setErro("A confirmação não bate com a nova senha.");
      return;
    }

    setSalvando(true);
    try {
      const resp = await apiFetch("/auth/trocar-senha", {
        method: "POST",
        body: JSON.stringify({ senha_atual: senhaAtual, senha_nova: senhaNova }),
      });
      if (!resp.ok) {
        const body = await resp.json().catch(() => null);
        setErro(body?.detail ?? "Não foi possível trocar a senha. Tente novamente.");
        return;
      }
      setSucesso(true);
      setSenhaAtual("");
      setSenhaNova("");
      setConfirmarSenha("");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <AppShell title="Configurações" description="Sua conta e preferências da plataforma">
      <Card className="max-w-md p-6">
        <div className="mb-4 flex items-center gap-2">
          <KeyRound className="h-4 w-4 text-primary" />
          <h2 className="font-display text-base font-semibold">Trocar senha</h2>
        </div>

        <form onSubmit={trocarSenha} className="space-y-4">
          <div>
            <label className="mb-1.5 block text-xs text-muted-foreground">Senha atual</label>
            <Input
              type="password"
              value={senhaAtual}
              onChange={(e) => setSenhaAtual(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="mb-1.5 block text-xs text-muted-foreground">Nova senha</label>
            <Input
              type="password"
              value={senhaNova}
              onChange={(e) => setSenhaNova(e.target.value)}
              minLength={8}
              required
            />
          </div>
          <div>
            <label className="mb-1.5 block text-xs text-muted-foreground">
              Confirmar nova senha
            </label>
            <Input
              type="password"
              value={confirmarSenha}
              onChange={(e) => setConfirmarSenha(e.target.value)}
              minLength={8}
              required
            />
          </div>

          {erro && <p className="text-sm text-destructive">{erro}</p>}
          {sucesso && (
            <p className="flex items-center gap-1.5 text-sm text-primary">
              <CheckCircle2 className="h-4 w-4" />
              Senha atualizada com sucesso.
            </p>
          )}

          <Button type="submit" disabled={salvando}>
            {salvando && <Loader2 className="h-4 w-4 animate-spin" />}
            {salvando ? "Salvando..." : "Salvar nova senha"}
          </Button>
        </form>
      </Card>
    </AppShell>
  );
}
