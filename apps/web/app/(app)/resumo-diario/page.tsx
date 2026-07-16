"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Pauta = {
  id: string;
  titulo: string;
  angulo: string;
  area: string;
  fonte: string;
  relevante_para_conteudo: boolean;
};

export default function ResumoDiarioPage() {
  const [pautas, setPautas] = useState<Pauta[]>([]);

  useEffect(() => {
    apiFetch("/pautas/resumo-diario")
      .then((r) => r.json())
      .then(setPautas);
  }, []);

  const porArea = pautas.reduce<Record<string, Pauta[]>>((acc, p) => {
    (acc[p.area] ??= []).push(p);
    return acc;
  }, {});

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ color: "var(--dourado)" }}>Resumo Jurídico Diário</h1>
      {Object.entries(porArea).map(([area, itens]) => (
        <section key={area} style={{ marginBottom: 24 }}>
          <h2>{area}</h2>
          <ul>
            {itens.map((p) => (
              <li key={p.id}>
                {p.titulo} — fonte: {p.fonte}
                {p.relevante_para_conteudo && (
                  <span style={{ color: "var(--dourado)" }}> · candidato a conteúdo</span>
                )}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </main>
  );
}
