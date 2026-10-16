"""Reels "5 coisas que a empresa não pode fazer com a gestante" (16/10/2026), a partir da gravação fragmentada da
Dra. Letícia (7 partes, PROJETOS/ecosystemmkt/BANCO IMAGENS/Advogada/videos Leticia). Um Reels só, ~41 s.
Fala montada em ../fontes/montar_fala.py (fatos e base legal no docstring de lá; "ou perigoso" cortado).
Padrão de 16/10/2026: visual limpo, textos no peito nas cenas de rosto (nunca na testa), vídeos do banco nas cenas
sem a Dra. (também escondem as emendas entre as partes), cabeçalho e barra embaixo da legenda.
Uso: py serie.py [1] [--amostras | --checar]
"""
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, outro, pilula, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({
    "src": m.AQUI / "videos" / "fala-r1.mp4",
    "serie": "Gestante · 5 coisas",
    "corrige": {"pré": "pré-natal", "-natal": ""},
    "destaques": {"cinco", "demitida", "justa", "salário", "insalubre.", "pré-natal", "atestados", "sindicato."},
})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.35) 0%, rgba(26,21,17,0) 14%, rgba(26,21,17,0) 46%, rgba(26,21,17,.55) 58%, rgba(26,21,17,.9) 100%)"
STOCK_VEU = "linear-gradient(180deg, rgba(26,21,17,.82) 0%, rgba(26,21,17,.5) 30%, rgba(26,21,17,.45) 55%, rgba(26,21,17,.88) 100%)"
PEITO = 975  # pílulas nas cenas de rosto: no peito, abaixo do queixo


DY = -190  # nesta gravação o rosto fica baixo no quadro: sobe o vídeo para o rosto ficar no terço de cima e o peito livre


def rosto(i, a, b, trans="corte", kb=(1.14, 1.18), els=(), **kw):
    """Cena com o rosto da Dra. nítido, em sincronia com a fala. Zoom de 1,14 ou mais para não abrir borda ao subir."""
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"rosto{i}", "fala-r1", a, b - a + 0.4), "kb": [kb[0], kb[1], 0, 0, DY, DY - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def corte(i, a, b, stock, trans="whip", els=(), **kw):
    """Cena sem a Dra.: vídeo do banco ligado ao assunto, com véu para os textos. Créditos em ../fontes/creditos-pexels.txt."""
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"stk_{stock}_{i}", f"stock-{stock}", 0.3, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": STOCK_VEU, "els": list(els), **kw}


def reel1(W, seg, fim):
    p2, p3, p4 = W("Você", 3.5), W("Não", 9.5), W("Você", 14.0)
    p5, p6, p7 = W("A", 17.0), W("E", 26.0), W("Meu")
    return [
        rosto(0, 0, p2, els=[
            texto("5 coisas que a empresa|<em>não pode</em> fazer", 0.05, 880, size=66, align="center")]),
        rosto(1, p2, W("a", 7.0), trans="whip", kb=(1.18, 1.22), els=[
            pilula("1 · Demissão", W("demitida"), PEITO, left=0, style=centro(380))]),
        corte(2, W("a", 7.0), p3, "gestante-sofa", trans="luz", els=[
            kick("1 · Estabilidade da gestante", W("a", 7.0) + .05),
            texto("Só por <em>justa causa</em>", W("a", 7.0) + .1, 520, size=96, align="center", anim="sobe"),
            pilula("Da gravidez até 5 meses após o parto", W("causa.") + .2, 720, left=0, style=centro(720))]),
        rosto(3, p3, W("seus"), trans="whip", kb=(1.14, 1.18), els=[
            pilula("2 · Salário e direitos", W("reduzir"), PEITO, left=0, style=centro(520))]),
        corte(4, W("seus"), p4, "calculadora", trans="tinta", tdur=.7, els=[
            kick("2 · Salário e direitos", W("seus") + .05),
            texto("Salário <em>reduzido</em>?", W("seus") + .1, 480, size=92, align="center", anim="sobe"),
            carimbo("Proibido", W("gravidez."), 720, 330, size=96)]),
        corte(5, p4, p5, "insalubre-mascara", trans="whip", els=[
            kick("3 · Ambiente insalubre", p4 + .05),
            texto("Grávida <em>fora</em>|do insalubre", p4 + .1, 480, size=90, align="center", anim="sobe"),
            pilula("Sem perder o salário", W("insalubre.") + .1, 720, left=0, style=centro(480))]),
        rosto(6, p5, W("consultas,"), trans="luz", kb=(1.18, 1.22), els=[
            pilula("4 · Pré-natal", W("impedir"), PEITO, left=0, style=centro(360))]),
        corte(7, W("consultas,"), p6, "ultrassom", trans="whip", els=[
            kick("4 · Pré-natal", W("consultas,") + .05),
            texto("Consultas e exames|<em>sem desconto</em>", W("consultas,") + .1, 480, size=84, align="center", anim="sobe"),
            pilula("No mínimo 6 consultas", W("pré-natal"), 720, left=0, style=centro(480)),
            pilula("Atestado médico não tem cota", W("atestados"), 820, left=0, style=centro(600))]),
        rosto(8, p6, W("pedido"), trans="tinta", tdur=.7, kb=(1.14, 1.18), els=[
            pilula("5 · Pedido de demissão", W("aceitar"), PEITO, left=0, style=centro(540))]),
        corte(9, W("pedido"), p7, "assinatura", trans="whip", els=[
            kick("5 · Pedido de demissão", W("pedido") + .05),
            texto("Só vale com o|<em>sindicato</em>", W("desacompanhada"), 480, size=96, align="center", anim="sobe"),
            pilula("CLT, art. 500", W("sindicato.") + .1, 720, left=0, style=centro(300))]),
        rosto(10, p7, fim, trans="luz", kb=(1.16, 1.2), els=[
            pilula("Dra. Letícia Barros", p7 + .05, PEITO, left=0, style=centro(520))]),
        outro(fim, "Direitos da gestante · CLT", "uma gestante", gestante=True),
    ]


REELS = {1: {"src": m.AQUI / "videos" / "fala-r1.mp4", "transcricao": m.AQUI / "transcricao-r1.json",
             "trechos": [(0.0, 37.47)], "roteiro": reel1, "prefixo": "gestante-5-coisas-", "serie": "Gestante · 5 coisas"}}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
