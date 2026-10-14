"""Monta o Reel #08 a partir de um único plano corrido (sem cortes
internos), seguindo o mesmo padrão validado no Reel 05: tratamento de
áudio uma vez só, correção leve de cor, conversão pra vertical
1080x1920, abertura/fechamento com identidade oficial (intro.png /
outro.png reaproveitados do Reel 05) e marca d'água durante a fala.
"""
import subprocess
from pathlib import Path

FFMPEG = (
    r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
)
SRC = Path(r"C:\Users\prosy\Desktop\novo video")
ARQUIVO_BRUTO = SRC / "video correto para usar .MOV"
WORK = Path(r"C:\tmp\videos-reels\08-novo-reel\work")
OUT_FINAL = Path(r"C:\tmp\videos-reels\08-novo-reel\reel_v1.mp4")

INICIO = 0.0
FIM = 77.3  # corta antes do silêncio/gesto de desligar a câmera (77.48s)

INTRO_DUR = 1.6
OUTRO_DUR = 2.2
XFADE = 0.4  # dissolve entre intro->fala e fala->outro, igual ao Reel 05

VIDEO_FILTER = (
    "crop=ih*9/16:ih,scale=1080:1920,"
    "eq=contrast=1.10:saturation=1.13:brightness=-0.16,"
    "curves=all='0/0 0.35/0.27 0.7/0.55 1/0.85',"
    "setpts=PTS-STARTPTS"
)
AUDIO_FINAL_FILTER = "highpass=f=90,afftdn=nr=12:nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11"


def imagem_para_clipe(imagem: Path, duracao: float, destino: Path) -> Path:
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", str(imagem),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-t", str(duracao),
        "-vf", "scale=1080:1920",
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(destino),
    ]
    subprocess.run(cmd, check=True)
    return destino


def processar_fala() -> Path:
    destino = WORK / "fala_proc.mp4"
    cmd = [
        FFMPEG, "-y",
        "-ss", str(INICIO), "-i", str(ARQUIVO_BRUTO), "-t", str(FIM - INICIO),
        "-vf", VIDEO_FILTER,
        "-af", "asetpts=PTS-STARTPTS",
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(destino),
    ]
    subprocess.run(cmd, check=True)
    return destino


def concatenar_com_transicoes(clipes: list[Path], durs: list[float], destino: Path) -> tuple[float, float]:
    inputs = []
    for c in clipes:
        inputs += ["-i", str(c)]

    n = len(clipes)
    filtro = []
    acumulado = durs[0]
    v_prev, a_prev = "0:v", "0:a"
    inicio_fala = durs[0] - XFADE

    for i in range(1, n):
        offset = acumulado - XFADE
        if i == 1:
            inicio_fala = offset + XFADE  # fim do dissolve intro->fala
        v_out = f"v{i}"
        a_out = f"a{i}"
        filtro.append(f"[{v_prev}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{v_out}]")
        filtro.append(f"[{a_prev}][{i}:a]acrossfade=d={XFADE}[{a_out}]")
        v_prev, a_prev = v_out, a_out
        acumulado += durs[i] - XFADE
        if i == n - 1:
            fim_fala = offset  # início do dissolve fala->outro (última iteração)

    filtro_str = ";".join(filtro)
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filtro_str,
        "-map", f"[{v_prev}]", "-map", f"[{a_prev}]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "pcm_s16le",
        str(destino),
    ]
    subprocess.run(cmd, check=True)
    return inicio_fala, fim_fala


def aplicar_audio_e_marca_dagua(bruto: Path, inicio_fala: float, fim_fala: float) -> None:
    identificacao = WORK / "identificacao.png"
    cmd = [
        FFMPEG, "-y",
        "-i", str(bruto),
        "-i", str(identificacao),
        "-filter_complex",
        (
            f"[1:v]format=rgba[wm];"
            f"[0:v][wm]overlay=x=48:y=1920-h-140:enable='between(t,{inicio_fala:.3f},{fim_fala:.3f})'[vout];"
            f"[0:a]{AUDIO_FINAL_FILTER}[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-maxrate", "6M", "-bufsize", "12M",
        "-c:a", "aac", "-b:a", "128k",
        str(OUT_FINAL),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    intro_clip = imagem_para_clipe(WORK / "intro.png", INTRO_DUR, WORK / "intro_clip.mp4")
    outro_clip = imagem_para_clipe(WORK / "outro.png", OUTRO_DUR, WORK / "outro_clip.mp4")
    fala = processar_fala()
    duracao_fala = FIM - INICIO

    bruto_unido = WORK / "unido_bruto.mp4"
    inicio_fala, fim_fala = concatenar_com_transicoes(
        [intro_clip, fala, outro_clip],
        [INTRO_DUR, duracao_fala, OUTRO_DUR],
        bruto_unido,
    )
    print(f"marca d'agua entre {inicio_fala:.2f}s e {fim_fala:.2f}s")

    aplicar_audio_e_marca_dagua(bruto_unido, inicio_fala, fim_fala)
    print("Reel final em", OUT_FINAL)


if __name__ == "__main__":
    main()
