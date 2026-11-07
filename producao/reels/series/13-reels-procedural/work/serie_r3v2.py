"""13º sem susto 3/3, versão 2 (06/11/2026): mesmo tratamento aprovado no 2/3 (eixo central, rosto sem texto por cima,
efeitos sonoros v2). Uso: py serie_r3v2.py 33 [--checar | --amostras]. Saída: ../13-sem-susto-reel-3-v2.mp4."""
import sys

import motor as m
import serie  # noqa: F401  (configura CFG da série 13º sem susto)
from motor import bloco_html, foto, no, outro, pilula, po, preparar_seq, traco
from v2base import CX, VEU_ROSTO, cc, kc, tc


def reel3v2(W, seg, fim):
    meses = "".join(
        f'<div style="text-align:center;padding:14px 0;border-radius:12px;font-size:28px;font-weight:800;'
        + ('background:linear-gradient(180deg,#F4E6BC,#C9A962);color:#231E1A' if i in (6, 7, 8, 9) else 'background:rgba(232,222,209,.14);color:#FAF6F0')
        + f'">{mm}</div>' for i, mm in enumerate("JFMAMJJASOND"))
    par = {"width": "300px", "textAlign": "center", "fontSize": "36px"}
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("r3_mae", "v-mae-bebe-0", 0.5, 4.5), "kb": [1.18, 1.04, 0, 0, -40, 0], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            tc("De licença-|<em>maternidade</em>?", 0.08, 420, size=120),
            po("13º inteiro", W("13º"), CX, 820, size=150)]},
        {"a": W("A"), "trans": "whip", "bg": {"src": foto("f-mae-bebe-2"), "blur": 9, "kb": [1.08, 1.16, 0, 0, 0, 0]},
         "veu": "rgba(26,21,17,.8)", "els": [
            kc("Seu ano de trabalho", W("A") + .05),
            bloco_html(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px">{meses}</div>'
                       '<div style="margin-top:18px;font-size:28px;font-weight:700;color:#F4E6BC;text-align:center">■ meses de licença</div>',
                       W("A") + .15, 430, 100, 880, anim="pop", padding="28px 30px"),
            cc("Contam como trabalhados", W("trabalhado."), 830, size=48)]},
        {"a": W("A", W("trabalhado.")), "trans": "zoom", "particulas": 22, "els": [
            kc("Quem paga", W("A", W("trabalhado.")) + .05),
            no("Empresa", W("empresa"), 260, top=520), no("Você", W("paga"), 820, top=520, sub="13º completo"),
            traco('<path class="desenha" d="M10 30 L420 30 M380 5 L420 30 L380 55"/>', W("paga"), 487, 330, 430, 60, dur=.6),
            no("INSS", W("compensa"), 260, top=880, sub="compensa a licença"),
            traco('<path class="desenha" d="M30 250 L30 10 M5 50 L30 10 L55 50"/>', W("compensa"), 615, 230, 60, 260, dur=.6)]},
        {"a": W("Quem"), "trans": "luz", "bg": {"src": foto("f-vendedora-5"), "kb": [1.06, 1.12, 0, 0, 110, 90], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            pilula("Autônoma", W("autônoma"), 400, left=225, style=par),
            pilula("Doméstica", W("doméstica,"), 400, left=555, style=par),
            tc("O 13º proporcional|<em>vem pelo INSS</em>", W("recebe"), 520, size=88)]},
        {"a": W("Valor"), "trans": "corte", "particulas": 26, "bg": {**preparar_seq("r3_aflita", "v-escritorio-2", 3.5, 3.0), "blur": 7},
         "veu": VEU_ROSTO, "els": [
            tc("Veio menor|pela licença?", W("Valor"), 400, size=118),
            cc("É erro", W("erro."), 720, size=140, rot=-6)]},
        {"a": W("Guarde"), "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-rh-1"), "blur": 7, "kb": [1.04, 1.12, 0, 0, -20, 0]},
         "veu": VEU_ROSTO, "els": [
            kc("O que fazer", W("Guarde") + .05),
            bloco_html('<div style="font-size:40px;font-weight:700;display:flex;gap:18px;align-items:center;justify-content:center"><span style="color:#C9A962">✓</span>Guarde os contracheques</div>',
                       W("Guarde") + .1, 430, 90, 900, anim="sobe", padding="26px 34px"),
            bloco_html('<div style="font-size:40px;font-weight:700;display:flex;gap:18px;align-items:center;justify-content:center"><span style="color:#C9A962">✓</span>Peça o cálculo ao RH</div>',
                       W("peça"), 570, 90, 900, anim="sobe", padding="26px 34px")]},
        outro(seg[1], "Salve a série completa", "uma gestante", gestante=True),
    ]


REELS = {33: {"trechos": [(51.25, 70.95), (71.40, 75.95)], "roteiro": reel3v2, "serie": "13º sem susto · 3/3",
              "nome": "13-sem-susto-reel-3-v2"}}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
