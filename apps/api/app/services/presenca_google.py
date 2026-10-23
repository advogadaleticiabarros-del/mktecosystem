"""Painel "Presença no Google": junta tudo que o Google sabe do escritório num dicionário só.

Interface: `await coletar_painel(api, conta, local, hoje)` devolve o painel. Cada seção
(perfil, desempenho, palavras-chave, avaliações, posts, fotos, verificação, botões,
Analytics, Search Console) é buscada de forma independente: se uma falhar (API
desativada, falta de permissão), ela fica `None` e o motivo vai para `painel["erros"]`,
sem derrubar as outras. O Analytics e o Search Console são achados sozinhos pelo
domínio do site cadastrado no Perfil.
"""
import re
import unicodedata
from datetime import date, datetime, timedelta, timezone
from urllib.parse import quote, urlparse

from app.integrations.social.google_api import GoogleApi, GoogleApiErro

INFO_URL = "https://mybusinessbusinessinformation.googleapis.com/v1"
PERF_URL = "https://businessprofileperformance.googleapis.com/v1"
V4_URL = "https://mybusiness.googleapis.com/v4"
VERIF_URL = "https://mybusinessverifications.googleapis.com/v1"
PLACE_URL = "https://mybusinessplaceactions.googleapis.com/v1"
GA_ADMIN_URL = "https://analyticsadmin.googleapis.com/v1beta"
GA_DATA_URL = "https://analyticsdata.googleapis.com/v1beta"
GSC_URL = "https://www.googleapis.com/webmasters/v3"

PERFIL_MASK = (
    "name,title,categories,phoneNumbers,websiteUri,regularHours,profile,serviceItems,"
    "storefrontAddress,metadata,openInfo,serviceArea"
)

METRICAS_DIARIAS = {
    "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH": "buscas",
    "BUSINESS_IMPRESSIONS_MOBILE_SEARCH": "buscas",
    "BUSINESS_IMPRESSIONS_DESKTOP_MAPS": "maps",
    "BUSINESS_IMPRESSIONS_MOBILE_MAPS": "maps",
    "CALL_CLICKS": "ligacoes",
    "BUSINESS_DIRECTION_REQUESTS": "rotas",
    "WEBSITE_CLICKS": "cliques_site",
    "BUSINESS_CONVERSATIONS": "conversas",
    "BUSINESS_BOOKINGS": "agendamentos",
}
CAMPOS_DESEMPENHO = ["buscas", "maps", "ligacoes", "rotas", "cliques_site", "conversas", "agendamentos"]

ESTRELAS = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}
DIAS_SEMANA = {
    "MONDAY": "Segunda", "TUESDAY": "Terça", "WEDNESDAY": "Quarta", "THURSDAY": "Quinta",
    "FRIDAY": "Sexta", "SATURDAY": "Sábado", "SUNDAY": "Domingo",
}

# Visitas que chegam de assistentes de IA (origem da sessão no Analytics).
FONTES_IA = re.compile(
    r"chatgpt|openai|perplexity|gemini|bard|copilot|claude\.ai|anthropic|deepseek|meta\.ai|grok|you\.com|phind",
    re.IGNORECASE,
)

# Eventos de contato registrados pelo /js/conversoes.js do site.
EVENTOS_CONTATO = {"contato_whatsapp": "whatsapp", "contato_ligacao": "ligacao", "generate_lead": "formulario"}

SECOES = [
    "perfil", "atributos", "desempenho", "palavras_chave", "avaliacoes", "posts", "midia",
    "verificacao", "botoes", "analytics", "search_console",
]


def _iso(d: date) -> str:
    return d.isoformat()


def _data_google(d: dict) -> str:
    return date(d["year"], d["month"], d["day"]).isoformat()


def _quando(texto: str | None) -> datetime | None:
    if not texto:
        return None
    return datetime.fromisoformat(texto.replace("Z", "+00:00"))


