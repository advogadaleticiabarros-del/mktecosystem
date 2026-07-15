"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  origem: string;
  fonte: string;
};

export default function PlanejamentoPage() {
  const [pautas, setPautas] = useState<Pauta[]>([]);
  const [loading, setLoading] = useState(false);
  const [manualTitulo, setManualTitulo] = useState("");
  const [manualAngulo, setManualAngulo] = useState("direitos");
  const [manualArea, setManualArea] = useState("Trabalhista");
  const router = useRouter();

  async function carregarSugestoes() {
    const response = await apiFetch("/pautas?relevante_para_conteudo=true");
    if (response.status === 401) {
      router.push("/login");
      return;
    }
    setPautas(await response.json());
  }

  useEffect(() => {
    carregarSugestoes();
  }, []);

  async function buscarNovasSugestoes() {
    setLoading(true);
    try {
      await apiFetch("/pautas/buscar", { method: "POST" });
      await carregarSugestoes();
    } finally {
      setLoading(false);
    }
  }

  async function criarPautaManual(event: React.FormEvent) {
    event.preventDefault();
    await apiFetch("/pautas", {
      method: "POST",
      body: JSON.stringify({ titulo: manualTitulo, angulo: manualAngulo, area: manualArea }),
    });
    setManualTitulo("");
    await carregarSugestoes();
  }

  function escolherPauta(pautaId: string) {
    router.push(`/aprovacao/${pautaId}`);
  }

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ color: "var(--dourado)" }}>Planejamento</h1>

      <button onClick={buscarNovasSugestoes} disabled={loading} style={{ marginBottom: 24 }}>
        {loading ? "Buscando..." : "Buscar sugestões de hoje"}
      </button>

      <ul>
        {pautas.map((pauta) => (
          <li key={pauta.id} style={{ marginBottom: 12 }}>
            <strong>{pauta.titulo}</strong> — {pauta.area} ({pauta.angulo}) — fonte:{" "}
            {pauta.fonte}
            <button onClick={() => escolherPauta(pauta.id)} style={{ marginLeft: 12 }}>
              Gerar conteúdo
            </button>
          </li>
        ))}
      </ul>

      <h2 style={{ color: "var(--dourado)" }}>Ou digite um tema livre</h2>
      <form onSubmit={criarPautaManual}>
        <input
          placeholder="Título do tema"
          value={manualTitulo}
          onChange={(e) => setManualTitulo(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 8, padding: 8 }}
        />
        <select value={manualAngulo} onChange={(e) => setManualAngulo(e.target.value)}>
          <option value="direitos">Direitos</option>
          <option value="sinceridade">Sinceridade</option>
        </select>
        <select value={manualArea} onChange={(e) => setManualArea(e.target.value)}>
          <option>Trabalhista</option>
          <option>Previdenciário</option>
          <option>Família</option>
          <option>Consumidor</option>
        </select>
        <button type="submit">Adicionar pauta</button>
      </form>
    </main>
  );
}
