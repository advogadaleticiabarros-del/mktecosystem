"""Motor 3D dos Reels da Letícia (15/10/2026): mundo em miniatura (three.js, mundo.js) + camada 2D (pagina.html),
renderizado quadro a quadro no Chromium (WebGL por software) e codificado com o áudio tratado do motor v2.

Um roteiro (ex.: reel_6x1.py) monta o dicionário ROTEIRO (câmera, trilhas, capítulos, etiquetas, selos, números,
legendas, fechamento) e chama rodar(). Margens da Meta verificadas por código (window.checar) antes do render.
"""
import asyncio
import base64
import json
import subprocess
import sys
from pathlib import Path

from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "motor"))
FF = Path(r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe")
LOGO = Path(r"C:\Users\prosy\mktecosystem\apps\api\app\assets\logo-leticia.png")
FPS = 30
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def _uri(texto: str) -> str:
    return "data:text/javascript;base64," + base64.b64encode(texto.encode("utf-8")).decode()


def pagina(roteiro: dict) -> str:
    html = (AQUI / "pagina.html").read_text(encoding="utf-8")
    html = (html.replace("__THREE__", _uri((AQUI / "vendor" / "three.module.min.js").read_text(encoding="utf-8")))
                .replace("__ROOMENV__", _uri((AQUI / "vendor" / "RoomEnvironment.js").read_text(encoding="utf-8")))
                .replace("__MUNDO__", _uri((AQUI / "mundo.js").read_text(encoding="utf-8"))))
    r = {**roteiro, "logo": "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()}
    return html.replace("<head>", f"<head><script>window.ROTEIRO = {json.dumps(r, ensure_ascii=False)};</script>", 1)


async def _abrir(p, roteiro):
    nav = await p.chromium.launch(args=ARGS)
    pg = await nav.new_page(viewport={"width": 1080, "height": 1920})
    await pg.set_content(pagina(roteiro), wait_until="networkidle")
    await pg.wait_for_function("window.pronto === true", timeout=60000)
    await pg.evaluate("document.fonts.ready")
    return nav, pg


async def checar(roteiro: dict) -> list[str]:
    async with async_playwright() as p:
        nav, pg = await _abrir(p, roteiro)
        erros = []
        t = 0.0
        while t < roteiro["total"]:
            erros += await pg.evaluate(f"window.checar({t})")
            t += 0.25
        await nav.close()
    return erros


async def amostras(roteiro: dict, tempos: list[float], pasta: Path) -> list[Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    saida = []
    async with async_playwright() as p:
        nav, pg = await _abrir(p, roteiro)
        for t in tempos:
            await pg.evaluate(f"window.quadro({t})")
            arq = pasta / f"amostra_{t:05.2f}.jpg"
            await pg.screenshot(path=str(arq), type="jpeg", quality=88)
            saida.append(arq)
        await nav.close()
    return saida


async def video_mudo(roteiro: dict, destino: Path) -> None:
    total = roteiro["total"]
    n = int(total * FPS)
    proc = subprocess.Popen([str(FF), "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(destino)],
                            stdin=subprocess.PIPE)
    async with async_playwright() as p:
        nav, pg = await _abrir(p, roteiro)
        for i in range(n):
            await pg.evaluate(f"window.quadro({i / FPS})")
            proc.stdin.write(await pg.screenshot(type="jpeg", quality=92))
            if i % 150 == 0:
                print(f"  quadro {i}/{n}", flush=True)
        await nav.close()
    proc.stdin.close()
    proc.wait()


def juntar(video: Path, audio: Path, destino: Path) -> None:
    subprocess.run([str(FF), "-v", "error", "-y", "-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-shortest",
                    "-movflags", "+faststart", str(destino)], check=True)
