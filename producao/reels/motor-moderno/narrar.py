"""Narração com a voz clonada da Letícia (ElevenLabs) no lugar do áudio do NotebookLM.

Entrada: um roteiro em texto, com uma parte por Reels separada por linhas "## ...".
Saída (na pasta indicada, normalmente fontes/):
- narracao.wav: as partes em sequência, com uma pausa entre elas (mono, 16 bits);
- transcricao.json: no mesmo formato do Whisper (segments → words), com o tempo exato de cada
  palavra vindo do próprio ElevenLabs. Não precisa transcrever nem corrigir palavras.

Uso: py narrar.py roteiro.txt [pasta_saida] [--checar]
Chave e voz: variáveis ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID, ou o arquivo
C:\\Users\\prosy\\.elevenlabs-leticia.json (fora do git): chave na 1ª linha e ID da voz na 2ª, ou JSON.

Boas práticas (adaptadas do OpenMontage, 14/10/2026):
- endpoint /with-timestamps: o tempo de cada palavra vem junto com o áudio;
- previous_text/next_text: cada parte é gerada sabendo o que vem antes e depois (entonação contínua);
- seed fixa: gerar de novo o mesmo texto dá a mesma fala;
- cache por conteúdo: texto e ajustes iguais não são cobrados de novo (pasta cache_voz/).
"""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

FF = Path(r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe")
CONFIG_LOCAL = Path.home() / ".elevenlabs-leticia.json"
API = "https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps"
TAXA = 44100
PAUSA = 0.6  # segundos de silêncio entre as partes
AJUSTES = {
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0, "use_speaker_boost": True},
    "seed": 2026,
}
# Escrever como se fala: o ElevenLabs lê mal número, símbolo e abreviação em português.
LER_POR_EXTENSO = re.compile(r"\d|º|ª|§|%|/|\bart\.|\bCLT\b|\bINSS\b|\bTST\b")
VETADOS = ("especialista", "garanto", "garantido", "100%", "melhor advogada")  # Provimento 205/2021
CARACTERES_POR_SEGUNDO = 15


# --------------------------------------------------------------------------- roteiro
def partes_do_roteiro(texto: str) -> list[dict]:
    """Divide o roteiro em partes (uma por Reels). Linhas que começam com "##" abrem uma parte nova."""
    partes, atual = [], None
    for linha in texto.splitlines():
        if linha.startswith("##"):
            atual = {"titulo": linha.lstrip("# ").strip(), "linhas": []}
            partes.append(atual)
        elif linha.strip() and not linha.startswith("#"):
            if atual is None:
                atual = {"titulo": "Parte 1", "linhas": []}
                partes.append(atual)
            atual["linhas"].append(linha.strip())
    return [{"titulo": p["titulo"], "texto": " ".join(p["linhas"])} for p in partes if p["linhas"]]


def checar(partes: list[dict]) -> list[str]:
    """Avisos antes de gastar crédito: leitura de números/siglas, termos vetados pela OAB e duração."""
    avisos = []
    for p in partes:
        for m in LER_POR_EXTENSO.finditer(p["texto"]):
            trecho = p["texto"][max(0, m.start() - 15):m.end() + 15]
            avisos.append(f'{p["titulo"]}: escreva por extenso ou como se fala → "…{trecho}…"')
        for termo in VETADOS:
            if termo in p["texto"].lower():
                avisos.append(f'{p["titulo"]}: termo vetado pela OAB → "{termo}"')
        seg = len(p["texto"]) / CARACTERES_POR_SEGUNDO
        if not 15 <= seg <= 50:
            avisos.append(f'{p["titulo"]}: ~{seg:.0f} s de fala (o Reels pede de 20 a 45 s)')
    return avisos


# --------------------------------------------------------------------------- ElevenLabs
def palavras_do_alinhamento(al: dict, desloca: float = 0.0) -> list[dict]:
    """Agrupa o tempo por caractere do ElevenLabs em palavras, no formato do Whisper (" palavra")."""
    texto, dono = "", []
    for i, c in enumerate(al["characters"]):
        texto += c
        dono += [i] * len(c)
    ini, fim = al["character_start_times_seconds"], al["character_end_times_seconds"]
    return [{"word": " " + m.group(), "start": round(ini[dono[m.start()]] + desloca, 3),
             "end": round(fim[dono[m.end() - 1]] + desloca, 3)} for m in re.finditer(r"\S+", texto)]


