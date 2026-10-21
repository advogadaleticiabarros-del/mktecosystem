"""Série 18, v2 (20/10/2026, pedido: "falas mais limpas, tirar as pausas e repetições, um pouco mais dinâmico").
Mesmo bruto e mesmos fatos/cortes de montar_falas.py (v1, que fica guardada). Diferenças:
- trechos menores, sem repetições: "vindo do INSS / vindo da empresa", "né?", "então", "quem tem que pagar esse
  salário" (repetia a frase anterior), "a empresa tem que pagar pelo período" e "se ele não trabalhou, não tem como
  ele receber" (repetiam a objeção);
- pausas medidas no áudio (silencedetect -44 dB, >= 0,25 s, em silencios.txt) e encurtadas para 0,18 s dentro de
  cada trecho;
- fala 5% mais rápida (setpts/atempo, sem mudar o tom).
Saída: ../work-v2/videos/fala-rN.mp4 + fala-rN.wav.
"""
import subprocess
from pathlib import Path

FF = r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
SRC = Path(r"C:\Users\prosy\Downloads\IMG_0330.MOV")
AQUI = Path(__file__).resolve().parent
VIDEOS = AQUI.parent / "work-v2" / "videos"
VEL = 1.05
MARGEM = 0.09  # silêncio mantido de cada lado de uma pausa encurtada
SILENCIOS = [tuple(map(float, linha.split())) for linha in (AQUI / "silencios.txt").read_text().split("\n") if linha.strip()]

# (início, fim) em segundos do bruto; as pausas internas são encurtadas automaticamente
FALAS = {
    1: [(0.00, 3.95),     # Você sabe o que é limbo previdenciário?
        (4.45, 12.88),    # Limbo previdenciário é quando o empregado está inapto para voltar às atividades no trabalho,
        (13.66, 16.70),   # seja por doença, acidente de trabalho.
        (23.85, 36.62),   # Por exemplo ... atestado escrito inapto, e aí ele vai para o INSS.
        (37.00, 44.25),   # Chegando lá, o INSS considera que ele está em alta, que não tem nenhum benefício para receber
        (64.40, 66.30),   # E aí o trabalhador fica nesse limbo,
        (67.20, 70.22),   # não tem nem dinheiro do INSS (sem o "fica nesse" e o "vindo do INSS" repetidos)
        (73.20, 76.10),   # e não tem nem dinheiro vindo da empresa.
        # (78,6-84,3 "então nem, nem, nem INSS paga..." ficou de fora: ela gagueja no "nem")
        (84.40, 87.55, "fixo"),  # O trabalhador muitas vezes pode ficar aí por meses (sem o "né?" logo depois)
        (183.80, 186.75)],  # Meu nome é Letícia Barros e aqui nesse perfil falo sobre seus direitos.
    2: [(96.30, 98.95),   # Durante esse período, no limbo previdenciário,
        (100.00, 103.80),  # quem é responsável por esse trabalhador? É a empresa.
        (103.80, 111.30),  # Porque o trabalhador não pode ser prejudicado ... ele está doente.
        (121.00, 122.95),  # Quem vai pagar esses salários,
        (124.98, 127.48),  # segundo a jurisprudência majoritária, (ela repete "segundo a jurisprudência")
        (131.40, 132.30),  # é a empresa.
        (135.95, 142.95),  # Ah, mas ele não trabalhou, mandou pro INSS, a empresa não tem mais essa responsabilidade.
        (145.40, 146.10),  # Errado.
        (150.85, 155.95),  # Se o trabalhador não conseguiu nenhum benefício do INSS, quem tem que pagar é a empresa.
        (166.25, 167.95),  # Tem que receber, mesmo sem trabalhar.
        (179.35, 182.95),  # A empresa tem que pagar como se o trabalhador estivesse de atestado.
        (183.80, 186.75)],
}
IMAGEM = "scale=1080:1920:flags=lanczos,fps=30,setsar=1"


def encostar(a: float, b: float, folga: float = 0.5) -> tuple[float, float]:
    """Os tempos do Whisper erram por alguns décimos: se a ponta do trecho cai em fala e há uma pausa real a até
    `folga` s, a ponta vai para a pausa (nunca corta palavra no meio)."""
    if not any(s <= a <= e for s, e in SILENCIOS):
        antes = [e for s, e in SILENCIOS if a - folga <= e <= a]
        if antes:
            a = max(antes) - MARGEM
    if not any(s <= b <= e for s, e in SILENCIOS):
        depois = [s for s, e in SILENCIOS if b <= s <= b + folga]
        if depois:
            b = min(depois) + MARGEM
    return a, b


def sem_pausas(a: float, b: float, fixo: str = "") -> list[tuple[float, float]]:
    """Divide [a, b] tirando o miolo de cada silêncio interno (fica MARGEM de cada lado)."""
    if not fixo:  # "fixo": ponta escolhida à mão (o ajuste levaria junto um "né?")
        a, b = encostar(a, b)
    partes, ini = [], a
    for s, e in SILENCIOS:
        if e <= a or s >= b:
            continue
        s, e = max(s, a), min(e, b)
        if s <= a + 0.01:          # silêncio no começo do trecho: começa onde a fala começa
            ini = max(ini, e - MARGEM)
            continue
        if e >= b - 0.01:          # silêncio no fim do trecho: termina onde a fala termina
            b = s + MARGEM
            break
        if e - s > 2 * MARGEM + 0.04:
            partes.append((ini, s + MARGEM))
            ini = e - MARGEM
    partes.append((ini, b))
    return [(round(x, 3), round(y, 3)) for x, y in partes if y - x > 0.05]


def montar(n: int) -> Path:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    destino = VIDEOS / f"fala-r{n}.mp4"
    pedacos = [p for t in FALAS[n] for p in sem_pausas(*t)]
    entradas, filtros, rotulos = [], [], ""
    for i, (a, b) in enumerate(pedacos):
        d = round(b - a, 3)
        entradas += ["-ss", str(a), "-t", str(d), "-i", str(SRC)]
        filtros.append(f"[{i}:v]{IMAGEM},setpts=PTS-STARTPTS[v{i}]")
        filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.02,"
                       f"afade=t=out:st={max(0, d - 0.03)}:d=0.03,asetpts=PTS-STARTPTS[a{i}]")
        rotulos += f"[v{i}][a{i}]"
    filtros.append(f"{rotulos}concat=n={len(pedacos)}:v=1:a=1[vc][ac]")
    filtros.append(f"[vc]setpts=PTS/{VEL},fps=30[v]")
    filtros.append(f"[ac]atempo={VEL}[a]")
    subprocess.run([FF, "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(destino)], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(destino), "-vn", "-ac", "1", "-ar", "16000", str(AQUI / f"fala-v2-r{n}.wav")],
                   check=True)
    print(f"r{n}: {len(pedacos)} pedaços, bruto {sum(t[1] - t[0] for t in FALAS[n]):.1f}s -> {sum(b - a for a, b in pedacos) / VEL:.1f}s")
    return destino


if __name__ == "__main__":
    import sys
    for n in [int(a) for a in sys.argv[1:]] or FALAS:
        montar(n)
