import motor as m


def test_sorteio_de_efeitos_e_fixo_e_nao_repete_seguido():
    eventos = [(0.0, "boom"), (1.0, "whoosh"), (2.0, "pop"), (3.0, "whoosh"), (4.0, "whoosh"), (5.0, "whoosh"), (6.0, "pop")]
    a = m.sortear_efeitos(eventos, {"boom": 4, "whoosh": 4, "pop": 3}, semente=21)
    assert a == m.sortear_efeitos(eventos, {"boom": 4, "whoosh": 4, "pop": 3}, semente=21)
    assert [(t, tipo) for t, tipo, _ in a] == eventos
    whooshes = [k for _, tipo, k in a if tipo == "whoosh"]
    assert all(x != y for x, y in zip(whooshes, whooshes[1:]))
    assert all(0 <= k < 4 for k in whooshes)
    assert m.sortear_efeitos(eventos, {"boom": 4, "whoosh": 4, "pop": 3}, semente=22) != a


def test_punch_in_alterna_nas_emendas_e_entre_cenas_de_rosto():
    cenas = [{"a": 0.0, "bg": {"seq": "s0", "rosto": True}},
             {"a": 5.0, "bg": {"seq": "banco"}},
             {"a": 8.0, "bg": {"seq": "s2", "rosto": True}},
             {"a": 12.0, "outro": True}]
    m.punch_in(cenas, emendas=[2.0, 3.5, 4.95, 5.6, 8.05, 9.0], fator=1.12)
    assert cenas[0]["bg"]["zooms"] == [[0.0, 1.0], [2.0, 1.12], [3.5, 1.0]]   # 4,95 cai no fim da cena: o corte já cobre
    assert "zooms" not in cenas[1]["bg"]                                      # banco cobre a emenda de 5,6
    assert cenas[2]["bg"]["zooms"] == [[0.0, 1.12], [1.0, 1.0]]               # 8,05 colada no início: ignorada


def test_emendas_da_fala_viram_tempo_do_reel():
    linha = [{"ini_src": 0.0, "fim_src": 10.0, "ini": 0.0, "fim": 10.0}, {"ini_src": 20.0, "fim_src": 25.0, "ini": 10.0, "fim": 15.0}]
    assert m.emendas_no_reel([2.0, 15.0, 21.5], linha) == [2.0, 11.5]


def test_audio_sai_em_14_lufs_sem_trilha(tmp_path):
    from pathlib import Path

    import conferir
    import fala
    m.AQUI = Path(__file__).resolve().parent  # modelos/voz-sh.rnnn
    voz = tmp_path / "fala-r1.mp4"
    fala.ff("-f", "lavfi", "-i", "color=c=black:s=320x568:r=30:d=5", "-f", "lavfi", "-i",
            "aevalsrc='0.3*sin(2*PI*220*t)*sin(2*PI*3*t)*lt(mod(t,1.2),0.9)':d=5:s=48000", "-c:v", "libx264", "-c:a", "aac", voz)
    efeitos = m.sfx(tmp_path / "sfx")
    assert all(3 <= len(v) <= 4 for v in efeitos.values())
    pasta = tmp_path / "audio"
    pasta.mkdir()
    mix = m.audio({"trechos": [(0.0, 5.0)], "src": voz}, pasta, [(0.0, "boom"), (1.0, "whoosh"), (2.5, "pop")], 5.5, efeitos)
    lufs, pico = conferir.ler_volume(conferir._stderr("-i", mix, "-af", "ebur128=peak=true", "-f", "null", "-"))
    assert abs(lufs + 14) <= 0.5 and pico <= -1.0
    assert not (pasta / "trilha.wav").exists()


