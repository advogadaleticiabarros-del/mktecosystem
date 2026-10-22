"use client";

import { useEffect, useState } from "react";
import { CalendarClock, ExternalLink, ImagePlus, Loader2, Plus, Send, Sparkles, Star, Trash2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { uploadMidia } from "@/app/(editorial)/_lib/editorial-api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { AvisoSecao, ListaOab, Secao, TextoComOab } from "./comuns";
import { dataCurta, lerErro, type Avaliacao, type Painel, type PostOrbit, type ProblemaOab, type Servico } from "./tipos";

const WHATSAPP = "https://wa.me/5527995151402";

function useAcao() {
  const [ocupado, setOcupado] = useState<string | null>(null);
  const [mensagem, setMensagem] = useState<{ tipo: "ok" | "erro"; texto: string; problemas?: ProblemaOab[] } | null>(null);
  async function rodar(nome: string, fn: () => Promise<Response>, sucesso: string, depois?: (r: Response) => Promise<void> | void) {
    setOcupado(nome);
    setMensagem(null);
    try {
      const resp = await fn();
      if (!resp.ok) {
        const erro = await lerErro(resp);
        setMensagem({ tipo: "erro", texto: erro.mensagem, problemas: erro.problemas });
        return;
      }
      await depois?.(resp);
      setMensagem({ tipo: "ok", texto: sucesso });
    } catch {
      setMensagem({ tipo: "erro", texto: "Falha de conexão. Tente de novo." });
    } finally {
      setOcupado(null);
    }
  }
  return { ocupado, mensagem, rodar, setMensagem };
}

function Mensagem({ m }: { m: ReturnType<typeof useAcao>["mensagem"] }) {
  if (!m) return null;
  return (
    <div className="space-y-2">
      <p className={`text-sm ${m.tipo === "ok" ? "text-emerald-600 dark:text-emerald-400" : "text-destructive"}`}>{m.texto}</p>
      {m.problemas && <ListaOab problemas={m.problemas} />}
    </div>
  );
}

const bloqueia = (p: ProblemaOab[]) => p.some((x) => x.nivel === "bloqueia");

/* ------------------------------------------------------------------ Perfil */

export function AbaPerfil({ painel, recarregar }: { painel: Painel; recarregar: () => Promise<void> }) {
  const perfil = painel.perfil;
  const [descricao, setDescricao] = useState(perfil?.descricao ?? "");
  const [oabDescricao, setOabDescricao] = useState<ProblemaOab[]>([]);
  const [site, setSite] = useState(perfil?.site ?? "");
  const [servicos, setServicos] = useState<Servico[]>(perfil?.servicos ?? []);
  const [agendar, setAgendar] = useState(painel.botoes?.find((b) => b.tipo === "APPOINTMENT")?.url ?? WHATSAPP);
  const [categoriaFoto, setCategoriaFoto] = useState("ADDITIONAL");
  const acao = useAcao();

  useEffect(() => {
    setDescricao(perfil?.descricao ?? "");
    setSite(perfil?.site ?? "");
    setServicos(perfil?.servicos ?? []);
  }, [perfil]);

  if (!perfil) return <AvisoSecao erro={painel.erros.perfil} nome="Perfil" />;

  const salvarPerfil = (corpo: object, sucesso: string) =>
    acao.rodar("perfil", () => apiFetch("/presenca/perfil", { method: "PATCH", body: JSON.stringify(corpo) }), sucesso, recarregar);

  const utm = `https://${painel.dominio ?? "advogadaleticiabarros.com.br"}/?utm_source=google&utm_medium=organic&utm_campaign=perfil-empresa`;

  async function enviarFoto(arquivo: File) {
    await acao.rodar("foto", async () => {
      const { url } = await uploadMidia(arquivo);
      return apiFetch("/presenca/fotos", { method: "POST", body: JSON.stringify({ url, categoria: categoriaFoto }) });
    }, "Foto enviada ao Google. Ela aparece no Perfil depois que o Google processa (alguns minutos).", recarregar);
  }

  return (
    <div className="space-y-6">
      <Mensagem m={acao.mensagem} />

      <Secao titulo={perfil.titulo} descricao={`${perfil.categoria_principal}${perfil.categorias_adicionais.length ? " · " + perfil.categorias_adicionais.join(" · ") : ""}`}
        acoes={perfil.maps_uri && <a href={perfil.maps_uri} target="_blank" rel="noreferrer"><Button size="sm" variant="outline"><ExternalLink /> Ver no Maps</Button></a>}>
        <dl className="grid gap-3 text-sm md:grid-cols-2">
          <div><dt className="text-xs text-muted-foreground">Endereço</dt><dd>{perfil.endereco}</dd></div>
          <div><dt className="text-xs text-muted-foreground">Telefones</dt><dd>{[perfil.telefone, ...perfil.telefones_extras].join(" · ")}</dd></div>
          <div><dt className="text-xs text-muted-foreground">Horários</dt><dd>{perfil.horarios.map((h) => `${h.dia} ${h.abre}–${h.fecha}`).join(" · ")}</dd></div>
          <div><dt className="text-xs text-muted-foreground">Área de atendimento</dt><dd>{perfil.area_atendimento.join(" · ")}</dd></div>
          {painel.atributos && (
            <div className="md:col-span-2"><dt className="text-xs text-muted-foreground">Atributos</dt>
              <dd>{Object.keys(painel.atributos).map((a) => a.replace(/^url_/, "link ").replaceAll("_", " ")).join(" · ")}</dd></div>
          )}
        </dl>
      </Secao>

      <Secao titulo="Descrição" descricao="Até 750 caracteres. O Orbit sugere um texto com a cidade e os assuntos mais buscados; nada vai para o Google sem você salvar."
        acoes={<Button size="sm" variant="outline" disabled={acao.ocupado === "sugerir"} onClick={() => acao.rodar("sugerir",
          () => apiFetch("/presenca/perfil/sugerir-descricao", { method: "POST" }), "Sugestão pronta. Revise antes de salvar.",
          async (r) => setDescricao((await r.json()).texto))}>
          {acao.ocupado === "sugerir" ? <Loader2 className="animate-spin" /> : <Sparkles />} Sugerir com IA</Button>}>
        <TextoComOab valor={descricao} aoMudar={setDescricao} linhas={8} limite={750} aoConferir={setOabDescricao} />
        <Button className="mt-3" disabled={acao.ocupado === "perfil" || descricao.length > 750 || bloqueia(oabDescricao) || descricao === perfil.descricao}
          onClick={() => salvarPerfil({ descricao }, "Descrição atualizada no Google.")}>
          <Send /> Salvar no Google
        </Button>
      </Secao>

      <Secao titulo="Serviços" descricao="Nome e descrição de cada serviço. Os serviços com nome técnico (estruturados) do Google são mantidos.">
        <div className="space-y-3">
          {servicos.map((s, i) => (
            <div key={i} className="grid gap-2 rounded-md border p-3 md:grid-cols-[14rem_1fr_auto]">
              <Input value={s.nome} placeholder="Nome do serviço" onChange={(e) => setServicos(servicos.map((x, j) => (j === i ? { ...x, nome: e.target.value } : x)))} />
              <Input value={s.descricao} placeholder="Descrição (1 ou 2 frases)" onChange={(e) => setServicos(servicos.map((x, j) => (j === i ? { ...x, descricao: e.target.value } : x)))} />
              <Button variant="ghost" size="icon" title="Remover" onClick={() => setServicos(servicos.filter((_, j) => j !== i))}><Trash2 /></Button>
            </div>
          ))}
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          <Button variant="outline" size="sm" onClick={() => setServicos([...servicos, { nome: "", descricao: "" }])}><Plus /> Adicionar serviço</Button>
          <Button size="sm" disabled={acao.ocupado === "perfil"} onClick={() => salvarPerfil({ servicos: servicos.filter((s) => s.nome.trim()) }, "Serviços atualizados no Google.")}>
            <Send /> Salvar serviços no Google
          </Button>
        </div>
      </Secao>

      <div className="grid gap-6 lg:grid-cols-2">
        <Secao titulo="Link do site" descricao="Com a marcação (utm), o Analytics separa as visitas que vêm do Perfil.">
          <Input value={site} onChange={(e) => setSite(e.target.value)} />
          <div className="mt-3 flex flex-wrap gap-2">
            <Button size="sm" variant="outline" onClick={() => setSite(utm)}>Usar link com rastreio</Button>
            <Button size="sm" disabled={acao.ocupado === "perfil" || site === perfil.site} onClick={() => salvarPerfil({ site }, "Link do site atualizado no Google.")}><Send /> Salvar</Button>
          </div>
        </Secao>
        <Secao titulo="Botão “Agendar”"descricao="Aparece no Perfil para quem quer marcar horário.">
          <AvisoSecao erro={painel.erros.botoes} nome="Botões do Perfil" />
          <Input value={agendar} onChange={(e) => setAgendar(e.target.value)} />
          <Button className="mt-3" size="sm" disabled={acao.ocupado === "botao"} onClick={() => acao.rodar("botao",
            () => apiFetch("/presenca/botao", { method: "PUT", body: JSON.stringify({ tipo: "APPOINTMENT", url: agendar }) }),
            "Botão \"Agendar\" salvo no Google.", recarregar)}><CalendarClock /> Salvar botão</Button>
        </Secao>
      </div>

      <Secao titulo="Fotos" descricao={painel.midia ? `${painel.midia.fotos} fotos e ${painel.midia.videos} vídeos no Perfil.` : undefined}>
        <AvisoSecao erro={painel.erros.midia} nome="Fotos" />
        <div className="flex flex-wrap items-center gap-2">
          <select value={categoriaFoto} onChange={(e) => setCategoriaFoto(e.target.value)} className="h-8 rounded-md border bg-background px-2 text-sm">
            <option value="ADDITIONAL">Outras</option>
            <option value="AT_WORK">No trabalho</option>
            <option value="TEAMS">Equipe</option>
            <option value="INTERIOR">Interior do escritório</option>
            <option value="EXTERIOR">Fachada</option>
            <option value="COVER">Capa</option>
            <option value="LOGO">Logo</option>
          </select>
          <label className="inline-flex cursor-pointer items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground">
            {acao.ocupado === "foto" ? <Loader2 className="h-4 w-4 animate-spin" /> : <ImagePlus className="h-4 w-4" />} Enviar foto
            <input type="file" accept="image/jpeg,image/png" className="hidden" onChange={(e) => e.target.files?.[0] && enviarFoto(e.target.files[0])} />
          </label>
        </div>
        {painel.midia && (
          <div className="mt-4 grid grid-cols-3 gap-2 md:grid-cols-6">
            {painel.midia.recentes.map((m) => (
              // eslint-disable-next-line @next/next/no-img-element
              <img key={m.name} src={m.url} alt="" className="aspect-square w-full rounded-md object-cover" />
            ))}
          </div>
        )}
      </Secao>
    </div>
  );
}

/* ------------------------------------------------------------------ Avaliações */

function CartaoAvaliacao({ a, aoResponder }: { a: Avaliacao; aoResponder: () => Promise<void> }) {
  const [texto, setTexto] = useState("");
  const [oab, setOab] = useState<ProblemaOab[]>([]);
  const acao = useAcao();
  return (
    <Card className={`p-5 hover:translate-y-0 ${!a.resposta && a.nota <= 3 ? "border-l-2 border-destructive" : ""}`}>
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm font-medium">{a.autor}</p>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{dataCurta(a.criada_em)}</span>
          <span className="flex">{Array.from({ length: a.nota }).map((_, i) => <Star key={i} className="h-3.5 w-3.5 fill-primary text-primary" />)}</span>
        </div>
      </div>
      {a.comentario && <p className="mt-2 text-sm text-muted-foreground">{a.comentario}</p>}
      {a.resposta ? (
        <p className="mt-3 rounded-md bg-accent/40 p-3 text-xs text-muted-foreground"><span className="font-medium text-foreground">Resposta: </span>{a.resposta}</p>
      ) : (
        <div className="mt-3 space-y-2">
          <TextoComOab valor={texto} aoMudar={setTexto} linhas={3} contexto="resposta_avaliacao" aoConferir={setOab} placeholder="Resposta pública da Dra." />
          <div className="flex flex-wrap gap-2">
            <Button size="sm" variant="outline" disabled={!!acao.ocupado} onClick={() => acao.rodar("sugerir",
              () => apiFetch("/presenca/avaliacoes/sugerir", { method: "POST", body: JSON.stringify({ autor: a.autor, nota: a.nota, comentario: a.comentario }) }),
              "Sugestão pronta. Revise antes de publicar.", async (r) => setTexto((await r.json()).texto))}>
              {acao.ocupado === "sugerir" ? <Loader2 className="animate-spin" /> : <Sparkles />} Sugerir resposta
            </Button>
            <Button size="sm" disabled={!!acao.ocupado || !texto.trim() || bloqueia(oab)} onClick={() => acao.rodar("responder",
              () => apiFetch("/presenca/avaliacoes/responder", { method: "POST", body: JSON.stringify({ name: a.name, texto }) }),
              "Resposta publicada no Google.", aoResponder)}>
              {acao.ocupado === "responder" ? <Loader2 className="animate-spin" /> : <Send />} Publicar resposta
            </Button>
          </div>
          <Mensagem m={acao.mensagem} />
        </div>
      )}
    </Card>
  );
}

export function AbaAvaliacoes({ painel, recarregar }: { painel: Painel; recarregar: () => Promise<void> }) {
  const [filtro, setFiltro] = useState<"sem_resposta" | "todas">("sem_resposta");
  const av = painel.avaliacoes;
  if (!av) return <AvisoSecao erro={painel.erros.avaliacoes} nome="Avaliações" />;
  const lista = filtro === "sem_resposta" ? av.lista.filter((a) => !a.resposta) : av.lista;
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-muted-foreground">
          Nota {av.media?.toLocaleString("pt-BR") ?? "—"} · {av.total} avaliações · {av.ultimos_30d} nos últimos 30 dias
          {painel.perfil?.link_avaliar && (
            <> · <a className="text-primary hover:underline" href={painel.perfil.link_avaliar} target="_blank" rel="noreferrer">link para pedir avaliação</a></>
          )}
        </p>
        <div className="flex gap-1">
          <Button size="sm" variant={filtro === "sem_resposta" ? "default" : "outline"} onClick={() => setFiltro("sem_resposta")}>Sem resposta ({av.sem_resposta})</Button>
          <Button size="sm" variant={filtro === "todas" ? "default" : "outline"} onClick={() => setFiltro("todas")}>Todas</Button>
        </div>
      </div>
      {!lista.length && <Card className="p-6 text-sm text-muted-foreground hover:translate-y-0">Tudo respondido.</Card>}
      {lista.map((a) => <CartaoAvaliacao key={a.name} a={a} aoResponder={recarregar} />)}
    </div>
  );
}

