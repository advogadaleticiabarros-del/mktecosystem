import base64
import json

import narrar as n


def alinhamento(texto, passo=0.1):
    return {"characters": list(texto),
            "character_start_times_seconds": [i * passo for i in range(len(texto))],
            "character_end_times_seconds": [(i + 1) * passo for i in range(len(texto))]}


class Resp:
    status_code = 200

    def __init__(self, texto):
        self.texto = texto

    def json(self):
        return {"audio_base64": base64.b64encode(b"mp3").decode(), "alignment": alinhamento(self.texto)}


def test_divide_roteiro_em_partes():
    partes = n.partes_do_roteiro("# Série\n## Parte 1\nOlá, tudo bem?\nSegunda linha.\n\n## Parte 2\nFim.\n")
    assert partes == [{"titulo": "Parte 1", "texto": "Olá, tudo bem? Segunda linha."}, {"titulo": "Parte 2", "texto": "Fim."}]


def test_checar_avisa_numero_e_termo_vetado():
    avisos = n.checar([{"titulo": "P1", "texto": "Sou especialista e o prazo é 30/11. " * 20}])
    assert any("extenso" in a for a in avisos)
    assert any("especialista" in a for a in avisos)


def test_palavras_no_formato_whisper_com_deslocamento():
    ws = n.palavras_do_alinhamento(alinhamento("Oi gente"), desloca=2.0)
    assert ws == [{"word": " Oi", "start": 2.0, "end": 2.2}, {"word": " gente", "start": 2.3, "end": 2.8}]


def test_config_em_json_ou_duas_linhas():
    assert n.ler_config('{"api_key": "sk_1", "voice_id": "v1"}') == {"api_key": "sk_1", "voice_id": "v1"}
    assert n.ler_config("sk_1\r\nv1\r\n") == {"api_key": "sk_1", "voice_id": "v1"}
    assert n.ler_config("sk_1") == {"api_key": "sk_1", "voice_id": None}


def test_narrar_junta_partes_com_pausa_e_usa_cache(tmp_path):
    chamadas = []

    def post(url, json, **kw):
        chamadas.append(json)
        return Resp(json["text"])

    partes = [{"titulo": "A", "texto": "Um dois"}, {"titulo": "B", "texto": "Três"}]
    um_segundo = lambda mp3: b"\x01\x00" * n.TAXA
    cfg = {"api_key": "k", "voice_id": "v"}
    pcm, tr, trechos = n.narrar(partes, cfg, post, tmp_path, um_segundo)

    assert chamadas[0]["next_text"] == "Três" and chamadas[1]["previous_text"] == "Um dois"
    assert trechos == [(0.0, 1.0), (1.6, 2.6)]
    assert tr["segments"][1]["words"][0] == {"word": " Três", "start": 1.6, "end": 2.0}
    assert len(pcm) == 2 * int((2 + 2 * n.PAUSA) * n.TAXA)

    n.narrar(partes, cfg, post, tmp_path, um_segundo)
    assert len(chamadas) == 2  # segunda vez veio do cache, sem cobrar de novo
