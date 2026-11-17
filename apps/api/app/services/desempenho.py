"""Desempenho: o mês de todos os canais numa tela só (site, Google, Perfil da Empresa, Instagram, Reels de teste,
LinkedIn, TikTok, blog).

Interface:
- `consolidar(fontes, hoje) -> dict` — função pura. Recebe o que cada canal já guarda no Orbit e devolve
  `{"avisos": [...], "secoes": [...]}`. Cada seção: `chave`, `titulo`, `situacao` ("ok" | "sem_dados" |
  "sem_conexao"), `resumo` (uma frase), `kpis` [{rotulo, valor, anterior, formato, explicacao}], `listas`
  [{titulo, colunas, linhas}], `link` (tela detalhada) e `atualizado_em`. `formato`: numero | percentual | posicao | nota.
- `montar_desempenho(db, tenant_id, hoje=None)` — lê do banco (painel do Google, análise e posts do Instagram,
  filas do LinkedIn, TikTok e blog) e chama `consolidar`.

Nada aqui chama API externa: os números vêm das coletas diárias (06h) que já existem.
"""
import uuid
from datetime import date, datetime, timedelta, timezone
from statistics import median

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.instagram_post import InstagramPost
from app.models.presenca_google import LinkedInPost
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.services.analise_instagram import montar_analise
from app.services.central_google import ultimo_painel
from app.services import tiktok as tiktok_servico
from app.services.teste_reels import MIN_COMPARTILHA_SALVA, FRACAO_DA_MEDIANA, julgar, views_referencia


def _kpi(rotulo: str, valor, anterior=None, formato: str = "numero", explicacao: str = "") -> dict:
    return {"rotulo": rotulo, "valor": valor, "anterior": anterior, "formato": formato, "explicacao": explicacao}


def _secao(chave, titulo, link, situacao="ok", resumo="", kpis=None, listas=None, atualizado_em=None) -> dict:
    return {"chave": chave, "titulo": titulo, "link": link, "situacao": situacao, "resumo": resumo,
            "kpis": kpis or [], "listas": listas or [], "atualizado_em": atualizado_em}


def _variacao(atual, anterior) -> str:
    if not anterior:
        return ""
    pct = round((atual - anterior) / anterior * 100)
    return f" ({'+' if pct >= 0 else ''}{pct}% sobre o mês anterior)"


def _site(painel: dict | None, coletado_em) -> dict:
    ga = (painel or {}).get("analytics")
    if not ga:
        return _secao("site", "Site (Google Analytics)", "/presenca", "sem_dados",
                      "Sem dados do Analytics ainda. Eles chegam com a atualização diária do painel do Google.")
    t, a = ga.get("totais_30d", {}), ga.get("totais_30d_anterior", {})
    contatos = ga.get("contatos", {})
    tipos = contatos.get("por_tipo", {})
    ia = ga.get("ia", {})
    paginas = [p for p in ga.get("paginas", []) if p.get("visualizacoes")][:8]
    return _secao(
        "site", "Site (Google Analytics)", "/presenca",
        resumo=f"{t.get('sessoes', 0)} visitas em 30 dias{_variacao(t.get('sessoes', 0), a.get('sessoes'))} "
               f"e {contatos.get('total_30d', 0)} contatos pelo site.",
        kpis=[
            _kpi("Visitas (30 dias)", t.get("sessoes", 0), a.get("sessoes"), explicacao="Sessões no site, blog e páginas."),
            _kpi("Pessoas (30 dias)", t.get("usuarios", 0), a.get("usuarios")),
            _kpi("Contatos pelo site (30 dias)", contatos.get("total_30d", 0),
                 explicacao=f"WhatsApp {tipos.get('whatsapp', 0)} · ligação {tipos.get('ligacao', 0)} · "
                            f"formulário {tipos.get('formulario', 0)}"),
            _kpi("Visitas vindas de IAs (90 dias)", ia.get("total_90d", 0),
                 explicacao="ChatGPT, Gemini, Perplexity e outras."),
        ],
        listas=[
            {"titulo": "Páginas mais vistas (30 dias)", "colunas": ["Página", "Visualizações"],
             "linhas": [[p["caminho"], p["visualizacoes"]] for p in paginas]},
            {"titulo": "De onde vêm as visitas (30 dias)", "colunas": ["Origem", "Visitas"],
             "linhas": [[f"{o['origem']} / {o['meio']}", o["sessoes"]] for o in ga.get("origens", [])[:8]]},
            {"titulo": "Páginas que geraram contato (30 dias)", "colunas": ["Página", "WhatsApp", "Ligação", "Formulário"],
             "linhas": [[p["caminho"], p["whatsapp"], p["ligacao"], p["formulario"]] for p in contatos.get("por_pagina", [])[:8]]},
        ],
        atualizado_em=coletado_em,
    )


