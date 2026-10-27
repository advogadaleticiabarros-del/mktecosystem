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

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 52%, rgba(26,21,17,.45) 62%, rgba(26,21,17,.8) 100%)"  # rosto intacto: só o peito escurece, para os textos (26/10/2026)
BAIXO_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 70%, rgba(26,21,17,.55) 100%)"
DY, ZB = -60, 1.06          # rosto em tela cheia (igual ao estilo inteiro)
DY_BAIXO, FOCO_BAIXO = 650, 445  # tela dividida: a boca desce para y~1400; o punch-in gira em torno dela
CORRIGE = {"na@20.58": "naquele", "agrididia.": "dia,", "Grívia.": "dia,", "pactuado": "acertado", "factuado": "acertado", "ver": "vir",
           "muito@0.00": "Muitos", "guarda,": "embora,", "Falei": "Trabalhei", "tempo.": "ter."}  # R2


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
    a5, a6, a7 = W("Então", 16.0), W("E", 21.0), W("Então", 26.0)
    a9, a10, a11 = W("Então", 33.5), W("Esse"), W("Meu")
    return [
        dividida(0, 0, a1, dg.titulo("Você sabia?", -1, "contrato por hora") + dg.relogio(-1, 540, 590, size=400)),
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
                 + dg.contracheque([W("recebe"), W("13º", 31.0), W("férias."), W("férias.") + .45], top=260)),
        dividida(7, a9, a10, dg.dezembro(a9 + .05, W("13º", a9), top=200)
                 + dg.fgts_deposito(W("receber.") - .2, top=800)),
        dividida(8, a10, a11, dg.relogio(a10 + .05, 540, 470, acesas=4)
                 + [texto("Contrato <em>intermitente</em>", a10 + .3, 700, size=72, align="center", anim="sobe")]),
        rosto(9, a11, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a11 + .05, 520)]),
        outro(fim, "Parte 2 · Quando vira problema", "quem trabalha por hora"),
    ]


def reel2(W, seg, fim):
    """Quando o contrato intermitente vira problema."""
    def baixo(i, a, b, els):
        return {"a": a, "trans": "corte", "painel": dg.PAINEL,
                "bg": {**preparar_seq(f"r2_baixo{i}", "fala-r2", a, b - a + 0.4), "rosto": True, "foco": FOCO_BAIXO,
                       "kb": [1.0, 1.03, 0, 0, DY_BAIXO, DY_BAIXO - 10]},
                "veu": BAIXO_VEU, "els": list(els)}

    def cara(i, a, b, kb=(1.0, 1.04), els=()):
        z = ZB - 1.0
        return {"a": a, "trans": "corte", "bg": {**preparar_seq(f"r2_rosto{i}", "fala-r2", a, b - a + 0.4), "rosto": True,
                                                 "kb": [kb[0] + z, kb[1] + z, 0, 0, DY, DY - 20]},
                "veu": FACE_VEU, "els": list(els)}

    a1, a2 = W("Por"), W("O", W("trabalhador.", W("correta")))
    a3, a4 = W("E", W("férias,")), W("E", W("intermitente.", W("final,")))
    a5, a6, a7 = W("Doutora,"), W("Se"), W("Agora")
    a8, a9, a10 = W("Porque"), W("Ah"), W("Mas", W("recusar."))
    a11, a12 = W("A", W("disso?")), W("Meu")
    return [
        baixo(0, 0, a1, dg.titulo("Contrato por hora", -1, "vira problema assim") + dg.relogio(-1, 540, 600, acesas=4, size=360)),
        cara(1, a1, a2, kb=(1.06, 1.1), els=[chip("Falta informação ao trabalhador", W("falta") - .1, 700)]),
        baixo(2, a2, a3, dg.titulo("O que ele acha que tem", a2 + .05)
              + [dg.comparacao(W("normal,"), 99)[0]]),
        cara(3, a3, a4, kb=(1.02, 1.06), els=[chip("No fim: era intermitente", W("intermitente.", a3) - .4, 600)]),
        baixo(4, a4, a5, dg.comparacao(a4 + .05, a4 + .3, top=260)),
        baixo(5, a5, a6, dg.balao("Mas a pessoa não está recebendo diariamente?", a5 + .05, top=380)),
        cara(6, a6, a7, kb=(1.04, 1.08), els=[chip("Entendeu e concordou: ok", W("concordar,") - .1, 600)]),
        baixo(7, a7, a8, dg.titulo("Todo dia, sem convocação", a7 + .05)
              + dg.meses([W("um", a7), W("dois", a7), W("três", a7)], W("entende") + .2, top=330)),
        cara(8, a8, a9, kb=(1.06, 1.1), els=[chip("Vínculo de emprego comum", a8 + .1, 600)]),
        baixo(9, a9, a10, dg.balao("Ah, não, mas eu convoco. Ela pode recusar.", a9 + .05, top=380, autor="empresa")),
        cara(10, a10, a11, kb=(1.1, 1.14), els=[texto("Ela <em>sabe</em> disso?", a10 + .05, 905, size=84, align="center")]),
        baixo(11, a11, a12, dg.titulo("Papel x prática", a11 + .05)
              + dg.papel_pratica(a11 + .3, W("prática") - .1, top=330)
              + [pilula("Funcionário sem ser funcionário", W("funcionário", a11) - .1, 790, left=0, style=centro(700))]),
        cara(12, a12, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a12 + .05, 520)]),
        outro(fim, "Parte 1 · O que é o intermitente", "quem trabalha por hora"),
    ]


def _reel(n, roteiro, serie, prefixo):
    fim = m.fim_da_fala(m.AQUI / "videos" / f"fala-r{n}.transcricao.json", m.AQUI / "videos" / f"fala-r{n}.mp4")
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / "videos" / f"fala-r{n}.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Contrato intermitente · 1/2", "contrato-intermitente-dividida-v3-"),
    2: _reel(2, reel2, "Contrato intermitente · 2/2", "contrato-intermitente-dividida-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
