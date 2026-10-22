"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { CalendarClock, ExternalLink, Loader2, Send, Sparkles, Trash2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ListaOab, Secao, TextoComOab } from "../presenca/_components/comuns";
import { lerErro, type ProblemaOab } from "../presenca/_components/tipos";

type Situacao = { conectado: boolean; nome?: string; dias_para_vencer?: number | null };
type Post = {
  id: string;
  texto: string;
  link: string | null;
  publicar_em: string;
  status: "rascunho" | "aprovado" | "publicado" | "erro";
  erro: string | null;
  link_publicado: string | null;
  problemas: ProblemaOab[];
};

const NOME_STATUS = { rascunho: "Rascunho", aprovado: "Agendado", publicado: "Publicado", erro: "Erro" };
const LIMITE = 3000;

function paraDatetimeLocal(iso?: string) {
  const d = iso ? new Date(iso) : new Date(Date.now() + 60 * 60 * 1000);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
}

const bloqueia = (p: ProblemaOab[]) => p.some((x) => x.nivel === "bloqueia");

export default function LinkedinPage() {
  const router = useRouter();
  const [situacao, setSituacao] = useState<Situacao | null>(null);
  const [posts, setPosts] = useState<Post[] | null>(null);
  const [tema, setTema] = useState("");
  const [texto, setTexto] = useState("");
  const [oab, setOab] = useState<ProblemaOab[]>([]);
  const [link, setLink] = useState("");
  const [quando, setQuando] = useState(paraDatetimeLocal());
  const [ocupado, setOcupado] = useState<string | null>(null);
  const [mensagem, setMensagem] = useState<{ tipo: "ok" | "erro"; texto: string; problemas?: ProblemaOab[] } | null>(null);

  const carregar = useCallback(async () => {
    const r = await apiFetch("/linkedin");
    if (r.status === 401) return router.push("/login");
    if (r.ok) setSituacao(await r.json());
    const p = await apiFetch("/linkedin/posts");
    if (p.ok) setPosts(await p.json());
  }, [router]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function rodar(nome: string, fn: () => Promise<Response>, sucesso: string, depois?: (r: Response) => Promise<void> | void) {
    setOcupado(nome);
    setMensagem(null);
    try {
      const r = await fn();
      if (!r.ok) {
        const e = await lerErro(r);
        setMensagem({ tipo: "erro", texto: e.mensagem, problemas: e.problemas });
        return;
      }
      await depois?.(r);
      setMensagem({ tipo: "ok", texto: sucesso });
    } catch {
      setMensagem({ tipo: "erro", texto: "Falha de conexão. Tente de novo." });
    } finally {
      setOcupado(null);
    }
  }

  function salvar(status: "rascunho" | "aprovado") {
    const corpo = { texto, link: link.trim() || null, publicar_em: new Date(quando).toISOString(), status };
    return rodar("salvar", () => apiFetch("/linkedin/posts", { method: "POST", body: JSON.stringify(corpo) }),
      status === "aprovado" ? "Post agendado. O Orbit publica no LinkedIn no horário marcado." : "Rascunho salvo.",
      async () => { setTexto(""); setTema(""); setLink(""); await carregar(); });
  }

  function aprovar(p: Post) {
    const quandoPost = new Date(p.publicar_em) < new Date() ? new Date(Date.now() + 10 * 60 * 1000).toISOString() : p.publicar_em;
    return rodar(`apr-${p.id}`, () => apiFetch(`/linkedin/posts/${p.id}`, {
      method: "PUT", body: JSON.stringify({ texto: p.texto, link: p.link, publicar_em: quandoPost, status: "aprovado" }),
    }), "Post aprovado. O Orbit publica no horário marcado.", carregar);
  }

  const conectado = situacao?.conectado;

  return (
    <AppShell title="LinkedIn" description="Posts no perfil da Dra., com checagem da OAB e aprovação antes de sair.">
      {situacao && !conectado && (
        <Card className="mb-6 p-6 text-sm hover:translate-y-0">
          <p className="font-medium">O LinkedIn ainda não está conectado.</p>
          <p className="mt-1 text-muted-foreground">
            Siga o manual "Conexão do LinkedIn" (página do escritório, aplicativo e chaves) e depois clique em Conectar no card do LinkedIn da Visão Geral. Enquanto isso, já dá para escrever e guardar rascunhos aqui.
          </p>
        </Card>
      )}
      {conectado && (
        <p className="mb-6 text-sm text-muted-foreground">
          Conectado como <span className="font-medium text-foreground">{situacao?.nome}</span>
          {typeof situacao?.dias_para_vencer === "number" && <> · a conexão vence em {situacao.dias_para_vencer} dias (renove em Visão Geral → Reconectar)</>}
        </p>
      )}

      <div className="space-y-6">
        <Secao titulo="Novo post" descricao="A IA escreve no tom da Dra. para empresas, RH e trabalhadores. Com o link de um artigo do blog, o post sai com o card do artigo (título, descrição e capa).">
          <div className="flex flex-wrap gap-2">
            <Input value={tema} onChange={(e) => setTema(e.target.value)} placeholder="Tema ou artigo (ex.: multa do artigo 477 para o RH)" className="min-w-64 flex-1" />
            <Button variant="outline" disabled={tema.trim().length < 3 || !!ocupado} onClick={() => rodar("sugerir",
              () => apiFetch("/linkedin/posts/sugerir", { method: "POST", body: JSON.stringify({ tema }) }),
              "Texto pronto. Revise antes de agendar.", async (r) => setTexto((await r.json()).texto))}>
              {ocupado === "sugerir" ? <Loader2 className="animate-spin" /> : <Sparkles />} Escrever com IA
            </Button>
          </div>
          <div className="mt-3"><TextoComOab valor={texto} aoMudar={setTexto} linhas={10} limite={LIMITE} aoConferir={setOab} placeholder="Texto do post" /></div>
          <div className="mt-3 grid gap-3 md:grid-cols-[1fr_14rem]">
            <Input value={link} onChange={(e) => setLink(e.target.value)} placeholder="Link do artigo (opcional): https://advogadaleticiabarros.com.br/blog/..." />
            <Input type="datetime-local" value={quando} onChange={(e) => setQuando(e.target.value)} />
          </div>
          <div className="mt-3 flex flex-wrap justify-end gap-2">
            <Button variant="outline" disabled={texto.trim().length < 10 || !!ocupado} onClick={() => salvar("rascunho")}>Salvar rascunho</Button>
            <Button disabled={texto.trim().length < 10 || texto.length > LIMITE || bloqueia(oab) || !!ocupado} onClick={() => salvar("aprovado")}>
              <CalendarClock /> Aprovar e agendar
            </Button>
          </div>
          {mensagem && (
            <div className="mt-3 space-y-2">
              <p className={`text-sm ${mensagem.tipo === "ok" ? "text-emerald-600 dark:text-emerald-400" : "text-destructive"}`}>{mensagem.texto}</p>
              {mensagem.problemas && <ListaOab problemas={mensagem.problemas} />}
            </div>
          )}
        </Secao>

        <Secao titulo="Fila do LinkedIn" descricao="Rascunhos, agendados e publicados. Post com link de artigo que ainda não está no blog espera o artigo ir ao ar.">
          {!posts?.length && <p className="text-sm text-muted-foreground">Nenhum post ainda.</p>}
          <ul className="space-y-3">
            {posts?.map((p) => (
              <li key={p.id} className="rounded-md border p-3">
                <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                  <span className={`rounded-full px-2 py-0.5 font-medium ${p.status === "erro" ? "bg-destructive/15 text-destructive" : "bg-muted"}`}>{NOME_STATUS[p.status]}</span>
                  <span className="text-muted-foreground">{new Date(p.publicar_em).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}</span>
                </div>
                <p className="mt-2 whitespace-pre-line text-sm">{p.texto}</p>
                {p.link && <p className="mt-1 break-all text-xs text-muted-foreground">Link: {p.link}</p>}
                {p.erro && <p className="mt-1 text-xs text-destructive">{p.erro}</p>}
                <ListaOab problemas={p.problemas} />
                <div className="mt-2 flex flex-wrap gap-2">
                  {p.link_publicado && <a href={p.link_publicado} target="_blank" rel="noreferrer"><Button size="xs" variant="outline"><ExternalLink /> Ver no LinkedIn</Button></a>}
                  {(p.status === "rascunho" || p.status === "erro") && (
                    <Button size="xs" variant="outline" disabled={!!ocupado || bloqueia(p.problemas)} onClick={() => aprovar(p)}><CalendarClock /> Aprovar e agendar</Button>
                  )}
                  {p.status !== "publicado" && conectado && (
                    <Button size="xs" disabled={!!ocupado || bloqueia(p.problemas)} onClick={() => rodar(`pub-${p.id}`,
                      () => apiFetch(`/linkedin/posts/${p.id}/publicar-agora`, { method: "POST" }), "Publicado no LinkedIn.", carregar)}>
                      {ocupado === `pub-${p.id}` ? <Loader2 className="animate-spin" /> : <Send />} Publicar agora
                    </Button>
                  )}
                  <Button size="xs" variant="ghost" disabled={!!ocupado} onClick={() => rodar(`del-${p.id}`,
                    () => apiFetch(`/linkedin/posts/${p.id}`, { method: "DELETE" }),
                    p.status === "publicado" ? "Post apagado também do LinkedIn." : "Post apagado.", carregar)}>
                    <Trash2 /> Apagar
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        </Secao>
      </div>
    </AppShell>
  );
}