def _busca(painel: dict | None, coletado_em) -> dict:
    sc = (painel or {}).get("search_console")
    if not sc:
        return _secao("busca", "Busca no Google (Search Console)", "/presenca", "sem_dados",
                      "Sem dados do Search Console ainda.")
    t, a = sc.get("totais_28d", {}), sc.get("totais_28d_anterior", {})
    return _secao(
        "busca", "Busca no Google (Search Console)", "/presenca",
        resumo=f"O site apareceu {t.get('impressoes', 0)} vezes no Google em 28 dias e recebeu {t.get('cliques', 0)} cliques"
               f"{_variacao(t.get('cliques', 0), a.get('cliques'))}.",
        kpis=[
            _kpi("Cliques (28 dias)", t.get("cliques", 0), a.get("cliques")),
            _kpi("Aparições na busca (28 dias)", t.get("impressoes", 0), a.get("impressoes")),
            _kpi("Taxa de clique", t.get("ctr", 0), a.get("ctr"), "percentual", "De cada 100 aparições, quantas viraram clique."),
            _kpi("Posição média", t.get("posicao", 0), a.get("posicao"), "posicao", "Quanto menor, mais perto do topo."),
        ],
        listas=[{"titulo": "Buscas que mais trouxeram o site (28 dias)",
                 "colunas": ["Busca", "Cliques", "Aparições", "Posição"],
                 "linhas": [[c["termo"], c["cliques"], c["impressoes"], c["posicao"]] for c in sc.get("consultas", [])[:10]]}],
        atualizado_em=coletado_em,
    )


def _perfil_google(painel: dict | None, coletado_em) -> dict:
    d = (painel or {}).get("desempenho")
    av = (painel or {}).get("avaliacoes") or {}
    if not d:
        return _secao("perfil_google", "Perfil da Empresa no Google", "/presenca", "sem_dados",
                      "Sem dados do Perfil da Empresa ainda.")
    t, a = d.get("totais_30d", {}), d.get("totais_30d_anterior", {})
    vistas, vistas_ant = t.get("buscas", 0) + t.get("maps", 0), a.get("buscas", 0) + a.get("maps", 0)
    acoes = t.get("ligacoes", 0) + t.get("rotas", 0) + t.get("cliques_site", 0) + t.get("conversas", 0)
    return _secao(
        "perfil_google", "Perfil da Empresa no Google", "/presenca",
        resumo=f"O perfil foi visto {vistas} vezes em 30 dias{_variacao(vistas, vistas_ant)} e gerou {acoes} ações "
               f"(ligações, rotas, cliques e conversas).",
        kpis=[
            _kpi("Visualizações (30 dias)", vistas, vistas_ant, explicacao="Na Busca e no Maps."),
            _kpi("Ligações", t.get("ligacoes", 0), a.get("ligacoes")),
            _kpi("Pedidos de rota", t.get("rotas", 0), a.get("rotas")),
            _kpi("Cliques no site", t.get("cliques_site", 0), a.get("cliques_site")),
            _kpi("Nota média", av.get("media"), None, "nota", f"{av.get('total', 0)} avaliações"),
            _kpi("Avaliações sem resposta", av.get("sem_resposta", 0)),
        ],
        atualizado_em=coletado_em,
    )


