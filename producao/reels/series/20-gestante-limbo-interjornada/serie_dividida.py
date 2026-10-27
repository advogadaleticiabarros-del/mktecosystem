"""Série 20 · gestante na experiência, limbo previdenciário e intervalo de 11 horas, estilo TELA DIVIDIDA (escolha da
Jessica, 27/10/2026; motor-dividida/ por cima da cópia do motor). Um Reel por tema.
Regra do Reel de referência de 27/10/2026 ("teste do mudo"): primeiro quadro forte, o gancho inteiro na tela desde o
quadro 1 (at=-1), fala sem respiro no começo e o resultado antes da explicação (o título já diz a resposta).
Fala: ../fontes/falas.py (fatos e cortes no docstring de lá). Diagramas: diagramas.py.
Uso: py serie.py [1 2 3] [--amostras | --checar]
"""
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, outro, pilula, preparar_seq, texto
import diagramas as dg

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Direitos em 1 minuto", "corrige": {},
              "destaques": {"estabilidade", "experiência.", "parto.", "limbo", "empresa.", "INSS.", "11", "extra.", "direitos."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 52%, rgba(26,21,17,.45) 62%, rgba(26,21,17,.8) 100%)"  # rosto intacto
BAIXO_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 70%, rgba(26,21,17,.55) 100%)"
DY, ZB = -60, 1.06
DY_BAIXO, FOCO_BAIXO = 650, 445
# legenda: o que o Whisper ouviu errado na fala montada (a fala está certa; confira na transcrição literal)
CORRIGE = {1: {"Isso": "Você", "a@15.04": "descobriu", "publico": "que", "provo": "prazo", "há@31.54": "até", "par": "parto."},
           2: {"A@51.18": "Meu", "minha": "nome é", "é@51.92": "e", "que@52.02": "aqui"},
           3: {"resalo": "intervalo", "evidado": "vedado", "oraís,": "hora extra."}}


def _cenas(n):
    def rosto(i, a, b, kb=(1.0, 1.04), els=(), trans="corte", **kw):
        z = ZB - 1.0
        return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "rosto": True,
                                               "kb": [kb[0] + z, kb[1] + z, 0, 0, DY, DY - 20]},
                "veu": FACE_VEU, "els": list(els), **kw}

    def dividida(i, a, b, els, trans="corte", **kw):
        return {"a": a, "trans": trans, "painel": dg.PAINEL,
                "bg": {**preparar_seq(f"r{n}_baixo{i}", f"fala-r{n}", a, b - a + 0.4), "rosto": True, "foco": FOCO_BAIXO,
                       "kb": [1.0, 1.03, 0, 0, DY_BAIXO, DY_BAIXO - 10]},
                "veu": BAIXO_VEU, "els": list(els), **kw}
    return rosto, dividida


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def grande(html, at, size=78):
    return texto(html, at, 905, size=size, align="center")


def reel1(W, seg, fim):
    """Gestante no contrato de experiência."""
    rosto, dividida = _cenas(1)
    a1, a2, a3 = W("No"), W("E", W("experiência.")), W("Você", W("agora?"))
    a4, a5, a6 = W("A", W("provisória.")), W("Comunica", W("RH.")), W("Ah,")
    a7, a8, a9, a10 = W("Quando"), W("A", W("embora.", W("Quando"))), W("que", 28.0), W("Meu")
    return [
        dividida(0, 0, a1, dg.titulo("Grávida na experiência", -1, "tem estabilidade")
                 + dg.etapas([("Contrato de experiência", W("empresa,")), ("Engravidou", W("engravida."))], top=420)),
        rosto(1, a1, a2, kb=(1.04, 1.08), els=[grande("Na <em>experiência</em>", a1 + .05, size=96)]),
        rosto(2, a2, a3, kb=(1.1, 1.14), els=[grande("E <em>agora?</em>", a2 + .05, size=110)]),
        dividida(3, a3, a4, dg.escudo(a3 + .1, "Estabilidade da gestante", top=260)
                 + [pilula("Estabilidade provisória", W("provisória.") - .3, 760, left=0, style=centro(560))]),
        dividida(4, a4, a5, dg.titulo("Começa na concepção", a4 + .05)
                 + dg.linha_tempo([("Concepção", W("concepção,")), ("Parto", None), ("+5 meses", None)], top=480)
                 + [pilula("Bom avisar o RH", W("RH.") - .3, 700, left=0, style=centro(420))]),
        rosto(5, a5, a6, kb=(1.02, 1.06), els=[chip("Não pode te mandar embora", W("embora.", a5) - .3, 640)]),
        dividida(6, a6, a7, dg.balao("Mas o contrato é por prazo determinado...", a6 + .05, top=360)),
        dividida(7, a7, a8, dg.titulo("Fim da experiência?", a7 + .05, "não pode dispensar")
                 + [carimbo("Estabilidade", W("embora.", a7) - .2, 520, 250, rot=-6, size=80)]),
        rosto(8, a8, a9, kb=(1.06, 1.1), els=[chip("Ou indeniza o período inteiro", W("indenize") - .1, 700)]),
        dividida(9, a9, a10, dg.titulo("Até quando?", a9 + .05)
                 + dg.linha_tempo([("Concepção", a9 + .3), ("Parto", W("parto.") - .4), ("+5 meses", W("cinco"))], top=480)
                 + [pilula("ADCT, art. 10 · TST, Súmula 244", W("parto.") + .2, 700, left=0, style=centro(640))]),
        rosto(10, a10, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a10 + .05, 520)]),
        outro(fim, "Vale no contrato de experiência", "uma amiga grávida"),
    ]


