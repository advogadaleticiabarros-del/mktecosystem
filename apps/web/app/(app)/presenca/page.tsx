"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, RefreshCw } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AbaBuscas, AbaMelhorias, AbaResumo, AbaSite } from "./_components/abas-leitura";
import { AbaAvaliacoes, AbaPerfil, AbaPosts } from "./_components/abas-gestao";
import { lerErro, type Aba, type Recomendacao, type RespostaPainel } from "./_components/tipos";

const ABAS: { chave: Aba; rotulo: string }[] = [
  { chave: "resumo", rotulo: "Resumo" },
  { chave: "melhorias", rotulo: "Melhorias" },
  { chave: "perfil", rotulo: "Perfil" },
  { chave: "avaliacoes", rotulo: "Avaliações" },
  { chave: "posts", rotulo: "Posts" },
  { chave: "buscas", rotulo: "Buscas" },
  { chave: "site", rotulo: "Site e IAs" },
];

export default function PresencaPage() {
  const router = useRouter();
  const [dados, setDados] = useState<RespostaPainel | null>(null);
  const [aba, setAba] = useState<Aba>("resumo");
  const [atualizando, setAtualizando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    const resp = await apiFetch("/presenca");
    if (resp.status === 401) return router.push("/login");
    if (resp.ok) setDados(await resp.json());
  }, [router]);

  const atualizar = useCallback(async () => {
    setAtualizando(true);
    setErro(null);
    try {
      const resp = await apiFetch("/presenca/atualizar", { method: "POST" });
      if (!resp.ok) setErro((await lerErro(resp)).mensagem);
      else setDados(await resp.json());
    } finally {
      setAtualizando(false);
    }
  }, []);

  useEffect(() => {
    const inicial = window.location.hash.replace("#", "") as Aba;
    if (ABAS.some((a) => a.chave === inicial)) setAba(inicial);
    carregar();
  }, [carregar]);

  function irPara(nova: Aba) {
    setAba(nova);
    window.history.replaceState(null, "", `#${nova}`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function marcar(chave: string, status: Recomendacao["status"]) {
    setDados((d) => d && { ...d, recomendacoes: d.recomendacoes.map((r) => (r.chave === chave ? { ...r, status } : r)) });
    await apiFetch(`/presenca/recomendacoes/${encodeURIComponent(chave)}`, { method: "PUT", body: JSON.stringify({ status }) });
  }

  const painel = dados?.painel;
  const pendentes = dados?.recomendacoes.filter((r) => r.status === "pendente").length ?? 0;

  return (
    <AppShell
      title="Google e site"
      description="Perfil da Empresa, avaliações, posts, busca orgânica, site e IAs num lugar só."
      headerActions={
        <div className="flex items-center gap-3">
          {dados?.coletado_em && (
            <span className="hidden text-xs text-muted-foreground md:inline">
              Atualizado {new Date(dados.coletado_em).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}
            </span>
          )}
          <Button size="sm" variant="outline" onClick={atualizar} disabled={atualizando}>
            {atualizando ? <Loader2 className="animate-spin" /> : <RefreshCw />} {atualizando ? "Buscando no Google..." : "Atualizar agora"}
          </Button>
        </div>
      }
    >
      {erro && <Card className="mb-4 p-4 text-sm text-destructive hover:translate-y-0">{erro}</Card>}

      {!dados && <p className="text-sm text-muted-foreground">Carregando...</p>}

      {dados && !painel && (
        <Card className="p-8 text-center hover:translate-y-0">
          <p className="font-medium">Ainda não há dados do Google.</p>
          <p className="mt-1 text-sm text-muted-foreground">Clique em &ldquo;Atualizar agora&rdquo;. A primeira busca leva cerca de 1 minuto. Depois disso o Orbit atualiza sozinho todo dia de madrugada.</p>
          <Button className="mt-4" onClick={atualizar} disabled={atualizando}>
            {atualizando ? <Loader2 className="animate-spin" /> : <RefreshCw />} Atualizar agora
          </Button>
        </Card>
      )}

      {painel && (
        <>
          <nav className="mb-6 flex gap-1 overflow-x-auto border-b">
            {ABAS.map((a) => (
              <button
                key={a.chave}
                type="button"
                onClick={() => irPara(a.chave)}
                className={`-mb-px whitespace-nowrap border-b-2 px-3 py-2 text-sm transition-colors ${
                  aba === a.chave ? "border-primary font-medium text-foreground" : "border-transparent text-muted-foreground hover:text-foreground"
                }`}
              >
                {a.rotulo}
                {a.chave === "melhorias" && pendentes > 0 && (
                  <span className="ml-1.5 rounded-full bg-primary px-1.5 text-[10px] font-semibold text-primary-foreground">{pendentes}</span>
                )}
                {a.chave === "avaliacoes" && (painel.avaliacoes?.sem_resposta ?? 0) > 0 && (
                  <span className="ml-1.5 rounded-full bg-destructive px-1.5 text-[10px] font-semibold text-white">{painel.avaliacoes!.sem_resposta}</span>
                )}
              </button>
            ))}
          </nav>
          {aba === "resumo" && <AbaResumo painel={painel} irPara={irPara} />}
          {aba === "melhorias" && <AbaMelhorias recomendacoes={dados!.recomendacoes} marcar={marcar} irPara={irPara} />}
          {aba === "perfil" && <AbaPerfil painel={painel} recarregar={carregar} />}
          {aba === "avaliacoes" && <AbaAvaliacoes painel={painel} recarregar={carregar} />}
          {aba === "posts" && <AbaPosts painel={painel} recarregar={carregar} />}
          {aba === "buscas" && <AbaBuscas painel={painel} />}
          {aba === "site" && <AbaSite painel={painel} />}
        </>
      )}
    </AppShell>
  );
}
