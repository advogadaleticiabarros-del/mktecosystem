"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck } from "lucide-react";
import { login } from "@/lib/api";
import { AmbientGlow } from "@/components/ambient-glow";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      router.push("/planejamento");
    } catch {
      setError("E-mail ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen grid-cols-1 bg-background text-foreground md:grid-cols-2">
      <section className="relative hidden flex-col items-center justify-center overflow-hidden p-10 md:flex">
        <AmbientGlow />
        <div className="relative z-10 flex w-full max-w-md flex-col">
          <div className="mb-10 flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full border border-primary/40">
              <div className="h-2.5 w-2.5 rounded-full bg-primary" />
            </div>
            <div>
              <p className="font-display text-lg font-semibold tracking-wide">ORBIT</p>
              <p className="text-xs text-muted-foreground">The Marketing Operating System.</p>
            </div>
          </div>
          <h1 className="font-display text-4xl font-semibold leading-tight">
            O centro de <br />
            todo o seu <span className="text-primary">marketing.</span>
          </h1>
          <p className="mt-4 text-muted-foreground">
            Inteligência, estratégia e automação trabalhando juntas para gerar
            resultados enquanto você foca no que importa.
          </p>
          <p className="relative z-10 mt-16 text-xs text-muted-foreground">
            © 2026 Orbit. Todos os direitos reservados.
          </p>
        </div>
      </section>

      <section className="flex items-center justify-center p-6 py-16">
        <div className="w-full max-w-sm rounded-2xl border border-border bg-card p-8">
          <h2 className="font-display text-xl font-semibold">Bem-vinda de volta!</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Faça login para acessar sua plataforma
          </p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div>
              <label className="mb-1.5 block text-xs text-muted-foreground">E-mail</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="mb-1.5 block text-xs text-muted-foreground">Senha</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <label className="flex items-center gap-2 opacity-50">
                <input type="checkbox" disabled className="h-3.5 w-3.5" />
                Lembrar de mim
              </label>
              <button
                type="button"
                disabled
                className="cursor-not-allowed text-primary/50"
                title="Em breve"
              >
                Esqueci minha senha
              </button>
            </div>

            {error && <p className="text-sm text-destructive">{error}</p>}

            <Button type="submit" disabled={loading} className="w-full">
              {loading ? "Entrando..." : "Entrar na plataforma"}
            </Button>
          </form>

          <div className="mt-6 flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
            <ShieldCheck className="h-3.5 w-3.5" />
            Segurança de nível empresarial
          </div>
        </div>
      </section>
    </main>
  );
}
