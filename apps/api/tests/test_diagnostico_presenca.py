from datetime import date

from app.services.diagnostico_presenca import diagnosticar, palavra_suspeita

HOJE = date(2026, 10, 22)


def _painel(**mudancas) -> dict:
    painel = {
        "dominio": "advogadaleticiabarros.com.br",
        "erros": {},
        "perfil": {
            "titulo": "Letícia Barros | Advocacia", "cidade": "Vitória",
            "descricao": "Advocacia trabalhista em Vitória. " + "x" * 500,
            "site": "https://advogadaleticiabarros.com.br/?utm_source=google",
            "servicos": [{"nome": "Rescisão indireta", "descricao": "Quando a empresa descumpre."}],
            "link_avaliar": "https://review",
        },
        "avaliacoes": {"media": 4.9, "total": 20, "sem_resposta": 0, "ultimos_30d": 2, "lista": []},
        "posts": {"ultimo_em": "2026-10-20T10:00:00Z", "total": 5},
        "midia": {"fotos": 30, "ultima_em": "2026-10-01T00:00:00Z"},
        "botoes": [{"tipo": "APPOINTMENT"}],
        "desempenho": {"totais_30d": {"buscas": 100, "maps": 50}, "totais_30d_anterior": {"buscas": 100, "maps": 50}},
        "palavras_chave": [{"termo": "advogada gestante"}],
        "search_console": {"consultas": [], "paginas": []},
        "analytics": {"ia": {"total_90d": 3}},
        "site": {"paginas_sem_analytics": [], "paginas_sem_descricao": [], "robos_ia_bloqueados": [],
                 "llms_txt": True, "home": {"schemas": ["LegalService"]}},
    }
    painel.update(mudancas)
    return painel


def _chaves(painel) -> list[str]:
    return [r["chave"] for r in diagnosticar(painel, HOJE)]


def test_perfil_em_dia_nao_gera_recomendacao():
    assert _chaves(_painel()) == []


def test_problemas_do_perfil_real():
    perfil = {
        "titulo": "Letícia Barros | Advocacia", "cidade": "Vitória",
        "descricao": "Advogada Especialista em Direito do Trabalho. Todo Brasil",
        "site": "https://contato.advogadaleticiabarros.com.br/",
        "servicos": [
            {"nome": "Advogado trabalhista", "descricao": "assedíio moral e verbas"},
            {"nome": "RescÏsão indireta", "descricao": "x"},
            {"nome": "Advogada Penal", "descricao": ""},
        ],
    }
    recs = {r["chave"]: r for r in diagnosticar(_painel(perfil=perfil), HOJE)}
    assert recs["perfil-site-utm"]["itens"] == [
        "https://advogadaleticiabarros.com.br/?utm_source=google&utm_medium=organic&utm_campaign=perfil-empresa"]
    assert recs["perfil-descricao-oab"]["prioridade"] == "media"
    assert "perfil-descricao-cidade" in recs and "perfil-descricao-curta" in recs
    assert recs["perfil-servicos-digitacao"]["itens"] == ["RescÏsão", "assedíio"]
    assert recs["perfil-servicos-sem-descricao"]["itens"] == ["Advogada Penal"]


def test_avaliacoes_posts_fotos_e_ordem_por_prioridade():
    recs = diagnosticar(_painel(
        avaliacoes={"media": 4.2, "total": 10, "sem_resposta": 3, "ultimos_30d": 0, "lista": []},
        posts={"ultimo_em": "2026-09-01T00:00:00Z"},
        midia={"fotos": 4, "ultima_em": "2026-05-01T00:00:00Z"},
        botoes=[],
    ), HOJE)
    chaves = [r["chave"] for r in recs]
    assert chaves[0] == "avaliacoes-sem-resposta"
    assert {"avaliacoes-ritmo", "avaliacoes-media", "posts-frequencia", "fotos-poucas", "fotos-recentes",
            "botoes-agendar"} <= set(chaves)
    assert next(r for r in recs if r["chave"] == "avaliacoes-ritmo")["link"] == "https://review"


def test_busca_quase_no_topo_ctr_baixo_queda_e_marca():
    recs = {r["chave"]: r for r in diagnosticar(_painel(
        desempenho={"totais_30d": {"buscas": 40, "maps": 10}, "totais_30d_anterior": {"buscas": 80, "maps": 20}},
        palavras_chave=[{"termo": "leticia barros"}, {"termo": "barros advocacia"}, {"termo": "advogada gestante"}],
        search_console={
            "consultas": [{"termo": "estabilidade gestante", "posicao": 7.4, "impressoes": 90},
                          {"termo": "x", "posicao": 2.0, "impressoes": 500}],
            "paginas": [{"pagina": "https://a/blog", "impressoes": 300, "ctr": 0.5}],
        },
    ), HOJE)}
    assert recs["desempenho-queda"]["prioridade"] == "alta"
    assert recs["palavras-so-marca"]["itens"] == ["advogada gestante"]
    assert recs["gsc-quase-primeira-pagina"]["itens"] == ["estabilidade gestante: posição 7.4, 90 aparições"]
    assert "gsc-ctr-baixo" in recs


def test_site_ia_e_configuracao():
    chaves = _chaves(_painel(
        erros={"avaliacoes": {"tipo": "api_desativada", "ativar_em": "https://console"},
               "analytics": {"tipo": "reconectar"}},
        analytics={"ia": {"total_90d": 0}},
        site={"paginas_sem_analytics": ["lp/guia.html"], "paginas_sem_descricao": [], "robos_ia_bloqueados": ["GPTBot"],
              "llms_txt": False, "home": {"schemas": []}},
    ))
    assert chaves[:2] == ["config-ativar-avaliacoes", "config-reconectar"]
    assert {"site-sem-analytics", "site-robos-ia", "site-llms-txt", "site-schema", "ia-sem-visitas"} <= set(chaves)


def test_palavra_suspeita():
    assert palavra_suspeita("RescÏsão") and palavra_suspeita("assedíio")
    assert not palavra_suspeita("rescisão") and not palavra_suspeita("previdenciária") and not palavra_suspeita("saúde")
