"use client";

import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import { Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

type DataEditorial = { data: string; nome: string; tipo: string; area: string; ideia: string };
type Foto = { url: string; autor: string; pagina: string; descricao: string; fonte: string; licenca: string };

async function chamar<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await apiFetch(path, init);
  const corpo = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(typeof corpo.detail === "string" ? corpo.detail : "Não deu certo. Tente de novo.");
  return corpo as T;
}

function Bloco({ titulo, descricao, children }: { titulo: string; descricao: string; children: ReactNode }) {
  return (
    <Card className="p-5 hover:translate-y-0">
      <h2 className="text-base font-semibold">{titulo}</h2>
      <p className="mb-4 text-sm text-muted-foreground">{descricao}</p>
      {children}
    </Card>
  );
}

/** Um campo + botão; mostra carregando, erro e o resultado que `render` devolver. */
function Consulta<T>({ placeholder, botao, executar, render, tipo = "text" }: {
  placeholder: string; botao: string; executar: (v: string) => Promise<T>; render: (r: T) => ReactNode; tipo?: string;
}) {
  const [valor, setValor] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [resultado, setResultado] = useState<T | null>(null);
  async function enviar(e: FormEvent) {
    e.preventDefault();
    if (!valor.trim()) return;
    setCarregando(true); setErro(null); setResultado(null);
    try { setResultado(await executar(valor.trim())); } catch (err) { setErro((err as Error).message); }
    finally { setCarregando(false); }
  }
  return (
    <div>
      <form onSubmit={enviar} className="flex gap-2">
        <Input type={tipo} value={valor} onChange={(e) => setValor(e.target.value)} placeholder={placeholder} />
        <Button type="submit" disabled={carregando}>{carregando ? <Loader2 className="h-4 w-4 animate-spin" /> : botao}</Button>
      </form>
      {erro && <p className="mt-3 text-sm text-destructive">{erro}</p>}
      {resultado !== null && <div className="mt-3 text-sm">{render(resultado)}</div>}
    </div>
  );
}

const SITUACAO_EMAIL: Record<string, string> = {
  ok: "Pode entrar na lista.", invalido: "Formato errado.", descartavel: "E-mail temporário (descartável).",
  sem_caixa: "Esse domínio não recebe e-mail.",
};

function Linha({ rotulo, valor }: { rotulo: string; valor: ReactNode }) {
  return <div className="flex justify-between gap-4 border-b py-1 last:border-0"><span className="text-muted-foreground">{rotulo}</span><span className="text-right">{valor || "—"}</span></div>;
}

