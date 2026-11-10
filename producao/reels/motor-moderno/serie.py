"""Série "13º sem susto" em 3 Reels (10/10/2026), só com o áudio do vídeo do NotebookLM
(O_Guia_Definitivo_do_Décimo_Terceiro_Para_Trabalhadoras.mp4). Motor v2 (motor.py + engine.html + fx.js).

Uso: py serie.py [1 2 3] [--amostras | --checar]
Fatos: Lei 4.749/1965 (parcelas e prazos); Lei 4.090/1962 (1/12 por mês de 15 dias); Decreto 57.155/1965, art. 2º
(faltas justificadas); Súmula 45 do TST (média de extras e adicionais); Súmula 157 do TST (proporcional na rescisão);
Lei 7.855/1989, art. 3º (multa); Lei 8.213/1991, art. 72, § 1º (empresa paga e compensa no INSS).
Cortado do áudio: 13,7–16,2 s ("contos contos de INSS", fala truncada pela IA).
"""
import sys
from pathlib import Path

import motor as m
from motor import (BALANCA, LINHA_HTML, bloco_html, carimbo, centro, foto, foto_card, kick, no, outro, pilula, po,
                   preparar_seq, risco, texto, traco)

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({
    "src": m.AQUI.parent / "fontes" / "v5.mp4",
    "serie": "13º sem susto",
    "corrige": {"Guardes": "Guarde", "contra": "contracheques", "cheques": "", "sexta": "sexta-feira,", "-feira,": "", "Da": "Na", "da": "dá"},
    "destaques": {"dezembro?", "não", "30", "novembro", "18", "sexta-feira", "multa", "meses", "13º", "rural", "doméstica", "temporária",
                  "carteira", "15", "inteiro", "atestado", "extras", "comissões", "noturno", "proporcional", "justa", "licença",
                  "inteiro", "completo", "compensa", "inss", "erro", "rh"},
})

CAL = ["", "", 1, 2, 3, 4, 5] + list(range(6, 32))  # dezembro/2026 começa numa terça


def calendario(at, top=430):
    cab = "".join(f'<div style="font-size:24px;font-weight:800;color:#8E6E2E;text-align:center">{d}</div>' for d in "DSTQQSS")
    dias = ""
    for d in CAL:
        estilo = "font-size:30px;font-weight:700;text-align:center;padding:6px 0;border-radius:12px;color:#2B231C"
        if d == 18:
            estilo += ";background:linear-gradient(180deg,#F4E6BC,#C9A962);box-shadow:0 0 0 4px #8E6E2E,0 0 30px rgba(201,169,98,.8)"
        if d == 20:
            estilo += ";color:#A4532E;text-decoration:line-through;text-decoration-thickness:4px"
        dias += f'<div style="{estilo}">{d or ""}</div>'
    html = (f'<div style="display:flex;justify-content:space-between;align-items:baseline"><span class="cg" style="font-size:58px;font-weight:700">Dezembro</span>'
            f'<span style="font-size:26px;font-weight:800;letter-spacing:3px;color:#8E6E2E">2026</span></div>'
            f'<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-top:18px">{cab}{dias}</div>')
    return bloco_html(html, at, top, 120, 840, cls="papel", anim="pop", transform="rotate(-2deg)", padding="28px 34px")


