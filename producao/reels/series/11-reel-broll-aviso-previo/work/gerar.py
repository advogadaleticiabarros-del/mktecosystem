"""Monta o reel com b-roll de fundo + texto cinético dourado sobreposto
(fundo transparente), padrão da squad reels-reel-generico.
"""
import asyncio
import base64
import subprocess
from pathlib import Path

from jinja2 import Template
from playwright.async_api import async_playwright

FFMPEG = (
    r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
)
LOGO = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\logo\logo-800x800.png")
WORK = Path(__file__).parent
XFADE = 0.4

CENAS = [
    {"kicker": "Gestante CLT", "texto": "Engravidou durante o <em>aviso prévio</em>? Isso muda alguma coisa", "tamanho_fonte": 54},
    {"kicker": "O que muda", "numero": "1", "texto": "A estabilidade começa na <em>confirmação da gravidez</em>, não na assinatura de um papel", "tamanho_fonte": 46},
    {"kicker": "O que muda", "numero": "2", "texto": "Vale <em>mesmo que a empresa já tenha avisado</em> que o contrato ia terminar", "tamanho_fonte": 48},
    {"kicker": "O que muda", "numero": "3", "texto": "A proteção vai até <em>5 meses após o parto</em>", "tamanho_fonte": 52},
    {"kicker": "", "texto": "Se isso é o seu caso,<br><em>procure uma advogada de confiança</em>", "tamanho_fonte": 48, "rodape": "Advogada Trabalhista | OAB/ES 39.948"},
]
DURACOES = [3.8, 4.6, 4.6, 4.2, 4.2]
BROLL = [WORK / f"broll_{i}.mp4" for i in range(5)]


def _logo_src() -> str:
    return "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()


async def renderizar_textos() -> list[Path]:
    tpl = Template((WORK / "scene.html").read_text(encoding="utf-8"))
    logo_src = _logo_src()
    caminhos = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for i, cena in enumerate(CENAS):
            html = tpl.render(logo_src=logo_src, **cena)
            await page.set_content(html)
            caminho = WORK / f"texto_{i}.png"
            await page.screenshot(path=str(caminho), omit_background=True)
            caminhos.append(caminho)
        await browser.close()
    return caminhos


def compor_cena(broll: Path, texto_png: Path, duracao: float, destino: Path) -> None:
    """Corta o b-roll pra duração da cena, escala/cropa pra 1080x1920,
    remove áudio original, e sobrepõe o PNG de texto (transparente)."""
    cmd = [
        FFMPEG, "-y",
        "-t", str(duracao), "-i", str(broll),
        "-loop", "1", "-t", str(duracao), "-i", str(texto_png),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1[bg];"
        "[bg][1:v]overlay=0:0:format=auto[v]",
        "-map", "[v]", "-map", "2:a",
        "-t", str(duracao),
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(destino),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def concatenar(clipes: list[Path], durs: list[float], destino: Path) -> None:
    inputs = []
    for c in clipes:
        inputs += ["-i", str(c)]

    n = len(clipes)
    filtro = []
    acumulado = durs[0]
    v_prev, a_prev = "0:v", "0:a"

    for i in range(1, n):
        offset = acumulado - XFADE
        v_out, a_out = f"v{i}", f"a{i}"
        filtro.append(f"[{v_prev}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{v_out}]")
        filtro.append(f"[{a_prev}][{i}:a]acrossfade=d={XFADE}[{a_out}]")
        v_prev, a_prev = v_out, a_out
        acumulado += durs[i] - XFADE

    filtro_str = ";".join(filtro)
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filtro_str,
        "-map", f"[{v_prev}]", "-map", f"[{a_prev}]",
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-maxrate", "6M", "-bufsize", "12M",
        "-c:a", "aac", "-b:a", "128k",
        str(destino),
    ]
    subprocess.run(cmd, check=True)


async def main():
    textos = await renderizar_textos()
    clipes = []
    for i, (broll, texto_png, dur) in enumerate(zip(BROLL, textos, DURACOES)):
        clipe = WORK / f"cena_{i}.mp4"
        compor_cena(broll, texto_png, dur, clipe)
        clipes.append(clipe)
        print(f"cena {i} composta ({dur}s)")
    saida = WORK.parent / "reel.mp4"
    concatenar(clipes, DURACOES, saida)
    print("Reel final em", saida)


if __name__ == "__main__":
    asyncio.run(main())
