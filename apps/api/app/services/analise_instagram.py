"""Análise do Instagram: transforma posts + retrato da conta em gráficos explicados.

Interface:
- `analisar(posts, raio_x, hoje) -> dict` — função pura. `posts` são dicts no
  formato de `InstagramPost` (ver `post_para_dict`); `raio_x` é o retrato da
  conta coletado por `coleta_instagram`. Devolve uma seção por gráfico, cada uma
  com os dados e uma `explicacao` em português simples, mais `recomendacoes`.
- `montar_analise(db, tenant_id)` — carrega do banco e chama `analisar`.
- `classificar_area(legenda)` — área jurídica de um post pelo texto.

"Típico" = mediana (um viral não distorce a comparação).
"""
import re
import uuid
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from statistics import median

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.instagram_post import InstagramPost
from app.models.social_metric import SocialMetric

BRASILIA = timezone(timedelta(hours=-3))
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
TOP = 10

_AREAS = [
    ("Previdenciário", r"\binss\b|aposentad|\bbpc\b|\bloas\b|auxílio|previd|pensão por morte|benefício"),
    ("Família", r"pensão|divórc|guarda|\bfilh|alimentos|casamento|união estável|herança|inventário|famíl|abandono|\bpai\b|\bmãe\b|genitor"),
    ("Consumidor", r"consumid|golpe|\bpix\b|cobrança|serasa|nome sujo|empréstimo|consignado|\bbanco"),
    ("Trabalhista", r"demiss|demitid|trabalh|\bclt\b|justa causa|rescis|fgts|empreg|patr[ãa]o|chefe|assédio|insalubr|hora extra|carteira|salári|férias|gestante|grávida|atestado|aviso prévio|6x1|empresa"),
]


def classificar_area(legenda: str | None) -> str:
    """Área com mais palavras-chave na legenda; empate fica com a que vem antes em `_AREAS`."""
    texto = (legenda or "").lower()
    pontos = [(len(re.findall(padrao, texto)), -i, area) for i, (area, padrao) in enumerate(_AREAS)]
    melhor = max(pontos)
    return melhor[2] if melhor[0] else "Institucional"


def _num(v) -> int:
    return int(v or 0)


def _fmt(n: float) -> str:
    return f"{n:,.0f}".replace(",", ".")


def _vezes(a: float, b: float) -> str:
    return f"{a / b:.1f}".replace(".", ",") + " vezes"


