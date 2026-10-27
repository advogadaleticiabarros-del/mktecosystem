"""Série 22 · Demissão por causa do voto (assédio eleitoral), Reels animado sem a Dra. em cena (27/10/2026).
Pedido da Jessica: "reels animado (sem precisar da advogada), com narração, ganchos e dinâmico"; voz clonada da Dra.
a partir das gravações de 26/10 (fontes/roteiro.txt → narrar.py). Estilo inteiro com banco de imagens + diagramas da
tela dividida (cópia do motor da série 19 work-motion). Neutro: nenhum partido nem candidato (OAB).

Fatos (briefing producao/campanhas/2026-10-assedio-eleitoral/BRIEFING.md):
- 140 denúncias ao MPT em 26/10/2026, um dia depois do 2º turno, maior número num único dia em 2026 (balanço do MPT,
  Metrópoles 26/10); 1.939 no ano até 25/10.
- Voto secreto: CF, art. 14. Ninguém privado de direitos por convicção política: CF, art. 5º, VIII. Convenção 111 OIT.
- Dispensa discriminatória: Lei 9.029/1995, art. 1º; art. 4º: à escolha do empregado, reintegração com ressarcimento
  integral do período (I) ou o dobro da remuneração do período de afastamento (II); dano moral à parte.
- Denúncia sigilosa no site do MPT.
Banco: creditos-pexels.txt.
Uso: py serie.py [1] [--amostras | --checar]
"""
import os
import subprocess
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, outro, pilula, po, preparar_seq, texto
import diagramas as dg

m.AQUI = Path(__file__).resolve().parent
FONTES = m.AQUI.parent / "fontes" / os.environ.get("NARRACAO", "")  # NARRACAO=rascunho-voz-antiga só mede o tempo
m.CFG.update({"src": FONTES / "narracao.wav", "serie": "Demissão por causa do voto", "corrige": {},
              "destaques": {"voto?", "quarenta", "recorde", "secreto,", "votou.", "discriminatória.", "voltar", "dobro",
                            "moral.", "mensagens,", "testemunhas.", "sigilosa."}})

VEU = "linear-gradient(180deg, rgba(26,21,17,.88) 0%, rgba(26,21,17,.62) 30%, rgba(26,21,17,.66) 62%, rgba(26,21,17,.92) 100%)"
VEU_DG = "linear-gradient(180deg, rgba(26,21,17,.9) 0%, rgba(26,21,17,.78) 25%, rgba(26,21,17,.76) 60%, rgba(26,21,17,.93) 100%)"
FFPROBE = str(m.FF).replace("ffmpeg.exe", "ffprobe.exe")


def duracao(stock):
    arq = m.AQUI / "videos" / f"stock-{stock}.mp4"
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def cena(i, a, b, stock, els, trans="corte", ini=0.3, veu=VEU, blur=0, kb=(1.0, 1.07), dy=(0, -20)):
    """Vídeo do banco em tela cheia, escurecido, com os textos ou o diagrama por cima."""
    precisa, tem = ini + (b - a) + 0.4, duracao(stock)
    assert precisa <= tem, f"cena {i}: {precisa:.1f}s sobre o vídeo '{stock}' de {tem:.1f}s (a imagem congelaria)"
    bg = {**preparar_seq(f"r1_c{i}_{stock}", f"stock-{stock}", ini, b - a + 0.4), "kb": [kb[0], kb[1], 0, 0, dy[0], dy[1]]}
    if blur:
        bg["blur"] = blur
    return {"a": a, "trans": trans, "bg": bg, "veu": veu, "els": list(els)}


