"""Monta a fala dos 2 Reels da série 18 (20/10/2026) a partir de Downloads/IMG_0330.MOV (tomada única, 3 min 07 s,
1080x1920 30 fps, boa luz: sem correção de cor). Cortes entre palavras (Whisper medium, transcricao-img0330.json):
cada trecho é (início da 1ª palavra, início da última palavra); o fim vem do fim da última palavra.
Fatos conferidos (20/10/2026):
- Limbo previdenciário: o INSS dá alta (ou nega o benefício por incapacidade) e o médico do trabalho/empresa considera o
  empregado inapto. Jurisprudência majoritária do TST: cessado o benefício, o contrato volta a produzir efeitos e o
  empregador responde pelos salários do período (o empregado fica à disposição, CLT art. 4º; risco da atividade é do
  empregador, CLT art. 2º).
CORTADOS:
- 44,6-51 s "auxílio-acidente comum / auxílio-acidente de trabalho": nome errado do benefício (o certo é auxílio por
  incapacidade temporária, comum ou acidentário; auxílio-acidente é outro benefício, indenizatório).
- 147-150 s e 174,5-178 s "o contrato fica suspenso": tecnicamente errado (com a alta o contrato volta a valer; contrato
  suspenso é sem salário).
- 88-95 s "tenho um caso aqui no escritório, 10 meses sem salário" e 158-160 s "já tive casos aqui": caso concreto do
  escritório (Provimento 205/2021 da OAB), mesmo critério da série 17. Aprovado pela Jessica em 20/10/2026.
- 56,8-64,2 s (repete o exemplo) e 111,6-118 s (repete a ideia), para caber em ~50 s.
"""
import json
import subprocess
from pathlib import Path

FF = r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
SRC = Path(r"C:\Users\prosy\Downloads\IMG_0330.MOV")
AQUI = Path(__file__).resolve().parent
VIDEOS = AQUI.parent / "work" / "videos"
PALAVRAS = [w for s in json.loads((AQUI / "transcricao-img0330.json").read_text(encoding="utf-8"))["segments"] for w in s["words"]]

FALAS = {
    # 1 · O que é limbo previdenciário
    1: [(0.00, 2.82), (4.66, 12.26), (13.66, 15.98), (23.93, 35.98), (37.08, 43.76), (64.44, 65.72),
        (78.56, 83.70), (84.46, 88.04), (183.86, 186.24)],
    # 2 · Quem paga o salário no limbo
    2: [(96.38, 98.24), (100.04, 103.54), (103.86, 110.84), (121.08, 122.28), (123.48, 126.66), (129.62, 131.98),
        (134.30, 145.46), (150.92, 155.44), (166.30, 167.48), (179.12, 182.28), (183.86, 186.24)],
}
IMAGEM = "scale=1080:1920:flags=lanczos,fps=30,setsar=1"


def _limites(ini: float, ult: float) -> tuple[float, float]:
    i = next(k for k, w in enumerate(PALAVRAS) if abs(w["start"] - ini) < 0.02)
    j = next(k for k, w in enumerate(PALAVRAS) if abs(w["start"] - ult) < 0.02)
    antes = PALAVRAS[i - 1]["end"] if i else 0.0
    depois = PALAVRAS[j + 1]["start"] if j + 1 < len(PALAVRAS) else PALAVRAS[j]["end"] + 0.4
    a = max(antes + 0.02, PALAVRAS[i]["start"] - 0.08)
    b = min(depois - 0.02, PALAVRAS[j]["end"] + 0.15)
    return round(a, 3), round(b, 3)


def montar(n: int) -> Path:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    destino = VIDEOS / f"fala-r{n}.mp4"
    entradas, filtros, rotulos = [], [], ""
    for i, (ini, ult) in enumerate(FALAS[n]):
        a, b = _limites(ini, ult)
        d = round(b - a, 3)
        entradas += ["-ss", str(a), "-t", str(d), "-i", str(SRC)]
        filtros.append(f"[{i}:v]{IMAGEM},setpts=PTS-STARTPTS[v{i}]")
        filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03,"
                       f"afade=t=out:st={d - 0.05}:d=0.05,asetpts=PTS-STARTPTS[a{i}]")
        rotulos += f"[v{i}][a{i}]"
    filtros.append(f"{rotulos}concat=n={len(FALAS[n])}:v=1:a=1[v][a]")
    subprocess.run([FF, "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(destino)], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(destino), "-vn", "-ac", "1", "-ar", "16000", str(AQUI / f"fala-r{n}.wav")],
                   check=True)
    return destino


if __name__ == "__main__":
    import sys
    for n in [int(a) for a in sys.argv[1:]] or FALAS:
        print("ok", montar(n))
