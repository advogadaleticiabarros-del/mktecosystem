"""Conferência do Reel renderizado (padrão premium de 21/10/2026, skill leticia-reels-premium).

Uso: py conferir.py <mp4> [cfg_rN.json]
Imprime em poucas linhas: duração, resolução, taxa e volume; avisos de imagem congelada (fora do fechamento),
volume fora de -14 LUFS / pico acima de -1 dBTP, formato fora da exportação do manual e cenas de vídeo mais longas
que o clipe (com o cfg). Gera <mp4>_folha.jpg: 10 quadros de 240 px para a revisão final.
Sai com código 1 se houver aviso.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from fala import FF, FFPROBE, duracao

FPS = 30
OUTRO = 3.8          # duração do fechamento (motor.OUTRO): parado de propósito
ALVO_LUFS, TOL_LUFS, PICO_MAX = -14.0, 1.0, -1.0
TAXA = (10_000_000, 12_000_000)


def _stderr(*args) -> str:
    return subprocess.run([str(FF), "-hide_banner", "-nostats", *map(str, args)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stderr


# --------------------------------------------------------------------------- leitura dos logs
def ler_congelamentos(log: str, ate: float, fim: float) -> list[tuple[float, float]]:
    """Trechos de imagem parada (freezedetect) que começam antes de `ate` (o início do fechamento)."""
    saida, ini = [], None
    for m in re.finditer(r"freeze_(start|end): ([\d.]+)", log):
        if m.group(1) == "start":
            ini = float(m.group(2))
        elif ini is not None:
            saida.append((ini, float(m.group(2))))
            ini = None
    if ini is not None:
        saida.append((ini, fim))
    return [(s, e) for s, e in saida if s < ate]


def ler_volume(log: str) -> tuple[float, float]:
    """(volume integrado em LUFS, pico verdadeiro em dBTP) do resumo do ebur128."""
    resumo = log[log.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", resumo)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", resumo)
    return float(i.group(1)), float(p.group(1))


# --------------------------------------------------------------------------- avisos
def avisos_volume(lufs: float, pico: float) -> list[str]:
    avisos = []
    if abs(lufs - ALVO_LUFS) > TOL_LUFS:
        avisos.append(f"volume: {lufs:.1f} LUFS (alvo -14 ±1)")
    if pico > PICO_MAX:
        avisos.append(f"pico: {pico:.1f} dBTP (máximo -1)")
    return avisos


def avisos_formato(info: dict) -> list[str]:
    avisos = []
    if (info["w"], info["h"]) != (1080, 1920):
        avisos.append(f"resolução {info['w']}x{info['h']} (alvo 1080x1920)")
    if abs(info["fps"] - FPS) > 0.01:
        avisos.append(f"{info['fps']:.2f} fps (alvo 30)")
    if not TAXA[0] * 0.97 <= info["vbr"] <= TAXA[1] * 1.03:
        avisos.append(f"vídeo a {info['vbr'] / 1e6:.1f} Mbps (alvo 10 a 12)")
    if info["acodec"] != "aac" or info["ar"] != 48000 or not 120_000 <= info["abr"] <= 136_000:
        avisos.append(f"áudio {info['acodec']} {info['ar']} Hz {info['abr'] // 1000} kbps (alvo AAC 48000 Hz 128 kbps)")
    return avisos


def cenas_longas(cfg: dict) -> list[str]:
    """Cenas cujo vídeo de fundo acaba antes da cena (o engine segura o último quadro: imagem congelada)."""
    avisos, cenas = [], cfg["cenas"]
    for i, c in enumerate(cenas):
        bg = c.get("bg") or {}
        if not bg.get("seq"):
            continue
        fim = cenas[i + 1]["a"] if i + 1 < len(cenas) else cfg["total"]
        precisa = (fim - c["a"]) * bg.get("vel", 1.0) + bg.get("ini", 0.0)
        tem = bg["n"] / FPS
        if precisa * FPS > bg["n"] + 0.5:
            congela = c["a"] + (tem - bg.get("ini", 0.0)) / bg.get("vel", 1.0)
            avisos.append(f"cena {i} ({bg['seq']}): {fim - c['a']:.1f}s sobre um clipe de {tem:.1f}s (congela aos {congela:.1f}s)")
    return avisos


# --------------------------------------------------------------------------- medição
def _formato(mp4) -> dict:
    r = json.loads(subprocess.run([str(FFPROBE), "-v", "error", "-show_entries",
                                   "stream=codec_type,codec_name,width,height,r_frame_rate,bit_rate,sample_rate", "-of", "json", str(mp4)],
                                  capture_output=True, text=True, check=True).stdout)
    v = next(s for s in r["streams"] if s["codec_type"] == "video")
    a = next((s for s in r["streams"] if s["codec_type"] == "audio"), {})
    num, den = map(int, v["r_frame_rate"].split("/"))
    return {"w": v["width"], "h": v["height"], "fps": num / den, "vbr": int(v.get("bit_rate", 0)),
            "acodec": a.get("codec_name", "-"), "ar": int(a.get("sample_rate", 0)), "abr": int(a.get("bit_rate", 0))}


def folha(mp4, destino, dur: float) -> None:
    """10 quadros espalhados pelo vídeo, 240 px de largura, em grade 5x2."""
    sel = "+".join(f"eq(n,{int((k + .5) * dur / 10 * FPS)})" for k in range(10))
    subprocess.run([str(FF), "-v", "error", "-y", "-i", str(mp4), "-vf", f"select='{sel}',scale=240:-2,tile=5x2", "-frames:v", "1",
                    "-q:v", "4", str(destino)], check=True)


def conferir(mp4, cfg: dict | None = None) -> tuple[list[str], list[str]]:
    """(resumo, avisos) do Reel; grava a folha de quadros ao lado do mp4."""
    mp4 = Path(mp4)
    dur, info = duracao(mp4), _formato(mp4)
    lufs, pico = ler_volume(_stderr("-i", mp4, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"))
    inicio_fechamento = (cfg["total"] - OUTRO) if cfg else dur - OUTRO
    for c in (cfg or {}).get("cenas", []):
        if c.get("outro"):
            inicio_fechamento = c["a"]
    parados = ler_congelamentos(_stderr("-i", mp4, "-an", "-vf", "freezedetect=n=-60dB:d=0.5", "-f", "null", "-"), inicio_fechamento, dur)
    avisos = [f"imagem congelada: {s:.1f}s a {e:.1f}s" for s, e in parados]
    avisos += avisos_volume(lufs, pico) + avisos_formato(info)
    if cfg:
        avisos += cenas_longas(cfg)
    destino = mp4.with_name(mp4.stem + "_folha.jpg")
    folha(mp4, destino, dur)
    resumo = [f"{mp4.name}: {dur:.1f}s, {info['w']}x{info['h']} a {info['fps']:.0f} fps, {info['vbr'] / 1e6:.1f} Mbps, "
              f"{lufs:.1f} LUFS, pico {pico:.1f} dBTP", f"folha: {destino}"]
    return resumo, avisos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cfg = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else None
    resumo, avisos = conferir(sys.argv[1], cfg)
    print("\n".join(resumo))
    print("sem avisos" if not avisos else "\n".join(f"AVISO {a}" for a in avisos))
    sys.exit(1 if avisos else 0)
