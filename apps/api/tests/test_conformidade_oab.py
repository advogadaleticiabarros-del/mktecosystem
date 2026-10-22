from app.services.conformidade_oab import bloqueia, verificar_texto_oab


def test_texto_limpo_passa():
    assert verificar_texto_oab("A lei prevê estabilidade para a gestante. Vamos avaliar seu caso.") == []


def test_promessa_e_captacao_bloqueiam():
    problemas = verificar_texto_oab("Garantimos sua vitória! Consulta grátis, ligue já.")
    assert bloqueia(problemas)
    assert {p["trecho"].lower() for p in problemas} >= {"garantimos", "grátis", "ligue já"}


def test_especialista_so_avisa():
    problemas = verificar_texto_oab("Advogada especialista em Direito do Trabalho")
    assert problemas and not bloqueia(problemas)


def test_sigilo_so_vale_para_resposta_de_avaliacao():
    texto = "Que bom que deu tudo certo no seu processo!"
    assert verificar_texto_oab(texto) == []
    assert bloqueia(verificar_texto_oab(texto, "resposta_avaliacao"))
