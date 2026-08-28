"""Aplica só as barras de acabamento dourado (topo/rodapé) por cima dos
slides Acho Chique já renderizados, sem mexer em mais nada."""
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
OUT = BASE / "_saida_acho_chique"
ACABAMENTO = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\ementos rdape dourado\cabeçalho e rodape.png")


def aplicar(caminho_png: Path) -> None:
    base = Image.open(caminho_png).convert("RGBA")
    acabamento = Image.open(ACABAMENTO).convert("RGBA")
    if acabamento.size != base.size:
        acabamento = acabamento.resize(base.size)
    composto = Image.alpha_composite(base, acabamento)
    composto.convert("RGB").save(caminho_png)


if __name__ == "__main__":
    for pasta in ["trabalhista", "familia"]:
        for i in range(1, 9):
            caminho = OUT / pasta / f"slide-{i}.png"
            aplicar(caminho)
            print(f"dourado aplicado: {caminho}")