export default function FerramentasPage() {
  const [datas, setDatas] = useState<DataEditorial[] | null>(null);
  const [avisoDatas, setAvisoDatas] = useState<string | null>(null);
  const [recorte, setRecorte] = useState<{ url?: string; erro?: string; carregando?: boolean }>({});

  useEffect(() => {
    chamar<{ aviso: string | null; datas: DataEditorial[] }>("/ferramentas/datas")
      .then((r) => { setDatas(r.datas); setAvisoDatas(r.aviso); })
      .catch((e) => setAvisoDatas((e as Error).message));
  }, []);

  async function recortar(arquivo: File | undefined) {
    if (!arquivo) return;
    setRecorte({ carregando: true });
    const form = new FormData();
    form.append("arquivo", arquivo);
    const r = await apiFetch("/ferramentas/recortar", { method: "POST", body: form });
    if (!r.ok) {
      const corpo = await r.json().catch(() => ({}));
      setRecorte({ erro: corpo.detail ?? "Não deu certo." });
      return;
    }
    setRecorte({ url: URL.createObjectURL(await r.blob()) });
  }

  const post = (body: object): RequestInit => ({ method: "POST", body: JSON.stringify(body) });

  return (
    <AppShell title="Ferramentas" description="Consultas rápidas com serviços públicos: datas, site, fotos, e-mails, empresas e links. As que pedem chave usam a de Configurações.">
      <div className="grid gap-4 lg:grid-cols-2">
        <Bloco titulo="Datas dos próximos 60 dias" descricao="Feriados nacionais e datas ligadas às áreas da Dra. A ideia é só ponto de partida: a peça passa pelo manual e pela OAB.">
          {avisoDatas && <p className="mb-2 text-sm text-amber-600">{avisoDatas}</p>}
          {!datas ? <Loader2 className="h-4 w-4 animate-spin" /> : (
            <ul className="space-y-2 text-sm">
              {datas.map((d) => (
                <li key={d.data + d.nome} className="flex gap-3">
                  <span className="w-12 shrink-0 font-medium tabular-nums">{d.data.slice(8, 10)}/{d.data.slice(5, 7)}</span>
                  <span><span className="font-medium">{d.nome}</span>{d.tipo === "feriado" && <span className="ml-1 text-xs text-muted-foreground">(feriado)</span>}<br />
                    <span className="text-muted-foreground">{d.area}: {d.ideia}</span></span>
                </li>
              ))}
            </ul>
          )}
        </Bloco>

        <Bloco titulo="Velocidade e SEO do site" descricao="Nota do Google (PageSpeed) no celular. Demora até 1 minuto. Precisa da chave do Google em Configurações para não esbarrar no limite.">
          <Consulta<{ notas: Record<string, number>; lcp_s: number | null; cls: number | null; tbt_ms: number | null }>
            placeholder="https://advogadaleticiabarros.com.br" botao="Medir" tipo="url"
            executar={(url) => chamar("/ferramentas/pagespeed", post({ url }))}
            render={(m) => (<>
              {Object.entries(m.notas).map(([k, v]) => <Linha key={k} rotulo={k.replace("_", " ")} valor={<span className={v >= 90 ? "text-emerald-600" : v >= 50 ? "text-amber-600" : "text-destructive"}>{v}</span>} />)}
              <Linha rotulo="Maior elemento (bom: até 2,5 s)" valor={m.lcp_s !== null ? `${m.lcp_s} s` : null} />
              <Linha rotulo="Página pulando (bom: até 0,1)" valor={m.cls} />
              <Linha rotulo="Tempo travado (bom: até 200 ms)" valor={m.tbt_ms !== null ? `${m.tbt_ms} ms` : null} />
            </>)} />
        </Bloco>

        <Bloco titulo="Buscar fotos" descricao="Pexels, Pixabay e Openverse juntos (só fotos de uso comercial liberado). Confira a página da foto antes de usar e não repita imagem entre posts.">
          <Consulta<Foto[]> placeholder="ex.: mulher grávida trabalhando" botao="Buscar"
            executar={(consulta) => chamar("/ferramentas/fotos", post({ consulta, quantidade: 12 }))}
            render={(fotos) => fotos.length === 0 ? <p>Nenhuma foto encontrada.</p> : (
              <div className="grid grid-cols-3 gap-2">
                {fotos.map((f) => (
                  <a key={f.url} href={f.pagina || f.url} target="_blank" rel="noreferrer" title={`${f.fonte} · ${f.licenca} · ${f.autor}`}>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={f.url} alt={f.descricao} className="aspect-[3/4] w-full rounded object-cover" loading="lazy" />
                    <span className="text-xs text-muted-foreground">{f.fonte}</span>
                  </a>
                ))}
              </div>
            )} />
        </Bloco>

        <Bloco titulo="Conferir e-mail" descricao="Antes de pôr na lista da newsletter: formato, e-mail temporário e se o domínio recebe e-mail.">
          <Consulta<{ situacao: string; conferido: boolean }> placeholder="nome@exemplo.com" botao="Conferir" tipo="email"
            executar={(email) => chamar("/ferramentas/verificar-email", post({ email }))}
            render={(r) => <p className={r.situacao === "ok" ? "text-emerald-600" : "text-destructive"}>{SITUACAO_EMAIL[r.situacao]}{!r.conferido && " (serviço fora do ar; não deu para conferir)"}</p>} />
        </Bloco>

        <Bloco titulo="Empresa pelo CNPJ" descricao="Dados públicos da Receita: situação, atividade, porte e cidade. Útil para o público de empresas (B2B).">
          <Consulta<Record<string, string | null>> placeholder="00.000.000/0000-00" botao="Consultar"
            executar={(c) => chamar(`/ferramentas/cnpj/${c.replace(/\D/g, "")}`)}
            render={(e) => (<>
              <Linha rotulo="Razão social" valor={e.razao_social} /><Linha rotulo="Nome fantasia" valor={e.nome_fantasia} />
              <Linha rotulo="Situação" valor={e.situacao} /><Linha rotulo="Atividade" valor={e.atividade} />
              <Linha rotulo="Porte" valor={e.porte} /><Linha rotulo="Cidade" valor={`${e.cidade}/${e.uf}`} />
              <Linha rotulo="Aberta em" valor={e.abertura?.split("-").reverse().join("/")} />
            </>)} />
        </Bloco>

        <Bloco titulo="Endereço pelo CEP" descricao="Correios, pela BrasilAPI (ou ViaCEP se ela cair).">
          <Consulta<Record<string, string>> placeholder="29055-000" botao="Buscar"
            executar={(c) => chamar(`/ferramentas/cep/${c.replace(/\D/g, "")}`)}
            render={(e) => <p>{[e.logradouro, e.bairro, `${e.cidade}/${e.uf}`].filter(Boolean).join(", ")}</p>} />
        </Bloco>

        <Bloco titulo="Link curto com contagem de cliques" descricao="Bitly. Use um link por lugar (bio, story, LinkedIn) para saber de onde vem cada visita.">
          <Consulta<{ link: string }> placeholder="https://advogadaleticiabarros.com.br/..." botao="Encurtar" tipo="url"
            executar={(url) => chamar("/ferramentas/encurtar", post({ url }))}
            render={(r) => <a className="font-medium underline" href={r.link} target="_blank" rel="noreferrer">{r.link}</a>} />
          <div className="mt-4">
            <Consulta<{ cliques: number }> placeholder="https://bit.ly/..." botao="Ver cliques"
              executar={(link) => chamar(`/ferramentas/cliques?link=${encodeURIComponent(link)}`)}
              render={(r) => <p>{r.cliques.toLocaleString("pt-BR")} cliques desde a criação.</p>} />
          </div>
        </Bloco>

        <Bloco titulo="Conferir links perigosos" descricao="Google Safe Browsing: cole os links da newsletter ou da legenda, um por linha ou separados por espaço.">
          <Consulta<{ seguro: boolean; perigosos: Record<string, string> }> placeholder="https://... https://..." botao="Conferir"
            executar={(texto) => chamar("/ferramentas/conferir-links", post({ urls: texto.split(/\s+/).filter((u) => u.startsWith("http")) }))}
            render={(r) => r.seguro ? <p className="text-emerald-600">Nenhum link perigoso.</p> : (
              <ul className="text-destructive">{Object.entries(r.perigosos).map(([u, m]) => <li key={u}>{u}: {m}</li>)}</ul>
            )} />
        </Bloco>

        <Bloco titulo="Recortar fundo de foto" descricao="remove.bg (50 grátis por mês, em tamanho de prévia). A foto original não é alterada.">
          <input type="file" accept="image/*" onChange={(e) => recortar(e.target.files?.[0])} className="text-sm" />
          {recorte.carregando && <Loader2 className="mt-3 h-4 w-4 animate-spin" />}
          {recorte.erro && <p className="mt-3 text-sm text-destructive">{recorte.erro}</p>}
          {recorte.url && (
            <div className="mt-3">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={recorte.url} alt="Foto recortada" className="max-h-64 rounded bg-[repeating-conic-gradient(#ddd_0_25%,transparent_0_50%)] bg-[length:16px_16px]" />
              <a href={recorte.url} download="recorte.png" className="mt-2 inline-block text-sm underline">Baixar PNG</a>
            </div>
          )}
        </Bloco>
      </div>
    </AppShell>
  );
}
