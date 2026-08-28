"""Comprime as imagens pesadas da home (fotos + logos), preservando
transparência (RGBA). Reduz resolução para o necessário no uso real e
recomprime PNG otimizado.
"""
from pathlib import Path

from PIL import Image

PASTA = Path(r"C:\tmp\home_imgs")

# arquivo -> largura máxima alvo
ALVOS = {
    "hero-leticia-sem-fundo.png": 900,
    "leticia-sentada-removebg-preview.png": 700,
    "santiagopradoebarrosescritorioadvogadas.png": 900,
    "logo-800x800.png": 512,
    "logo-sem-fundo.png": 300,
}

for nome, largura_max in ALVOS.items():
    caminho = PASTA / nome
    tamanho_antes = caminho.stat().st_size
    img = Image.open(caminho)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    if img.width > largura_max:
        nova_altura = int(img.height * largura_max / img.width)
        img = img.resize((largura_max, nova_altura), Image.LANCZOS)
    img.save(caminho, "PNG", optimize=True)
    tamanho_depois = caminho.stat().st_size
    reducao = 100 * (1 - tamanho_depois / tamanho_antes)
    print(f"{nome}: {tamanho_antes//1024}KB -> {tamanho_depois//1024}KB ({reducao:.0f}% menor)")
