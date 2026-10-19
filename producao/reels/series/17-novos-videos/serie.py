"""Série 17 (18/10/2026): 5 Reels a partir das gravações da Dra. Letícia em Desktop/novo video (a pasta "ja usou" não é
usada). Falas montadas em ../fontes/montar_falas.py (fatos, base legal e o que foi cortado no docstring de lá).
1 Pediu demissão? A multa do 477 também vale · 2 Conselhos da advogada · 3-5 Série Hora extra (quanto vale, banco de
horas, como provar). Padrão de 16/10/2026: visual limpo, textos no peito nas cenas de rosto, vídeos do banco nas cenas
sem a Dra. (escondem as emendas), cabeçalho e barra embaixo da legenda.
Uso: py serie.py [1 2 3 4 5] [--amostras | --checar]
"""
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, outro, pilula, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Direito Trabalhista", "corrige": {},
              "destaques": {"demissão", "477", "salário.", "domingos", "Prints", "50%", "100%", "acordo", "pagar.",
                            "seis", "testemunhal.", "WhatsApp", "print,"}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.35) 0%, rgba(26,21,17,0) 14%, rgba(26,21,17,0) 46%, rgba(26,21,17,.55) 58%, rgba(26,21,17,.9) 100%)"
STOCK_VEU = "linear-gradient(180deg, rgba(26,21,17,.82) 0%, rgba(26,21,17,.5) 30%, rgba(26,21,17,.45) 55%, rgba(26,21,17,.88) 100%)"
PEITO = 975
DY = {1: -335, 2: -120, 3: -335, 4: -335, 5: -335}  # sobe o vídeo: o queixo fica acima da faixa de texto (y~870)
ZB = {1: 1.27, 2: 1.12, 3: 1.27, 4: 1.27, 5: 1.27}  # zoom-base: cobre a borda ao subir (rosto grande nessas tomadas)


def rosto(n, i, a, b, trans="corte", kb=(1.12, 1.16), els=(), **kw):
    dy, z = DY[n], ZB[n] - 1.12  # kb é relativo ao zoom-base do reel
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "kb": [kb[0] + z, kb[1] + z, 0, 0, dy, dy - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def corte(n, i, a, b, stock, trans="whip", els=(), **kw):
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_stk{i}_{stock}", f"stock-{stock}", 0.3, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": STOCK_VEU, "els": list(els), **kw}


def chip(txt, at, w):
    return pilula(txt, at, PEITO, left=0, style=centro(w))


def chipb(txt, at, w):
    """Selo do peito mais baixo, para a tomada da hora extra (rosto grande): fica abaixo do queixo e acima da legenda."""
    return pilula(txt, at, 1005, left=0, style=centro(w))


def reel1(W, seg, fim):
    """Pediu demissão? A multa do 477 também vale."""
    a1, a2, a3, a4 = W("Se"), W("ainda"), W("estabelecido"), W("Meu")
    return [
        rosto(1, 0, 0, a1, els=[texto("Pediu demissão?|A <em>multa do 477</em> também vale", 0.05, 905, size=62, align="center")]),
        corte(1, 1, a1, a2, "saida-caixa", trans="whip", els=[
            kick("Prazo da rescisão", a1 + .05),
            texto("<em>10 dias</em> para pagar|e entregar os documentos", W("prazo"), 480, size=76, align="center", anim="sobe"),
            pilula("Vale também no pedido de demissão", W("pagamento"), 720, left=0, style=centro(760))]),
        rosto(1, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chip("Qualquer valor, no prazo", W("irrisório,"), 600)]),
        corte(1, 3, a3, a4, "documentos", trans="tinta", tdur=.7, els=[
            kick("CLT, art. 477", a3 + .05),
            texto("Atrasou?|Multa de <em>um salário</em>", a3 + .1, 480, size=84, align="center", anim="sobe"),
            carimbo("+ 1 salário", W("salário."), 720, 300, size=84)]),
        rosto(1, 4, a4, fim, trans="whip", kb=(1.14, 1.18), els=[chip("Dra. Letícia Barros", a4 + .05, 520)]),
        outro(fim, "Rescisão · CLT, art. 477", "quem vai pedir demissão"),
    ]


