"""Clipes 3D curtos e sem textos, para entrar como cena de fundo no motor 2D dos Reels (26/10/2026).
A skill leticia-reels-premium pede 3D em 1 ou 2 momentos de destaque; este gerador reaproveita o mundo em miniatura
de mundo.js (semana, cofre com moedas, papéis...) com a câmera de cada clipe e esconde a camada 2D (cabeçalho,
legenda, selos), que no Reel vem do engine.html.

Uso: py clip3d.py <destino_dir> <clipe> [...] [--amostras]
     grava <destino_dir>/stock-3d-<clipe>.mp4 (1080x1920, 30 fps, mudo); o motor 2D usa como corte(..., "3d-<clipe>").
"""
import asyncio
import sys
from pathlib import Path

import motor3d as m3

# câmeras do mundo (posição x, y, z e alvo x, y, z), as mesmas da série 6x1
LONGE = [7, 10.5, 29, 0.3, 2.2, 0]   # alvo acima dos objetos: eles descem para o meio do quadro (o topo fica sob o véu)
SEM = [4.5, 7.5, 21, 0.3, 2.0, 0]
SEM_PERTO = [2.5, 5.2, 15, 0.3, 1.6, 0]
COFRE = [-5.2, 6.5, 15, -8.0, 1.6, 0]
COFRE_PERTO = [-6.6, 4.4, 10.5, -8.0, 1.2, 0]

_PARADO = {"semana_sobe": [[0, 1]], "horas": [[0, 1]], "sabado_folga": [[0, 0]], "carimbo_vis": [[0, 0]],
           "carimbo": [[0, 0]], "livro_abre": [[0, 0]], "assina": [[0, 0]], "moedas": [[0, 0]], "papeis": [[0, 0]]}

CLIPES = {
    # a semana de trabalho se ergue e a câmera chega perto: convocação, dias de trabalho
    "semana": {"total": 8.0, "camera": [[0, LONGE], [1.8, SEM], [8.0, SEM_PERTO]],
               "trilhas": {"semana_sobe": [[0.1, 0], [1.6, 1]]}},
    # moedas caindo no cofre: o FGTS depositado
    "cofre": {"total": 6.0, "camera": [[0, COFRE], [6.0, COFRE_PERTO]],
              "trilhas": {"moedas": [[0.3, 0], [3.8, 1]]}},
}


def roteiro(nome: str) -> dict:
    c = CLIPES[nome]
    return {"tema": "", "total": c["total"], "camera": c["camera"], "trilhas": {**_PARADO, **c["trilhas"]},
            "capitulos": [], "callouts": [], "selos": [], "numeros": [], "legendas": [],
            "fechamento": {"a": c["total"] + 99, "titulo": ""}}


_pagina = m3.pagina
m3.pagina = lambda r: _pagina(r).replace("</head>", "<style>#camada,#fio{display:none!important}</style></head>", 1)


def main(argv) -> int:
    destino, nomes = Path(argv[0]), [a for a in argv[1:] if not a.startswith("--")]
    destino.mkdir(parents=True, exist_ok=True)
    for nome in nomes:
        r = roteiro(nome)
        if "--amostras" in argv:
            for f in asyncio.run(m3.amostras(r, [0.5, r["total"] / 2, r["total"] - 0.2], destino / f"amostras-3d-{nome}")):
                print(f)
        else:
            arq = destino / f"stock-3d-{nome}.mp4"
            asyncio.run(m3.video_mudo(r, arq))
            print("ok", arq)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