def reel1(W, seg, fim):
    """Parte 1 · Prazos do 13º."""
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-calendario-2"), "kb": [1.22, 1.06, 0, 0, -50, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.82), rgba(26,21,17,.35) 45%, rgba(26,21,17,.9))", "els": [
            kick("13º salário", 0.05),
            texto("O 13º só em|<em>dezembro?</em>", 0.08, 410, size=140),
            carimbo("Não pode", W("Não"), 760, 230, rot=-8, size=110)]},
        {"a": W("A", 4.0), "trans": "tinta", "tdur": .8, "bg": {**preparar_seq("r1_cal", "v-calendario-1", 0.5, 5.0), "blur": 3},
         "veu": "rgba(26,21,17,.72)", "els": [
            kick("1ª parcela", W("A", 4.0) + .1),
            texto("vence até", W("vence"), 420, size=80, anim="sobe"),
            po("30/11", W("30"), 540, 650, size=280),
            pilula("sem descontos", W("sem"), 860, left=0, style=centro(420))]},
        {"a": W("Como"), "trans": "whip", "bg": {"src": foto("f-calendario-4"), "blur": 10, "kb": [1.1, 1.18, 0, 0, 0, 0]},
         "veu": "rgba(26,21,17,.75)", "els": [
            kick("2ª parcela", W("Como") + .1),
            calendario(W("Como") + .2, top=400),
            carimbo("Até sexta, 18", W("18"), 925, 250, rot=-6, size=64),
            pilula("INSS e IR descontados na 2ª", W("18") + .9, 1030, left=0, style={**centro(640), "fontSize": "26px"})]},
        {"a": seg[1], "trans": "luz", "bg": {"src": foto("f-escritorio-1"), "kb": [1.05, 1.15, 0, 0, -30, 20]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.3) 50%, rgba(26,21,17,.9))", "els": [
            texto("Tudo de|uma vez?", seg[1] + .1, 390, size=130),
            texto("Só até <em>30/11</em>", W("até", seg[1]), 690, size=110, anim="sobe")]},
        {"a": W("Atrasar"), "trans": "corte", "particulas": 26, "bg": {**preparar_seq("r1_aflita", "v-escritorio-2", 0.8, 3.0), "blur": 7},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.45) 50%, rgba(26,21,17,.9))", "els": [
            texto("Atrasou?", W("Atrasar"), 400, size=150),
            carimbo("Multa", W("multa."), 690, 300, rot=-9, size=150)]},
        {"a": seg[2], "trans": "tinta", "tdur": .8, "bg": {"src": foto("f-rural-4"), "kb": [1.04, 1.14, 0, 0, 0, -30]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.88), rgba(26,21,17,.4) 45%, rgba(26,21,17,.92))", "els": [
            pilula("Parte 2", seg[2] + .1, 380, left=70),
            texto("Trabalhei só|alguns meses.", seg[2] + .3, 480, size=104),
            texto("<em>Quanto recebo?</em>", seg[2] + 1.0, 720, size=112, anim="sobe")]},
        outro(fim, "Parte 2 · 13º proporcional", "quem espera o 13º"),
    ]