def test_codificar_entrega_entre_10_e_12_mbps_e_recusa_sobrescrever(tmp_path):
    import pytest

    import conferir
    import fala
    m.AQUI = tmp_path / "work"
    quadros = m.AQUI / "quadros_r1"
    quadros.mkdir(parents=True)
    # imagem quase parada (fundo liso + um elemento andando), como as cenas de motion graphics: em uma passada o
    # x264 entregava 4 Mbps aqui
    fala.ff("-f", "lavfi", "-i", "color=c=0x1a1511:s=1080x1920:r=30:d=4[a];testsrc2=s=360x360:r=30:d=4[b];"
            "[a][b]overlay=x='100+t*120':y=700", "-q:v", "3", quadros / "%05d.jpg")
    som = tmp_path / "som.wav"
    fala.ff("-f", "lavfi", "-i", "sine=f=330:d=4:sample_rate=48000", "-ac", "2", som)
    mp4 = m.codificar(1, quadros, 4.0, som, prefixo="teste-")
    info = conferir._formato(mp4)
    assert 10e6 * 0.97 <= info["vbr"] <= 12e6 * 1.03 and info["ar"] == 48000
    with pytest.raises(FileExistsError):
        m.codificar(1, quadros, 4.0, som, prefixo="teste-")


def test_fim_da_fala_nao_passa_do_fim_do_video(tmp_path):
    import json

    import fala
    src = tmp_path / "fala-r1.mp4"
    fala.ff("-f", "lavfi", "-i", "color=c=black:s=320x568:r=30:d=2", "-f", "lavfi", "-i", "sine=d=2", "-c:v", "libx264", "-c:a", "aac",
            "-shortest", src)
    trans = tmp_path / "t.json"
    trans.write_text(json.dumps({"segments": [{"words": [{"word": " fim", "start": 1.5, "end": 1.9}]}]}))
    assert abs(m.fim_da_fala(trans, src) - (fala.duracao(src) - 1 / 30)) < 0.01   # 1,9 + 0,25 passaria do vídeo
    trans.write_text(json.dumps({"segments": [{"words": [{"word": " fim", "start": 1.0, "end": 1.2}]}]}))
    assert m.fim_da_fala(trans, src) == 1.45


def test_normalizacao_chega_a_14_lufs_mesmo_com_pico_isolado(tmp_path):
    # caso do Reel 2 da validação: mix a -17,7 LUFS com um pico a -0,97 dBTP (o boom); o ajuste linear não podia subir
    import conferir
    import fala
    bruto = tmp_path / "bruto.wav"
    fala.ff("-f", "lavfi", "-i", "aevalsrc='0.07*sin(2*PI*220*t)*sin(2*PI*3*t)+0.95*sin(2*PI*50*t)*exp(-6*t)':d=12:s=48000", "-ac", "2", bruto)
    saida = tmp_path / "mix.wav"
    m._loudnorm(bruto, saida)
    lufs, pico = conferir.ler_volume(conferir._stderr("-i", saida, "-af", "ebur128=peak=true", "-f", "null", "-"))
    assert abs(lufs + 14) <= 0.5 and pico <= -1.4


def test_pausas_ficam_silenciosas_sem_chiado_de_fundo(tmp_path):
    # 21/10/2026: a ambiência (ruído marrom a -32 LUFS) virou chiado que abafava a voz da Dra.; nas pausas, o mix
    # tem de ficar tão quieto quanto a voz tratada
    import wave
    from pathlib import Path

    import numpy as np

    import fala
    m.AQUI = Path(__file__).resolve().parent
    voz = tmp_path / "fala-r1.mp4"
    fala.ff("-f", "lavfi", "-i", "color=c=black:s=320x568:r=30:d=8", "-f", "lavfi", "-i",
            "aevalsrc='0.3*sin(2*PI*220*t)*sin(2*PI*3*t)*lt(mod(t,2),1)':d=8:s=48000", "-c:v", "libx264", "-c:a", "aac", voz)
    pasta = tmp_path / "audio"
    pasta.mkdir()
    mix = m.audio({"trechos": [(0.0, 8.0)], "src": voz}, pasta, [], 8.0, m.sfx(tmp_path / "sfx"))
    mono = tmp_path / "mono.wav"
    fala.ff("-i", mix, "-ac", "1", mono)
    with wave.open(str(mono)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
        sr = w.getframerate()
    pausa = x[int(1.3 * sr):int(1.8 * sr)]   # meio da primeira pausa (a fala volta aos 2 s)
    assert 20 * np.log10(np.sqrt((pausa ** 2).mean()) + 1e-9) < -55