def _instagram(analise: dict | None, recentes: list[dict], publicados_30d: int, agendados_7d: int) -> dict:
    kpis_ig = {k["chave"]: k for k in ((analise or {}).get("resumo") or {}).get("kpis", [])}
    if not kpis_ig or not kpis_ig.get("seguidores", {}).get("valor"):
        return _secao("instagram", "Instagram", "/crescimento", "sem_dados", "Sem dados do Instagram ainda.")

    def v(chave):
        return (kpis_ig.get(chave) or {}).get("valor", 0)

    return _secao(
        "instagram", "Instagram", "/crescimento",
        resumo=((analise or {}).get("resumo") or {}).get("texto", ""),
        kpis=[
            _kpi("Seguidores", v("seguidores")),
            _kpi("Novos seguidores (30 dias)", v("novos_seguidores_30d")),
            _kpi("Contas alcançadas (30 dias)", v("alcance_30d")),
            _kpi("Contas que interagiram (30 dias)", v("contas_engajadas_30d")),
            _kpi("Salvamentos (30 dias)", v("salvamentos_30d")),
            _kpi("Compartilhamentos (30 dias)", v("compartilhamentos_30d")),
            _kpi("Cliques no site (30 dias)", v("cliques_site_30d")),
            _kpi("Publicações (30 dias)", publicados_30d, explicacao=f"{agendados_7d} agendadas para os próximos 7 dias."),
        ],
        listas=[{"titulo": "Posts dos últimos 30 dias que mais alcançaram",
                 "colunas": ["Data", "Formato", "Post", "Alcance", "Interações", "Salvos", "Envios"],
                 "linhas": [[p["data"], p["formato"], p["legenda"], p["alcance"], p["interacoes"], p["salvamentos"],
                             p["compartilhamentos"]] for p in recentes[:8]],
                 "links": [p.get("permalink") for p in recentes[:8]]}],
    )


def _reels_teste(testes: list[dict], referencia: list[int], agora: datetime) -> dict:
    """Reels de teste (Trial Reels, só para quem não segue): números de cada teste e se ele já pode ir para a grade.
    Pedido da Jessica, 17/11/2026: "precisamos de uma seção de Reels de teste para sabermos do desempenho"."""
    if not testes:
        return _secao("reels_teste", "Reels de teste", "/calendario", "sem_dados",
                      "Nenhum Reels de teste ainda. Eles aparecem aqui assim que forem agendados.")
    meta = round(median(referencia) * FRACAO_DA_MEDIANA) if referencia else None
    resumo = "Os testes vão primeiro para quem não segue o perfil. " + (
        f"Meta para ir para a grade: {meta} visualizações (70% da mediana dos últimos {len(referencia)} Reels do feed) "
        f"ou {MIN_COMPARTILHA_SALVA} envios + salvamentos." if meta is not None else "Ainda não há Reels do feed para comparar.")

    def situacao(t: dict) -> str:
        if t["status"] != "publicado":
            return "Não publicou: veja o calendário" if t["status"] in ("erro", "falhou") else f"Agendado para {t['agendado']}"
        if t.get("views") is None:
            return "Aguardando a coleta (todo dia de manhã, ou em Atualizar agora)"
        pub = t.get("publicado_em")
        if pub and agora - pub < timedelta(hours=24):
            return "Menos de 24 h no ar: ainda é cedo para julgar"
        if t["views"] == 0:
            return "0 visualizações: confira no app se o teste foi entregue"
        v = julgar({"views": t["views"], "shares": t.get("shares") or 0, "saved": t.get("saved") or 0}, referencia)
        return "Vai bem: pode ir para a grade" if v.liberado else "Abaixo da meta"

    def n(v):
        return v if v is not None else "—"

    publicados = [t for t in testes if t.get("views") is not None]
    linhas = [[t["titulo"], t["publicado_em"].strftime("%d/%m %H:%M") if t.get("publicado_em") else "—", n(t.get("views")),
               n(t.get("alcance")), n(t.get("shares")), n(t.get("saved")), n(t.get("curtidas")),
               round(t["tempo_medio_ms"] / 1000, 1) if t.get("tempo_medio_ms") else "—", situacao(t)] for t in testes]
    return _secao(
        "reels_teste", "Reels de teste", "/calendario", resumo=resumo,
        kpis=[_kpi("Testes com números", len(publicados), explicacao=f"{len(testes)} testes nos últimos 60 dias."),
              _kpi("Melhor teste (visualizações)", max((t["views"] for t in publicados), default=None)),
              _kpi("Visualizações somadas", sum(t["views"] for t in publicados)),
              _kpi("Envios + salvamentos", sum((t.get("shares") or 0) + (t.get("saved") or 0) for t in publicados),
                   explicacao="O sinal mais forte de que o Reels circula.")],
        listas=[{"titulo": "Reels de teste", "colunas": ["Reels", "Publicado", "Visualizações", "Alcance", "Envios", "Salvos",
                                                       "Curtidas", "Tempo médio (s)", "Situação"],
                 "linhas": linhas, "links": [t.get("permalink") for t in testes]}],
    )


