"""13º proporcional e 13º as 4 regras, versão 2 (06/11/2026): mesmo tratamento aprovado no 2/3 (eixo central, rosto
sem texto por cima, efeitos sonoros v2). Nas 4 regras, a regra 2 agora termina a frase ("no cálculo do benefício"),
antes cortada em "período no".
Uso: py serie2_v2.py 44 66 [--checar | --amostras]. Saída: ../13-proporcional-calculo-v2.mp4 e ../13-quatro-regras-v2.mp4."""
import sys

import motor as m
import serie2
from motor import bloco_html, foto, po
from serie2 import linha_ok
from v2base import CX, VEU_ROSTO, cc, kc, pc, tc


def p13v2(W, seg, fim):
    meses = "".join(
        f'<div class="m{i}" style="text-align:center;padding:14px 0;border-radius:12px;font-size:28px;font-weight:800;'
        + ('background:linear-gradient(180deg,#F4E6BC,#C9A962);color:#231E1A' if i >= 7 else 'background:rgba(232,222,209,.14);color:#FAF6F0')
        + f'">{mm}</div>' for i, mm in enumerate("JFMAMJJASOND"))
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-novo-emprego-0"), "kb": [1.16, 1.04, 0, 0, 80, 120], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            kc("13º proporcional", 0.05),
            tc("Começou no|<em>meio do ano</em>?", 0.08, 420, size=124),
            pc("garantido por lei", W("garantido"), 720, 460)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-calculadora-1"), "blur": 6}, "veu": "rgba(26,21,17,.76)", "els": [
            kc("Exemplo", seg[1] + .05),
            bloco_html('<div style="font-size:27px;font-weight:800;letter-spacing:3px;color:#8E6E2E">CONTRATO</div>'
                       '<div style="display:flex;justify-content:space-between;font-size:40px;margin-top:22px"><span>Salário</span><b>R$ 3.000</b></div>'
                       '<div style="display:flex;justify-content:space-between;font-size:40px;margin-top:12px"><span>Início</span><b>10 de agosto</b></div>',
                       W("salário"), 420, 110, 860, cls="papel", anim="pop"),
            po("÷ 12", W("12"), CX, 860, size=200)]},
        {"a": seg[2], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-calendario-4"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            kc("E o mês quebrado?", seg[2] + .05),
            tc("Começou dia 10.|Agosto <em>conta</em>?", W("Como"), 420, size=100)]},
        {"a": seg[3], "trans": "zoom", "particulas": 22, "els": [
            kc("A regra dos 15 dias", seg[3] + .05),
            po("15 dias", W("15", seg[3]), CX, 500, size=200),
            cc("= mês inteiro", W("inteira."), 680, size=84)]},
        {"a": seg[4], "trans": "luz", "bg": {"src": foto("f-calculadora-5"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            kc("Agosto a dezembro", seg[4] + .05),
            bloco_html(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px">{meses}</div>', seg[4] + .2, 430, 100, 880,
                       anim="pop", padding="28px 30px"),
            po("5 fatias", W("cinco"), CX, 820, size=170)]},
        {"a": seg[5], "trans": "whipV", "particulas": 26, "els": [
            tc("R$ 3.000 ÷ 12 × 5", W("multiplicar"), 420, size=96, anim="sobe"),
            po("R$ 1.250", W("1.250"), CX, 720, size=230),
            pc("no fim do ano", W("fim", seg[6]), 900, 400)]},
        m.outro(fim, "1ª parcela até 30/11", "quem começou este ano"),
    ]


def regras13v2(W, seg, fim):
    def regra(n, nome, at):
        return po(f"Regra {n}", at, CX, 470, size=150), pc(nome, at + .5, 560, 700)
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-calculadora-1"), "kb": [1.2, 1.05, 0, 0, -40, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.88), rgba(26,21,17,.5) 45%, rgba(26,21,17,.9))", "els": [
            kc("13º salário", 0.05),
            tc("Seu 13º está|<em>correto</em>?", 0.08, 410, size=130),
            po("4 regras", W("quatro"), CX, 820, size=200)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-calendario-2"), "blur": 8}, "veu": "rgba(26,21,17,.8)", "els": [
            *regra(1, "Prazos e impostos", seg[1] + .05),
            linha_ok("1ª parcela até 30/11, sem desconto", W("30", seg[1]), 690),
            linha_ok("2ª até 18/12, com INSS e IR", W("Como", seg[1]), 820)]},
        {"a": seg[2], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-calendario-4"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            *regra(2, "Contagem dos meses", seg[2] + .05),
            cc("15 dias = 1 mês", W("15", seg[2]), 720, size=76)]},
        {"a": seg[3], "trans": "luz", "bg": {"src": foto("f-noite-4"), "blur": 9}, "veu": VEU_ROSTO, "els": [
            *regra(3, "O que soma e o que protege", seg[3] + .05),
            pc("Horas extras", W("horas"), 670, 460, fontSize="32px"),
            pc("Adicional noturno", W("adicional"), 750, 460, fontSize="32px"),
            pc("Comissões", W("comissões"), 830, 460, fontSize="32px"),
            cc("Não reduzem o 13º", W("diminuem"), 940, size=60)]},
        {"a": seg[4], "trans": "zoom", "bg": {"src": foto("f-rh-0"), "blur": 8}, "veu": VEU_ROSTO, "els": [
            *regra(4, "Rescisão", seg[4] + .05),
            linha_ok("Pediu demissão: recebe", W("Pediu"), 690),
            linha_ok("Sem justa causa: recebe", W("justa", seg[4]), 820),
            cc("Justa causa: perde", W("zera"), 960, size=64)]},
        m.outro(fim, "1ª parcela: até 30/11", "quem espera o 13º"),
    ]


REELS = {
    44: {**serie2.REELS[4], "roteiro": p13v2, "nome": "13-proporcional-calculo-v2"},
    66: {**serie2.REELS[6], "roteiro": regras13v2, "nome": "13-quatro-regras-v2",
         "trechos": [(0.0, 9.9), (10.4, 26.35), (26.9, 35.9), (36.4, 49.92), (50.9, 61.15)]},
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
