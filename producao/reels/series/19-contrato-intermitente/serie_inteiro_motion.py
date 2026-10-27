"""Série 19 · Contrato intermitente, estilo INTEIRO COM AS ANIMAÇÕES DA TELA DIVIDIDA (Jessica, 27/10/2026: "faça na versão
inteira, mas use os mesmos tipos de animações que a outra está usando").
A Dra. em tela cheia nas falas diretas (como no inteiro); nos trechos de explicação, banco ou 3D escurecido com os mesmos
diagramas da tela dividida (traço SVG que se desenha, relógio que volta e se completa, calendário, recibo, dezembro),
descidos para a faixa limpa do quadro cheio. Motor: cópia do motor/ com engine.html, fx.js e diagramas.py da
motor-dividida/ (cena sem "painel" fica igual ao motor/). O motor/ não muda.
Fala: ../fontes/falas.py (fatos e cortes no docstring de lá). Banco: creditos-pexels.txt. 3D: motor3d/clip3d.py.
Uso: py serie.py [1] [--amostras | --checar]
"""
import subprocess
import sys
from pathlib import Path

import motor as m
from motor import centro, outro, pilula, preparar_seq, texto
import diagramas as dg

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Contrato intermitente", "corrige": {},
              "destaques": {"hora", "intermitente.", "três", "recusar.", "acertado", "13º", "férias.", "direitos."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 52%, rgba(26,21,17,.45) 62%, rgba(26,21,17,.8) 100%)"  # rosto intacto: só o peito escurece, para os textos (26/10/2026)
DIAGRAMA_VEU = "linear-gradient(180deg, rgba(26,21,17,.9) 0%, rgba(26,21,17,.76) 25%, rgba(26,21,17,.74) 60%, rgba(26,21,17,.92) 100%)"  # o traço dourado precisa de fundo calmo
DY, ZB = -60, 1.06   # rosto desta gravação já fica alto no quadro: sobe pouco, zoom-base leve
DESCE = 150          # diagramas da tela dividida (y 175 a 900 do painel) descem para a faixa limpa do quadro cheio
CORRIGE = {"na@20.58": "naquele", "agrididia.": "dia,", "Grívia.": "dia,", "pactuado": "acertado", "factuado": "acertado", "ver": "vir"}
FFPROBE = str(m.FF).replace("ffmpeg.exe", "ffprobe.exe")


def duracao(stock):
    arq = m.AQUI / "videos" / f"stock-{stock}.mp4"
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def desce(els, dy=DESCE):
    """Leva os elementos do painel para baixo no quadro cheio (top e o estouro do carimbo)."""
    for e in els:
        st = e.get("style", {})
        if str(st.get("top", "")).endswith("px"):
            st["top"] = f"{float(st['top'][:-2]) + dy:g}px"
        if "burst" in e:
            e["burst"]["y"] += dy
    return els


def rosto(i, a, b, kb=(1.0, 1.04), els=(), trans="corte"):
    z = ZB - 1.0
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r1_rosto{i}", "fala-r1", a, b - a + 0.4), "rosto": True,
                                           "kb": [kb[0] + z, kb[1] + z, 0, 0, DY, DY - 20]},
            "veu": FACE_VEU, "els": list(els)}


def diagrama(i, a, b, stock, els, trans="corte", ini=0.3):
    """Banco ou 3D escurecido em tela cheia, com o diagrama desenhado por cima."""
    precisa, tem = ini + (b - a) + 0.4, duracao(stock)
    assert precisa <= tem, f"cena {i}: {precisa:.1f}s sobre o vídeo '{stock}' de {tem:.1f}s (a imagem congelaria)"
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r1_dg{i}_{stock}", f"stock-{stock}", ini, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": DIAGRAMA_VEU, "els": desce(list(els))}


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def reel1(W, seg, fim):
    """O que é o contrato intermitente e como funciona (mesma fala do R1 v3)."""
    a1, a2, a3 = W("Já", 2.5), W("Como"), W("A", 6.0)
    conv, a5, a6 = W("convoca"), W("Então", 16.0), W("E", 21.0)
    a7, rec, a9 = W("Então", 26.0), W("recebe"), W("Então", 33.5)
    a10, a11 = W("Esse"), W("Meu")
    return [
        rosto(0, 0, a1, kb=(1.06, 1.1), els=[texto("Você sabia que o|<em>contrato por hora</em> já existe?", -1, 905, size=60, align="center")]),
        diagrama(1, a1, a2, "celular", trans="whip", els=dg.titulo("O nome dele é", a1 + .1, "contrato intermitente")
                 + [pilula("CLT, art. 452-A", W("intermitente.") + .1, 420, left=0, style=centro(420))]
                 + dg.relogio(W("intermitente.") + .3, 540, 680, acesas=1, size=240)),
        rosto(2, a2, a3, kb=(1.06, 1.1), els=[texto("Como <em>funciona?</em>", a2 + .05, 905, size=72, align="center")]),
        diagrama(3, a3, conv, "3d-semana", ini=0.0, els=dg.titulo("Quem quer", a3 + .05, "te contratar")
                 + [pilula("O empregador", W("empregador,") + .05, 430, left=0, style=centro(400))]
                 + dg.relogio(W("empregador,") + .3, 540, 660, size=280)),
        # o banco "calendario" tem corações vermelhos, fora da paleta: aqui vai outro trecho do celular
        diagrama(4, conv, a5, "celular", ini=13.0, els=dg.titulo("Ele", conv + .05, "te convoca")
                 + dg.calendario(W("pelo"), W("recusar."), top=470)),
        rosto(5, a5, a6, kb=(1.04, 1.08), els=[chip("Sem resposta conta como recusa", W("disponível"), 760)]),
        diagrama(6, a6, a7, "barista", trans="luz", els=dg.titulo("E o pagamento?", a6 + .05, "o valor da hora")
                 + dg.relogio(W("acertado"), 540, 620, acesas=2, rotulo="Combinado antes")),
        rosto(7, a7, rec, kb=(1.02, 1.06), els=[chip("No fim do período", a7 + .05, 520)]),
        diagrama(8, rec, a9, "presente", els=dg.titulo("Você recebe", rec + .05)
                 + dg.contracheque([rec + .4, W("13º", 31.0), W("férias."), W("férias.") + .45], top=260)),
        diagrama(9, a9, a10, "3d-cofre", ini=0.0, els=dg.dezembro(a9 + .05, W("13º", a9), top=200)
                 + dg.fgts_deposito(W("receber.") - .2, top=800)),
        diagrama(10, a10, a11, "celular", ini=8.0, els=dg.relogio(a10 + .05, 540, 470, acesas=4)
                 + [texto("Contrato <em>intermitente</em>", a10 + .3, 700, size=72, align="center", anim="sobe")]),
        rosto(11, a11, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", a11 + .05, 520)]),
        outro(fim, "Parte 2 · Quando vira problema", "quem trabalha por hora"),
    ]


def _reel(n, roteiro, serie, prefixo):
    fim = m.fim_da_fala(m.AQUI / "videos" / f"fala-r{n}.transcricao.json", m.AQUI / "videos" / f"fala-r{n}.mp4")
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / "videos" / f"fala-r{n}.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Contrato intermitente · 1/2", "contrato-intermitente-inteiro-motion-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
