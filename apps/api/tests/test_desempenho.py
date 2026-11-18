from datetime import date, datetime, timezone

import pytest

from app.models.instagram_post import InstagramPost
from app.services.desempenho import consolidar, montar_desempenho

HOJE = date(2026, 10, 23)

PAINEL = {
    "analytics": {
        "totais_30d": {"sessoes": 300, "usuarios": 220, "conversoes": 9},
        "totais_30d_anterior": {"sessoes": 200, "usuarios": 150, "conversoes": 4},
        "paginas": [{"caminho": "/blog/x.html", "secao": "blog", "visualizacoes": 80, "sessoes": 60},
                    {"caminho": "/", "secao": "site", "visualizacoes": 50, "sessoes": 40},
                    {"caminho": "/blog/", "secao": "blog", "visualizacoes": 30, "sessoes": 20}],
        "origens": [{"origem": "google", "meio": "organic", "sessoes": 150}],
        "ia": {"total_90d": 7},
        "contatos": {"total_30d": 6, "por_tipo": {"whatsapp": 4, "ligacao": 1, "formulario": 1},
                     "por_pagina": [{"caminho": "/blog/x.html", "whatsapp": 3, "ligacao": 0, "formulario": 1}]},
        "linkedin": {"sessoes_90d": 12, "contatos_90d": 2, "por_pagina": [{"pagina": "/lp/e.html", "campanha": "x", "sessoes": 12, "contatos": 2}]},
    },
    "search_console": {"totais_28d": {"cliques": 40, "impressoes": 2000, "ctr": 2.0, "posicao": 12.3},
                       "totais_28d_anterior": {"cliques": 20, "impressoes": 1500, "ctr": 1.3, "posicao": 15.0},
                       "consultas": [{"termo": "estabilidade gestante", "cliques": 5, "impressoes": 90, "ctr": 5.5, "posicao": 7.4}]},
    "desempenho": {"totais_30d": {"buscas": 500, "maps": 100, "ligacoes": 6, "rotas": 3, "cliques_site": 20, "conversas": 0},
                   "totais_30d_anterior": {"buscas": 400, "maps": 50, "ligacoes": 2, "rotas": 1, "cliques_site": 10, "conversas": 0}},
    "avaliacoes": {"media": 5.0, "total": 31, "sem_resposta": 2},
}


def _fontes(**extra):
    base = {
        "painel_google": PAINEL, "painel_coletado_em": "2026-10-23T09:00:00+00:00",
        "analise_instagram": {"resumo": {"texto": "O perfil tem 2.000 seguidores.", "kpis": [
            {"chave": "seguidores", "valor": 2000}, {"chave": "novos_seguidores_30d", "valor": 40},
            {"chave": "alcance_30d", "valor": 9000}]}},
        "instagram_recentes": [{"data": "2026-10-20", "formato": "reels", "legenda": "Gestante", "alcance": 900,
                                "interacoes": 50, "salvamentos": 10, "compartilhamentos": 7, "permalink": "https://ig/p"}],
        "instagram_publicados_30d": 18, "instagram_agendados_7d": 5,
        "linkedin_conexao": {"dias_para_vencer": 5},
        "linkedin_posts": [
            {"status": "publicado", "publicar_em": datetime(2026, 10, 20, 11, tzinfo=timezone.utc), "texto": "A", "erro": None},
            {"status": "aprovado", "publicar_em": datetime(2026, 10, 27, 11, tzinfo=timezone.utc), "texto": "B\nresto", "erro": None},
            {"status": "aprovado", "publicar_em": datetime(2026, 10, 28, 11, tzinfo=timezone.utc), "texto": "C",
             "erro": "Aguardando o artigo ir ao ar"},
        ],
        "tiktok": {"conectado": False, "no_rascunho": [], "ultimos": []},
        "blog_publicados_30d": ["Artigo 1"], "blog_proximos": [(date(2026, 11, 9), "13º da gestante")],
    }
    return {**base, **extra}


