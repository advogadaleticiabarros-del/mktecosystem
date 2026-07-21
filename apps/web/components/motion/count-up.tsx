// apps/web/components/motion/count-up.tsx
"use client";

import { useEffect, useState } from "react";
import { useReducedMotion } from "framer-motion";

export function CountUp({
  valor,
  duracaoMs = 800,
}: {
  valor: number;
  duracaoMs?: number;
}) {
  const reduzirMovimento = useReducedMotion();
  const [exibido, setExibido] = useState(reduzirMovimento ? valor : 0);

  useEffect(() => {
    if (reduzirMovimento) {
      setExibido(valor);
      return;
    }

    let frameId: number;
    const inicio = performance.now();

    function passo(agora: number) {
      const progresso = Math.min(1, (agora - inicio) / duracaoMs);
      setExibido(Math.round(progresso * valor));
      if (progresso < 1) {
        frameId = requestAnimationFrame(passo);
      }
    }

    frameId = requestAnimationFrame(passo);
    return () => cancelAnimationFrame(frameId);
  }, [valor, duracaoMs, reduzirMovimento]);

  return <span className="font-mono tabular-nums">{exibido.toLocaleString("pt-BR")}</span>;
}