def _sem_acento(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def dominio_raiz(url: str | None) -> str | None:
    """`https://contato.exemplo.com.br/x` -> `exemplo.com.br`."""
    if not url:
        return None
    host = (urlparse(url if "//" in url else f"https://{url}").hostname or "").lower()
    partes = host.split(".")
    if len(partes) < 2:
        return None
    if len(partes) >= 3 and len(partes[-1]) == 2 and partes[-2] in {"com", "org", "net", "gov", "edu", "adv", "art"}:
        return ".".join(partes[-3:])
    return ".".join(partes[-2:])


def secao_da_pagina(host: str, caminho: str) -> str:
    host = (host or "").lower()
    if host.startswith("contato."):
        return "contato"
    if caminho.startswith("/blog"):
        return "blog"
    if caminho.startswith("/lp/") or caminho.startswith("/lp"):
        return "lp"
    return "site"


# ---------------------------------------------------------------- Perfil


def _normalizar_perfil(bruto: dict) -> dict:
    categorias = bruto.get("categories", {})
    endereco = bruto.get("storefrontAddress", {})
    telefones = bruto.get("phoneNumbers", {})
    horarios = [
        {
            "dia": DIAS_SEMANA.get(p.get("openDay"), p.get("openDay")),
            "abre": f"{p.get('openTime', {}).get('hours', 0):02d}:{p.get('openTime', {}).get('minutes', 0):02d}",
            "fecha": f"{p.get('closeTime', {}).get('hours', 0):02d}:{p.get('closeTime', {}).get('minutes', 0):02d}",
        }
        for p in bruto.get("regularHours", {}).get("periods", [])
    ]
    # Serviços de texto livre (editáveis no Orbit) e os "padrão" do Google, que são só um código
    # (`job_type_id:...`) e ficam intactos quando a lista de texto livre é salva.
    servicos, servicos_padrao = [], []
    for item in bruto.get("serviceItems", []):
        livre = item.get("freeFormServiceItem")
        if livre:
            rotulo = livre.get("label", {})
            servicos.append({"nome": rotulo.get("displayName", ""), "descricao": rotulo.get("description", "")})
        elif item.get("structuredServiceItem"):
            codigo = item["structuredServiceItem"].get("serviceTypeId", "")
            servicos_padrao.append(codigo.split(":")[-1].replace("_", " "))
    metadata = bruto.get("metadata", {})
    aberto = bruto.get("openInfo", {}).get("openingDate")
    return {
        "titulo": bruto.get("title", ""),
        "descricao": bruto.get("profile", {}).get("description", ""),
        "categoria_principal": categorias.get("primaryCategory", {}).get("displayName", ""),
        "categorias_adicionais": [c.get("displayName", "") for c in categorias.get("additionalCategories", [])],
        "telefone": telefones.get("primaryPhone", ""),
        "telefones_extras": telefones.get("additionalPhones", []),
        "site": bruto.get("websiteUri", ""),
        "endereco": ", ".join(
            [*endereco.get("addressLines", []), endereco.get("sublocality", ""), endereco.get("locality", ""),
             endereco.get("administrativeArea", ""), endereco.get("postalCode", "")]
        ).replace(", ,", ",").strip(", "),
        "cidade": endereco.get("locality", ""),
        "area_atendimento": [
            p.get("placeName", "") for p in bruto.get("serviceArea", {}).get("places", {}).get("placeInfos", [])
        ],
        "horarios": horarios,
        "servicos": servicos,
        "servicos_padrao": servicos_padrao,
        "maps_uri": metadata.get("mapsUri"),
        "link_avaliar": metadata.get("newReviewUri"),
        "place_id": metadata.get("placeId"),
        "status": bruto.get("openInfo", {}).get("status"),
        "aberto_desde": f"{aberto['year']}-{aberto.get('month', 1):02d}" if aberto else None,
    }


async def buscar_perfil(api: GoogleApi, local: str) -> dict:
    return _normalizar_perfil(await api.get(f"{INFO_URL}/{local}", {"readMask": PERFIL_MASK}))


async def _atributos(api: GoogleApi, local: str) -> dict:
    resultado = await api.get(f"{INFO_URL}/{local}/attributes")
    atributos = {}
    for a in resultado.get("attributes", []):
        nome = a.get("name", "").split("/")[-1]
        if "uriValues" in a:
            atributos[nome] = [u.get("uri") for u in a["uriValues"]]
        else:
            valores = a.get("values", [])
            atributos[nome] = valores[0] if len(valores) == 1 else valores
    return atributos


# ---------------------------------------------------------------- Desempenho


def _somar(serie: list[dict], inicio: date, fim: date) -> dict:
    totais = dict.fromkeys(CAMPOS_DESEMPENHO, 0)
    for ponto in serie:
        if _iso(inicio) <= ponto["data"] <= _iso(fim):
            for campo in CAMPOS_DESEMPENHO:
                totais[campo] += ponto[campo]
    return totais


async def _desempenho(api: GoogleApi, local: str, hoje: date) -> dict:
    fim = hoje - timedelta(days=1)
    inicio = fim - timedelta(days=89)
    params = {
        "dailyMetrics": list(METRICAS_DIARIAS),
        "dailyRange.start_date.year": str(inicio.year),
        "dailyRange.start_date.month": str(inicio.month),
        "dailyRange.start_date.day": str(inicio.day),
        "dailyRange.end_date.year": str(fim.year),
        "dailyRange.end_date.month": str(fim.month),
        "dailyRange.end_date.day": str(fim.day),
    }
    resultado = await api.get(f"{PERF_URL}/{local}:fetchMultiDailyMetricsTimeSeries", params)
    por_dia: dict[str, dict] = {}
    for bloco in resultado.get("multiDailyMetricTimeSeries", []):
        for serie in bloco.get("dailyMetricTimeSeries", []):
            campo = METRICAS_DIARIAS.get(serie.get("dailyMetric"))
            if campo is None:
                continue
            for valor in serie.get("timeSeries", {}).get("datedValues", []):
                dia = _data_google(valor["date"])
                ponto = por_dia.setdefault(dia, {"data": dia, **dict.fromkeys(CAMPOS_DESEMPENHO, 0)})
                ponto[campo] += int(valor.get("value", 0))
    serie_ordenada = [por_dia[d] for d in sorted(por_dia)]
    return {
        "serie": serie_ordenada,
        "totais_30d": _somar(serie_ordenada, fim - timedelta(days=29), fim),
        "totais_30d_anterior": _somar(serie_ordenada, fim - timedelta(days=59), fim - timedelta(days=30)),
    }


def _mes_anterior(d: date, meses: int) -> date:
    total = d.year * 12 + d.month - 1 - meses
    return date(total // 12, total % 12 + 1, 1)


async def _palavras_chave(api: GoogleApi, local: str, hoje: date) -> list[dict]:
    inicio, fim = _mes_anterior(hoje, 6), _mes_anterior(hoje, 1)
    itens = await api.paginar(
        f"{PERF_URL}/{local}/searchkeywords/impressions/monthly",
        "searchKeywordsCounts",
        {
            "monthlyRange.start_month.year": str(inicio.year),
            "monthlyRange.start_month.month": str(inicio.month),
            "monthlyRange.end_month.year": str(fim.year),
            "monthlyRange.end_month.month": str(fim.month),
        },
    )
    palavras = []
    for item in itens:
        valor = item.get("insightsValue", {})
        palavras.append(
            {
                "termo": item.get("searchKeyword", "").strip()[:120],
                "valor": int(valor["value"]) if "value" in valor else None,
                "abaixo_de": int(valor["threshold"]) if "threshold" in valor else None,
            }
        )
    return sorted(palavras, key=lambda p: (p["valor"] is None, -(p["valor"] or 0)))


# ---------------------------------------------------------------- Avaliações, posts, fotos (API v4)


def _normalizar_avaliacao(r: dict) -> dict:
    resposta = r.get("reviewReply") or {}
    return {
        "name": r.get("name"),
        "autor": r.get("reviewer", {}).get("displayName", "Anônimo"),
        "foto_autor": r.get("reviewer", {}).get("profilePhotoUrl"),
        "nota": ESTRELAS.get(r.get("starRating"), 0),
        "comentario": r.get("comment", ""),
        "criada_em": r.get("createTime"),
        "resposta": resposta.get("comment"),
        "respondida_em": resposta.get("updateTime"),
    }


async def _avaliacoes(api: GoogleApi, conta: str, local: str, hoje: date) -> dict:
    url = f"{V4_URL}/{conta}/{local}/reviews"
    params: dict = {"pageSize": 50, "orderBy": "updateTime desc"}
    brutas: list[dict] = []
    media, total = None, 0
    for _ in range(10):
        resultado = await api.get(url, params)
        brutas.extend(resultado.get("reviews", []))
        media = resultado.get("averageRating", media)
        total = resultado.get("totalReviewCount", total)
        if not resultado.get("nextPageToken"):
            break
        params["pageToken"] = resultado["nextPageToken"]
    lista = [_normalizar_avaliacao(r) for r in brutas]
    limite = datetime.combine(hoje - timedelta(days=30), datetime.min.time(), tzinfo=timezone.utc)
    return {
        "media": round(float(media), 2) if media is not None else None,
        "total": total or len(lista),
        "sem_resposta": sum(1 for a in lista if not a["resposta"]),
        "ultimos_30d": sum(1 for a in lista if (_quando(a["criada_em"]) or limite) > limite),
        "lista": lista,
    }


async def _posts(api: GoogleApi, conta: str, local: str, hoje: date) -> dict:
    brutos = await api.paginar(f"{V4_URL}/{conta}/{local}/localPosts", "localPosts", {"pageSize": 100}, limite=3)
    posts = sorted(
        (
            {
                "name": p.get("name"),
                "tipo": p.get("topicType", "STANDARD"),
                "texto": p.get("summary", ""),
                "criado_em": p.get("createTime"),
                "estado": p.get("state"),
                "link": p.get("searchUrl"),
                "imagem": (p.get("media") or [{}])[0].get("googleUrl"),
            }
            for p in brutos
        ),
        key=lambda p: p["criado_em"] or "",
        reverse=True,
    )
    limite = (hoje - timedelta(days=30)).isoformat()
    return {
        "total": len(posts),
        "ultimo_em": posts[0]["criado_em"] if posts else None,
        "ultimos_30d": sum(1 for p in posts if (p["criado_em"] or "") >= limite),
        "lista": posts[:30],
    }


async def _midia(api: GoogleApi, conta: str, local: str) -> dict:
    itens = await api.paginar(f"{V4_URL}/{conta}/{local}/media", "mediaItems", {"pageSize": 100}, limite=5)
    itens.sort(key=lambda m: m.get("createTime", ""), reverse=True)
    por_categoria: dict[str, int] = {}
    for m in itens:
        categoria = m.get("locationAssociation", {}).get("category", "OUTRA")
        por_categoria[categoria] = por_categoria.get(categoria, 0) + 1
    return {
        "total": len(itens),
        "fotos": sum(1 for m in itens if m.get("mediaFormat") == "PHOTO"),
        "videos": sum(1 for m in itens if m.get("mediaFormat") == "VIDEO"),
        "ultima_em": itens[0].get("createTime") if itens else None,
        "por_categoria": por_categoria,
        "recentes": [
            {"name": m.get("name"), "url": m.get("thumbnailUrl") or m.get("googleUrl"), "criada_em": m.get("createTime")}
            for m in itens[:12]
        ],
    }


async def _verificacao(api: GoogleApi, local: str) -> dict:
    return await api.get(f"{VERIF_URL}/{local}/VoiceOfMerchantState")


async def _botoes(api: GoogleApi, local: str) -> list[dict]:
    links = await api.paginar(f"{PLACE_URL}/{local}/placeActionLinks", "placeActionLinks")
    return [{"name": b.get("name"), "tipo": b.get("placeActionType"), "url": b.get("uri")} for b in links]


# ---------------------------------------------------------------- Google Analytics 4


def _linhas(relatorio: dict) -> list[tuple[list[str], list[float]]]:
    return [
        ([d.get("value", "") for d in linha.get("dimensionValues", [])],
         [float(m.get("value", 0) or 0) for m in linha.get("metricValues", [])])
        for linha in relatorio.get("rows", [])
    ]


async def _propriedade_ga4(api: GoogleApi, dominio: str | None) -> tuple[str, str]:
    resumos = await api.paginar(f"{GA_ADMIN_URL}/accountSummaries", "accountSummaries", {"pageSize": 200})
    propriedades = [p for conta in resumos for p in conta.get("propertySummaries", [])]
    if not propriedades:
        raise GoogleApiErro("sem_acesso", "A conta conectada não tem acesso a nenhuma propriedade do Google Analytics.")
    if dominio:
        for p in propriedades:
            streams = await api.get(f"{GA_ADMIN_URL}/{p['property']}/dataStreams")
            for s in streams.get("dataStreams", []):
                if dominio in (s.get("webStreamData", {}).get("defaultUri") or ""):
                    return p["property"], p.get("displayName", "")
    return propriedades[0]["property"], propriedades[0].get("displayName", "")


async def _analytics(api: GoogleApi, dominio: str | None, hoje: date) -> dict:
    propriedade, nome = await _propriedade_ga4(api, dominio)
    ontem = hoje - timedelta(days=1)
    ultimos_90 = {"startDate": _iso(ontem - timedelta(days=89)), "endDate": _iso(ontem)}
    ultimos_30 = {"startDate": _iso(ontem - timedelta(days=29)), "endDate": _iso(ontem)}

    async def relatorio(corpo: dict) -> list:
        return _linhas(await api.chamar("POST", f"{GA_DATA_URL}/{propriedade}:runReport", json=corpo))

    diario = await relatorio({
        "dateRanges": [ultimos_90], "dimensions": [{"name": "date"}],
        "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "keyEvents"}],
        "orderBys": [{"dimension": {"dimensionName": "date"}}], "limit": 400,
    })
    serie = [
        {"data": f"{d[0][:4]}-{d[0][4:6]}-{d[0][6:]}", "sessoes": int(m[0]), "usuarios": int(m[1]), "conversoes": int(m[2])}
        for d, m in diario
    ]
    paginas_brutas = await relatorio({
        "dateRanges": [ultimos_30], "dimensions": [{"name": "hostName"}, {"name": "pagePath"}],
        "metrics": [{"name": "screenPageViews"}, {"name": "sessions"}],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}], "limit": 200,
    })
    paginas = [
        {"host": d[0], "caminho": d[1], "secao": secao_da_pagina(d[0], d[1]),
         "visualizacoes": int(m[0]), "sessoes": int(m[1])}
        for d, m in paginas_brutas
    ]
    por_secao: dict[str, int] = {}
    for p in paginas:
        por_secao[p["secao"]] = por_secao.get(p["secao"], 0) + p["visualizacoes"]
    origens = await relatorio({
        "dateRanges": [ultimos_30], "dimensions": [{"name": "sessionSource"}, {"name": "sessionMedium"}],
        "metrics": [{"name": "sessions"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}], "limit": 50,
    })
    fontes_90 = await relatorio({
        "dateRanges": [ultimos_90], "dimensions": [{"name": "sessionSource"}],
        "metrics": [{"name": "sessions"}], "limit": 500,
    })
    contatos_brutos = await relatorio({
        "dateRanges": [ultimos_30], "dimensions": [{"name": "eventName"}, {"name": "pagePath"}],
        "metrics": [{"name": "eventCount"}],
        "dimensionFilter": {"filter": {"fieldName": "eventName",
                                       "inListFilter": {"values": list(EVENTOS_CONTATO)}}},
        "limit": 300,
    })
    por_tipo = dict.fromkeys(EVENTOS_CONTATO.values(), 0)
    por_pagina: dict[str, dict] = {}
    for d, m in contatos_brutos:
        tipo = EVENTOS_CONTATO.get(d[0])
        if tipo is None:
            continue
        por_tipo[tipo] += int(m[0])
        linha = por_pagina.setdefault(d[1], {"caminho": d[1], **dict.fromkeys(EVENTOS_CONTATO.values(), 0)})
        linha[tipo] += int(m[0])
    contatos = {
        "total_30d": sum(por_tipo.values()),
        "por_tipo": por_tipo,
        "por_pagina": sorted(por_pagina.values(), key=lambda l: -(l["whatsapp"] + l["ligacao"] + l["formulario"])),
    }
    # Quem chegou pelo LinkedIn (linkedin.com, app e encurtador lnkd.in) e quantos contatos (eventos principais) fez.
    vindos_linkedin = await relatorio({
        "dateRanges": [ultimos_90], "dimensions": [{"name": "landingPage"}, {"name": "sessionCampaignName"}],
        "metrics": [{"name": "sessions"}, {"name": "keyEvents"}],
        "dimensionFilter": {"orGroup": {"expressions": [
            {"filter": {"fieldName": "sessionSource", "stringFilter": {"matchType": "CONTAINS", "value": valor,
                                                                        "caseSensitive": False}}}
            for valor in ("linkedin", "lnkd.in")]}},
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}], "limit": 100,
    })
    linkedin = {
        "sessoes_90d": sum(int(m[0]) for _, m in vindos_linkedin),
        "contatos_90d": sum(int(m[1]) for _, m in vindos_linkedin),
        "por_pagina": [
            {"pagina": d[0], "campanha": None if d[1].startswith("(") else d[1], "sessoes": int(m[0]), "contatos": int(m[1])}
            for d, m in vindos_linkedin
        ],
    }
    ia = sorted(
        ({"fonte": d[0], "sessoes": int(m[0])} for d, m in fontes_90 if FONTES_IA.search(d[0])),
        key=lambda f: -f["sessoes"],
    )

    def total(campo: str, inicio: date, fim: date) -> int:
        return sum(p[campo] for p in serie if _iso(inicio) <= p["data"] <= _iso(fim))

    totais = {
        campo: total(campo, ontem - timedelta(days=29), ontem) for campo in ("sessoes", "usuarios", "conversoes")
    }
    anteriores = {
        campo: total(campo, ontem - timedelta(days=59), ontem - timedelta(days=30))
        for campo in ("sessoes", "usuarios", "conversoes")
    }
    return {
        "propriedade": propriedade,
        "nome": nome,
        "serie": serie,
        "totais_30d": totais,
        "totais_30d_anterior": anteriores,
        "paginas": paginas,
        "por_secao": por_secao,
        "origens": [{"origem": d[0], "meio": d[1], "sessoes": int(m[0])} for d, m in origens],
        "ia": {"total_90d": sum(f["sessoes"] for f in ia), "por_fonte": ia},
        "contatos": contatos,
        "linkedin": linkedin,
    }