def reel1(W, seg, fim):
    """Gancho → número do MPT → a regra → carimbo → a escolha (o dobro em pó de ouro, ~65%) → provas → denúncia."""
    a1 = W("Um")
    a2 = W("O", W("ano."))
    a3 = W("Demitir")
    a4 = W("A", a3)
    a5 = W("ou", a4)
    a6 = W("Guarde")
    a7 = W("E", W("testemunhas."))
    a8 = W("Cada")
    return [
        cena(0, 0, a1, "caixa", ini=1.0, kb=(1.12, 1.04), dy=(-40, -10), els=[
            kick("Assédio eleitoral", -1, top=370),
            texto("Demitido por|causa do <em>seu voto?</em>", -1, 440, size=112),
        ]),
        cena(1, a1, a2, "celular", trans="whip", ini=2.0, blur=3, els=[
            kick("Ministério Público do Trabalho", a1 + .05, top=380),
            po("140", W("quarenta"), 540, 640, size=300),
            texto("denúncias em|<em>um só dia</em>", W("denúncias"), 830, size=70, align="center", anim="sobe"),
            pilula("Recorde no ano", W("Recorde"), 1010, left=0, style=centro(420)),
        ]),
        cena(2, a2, a3, "janela", trans="tinta", ini=0.5, blur=8, veu=VEU_DG, els=[
            texto("O voto é|<em>secreto</em>", a2 + .05, 420, size=120),
            texto("Não importa em|quem <em>você votou</em>", W("Não"), 700, size=76, anim="sobe"),
            pilula("Constituição, arts. 5º e 14", W("ninguém"), 930, left=90),
        ]),
        cena(3, a3, a4, "abatido", trans="corte", ini=0.5, blur=7, veu=VEU_DG, els=[
            texto("Demitir por <em>isso</em>", a3 + .05, 430, size=96, align="center"),
            carimbo("Dispensa discriminatória", W("dispensa"), 640, 90, rot=-6, size=82),
            pilula("Lei 9.029/1995", W("discriminatória.") + .35, 900, left=0, style=centro(380)),
        ]),
        cena(4, a4, a5, "cracha", trans="luz", ini=0.3, veu=VEU_DG, blur=8, els=[
            kick("A lei prevê: você escolhe", a4 + .05, top=380),
            texto("Voltar ao|<em>trabalho</em>", W("voltar"), 470, size=118, align="center"),
            pilula("com os salários do período", W("salários"), 790, left=0, style=centro(640)),
        ]),
        cena(5, a5, a6, "notebook", trans="zoom", ini=2.0, veu=VEU_DG, blur=6, els=[
            kick("Ou receber em dobro", a5 + .02, top=380),
            po("2x", W("dobro"), 540, 580, size=300),
            texto("o que ganharia|nesse <em>tempo</em>", W("ganharia"), 770, size=70, align="center", anim="sobe"),
            pilula("+ dano moral", W("dano"), 1000, left=0, style=centro(360)),
        ]),
        cena(6, a6, a7, "maos", trans="tinta", ini=0.2, veu=VEU_DG, blur=5, els=[
            kick("Guarde as provas", a6 + .05, top=360),
            *dg.etapas([("Mensagens e áudios", W("mensagens,")), ("Prints de grupos e posts", W("prints")),
                        ("Testemunhas", W("testemunhas."))], top=450, gap=160),
        ]),
        cena(7, a7, a8, "notebook", trans="whip", ini=12.0, veu=VEU_DG, blur=4, els=[
            *dg.escudo(a7 + .1, "Denúncia sigilosa no MPT", top=400),
        ]),
        outro(a8, "Passo a passo: link na bio", "quem precisa saber"),
    ]


def _reel():
    trans = FONTES / "transcricao.json"
    fim = m.fim_da_fala(trans, FONTES / "narracao.wav") if trans.exists() else 40.0
    return {"src": FONTES / "narracao.wav", "transcricao": trans, "trechos": [(0.0, round(fim, 2))], "roteiro": reel1,
            "serie": "Demissão por causa do voto", "prefixo": "demissao-por-voto-motion-", "punch": 1.0}


REELS = {1: _reel()}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
