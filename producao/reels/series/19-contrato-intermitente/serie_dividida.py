"""Série 19 · Contrato intermitente, estilo TELA DIVIDIDA (motor-dividida/ por cima da cópia do motor).
Teste de estilo (Jessica, 26/10/2026): o R1 sai neste estilo e em tela inteira com banco (../work/), os dois como Reels de
teste do Instagram (só não seguidores); o R2 sai depois no estilo que ganhar.
Referência: Reels de explicação (diagrama no alto, pessoa embaixo, símbolo que volta e se completa), com a nossa identidade.
Fala: ../fontes/falas.py (fatos e cortes no docstring de lá). Diagramas: diagramas.py.
Uso: py serie.py [1] [--amostras | --checar]
"""
import sys
from pathlib import Path

import motor as m
from motor import centro, outro, pilula, preparar_seq, texto
import diagramas as dg

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Contrato intermitente", "corrige": {},
              "destaques": {"hora", "intermitente.", "três", "recusar.", "acertado", "13º", "férias.", "direitos."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,.35) 0%, rgba(26,21,17,0) 14%, rgba(26,21,17,0) 46%, rgba(26,21,17,.55) 58%, rgba(26,21,17,.9) 100%)"
BAIXO_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 70%, rgba(26,21,17,.55) 100%)"
DY, ZB = -60, 1.06          # rosto em tela cheia (igual ao estilo inteiro)
DY_BAIXO, FOCO_BAIXO = 650, 445  # tela dividida: a boca desce para y~1400; o punch-in gira em torno dela
CORRIGE = {"na@20.58": "naquele", "agrididia.": "dia,", "pactuado": "acertado", "ver": "vir"}


def rosto(i, a, b, kb=(1.0, 1.04), els=(), trans="corte", **kw):
    z = ZB - 1.0
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r1_rosto{i}", "fala-r1", a, b - a + 0.4), "rosto": True,
                                           "kb": [kb[0] + z, kb[1] + z, 0, 0, DY, DY - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def dividida(i, a, b, els, trans="corte", **kw):
    """Diagrama no painel do alto, a Dra. falando embaixo (punch-in nas emendas, em torno da boca)."""
    return {"a": a, "trans": trans, "painel": dg.PAINEL,
            "bg": {**preparar_seq(f"r1_baixo{i}", "fala-r1", a, b - a + 0.4), "rosto": True, "foco": FOCO_BAIXO,
                   "kb": [1.0, 1.03, 0, 0, DY_BAIXO, DY_BAIXO - 10]},
            "veu": BAIXO_VEU, "els": list(els), **kw}


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def reel1(W, seg, fim):
    """O que é o contrato intermitente e como funciona."""
    a1, a2, a3 = W("Já", 2.5), W("Como"), W("A", 6.0)
    a5, a6, a7 = W("Então", 16.0), W("E", 21.0), W("Então", 27.0)
    a9, a10, a11 = W("Então", 37.0), W("Esse"), W("Meu")
    return [
        dividida(0, 0, a1, dg.titulo("Você sabia?", .05, "contrato por hora") + dg.relogio(.5, 540, 590, size=400)),
        dividida(1, a1, a2, dg.titulo("O nome dele é", a1 + .1, "contrato intermitente")
                 + [pilula("CLT, art. 452-A", W("intermitente.") + .1, 420, left=0, style=centro(420))]
                 + dg.relogio(W("intermitente.") + .3, 540, 680, acesas=1, size=240)),
        rosto(2, a2, a3, kb=(1.06, 1.1), els=[texto("Como <em>funciona?</em>", a2 + .05, 905, size=72, align="center")]),
        dividida(3, a3, a5, dg.titulo("A empresa", a3 + .05, "te convoca")
                 + dg.calendario(W("pelo"), W("recusar."), top=470)),
        rosto(4, a5, a6, kb=(1.04, 1.08), els=[chip("Sem resposta conta como recusa", W("disponível"), 760)]),
        dividida(5, a6, a7, dg.titulo("E o pagamento?", a6 + .05, "o valor da hora")
                 + dg.relogio(W("acertado"), 540, 620, acesas=2, rotulo="Combinado antes")),
        dividida(6, a7, a9, dg.titulo("No fim do período", a7 + .05)
                 + dg.contracheque([W("recebe"), W("13º", 34.5), W("férias."), W("férias.") + .45], top=260)),
        dividida(7, a9, a10, dg.dezembro(a9 + .05, W("13º", a9), top=200)
                 + dg.fgts_deposito(W("receber.") - .2, top=800)),
        dividida(8, a10, a11, dg.relogio(a10 + .05, 540, 470, acesas=4)
                 + [texto("Contrato <em>intermitente</em>", a10 + .3, 700, size=72, align="center", anim="sobe")]),
        rosto(9, a11, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a11 + .05, 520)]),
        outro(fim, "Parte 2 · Quando vira problema", "quem trabalha por hora"),
    ]


def _reel(n, roteiro, serie, prefixo):
    fim = m.fim_da_fala(m.AQUI / "videos" / f"fala-r{n}.transcricao.json", m.AQUI / "videos" / f"fala-r{n}.mp4")
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / "videos" / f"fala-r{n}.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Contrato intermitente · 1/2", "contrato-intermitente-dividida-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
