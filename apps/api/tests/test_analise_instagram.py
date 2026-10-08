from datetime import date, datetime, timezone

from app.services.analise_instagram import analisar, classificar_area

HOJE = date(2026, 10, 8)


def _post(media_id, quando, formato="Imagem", alcance=100, interacoes=10, compartilhamentos=0,
          salvamentos=0, seguidores_ganhos=None, area="Trabalhista", legenda="legenda"):
    return {
        "media_id": media_id,
        "publicado_em": quando,
        "formato": formato,
        "area": area,
        "legenda": legenda,
        "permalink": f"https://instagram.com/p/{media_id}",
        "alcance": alcance,
        "visualizacoes": alcance * 2,
        "curtidas": interacoes,
        "comentarios": 0,
        "compartilhamentos": compartilhamentos,
        "salvamentos": salvamentos,
        "interacoes": interacoes,
        "seguidores_ganhos": seguidores_ganhos,
        "visitas_perfil": None,
    }


def _utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


RAIO_X = {
    "perfil": {"followers_count": 416, "follows_count": 442, "media_count": 6},
    "totais_30d": {"reach": 1256, "accounts_engaged": 89, "saves": 0, "shares": 20, "website_clicks": 3, "profile_views": 88},
    "serie_alcance": [["2026-10-06", 50], ["2026-10-07", 145], ["2026-10-08", 34]],
    "serie_seguidores": [["2026-10-06", 1], ["2026-10-07", 0], ["2026-10-08", 2]],
    "demografia": {
        "genero": {"F": 300, "M": 71, "U": 38},
        "idade": {"18-24": 27, "25-34": 202, "35-44": 110},
        "cidades": {"Vitória, Espírito Santo": 159, "Serra, Espírito Santo": 43, "Maringá, Paraná": 34},
    },
}

POSTS = [
    _post("r1", _utc(2026, 5, 28, 23, 0), "Reels", alcance=900, interacoes=50, compartilhamentos=5),  # 20h Brasília
    _post("r2", _utc(2026, 6, 2, 23, 0), "Reels", alcance=300, interacoes=30),
    _post("c1", _utc(2026, 8, 10, 15, 0), "Carrossel", alcance=100, interacoes=9, seguidores_ganhos=3),  # 12h
    _post("i1", _utc(2026, 8, 10, 12, 0), "Imagem", alcance=60, interacoes=5),  # 9h
    _post("i2", _utc(2026, 8, 11, 12, 0), "Imagem", alcance=80, interacoes=6, area="Família"),
    _post("i3", _utc(2026, 8, 12, 12, 0), "Imagem", alcance=40, interacoes=4),
]


def test_formatos_ordenados_pelo_alcance_tipico_com_explicacao_comparando_ao_mais_usado():
    r = analisar(POSTS, RAIO_X, HOJE)
    itens = r["formatos"]["itens"]
    assert [i["formato"] for i in itens] == ["Reels", "Carrossel", "Imagem"]
    assert itens[0]["alcance_tipico"] == 600  # mediana de 900 e 300
    assert itens[2]["posts"] == 3
    assert "Reels" in r["formatos"]["explicacao"]
    assert "10,0 vezes" in r["formatos"]["explicacao"]  # 600 / 60 (Imagem, o mais usado)


def test_horario_e_dia_usam_o_horario_de_brasilia():
    r = analisar(POSTS, RAIO_X, HOJE)
    horas = {i["hora"]: i for i in r["horarios"]["itens"]}
    assert horas[20]["posts"] == 2
    assert horas[9]["posts"] == 3
    assert 23 not in horas


def test_ranking_por_alcance_e_por_seguidores():
    r = analisar(POSTS, RAIO_X, HOJE)
    assert [p["media_id"] for p in r["ranking"]["alcance"]][:2] == ["r1", "r2"]
    assert [p["media_id"] for p in r["ranking"]["seguidores"]] == ["c1"]


def test_volume_mensal_conta_posts_e_alcance_medio():
    r = analisar(POSTS, RAIO_X, HOJE)
    meses = {i["mes"]: i for i in r["volume_mensal"]["itens"]}
    assert meses["2026-08"]["posts"] == 4
    assert meses["2026-08"]["alcance_medio"] == 70


def test_resumo_traz_numeros_da_conta():
    r = analisar(POSTS, RAIO_X, HOJE)
    kpis = {k["chave"]: k for k in r["resumo"]["kpis"]}
    assert kpis["seguidores"]["valor"] == 416
    assert kpis["novos_seguidores_30d"]["valor"] == 3
    assert kpis["alcance_30d"]["valor"] == 1256
    assert kpis["salvamentos_30d"]["valor"] == 0
    assert all(k["explicacao"] for k in r["resumo"]["kpis"])


def test_alcance_diario_aponta_o_pico():
    r = analisar(POSTS, RAIO_X, HOJE)
    assert r["alcance_diario"]["pico"] == {"data": "2026-10-07", "valor": 145}
    assert len(r["alcance_diario"]["serie"]) == 3


def test_publico_em_percentual_e_cidades_ordenadas():
    r = analisar(POSTS, RAIO_X, HOJE)
    genero = {g["rotulo"]: g for g in r["publico"]["genero"]}
    assert genero["Mulheres"]["pct"] == 73
    assert r["publico"]["cidades"][0]["rotulo"] == "Vitória"
    assert "73%" in r["publico"]["explicacao"]


def test_recomendacoes_pegam_salvamentos_zerados_e_formato_subusado():
    r = analisar(POSTS, RAIO_X, HOJE)
    texto = " ".join(r["recomendacoes"])
    assert "salv" in texto.lower()
    assert "Reels" in texto


def test_sem_dados_nao_quebra():
    r = analisar([], {}, HOJE)
    assert r["formatos"]["itens"] == []
    assert r["formatos"]["explicacao"]
    assert r["ranking"]["alcance"] == []


def test_classificar_area_pelo_texto_da_legenda():
    assert classificar_area("Fui demitida grávida, e agora?") == "Trabalhista"
    assert classificar_area("Revisão de pensão alimentícia") == "Família"
    assert classificar_area("Como pedir o BPC no INSS") == "Previdenciário"
    assert classificar_area("Caí no golpe do Pix") == "Consumidor"
    assert classificar_area("Sextou!") == "Institucional"
