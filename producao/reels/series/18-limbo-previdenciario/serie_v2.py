"""Série 18 v2 (20/10/2026): Limbo previdenciário em 2 Reels, falas limpas (sem pausas longas nem repetições, 5% mais
rápidas) montadas em ../fontes/montar_falas_v2.py (fatos e cortes no docstring de montar_falas.py e de lá).
Pedido: "falas mais limpas, tirar as pausas e repetições, um pouco mais dinâmico, o segundo vídeo está travando".
O travamento da v1 era a cena "Mas ele não trabalhou" (11,9 s) sobre um vídeo do banco de 10 s: a imagem congelava
aos 33,6 s. Agora `corte()` recusa cena maior que o clipe.
Uso: py serie.py [1 2] [--amostras | --checar]
"""
import json
import subprocess
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, outro, pilula, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Limbo previdenciário", "corrige": {},
              "destaques": {"inapto", "inapto,", "alta,", "meses.", "empresa.", "errado.", "jurisprudência", "trabalhar."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.35) 0%, rgba(26,21,17,0) 14%, rgba(26,21,17,0) 46%, rgba(26,21,17,.55) 58%, rgba(26,21,17,.9) 100%)"
STOCK_VEU = "linear-gradient(180deg, rgba(26,21,17,.82) 0%, rgba(26,21,17,.5) 30%, rgba(26,21,17,.45) 55%, rgba(26,21,17,.88) 100%)"
DY = {1: -200, 2: -200}  # sobe o vídeo: o queixo fica acima da faixa de texto do peito
ZB = {1: 1.12, 2: 1.12}  # zoom-base (com 1.22 a testa saía cortada)
CORRIGE = {"inápito": "inapto", "inápito,": "inapto,", "as@8.54": "às", "que@32.36": "", "vídeo": "perfil", "eu": "",
           "mais@15.10": "", "veritária,": "majoritária,", "trabalhado.": "trabalhar.", "deitado.": "de atestado.",
           "seu": "seus", "direito.": "direitos."}
FFPROBE = str(m.FF).replace("ffmpeg.exe", "ffprobe.exe")


def duracao(stock):
    arq = next((m.AQUI / "videos").glob(f"stock-{stock}*.mp4"))
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def rosto(n, i, a, b, trans="corte", kb=(1.12, 1.16), els=(), **kw):
    dy, z = DY[n], ZB[n] - 1.12  # kb é relativo ao zoom-base do reel
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "kb": [kb[0] + z, kb[1] + z, 0, 0, dy, dy - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def corte(n, i, a, b, stock, trans="whip", els=(), **kw):
    precisa, tem = 0.3 + (b - a) + 0.4, duracao(stock)
    assert precisa <= tem, f"r{n} cena {i}: {precisa:.1f}s sobre o vídeo '{stock}' de {tem:.1f}s (a imagem congelaria)"
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_stk{i}_{stock}", f"stock-{stock}", 0.3, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": STOCK_VEU, "els": list(els), **kw}


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def reel1(W, seg, fim):
    """O que é limbo previdenciário."""
    a1, a2, a3, a4, a5, a6, a7, a8 = (W("Limbo", 2.5), W("seja"), W("por", 14.0), W("e", 21.3), W("que", 26.5),
                                      W("E", 30.0), W("O", 37.0), W("Meu"))
    return [
        rosto(1, 0, 0, a1, els=[texto("Você sabe o que é|<em>limbo previdenciário?</em>", 0.05, 905, size=62, align="center")]),
        corte(1, 1, a1, a2, "trabalhador", trans="whip", els=[
            kick("Limbo previdenciário", a1 + .05),
            texto("Empregado <em>inapto</em>|para voltar ao trabalho", W("empregado"), 480, size=74, align="center", anim="sobe")]),
        rosto(1, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chip("Doença ou acidente", W("doença,"), 440)]),
        corte(1, 3, a3, a4, "inapto", trans="whip", els=[
            kick("Um exemplo", a3 + .05),
            texto("Médico do trabalho:|<em>inapto</em>", W("médico"), 480, size=86, align="center", anim="sobe")]),
        rosto(1, 4, a4, a5, trans="whipV", kb=(1.14, 1.18), els=[chip("INSS: alta", W("alta,"), 300)]),
        corte(1, 5, a5, a6, "espera", trans="luz", els=[
            kick("No INSS", a5 + .05),
            texto("Sem <em>benefício</em>", W("benefício"), 520, size=96, align="center", anim="sobe")]),
        corte(1, 6, a6, a7, "contas", trans="tinta", tdur=.7, els=[
            kick("O limbo", a6 + .05),
            texto("Nem o INSS,|<em>nem a empresa</em>", W("nem"), 470, size=84, align="center", anim="sobe"),
            carimbo("Sem salário", W("empresa.", 35.0), 720, 250, size=84)]),
        rosto(1, 7, a7, a8, trans="whip", kb=(1.14, 1.18), els=[chip("Pode durar meses", W("muitas"), 440)]),
        rosto(1, 8, a8, fim, trans="corte", kb=(1.12, 1.16), els=[chip("Dra. Letícia Barros", a8 + .05, 520)]),
        outro(fim, "Parte 2 · Quem paga o salário", "quem está afastado pelo INSS"),
    ]


def reel2(W, seg, fim):
    """Quem paga o salário no limbo."""
    a1, a2, a3, a4, a5, a6 = W("É", 4.5), W("Quem", 11.0), W("Ah,"), W("Se", 23.3), W("Tem", 27.5), W("Meu")
    return [
        rosto(2, 0, 0, a1, els=[texto("Limbo previdenciário:|<em>quem paga o salário?</em>", 0.05, 905, size=60, align="center")]),
        corte(2, 1, a1, a2, "chefe", trans="whip", els=[
            kick("A responsabilidade", a1 + .05),
            texto("É da|<em>empresa</em>", a1 + .08, 480, size=110, align="center", anim="sobe"),
            pilula("A culpa não é do trabalhador", W("culpa"), 740, left=0, style=centro(680))]),
        rosto(2, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chip("Jurisprudência majoritária", W("jurisprudência"), 620)]),
        corte(2, 3, a3, a4, "recusa", trans="whip", els=[
            kick("O argumento da empresa", a3 + .05),
            texto("“Mas ele|<em>não trabalhou</em>”", a3 + .08, 470, size=90, align="center", anim="sobe"),
            carimbo("Errado", W("Errado."), 720, 330, size=96)]),
        rosto(2, 4, a4, a5, trans="tinta", tdur=.7, kb=(1.14, 1.18), els=[chip("Sem benefício: a empresa paga", W("benefício"), 680)]),
        corte(2, 5, a5, a6, "doente", trans="whipV", els=[
            kick("Mesmo sem trabalhar", a5 + .05),
            texto("Recebe como se|<em>estivesse de atestado</em>", W("Então"), 480, size=74, align="center", anim="sobe")]),
        rosto(2, 6, a6, fim, trans="luz", kb=(1.12, 1.16), els=[chip("Dra. Letícia Barros", a6 + .05, 520)]),
        outro(fim, "Parte 1 · O que é o limbo", "quem está afastado pelo INSS"),
    ]


def _reel(n, roteiro, serie, prefixo):
    d = json.load(open(m.AQUI / f"transcricao-r{n}.json", encoding="utf-8"))
    fim = max(w["end"] for s in d["segments"] for w in s["words"]) + 0.25
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / f"transcricao-r{n}.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Limbo previdenciário · 1/2", "limbo-previdenciario-v2-"),
    2: _reel(2, reel2, "Limbo previdenciário · 2/2", "limbo-previdenciario-v2-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
