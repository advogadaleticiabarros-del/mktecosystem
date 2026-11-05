"""Tira marca, texto em inglês e dados impressos das fotos (regra: sem marca de terceiros). Grava em fotos/ (fora do git)."""
from pathlib import Path

import cv2
import numpy as np

AQUI = Path(__file__).resolve().parent
BANCO = AQUI.parents[2] / "apps" / "api" / "_saida_producao_1510" / "_fotos_pexels"
# foto de origem: (arquivo novo, áreas x0, y0, x1, y1)
RETOQUES = {
    "31103955.jpg": ("relogio-sem-marca.png", [(552, 628, 660, 662), (558, 830, 638, 858)]),
    "32592295.jpg": ("ultrassom-sem-dados.png", [(231, 559, 482, 581), (455, 581, 482, 680)]),
}

(AQUI / "fotos").mkdir(exist_ok=True)
for origem, (novo, areas) in RETOQUES.items():
    im = cv2.imread(str(BANCO / origem))
    mascara = np.zeros(im.shape[:2], np.uint8)
    for x0, y0, x1, y1 in areas:
        mascara[y0:y1, x0:x1] = 255
    cv2.imwrite(str(AQUI / "fotos" / novo), cv2.inpaint(im, mascara, 5, cv2.INPAINT_TELEA))
