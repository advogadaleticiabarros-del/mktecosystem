"""13º sem susto 2/3, versão 2 (06/11/2026, pedido da Jessica: "quero melhorar a aparência também, o alinhamento
das frases e elementos").
- Tudo num eixo central (x=540), igual à legenda; kicker, títulos, pílulas e carimbos centralizados.
- Gancho na tela com dúvida: "Entrou no meio do ano?" (narração igual).
- Sai o "Na parte 3." solto (46,74–47,46 s do áudio).
- Texto nunca sobre rosto nítido: fotos com rosto ganham desfoque e véu mais escuro.
- Efeitos sonoros v2 (som2.py).
Uso: py serie_r2v2.py 22 [--checar | --amostras]. Saída: ../13-sem-susto-reel-2-v2.mp4 (o original fica intacto)."""
import sys

import motor as m
import serie  # noqa: F401  (configura CFG da série 13º sem susto)
import som2
from motor import LINHA_HTML, bloco_html, carimbo, centro, foto, foto_card, kick, no, outro, pilula, po, preparar_seq, texto

m.sfx = lambda pasta: som2.efeitos_v2(m.AQUI / "sfx2")

CX = 540
VEU_ROSTO = "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.62) 45%, rgba(26,21,17,.92))"


def kc(txt, at, top=350):
    return kick(txt, at, top=top, style=centro(800))


def pc(txt, at, top, w=560, **st):
    return pilula(txt, at, top, style={**centro(w), **st})


def tc(html, at, top, size=110, **kw):
    return texto(html, at, top, size=size, align="center", **kw)


def cc(txt, at, top, size=76, rot=-4):
    w = len(txt) * size * 0.66 + 70
    return carimbo(txt, at, top, int((1080 - w) / 2), rot=rot, size=size)


def reel2v2(W, seg, fim):
    L, R, T1, T2 = 95, 555, 450, 790
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("r2_lap", "v-escritorio-0", 0.5, 5.5), "kb": [1.15, 1.04, 0, 0, -40, 0], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            tc("Entrou no|<em>meio do ano</em>?", 0.08, 380, size=120),
            po("13º", W("13º"), CX, 800, size=260),
            pc("é seu do mesmo jeito", W("mesmo"), 990)]},
        {"a": W("Seja"), "trans": "whipV", "particulas": 24, "els": [
            kc("Todas têm direito", W("Seja") + .05, top=370),
            foto_card(foto("f-rural-4"), "Rural", W("rural,"), T1, L),
            foto_card(foto("f-domestica-0"), "Doméstica", W("doméstica,"), T1, R),
            foto_card(foto("f-vendedora-4"), "Temporária", W("temporária"), T2, L),
            foto_card(foto("f-escritorio-0"), "Carteira assinada", W("carteira"), T2, R)]},
        {"a": W("15"), "trans": "zoom", "bg": {**preparar_seq("r2_cal", "v-calendario-1", 2.0, 5.0), "blur": 8},
         "veu": "rgba(26,21,17,.8)", "els": [
            kc("A regra dos 15 dias", W("15") + .05),
            po("15 dias", W("15"), CX, 530, size=200),
            {"tipo": "linha", "html": LINHA_HTML, "at": W("trabalhados"), "ateFim": W("inteiro.") + .1,
             "style": {"top": "720px", "left": "140px", "width": "800px"}},
            no("1º dia", W("trabalhados"), 140, top=720), no("15º dia", W("valem"), CX, top=720), no("mês", W("inteiro."), 940, top=720),
            cc("= 1/12 do 13º", W("inteiro."), 880, size=80)]},
        {"a": W("Faltas"), "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-atestado-2"), "kb": [1.05, 1.16, 0, 0, -20, 20], "blur": 8},
         "veu": VEU_ROSTO, "els": [
            kc("Faltou com atestado?", W("Faltas") + .05),
            bloco_html('<div style="font-size:27px;font-weight:800;letter-spacing:3px;color:#8E6E2E">ATESTADO MÉDICO</div>'
                       '<div class="cg" style="font-size:64px;font-weight:700;line-height:1;margin-top:12px">Falta justificada</div>'
                       '<div style="margin-top:18px;height:8px;background:#2B231C22;border-radius:4px"></div>'
                       '<div style="margin-top:10px;height:8px;width:65%;background:#2B231C22;border-radius:4px"></div>',
                       W("Faltas") + .1, 470, 190, 700, cls="papel", anim="sobe"),
            cc("Não reduz", W("diminuem"), 800, size=96)]},
        {"a": W("Horas"), "trans": "whip", "bg": {"src": foto("f-noite-4"), "blur": 9, "kb": [1.06, 1.14, 0, 0, 0, -30]},
         "veu": VEU_ROSTO, "els": [
            kc("Entram na média", W("Horas") + .05),
            pc("Horas extras", W("Horas"), 440, 560, fontSize="38px"),
            pc("Comissões", W("comissões"), 545, 560, fontSize="38px"),
            pc("Adicional noturno", W("noturno"), 650, 560, fontSize="38px"),
            tc("<em>+ no seu 13º</em>", W("entram"), 800, size=110, anim="sobe")]},
        {"a": W("Na", W("conta.")), "trans": "luz", "bg": {"src": foto("f-rh-0"), "kb": [1.04, 1.12, 0, 0, -20, 0], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            tc("Demitida sem|justa causa?", W("demissão"), 400, size=104),
            tc("Recebe o|<em>proporcional</em>", W("recebe"), 640, size=104, anim="sobe"),
            cc("Só a justa causa tira", W("Só"), 900, size=54)]},
        {"a": seg[1], "trans": "tinta", "tdur": .8, "bg": {"src": foto("f-mae-bebe-0"), "kb": [1.04, 1.14, 0, 0, 0, -30], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            pc("Parte 3", seg[1] + .1, 400, 260),
            tc("De licença-|maternidade:", W("Quem"), 500, size=104),
            tc("<em>13º inteiro?</em>", W("13º", seg[1]), 740, size=120, anim="sobe")]},
        outro(fim, "Parte 3 · Licença e 13º", "quem espera o 13º"),
    ]


REELS = {22: {"trechos": [(25.22, 46.05), (47.75, 50.95)], "roteiro": reel2v2, "serie": "13º sem susto · 2/3",
              "nome": "13-sem-susto-reel-2-v2"}}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
