"""Aplica o acabamento dourado padrão nos 16 slides sem texto."""
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
OUT = BASE / "_saida_acho_chique_sem_texto"
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
            caminho = OUT / pasta / f"slide-{i}-sem-texto.png"
            aplicar(caminho)
            print(f"dourado aplicado: {caminho}")