def _linkedin(conexao: dict | None, posts: list[dict], painel: dict | None, hoje: date) -> dict:
    vindos = ((painel or {}).get("analytics") or {}).get("linkedin") or {}
    publicados = [p for p in posts if p["status"] == "publicado"]
    agendados = sorted((p for p in posts if p["status"] == "aprovado"), key=lambda p: p["publicar_em"])
    com_erro = [p for p in posts if p["status"] == "erro" or (p["erro"] and p["status"] == "aprovado")]
    if conexao is None:
        return _secao("linkedin", "LinkedIn", "/linkedin", "sem_conexao", "LinkedIn não conectado.")
    ultimos_30 = [p for p in publicados if p["publicar_em"].date() >= hoje - timedelta(days=30)]
    proximo = agendados[0]["publicar_em"] if agendados else None
    return _secao(
        "linkedin", "LinkedIn", "/linkedin",
        resumo=f"{len(ultimos_30)} posts publicados em 30 dias e {len(agendados)} agendados"
               + (f"; o próximo sai em {proximo:%d/%m}." if proximo else "."),
        kpis=[
            _kpi("Posts publicados (30 dias)", len(ultimos_30)),
            _kpi("Posts agendados", len(agendados)),
            _kpi("Visitas ao site vindas do LinkedIn (90 dias)", vindos.get("sessoes_90d", 0),
                 explicacao="Pelo Google Analytics: a API do LinkedIn não entrega números de posts."),
            _kpi("Contatos dessas visitas (90 dias)", vindos.get("contatos_90d", 0)),
            _kpi("Conexão vence em (dias)", conexao.get("dias_para_vencer")),
        ],
        listas=[
            {"titulo": "Próximos posts", "colunas": ["Data", "Início do texto"],
             "linhas": [[f"{p['publicar_em']:%d/%m}", p["texto"].split("\n")[0][:110]] for p in agendados[:5]]},
            {"titulo": "Páginas do site abertas a partir do LinkedIn (90 dias)", "colunas": ["Página", "Visitas", "Contatos"],
             "linhas": [[l["pagina"], l["sessoes"], l["contatos"]] for l in vindos.get("por_pagina", [])[:8]]},
        ] + ([{"titulo": "Posts com aviso", "colunas": ["Data", "Aviso"],
               "linhas": [[f"{p['publicar_em']:%d/%m}", p["erro"]] for p in com_erro[:5]]}] if com_erro else []),
    )


def _tiktok(situacao: dict) -> dict:
    if not situacao.get("conectado"):
        return _secao("tiktok", "TikTok", "/tiktok", "sem_conexao",
                      "TikTok não conectado. Conecte na Visão Geral para os Reels irem também para lá.")
    ultimos = situacao.get("ultimos", [])
    return _secao(
        "tiktok", "TikTok", "/tiktok",
        resumo=f"{sum(1 for e in ultimos if e['status'] == 'publicado')} Reels publicados e "
               f"{len(situacao.get('no_rascunho', []))} esperando publicação no app.",
        kpis=[
            _kpi("Reels publicados", sum(1 for e in ultimos if e["status"] == "publicado")),
            _kpi("Esperando no app do TikTok", len(situacao.get("no_rascunho", []))),
            _kpi("Com erro", sum(1 for e in ultimos if e["status"] == "erro")),
            _kpi("Na fila do TikTok", len(situacao.get("fila", []))),
        ],
        listas=[{"titulo": "Últimos envios", "colunas": ["Reels", "Situação"],
                 "linhas": [[e["titulo"], e["status"]] for e in ultimos[:8]]}],
    )