# ---------------------------------------------------------------- Search Console


async def _site_search_console(api: GoogleApi, dominio: str | None) -> str:
    sites = [
        s["siteUrl"] for s in (await api.get(f"{GSC_URL}/sites")).get("siteEntry", [])
        if s.get("permissionLevel") != "siteUnverifiedUser"
    ]
    if not sites:
        raise GoogleApiErro("sem_acesso", "A conta conectada não tem nenhum site verificado no Search Console.")
    if dominio:
        if f"sc-domain:{dominio}" in sites:
            return f"sc-domain:{dominio}"
        for s in sites:
            if dominio in s:
                return s
    return sites[0]


async def _search_console(api: GoogleApi, dominio: str | None, hoje: date) -> dict:
    site = await _site_search_console(api, dominio)
    url = f"{GSC_URL}/sites/{quote(site, safe='')}/searchAnalytics/query"
    fim = hoje - timedelta(days=3)  # o Search Console tem uns 3 dias de atraso

    async def consulta(inicio: date, dimensoes: list[str], linhas: int = 1000) -> list[dict]:
        corpo = {"startDate": _iso(inicio), "endDate": _iso(fim), "dimensions": dimensoes, "rowLimit": linhas}
        return (await api.chamar("POST", url, json=corpo)).get("rows", [])

    def linha(r: dict, chave: str) -> dict:
        return {
            chave: r["keys"][0] if r.get("keys") else "",
            "cliques": int(r.get("clicks", 0)),
            "impressoes": int(r.get("impressions", 0)),
            "ctr": round(float(r.get("ctr", 0)) * 100, 2),
            "posicao": round(float(r.get("position", 0)), 1),
        }

    inicio_28 = fim - timedelta(days=27)
    serie = [
        {"data": r["keys"][0], "cliques": int(r.get("clicks", 0)), "impressoes": int(r.get("impressions", 0)),
         "posicao": round(float(r.get("position", 0)), 1)}
        for r in await consulta(fim - timedelta(days=89), ["date"])
    ]

    def totais(inicio: date, ate: date) -> dict:
        pontos = [p for p in serie if _iso(inicio) <= p["data"] <= _iso(ate)]
        impressoes = sum(p["impressoes"] for p in pontos)
        cliques = sum(p["cliques"] for p in pontos)
        posicao = sum(p["posicao"] * p["impressoes"] for p in pontos) / impressoes if impressoes else 0
        return {"cliques": cliques, "impressoes": impressoes,
                "ctr": round(cliques / impressoes * 100, 2) if impressoes else 0, "posicao": round(posicao, 1)}

    return {
        "site": site,
        "serie": serie,
        "totais_28d": totais(inicio_28, fim),
        "totais_28d_anterior": totais(inicio_28 - timedelta(days=28), inicio_28 - timedelta(days=1)),
        "consultas": [linha(r, "termo") for r in await consulta(inicio_28, ["query"], 250)],
        "paginas": [linha(r, "pagina") for r in await consulta(inicio_28, ["page"], 100)],
    }