def test_cada_canal_vira_uma_secao_com_numeros_e_comparacao():
    r = consolidar(_fontes(), HOJE)
    secoes = {s["chave"]: s for s in r["secoes"]}
    assert list(secoes) == ["site", "busca", "perfil_google", "instagram", "reels_teste", "linkedin", "tiktok", "blog"]

    site = secoes["site"]
    assert site["kpis"][0] == {"rotulo": "Visitas (30 dias)", "valor": 300, "anterior": 200, "formato": "numero",
                               "explicacao": "Sessões no site, blog e páginas."}
    assert "+50% sobre o mês anterior" in site["resumo"] and "6 contatos" in site["resumo"]

    assert secoes["busca"]["kpis"][3]["formato"] == "posicao" and secoes["busca"]["kpis"][3]["valor"] == 12.3
    perfil = {k["rotulo"]: k for k in secoes["perfil_google"]["kpis"]}
    assert perfil["Visualizações (30 dias)"]["valor"] == 600 and perfil["Visualizações (30 dias)"]["anterior"] == 450

    ig = {k["rotulo"]: k["valor"] for k in secoes["instagram"]["kpis"]}
    assert ig["Seguidores"] == 2000 and ig["Publicações (30 dias)"] == 18
    assert secoes["instagram"]["listas"][0]["links"] == ["https://ig/p"]

    li = secoes["linkedin"]
    assert {k["rotulo"]: k["valor"] for k in li["kpis"]}["Posts agendados"] == 2
    assert "o próximo sai em 27/10" in li["resumo"]
    assert li["listas"][0]["linhas"][0] == ["27/10", "B"]
    assert li["listas"][-1]["titulo"] == "Posts com aviso"

    blog = secoes["blog"]
    assert blog["listas"][0]["linhas"] == [["/blog/x.html", 80]]  # o índice do blog não entra como artigo


def test_avisos_juntam_o_que_precisa_de_atencao():
    avisos = [a["texto"] for a in consolidar(_fontes(), HOJE)["avisos"]]
    assert "2 avaliação(ões) do Google sem resposta." in avisos
    assert any("LinkedIn vence em 5" in a for a in avisos)
    assert any("TikTok não conectado" in a for a in avisos)


def test_sem_dados_nao_quebra():
    r = consolidar({"tiktok": {}}, HOJE)
    situacoes = {s["chave"]: s["situacao"] for s in r["secoes"]}
    assert situacoes == {"site": "sem_dados", "busca": "sem_dados", "perfil_google": "sem_dados",
                         "instagram": "sem_dados", "reels_teste": "sem_dados", "linkedin": "sem_conexao", "tiktok": "sem_conexao",
                         "blog": "ok"}


@pytest.mark.anyio
async def test_montar_com_banco_vazio_e_rota(client, db_session):
    from app.core.security import create_access_token, hash_password
    from app.models.tenant import Tenant
    from app.models.user import User

    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    user = User(tenant_id=tenant.id, email="l@example.com", nome="L", hashed_password=hash_password("s"), role="owner")
    db_session.add(user)
    await db_session.commit()

    r = await montar_desempenho(db_session, tenant.id, HOJE)
    assert len(r["secoes"]) == 8
    resposta = await client.get("/desempenho", headers={"Authorization": f"Bearer {create_access_token(user.id)}"})
    assert resposta.status_code == 200 and len(resposta.json()["secoes"]) == 8


# --------------------------------------------------------------------------- Reels de teste (17/11/2026)
AGORA = datetime(2026, 11, 18, 15, 0, tzinfo=timezone.utc)
REF = [75, 57, 183, 82, 333, 367, 1017, 355, 517, 211]  # mediana 272 -> meta 190


def _teste(**extra):
    base = {"titulo": "Teste · intermitente", "agendado": "17/11 09:30", "status": "publicado",
            "publicado_em": datetime(2026, 11, 17, 12, 30, tzinfo=timezone.utc), "permalink": "https://ig/r",
            "views": 640, "alcance": 500, "shares": 4, "saved": 2, "curtidas": 30, "tempo_medio_ms": 9000}
    return {**base, **extra}


def _secao_testes(testes, referencia=REF):
    r = consolidar(_fontes(reels_teste=testes, reels_teste_referencia=referencia, agora=AGORA), HOJE)
    return next(s for s in r["secoes"] if s["chave"] == "reels_teste")


