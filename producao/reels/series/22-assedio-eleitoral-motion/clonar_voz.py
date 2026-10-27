"""Cria o clone Instant da voz da Dra. no ElevenLabs a partir da amostra tirada das gravações dela (27/10/2026).

Precisa da chave com a permissão "Voices: Write" (a de 14/10 só tinha Text to Speech). A amostra
Desktop\\NOVOS REELS\\voz-para-clonar-leticia.wav tem 3 min 54 s de fala limpa (VIDEO 1 e VIDEO 2).
Guarda o ID antigo em ~/.elevenlabs-leticia.json.antigo-<id> e grava o novo na 2ª linha do arquivo de config,
que é onde o narrar.py procura. Depois: gerar a frase de teste e mandar para a Jessica aprovar antes de narrar a série.

Uso: py clonar_voz.py [amostra.wav]
"""
import shutil
import sys
from pathlib import Path

import requests

CONFIG = Path.home() / ".elevenlabs-leticia.json"
AMOSTRA = Path.home() / "Desktop" / "NOVOS REELS" / "voz-para-clonar-leticia.wav"


def main(argv):
    amostra = Path(argv[0]) if argv else AMOSTRA
    chave, antigo = [l.strip() for l in CONFIG.read_text(encoding="utf-8").splitlines()[:2]]
    with amostra.open("rb") as f:
        r = requests.post("https://api.elevenlabs.io/v1/voices/add", headers={"xi-api-key": chave}, timeout=300,
                          data={"name": "Letícia Barros (gravações 10-2026)", "remove_background_noise": "false",
                                "description": "Clone Instant a partir das gravações de Reels de 26-27/10/2026"},
                          files={"files": (amostra.name, f, "audio/wav")})
    if r.status_code != 200:
        sys.exit(f"ElevenLabs recusou ({r.status_code}): {r.text[:300]}")
    novo = r.json()["voice_id"]
    shutil.copy(CONFIG, CONFIG.with_name(f"{CONFIG.name}.antigo-{antigo}"))
    CONFIG.write_text(f"{chave}\n{novo}\n", encoding="utf-8")
    print("clone criado:", novo, "| ID antigo guardado em", CONFIG.with_name(f"{CONFIG.name}.antigo-{antigo}"))


if __name__ == "__main__":
    main(sys.argv[1:])
