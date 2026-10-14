"""Monta um reel 100% de montagem (sem gravação): cenas de texto cinético
no padrão dourado/preto da marca, com transição suave entre cenas.
Reutilizável para qualquer reel desse tipo — só troca CENAS/pasta.
"""
import asyncio
import base64
import subprocess
import sys
from pathlib import Path

from jinja2 import Template
from playwright.async_api import async_playwright

FFMPEG = (
    r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
)
LOGO = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\logo\logo-800x800.png")
XFADE = 0.4


def _logo_src() -> str:
    return "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()


async def renderizar_cenas(pasta: Path, cenas: list[dict]) -> list[Path]:
    tpl = Template((pasta / "scene.html").read_text(encoding="utf-8"))
    logo_src = _logo_src()
    caminhos = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for i, cena in enumerate(cenas):
            html = tpl.render(logo_src=logo_src, **cena)
            await page.set_content(html)
            caminho = pasta / f"cena_{i}.png"
            await page.screenshot(path=str(caminho))
            caminhos.append(caminho)
        await browser.close()
    return caminhos


def imagem_para_clipe(imagem: Path, duracao: float, destino: Path) -> Path:
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", str(imagem),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-t", str(duracao),
        "-vf", "scale=1080:1920",
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(destino),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return destino


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


async def montar(pasta_reel: str, cenas: list[dict], durs: list[float], saida: str) -> None:
    pasta = Path(pasta_reel)
    work = pasta / "work"
    imagens = await renderizar_cenas(work, cenas)
    clipes = []
    for i, (img, dur) in enumerate(zip(imagens, durs)):
        clipe = imagem_para_clipe(img, dur, work / f"clipe_{i}.mp4")
        clipes.append(clipe)
        print(f"cena {i} renderizada ({dur}s)")
    concatenar(clipes, durs, Path(saida))
    print("Reel final em", saida)


if __name__ == "__main__":
    print("Use como módulo: import montar_reel_montagem", file=sys.stderr)
