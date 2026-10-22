from app.services.conformidade_oab import bloqueia, verificar_texto_oab


def test_texto_limpo_passa():
    assert verificar_texto_oab("A lei prevê estabilidade para a gestante. Vamos avaliar seu caso.") == []


def test_promessa_e_captacao_bloqueiam():
    problemas = verificar_texto_oab("Garantimos sua vitória! Consulta grátis, ligue já.")
    assert bloqueia(problemas)
    assert {p["trecho"].lower() for p in problemas} >= {"garantimos", "grátis", "ligue já"}


def test_informacao_juridica_nao_e_promessa_nem_oferta():
    assert verificar_texto_oab("Voltou da licença? Veja o que a lei garante à mãe que volta ao trabalho.") == []
    assert verificar_texto_oab("A 2ª parcela do 13º sai até 18 de dezembro e traz todos os descontos.") == []
    assert verificar_texto_oab("Para quem quer garantir os direitos trabalhistas.") == []


def test_oferta_comercial_bloqueia():
    for texto in ["Consulta com 20% de desconto", "Parcelamos em até 10x", "Honorários a partir de R$ 300",
                  "Garantia de êxito na ação"]:
        assert bloqueia(verificar_texto_oab(texto)), texto


def test_especialista_so_avisa():
    problemas = verificar_texto_oab("Advogada especialista em Direito do Trabalho")
    assert problemas and not bloqueia(problemas)


def test_sigilo_so_vale_para_resposta_de_avaliacao():
    texto = "Que bom que deu tudo certo no seu processo!"
    assert verificar_texto_oab(texto) == []
    assert bloqueia(verificar_texto_oab(texto, "resposta_avaliacao"))