def reel2(W, seg, fim):
    """Parte 2 · Quem tem direito e como calcular."""
    L, R, T1, T2 = 95, 555, 420, 760
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("r2_lap", "v-escritorio-0", 0.5, 5.5), "kb": [1.15, 1.04, 0, 0, -40, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.35) 45%, rgba(26,21,17,.9))", "els": [
            texto("Só alguns|<em>meses</em>?", 0.08, 400, size=140),
            po("13º", W("13º"), 540, 830, size=260),
            pilula("é seu do mesmo jeito", W("mesmo"), 990, left=0, style=centro(560))]},
        {"a": W("Seja"), "trans": "whipV", "particulas": 24, "els": [
            kick("Todas têm direito", W("Seja") + .05, top=350),
            foto_card(foto("f-rural-4"), "Rural", W("rural,"), T1, L),
            foto_card(foto("f-domestica-0"), "Doméstica", W("doméstica,"), T1, R),
            foto_card(foto("f-vendedora-4"), "Temporária", W("temporária"), T2, L),
            foto_card(foto("f-escritorio-0"), "Carteira assinada", W("carteira"), T2, R)]},
        {"a": W("15"), "trans": "zoom", "bg": {**preparar_seq("r2_cal", "v-calendario-1", 2.0, 5.0), "blur": 8},
         "veu": "rgba(26,21,17,.78)", "els": [
            kick("A regra dos 15 dias", W("15") + .05),
            po("15 dias", W("15"), 540, 530, size=200),
            {"tipo": "linha", "html": LINHA_HTML, "at": W("trabalhados"), "ateFim": W("inteiro.") + .1, "style": {"top": "720px", "left": "140px", "width": "800px"}},
            no("1º dia", W("trabalhados"), 140, top=720), no("15º dia", W("valem"), 540, top=720), no("mês", W("inteiro."), 940, top=720),
            carimbo("= 1/12 do 13º", W("inteiro."), 900, 200, rot=-6, size=80)]},
        {"a": W("Faltas"), "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-atestado-2"), "kb": [1.05, 1.16, 0, 0, -20, 20]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.35) 50%, rgba(26,21,17,.9))", "els": [
            bloco_html('<div style="font-size:24px;font-weight:800;letter-spacing:3px;color:#8E6E2E">ATESTADO MÉDICO</div>'
                       '<div class="cg" style="font-size:56px;font-weight:700;line-height:1;margin-top:10px">Falta<br>justificada</div>'
                       '<div style="margin-top:16px;height:8px;background:#2B231C22;border-radius:4px"></div><div style="margin-top:10px;height:8px;width:65%;background:#2B231C22;border-radius:4px"></div>',
                       W("Faltas") + .1, 700, 120, 420, cls="papel", anim="desliza", dx=-400, transform="rotate(-4deg)"),
            carimbo("Não reduz", W("diminuem"), 960, 300, rot=-8, size=96)]},
        {"a": W("Horas"), "trans": "whip", "bg": {"src": foto("f-noite-4"), "blur": 9, "kb": [1.06, 1.14, 0, 0, 0, -30]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.88), rgba(26,21,17,.55) 50%, rgba(26,21,17,.92))", "els": [
            kick("Entram na média", W("Horas") + .05),
            pilula("Horas extras", W("Horas"), 430, left=90, style={"fontSize": "36px"}),
            pilula("Comissões", W("comissões"), 540, left=230, style={"fontSize": "36px"}),
            pilula("Adicional noturno", W("noturno"), 650, left=140, style={"fontSize": "36px"}),
            texto("<em>+ no seu 13º</em>", W("entram"), 800, size=110, anim="sobe")]},
        {"a": W("Na", W("conta.")), "trans": "luz", "bg": {"src": foto("f-rh-0"), "kb": [1.04, 1.12, 0, 0, -20, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.88), rgba(26,21,17,.4) 45%, rgba(26,21,17,.92))", "els": [
            texto("Demitida sem|justa causa?", W("demissão"), 400, size=104),
            texto("Recebe o|<em>proporcional</em>", W("recebe"), 630, size=104, anim="sobe"),
            carimbo("Só a justa causa tira", W("Só"), 900, 110, rot=-5, size=62)]},
        {"a": seg[1], "trans": "tinta", "tdur": .8, "bg": {"src": foto("f-mae-bebe-0"), "kb": [1.04, 1.14, 0, 0, 0, -30]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.88), rgba(26,21,17,.35) 45%, rgba(26,21,17,.92))", "els": [
            pilula("Parte 3", seg[1] + .1, 380, left=70),
            texto("De licença-|maternidade:", W("Quem"), 480, size=104),
            texto("<em>13º inteiro?</em>", W("13º", seg[1]), 720, size=120, anim="sobe")]},
        outro(fim, "Parte 3 · Licença e 13º", "quem espera o 13º"),
    ]