# ---------------------------------------------------------------- Interface


async def coletar_painel(api: GoogleApi, conta: str, local: str, hoje: date | None = None) -> dict:
    hoje = hoje or date.today()
    painel: dict = {"coletado_em": datetime.now(timezone.utc).isoformat(), "conta": conta, "local": local, "erros": {}}

    async def secao(nome: str, coro) -> None:
        try:
            painel[nome] = await coro
        except GoogleApiErro as erro:
            painel[nome] = None
            painel["erros"][nome] = erro.como_dict()

    await secao("perfil", buscar_perfil(api, local))
    dominio = dominio_raiz((painel.get("perfil") or {}).get("site"))
    painel["dominio"] = dominio
    await secao("atributos", _atributos(api, local))
    await secao("desempenho", _desempenho(api, local, hoje))
    await secao("palavras_chave", _palavras_chave(api, local, hoje))
    await secao("avaliacoes", _avaliacoes(api, conta, local, hoje))
    await secao("posts", _posts(api, conta, local, hoje))
    await secao("midia", _midia(api, conta, local))
    await secao("verificacao", _verificacao(api, local))
    await secao("botoes", _botoes(api, local))
    await secao("analytics", _analytics(api, dominio, hoje))
    await secao("search_console", _search_console(api, dominio, hoje))
    return painel
