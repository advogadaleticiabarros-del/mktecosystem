"""Série "Guarda compartilhada x unilateral" em 3 Reels (15/10/2026), pedido de ajuste da Letícia no Orbit sobre o
Reels 04 do acervo: "editar como os outros do padrão, com o motor novo, efeitos sonoros que não atrapalhem a fala,
mais moderno e dinâmico, pode dividir em partes".
Base: gravações 4K de 15/08/2025 (rosto real dela), trechos em ../fontes/montar_falas.py. Motor v2 com o vídeo dela
como fundo das cenas de rosto e cenas de corte (rosto desfocado + véu) para os gráficos.
Fatos: CC arts. 1.583 e 1.584 (guarda compartilhada como regra; unilateral quando um dos pais não pode ou não quer;
o outro mantém convivência e o dever de supervisionar); ECA e CF art. 227 (proteção integral, melhor interesse).
Cortado de propósito: "ele perde o direito de opinar" (impreciso: na unilateral o outro supervisiona, CC 1.583 §5º) e
falas de bastidor do fim da tomada limpa.
Uso: py serie.py [1 2 3] [--amostras | --checar]
"""
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, no, outro, pilula, po, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({
    "src": m.AQUI / "videos" / "fala-r1.mp4",
    "serie": "Guarda dos filhos",
    "corrige": {"vê": "vê-lo.", "-lo.": "", "bem": "bem-estar", "-estar": "", "até": "tem"},
    "destaques": {"compartilhada,", "unilateral,", "simples", "regra", "decisões,", "dois", "ambos", "um", "responsável",
                  "visitas,", "convivência,", "assistidas", "pai,", "mãe,", "nunca,", "exceções", "específicos.",
                  "bem-estar", "extremamente", "danosos", "juiz", "ministério", "psicólogos", "doutora?"},
})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.55) 0%, rgba(26,21,17,0) 18%, rgba(26,21,17,0) 52%, rgba(26,21,17,.55) 62%, rgba(26,21,17,.9) 100%)"
CORTE_VEU = "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.62) 45%, rgba(26,21,17,.92))"


def rosto(n, i, a, b, trans="corte", kb=(1.0, 1.06), els=(), dy=0, **kw):
    """Cena com o rosto da Letícia nítido (vídeo dela em sincronia com a fala). Textos só na altura do peito."""
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "kb": [kb[0], kb[1], 0, dy, 0, dy - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def corte(n, i, a, b, trans="whip", els=(), **kw):
    """Cena de corte: o vídeo dela continua por trás, desfocado e escurecido; os gráficos ficam na frente."""
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_corte{i}", f"fala-r{n}", a, b - a + 0.4), "blur": 8, "kb": [1.08, 1.14, 0, 0, 0, 0]},
            "veu": CORTE_VEU, "els": list(els), **kw}


PEITO = 975  # pílulas nas cenas de rosto ficam no peito, longe do rosto (y 380–900)


def reel1(W, seg, fim):
    """1/3 · Compartilhada x unilateral: quem decide."""
    return [
        rosto(1, 0, 0, W("Na"), els=[
            carimbo("Mais simples", W("simples"), 965, 290, rot=-6, size=70)]),
        corte(1, 1, W("Na"), W("Ambos"), trans="whip", els=[
            kick("Guarda compartilhada", W("Na") + .05),
            po("A regra", W("regra"), 540, 560, size=210),
            texto("Decisões <em>divididas</em>", W("decisões,"), 760, size=88, align="center", anim="sobe"),
            no("Mãe", W("dois"), 330, top=930), no("Pai", W("pais."), 750, top=930)]),
        rosto(1, 2, W("Ambos"), W("Já"), trans="luz", kb=(1.04, 1.1), els=[
            pilula("Os dois participam", W("Ambos") + .1, PEITO, left=0, style=centro(560))]),
        corte(1, 3, W("Já"), fim, trans="tinta", tdur=.7, els=[
            kick("Guarda unilateral", W("Já") + .05),
            po("1", W("um"), 540, 520, size=300),
            texto("<em>um</em> dos pais decide", W("responsável"), 760, size=80, align="center", anim="sobe"),
            carimbo("A exceção", W("decisões", W("um")), 900, 330, rot=-6, size=76)]),
        outro(fim, "Parte 2 · Não deixa de ser pai", "quem está se separando", area="Direito de Família"),
    ]