def reel2(W, seg, fim):
    """Conselhos da advogada (3 frases + cartões)."""
    p1, p2, p3, p4 = 4.80, 8.00, 11.78, 14.78  # emendas da montagem (fala, pausa, fala, pausa, fala)
    return [
        rosto(2, 0, 0, p1, els=[chip("Conselho da advogada", 0.05, 520),
                                texto("Treinamento no domingo|<em>é hora extra</em>", W("Treinamento"), 1030 - 250, size=60, align="center")]),
        corte(2, 1, p1, p2, "treinamento", trans="whip", els=[
            kick("Treinamento obrigatório", p1 + .05),
            texto("Conta como|<em>tempo de trabalho</em>", p1 + .1, 480, size=84, align="center", anim="sobe"),
            pilula("CLT, art. 4º", p1 + .9, 720, left=0, style=centro(300))]),
        rosto(2, 2, p2, p3, trans="luz", kb=(1.16, 1.2), els=[chip("Dica do dia", W("Dica") + .05, 360)]),
        corte(2, 3, p3, p4, "celular-escritorio", trans="tinta", tdur=.7, els=[
            kick("Guarde tudo", p3 + .05),
            texto("Mensagens e e-mails|<em>valem como prova</em>", p3 + .1, 480, size=80, align="center", anim="sobe"),
            pilula("Convocações, escalas e horários", p3 + .9, 720, left=0, style=centro(740))]),
        rosto(2, 4, p4, fim, trans="whip", kb=(1.14, 1.18), els=[chip("Conselho de advogado", W("Conselho", 14.0) + .05, 520)]),
        outro(fim, "Conselhos da Dra. Letícia", "quem precisa ouvir isso"),
    ]


def reel3(W, seg, fim):
    """Hora extra 1/3: quanto vale."""
    a1, a2, a3, a4 = W("Muitos"), W("E", 11.0), W("Se", 16.0), W("Aos")
    return [
        rosto(3, 0, 0, a1, els=[texto("Hora extra:|<em>quanto vale?</em>", 0.05, 905, size=72, align="center")]),
        corte(3, 1, a1, a2, "noite-trabalho", trans="whip", els=[
            kick("Hora extra · 1/3", a1 + .05),
            texto("Muita gente|<em>perde dinheiro</em>", a1 + .1, 520, size=92, align="center", anim="sobe")]),
        rosto(3, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chipb("+ 50% sobre a hora", W("Vai") + .05, 480)]),
        corte(3, 3, a3, a4, "calculadora", trans="tinta", tdur=.7, els=[
            kick("Exemplo", a3 + .05),
            texto("Hora normal: <em>R$ 50</em>", a3 + .1, 460, size=78, align="center", anim="sobe"),
            texto("Hora extra: <em>R$ 75</em>", W("25"), 600, size=78, align="center", anim="sobe"),
            pilula("Em dias comuns: + 50%", W("comuns,"), 760, left=0, style=centro(460))]),
        rosto(3, 4, a4, fim, trans="whip", kb=(1.14, 1.18), els=[chipb("Domingo e feriado: 100%", W("domingos") + .05, 620)]),
        outro(fim, "Parte 2 · Banco de horas", "quem faz hora extra"),
    ]


