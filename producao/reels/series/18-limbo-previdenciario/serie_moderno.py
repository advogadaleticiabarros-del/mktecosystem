"""Limbo previdenciário 1/2 no motor moderno (10/11/2026), piloto do pedido da Jessica: "estão feios e mal editados...
preciso que seja mais moderno, com motions mais legais, transição de cenas de ângulos diferentes, mesclagem de imagens
sobre o assunto com a imagem da Dra. Letícia". Estilo: inteiro.
Fala: a mesma da validação premium (fontes/falas.py, "fala ok"); fatos e cortes no docstring de
series/18-limbo-previdenciario/montar_falas.py. Só o visual muda:
- cenas de rosto trocam de ângulo a cada emenda (close, lateral, médio);
- a Dra. em janela 3D com borda de ouro sobre o vídeo do assunto, e o assunto em janela ao lado dela;
- títulos palavra por palavra, legenda curta e maior, transições zoom-desfoque e giro 3D.
Uso: py serie.py 1 [--amostras | --checar]
"""
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, janela, kick, outro, pilula, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Limbo previdenciário", "corrige": {}, "leg_max": 16,
              "destaques": {"inapto", "inapto,", "alta,", "meses.", "empresa.", "benefício"}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.35) 0%, rgba(26,21,17,0) 14%, rgba(26,21,17,0) 46%, rgba(26,21,17,.55) 58%, rgba(26,21,17,.9) 100%)"
STOCK_VEU = "linear-gradient(180deg, rgba(26,21,17,.85) 0%, rgba(26,21,17,.55) 28%, rgba(26,21,17,.5) 55%, rgba(26,21,17,.9) 100%)"
DY, ZB = -200, 1.12
CORRIGE = {"médio": "médico", "de@18.02": "do", "INAP,": "inapto,", "tibio": "tipo", "vídeo": "perfil",
           "eu": "", "seu": "seus", "direito.": "direitos."}


def rosto(i, a, b, trans="corte", ang=None, els=()):
    bg = {**preparar_seq(f"r1_rosto{i}", "fala-r1", a, b - a + 0.4), "rosto": True, "kb": [ZB, ZB + .03, 0, 0, DY, DY - 20]}
    if ang:
        bg["ang"] = ang
    return {"a": a, "trans": trans, "bg": bg, "veu": FACE_VEU, "els": list(els)}


def assunto(i, a, b, stock, trans="corte", els=(), tdur=None):
    c = {"a": a, "trans": trans, "bg": {**preparar_seq(f"r1_stk{i}_{stock}", f"stock-{stock}", 0.3, b - a + 0.6), "kb": [1.0, 1.08, 0, 0, 0, -30]},
         "veu": STOCK_VEU, "els": list(els)}
    if tdur:
        c["tdur"] = tdur
    return c


def dra(i, a, b, at, x, y, w, h, ry):
    """A Dra. numa janela 3D (boca sincronizada com a voz: o quadro 1 é o início da cena)."""
    return janela(preparar_seq(f"r1_jan{i}", "fala-r1", a, b - a + 0.4), at, x, y, w, h, desde=a, rosto=True, ry=ry, zoom=1.75,
                  ry0=ry * 4, foco="50% 32%")


def tema(i, stock, at, dur, x, y, w, h, ry):
    return janela(preparar_seq(f"r1_tema{i}_{stock}", f"stock-{stock}", 0.5, dur + 0.6), at, x, y, w, h, ry=ry, ry0=ry * 4,
                  foco="50% 40%")


def chip(txt, at, w):
    return pilula(txt, at, 955, left=0, style=centro(w))


def titulo(html, at, top, size=74):
    return texto(html, at, top, size=size, align="center", anim="palavras")


def reel1(W, seg, fim):
    a1, a2, a3, a4, a5, a6, a7, a8 = (W("Limbo", 2.5), W("seja"), W("por", 13.5), W("e", 20.5), W("que", 25.5),
                                      W("E", 28.5), W("O", 35.8), W("Meu"))
    return [
        rosto(0, 0, a1, els=[titulo("Você sabe o que é|<em>limbo previdenciário?</em>", 0.05, 905, size=62)]),
        # a Dra. em janela sobre o trabalhador (zoom com desfoque: 1ª transição de destaque)
        assunto(1, a1, a2, "trabalhador", trans="zoomblur", tdur=.5, els=[
            kick("Limbo previdenciário", a1 + .1, top=190, left=0, style=centro(900)),
            titulo("Empregado <em>inapto</em>|para voltar ao trabalho", W("empregado"), 240, size=66),
            dra(1, a1, a2, a1 + .15, 100, 470, 540, 630, ry=9)]),
        rosto(2, a2, a3, els=[chip("Doença ou acidente", W("doença,"), 440)]),
        # o médico do trabalho em tela cheia, a Dra. numa janela menor
        assunto(3, a3, a4, "inapto", trans="whip", els=[
            kick("Um exemplo", a3 + .1, top=190, left=0, style=centro(900)),
            titulo("Médico do trabalho:|<em>inapto</em>", W("médico"), 240, size=80),
            dra(3, a3, a4, a3 + .35, 590, 600, 380, 470, ry=-10),
            carimbo("Inapto", W("inapto,"), 700, 130, size=88)]),
        # a Dra. à esquerda, o INSS (espera) numa janela à direita
        rosto(4, a4, a5, ang="lado", els=[
            tema(4, "espera", a4 + .2, a5 - a4, 570, 240, 410, 550, ry=-10),
            chip("INSS: alta", W("alta,"), 300)]),
        assunto(5, a5, a6, "recusa", trans="luz", els=[
            kick("No INSS", a5 + .05, top=190, left=0, style=centro(900)),
            titulo("Sem <em>benefício</em>", a5 + .1, 240, size=104),
            dra(5, a5, a6, a5 + .1, 440, 470, 540, 630, ry=-9)]),
        # giro 3D: 2ª transição de destaque
        assunto(6, a6, a7, "contas", trans="giro", tdur=.6, els=[
            kick("O limbo", a6 + .1, top=300, left=0, style=centro(900)),
            titulo("Nem o INSS,|<em>nem a empresa</em>", W("nem"), 360, size=88),
            carimbo("Sem salário", W("vindo"), 700, 250, size=84)]),
        rosto(7, a7, a8, els=[chip("Pode durar meses", W("muitas"), 440)]),
        rosto(8, a8, fim, els=[chip("Dra. Letícia Barros", a8 + .05, 520)]),
        outro(fim, "Parte 2 · Quem paga o salário", "quem está afastado pelo INSS"),
    ]


def _reel():
    fim = m.fim_da_fala(m.AQUI / "videos" / "fala-r1.transcricao.json", m.AQUI / "videos" / "fala-r1.mp4")
    return {"src": m.AQUI / "videos" / "fala-r1.mp4", "transcricao": m.AQUI / "videos" / "fala-r1.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": reel1, "serie": "Limbo previdenciário · 1/2",
            "prefixo": "limbo-previdenciario-moderno-", "corrige": CORRIGE}


REELS = {1: _reel()}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
