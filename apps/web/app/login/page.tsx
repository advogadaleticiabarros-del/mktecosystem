"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import { login } from "@/lib/api";
import { AmbientGlow } from "@/components/ambient-glow";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const CAMPO_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" as const } },
};

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const reduzirMovimento = useReducedMotion();

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
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="/logo/elemento-a.png"
              alt="Orbit"
              className="h-8 w-8 mix-blend-screen"
            />
            <div>
              <p className="font-display text-lg font-semibold tracking-wide">ORBIT</p>
              <p className="font-mono text-xs text-muted-foreground">The Marketing Operating System.</p>
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
          <p className="relative z-10 mt-16 font-mono text-xs text-muted-foreground">
            © 2026 Orbit. Todos os direitos reservados.
          </p>
        </div>
      </section>

      <section className="flex items-center justify-center p-6 py-16">
        <motion.div
          className="w-full max-w-sm rounded-2xl border border-border bg-card p-8"
          initial={reduzirMovimento ? false : "hidden"}
          animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.07, delayChildren: 0.1 } } }}
        >
          <motion.h2 variants={CAMPO_VARIANTS} className="font-display text-xl font-semibold">
            Bem-vinda de volta!
          </motion.h2>
          <motion.p variants={CAMPO_VARIANTS} className="mt-1 text-sm text-muted-foreground">
            Faça login para acessar sua plataforma
          </motion.p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <motion.div variants={CAMPO_VARIANTS}>
              <label className="mb-1.5 block text-xs text-muted-foreground">E-mail</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="transition-shadow focus-visible:shadow-[0_0_0_4px_color-mix(in_srgb,var(--primary)_25%,transparent)]"
              />
            </motion.div>
            <motion.div variants={CAMPO_VARIANTS}>
              <label className="mb-1.5 block text-xs text-muted-foreground">Senha</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="transition-shadow focus-visible:shadow-[0_0_0_4px_color-mix(in_srgb,var(--primary)_25%,transparent)]"
              />
            </motion.div>

            <motion.div variants={CAMPO_VARIANTS} className="flex items-center justify-between text-xs text-muted-foreground">
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
            </motion.div>

            {error && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-sm text-destructive"
              >
                {error}
              </motion.p>
            )}

            <motion.div variants={CAMPO_VARIANTS}>
              <Button type="submit" disabled={loading} className="w-full transition-transform active:scale-[0.98]">
                {loading ? "Entrando..." : "Entrar na plataforma"}
              </Button>
            </motion.div>
          </form>

          <motion.div
            variants={CAMPO_VARIANTS}
            className="mt-6 flex items-center justify-center gap-1.5 font-mono text-xs text-muted-foreground"
          >
            <ShieldCheck className="h-3.5 w-3.5" />
            Segurança de nível empresarial
          </motion.div>
        </motion.div>
      </section>
    </main>
  );
}
