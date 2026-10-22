"use client";

import { Check, EyeOff, ExternalLink, RotateCcw, Wand2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { BarrasHorizontais, LinhaAlcance } from "../../crescimento/_components/graficos";
import { AvisoSecao, Kpi, Secao, Tabela } from "./comuns";
import { numero, type Aba, type Painel, type Recomendacao } from "./tipos";

function serieLinha(pontos: { data: string; valor: number }[]) {
  const media = pontos.length ? pontos.reduce((s, p) => s + p.valor, 0) / pontos.length : 0;
  const pico = pontos.length ? pontos.reduce((a, b) => (b.valor > a.valor ? b : a)) : null;
  return { serie: pontos, media, pico };
}

const NOME_SECAO: Record<string, string> = { site: "Site", blog: "Blog", lp: "Landing pages", contato: "Página de contato" };

/* ------------------------------------------------------------------ Resumo */

export function AbaResumo({ painel, irPara }: { painel: Painel; irPara: (a: Aba) => void }) {
  const d = painel.desempenho;
  const ga = painel.analytics;
  const gsc = painel.search_console;
  const av = painel.avaliacoes;
  return (
    <div className="space-y-6">
      <Secao titulo="Perfil da Empresa no Google" descricao="Últimos 30 dias, comparados com os 30 anteriores.">
        <AvisoSecao erro={painel.erros.desempenho} nome="Desempenho do Perfil" />
        {d && (
          <>
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              <Kpi rotulo="Aparições na Busca" valor={d.totais_30d.buscas} anterior={d.totais_30d_anterior.buscas} />
              <Kpi rotulo="Aparições no Maps" valor={d.totais_30d.maps} anterior={d.totais_30d_anterior.maps} />
              <Kpi rotulo="Ligações" valor={d.totais_30d.ligacoes} anterior={d.totais_30d_anterior.ligacoes} />
              <Kpi rotulo="Pedidos de rota" valor={d.totais_30d.rotas} anterior={d.totais_30d_anterior.rotas} />
              <Kpi rotulo="Cliques no site" valor={d.totais_30d.cliques_site} anterior={d.totais_30d_anterior.cliques_site} />
              <Kpi rotulo="Conversas" valor={d.totais_30d.conversas} anterior={d.totais_30d_anterior.conversas} />
              {av && <Kpi rotulo="Nota no Google" valor={av.media ? av.media.toLocaleString("pt-BR") : "—"} sufixo={`(${av.total})`} />}
              {av && <Kpi rotulo="Avaliações sem resposta" valor={av.sem_resposta} />}
            </div>
            <div className="mt-6">
              <p className="mb-2 text-xs font-medium text-muted-foreground">Aparições por dia (Busca + Maps), 90 dias</p>
              <LinhaAlcance {...serieLinha(d.serie.map((p) => ({ data: p.data, valor: p.buscas + p.maps })))} />
            </div>
          </>
        )}
      </Secao>

      <div className="grid gap-6 lg:grid-cols-2">
        <Secao titulo="Site (Google Analytics)" descricao="Visitas no site, blog e landing pages, 30 dias.">
          <AvisoSecao erro={painel.erros.analytics} nome="Google Analytics" />
          {ga && (
            <>
              <div className="grid grid-cols-3 gap-3">
                <Kpi rotulo="Visitas" valor={ga.totais_30d.sessoes} anterior={ga.totais_30d_anterior.sessoes} />
                <Kpi rotulo="Pessoas" valor={ga.totais_30d.usuarios} anterior={ga.totais_30d_anterior.usuarios} />
                <Kpi rotulo="Conversões" valor={ga.totais_30d.conversoes} anterior={ga.totais_30d_anterior.conversoes} />
              </div>
              <div className="mt-5">
                <LinhaAlcance {...serieLinha(ga.serie.map((p) => ({ data: p.data, valor: p.sessoes })))} />
              </div>
            </>
          )}
        </Secao>
        <Secao titulo="Busca orgânica (Search Console)" descricao="Como o site aparece no Google, 28 dias.">
          <AvisoSecao erro={painel.erros.search_console} nome="Search Console" />
          {gsc && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <Kpi rotulo="Cliques" valor={gsc.totais_28d.cliques} anterior={gsc.totais_28d_anterior.cliques} />
                <Kpi rotulo="Aparições" valor={gsc.totais_28d.impressoes} anterior={gsc.totais_28d_anterior.impressoes} />
                <Kpi rotulo="Taxa de clique" valor={gsc.totais_28d.ctr.toLocaleString("pt-BR")} sufixo="%" />
                <Kpi rotulo="Posição média" valor={gsc.totais_28d.posicao.toLocaleString("pt-BR")} ajuda="Quanto menor, melhor (1 = topo)." />
              </div>
              <div className="mt-5">
                <LinhaAlcance {...serieLinha(gsc.serie.map((p) => ({ data: p.data, valor: p.cliques })))} />
              </div>
            </>
          )}
        </Secao>
      </div>

      {ga && (
        <Card className="flex flex-wrap items-center justify-between gap-4 p-6 hover:translate-y-0">
          <div>
            <p className="text-xs font-semibold text-primary">Visitas vindas de IAs (90 dias)</p>
            <p className="mt-1 font-display text-3xl font-semibold">{numero(ga.ia.total_90d)}</p>
            <p className="mt-1 text-sm text-muted-foreground">
              {ga.ia.por_fonte.length
                ? ga.ia.por_fonte.map((f) => `${f.fonte} (${f.sessoes})`).join(" · ")
                : "Nenhuma visita de ChatGPT, Gemini, Perplexity ou Copilot ainda."}
            </p>
          </div>
          <Button variant="outline" onClick={() => irPara("site")}>Ver site e IAs</Button>
        </Card>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ Melhorias */

const COR_PRIORIDADE = { alta: "bg-destructive/15 text-destructive", media: "bg-amber-500/15 text-amber-600 dark:text-amber-400", baixa: "bg-muted text-muted-foreground" };
const NOME_PRIORIDADE = { alta: "Alta", media: "Média", baixa: "Baixa" };
const ABA_DA_ACAO: Record<string, Aba> = { editar_perfil: "perfil", responder_avaliacoes: "avaliacoes", criar_post: "posts", enviar_fotos: "perfil" };
const NOME_AREA: Record<string, string> = { configuracao: "Configuração", perfil: "Perfil", avaliacoes: "Avaliações", conteudo: "Conteúdo", busca: "Busca", site: "Site", ia: "IAs" };

export function AbaMelhorias({
  recomendacoes,
  marcar,
  irPara,
}: {
  recomendacoes: Recomendacao[];
  marcar: (chave: string, status: Recomendacao["status"]) => void;
  irPara: (a: Aba) => void;
}) {
  const pendentes = recomendacoes.filter((r) => r.status === "pendente");
  const resolvidas = recomendacoes.filter((r) => r.status !== "pendente");
  return (
    <div className="space-y-4">
      {!pendentes.length && (
        <Card className="p-6 text-sm text-muted-foreground hover:translate-y-0">Nenhuma melhoria pendente. O Orbit revisa tudo de novo a cada atualização.</Card>
      )}
      {pendentes.map((r) => (
        <Card key={r.chave} className="p-5 hover:translate-y-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${COR_PRIORIDADE[r.prioridade]}`}>{NOME_PRIORIDADE[r.prioridade]}</span>
            <span className="text-[11px] text-muted-foreground">{NOME_AREA[r.area] ?? r.area}</span>
          </div>
          <h3 className="mt-2 font-medium">{r.titulo}</h3>
          <p className="mt-1 text-sm text-muted-foreground">{r.motivo}</p>
          {r.itens.length > 0 && (
            <ul className="mt-2 list-disc space-y-0.5 pl-5 text-sm">
              {r.itens.map((i) => <li key={i} className="break-all">{i}</li>)}
            </ul>
          )}
          <p className="mt-2 text-sm"><span className="font-medium">O que fazer: </span>{r.acao}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {r.aplicar && (
              <Button size="sm" onClick={() => irPara(ABA_DA_ACAO[r.aplicar!])}>
                <Wand2 /> Fazer pelo Orbit
              </Button>
            )}
            {r.link && (
              <a href={r.link} target="_blank" rel="noreferrer">
                <Button size="sm" variant="outline"><ExternalLink /> Abrir</Button>
              </a>
            )}
            <Button size="sm" variant="outline" onClick={() => marcar(r.chave, "feita")}><Check /> Marcar como feita</Button>
            <Button size="sm" variant="ghost" onClick={() => marcar(r.chave, "ignorada")}><EyeOff /> Ignorar</Button>
          </div>
        </Card>
      ))}
      {resolvidas.length > 0 && (
        <details className="rounded-lg border p-4">
          <summary className="cursor-pointer text-sm text-muted-foreground">Feitas e ignoradas ({resolvidas.length})</summary>
          <ul className="mt-3 space-y-2">
            {resolvidas.map((r) => (
              <li key={r.chave} className="flex items-center justify-between gap-3 text-sm">
                <span className={r.status === "feita" ? "line-through text-muted-foreground" : "text-muted-foreground"}>{r.titulo}</span>
                <Button size="xs" variant="ghost" onClick={() => marcar(r.chave, "pendente")}><RotateCcw /> Reabrir</Button>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ Buscas */

export function AbaBuscas({ painel }: { painel: Painel }) {
  const palavras = painel.palavras_chave ?? [];
  const gsc = painel.search_console;
  return (
    <div className="space-y-6">
      <Secao titulo="O que as pessoas buscam quando acham o Perfil" descricao="Termos digitados no Google e no Maps antes de ver o Perfil (últimos 6 meses). O Google esconde números abaixo de 15.">
        <AvisoSecao erro={painel.erros.palavras_chave} nome="Palavras buscadas" />
        <Tabela
          colunas={[{ rotulo: "Busca" }, { rotulo: "Vezes", alinhar: "direita" }]}
          linhas={palavras.map((p) => [p.termo, p.valor !== null ? numero(p.valor) : `menos de ${p.abaixo_de}`])}
        />
      </Secao>
      <Secao titulo="Buscas em que o site aparece (Search Console)" descricao="28 dias. Em destaque: posição de 4 a 20, as que estão perto do topo e valem um reforço no conteúdo.">
        <AvisoSecao erro={painel.erros.search_console} nome="Search Console" />
        {gsc && (
          <Tabela
            colunas={[{ rotulo: "Busca" }, { rotulo: "Aparições", alinhar: "direita" }, { rotulo: "Cliques", alinhar: "direita" }, { rotulo: "Taxa", alinhar: "direita" }, { rotulo: "Posição", alinhar: "direita" }]}
            linhas={[...gsc.consultas].sort((a, b) => b.impressoes - a.impressoes).slice(0, 100).map((c) => [
              <span key="t" className={c.posicao >= 4 && c.posicao <= 20 ? "font-medium text-primary" : ""}>{c.termo}</span>,
              numero(c.impressoes), numero(c.cliques), `${c.ctr.toLocaleString("pt-BR")}%`, c.posicao.toLocaleString("pt-BR"),
            ])}
          />
        )}
      </Secao>
      {gsc && (
        <Secao titulo="Páginas do site no Google" descricao="28 dias, ordenadas por aparições.">
          <Tabela
            colunas={[{ rotulo: "Página" }, { rotulo: "Aparições", alinhar: "direita" }, { rotulo: "Cliques", alinhar: "direita" }, { rotulo: "Taxa", alinhar: "direita" }, { rotulo: "Posição", alinhar: "direita" }]}
            linhas={[...gsc.paginas].sort((a, b) => b.impressoes - a.impressoes).map((p) => [
              <a key="p" href={p.pagina} target="_blank" rel="noreferrer" className="break-all hover:underline">{p.pagina.replace(/^https?:\/\/[^/]+/, "") || "/"}</a>,
              numero(p.impressoes), numero(p.cliques), `${p.ctr.toLocaleString("pt-BR")}%`, p.posicao.toLocaleString("pt-BR"),
            ])}
          />
        </Secao>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ Site e IAs */

function Item({ ok, texto }: { ok: boolean; texto: string }) {
  return (
    <li className="flex items-start gap-2 text-sm">
      <span className={`mt-1 h-2 w-2 shrink-0 rounded-full ${ok ? "bg-emerald-500" : "bg-destructive"}`} />
      {texto}
    </li>
  );
}

export function AbaSite({ painel }: { painel: Painel }) {
  const ga = painel.analytics;
  const site = painel.site;
  return (
    <div className="space-y-6">
      <AvisoSecao erro={painel.erros.analytics} nome="Google Analytics" />
      {ga && (
        <div className="grid gap-6 lg:grid-cols-2">
          <Secao titulo="Visualizações por parte do site" descricao="30 dias.">
            <BarrasHorizontais itens={Object.entries(ga.por_secao).sort((a, b) => b[1] - a[1]).map(([s, v]) => ({ rotulo: NOME_SECAO[s] ?? s, valor: v }))} />
          </Secao>
          <Secao titulo="De onde vêm as visitas" descricao="30 dias.">
            <BarrasHorizontais itens={ga.origens.slice(0, 10).map((o) => ({ rotulo: `${o.origem} / ${o.meio}`, valor: o.sessoes }))} />
          </Secao>
        </div>
      )}
      {ga && (
        <Secao titulo="Páginas mais vistas" descricao="30 dias, site, blog e landing pages.">
          <Tabela
            colunas={[{ rotulo: "Página" }, { rotulo: "Parte" }, { rotulo: "Visualizações", alinhar: "direita" }, { rotulo: "Visitas", alinhar: "direita" }]}
            linhas={ga.paginas.slice(0, 60).map((p) => [
              <span key="c" className="break-all">{p.host.startsWith("contato.") ? `contato · ${p.caminho}` : p.caminho}</span>,
              NOME_SECAO[p.secao] ?? p.secao, numero(p.visualizacoes), numero(p.sessoes),
            ])}
          />
        </Secao>
      )}
      <Secao titulo="Pronto para as IAs?" descricao="O que ChatGPT, Gemini, Perplexity e o Google precisam encontrar no site.">
        <AvisoSecao erro={painel.erros.site} nome="Checagem do site" />
        {site ? (
          <ul className="space-y-2">
            <Item ok={!site.robos_ia_bloqueados.length} texto={site.robos_ia_bloqueados.length ? `Robôs bloqueados no robots.txt: ${site.robos_ia_bloqueados.join(", ")}` : "Robôs de IA e de busca liberados no robots.txt"} />
            <Item ok={site.llms_txt} texto={site.llms_txt ? "Arquivo llms.txt publicado" : "Falta o arquivo llms.txt"} />
            <Item ok={site.home.schemas.some((s) => ["LegalService", "Attorney", "LocalBusiness"].includes(s))} texto={`Dados estruturados na página inicial: ${site.home.schemas.join(", ") || "nenhum"}`} />
            <Item ok={site.sitemap.ok} texto={site.sitemap.ok ? `Sitemap com ${site.sitemap.paginas} páginas${painel.sitemap_enviado ? ", enviado ao Google hoje" : ""}` : "Sitemap não encontrado"} />
            <Item ok={!site.paginas_sem_analytics.length} texto={site.paginas_sem_analytics.length ? `${site.paginas_sem_analytics.length} de ${site.paginas_html} páginas sem Google Analytics: ${site.paginas_sem_analytics.join(", ")}` : `Todas as ${site.paginas_html} páginas com Google Analytics`} />
            <Item ok={!site.paginas_sem_descricao.length} texto={site.paginas_sem_descricao.length ? `${site.paginas_sem_descricao.length} páginas sem descrição para o Google: ${site.paginas_sem_descricao.join(", ")}` : "Todas as páginas com descrição"} />
          </ul>
        ) : (
          !painel.erros.site && <p className="text-sm text-muted-foreground">A checagem do site roda junto com a atualização do painel.</p>
        )}
      </Secao>
    </div>
  );
}
