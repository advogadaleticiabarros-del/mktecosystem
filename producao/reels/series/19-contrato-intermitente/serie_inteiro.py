"""Série 19 · Contrato intermitente, estilo INTEIRO COM BANCO DE IMAGENS (padrão premium, motor/ intacto).
Teste de estilo (Jessica, 26/10/2026): o R1 sai neste estilo e em tela dividida (work-dividida/), os dois como Reels de
teste do Instagram (só não seguidores); o R2 sai depois no estilo que ganhar.
Fala: ../fontes/falas.py (fatos e cortes no docstring de lá). Banco: ../fontes/creditos-pexels.txt. 3D: motor3d/clip3d.py.
Uso: py serie.py [1] [--amostras | --checar]
"""
import subprocess
import sys
from pathlib import Path

import motor as m
from motor import centro, kick, outro, pilula, preparar_seq, texto

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Contrato intermitente", "corrige": {},
              "destaques": {"hora", "intermitente.", "três", "recusar.", "acertado", "13º", "férias.", "direitos."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 52%, rgba(26,21,17,.45) 62%, rgba(26,21,17,.8) 100%)"  # rosto intacto: só o peito escurece, para os textos (26/10/2026)
STOCK_VEU = "linear-gradient(180deg, rgba(26,21,17,.82) 0%, rgba(26,21,17,.5) 30%, rgba(26,21,17,.45) 55%, rgba(26,21,17,.88) 100%)"
DY = {1: -60}    # o rosto desta gravação já fica alto no quadro (folha do bruto): sobe pouco
ZB = {1: 1.06}   # zoom-base leve: com mais, a testa e o cabelo saem cortados
CORRIGE = {"na@20.58": "naquele", "agrididia.": "dia,", "pactuado": "acertado", "ver": "vir"}
FFPROBE = str(m.FF).replace("ffmpeg.exe", "ffprobe.exe")


def duracao(stock):
    arq = next((m.AQUI / "videos").glob(f"stock-{stock}.mp4"))
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def rosto(n, i, a, b, trans="corte", kb=(1.0, 1.04), els=(), **kw):
    dy, z = DY[n], ZB[n] - 1.0
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "rosto": True,
                                           "kb": [kb[0] + z, kb[1] + z, 0, 0, dy, dy - 20]},
            "veu": FACE_VEU, "els": list(els), **kw}


def corte(n, i, a, b, stock, trans="corte", els=(), ini=0.3, **kw):
    precisa, tem = ini + (b - a) + 0.4, duracao(stock)
    assert precisa <= tem, f"r{n} cena {i}: {precisa:.1f}s sobre o vídeo '{stock}' de {tem:.1f}s (a imagem congelaria)"
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_stk{i}_{stock}", f"stock-{stock}", ini, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": STOCK_VEU, "els": list(els), **kw}


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def reel1(W, seg, fim):
    """O que é o contrato intermitente e como funciona."""
    a1, a2, a3 = W("Já", 2.5), W("Como"), W("A", 6.0)
    a4, a5, a6 = W("pelo"), W("Então", 16.0), W("E", 21.0)
    a7, a8, a9 = W("Então", 27.0), W("já", 34.5), W("Então", 37.0)
    a10, a11 = W("Esse"), W("Meu")
    return [
        rosto(1, 0, 0, a1, els=[texto("Você sabia que o|<em>contrato por hora</em> já existe?", 0.05, 905, size=60, align="center")]),
        corte(1, 1, a1, a2, "celular", trans="whip", els=[
            kick("Já existe", a1 + .05),
            texto("Contrato|<em>intermitente</em>", a1 + .1, 480, size=100, align="center", anim="sobe"),
            pilula("CLT, art. 452-A", W("intermitente.") + .2, 760, left=0, style=centro(420))]),
        rosto(1, 2, a2, a3, kb=(1.06, 1.1), els=[texto("Como <em>funciona?</em>", a2 + .05, 905, size=72, align="center")]),
        corte(1, 3, a3, a4, "3d-semana", ini=0.0, els=[
            kick("A convocação", a3 + .05),
            texto("A empresa|<em>te chama</em>", W("convoca"), 400, size=92, align="center", anim="sobe")]),
        corte(1, 4, a4, a5, "calendario", els=[
            kick("O prazo", a4 + .05),
            texto("<em>3 dias</em>|de antecedência", W("três"), 480, size=96, align="center", anim="sobe"),
            pilula("1 dia útil para responder", W("recusar."), 760, left=0, style=centro(640))]),
        rosto(1, 5, a5, a6, kb=(1.04, 1.08), els=[chip("Sem resposta conta como recusa", W("disponível"), 760)]),
        corte(1, 6, a6, a7, "barista", trans="luz", els=[
            kick("O pagamento", a6 + .05),
            texto("Valor da hora|<em>combinado</em>", W("acertado"), 480, size=92, align="center", anim="sobe")]),
        rosto(1, 7, a7, a8, kb=(1.02, 1.06), els=[chip("Recebe no fim do período", W("recebe"), 640)]),
        corte(1, 8, a8, a9, "chef", els=[
            kick("Já vem junto", a8 + .05),
            texto("<em>13º</em> e férias", W("13º", a8 - .1), 500, size=110, align="center", anim="sobe")]),
        corte(1, 9, a9, a10, "3d-cofre", ini=0.0, els=[
            kick("Em dezembro", a9 + .05),
            texto("Sem 13º|<em>de uma vez</em>", W("final", a9), 400, size=88, align="center", anim="sobe"),
            pilula("FGTS: depositado todo mês", W("receber.") - .2, 600, left=0, style=centro(640))]),
        rosto(1, 10, a10, a11, kb=(1.06, 1.1), els=[chip("Contrato intermitente", a10 + .05, 520)]),
        rosto(1, 11, a11, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a11 + .05, 520)]),
        outro(fim, "Parte 2 · Quando vira problema", "quem trabalha por hora"),
    ]


def _reel(n, roteiro, serie, prefixo):
    fim = m.fim_da_fala(m.AQUI / "videos" / f"fala-r{n}.transcricao.json", m.AQUI / "videos" / f"fala-r{n}.mp4")
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / "videos" / f"fala-r{n}.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Contrato intermitente · 1/2", "contrato-intermitente-inteiro-v2-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