def _blog(publicados_30d: list[str], proximos: list[tuple[date, str]], painel: dict | None) -> dict:
    paginas = [p for p in ((painel or {}).get("analytics") or {}).get("paginas", []) if p.get("secao") == "blog"
               and p["caminho"].rstrip("/") not in ("/blog", "/blog/index.html")]
    return _secao(
        "blog", "Blog", "/calendario",
        resumo=f"{len(publicados_30d)} artigos publicados em 30 dias e {len(proximos)} agendados.",
        kpis=[_kpi("Artigos publicados (30 dias)", len(publicados_30d)), _kpi("Artigos agendados", len(proximos))],
        listas=[
            {"titulo": "Artigos mais lidos (30 dias)", "colunas": ["Artigo", "Visualizações"],
             "linhas": [[p["caminho"], p["visualizacoes"]] for p in paginas[:8]]},
            {"titulo": "Próximos artigos", "colunas": ["Data", "Título"],
             "linhas": [[f"{d:%d/%m}", t] for d, t in proximos[:6]]},
        ],
    )


def _avisos(secoes: list[dict], painel: dict | None, conexao_li: dict | None, tiktok: dict) -> list[dict]:
    avisos = []
    av = (painel or {}).get("avaliacoes") or {}
    if av.get("sem_resposta"):
        avisos.append({"texto": f"{av['sem_resposta']} avaliação(ões) do Google sem resposta.", "link": "/presenca"})
    if conexao_li and conexao_li.get("dias_para_vencer") is not None and conexao_li["dias_para_vencer"] <= 7:
        avisos.append({"texto": f"A conexão do LinkedIn vence em {conexao_li['dias_para_vencer']} dia(s): reconecte na Visão Geral.",
                       "link": "/visao-geral"})
    if tiktok.get("no_rascunho"):
        avisos.append({"texto": f"{len(tiktok['no_rascunho'])} Reels esperando publicação no app do TikTok.", "link": "/tiktok"})
    for s in secoes:
        if s["situacao"] == "sem_conexao":
            avisos.append({"texto": s["resumo"], "link": s["link"] if s["chave"] != "tiktok" else "/visao-geral"})
    return avisos


def consolidar(fontes: dict, hoje: date) -> dict:
    painel, coletado = fontes.get("painel_google"), fontes.get("painel_coletado_em")
    secoes = [
        _site(painel, coletado),
        _busca(painel, coletado),
        _perfil_google(painel, coletado),
        _instagram(fontes.get("analise_instagram"), fontes.get("instagram_recentes", []),
                   fontes.get("instagram_publicados_30d", 0), fontes.get("instagram_agendados_7d", 0)),
        _reels_teste(fontes.get("reels_teste", []), fontes.get("reels_teste_referencia", []),
                     fontes.get("agora") or datetime.now(timezone.utc)),
        _linkedin(fontes.get("linkedin_conexao"), fontes.get("linkedin_posts", []), painel, hoje),
        _tiktok(fontes.get("tiktok", {})),
        _blog(fontes.get("blog_publicados_30d", []), fontes.get("blog_proximos", []), painel),
    ]
    return {"avisos": _avisos(secoes, painel, fontes.get("linkedin_conexao"), fontes.get("tiktok", {})),
            "secoes": secoes, "gerado_em": datetime.now(timezone.utc).isoformat()}


