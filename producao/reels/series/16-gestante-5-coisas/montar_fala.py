"""Junta as 7 partes da gravação "5 coisas que a empresa não pode fazer com a gestante" (31/07/2026, 4K vertical,
pasta PROJETOS/ecosystemmkt/BANCO IMAGENS/Advogada/videos Leticia) num vídeo de fala 1080x1920 a 30 fps.
Cortes pelo silêncio medido (silencedetect) e pelos tempos de palavra do Whisper.
Fatos conferidos em 16/10/2026:
- 1 estabilidade: ADCT art. 10, II, b (da confirmação da gravidez até 5 meses após o parto; só justa causa).
- 2 salário e direitos: CF art. 7º, VI e XXX; Lei 9.029/1995 (proíbe discriminação por gravidez).
- 3 insalubre: CLT art. 394-A + STF ADI 5.938 (afastamento de atividade insalubre em qualquer grau).
  CORTADO "ou perigoso": a lei fala de insalubridade; periculosidade não está no art. 394-A.
- 4 pré-natal: CLT art. 392, § 4º, II (dispensa para no mínimo 6 consultas e exames, sem desconto).
- 5 pedido de demissão: CLT art. 500 (empregado estável só pede demissão com assistência do sindicato ou
  autoridade do Ministério do Trabalho); aplicado à gestante pelo TST.
Cor: sem clarear (tom de pele já fiel no bruto; regra da skill leticia-reels).
"""
import subprocess
from pathlib import Path

FF = r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
SRC = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\Advogada\videos Leticia")
AQUI = Path(__file__).resolve().parent
VIDEOS = AQUI.parent / "work" / "videos"

# (parte, início, fim) em segundos
TRECHOS = [(1, 1.25, 4.97), (2, 0.66, 6.32), (3, 0.38, 5.36), (4, 2.02, 5.00), (5, 1.08, 9.84), (6, 0.18, 7.14),
           (7, 1.20, 5.50)]
IMAGEM = "scale=1080:1920:flags=lanczos,fps=30,setsar=1"


def montar() -> Path:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    destino = VIDEOS / "fala-r1.mp4"
    entradas, filtros, rotulos = [], [], ""
    for i, (parte, a, b) in enumerate(TRECHOS):
        d = round(b - a, 3)
        entradas += ["-ss", str(a), "-t", str(d), "-i", str(SRC / f"{parte}.mp4")]
        filtros.append(f"[{i}:v]{IMAGEM},setpts=PTS-STARTPTS[v{i}]")
        filtros.append(f"[{i}:a]aresample=48000,afade=t=in:d=0.03,afade=t=out:st={d - 0.05}:d=0.05,asetpts=PTS-STARTPTS[a{i}]")
        rotulos += f"[v{i}][a{i}]"
    filtros.append(f"{rotulos}concat=n={len(TRECHOS)}:v=1:a=1[v][a]")
    subprocess.run([FF, "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(destino)], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(destino), "-vn", "-ac", "1", "-ar", "16000", str(AQUI / "fala-r1.wav")],
                   check=True)
    return destino


if __name__ == "__main__":
    print("ok", montar())
