from app.services.blog_slug import gerar_slug


def test_remove_acentos_e_usa_minusculas():
    assert gerar_slug("Carga Horária Máxima CLT") == "carga-horaria-maxima-clt"


def test_troca_pontuacao_por_hifen():
    assert gerar_slug("Pedi demissão, grávida: posso reverter?") == "pedi-demissao-gravida-posso-reverter"


def test_colapsa_espacos_e_hifens_duplicados():
    assert gerar_slug("Racismo   no  trabalho -- como provar") == "racismo-no-trabalho-como-provar"


def test_remove_hifen_nas_bordas():
    assert gerar_slug("  -BPC/LOAS em 2026- ") == "bpc-loas-em-2026"
