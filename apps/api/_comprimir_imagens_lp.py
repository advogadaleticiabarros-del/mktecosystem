"""Comprime as imagens de hero das LPs para melhorar performance (PageSpeed),
mantendo qualidade visual. Redimensiona para no máximo 1920px de largura
(suficiente para background-size:cover em qualquer tela) e recomprime em
JPEG qualidade 78.
"""
from pathlib import Path

from PIL import Image

PASTA = Path(r"C:\Users\prosy\blogautomaticoleticia\assets\images\lp")
LARGURA_MAX = 1920
QUALIDADE = 78

for arquivo in sorted(PASTA.glob("*.jpg")):
    tamanho_antes = arquivo.stat().st_size
    img = Image.open(arquivo).convert("RGB")
    if img.width > LARGURA_MAX:
        nova_altura = int(img.height * LARGURA_MAX / img.width)
        img = img.resize((LARGURA_MAX, nova_altura), Image.LANCZOS)
    img.save(arquivo, "JPEG", quality=QUALIDADE, optimize=True)
    tamanho_depois = arquivo.stat().st_size
    reducao = 100 * (1 - tamanho_depois / tamanho_antes)
    print(f"{arquivo.name}: {tamanho_antes//1024}KB -> {tamanho_depois//1024}KB ({reducao:.0f}% menor)")