def test_reels_de_teste_mostra_numeros_e_veredito_de_cada_teste():
    s = _secao_testes([_teste(), _teste(titulo="Teste · fraco", views=80, shares=0, saved=0, permalink=None)])
    assert s["situacao"] == "ok" and "190" in s["resumo"]
    lista = s["listas"][0]
    assert lista["colunas"][:3] == ["Reels", "Publicado", "Visualizações"]
    bom, fraco = lista["linhas"]
    assert bom[1] == "17/11 09:30"  # 12:30 UTC no horário de Brasília
    assert bom[2] == 640 and bom[-1].startswith("Vai bem")
    assert fraco[-1].startswith("Abaixo da meta")
    assert lista["links"] == ["https://ig/r", None]
    kpis = {k["rotulo"]: k["valor"] for k in s["kpis"]}
    assert kpis["Melhor teste (visualizações)"] == 640 and kpis["Envios + salvamentos"] == 6


def test_reels_de_teste_agendado_recente_e_zerado_tem_situacao_propria():
    s = _secao_testes([
        _teste(status="pronto", publicado_em=None, views=None),
        _teste(publicado_em=datetime(2026, 11, 18, 9, 0, tzinfo=timezone.utc), views=None),
        _teste(publicado_em=datetime(2026, 11, 18, 9, 0, tzinfo=timezone.utc), views=20),
        _teste(views=0, shares=0, saved=0),
    ])
    agendado, sem_coleta, recente, zerado = (l[-1] for l in s["listas"][0]["linhas"])
    assert agendado == "Agendado para 17/11 09:30"
    assert sem_coleta.startswith("Aguardando a coleta")
    assert recente.startswith("Menos de 24 h")
    assert "confira no app" in zerado


def test_sem_reels_de_teste_a_secao_avisa():
    s = _secao_testes([])
    assert s["situacao"] == "sem_dados" and s["listas"] == []


async def test_montar_le_os_testes_e_tira_os_testes_da_referencia(db_session):
    from datetime import date as d
    from app.models.content_piece import ContentPiece
    from app.models.pauta import Pauta
    from app.models.scheduled_post import ScheduledPost
    from app.models.tenant import Tenant
    from app.services.teste_reels import views_referencia

    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.flush()
    quando = datetime(2026, 11, 17, 12, 30, tzinfo=timezone.utc)
    db_session.add_all([
        InstagramPost(tenant_id=tenant.id, media_id="trial1", publicado_em=quando, formato="Reels", area="x",
                      permalink="https://ig/t", visualizacoes=700, alcance=600, compartilhamentos=3, salvamentos=1),
        InstagramPost(tenant_id=tenant.id, media_id="feed1", publicado_em=quando, formato="Reels", area="x", visualizacoes=100),
        InstagramPost(tenant_id=tenant.id, media_id="feed2", publicado_em=quando, formato="Reels", area="x", visualizacoes=300),
    ])
    db_session.add_all([
        ScheduledPost(tenant_id=tenant.id, titulo="Teste · A", canal="instagram", formato="trial", data_agendada=d(2026, 11, 17),
                      horario="09:30", status="publicado", platform_post_id="trial1"),
        ScheduledPost(tenant_id=tenant.id, titulo="Teste · B", canal="instagram", formato="trial", data_agendada=d(2026, 11, 17),
                      horario="11:30", status="pronto"),
        ScheduledPost(tenant_id=tenant.id, titulo="Feed", canal="instagram", formato="reels", data_agendada=d(2026, 11, 17),
                      horario="19:00", status="publicado", platform_post_id="feed1"),
    ])
    await db_session.commit()

    assert sorted(await views_referencia(db_session, tenant.id)) == [100, 300]
    r = await montar_desempenho(db_session, tenant.id, d(2026, 11, 18))
    s = next(x for x in r["secoes"] if x["chave"] == "reels_teste")
    linhas = {l[0]: l for l in s["listas"][0]["linhas"]}
    assert linhas["Teste · A"][2] == 700 and linhas["Teste · B"][-1] == "Agendado para 17/11 11:30"
    assert "140" in s["resumo"]  # 70% da mediana 200 dos Reels do feed
