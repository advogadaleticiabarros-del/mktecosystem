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


def test_audio_sai_no_alvo_sem_trilha(tmp_path):
    from pathlib import Path

    import conferir
    import fala
    m.AQUI = Path(__file__).resolve().parent
    voz = tmp_path / "fala-r1.mp4"
    fala.ff("-f", "lavfi", "-i", "color=c=black:s=320x568:r=30:d=5", "-f", "lavfi", "-i",
            "aevalsrc='0.3*sin(2*PI*220*t)*sin(2*PI*3*t)*lt(mod(t,1.2),0.9)':d=5:s=48000", "-c:v", "libx264", "-c:a", "aac", voz)
    efeitos = m.sfx(tmp_path / "sfx")
    assert all(3 <= len(v) <= 4 for v in efeitos.values())
    pasta = tmp_path / "audio"
    pasta.mkdir()
    mix = m.audio({"trechos": [(0.0, 5.0)], "src": voz}, pasta, [(0.0, "boom"), (1.0, "whoosh"), (2.5, "pop")], 5.5, efeitos)
    lufs, pico = conferir.ler_volume(conferir._stderr("-i", mix, "-af", "ebur128=peak=true", "-f", "null", "-"))
    assert abs(lufs - m.ALVO_LUFS) <= 0.5 and pico <= -1.0
    # a voz entra na mistura com o pico sempre no mesmo ponto (só ganho), e os efeitos ficam 8 a 12 dB abaixo dela
    _, pico_voz = conferir.ler_volume(conferir._stderr("-i", pasta / "voz.wav", "-af", "ebur128=peak=true", "-f", "null", "-"))
    assert abs(pico_voz - m.VOZ_PICO) <= 0.5
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


def test_normalizacao_nao_corta_mais_de_2_db_dos_picos(tmp_path):
    # escolha dela (21/10/2026): som intacto vale mais que volume. Gravação com pico forte (aqui, um boom) fica mais
    # baixa em vez de ter os picos esmagados; o limitador corta no máximo CORTE_MAX dB
    import conferir
    import fala
    bruto = tmp_path / "bruto.wav"
    fala.ff("-f", "lavfi", "-i", "aevalsrc='0.07*sin(2*PI*220*t)*sin(2*PI*3*t)+0.95*sin(2*PI*50*t)*exp(-6*t)':d=12:s=48000", "-ac", "2", bruto)
    teto = m._lufs(bruto) + (-1.5 - 0.5 - m._pico(bruto)) + m.CORTE_MAX
    assert teto < m.ALVO_LUFS                       # este sinal só chegaria a -14 esmagando o pico
    saida = tmp_path / "mix.wav"
    m._loudnorm(bruto, saida)
    lufs, pico = conferir.ler_volume(conferir._stderr("-i", saida, "-af", "ebur128=peak=true", "-f", "null", "-"))
    assert abs(lufs - teto) <= 0.4 and pico <= -1.4


def test_voz_da_dra_sai_como_foi_gravada(tmp_path):
    # 21/10/2026: a cadeia de tratamento (redução de ruído, equalização, realce, compressão, portão) "estragou o áudio";
    # pedido dela: não mexer na voz, manter o original. Só muda o volume: mesmo timbre e mesmo fundo nas pausas.
    import wave
    from pathlib import Path

    import numpy as np

    import fala
    m.AQUI = Path(__file__).resolve().parent
    voz = tmp_path / "fala-r1.mp4"
    fala.ff("-f", "lavfi", "-i", "color=c=black:s=320x568:r=30:d=8", "-f", "lavfi", "-i",
            "aevalsrc='0.2*(sin(2*PI*220*t)+0.5*sin(2*PI*2500*t)+0.3*sin(2*PI*6000*t))*sin(2*PI*3*t)*lt(mod(t,2),1)"
            "+0.02*(random(0)-0.5)':d=8:s=48000", "-c:v", "libx264", "-c:a", "aac", "-b:a", "256k", voz)
    pasta = tmp_path / "audio"
    pasta.mkdir()
    mix = m.audio({"trechos": [(0.0, 8.0)], "src": voz}, pasta, [], 8.0, m.sfx(tmp_path / "sfx"))

    def ler(arq):
        mono = tmp_path / f"{Path(arq).stem}_mono.wav"
        fala.ff("-i", arq, "-vn", "-ac", "1", "-ar", "48000", mono)
        with wave.open(str(mono)) as w:
            return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768

    def perfil(x):
        sr = 48000
        db = lambda t: 20 * np.log10(np.sqrt((t ** 2).mean()) + 1e-9)
        pausa, falando = x[int(1.3 * sr):int(1.8 * sr)], x[int(2.2 * sr):int(2.8 * sr)]
        P = np.abs(np.fft.rfft(falando)) ** 2
        f = np.fft.rfftfreq(len(falando), 1 / sr)
        return db(falando) - db(pausa), 10 * np.log10(P[f > 4000].sum() / P.sum())

    dist_src, agudos_src = perfil(ler(voz))
    dist_mix, agudos_mix = perfil(ler(mix))
    assert abs(dist_mix - dist_src) <= 2, (dist_src, dist_mix)       # sem portão nem redução de ruído
    assert abs(agudos_mix - agudos_src) <= 1, (agudos_src, agudos_mix)  # sem equalização nem realce
