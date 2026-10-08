"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

// O Resumo Jurídico Diário virou a aba "Novas" do Planejamento (Jornalista).
// Esta rota só existe para não quebrar endereços salvos.
export default function ResumoDiarioRedirect() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/planejamento");
  }, [router]);
  return null;
}
