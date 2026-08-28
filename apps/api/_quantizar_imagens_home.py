"""Segunda passada: quantiza as PNGs já redimensionadas para reduzir
ainda mais o peso, mantendo transparência e qualidade visual (256 cores
com dithering é imperceptível em fotos/logos como estes).
"""
from pathlib import Path

from PIL import Image

PASTA = Path(r"C:\tmp\home_imgs")
ARQUIVOS = [
    "hero-leticia-sem-fundo.png",
    "leticia-sentada-removebg-preview.png",
    "santiagopradoebarrosescritorioadvogadas.png",
    "logo-800x800.png",
    "logo-sem-fundo.png",
]

for nome in ARQUIVOS:
    caminho = PASTA / nome
    tamanho_antes = caminho.stat().st_size
    img = Image.open(caminho).convert("RGBA")
    quant = img.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    quant.save(caminho, "PNG", optimize=True)
    tamanho_depois = caminho.stat().st_size
    reducao = 100 * (1 - tamanho_depois / tamanho_antes)
    print(f"{nome}: {tamanho_antes//1024}KB -> {tamanho_depois//1024}KB ({reducao:.0f}% menor)")
