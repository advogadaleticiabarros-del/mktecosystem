"""Série 18 (20/10/2026): Limbo previdenciário em 2 Reels, a partir da gravação da Dra. Letícia (Downloads/IMG_0330.MOV).
Falas montadas em ../fontes/montar_falas.py (fatos, base legal e o que foi cortado no docstring de lá).
1 O que é limbo previdenciário · 2 Quem paga o salário no limbo. Padrão da série 17: visual limpo, textos no peito nas
cenas de rosto, vídeos do banco nas cenas sem a Dra. (escondem as emendas), cabeçalho e barra embaixo da legenda.
Uso: py serie.py [1 2] [--amostras | --checar]
"""
import json
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, outro, pilula, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Limbo previdenciário", "corrige": {},
              "destaques": {"inapto", "inapto.", "alta,", "meses.", "empresa.", "errado.", "jurisprudência", "trabalhar."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.35) 0%, rgba(26,21,17,0) 14%, rgba(26,21,17,0) 46%, rgba(26,21,17,.55) 58%, rgba(26,21,17,.9) 100%)"
STOCK_VEU = "linear-gradient(180deg, rgba(26,21,17,.82) 0%, rgba(26,21,17,.5) 30%, rgba(26,21,17,.45) 55%, rgba(26,21,17,.88) 100%)"
DY = {1: -200, 2: -200}  # sobe o vídeo: o queixo fica acima da faixa de texto do peito
ZB = {1: 1.12, 2: 1.12}  # zoom-base: cobre a borda ao subir
CORRIGE = {"inapito": "inapto", "inapito.": "inapto.", "seu": "seus", "direito.": "direitos.", "vídeo": "perfil", "eu": "",
           "deatestado.": "de atestado.", "por@29.48": "pro"}


def rosto(n, i, a, b, trans="corte", kb=(1.12, 1.16), els=(), **kw):
    dy, z = DY[n], ZB[n] - 1.12  # kb é relativo ao zoom-base do reel
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "kb": [kb[0] + z, kb[1] + z, 0, 0, dy, dy - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def corte(n, i, a, b, stock, trans="whip", els=(), **kw):
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_stk{i}_{stock}", f"stock-{stock}", 0.3, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": STOCK_VEU, "els": list(els), **kw}


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def reel1(W, seg, fim):
    """O que é limbo previdenciário."""
    a1, a2, a3, a4, a5, a6, a7 = W("Limbo", 3.0), W("por", 16.0), W("e", 21.9), W("E", 26.0), W("E", 36.0), W("O", 44.0), W("Meu")
    return [
        rosto(1, 0, 0, a1, els=[texto("Você sabe o que é|<em>limbo previdenciário?</em>", 0.05, 905, size=62, align="center")]),
        corte(1, 1, a1, a2, "trabalhador", trans="whip", els=[
            kick("Limbo previdenciário", a1 + .05),
            texto("Empregado <em>inapto</em>|para voltar ao trabalho", W("empregado"), 480, size=74, align="center", anim="sobe"),
            pilula("Por doença ou acidente", W("doença,"), 720, left=0, style=centro(560))]),
        rosto(1, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chip("Um exemplo", a2 + .05, 320)]),
        corte(1, 3, a3, a4, "inapto", trans="whip", els=[
            kick("Médico do trabalho", a3 + .05),
            texto("Atestado:|<em>inapto</em>", W("atestado"), 500, size=96, align="center", anim="sobe")]),
        rosto(1, 4, a4, a5, trans="luz", kb=(1.14, 1.18), els=[chip("INSS: alta, sem benefício", W("alta,"), 600)]),
        corte(1, 5, a5, a6, "contas", trans="tinta", tdur=.7, els=[
            kick("O limbo", a5 + .05),
            texto("Nem o INSS paga,|<em>nem a empresa</em>", W("nem"), 470, size=80, align="center", anim="sobe"),
            carimbo("Sem salário", W("pagando."), 720, 250, size=84)]),
        rosto(1, 6, a6, a7, trans="whip", kb=(1.14, 1.18), els=[chip("Pode durar meses", W("muitas"), 440)]),
        rosto(1, 7, a7, fim, trans="corte", kb=(1.12, 1.16), els=[chip("Dra. Letícia Barros", a7 + .05, 520)]),
        outro(fim, "Parte 2 · Quem paga o salário", "quem está afastado pelo INSS"),
    ]


def reel2(W, seg, fim):
    """Quem paga o salário no limbo."""
    a1, a2, a3, a4, a5, a6 = W("É", 5.0), W("Quem", 14.0), W("A", 23.6), W("Se", 35.5), W("Tem", 40.5), W("Meu")
    return [
        rosto(2, 0, 0, a1, els=[texto("Limbo previdenciário:|<em>quem paga o salário?</em>", 0.05, 905, size=60, align="center")]),
        corte(2, 1, a1, a2, "empresa", trans="whip", els=[
            kick("A responsabilidade", a1 + .05),
            texto("É da|<em>empresa</em>", a1 + .08, 480, size=110, align="center", anim="sobe"),
            pilula("A culpa não é do trabalhador", W("culpa"), 740, left=0, style=centro(680))]),
        rosto(2, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chip("Jurisprudência majoritária", W("jurisprudência"), 620)]),
        corte(2, 3, a3, a4, "recusa", trans="whip", els=[
            kick("O argumento da empresa", a3 + .05),
            texto("“Mas ele|<em>não trabalhou</em>”", W("Ah,"), 470, size=90, align="center", anim="sobe"),
            carimbo("Errado", W("Errado."), 720, 330, size=96)]),
        rosto(2, 4, a4, a5, trans="tinta", tdur=.7, kb=(1.14, 1.18), els=[chip("Sem benefício: a empresa paga", W("benefício"), 680)]),
        corte(2, 5, a5, a6, "doente", trans="whip", els=[
            kick("Mesmo sem trabalhar", a5 + .05),
            texto("Recebe como se|<em>estivesse de atestado</em>", W("Então,"), 480, size=74, align="center", anim="sobe")]),
        rosto(2, 6, a6, fim, trans="luz", kb=(1.12, 1.16), els=[chip("Dra. Letícia Barros", a6 + .05, 520)]),
        outro(fim, "Parte 1 · O que é o limbo", "quem está afastado pelo INSS"),
    ]


def _reel(n, roteiro, serie, prefixo):
    d = json.load(open(m.AQUI / f"transcricao-r{n}.json", encoding="utf-8"))
    fim = max(w["end"] for s in d["segments"] for w in s["words"]) + 0.25
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / f"transcricao-r{n}.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Limbo previdenciário · 1/2", "limbo-previdenciario-"),
    2: _reel(2, reel2, "Limbo previdenciário · 2/2", "limbo-previdenciario-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
