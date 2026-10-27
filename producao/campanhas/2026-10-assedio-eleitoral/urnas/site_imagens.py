"""Imagens do site com a urna (27/10/2026): fundo do topo da LP (só a urna, dedo no CONFIRMA à direita, que é o lado
visível sob o véu e no celular) e capa do artigo em díptico (urna à esquerda, trabalhador com a caixa à direita, fio
dourado no meio). As imagens antigas ficam no servidor (LP: arquivo novo; capa: backup antes de trocar).
Uso: py site_imagens.py  → ../blog-lp/lp-demissao-voto-urna.jpg e ../blog-lp/capa-blog-urna.jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw

import urnas

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI.parent / "blog-lp"


def abrir(chave: str) -> Image.Image:
    return Image.open(urnas.FOTOS / urnas.URNAS[chave][0]).convert("RGB")


def cortar(im: Image.Image, w: int, h: int, fx: float, fy: float) -> Image.Image:
    W, H = im.size
    p = w / h
    cw, ch = (W, W / p) if W / H < p else (H * p, H)
    x0 = min(max(fx * W - cw / 2, 0), W - cw)
    y0 = min(max(fy * H - ch / 2, 0), H - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)


def main() -> None:
    lp = cortar(abrir("confirma"), 1600, 1000, 0.6, 0.5)
    lp.save(SAIDA / "lp-demissao-voto-urna.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    capa = Image.new("RGB", (1200, 630))
    capa.paste(cortar(abrir("confirma"), 600, 630, 0.74, 0.5), (0, 0))
    trab = Image.open(urnas.FOTOS / "original-assedio-eleitoral-voto.jpg").convert("RGB")
    capa.paste(cortar(trab, 600, 630, 0.5, 0.3), (600, 0))
    ImageDraw.Draw(capa).rectangle((597, 0, 602, 630), fill="#C9A962")
    capa.save(SAIDA / "capa-blog-urna.jpg", "JPEG", quality=88)
    print("ok")


if __name__ == "__main__":
    main()
