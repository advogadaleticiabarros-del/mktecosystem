"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

// As avaliações viraram a aba "Avaliações" da tela Google e site (resposta sugerida
// por IA, checagem da OAB e publicação no Google). Esta rota só existe para não
// quebrar endereços salvos.
export default function AvaliacoesRedirect() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/presenca#avaliacoes");
  }, [router]);
  return null;
}
