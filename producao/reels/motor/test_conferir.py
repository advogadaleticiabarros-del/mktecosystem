import conferir as c
import fala

LOG_FREEZE = """[freezedetect @ 0x1] lavfi.freezedetect.freeze_start: 33.6
[freezedetect @ 0x1] lavfi.freezedetect.freeze_duration: 1.2
[freezedetect @ 0x1] lavfi.freezedetect.freeze_end: 34.8
[freezedetect @ 0x1] lavfi.freezedetect.freeze_start: 44.1
[freezedetect @ 0x1] lavfi.freezedetect.freeze_duration: 2.3
[freezedetect @ 0x1] lavfi.freezedetect.freeze_end: 46.4
[freezedetect @ 0x1] lavfi.freezedetect.freeze_start: 47.0
"""

LOG_EBUR = """[Parsed_ebur128_0 @ 0x1] t: 10.0  TARGET:-23 LUFS    M: -13.0 S: -14.1     I: -14.5 LUFS
[Parsed_ebur128_0 @ 0x1] Summary:

  Integrated loudness:
    I:         -14.2 LUFS
    Threshold: -24.4 LUFS

  Loudness range:
    LRA:         4.1 LU

  True peak:
    Peak:       -0.4 dBFS
"""


def test_congelamentos_ignoram_o_fechamento():
    assert c.ler_congelamentos(LOG_FREEZE, ate=42.7, fim=48.0) == [(33.6, 34.8)]


def test_congelamento_aberto_fecha_no_fim():
    assert c.ler_congelamentos(LOG_FREEZE, ate=99, fim=48.0)[-1] == (47.0, 48.0)


def test_volume_do_resumo_do_ebur128():
    assert c.ler_volume(LOG_EBUR) == (-14.2, -0.4)


def test_avisos_de_volume():
    assert c.avisos_volume(-14.2, -1.3) == []
    assert c.avisos_volume(-15.6, -1.3) == ["volume: -15.6 LUFS (alvo -14 ±1)"]
    assert c.avisos_volume(-14.0, -0.4) == ["pico: -0.4 dBTP (máximo -1)"]


def test_avisos_de_formato():
    ok = {"w": 1080, "h": 1920, "fps": 30.0, "vbr": 11_000_000, "acodec": "aac", "ar": 48000, "abr": 128_000}
    assert c.avisos_formato(ok) == []
    ruim = {**ok, "w": 720, "vbr": 6_000_000, "ar": 44100}
    assert c.avisos_formato(ruim) == ["resolução 720x1920 (alvo 1080x1920)", "vídeo a 6.0 Mbps (alvo 10 a 12)",
                                      "áudio aac 44100 Hz 128 kbps (alvo AAC 48000 Hz 128 kbps)"]


def test_cena_de_video_mais_longa_que_o_clipe():
    cfg = {"total": 20.0, "cenas": [
        {"a": 0.0, "bg": {"seq": "seq/r1_rosto0", "n": 125, "vel": 1.0}},          # 4,0 s precisam de 120 quadros: ok
        {"a": 4.0, "bg": {"seq": "seq/r1_stk1_contas", "n": 240, "vel": 1.0}},     # 11,9 s precisam de 357: congela
        {"a": 15.9, "bg": {"seq": "seq/r1_rosto2", "n": 60, "vel": 1.0}},          # até o fechamento: 2,1 s = 63 > 60
        {"a": 18.0, "outro": True, "els": []}]}
    assert c.cenas_longas(cfg) == ["cena 1 (seq/r1_stk1_contas): 11.9s sobre um clipe de 8.0s (congela aos 12.0s)",
                                   "cena 2 (seq/r1_rosto2): 2.1s sobre um clipe de 2.0s (congela aos 17.9s)"]


def test_conferir_de_ponta_a_ponta(tmp_path):
    mp4 = tmp_path / "x.mp4"
    fala.ff("-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30:d=6", "-f", "lavfi", "-i", "sine=f=440:d=6:sample_rate=48000",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", mp4)
    resumo, avisos = c.conferir(mp4)
    assert "6.0s" in resumo[0] and "1080x1920" in resumo[0]
    assert any(a.startswith("vídeo a") for a in avisos)          # o teste foi codificado com taxa baixa
    assert mp4.with_name("x_folha.jpg").exists()
