"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError(null);
    try {
      await login(email, password);
      router.push("/planejamento");
    } catch {
      setError("E-mail ou senha inválidos.");
    }
  }

  return (
    <main style={{ maxWidth: 360, margin: "80px auto" }}>
      <h1 style={{ color: "var(--dourado)" }}>Marketing OS</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 12, padding: 8 }}
        />
        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 12, padding: 8 }}
        />
        {error && <p style={{ color: "#e57373" }}>{error}</p>}
        <button type="submit" style={{ padding: "8px 16px", background: "var(--dourado)" }}>
          Entrar
        </button>
      </form>
    </main>
  );
}