def _local(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(BRASILIA)


def _agrupar(posts, chave):
    grupos = defaultdict(list)
    for p in posts:
        grupos[chave(p)].append(p)
    return grupos


def _resumo_post(p) -> dict:
    return {
        "media_id": p["media_id"],
        "data": _local(p["publicado_em"]).date().isoformat(),
        "formato": p["formato"],
        "area": p["area"],
        "legenda": (p.get("legenda") or "").strip()[:140],
        "permalink": p.get("permalink"),
        "alcance": _num(p["alcance"]),
        "interacoes": _num(p["interacoes"]),
        "compartilhamentos": _num(p["compartilhamentos"]),
        "salvamentos": _num(p["salvamentos"]),
        "seguidores_ganhos": _num(p.get("seguidores_ganhos")),
    }


def _resumo(raio_x: dict) -> dict:
    perfil = raio_x.get("perfil", {})
    totais = raio_x.get("totais_30d", {})
    novos = sum(v for _, v in raio_x.get("serie_seguidores", []))
    seguidores, seguindo = _num(perfil.get("followers_count")), _num(perfil.get("follows_count"))
    alcance, engajadas = _num(totais.get("reach")), _num(totais.get("accounts_engaged"))
    kpis = [
        {"chave": "seguidores", "rotulo": "Seguidores", "valor": seguidores,
         "explicacao": f"Pessoas que seguem o perfil hoje. O perfil segue {_fmt(seguindo)} contas."},
        {"chave": "novos_seguidores_30d", "rotulo": "Novos seguidores (30 dias)", "valor": novos,
         "explicacao": "Quantas pessoas começaram a seguir nos últimos 30 dias."},
        {"chave": "alcance_30d", "rotulo": "Contas alcançadas (30 dias)", "valor": alcance,
         "explicacao": "Pessoas diferentes que viram algum conteúdo do perfil no período."},
        {"chave": "contas_engajadas_30d", "rotulo": "Contas que interagiram (30 dias)", "valor": engajadas,
         "explicacao": "Pessoas que curtiram, comentaram, salvaram ou compartilharam algo."
                       + (f" São {round(engajadas / alcance * 100)}% de quem viu." if alcance else "")},
        {"chave": "salvamentos_30d", "rotulo": "Salvamentos (30 dias)", "valor": _num(totais.get("saves")),
         "explicacao": "Quando alguém salva um post para ver depois. É o sinal mais forte de conteúdo útil para o Instagram."},
        {"chave": "compartilhamentos_30d", "rotulo": "Compartilhamentos (30 dias)", "valor": _num(totais.get("shares")),
         "explicacao": "Envios de posts para outras pessoas. É o que leva o perfil a quem ainda não segue."},
        {"chave": "visitas_perfil_30d", "rotulo": "Visitas ao perfil (30 dias)", "valor": _num(totais.get("profile_views")),
         "explicacao": "Pessoas que abriram o perfil depois de ver um post."},
        {"chave": "cliques_site_30d", "rotulo": "Cliques no site (30 dias)", "valor": _num(totais.get("website_clicks")),
         "explicacao": "Toques no link do site na bio."},
    ]
    if not perfil:
        texto = "Ainda não há dados da conta. Clique em Atualizar dados para buscar no Instagram."
    else:
        texto = (
            f"O perfil tem {_fmt(seguidores)} seguidores e ganhou {novos} nos últimos 30 dias. "
            f"Nesse período, {_fmt(alcance)} contas viram algum conteúdo e {_fmt(engajadas)} interagiram."
        )
    return {"kpis": kpis, "texto": texto}


def _alcance_diario(raio_x: dict) -> dict:
    serie = [{"data": d, "valor": _num(v)} for d, v in raio_x.get("serie_alcance", [])]
    if not serie:
        return {"serie": [], "media": 0, "pico": None, "explicacao": "Sem dados de alcance diário ainda."}
    media = round(sum(p["valor"] for p in serie) / len(serie))
    pico = max(serie, key=lambda p: p["valor"])
    data_pico = date.fromisoformat(pico["data"]).strftime("%d/%m")
    return {
        "serie": serie,
        "media": media,
        "pico": {"data": pico["data"], "valor": pico["valor"]},
        "explicacao": (
            f"Contas alcançadas por dia nos últimos {len(serie)} dias. A média é de {_fmt(media)} contas por dia, "
            f"e o melhor dia foi {data_pico}, com {_fmt(pico['valor'])}. Dias sem post costumam cair, "
            "por isso o ritmo constante importa mais que picos de volume."
        ),
    }


def _janela(posts, hoje: date):
    """Último ano quando há posts suficientes; senão, tudo."""
    corte = hoje - timedelta(days=365)
    recentes = [p for p in posts if _local(p["publicado_em"]).date() >= corte]
    return (recentes, "nos últimos 12 meses") if len(recentes) >= 10 else (posts, "desde o início do perfil")


def _formatos(posts, hoje: date) -> dict:
    base, periodo = _janela(posts, hoje)
    if not base:
        return {"itens": [], "explicacao": "Sem publicações para comparar ainda."}
    itens = []
    for formato, grupo in _agrupar(base, lambda p: p["formato"]).items():
        itens.append({
            "formato": formato,
            "posts": len(grupo),
            "alcance_tipico": round(median(_num(p["alcance"]) for p in grupo)),
            "interacoes_tipicas": round(median(_num(p["interacoes"]) for p in grupo)),
            "compartilhamentos": sum(_num(p["compartilhamentos"]) for p in grupo),
            "salvamentos": sum(_num(p["salvamentos"]) for p in grupo),
            "seguidores_ganhos": sum(_num(p.get("seguidores_ganhos")) for p in grupo),
        })
    itens.sort(key=lambda i: -i["alcance_tipico"])
    melhor = itens[0]
    mais_usado = max(itens, key=lambda i: i["posts"])
    explicacao = (
        f"Comparação {periodo}, pelo alcance típico de cada post. "
        f"{melhor['formato']} é o formato que mais alcança: {_fmt(melhor['alcance_tipico'])} contas por post."
    )
    if mais_usado is not melhor and mais_usado["alcance_tipico"]:
        explicacao += (
            f" Isso é {_vezes(melhor['alcance_tipico'], mais_usado['alcance_tipico'])} o de "
            f"{mais_usado['formato']}, que é o formato mais publicado ({mais_usado['posts']} posts)."
        )
    return {"itens": itens, "periodo": periodo, "explicacao": explicacao}


def _areas(posts, hoje: date) -> dict:
    base, periodo = _janela(posts, hoje)
    itens = [
        {"area": area, "posts": len(g), "alcance_tipico": round(median(_num(p["alcance"]) for p in g))}
        for area, g in _agrupar(base, lambda p: p["area"]).items()
    ]
    itens.sort(key=lambda i: -i["posts"])
    if not itens:
        return {"itens": [], "explicacao": "Sem publicações para comparar ainda."}
    principal = itens[0]
    melhor = max(itens, key=lambda i: i["alcance_tipico"])
    explicacao = (
        f"Áreas identificadas pelo texto da legenda, {periodo}. {principal['area']} concentra "
        f"{round(principal['posts'] / len(base) * 100)}% dos posts."
    )
    if melhor is not principal:
        explicacao += f" Quem alcança mais por post é {melhor['area']} ({_fmt(melhor['alcance_tipico'])} contas)."
    explicacao += " \"Institucional\" reúne bastidores, datas e posts pessoais."
    return {"itens": itens, "periodo": periodo, "explicacao": explicacao}


def _horarios(posts, hoje: date) -> dict:
    base, periodo = _janela(posts, hoje)
    itens = [
        {"hora": h, "posts": len(g), "alcance_tipico": round(median(_num(p["alcance"]) for p in g))}
        for h, g in _agrupar(base, lambda p: _local(p["publicado_em"]).hour).items()
    ]
    itens.sort(key=lambda i: i["hora"])
    confiaveis = [i for i in itens if i["posts"] >= 3] or itens
    if not confiaveis:
        return {"itens": [], "explicacao": "Sem publicações para comparar ainda."}
    melhor = max(confiaveis, key=lambda i: i["alcance_tipico"])
    return {
        "itens": itens,
        "explicacao": (
            f"Alcance típico pela hora em que o post saiu (horário de Brasília), {periodo}. "
            f"Entre os horários com pelo menos 3 posts, o melhor é {melhor['hora']}h "
            f"({_fmt(melhor['alcance_tipico'])} contas). Horários com poucos posts ainda são palpite: "
            "o Orbit vai testando e ajustando."
        ),
    }


def _dias_semana(posts, hoje: date) -> dict:
    base, periodo = _janela(posts, hoje)
    itens = [
        {"dia": DIAS[d], "indice": d, "posts": len(g), "alcance_tipico": round(median(_num(p["alcance"]) for p in g))}
        for d, g in _agrupar(base, lambda p: _local(p["publicado_em"]).weekday()).items()
    ]
    itens.sort(key=lambda i: i["indice"])
    if not itens:
        return {"itens": [], "explicacao": "Sem publicações para comparar ainda."}
    melhor = max(itens, key=lambda i: i["alcance_tipico"])
    pior = min(itens, key=lambda i: i["alcance_tipico"])
    return {
        "itens": itens,
        "explicacao": (
            f"Alcance típico pelo dia da semana, {periodo}. O melhor dia é {melhor['dia']} "
            f"({_fmt(melhor['alcance_tipico'])} contas) e o mais fraco é {pior['dia']} "
            f"({_fmt(pior['alcance_tipico'])})."
        ),
    }


def _volume_mensal(posts) -> dict:
    itens = []
    for mes, g in sorted(_agrupar(posts, lambda p: _local(p["publicado_em"]).strftime("%Y-%m")).items()):
        ano, m = mes.split("-")
        itens.append({
            "mes": mes,
            "rotulo": f"{MESES[int(m) - 1]}/{ano[2:]}",
            "posts": len(g),
            "alcance_medio": round(sum(_num(p["alcance"]) for p in g) / len(g)),
        })
    if not itens:
        return {"itens": [], "explicacao": "Sem publicações ainda."}
    mais_posts = max(itens, key=lambda i: i["posts"])
    melhor = max(itens, key=lambda i: i["alcance_medio"])
    explicacao = (
        f"Quantos posts saíram por mês e quanto cada post alcançou, em média. "
        f"O mês com mais posts foi {mais_posts['rotulo']} ({mais_posts['posts']}), "
        f"com {_fmt(mais_posts['alcance_medio'])} contas por post."
    )
    if melhor is not mais_posts:
        explicacao += (
            f" O melhor alcance por post foi em {melhor['rotulo']} ({_fmt(melhor['alcance_medio'])}). "
            "Mais posts não significa mais alcance: ritmo e formato pesam mais."
        )
    return {"itens": itens, "explicacao": explicacao}


def _ranking(posts) -> dict:
    def top(campo, minimo=1):
        escolhidos = [p for p in posts if _num(p.get(campo)) >= minimo]
        escolhidos.sort(key=lambda p: -_num(p.get(campo)))
        return [_resumo_post(p) for p in escolhidos[:TOP]]

    return {
        "alcance": top("alcance"),
        "interacoes": top("interacoes"),
        "compartilhamentos": top("compartilhamentos"),
        "seguidores": top("seguidores_ganhos"),
        "explicacao": (
            "Os 10 posts que mais se destacaram em cada critério. Alcance mostra o que chegou a mais gente; "
            "interações, o que mais gerou conversa; compartilhamentos, o que as pessoas mandaram para outras; "
            "seguidores, o que fez gente nova seguir o perfil (o Instagram só informa isso para posts de imagem e carrossel)."
        ),
    }


def _publico(raio_x: dict) -> dict:
    demo = raio_x.get("demografia", {})

    def em_lista(dados: dict, rotulos=None, limite=None):
        total = sum(dados.values()) or 1
        itens = [
            {"rotulo": (rotulos or {}).get(k, k.split(",")[0]), "valor": v, "pct": round(v / total * 100)}
            for k, v in dados.items()
        ]
        return itens

    genero = em_lista(demo.get("genero", {}), {"F": "Mulheres", "M": "Homens", "U": "Não informado"})
    genero.sort(key=lambda i: -i["valor"])
    idade = em_lista(demo.get("idade", {}))
    idade.sort(key=lambda i: i["rotulo"])
    cidades_dict = demo.get("cidades", {})
    cidades = em_lista(cidades_dict)
    cidades.sort(key=lambda i: -i["valor"])
    total_cidades = sum(cidades_dict.values())
    es = sum(v for k, v in cidades_dict.items() if "Espírito Santo" in k)

    if not genero:
        return {"genero": [], "idade": [], "cidades": [], "explicacao": "O Instagram ainda não liberou os dados de público."}
    mulheres = next((g["pct"] for g in genero if g["rotulo"] == "Mulheres"), 0)
    faixa = max(idade, key=lambda i: i["valor"]) if idade else None
    explicacao = f"{mulheres}% de quem segue são mulheres"
    if faixa:
        explicacao += f", e a faixa principal é de {faixa['rotulo']} anos ({faixa['pct']}%)"
    explicacao += "."
    if total_cidades:
        explicacao += f" {round(es / total_cidades * 100)}% estão no Espírito Santo."
    return {"genero": genero, "idade": idade, "cidades": cidades[:8], "explicacao": explicacao}


def _recomendacoes(formatos: dict, raio_x: dict) -> list[str]:
    recs = []
    itens = formatos.get("itens", [])
    if itens:
        melhor = itens[0]
        total = sum(i["posts"] for i in itens)
        if melhor["posts"] / total < 0.4:
            recs.append(
                f"{melhor['formato']} é o formato que mais alcança, mas foi só {round(melhor['posts'] / total * 100)}% "
                f"dos posts. Vale aumentar a frequência de {melhor['formato']}."
            )
    totais = raio_x.get("totais_30d", {})
    if totais and _num(totais.get("saves")) == 0:
        recs.append(
            "Nenhum post foi salvo nos últimos 30 dias. Carrosséis com passo a passo e o pedido "
            "\"salve para consultar depois\" no último slide ajudam a mudar isso."
        )
    perfil = raio_x.get("perfil", {})
    if perfil and _num(perfil.get("follows_count")) > _num(perfil.get("followers_count")):
        recs.append("O perfil segue mais contas do que é seguido. Uma limpeza nas contas seguidas melhora a percepção de autoridade.")
    if totais and _num(totais.get("website_clicks")) < 10:
        recs.append("Poucos cliques no site. Citar o artigo do blog na legenda e no story do dia leva mais gente ao site.")
    return recs


def analisar(posts: list[dict], raio_x: dict, hoje: date) -> dict:
    formatos = _formatos(posts, hoje)
    return {
        "resumo": _resumo(raio_x),
        "alcance_diario": _alcance_diario(raio_x),
        "formatos": formatos,
        "areas": _areas(posts, hoje),
        "horarios": _horarios(posts, hoje),
        "dias_semana": _dias_semana(posts, hoje),
        "volume_mensal": _volume_mensal(posts),
        "ranking": _ranking(posts),
        "publico": _publico(raio_x),
        "recomendacoes": _recomendacoes(formatos, raio_x),
        "total_posts": len(posts),
    }


def post_para_dict(p: InstagramPost) -> dict:
    return {
        "media_id": p.media_id,
        "publicado_em": p.publicado_em,
        "formato": p.formato,
        "area": p.area,
        "legenda": p.legenda,
        "permalink": p.permalink,
        "alcance": p.alcance,
        "visualizacoes": p.visualizacoes,
        "curtidas": p.curtidas,
        "comentarios": p.comentarios,
        "compartilhamentos": p.compartilhamentos,
        "salvamentos": p.salvamentos,
        "interacoes": p.interacoes,
        "seguidores_ganhos": p.seguidores_ganhos,
        "visitas_perfil": p.visitas_perfil,
    }


async def montar_analise(db: AsyncSession, tenant_id: uuid.UUID, hoje: date | None = None) -> dict:
    posts = (
        await db.execute(select(InstagramPost).where(InstagramPost.tenant_id == tenant_id))
    ).scalars().all()
    ultimo = (
        await db.execute(
            select(SocialMetric)
            .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == "ig_raio_x")
            .order_by(SocialMetric.coletado_em.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    analise = analisar(
        [post_para_dict(p) for p in posts],
        ultimo.metricas if ultimo else {},
        hoje or datetime.now(BRASILIA).date(),
    )
    analise["atualizado_em"] = ultimo.coletado_em.isoformat() if ultimo else None
    return analise
