from app.services.teste_reels import julgar

REFERENCIA = [75, 57, 183, 82, 333, 367, 1017, 355, 517, 211]  # Reels do perfil em 27/10/2026: mediana 272


def test_teste_que_alcanca_70_por_cento_da_mediana_libera_o_post_dos_seguidores():
    v = julgar({"views": 191, "shares": 0, "saved": 0}, REFERENCIA)
    assert v.liberado and "meta 190" in v.motivo


def test_teste_fraco_segura_o_post_e_diz_por_que():
    v = julgar({"views": 120, "shares": 1, "saved": 0}, REFERENCIA)
    assert not v.liberado
    assert "120 visualizações" in v.motivo and "meta 190" in v.motivo


def test_compartilhamentos_e_salvamentos_liberam_mesmo_com_poucas_visualizacoes():
    assert julgar({"views": 90, "shares": 2, "saved": 1}, REFERENCIA).liberado


def test_sem_reels_de_referencia_libera():
    assert julgar({"views": 10}, []).liberado