def reel2(W, seg, fim):
    """2/3 · Na unilateral, o outro não deixa de ser pai."""
    return [
        corte(2, 0, 0, W("visitas,"), trans="corte", els=[
            kick("Quem não tem a guarda", 0.05),
            texto("<em>Perde</em>|o filho?", 0.08, 430, size=140)]),
        rosto(2, 1, W("visitas,"), W("às"), trans="whip", els=[
            pilula("Visitas", W("visitas,") + .05, PEITO, left=190, style={"fontSize": "40px"}),
            pilula("Convivência", W("convivência,"), PEITO, left=520, style={"fontSize": "40px"})]),
        corte(2, 2, W("às"), W("Ele"), trans="iris", irisY=45, els=[
            kick("Em alguns casos", W("às") + .05),
            texto("Visita <em>assistida</em>", W("assistidas"), 520, size=110, align="center", anim="sobe"),
            pilula("depende do caso", W("dependendo"), 720, left=0, style=centro(460))]),
        rosto(2, 3, W("Ele"), W("A"), trans="luz", kb=(1.16, 1.22), dy=-190, els=[
            carimbo("Nunca", W("nunca,"), 960, 380, rot=-7, size=110)]),
        corte(2, 4, W("A"), W("O", W("específicos.")), trans="tinta", tdur=.7, els=[
            kick("A regra no Brasil", W("A") + .05),
            po("Compartilhada", W("compartilhada,"), 540, 560, size=124),
            texto("exceções em <em>casos específicos</em>", W("exceções"), 760, size=70, align="center", anim="sobe")]),
        rosto(2, 5, W("O", W("específicos.")), fim, trans="whip", els=[
            pilula("O bem-estar da criança", W("bem-estar") + .05, PEITO, left=0, style=centro(620))]),
        outro(fim, "Parte 3 · Quando o contato é suspenso", "quem está se separando", area="Direito de Família"),
    ]


def reel3(W, seg, fim):
    """3/3 · Quando o contato com o pai ou a mãe pode ser suspenso."""
    return [
        corte(3, 0, 0, W("Não,"), trans="corte", els=[
            kick("A dúvida que mais chega", 0.05),
            texto("Tenho a guarda.|O outro <em>pode ver</em> o filho?", 0.08, 430, size=92)]),
        rosto(3, 1, W("Não,"), W("Isso", 12.0), trans="whip", kb=(1.14, 1.2), dy=-190, els=[
            pilula("Restrição de contato", W("restrição"), PEITO, left=0, style=centro(520))]),
        corte(3, 2, W("Isso", 12.0), W("Então,"), trans="iris", irisY=45, els=[
            kick("Só acontece em casos", W("Isso", 12.0) + .05),
            carimbo("Extremos", W("extremamente"), 540, 230, rot=-6, size=100),
            texto("que causam <em>dano</em> à criança", W("danosos"), 780, size=72, align="center", anim="sobe")]),
        rosto(3, 3, W("Então,"), W("Não", W("Então,")), trans="luz", kb=(1.14, 1.2), dy=-190, els=[
            pilula("O bem-estar da criança", W("bem-estar") + .05, PEITO, left=0, style=centro(620))]),
        corte(3, 4, W("Não", W("Então,")), W("Tem", 28.0), trans="tinta", tdur=.7, els=[
            kick("Não basta um pedir", W("Não", W("Então,")) + .05),
            texto("O juiz não tira|<em>só porque um quer</em>", W("juiz"), 460, size=86, align="center")]),
        corte(3, 5, W("Tem", 28.0), W("Meu", 34.0), trans="zoom", particulas=22, els=[
            kick("Quem analisa", W("Tem", 28.0) + .05),
            no("Juiz", W("juiz", W("Tem", 28.0)), 200, top=600), no("MP", W("Ministério"), 540, top=600, sub="Ministério Público"),
            no("Psicólogos", W("psicólogos"), 880, top=600)]),
        rosto(3, 6, W("Meu", 34.0), fim, trans="whip", kb=(1.14, 1.2), dy=-190, els=[
            pilula("Dra. Letícia Barros", W("Meu", 34.0) + .05, PEITO, left=0, style=centro(520))]),
        outro(fim, "Salve a série completa", "quem está se separando", area="Direito de Família"),
    ]


def _reel(n, dur, roteiro):
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / f"transcricao-r{n}.json",
            "trechos": [(0.0, dur)], "roteiro": roteiro, "prefixo": "guarda-compartilhada-", "serie": f"Guarda dos filhos · {n}/3"}


REELS = {1: _reel(1, 27.90, reel1), 2: _reel(2, 27.46, reel2), 3: _reel(3, 37.96, reel3)}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
