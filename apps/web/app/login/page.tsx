"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, Eye, EyeOff, Lock, Mail, ShieldCheck } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import { login } from "@/lib/api";
import { AmbientGlow } from "@/components/ambient-glow";
import { LogoMark } from "@/components/logo-mark";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const CAMPO_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" as const } },
};

const LIGHT_INPUT_CLASSES =
  "h-11 rounded-xl border-black/10 bg-[#f7f7fa] pl-10 text-[#1f2430] placeholder:text-[#a1a5b0] transition-shadow focus-visible:border-primary focus-visible:bg-white focus-visible:shadow-[0_0_0_4px_color-mix(in_srgb,var(--primary)_20%,transparent)] focus-visible:ring-0";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
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
    <main className="relative grid min-h-screen grid-cols-1 overflow-hidden bg-[#f3f2f7] text-[#161a23] md:grid-cols-2">
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        aria-hidden="true"
        style={{
          backgroundImage: "radial-gradient(circle, color-mix(in srgb, var(--primary) 55%, transparent) 1px, transparent 1px)",
          backgroundSize: "30px 30px",
        }}
      />

      <section className="relative hidden flex-col justify-center overflow-hidden px-16 md:flex">
        <AmbientGlow anchorLeft="88%" />
        <div className="relative z-10 max-w-md">
          <div className="mb-16 flex items-center gap-2.5">
            <LogoMark className="h-8 w-8" />
            <span className="font-display text-xl font-bold tracking-wide text-[#161a23]">ORBIT</span>
          </div>
          <h1 className="font-display text-5xl font-bold leading-tight text-[#161a23]">
            O centro de <br />
            todo o seu <span className="text-primary">marketing.</span>
          </h1>
          <div className="mt-6 h-1 w-12 rounded-full bg-primary" />
          <p className="mt-6 text-[#5b6270]">
            Inteligência, estratégia e automação trabalhando juntas para gerar
            resultados enquanto você foca no que importa.
          </p>
          <p className="relative z-10 mt-24 font-mono text-xs text-[#9a9fab]">
            © 2026 Orbit. Todos os direitos reservados.
          </p>
        </div>
      </section>

      <section className="relative z-10 flex items-center justify-center p-6 py-16">
        <motion.div
          className="w-full max-w-sm rounded-3xl bg-white p-10 shadow-[0_24px_64px_-20px_rgba(30,20,10,0.28)] ring-1 ring-black/[0.04]"
          initial={reduzirMovimento ? false : "hidden"}
          animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.07, delayChildren: 0.1 } } }}
        >
          <motion.div
            variants={CAMPO_VARIANTS}
            className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border-2 border-primary/25 bg-primary/[0.06]"
          >
            <Lock className="h-6 w-6 text-primary" />
          </motion.div>

          <motion.h2
            variants={CAMPO_VARIANTS}
            className="mt-6 text-center font-display text-2xl font-bold text-[#161a23]"
          >
            Bem-vinda de volta!
          </motion.h2>
          <motion.p variants={CAMPO_VARIANTS} className="mt-1 text-center text-sm text-[#8b8f99]">
            Faça login para acessar sua plataforma
          </motion.p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            <motion.div variants={CAMPO_VARIANTS}>
              <label className="mb-1.5 block text-xs font-medium text-[#5b6270]">E-mail</label>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#a1a5b0]" />
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className={LIGHT_INPUT_CLASSES}
                />
              </div>
            </motion.div>

            <motion.div variants={CAMPO_VARIANTS}>
              <label className="mb-1.5 block text-xs font-medium text-[#5b6270]">Senha</label>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#a1a5b0]" />
                <Input
                  type={mostrarSenha ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className={`${LIGHT_INPUT_CLASSES} pr-10`}
                />
                <button
                  type="button"
                  onClick={() => setMostrarSenha((v) => !v)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#a1a5b0] hover:text-[#5b6270]"
                  aria-label={mostrarSenha ? "Ocultar senha" : "Mostrar senha"}
                >
                  {mostrarSenha ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </motion.div>

            <motion.div variants={CAMPO_VARIANTS} className="flex items-center justify-between text-xs text-[#8b8f99]">
              <label className="flex items-center gap-2 opacity-60">
                <input type="checkbox" disabled className="h-3.5 w-3.5 rounded border-black/20" />
                Lembrar de mim
              </label>
              <button
                type="button"
                disabled
                className="cursor-not-allowed font-medium text-primary/60"
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
              <Button
                type="submit"
                disabled={loading}
                className="h-12 w-full gap-2 rounded-full bg-gradient-to-r from-[#e9c27a] to-[#c9922e] text-base font-semibold text-[#2a1c05] shadow-[0_10px_30px_-8px_color-mix(in_srgb,var(--primary)_60%,transparent)] transition-transform hover:brightness-[1.03] active:scale-[0.98]"
              >
                {loading ? "Entrando..." : "Entrar na plataforma"}
                {!loading && <ArrowRight className="h-4 w-4" />}
              </Button>
            </motion.div>
          </form>

          <motion.div
            variants={CAMPO_VARIANTS}
            className="mt-8 flex items-center justify-center gap-3 font-mono text-xs text-[#a1a5b0]"
          >
            <span className="h-px flex-1 bg-black/[0.06]" />
            <span className="flex items-center gap-1.5 whitespace-nowrap">
              <ShieldCheck className="h-3.5 w-3.5" />
              Segurança de nível empresarial
            </span>
            <span className="h-px flex-1 bg-black/[0.06]" />
          </motion.div>
        </motion.div>
      </section>
    </main>
  );
}