def reel3(W, seg, fim):
    """Parte 3 · A gestante e o 13º."""
    meses = "".join(
        f'<div style="text-align:center;padding:14px 0;border-radius:12px;font-size:28px;font-weight:800;'
        + ('background:linear-gradient(180deg,#F4E6BC,#C9A962);color:#231E1A' if i in (6, 7, 8, 9) else 'background:rgba(232,222,209,.14);color:#FAF6F0')
        + f'">{mm}</div>' for i, mm in enumerate("JFMAMJJASOND"))
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("r3_mae", "v-mae-bebe-0", 0.5, 4.5), "kb": [1.18, 1.04, 0, 0, -40, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.3) 45%, rgba(26,21,17,.9))", "els": [
            texto("De licença-|<em>maternidade</em>?", 0.08, 610, size=120),
            po("13º inteiro", W("13º"), 540, 1010, size=150)]},
        {"a": W("A"), "trans": "whip", "bg": {"src": foto("f-mae-bebe-2"), "blur": 9, "kb": [1.08, 1.16, 0, 0, 0, 0]},
         "veu": "rgba(26,21,17,.76)", "els": [
            kick("Seu ano de trabalho", W("A") + .05),
            bloco_html(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px">{meses}</div>'
                       '<div style="margin-top:18px;font-size:28px;font-weight:700;color:#F4E6BC">■ meses de licença</div>',
                       W("A") + .15, 430, 100, 880, anim="pop", padding="28px 30px"),
            carimbo("Contam como trabalhados", W("trabalhado."), 830, 120, rot=-5, size=48)]},
        {"a": W("A", W("trabalhado.")), "trans": "zoom", "particulas": 22, "els": [
            kick("Quem paga", W("A", W("trabalhado.")) + .05),
            no("Empresa", W("empresa"), 260, top=520), no("Você", W("paga"), 820, top=520, sub="13º completo"),
            traco('<path class="desenha" d="M10 30 L420 30 M380 5 L420 30 L380 55"/>', W("paga"), 487, 330, 430, 60, dur=.6),
            no("INSS", W("compensa"), 260, top=880, sub="compensa a licença"),
            traco('<path class="desenha" d="M30 250 L30 10 M5 50 L30 10 L55 50"/>', W("compensa"), 615, 230, 60, 260, dur=.6)]},
        {"a": W("Quem"), "trans": "luz", "bg": {"src": foto("f-vendedora-5"), "kb": [1.06, 1.12, 0, 0, 110, 90]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.45) 40%, rgba(26,21,17,.2) 60%, rgba(26,21,17,.9))", "els": [
            pilula("Autônoma", W("autônoma"), 370, left=90, style={"fontSize": "36px"}),
            pilula("Doméstica", W("doméstica,"), 370, left=400, style={"fontSize": "36px"}),
            texto("O 13º proporcional|<em>vem pelo INSS</em>", W("recebe"), 465, size=88)]},
        {"a": W("Valor"), "trans": "corte", "particulas": 26, "bg": {**preparar_seq("r3_aflita", "v-escritorio-2", 3.5, 3.0), "blur": 7},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.86), rgba(26,21,17,.45) 50%, rgba(26,21,17,.9))", "els": [
            texto("Veio menor|pela licença?", W("Valor"), 400, size=118),
            carimbo("É erro", W("erro."), 720, 280, rot=-9, size=140)]},
        {"a": W("Guarde"), "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-rh-1"), "blur": 7, "kb": [1.04, 1.12, 0, 0, -20, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.4) 45%, rgba(26,21,17,.92))", "els": [
            kick("O que fazer", W("Guarde") + .05),
            bloco_html('<div style="font-size:40px;font-weight:700;display:flex;gap:18px;align-items:center"><span style="color:#C9A962">✓</span>Guarde os contracheques</div>',
                       W("Guarde") + .1, 430, 90, 900, anim="desliza", dx=-300, padding="26px 34px"),
            bloco_html('<div style="font-size:40px;font-weight:700;display:flex;gap:18px;align-items:center"><span style="color:#C9A962">✓</span>Peça o cálculo ao RH</div>',
                       W("peça"), 570, 90, 900, anim="desliza", dx=-300, padding="26px 34px")]},
        outro(seg[1], "Salve a série completa", "uma gestante", gestante=True),
    ]


REELS = {
    1: {"trechos": [(0.0, 13.45), (16.20, 20.45), (21.05, 24.85)], "roteiro": reel1, "prefixo": "13-sem-susto-"},
    2: {"trechos": [(25.22, 46.05), (46.65, 50.95)], "roteiro": reel2, "prefixo": "13-sem-susto-"},
    3: {"trechos": [(51.25, 70.95), (71.40, 75.95)], "roteiro": reel3, "prefixo": "13-sem-susto-"},
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
