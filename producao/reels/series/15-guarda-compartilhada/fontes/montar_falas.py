"""Junta os trechos escolhidos das gravações 4K (15/08/2025) num vídeo de fala por Reels (1080x1920, 30 fps).
Cortes entre palavras (tempos do Whisper). A = tomada limpa 163603; B = tomada longa 162647.
"""
import subprocess
from pathlib import Path

FF = r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
SRC = Path(r"C:\Users\prosy\Desktop\Leticia conteudos\novos videos\Guarda compartilhada x unilateral")
A, B = SRC / "20250815_163603.mp4", SRC / "20250815_162647.mp4"
AQUI = Path(__file__).resolve().parent
VIDEOS = AQUI.parent / "work" / "videos"

FALAS = {
    1: [(A, 0.75, 28.62)],
    2: [(A, 28.40, 36.62), (B, 30.08, 34.46), (A, 49.15, 63.98)],
    3: [(B, 66.20, 85.62), (B, 92.88, 101.88), (B, 104.78, 111.35), (B, 166.25, 169.12)],
}
GRADE = "scale=1080:1920:flags=lanczos,eq=contrast=1.05:saturation=0.96:gamma=0.99,colorbalance=rm=0.03:gm=0.01:bm=-0.03"


def montar(n: int, trechos) -> Path:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    destino = VIDEOS / f"fala-r{n}.mp4"
    entradas, filtros, rotulos = [], [], ""
    for i, (arq, a, b) in enumerate(trechos):
        d = round(b - a, 3)
        entradas += ["-ss", str(a), "-t", str(d), "-i", str(arq)]
        filtros.append(f"[{i}:v]{GRADE},fps=30,setpts=PTS-STARTPTS[v{i}]")
        filtros.append(f"[{i}:a]aresample=48000,afade=t=in:d=0.02,afade=t=out:st={d - 0.03}:d=0.03,asetpts=PTS-STARTPTS[a{i}]")
        rotulos += f"[v{i}][a{i}]"
    filtros.append(f"{rotulos}concat=n={len(trechos)}:v=1:a=1[v][a]")
    subprocess.run([FF, "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(destino)], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(destino), "-vn", "-ac", "1", "-ar", "16000", str(AQUI / f"fala-r{n}.wav")], check=True)
    return destino


if __name__ == "__main__":
    for n, tr in FALAS.items():
        print("ok", montar(n, tr))