def reel2(W, seg, fim):
    """Limbo previdenciário."""
    rosto, dividida = _cenas(2)
    a1, a2, a3 = W("tem"), W("Depois"), W("Chegando")
    a4, a6, a7 = W("E", W("trabalho.", W("Chegando"))), W("E", W("trabalho.", W("olha,"))), W("E", W("INSS.", W("nem")))
    a8, a9 = W("Para", 45.0), W("Meu")
    return [
        dividida(0, 0, a1, dg.titulo("Limbo previdenciário", -1, "quem paga é a empresa")
                 + dg.vai_e_volta(.6, 1.6, top=470)),
        dividida(1, a1, a2, dg.etapas([("Carteira assinada", a1 + .05), ("Afastada mais de 15 dias", W("15") - .2),
                                       ("Encaminhada ao INSS", W("INSS.") - .3)], top=300, gap=170)),
        dividida(2, a2, a3, dg.ficha("INSS", a2 + .05, "Alta", W("considerou"), nota="Perícia")),
        dividida(3, a3, a4, dg.ficha("Médico da empresa", a3 + .05, "Inapta", W("apta") - .1, nota="Exame de retorno")),
        dividida(4, a4, a6, dg.titulo("Vai e volta", a4 + .05) + dg.vai_e_volta(W("devolve"), W("falar"), top=470)),
        dividida(5, a6, a7, dg.titulo("No limbo", a6 + .05, "sem salário")
                 + dg.sem_salario(W("empresa,", a6) - .2, W("INSS.", a6) - .3, top=430)),
        rosto(6, a7, a8, kb=(1.04, 1.08), els=[chip("Pode buscar na Justiça", W("justiça") - .1, 560)]),
        dividida(7, a8, a9, dg.titulo("Quem paga?", a8 + .05, "a empresa")
                 + [carimbo("Empresa paga", W("empresa.", a8) - .2, 520, 220, rot=-6, size=84)]),
        rosto(8, a9, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a9 + .05, 520)]),
        outro(fim, "Salário do limbo é da empresa", "quem está afastado pelo INSS"),
    ]


def reel3(W, seg, fim):
    """Intervalo de 11 horas entre jornadas."""
    rosto, dividida = _cenas(3)
    a1, a2, a3 = W("10"), W("E"), W("O", W("manhã."))
    a4, a5, a6, a7, a8 = W("Precisa"), W("até", 28.0), W("Se"), W("a", 33.5), W("Meu")
    return [
        dividida(0, 0, a1, dg.titulo("Saiu às 22h, volta às 7h?", -1, "a lei não deixa") + dg.relogio(-1, 540, 600, size=380)),
        dividida(1, a1, a2, dg.titulo("Saída", a1 + .05, "22h") + dg.relogio(a1 + .2, 540, 620, acesas=3, size=340)),
        dividida(2, a2, a3, dg.titulo("Entrada", a2 + .05, "7h da manhã")
                 + dg.descanso(W("7") - .2, 99, top=480)),
        rosto(3, a3, a4, kb=(1.06, 1.1), els=[grande("Isso <em>não pode</em>", W("pode") - .1)]),
        dividida(4, a4, a5, dg.titulo("Mínimo: 11 horas", a4 + .05, "entre uma jornada e outra")
                 + dg.descanso(a4 + .3, W("11", a4) + .1, top=480)
                 + [pilula("CLT, art. 66", W("descanso.", W("jornada,")) - .3, 800, left=0, style=centro(360))]),
        rosto(5, a5, a6, kb=(1.02, 1.06), els=[chip("Para proteger a sua saúde", a5 + .1, 600)]),
        dividida(6, a6, a7, dg.titulo("Não cumpriu?", a6 + .05, "paga hora extra")
                 + [pilula("Horas que faltaram = hora extra", W("pagar") - .2, 520, left=0, style=centro(720)),
                    pilula("TST, OJ 355", W("pagar") + .7, 640, left=0, style=centro(320))]),
        rosto(7, a7, a8, kb=(1.06, 1.1), els=[grande("Violação de <em>direitos trabalhistas</em>", a7 + .05, size=64)]),
        rosto(8, a8, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a8 + .05, 520)]),
        outro(fim, "Mínimo de 11 horas de descanso", "quem trabalha de escala"),
    ]


def _reel(n, roteiro, serie, prefixo):
    fim = m.fim_da_fala(m.AQUI / "videos" / f"fala-r{n}.transcricao.json", m.AQUI / "videos" / f"fala-r{n}.mp4")
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / "videos" / f"fala-r{n}.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE[n]}


REELS = {
    1: _reel(1, reel1, "Gestante · estabilidade", "gestante-experiencia-dividida-"),
    2: _reel(2, reel2, "Limbo previdenciário", "limbo-previdenciario-dividida-"),
    3: _reel(3, reel3, "Intervalo de 11 horas", "intervalo-11-horas-dividida-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