async def montar_desempenho(db: AsyncSession, tenant_id: uuid.UUID, hoje: date | None = None) -> dict:
    hoje = hoje or datetime.now(timezone.utc).date()
    painel, coletado_em = await ultimo_painel(db, tenant_id)

    limite = datetime.now(timezone.utc) - timedelta(days=30)
    recentes = (await db.execute(select(InstagramPost).where(
        InstagramPost.tenant_id == tenant_id, InstagramPost.publicado_em >= limite)
        .order_by(InstagramPost.alcance.desc().nulls_last()).limit(8))).scalars().all()

    async def contar(canal: str, status: str, inicio: date, fim: date) -> int:
        return (await db.execute(select(func.count(ScheduledPost.id)).where(
            ScheduledPost.tenant_id == tenant_id, ScheduledPost.canal == canal, ScheduledPost.status == status,
            ScheduledPost.formato != "story", ScheduledPost.data_agendada >= inicio,
            ScheduledPost.data_agendada <= fim))).scalar_one()

    blog = (await db.execute(select(ScheduledPost).where(
        ScheduledPost.tenant_id == tenant_id, ScheduledPost.canal == "blog",
        ScheduledPost.data_agendada >= hoje - timedelta(days=30)).order_by(ScheduledPost.data_agendada))).scalars().all()

    conexao_li = (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == tenant_id, SocialConnection.plataforma == "linkedin",
        SocialConnection.status == "ativo"))).scalar_one_or_none()
    dias_li = None
    if conexao_li and conexao_li.expira_em:
        expira = conexao_li.expira_em if conexao_li.expira_em.tzinfo else conexao_li.expira_em.replace(tzinfo=timezone.utc)
        dias_li = (expira.date() - hoje).days
    posts_li = (await db.execute(select(LinkedInPost).where(LinkedInPost.tenant_id == tenant_id))).scalars().all()

    def _aware(d: datetime) -> datetime:
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)

    testes = (await db.execute(
        select(ScheduledPost, InstagramPost).outerjoin(InstagramPost, (InstagramPost.tenant_id == tenant_id)
                                                       & (InstagramPost.media_id == ScheduledPost.platform_post_id))
        .where(ScheduledPost.tenant_id == tenant_id, ScheduledPost.formato == "trial",
               ScheduledPost.data_agendada >= hoje - timedelta(days=60))
        .order_by(ScheduledPost.data_agendada.desc(), ScheduledPost.horario.desc()).limit(30))).all()

    fontes = {
        "reels_teste": [{
            "titulo": sp.titulo, "agendado": f"{sp.data_agendada.strftime('%d/%m')} {sp.horario}", "status": sp.status,
            "publicado_em": _aware(ig.publicado_em) if ig and ig.publicado_em else None,
            "permalink": ig.permalink if ig else None, "views": ig.visualizacoes if ig else None,
            "alcance": ig.alcance if ig else None, "shares": ig.compartilhamentos if ig else None,
            "saved": ig.salvamentos if ig else None, "curtidas": ig.curtidas if ig else None,
            "tempo_medio_ms": ig.tempo_medio_ms if ig else None} for sp, ig in testes],
        "reels_teste_referencia": await views_referencia(db, tenant_id),
        "painel_google": painel, "painel_coletado_em": coletado_em.isoformat() if coletado_em else None,
        "analise_instagram": await montar_analise(db, tenant_id),
        "instagram_recentes": [{
            "data": p.publicado_em.date().isoformat() if p.publicado_em else "", "formato": p.formato or "",
            "legenda": (p.legenda or "").strip().split("\n")[0][:90], "alcance": p.alcance or 0,
            "interacoes": p.interacoes or 0, "salvamentos": p.salvamentos or 0,
            "compartilhamentos": p.compartilhamentos or 0, "permalink": p.permalink} for p in recentes],
        "instagram_publicados_30d": await contar("instagram", "publicado", hoje - timedelta(days=30), hoje),
        "instagram_agendados_7d": await contar("instagram", "pronto", hoje, hoje + timedelta(days=7)),
        "linkedin_conexao": {"dias_para_vencer": dias_li} if conexao_li else None,
        "linkedin_posts": [{"status": p.status, "publicar_em": _aware(p.publicar_em), "texto": p.texto, "erro": p.erro}
                           for p in posts_li],
        "tiktok": await tiktok_servico.situacao(db, tenant_id),
        "blog_publicados_30d": [b.titulo for b in blog if b.status == "publicado" and b.data_agendada <= hoje],
        "blog_proximos": [(b.data_agendada, b.titulo) for b in blog if b.status != "publicado" and b.data_agendada >= hoje],
    }
    return consolidar(fontes, hoje)