def sintetizar(texto: str, antes: str, depois: str, cfg: dict, post, cache: Path) -> dict:
    """Uma parte → {"mp3": bytes, "alinhamento": {...}}. Usa o cache quando o pedido é idêntico."""
    corpo = {"text": texto, **AJUSTES}
    if antes:
        corpo["previous_text"] = antes
    if depois:
        corpo["next_text"] = depois
    chave = hashlib.sha256(json.dumps([cfg["voice_id"], corpo], sort_keys=True).encode()).hexdigest()[:20]
    guardado = cache / f"{chave}.json"
    if guardado.exists():
        r = json.loads(guardado.read_text(encoding="utf-8"))
    else:
        resp = post(API.format(voz=cfg["voice_id"]), json=corpo, timeout=180,
                    headers={"xi-api-key": cfg["api_key"], "Accept": "application/json"},
                    params={"output_format": "mp3_44100_128"})
        if resp.status_code != 200:
            raise RuntimeError(f"ElevenLabs {resp.status_code}: {resp.text[:300]}")
        r = resp.json()
        cache.mkdir(parents=True, exist_ok=True)
        guardado.write_text(json.dumps(r), encoding="utf-8")
    return {"mp3": base64.b64decode(r["audio_base64"]), "alinhamento": r.get("alignment") or r["normalized_alignment"]}


def narrar(partes: list[dict], cfg: dict, post, cache: Path, decodificar) -> tuple[bytes, dict, list]:
    """Gera todas as partes e junta: (pcm mono 16 bits, transcricao no formato Whisper, trechos por parte).

    `decodificar(mp3) -> pcm` converte cada parte para PCM em TAXA Hz (ffmpeg em produção)."""
    pcm, segmentos, trechos, t = b"", [], [], 0.0
    silencio = b"\x00\x00" * int(PAUSA * TAXA)
    for i, p in enumerate(partes):
        antes = partes[i - 1]["texto"] if i else ""
        depois = partes[i + 1]["texto"] if i + 1 < len(partes) else ""
        r = sintetizar(p["texto"], antes, depois, cfg, post, cache)
        bruto = decodificar(r["mp3"])
        dur = len(bruto) / 2 / TAXA
        palavras = palavras_do_alinhamento(r["alinhamento"], desloca=t)
        segmentos.append({"start": round(t, 3), "end": round(t + dur, 3), "text": " " + p["texto"], "words": palavras})
        trechos.append((round(t, 2), round(t + dur, 2)))
        pcm += bruto + silencio
        t += dur + PAUSA
    return pcm, {"text": " ".join(p["texto"] for p in partes), "segments": segmentos, "language": "pt"}, trechos


# --------------------------------------------------------------------------- execução
def ler_config(texto: str) -> dict:
    """Aceita JSON {"api_key", "voice_id"} ou texto simples: chave na 1ª linha, ID da voz na 2ª."""
    texto = texto.strip()
    if texto.startswith("{"):
        return json.loads(texto)
    linhas = [l.strip() for l in texto.splitlines() if l.strip() and "COLE" not in l]
    return {"api_key": linhas[0] if linhas else None, "voice_id": linhas[1] if len(linhas) > 1 else None}


def carregar_cfg() -> dict:
    cfg = {"api_key": os.environ.get("ELEVENLABS_API_KEY"), "voice_id": os.environ.get("ELEVENLABS_VOICE_ID")}
    if CONFIG_LOCAL.exists():
        local = ler_config(CONFIG_LOCAL.read_text(encoding="utf-8-sig"))
        cfg = {k: cfg[k] or local.get(k) for k in cfg}
    falta = [k for k, v in cfg.items() if not v]
    if falta:
        raise SystemExit(f"Falta {', '.join(falta)}: defina ELEVENLABS_API_KEY/ELEVENLABS_VOICE_ID ou {CONFIG_LOCAL}")
    return cfg


def mp3_para_pcm(mp3: bytes) -> bytes:
    r = subprocess.run([str(FF), "-v", "error", "-i", "pipe:0", "-f", "s16le", "-ac", "1", "-ar", str(TAXA), "pipe:1"],
                       input=mp3, capture_output=True, check=True)
    return r.stdout


def principal(argv: list[str]) -> None:
    so_checar = "--checar" in argv
    args = [a for a in argv if not a.startswith("--")]
    roteiro = Path(args[0])
    saida = Path(args[1]) if len(args) > 1 else roteiro.parent
    partes = partes_do_roteiro(roteiro.read_text(encoding="utf-8"))
    avisos = checar(partes)
    for a in avisos:
        print("AVISO", a)
    print(f"{len(partes)} parte(s), {sum(len(p['texto']) for p in partes)} caracteres")
    if so_checar or (avisos and "--mesmo-assim" not in argv):
        if avisos:
            print("Corrija os avisos (ou rode com --mesmo-assim) antes de gerar.")
        return
    import requests
    pcm, transcricao, trechos = narrar(partes, carregar_cfg(), requests.post, saida / "cache_voz", mp3_para_pcm)
    saida.mkdir(parents=True, exist_ok=True)
    with wave.open(str(saida / "narracao.wav"), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(TAXA); f.writeframes(pcm)
    (saida / "transcricao.json").write_text(json.dumps(transcricao, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok: {saida / 'narracao.wav'} + transcricao.json")
    for p, (a, b) in zip(partes, trechos):
        print(f'  {p["titulo"]}: trechos [({a}, {b})]')


if __name__ == "__main__":
    principal(sys.argv[1:])