/* ------------------------------------------------------------------ Posts */

const BOTOES = [
  { valor: "", rotulo: "Sem botão" },
  { valor: "LEARN_MORE", rotulo: "Saiba mais" },
  { valor: "BOOK", rotulo: "Agendar" },
  { valor: "CALL", rotulo: "Ligar" },
];
const NOME_STATUS = { rascunho: "Rascunho", aprovado: "Agendado", publicado: "Publicado", erro: "Erro" };

function paraDatetimeLocal(iso?: string) {
  const d = iso ? new Date(iso) : new Date(Date.now() + 60 * 60 * 1000);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
}

export function AbaPosts({ painel, recarregar }: { painel: Painel; recarregar: () => Promise<void> }) {
  const [posts, setPosts] = useState<PostOrbit[] | null>(null);
  const [tema, setTema] = useState("");
  const [texto, setTexto] = useState("");
  const [oab, setOab] = useState<ProblemaOab[]>([]);
  const [botao, setBotao] = useState("LEARN_MORE");
  const [link, setLink] = useState(`https://${painel.dominio ?? "advogadaleticiabarros.com.br"}/blog/`);
  const [imagem, setImagem] = useState<string | null>(null);
  const [quando, setQuando] = useState(paraDatetimeLocal());
  const acao = useAcao();

  async function carregar() {
    const resp = await apiFetch("/presenca/posts");
    if (resp.ok) setPosts(await resp.json());
  }
  useEffect(() => { carregar(); }, []);

  function salvar(status: "rascunho" | "aprovado") {
    const corpo = { texto, botao: botao || null, link: botao && botao !== "CALL" ? link : null, imagem_url: imagem, publicar_em: new Date(quando).toISOString(), status };
    return acao.rodar("salvar", () => apiFetch("/presenca/posts", { method: "POST", body: JSON.stringify(corpo) }),
      status === "aprovado" ? "Post agendado. O Orbit publica no Google no horário marcado." : "Rascunho salvo.",
      async () => { setTexto(""); setTema(""); setImagem(null); await carregar(); });
  }

  return (
    <div className="space-y-6">
      <Secao titulo="Novo post no Google" descricao="O post aparece no Perfil, na Busca e no Maps. Toda publicação passa pela checagem da OAB.">
        <div className="flex flex-wrap gap-2">
          <Input value={tema} onChange={(e) => setTema(e.target.value)} placeholder="Tema (ex.: estabilidade da gestante no contrato de experiência)" className="min-w-64 flex-1" />
          <Button variant="outline" disabled={tema.trim().length < 3 || !!acao.ocupado} onClick={() => acao.rodar("sugerir",
            () => apiFetch("/presenca/posts/sugerir", { method: "POST", body: JSON.stringify({ tema }) }), "Texto pronto. Revise antes de agendar.",
            async (r) => setTexto((await r.json()).texto))}>
            {acao.ocupado === "sugerir" ? <Loader2 className="animate-spin" /> : <Sparkles />} Escrever com IA
          </Button>
        </div>
        <div className="mt-3"><TextoComOab valor={texto} aoMudar={setTexto} linhas={7} limite={1500} aoConferir={setOab} placeholder="Texto do post" /></div>
        <div className="mt-3 grid gap-3 md:grid-cols-[10rem_1fr_14rem]">
          <select value={botao} onChange={(e) => setBotao(e.target.value)} className="h-8 rounded-md border bg-background px-2 text-sm">
            {BOTOES.map((b) => <option key={b.valor} value={b.valor}>{b.rotulo}</option>)}
          </select>
          <Input value={link} onChange={(e) => setLink(e.target.value)} disabled={!botao || botao === "CALL"} placeholder="Link do botão" />
          <Input type="datetime-local" value={quando} onChange={(e) => setQuando(e.target.value)} />
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <label className="inline-flex cursor-pointer items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm">
            <ImagePlus className="h-4 w-4" /> {imagem ? "Trocar imagem" : "Imagem (opcional)"}
            <input type="file" accept="image/jpeg,image/png" className="hidden" onChange={async (e) => {
              const f = e.target.files?.[0];
              if (f) setImagem((await uploadMidia(f)).url);
            }} />
          </label>
          {imagem && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={imagem} alt="" className="h-12 w-12 rounded object-cover" />
          )}
          <div className="ml-auto flex gap-2">
            <Button variant="outline" disabled={texto.trim().length < 10 || !!acao.ocupado} onClick={() => salvar("rascunho")}>Salvar rascunho</Button>
            <Button disabled={texto.trim().length < 10 || texto.length > 1500 || bloqueia(oab) || !!acao.ocupado} onClick={() => salvar("aprovado")}>
              <CalendarClock /> Aprovar e agendar
            </Button>
          </div>
        </div>
        <div className="mt-3"><Mensagem m={acao.mensagem} /></div>
      </Secao>

      <Secao titulo="Fila do Orbit" descricao="Rascunhos, agendados e publicados pelo Orbit.">
        {!posts?.length && <p className="text-sm text-muted-foreground">Nenhum post ainda.</p>}
        <ul className="space-y-3">
          {posts?.map((p) => (
            <li key={p.id} className="rounded-md border p-3">
              <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                <span className={`rounded-full px-2 py-0.5 font-medium ${p.status === "erro" ? "bg-destructive/15 text-destructive" : "bg-muted"}`}>{NOME_STATUS[p.status]}</span>
                <span className="text-muted-foreground">{new Date(p.publicar_em).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}</span>
              </div>
              <p className="mt-2 whitespace-pre-line text-sm">{p.texto}</p>
              {p.erro && <p className="mt-1 text-xs text-destructive">{p.erro}</p>}
              <div className="mt-2 flex flex-wrap gap-2">
                {p.link_publicado && <a href={p.link_publicado} target="_blank" rel="noreferrer"><Button size="xs" variant="outline"><ExternalLink /> Ver no Google</Button></a>}
                {p.status !== "publicado" && (
                  <Button size="xs" disabled={!!acao.ocupado || bloqueia(p.problemas)} onClick={() => acao.rodar(`pub-${p.id}`,
                    () => apiFetch(`/presenca/posts/${p.id}/publicar-agora`, { method: "POST" }), "Publicado no Google.", async () => { await carregar(); await recarregar(); })}>
                    <Send /> Publicar agora
                  </Button>
                )}
                <Button size="xs" variant="ghost" disabled={!!acao.ocupado} onClick={() => {
                  if (p.status === "publicado" && !confirm("Apagar este post também do Google?")) return;
                  acao.rodar(`del-${p.id}`, () => apiFetch(`/presenca/posts/${p.id}`, { method: "DELETE" }), "Post apagado.", carregar);
                }}><Trash2 /> Apagar</Button>
              </div>
            </li>
          ))}
        </ul>
      </Secao>

      <Secao titulo="Posts que já estão no Google" descricao={painel.posts ? `${painel.posts.total} posts · ${painel.posts.ultimos_30d} nos últimos 30 dias` : undefined}>
        <AvisoSecao erro={painel.erros.posts} nome="Posts" />
        <ul className="space-y-3">
          {painel.posts?.lista.map((p) => (
            <li key={p.name} className="flex gap-3 rounded-md border p-3">
              {p.imagem && (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={p.imagem} alt="" className="h-16 w-16 shrink-0 rounded object-cover" />
              )}
              <div className="min-w-0">
                <p className="text-xs text-muted-foreground">{dataCurta(p.criado_em)} · {p.estado === "LIVE" ? "No ar" : p.estado}</p>
                <p className="mt-1 line-clamp-3 text-sm">{p.texto}</p>
                {p.link && <a href={p.link} target="_blank" rel="noreferrer" className="text-xs text-primary hover:underline">Ver no Google</a>}
              </div>
            </li>
          ))}
        </ul>
      </Secao>
    </div>
  );
}