def reel4(W, seg, fim):
    """Hora extra 2/3: banco de horas."""
    a1, a2, a3 = W("Caso"), W("Esse", 12.0), W("Até")
    return [
        rosto(4, 0, 0, a1, els=[texto("Banco de horas|<em>tem regra</em>", 0.05, 905, size=72, align="center"),
                                ]),
        corte(4, 1, a1, a2, "agenda", trans="whip", els=[
            kick("Hora extra · 2/3", a1 + .05),
            texto("Sem acordo,|<em>a empresa paga</em>", a1 + .1, 460, size=86, align="center", anim="sobe"),
            pilula("Acordo individual: até 6 meses", W("convenção"), 680, left=0, style=centro(720)),
            pilula("Convenção coletiva: até 1 ano", W("convenção") + .4, 770, left=0, style=centro(700))]),
        rosto(4, 2, a2, a3, trans="luz", kb=(1.16, 1.2), els=[chipb("Você tem direito ao extrato", W("demonstrativo") + .05, 660)]),
        corte(4, 3, a3, fim, "relogio", trans="tinta", tdur=.7, els=[
            kick("Prazo para compensar", a3 + .05),
            texto("<em>6 meses</em> no acordo|individual", W("seis"), 480, size=84, align="center", anim="sobe"),
            pilula("Não compensou? Paga como extra", W("folga"), 720, left=0, style=centro(700))]),
        outro(fim, "Parte 3 · Como provar", "quem faz hora extra"),
    ]


def reel5(W, seg, fim):
    """Hora extra 3/3: não bate ponto? Como provar."""
    a1, a2, a3, a4, a5, a6 = W("existe"), W("Algum"), W("Outra"), W("Geralmente"), W("É", 40.0), W("E", 50.0)
    return [
        rosto(5, 0, 0, a1, els=[texto("Não bate ponto?|<em>Como provar</em> hora extra", 0.05, 905, size=62, align="center")]),
        rosto(5, 1, a1, a2, trans="luz", kb=(1.16, 1.2), els=[chipb("Prova testemunhal", W("testemunhal.") , 420)]),
        corte(5, 2, a2, a3, "colegas", trans="whip", els=[
            kick("Hora extra · 3/3", a2 + .05),
            texto("Colega que <em>vê</em>|o seu horário", a2 + .1, 480, size=86, align="center", anim="sobe"),
            pilula("1 · Testemunha", a2 + .9, 720, left=0, style=centro(360))]),
        rosto(5, 3, a3, a4, trans="tinta", tdur=.7, kb=(1.14, 1.18), els=[chipb("2 · Prints", W("print,"), 300)]),
        corte(5, 4, a4, a5, "celular-rua", trans="whip", els=[
            kick("Registre tudo", a4 + .05),
            texto("Convocação, entrada|<em>e saída</em>", a4 + .1, 480, size=82, align="center", anim="sobe"),
            pilula("WhatsApp, e-mail e fotos", W("registrado"), 720, left=0, style=centro(600))]),
        rosto(5, 5, a5, a6, trans="luz", kb=(1.16, 1.2), els=[chipb("Vale como prova no processo", W("anexar"), 680)]),
        rosto(5, 6, a6, fim, trans="whip", kb=(1.12, 1.16), els=[chipb("Dra. Letícia Barros", W("Meu") + .05, 520)]),
        outro(fim, "Série Hora extra · 3/3", "quem faz hora extra"),
    ]


def _reel(n, roteiro, serie, prefixo):
    import json
    d = json.load(open(m.AQUI / f"transcricao-r{n}.json", encoding="utf-8"))
    fim = max(w["end"] for s in d["segments"] for w in s["words"]) + 0.25
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / f"transcricao-r{n}.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo}


REELS = {
    1: _reel(1, reel1, "Rescisão · art. 477", "multa-477-pedido-demissao-"),
    2: _reel(2, reel2, "Conselhos da advogada", "conselhos-advogada-"),
    3: _reel(3, reel3, "Hora extra · 1/3", "hora-extra-"),
    4: _reel(4, reel4, "Hora extra · 2/3", "hora-extra-"),
    5: _reel(5, reel5, "Hora extra · 3/3", "hora-extra-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
