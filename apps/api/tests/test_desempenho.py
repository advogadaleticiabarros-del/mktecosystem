from datetime import date, datetime, timezone

import pytest

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
    assert list(secoes) == ["site", "busca", "perfil_google", "instagram", "linkedin", "tiktok", "blog"]

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
                         "instagram": "sem_dados", "linkedin": "sem_conexao", "tiktok": "sem_conexao", "blog": "ok"}


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
    assert len(r["secoes"]) == 7
    resposta = await client.get("/desempenho", headers={"Authorization": f"Bearer {create_access_token(user.id)}"})
    assert resposta.status_code == 200 and len(resposta.json()["secoes"]) == 7
