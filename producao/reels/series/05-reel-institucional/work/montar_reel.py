"""Monta o reel institucional a partir dos brutos.

v2: corrige o desencontro de áudio/vídeo da v1 (o tratamento de áudio por
cena, antes da concatenação, ia acumulando um pequeno atraso a cada
transição). Agora cada cena só é cortada e tem o PTS resetado; o
tratamento de áudio (ruído, volume) roda uma vez só, no vídeo inteiro já
montado. Cortes com mais folga nas pontas pra não cortar fala. Adiciona
a identificação (avatar + @adv.leticiabarros2) como marca-d'água durante
a parte falada, no mesmo padrão da skill de criativo pergunta.
"""
import subprocess
from pathlib import Path

FFMPEG = (
    r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
)
SRC = Path(r"C:\Users\prosy\Downloads\videos Leticia")
WORK = Path(r"C:\tmp\videos-reels\05-reel-institucional\work")
OUT_RAW = WORK / "reel_v2_bruto.mp4"
OUT_FINAL = Path(r"C:\tmp\videos-reels\05-reel-institucional\reel_v1.mp4")

# cada item e uma cena. Uma cena pode ser um unico (arquivo, inicio, fim),
# ou uma LISTA de sub-trechos do mesmo plano continuo, unidos por CORTE
# SECO (sem dissolve) - usado quando so precisamos tirar um pedaco do
# meio de uma cena, sem criar uma transicao onde nao existe troca de cena.
CLIPES = [
    [("1.mp4", 1.05, 4.85), ("1.mp4", 5.85, 6.55)],  # corte seco: tira o trecho de desligar a camera
    ("2.mp4", 0.55, 7.00),
    ("3.mp4", 0.65, 5.50),
    ("4.mp4", 1.60, 7.20),
    ("5.mp4", 0.90, 10.00),
    ("6.mp4", 0.00, 7.35),
    ("7.mp4", 1.05, 5.75),
]

XFADE = 0.4  # transicao suave e sutil, em segundos
INTRO_DUR = 1.6
OUTRO_DUR = 2.2

VIDEO_FILTER = "scale=1080:1920,eq=contrast=1.06:saturation=1.08:brightness=0.01,setpts=PTS-STARTPTS"
# audio tratado uma vez so, depois de concatenado (ver concatenar_com_transicoes)
AUDIO_FINAL_FILTER = "highpass=f=90,afftdn=nr=12:nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11"


def processar_clipe(nome: str, inicio: float, fim: float, indice: str) -> Path:
    origem = SRC / nome
    destino = WORK / f"proc_{indice}.mp4"
    duracao = fim - inicio
    cmd = [
        FFMPEG, "-y",
        "-ss", str(inicio), "-i", str(origem), "-t", str(duracao),
        "-vf", VIDEO_FILTER,
        "-af", "asetpts=PTS-STARTPTS",
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(destino),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return destino


def unir_com_corte_seco(sub_clipes: list[Path], destino: Path) -> Path:
    """Concatena sub-clipes do MESMO plano com corte seco (sem dissolve)."""
    lista_txt = destino.with_suffix(".txt")
    lista_txt.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in sub_clipes), encoding="utf-8"
    )
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", str(lista_txt),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(destino),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return destino


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
    subprocess.run(cmd, check=True, capture_output=True)
    return destino


def concatenar_com_transicoes(clipes: list[Path], durs: list[float]) -> tuple[float, float]:
    """Concatena com xfade/acrossfade. Retorna (inicio_fala, fim_fala) em
    segundos no timeline final, pra saber onde ligar a marca d'água.
    """
    inputs = []
    for c in clipes:
        inputs += ["-i", str(c)]

    n = len(clipes)
    filtro = []
    acumulado = durs[0]
    v_prev, a_prev = "0:v", "0:a"
    inicio_fala = durs[0] - XFADE  # fala comeca quando a 1a cena (indice 1) entra

    for i in range(1, n):
        offset = acumulado - XFADE
        if i == 1:
            inicio_fala = offset
        v_out = f"v{i}"
        a_out = f"a{i}"
        filtro.append(
            f"[{v_prev}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{v_out}]"
        )
        filtro.append(
            f"[{a_prev}][{i}:a]acrossfade=d={XFADE}[{a_out}]"
        )
        v_prev, a_prev = v_out, a_out
        acumulado += durs[i] - XFADE

    fim_fala = acumulado - (durs[-1] - XFADE) - XFADE  # onde comeca o outro

    filtro_str = ";".join(filtro)
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filtro_str,
        "-map", f"[{v_prev}]", "-map", f"[{a_prev}]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "pcm_s16le",
        str(OUT_RAW),
    ]
    subprocess.run(cmd, check=True)
    return inicio_fala, fim_fala


def aplicar_audio_e_marca_dagua(inicio_fala: float, fim_fala: float) -> None:
    identificacao = WORK / "identificacao.png"
    cmd = [
        FFMPEG, "-y",
        "-i", str(OUT_RAW),
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

    processados = [intro_clip]
    duracoes = [INTRO_DUR]
    for i, cena in enumerate(CLIPES, start=1):
        if isinstance(cena, tuple):
            cena = [cena]
        sub_clipes = []
        duracao_total = 0.0
        for j, (nome, ini, fim) in enumerate(cena):
            p = processar_clipe(nome, ini, fim, f"{i}_{j}")
            sub_clipes.append(p)
            duracao_total += fim - ini
            print(f"processado {nome} [{ini}-{fim}]: {fim - ini:.2f}s")

        if len(sub_clipes) > 1:
            unido = unir_com_corte_seco(sub_clipes, WORK / f"cena_{i}.mp4")
            processados.append(unido)
        else:
            processados.append(sub_clipes[0])
        duracoes.append(duracao_total)

    processados.append(outro_clip)
    duracoes.append(OUTRO_DUR)

    inicio_fala, fim_fala = concatenar_com_transicoes(processados, duracoes)
    print(f"marca d'agua entre {inicio_fala:.2f}s e {fim_fala:.2f}s")

    aplicar_audio_e_marca_dagua(inicio_fala, fim_fala)
    print("Reel final em", OUT_FINAL)


if __name__ == "__main__":
    main()
