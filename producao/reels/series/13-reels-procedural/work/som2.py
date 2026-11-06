"""Efeitos sonoros v2 (06/11/2026, pedido da Jessica: "só melhore o efeito sonoro").
Troca só os efeitos dos Reels do 13º: mesmos momentos, mesma voz e trilha, vídeo copiado do Reels publicado.
Uso: py som2.py serie 2 | py som2.py serie 3 | py som2.py serie2 4 | py som2.py serie2 6
Saída: renders_som2/<nome>-som2.mp4 (o vídeo antigo fica intacto)."""
import importlib
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
SR = 48000
RNG = np.random.default_rng(13)
NOMES = {("serie", 2): "13-sem-susto-reel-2", ("serie", 3): "13-sem-susto-reel-3",
         ("serie2", 4): "13-proporcional-calculo", ("serie2", 6): "13-quatro-regras"}
# nível final de cada efeito (antes era: whoosh .22, boom .55, pop .26, carimbo .45, brilho .30, po .5)
NIVEL = {"whoosh": .20, "boom": .42, "pop": .16, "carimbo": .30, "brilho": .18, "po": .16}
VOLS_MOTOR = {"whoosh": 0.22, "boom": 0.55, "pop": 0.26, "carimbo": 0.45, "brilho": 0.30, "po": 0.5}


def t(d):
    return np.arange(int(d * SR)) / SR


def passa_baixa(x, fc):
    """Filtro de 1 polo com corte variável (fc escalar ou vetor)."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y, v = np.empty_like(x), 0.0
    for i in range(len(x)):
        v = (1 - a[i]) * x[i] + a[i] * v
        y[i] = v
    return y


def reverb(x, dur=.7, mix=.22):
    ir = RNG.standard_normal(int(dur * SR)) * np.exp(-t(dur) * 7)
    ir = passa_baixa(ir, 5000)
    ir /= np.abs(ir).sum() ** .5 * 6
    molhado = np.convolve(x, ir)[:len(x) + len(ir)]
    seco = np.pad(x, (0, len(molhado) - len(x)))
    return seco * (1 - mix) + molhado * mix


def estereo(x, pan=None):
    """pan de -1 (esq.) a 1 (dir.), escalar ou vetor."""
    pan = np.zeros_like(x) if pan is None else np.broadcast_to(pan, x.shape)
    ang = (pan + 1) * np.pi / 4
    return np.stack([x * np.cos(ang), x * np.sin(ang)], axis=1)


def whoosh():
    d = .6; tt = t(d)
    ruido = np.cumsum(RNG.standard_normal(len(tt))) ; ruido -= passa_baixa(ruido, 40)  # ruído marrom sem DC
    ruido /= np.abs(ruido).max()
    env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2.2
    fc = 250 + 3200 * np.sin(np.pi * tt / d) ** 3
    x = passa_baixa(passa_baixa(ruido, fc), fc) * env
    x -= passa_baixa(x, 180)
    y = reverb(x, .4, .15)
    return estereo(y, np.clip(np.linspace(-.6, .6 * len(y) / len(tt), len(y)), -.6, .6))  # passa da esquerda para a direita


def boom():
    d = 1.6; tt = t(d)
    f = 48 + 70 * np.exp(-14 * tt)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-2.6 * tt)
    golpe = passa_baixa(RNG.standard_normal(len(tt)) * np.exp(-60 * tt), 1800)
    x = sub + .5 * golpe
    return estereo(reverb(x, 1.2, .28))


def pop():
    d = .12; tt = t(d)
    x = (np.sin(2 * np.pi * 1900 * tt) + .6 * np.sin(2 * np.pi * 2870 * tt)) * np.exp(-70 * tt)
    x += .25 * passa_baixa(RNG.standard_normal(len(tt)), 4000) * np.exp(-200 * tt)
    return estereo(reverb(x, .3, .18))


def carimbo():
    d = .45; tt = t(d)
    corpo = np.sin(2 * np.pi * np.cumsum(140 * (1 + .6 * np.exp(-40 * tt))) / SR) * np.exp(-18 * tt)
    papel = passa_baixa(RNG.standard_normal(len(tt)), 2600) * np.exp(-45 * tt)
    papel -= passa_baixa(papel, 400)
    return estereo(reverb(corpo + .7 * papel, .35, .14))


def brilho():
    d = 2.2; tt = t(d)
    x = np.zeros_like(tt)
    for f0, atraso in ((1318.5, 0), (1975.5, .09)):  # Mi6 e Si6, sino suave
        tl = np.clip(tt - atraso, 0, None); on = tt >= atraso
        for k, (r, a, dec) in enumerate(((1, 1, 2.4), (2.76, .35, 4.5), (5.4, .12, 8))):
            x += on * a * np.sin(2 * np.pi * f0 * r * tl) * np.exp(-dec * tl) * (1 - np.exp(-tl * 400))
    return estereo(reverb(x, 1.4, .35))


def po():
    d = 1.4; tt = t(d)
    x = np.zeros(len(tt))
    for _ in range(46):
        ini = RNG.uniform(0, 1.0) ** 1.4; f = RNG.uniform(2400, 6200); dur = RNG.uniform(.05, .14)
        i0 = int(ini * SR); g = t(dur)
        grao = np.sin(2 * np.pi * f * g) * np.sin(np.pi * g / dur) ** 2 * (1 - ini) * RNG.uniform(.4, 1)
        x[i0:i0 + len(g)] += grao[:len(x) - i0]
    y = reverb(x, 1.0, .4)
    return estereo(y, .5 * np.sin(np.linspace(0, 6, len(y))))  # cintilação passeando entre os lados


def gravar(nome, x, pasta):
    x = x / (np.abs(x).max() + 1e-9) * (NIVEL[nome] / VOLS_MOTOR[nome])
    x = np.clip(x, -1, 1)
    arq = pasta / f"{nome}.wav"
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32000).astype("<i2").tobytes())
    return arq


def efeitos_v2(pasta: Path) -> dict:
    pasta.mkdir(exist_ok=True)
    return {n: gravar(n, f(), pasta) for n, f in
            (("whoosh", whoosh), ("boom", boom), ("pop", pop), ("carimbo", carimbo), ("brilho", brilho), ("po", po))}


def main():
    mod, n = sys.argv[1], int(sys.argv[2])
    nome = NOMES[(mod, n)]
    serie = importlib.import_module(mod)
    m = serie.m
    efeitos = efeitos_v2(AQUI / "sfx2")
    cfg, eventos = m.montar_cfg(n, serie.REELS)
    pasta = AQUI / f"audio_som2_{nome}"; pasta.mkdir(exist_ok=True)
    com, _ = m.audio(serie.REELS[n], pasta, eventos, cfg["total"], efeitos)
    saida = AQUI.parent / "renders_som2"; saida.mkdir(exist_ok=True)
    antigo = saida / f"{nome}-publicado.mp4"
    if not antigo.exists():
        urllib.request.urlretrieve(f"https://api.orbit.advogadaleticiabarros.com.br/media/{nome}.mp4", antigo)
    final = saida / f"{nome}-som2.mp4"
    subprocess.run([str(m.FF), "-v", "error", "-y", "-i", antigo, "-i", com, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-shortest", "-movflags", "+faststart", final], check=True)
    print(nome, "eventos:", len(eventos), "total:", cfg["total"], "->", final)


if __name__ == "__main__":
    main()
