import importlib.util
import json
from pathlib import Path

import pytest

import fala

SERIE18 = Path(__file__).resolve().parents[1] / "series" / "18-limbo-previdenciario"


def carregar_v2():
    spec = importlib.util.spec_from_file_location("montar_falas_v2", SERIE18 / "montar_falas_v2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- cortes
def test_planejar_reproduz_os_pedacos_da_v2_da_serie_18():
    v2 = carregar_v2()
    for n, trechos in v2.FALAS.items():
        for t in trechos:
            fixo = len(t) > 2 and t[2] == "fixo"
            assert fala.planejar((t[0], t[1], "", "fixo") if fixo else (t[0], t[1], ""), v2.SILENCIOS) == v2.sem_pausas(*t), (n, t)


def test_planejar_encosta_a_ponta_que_cai_em_fala_na_pausa_real():
    # o Whisper marcou 10.1 e 14.0, já dentro da fala; as pausas reais estão logo antes (9.9) e logo depois (14.2)
    sil = [(9.5, 9.9), (14.2, 14.6)]
    assert fala.planejar((10.1, 14.0, "x"), sil) == [(9.81, 14.29)]


def test_planejar_encurta_pausa_interna_deixando_018s():
    sil = [(11.0, 12.0)]
    pedacos = fala.planejar((10.0, 13.0, "x"), sil)
    assert pedacos == [(10.0, 11.09), (11.91, 13.0)]
    pausa_que_sobra = (pedacos[0][1] - 11.0) + (12.0 - pedacos[1][0])
    assert pausa_que_sobra == pytest.approx(0.18)


def test_aparar_tira_o_silencio_curto_das_pontas_do_trecho():
    # silêncios curtos (< 0,25 s, não entram no planejamento) somados de dois trechos dariam pausa longa na emenda
    curtos = [(9.9, 10.12), (13.8, 14.0), (11.0, 11.1)]
    assert fala.aparar([(10.0, 11.5), (12.0, 13.9)], curtos) == [(10.03, 11.5), (12.0, 13.89)]


def test_aparar_nao_mexe_em_ponta_que_cai_em_fala():
    assert fala.aparar([(10.0, 13.9)], [(11.0, 11.2)]) == [(10.0, 13.9)]


def test_unir_pausas_que_se_sobrepoem():
    assert fala.unir([(103.79, 104.16), (5.0, 6.0), (103.78, 104.37)]) == [(5.0, 6.0), (103.78, 104.37)]


def test_retiradas_sao_os_miolos_das_pausas_e_a_borda_de_cada_ponta():
    assert fala.retiradas([(10.0, 11.09), (11.91, 13.0)]) == [(9.94, 10.0), (11.09, 11.91), (13.0, 13.06)]


def test_ler_silencios_do_log_do_ffmpeg():
    log = ("[silencedetect @ 0x1] silence_start: 0\n[silencedetect @ 0x1] silence_end: 1.011542 | silence_duration: 1.01\n"
           "lixo\n[silencedetect @ 0x1] silence_start: 3.867375\n[silencedetect @ 0x1] silence_end: 4.473854 | silence_duration: 0.6\n"
           "[silencedetect @ 0x1] silence_start: 9.5\n")
    assert fala.ler_silencios(log, fim=10.0) == [(0.0, 1.011542), (3.867375, 4.473854), (9.5, 10.0)]


def test_pausas_longas_ignora_as_pontas():
    sil = [(0.0, 0.4), (3.0, 3.2), (5.0, 5.5), (9.7, 10.0)]
    assert fala.pausas_longas(sil, dur=10.0) == [(5.0, 5.5)]


# --------------------------------------------------------------------------- texto
def test_comparar_aceita_diferenca_de_pontuacao_acento_e_grafia_do_whisper():
    assert fala.comparar("Limbo previdenciário é quando o empregado está inapto,", "limbo previdenciario é quando o empregado está inápito") == []


def test_comparar_acusa_palavra_comida():
    assert fala.comparar("e não tem nem dinheiro vindo da empresa", "e não tem nem dinheiro vindo da") == ["comida: 'empresa'"]


def test_comparar_acusa_repeticao_muleta_e_sobra():
    probs = fala.comparar("quem paga é a empresa", "quem quem paga né é a empresa mesmo")
    assert probs == ["repetição: 'quem'", "muleta: 'né'", "sobra: 'mesmo'"]


def test_comparar_tolera_artigo_trocado_pelo_whisper():
    assert fala.comparar("sai de lá com um atestado", "sai de lá com o atestado") == []


def test_comparar_acusa_palavra_trocada():
    assert fala.comparar("é a empresa", "é o trabalhador") == ["trocada: 'a empresa' -> 'o trabalhador'"]


def palavras(*pares):
    return [{"word": " " + w, "start": t, "end": t + 0.3} for w, t in pares]


def test_gaguejos_acusa_palavra_repetida_palavra_partida_e_hesitacao():
    # série 19 (27/10/2026): "fala ok" passava com gaguejo, porque o Whisper normal limpa a hesitação
    ws = palavras(("a", 1.0), ("pes-", 1.2), ("pessoa,", 1.5), ("ela", 2.0), ("ela", 2.3), ("vai", 2.6), ("hã,", 3.0), ("receber.", 3.4))
    assert fala.gaguejos(ws) == ["palavra partida: 'pes-' em 1.20s", "repetição: 'ela ela' em 2.00s", "hesitação: 'hã' em 3.00s"]


def test_gaguejos_acusa_grupo_de_palavras_repetido():
    # R1 da série 19 saiu com "Vai ser, vai ser acertado" e passou no "fala ok"
    ws = palavras(("Vai", 23.58), ("ser,", 23.66), ("vai", 24.08), ("ser", 24.56), ("acertado", 24.92))
    assert fala.gaguejos(ws) == ["repetição: 'Vai ser vai ser' em 23.58s"]


def test_gaguejos_acusa_palavra_curta_arrastada():
    # "que..." de 2,3 s no R1 da série 19: hesitação que o Whisper escreve como palavra comum
    ws = [{"word": " valor", "start": 30.9, "end": 31.2}, {"word": " que", "start": 31.24, "end": 33.56},
          {"word": " 13º", "start": 35.54, "end": 36.64}]
    assert fala.gaguejos(ws) == ["palavra arrastada: 'que' (2.32s) em 31.24s"]


def test_gaguejos_aceita_fala_limpa_e_repeticao_separada_por_pontuacao_de_frase():
    ws = palavras(("Já", 0.0), ("existe.", 0.3), ("Existe,", 0.8), ("sim.", 1.1), ("Trabalhei", 1.5), ("um", 2.0), ("mês.", 2.2))
    assert fala.gaguejos(ws) == []


# --------------------------------------------------------------------------- montagem de ponta a ponta (ffmpeg real, Whisper falso)
class OuvidoFalso:
    """Devolve o texto esperado na ordem em que os trechos são ouvidos."""

    def __init__(self, textos, completa=(), literal=None):
        self.textos, self.i = list(textos), 0
        self.completa = [{"word": " " + w, "start": t, "end": t + 0.3} for w, t in completa]
        self.literal = palavras(*literal) if literal is not None else self.completa

    def transcrever(self, wav, palavras=False, prompt=""):
        if palavras and fala.LITERAL in prompt:  # passada literal, só para achar gaguejo
            return {"text": "", "segments": [{"start": 0, "end": 1, "text": "", "words": self.literal}]}
        if palavras:  # transcrição da fala montada inteira (com contexto), também usada pela legenda do motor
            return {"text": " ".join(self.textos), "segments": [{"start": 0, "end": 1, "text": "", "words": self.completa}]}
        self.i += 1
        return {"text": self.textos[self.i - 1]}


def bruto_sintetico(pasta: Path, fim_mudo=False) -> Path:
    """6 s: tom de 0-2 s, silêncio 2-3 s, tom 3-6 s (ou 3-5 s e silêncio no fim, com `fim_mudo`)."""
    destino = pasta / "bruto.mp4"
    fala.ff("-f", "lavfi", "-i", "testsrc2=s=720x1280:r=30:d=6",
            "-f", "lavfi", "-i", f"aevalsrc='0.5*sin(2*PI*440*t)*(lt(t,2)+gte(t,3)*lt(t,{5 if fim_mudo else 7}))':d=6:s=48000",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", destino)
    return destino


def test_montar_tira_a_pausa_grava_emendas_e_confere_o_texto(tmp_path):
    src = bruto_sintetico(tmp_path)
    ouvido = OuvidoFalso(["um dois três"])
    destino = tmp_path / "fala-r1.mp4"
    problemas = fala.montar(src, [(0.0, 6.0, "um dois três")], destino, ouvido, vel=1.0)
    assert problemas == []
    dur = fala.duracao(destino)
    assert dur == pytest.approx(6.0 - (1.0 - 0.18), abs=0.07)  # a pausa de 1 s vira 0,18 s
    emendas = json.loads(destino.with_suffix(".emendas.json").read_text())
    assert len(emendas) == 1 and emendas[0] == pytest.approx(2.09, abs=0.04)
    assert destino.with_suffix(".wav").exists()
    assert json.loads(destino.with_suffix(".transcricao.json").read_text(encoding="utf-8"))["segments"]


def test_montar_recusa_acelerar_mais_de_5_por_cento(tmp_path):
    with pytest.raises(ValueError):
        fala.montar(tmp_path / "x.mp4", [(0, 1, "a")], tmp_path / "y.mp4", OuvidoFalso(["a"]), vel=1.08)


def test_montar_acusa_texto_divergente_com_o_numero_do_trecho(tmp_path):
    src = bruto_sintetico(tmp_path)
    ouvido = OuvidoFalso(["um dois", "quatro"], completa=[("um", 0.1), ("dois", 1.0), ("quatro", 3.5)])
    # o trecho 2 termina em 5,0 s, no meio do tom: o corte tira som audível, então a troca pode ser palavra comida
    problemas = fala.montar(src, [(0.0, 2.0, "um dois"), (3.0, 5.0, "três")], tmp_path / "f.mp4", ouvido, vel=1.0)
    assert problemas == ["trecho 2 (3.00-5.00): trocada: 'três' -> 'quatro'"]


def test_montar_rebaixa_a_nota_quando_nada_audivel_foi_cortado(tmp_path):
    src = bruto_sintetico(tmp_path, fim_mudo=True)
    ouvido = OuvidoFalso(["um dois", "quatro"], completa=[("um", 0.1), ("dois", 1.0), ("quatro", 3.5)])
    problemas = fala.montar(src, [(0.0, 2.0, "um dois"), (3.0, 6.0, "três")], tmp_path / "f.mp4", ouvido, vel=1.0)
    assert problemas == ["nota: trecho 2 (3.00-6.00): trocada: 'três' -> 'quatro' (nada audível foi cortado: provável engano do Whisper)"]


def test_montar_releva_trecho_curto_que_o_whisper_so_erra_sem_contexto(tmp_path):
    src = bruto_sintetico(tmp_path)
    ouvido = OuvidoFalso(["um dois", "e RAB"], completa=[("um", 0.1), ("dois", 1.0), ("Errado.", 3.5)])
    assert fala.montar(src, [(0.0, 2.0, "um dois"), (3.0, 6.0, "Errado.")], tmp_path / "f.mp4", ouvido, vel=1.0) == []


def test_montar_acusa_gaguejo_que_so_a_transcricao_literal_ouve(tmp_path):
    src = bruto_sintetico(tmp_path)
    ouvido = OuvidoFalso(["um dois três"], literal=[("um", 0.1), ("um", 0.4), ("dois", 1.0), ("três", 2.2)])
    problemas = fala.montar(src, [(0.0, 6.0, "um dois três")], tmp_path / "f.mp4", ouvido, vel=1.0)
    assert problemas == ["gaguejo na fala montada: repetição: 'um um' em 0.10s"]


def test_pausa_partida_por_estalo_entra_mas_consoante_dentro_da_palavra_nao():
    # a -40 dB a pausa aparece inteira; a -44 dB ela é quase toda silêncio (o estalo é curto e fraco)
    fracas = [(6.29, 6.64), (31.7, 32.1)]
    curtos = [(6.3, 6.4), (6.45, 6.63), (31.8, 31.89), (31.96, 32.08)]   # 31,7-32,1: o "t" de "atestado"
    assert fala.pausas_com_estalo(fracas, curtos) == [(6.29, 6.64)]


def test_imagem_converte_hdr_do_iphone_para_a_cor_dos_reels():
    # gravação HDR (HLG ou PQ) lida como SDR fica acinzentada (série 19, 26/10/2026): converte com tonemap
    for trc in ("arib-std-b67", "smpte2084"):
        f = fala.imagem(trc)
        assert "tonemap=tonemap=mobius" in f and "t=bt709" in f and f.endswith(fala.IMAGEM)


def test_imagem_de_fonte_comum_fica_como_estava():
    assert fala.imagem("bt709") == fala.IMAGEM
    assert fala.imagem("") == fala.IMAGEM


def test_transferencia_le_a_saida_do_ffprobe_com_virgula_sobrando(monkeypatch):
    # o ffprobe devolve "arib-std-b67," no .mov do iPhone; com a vírgula a conversão HDR não rodava (série 19/20, 27/10/2026)
    class R:
        stdout = "arib-std-b67,\n"
    monkeypatch.setattr(fala.subprocess, "run", lambda *a, **k: R())
    assert fala.transferencia("x.mov") == "arib-std-b67"
    assert "tonemap" in fala.imagem(fala.transferencia("x.mov"))
