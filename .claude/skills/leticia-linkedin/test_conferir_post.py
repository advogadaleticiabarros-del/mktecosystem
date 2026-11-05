import json

from conferir_post import conferir, main


def sem_oab(_texto):
    return []


def motivos(avisos):
    return " | ".join(a["motivo"] for a in avisos)


def test_data_relativa_pede_conferencia_com_a_data_de_publicacao():
    # Erro real: post de 11/11 dizia "deste mês" sobre julgamento de 28/09/2026.
    avisos = conferir("Uma decisão do TST deste mês muda a conta do passivo.", oab=sem_oab)
    assert any(a["trecho"] == "deste mês" and a["nivel"] == "atencao" for a in avisos)
    assert any(a["trecho"] == "Em duas semanas" for a in conferir("Em duas semanas a regra muda.", oab=sem_oab))


def test_bloqueio_da_oab_vem_do_verificador_recebido():
    def oab(_texto):
        return [{"trecho": "grátis", "motivo": "captação", "nivel": "bloqueia"}]

    assert {"trecho": "grátis", "motivo": "captação", "nivel": "bloqueia"} in conferir("Consulta grátis.", oab=oab)


def test_experiencia_em_primeira_pessoa_pede_confirmacao_da_dra():
    avisos = conferir("Os erros que mais vejo nas contas de 13º. Cinco dúvidas que chegam toda semana ao RH.", oab=sem_oab)
    assert {a["trecho"] for a in avisos if "Dra." in a["motivo"]} == {"mais vejo", "chegam toda semana"}


def test_regras_fixas_de_escrita_bloqueiam():
    avisos = conferir("Trabalhador com deficiência — regra nova. Me chama no direct.", oab=sem_oab)
    bloqueados = {a["trecho"].lower() for a in avisos if a["nivel"] == "bloqueia"}
    assert bloqueados == {"deficiência", "—", "me chama"}


def test_ex_empregado_passa_mas_ex_marido_nao():
    assert conferir("O ex-empregado recebeu as verbas.\n\n" + "x" * 600, oab=sem_oab) == []
    assert any(a["trecho"] == "ex-marido" for a in conferir("O ex-marido pagou.", oab=sem_oab))


def test_formula_de_ia_e_reversao_avisam():
    texto = "A verdade é que a Justiça olha para a realidade, não para o nome do contrato."
    trechos = {a["trecho"] for a in conferir(texto, oab=sem_oab)}
    assert {"A verdade é", ", não para"} <= trechos


def test_tamanho_gancho_hashtags_e_negrito():
    gancho_longo = "g" * 150
    texto = gancho_longo + "\n\n" + "c" * 1200 + " **forte**\n\n#Um #Dois #Tres #Quatro"
    m = motivos(conferir(texto, oab=sem_oab))
    assert "1.300" in m and "gancho" in m.lower() and "hashtags" in m and "negrito" in m


def test_post_curto_avisa_e_acima_do_limite_bloqueia():
    assert "600" in motivos(conferir("Curto.", oab=sem_oab))
    assert any(a["nivel"] == "bloqueia" and "3.000" in a["motivo"] for a in conferir("x" * 3001, oab=sem_oab))


def test_linha_de_comando_confere_a_faixa_de_datas_do_arquivo_de_fila(tmp_path, capsys):
    fila = tmp_path / "fila.json"
    fila.write_text(json.dumps([
        {"data": "2026-11-10", "tema": "Excluido", "link": None, "texto": "Consulta grátis."},
        {"data": "2026-11-11", "tema": "Incluido", "link": None, "texto": "Uma decisão deste mês."},
    ]), encoding="utf-8")
    assert main([str(fila), "--de", "2026-11-11", "--ate", "2026-11-11"]) == 0
    saida = capsys.readouterr().out
    assert "Incluido" in saida and "deste mês" in saida and "Excluido" not in saida


def test_linha_de_comando_devolve_1_quando_algo_bloqueia(tmp_path, capsys):
    post = tmp_path / "post.txt"
    post.write_text("Consulta grátis, me chama.", encoding="utf-8")
    assert main([str(post)]) == 1
    assert "BLOQUEIA" in capsys.readouterr().out
