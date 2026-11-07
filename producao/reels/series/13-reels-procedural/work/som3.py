"""Efeitos sonoros v3 (07/11/2026, pedido da Jessica: "procure efeitos sonoros melhores").
Troca os efeitos sintetizados (som2) por gravações reais da Mixkit (licença Mixkit Sound Effects Free License: uso
comercial em vídeo liberado, sem atribuição). Mesmos nomes e níveis do som2, então entra no motor sem mudar nada.
Uso no roteiro: m.sfx = lambda pasta: som3.efeitos_v3(m.AQUI / "sfx3")"""
import subprocess
import urllib.request
import wave
from pathlib import Path

import numpy as np

from som2 import NIVEL, SR, VOLS_MOTOR

# nome: (id Mixkit, título, início s, duração máx. s)
FONTES = {
    "whoosh": (1491, "Cinematic whoosh fast transition", 0.0, 0.9),
    "boom": (788, "Cinematic whoosh deep impact", 0.0, 1.8),
    "pop": (2925, "Dry pop up notification alert", 0.0, 0.4),
    "carimbo": (2589, "Wood hard hit", 0.0, 0.7),
    "brilho": (866, "Fairy magic sparkle", 0.0, 1.6),
    "po": (3062, "Fairy sparkle whoosh", 0.0, 1.3),
}


def baixar(i, pasta):
    arq = pasta / f"mixkit-{i}.mp3"
    if not arq.exists():
        req = urllib.request.Request(f"https://assets.mixkit.co/active_storage/sfx/{i}/{i}-preview.mp3",
                                     headers={"User-Agent": "Mozilla/5.0"})
        arq.write_bytes(urllib.request.urlopen(req).read())
    return arq


def ler(mp3, ini, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ini), "-t", str(dur), "-i", str(mp3),
                          "-af", f"afade=t=out:st={max(dur - .25, 0)}:d=0.25", "-ac", "2", "-ar", str(SR),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").reshape(-1, 2) / 32768


def efeitos_v3(pasta: Path) -> dict:
    pasta.mkdir(exist_ok=True)
    saida = {}
    for nome, (i, _, ini, dur) in FONTES.items():
        x = ler(baixar(i, pasta), ini, dur)
        x = np.clip(x / (np.abs(x).max() + 1e-9) * (NIVEL[nome] / VOLS_MOTOR[nome]), -1, 1)
        arq = saida[nome] = pasta / f"{nome}.wav"
        with wave.open(str(arq), "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 32000).astype("<i2").tobytes())
    return saida


if __name__ == "__main__":
    for k, v in efeitos_v3(Path(__file__).resolve().parent / "sfx3").items():
        print(k, v)
