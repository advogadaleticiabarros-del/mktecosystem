"""Mais 6 Reels (10/10/2026) com o áudio dos outros vídeos do NotebookLM enviados pela Letícia. Motor v2.

1-3 · Série "Gestante e insalubridade" (Gestante_e_Trabalho.mp4): 10, 12 e 14/11.
4 · 13º proporcional, o cálculo (Como_Calcular_o_13º_Proporcional.mp4): 09/11.
5 · Pensão: o mito dos 30% (Como_a_Pensão_Alimentícia_é_Calculada.mp4): 16/11.
6 · 13º: as 4 regras (O_Guia_Definitivo_do_Décimo_Terceiro.mp4): 29/11.

Fatos: CLT, art. 394-A (afastamento de qualquer grau, salário e adicional mantidos, § 2º compensação, § 3º gravidez de
risco e salário-maternidade); STF, ADI 5938 (vale também para a lactante, sem atestado); CLT, art. 396 (2 descansos de
30 min até os 6 meses); Lei 4.090/1962 e Lei 4.749/1965 (13º); CC, arts. 1.694, § 1º e 1.699 (necessidade e
possibilidade; revisão); CPC, art. 528 (prisão civil por dívida de alimentos).
Fora do áudio (gestante): "especialistas apontam" (termo vetado), "30 dias para avisar" (não é regra da lei),
"frigorífico" (fala embolada), "pergunta de 1 milhão de dólares". Pensão: "boletos" no fim (fala embolada).
"""
import sys
from pathlib import Path

import motor as m
from motor import (BALANCA, COLUNAS, LINHA_HTML, bloco_html, carimbo, centro, foto, foto_card, kick, no, outro, pilula,
                   po, preparar_seq, risco, texto, traco)

m.AQUI = Path(__file__).resolve().parent
F = m.AQUI.parent / "fontes"
m.CFG.update({"src": F / "v1.mp4", "serie": "Gestante e insalubridade", "corrige": {}, "destaques": set()})

GEST = {"src": F / "v1.mp4", "transcricao": F / "v1.json",
        "corrige": {"perigos": "perigo", "grave": "gravidez", "desde": "de", "deis": "", "tirando": "tirando-a", "-a": "",
                    "100": "100%", "%": "", "insalobridade": "insalubridade"},
        "destaques": {"2017", "máxima.", "atestado", "inconstitucional.", "automático.", "empregador", "imediatamente.", "salário",
                      "transferir", "risco.", "maternidade", "protegida.", "adicional", "inss", "lactante.", "amamentando",
                      "salubre", "6", "pausas", "30", "desconto"}}


def linha_ok(txt, at, top):
    return bloco_html(f'<div style="font-size:38px;font-weight:700;display:flex;gap:18px;align-items:center"><span style="color:#C9A962">✓</span>{txt}</div>',
                      at, top, 90, 900, anim="desliza", dx=-300, padding="22px 34px")


def niveis(at, top=430):
    """Graus de insalubridade: em 2017 só o máximo afastava."""
    def barra(nome, alt, cor):
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">'
                f'<div style="width:150px;height:{alt}px;border-radius:14px;background:{cor}"></div>'
                f'<div style="font-size:30px;font-weight:800;letter-spacing:2px;color:#FAF6F0">{nome}</div></div>')
    html = ('<div style="display:flex;justify-content:space-around;align-items:flex-end;height:330px">'
            + barra("MÍNIMO", 110, "rgba(232,222,209,.35)") + barra("MÉDIO", 190, "rgba(232,222,209,.55)")
            + barra("MÁXIMO", 280, "linear-gradient(180deg,#F4E6BC,#C9A962)") + '</div>')
    return bloco_html(html, at, top, 100, 880, anim="pop", padding="30px 26px")


def g1(W, seg, fim):
    """Gestante e insalubridade 1/3 · afastamento automático."""
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("g1_fabrica", "v-fabrica-mulher-1", 0.5, 7.5), "kb": [1.2, 1.05, 0, 0, -40, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.86), rgba(26,21,17,.35) 45%, rgba(26,21,17,.9))", "els": [
            kick("Gestante e insalubridade", 0.05),
            texto("Grávida em|<em>local insalubre</em>?", 0.08, 410, size=118),
            pilula("esforço físico", W("esforço"), 720, left=90, style={"fontSize": "34px"}),
            pilula("produtos nocivos", W("produtos"), 720, left=480, style={"fontSize": "34px"})]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-fabrica-2"), "blur": 8, "kb": [1.06, 1.14, 0, 0, 0, -20]},
         "veu": "rgba(26,21,17,.78)", "els": [
            kick("Como era desde 2017", seg[1] + .1),
            niveis(W("máxima.") - .6, top=430),
            pilula("só o máximo afastava", W("máxima."), 880, left=0, style=centro(560)),
            carimbo("Só com atestado", W("atestado"), 960, 230, rot=-6, size=66)]},
        {"a": seg[2], "trans": "iris", "irisY": 40, "particulas": 24, "els": [
            pilula("STF · ADI 5938", seg[2] + .1, 360, left=0, style=centro(360)),
            traco(COLUNAS, seg[2] + .1, 440, 270, 540, 410, dur=1.3, stagger=.07),
            carimbo("Inconstitucional", W("inconstitucional."), 900, 150, rot=-6, size=68)]},
        {"a": W("Hoje,"), "trans": "tinta", "tdur": .7, "bg": {**preparar_seq("g1_gest", "v-gestante-negra-0", 0.5, 7.0), "blur": 7},
         "veu": "rgba(26,21,17,.74)", "els": [
            kick("Hoje", W("Hoje,") + .05),
            po("100%", W("100%"), 540, 560, size=280),
            texto("<em>automático</em>, em qualquer grau", W("automático."), 760, size=72, align="center", anim="sobe"),
            pilula("sem atestado médico", W("Não", W("automático.")), 900, left=0, style=centro(520))]},
        {"a": seg[3], "trans": "luz", "bg": {"src": foto("f-gestante-negra-3"), "kb": [1.05, 1.12, 0, 0, 120, 100]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.35) 40%, rgba(26,21,17,.25) 60%, rgba(26,21,17,.9))", "els": [
            texto("Quem age agora|é a <em>empresa</em>", W("empregador"), 380, size=100),
            pilula("assim que sabe da gravidez", W("sabendo"), 610, left=90, style={"fontSize": "32px"})]},
        outro(fim, "Parte 2 · O salário não cai", "uma gestante", gestante=True),
    ]


def g2(W, seg, fim):
    """Gestante e insalubridade 2/3 · o salário não cai."""
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-gestante-negra-5"), "kb": [1.16, 1.04, 0, 0, 60, 120]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.4) 40%, rgba(26,21,17,.3) 60%, rgba(26,21,17,.9))", "els": [
            kick("Gestante afastada", 0.05),
            texto("Meu salário|<em>vai cair</em>?", 0.08, 400, size=130)]},
        {"a": seg[1], "trans": "whipV", "bg": {"src": foto("f-laboratorio-1"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            kick("O caminho na lei", seg[1] + .05),
            {"tipo": "linha", "html": LINHA_HTML, "at": seg[1] + .2, "ateFim": W("casa,", seg[3]) + .2,
             "style": {"top": "560px", "left": "180px", "width": "720px"}},
            no("Passo 1", W("Passo"), 180, top=560, sub="outra função segura"),
            no("Passo 2", W("passo", seg[3]), 540, top=560, sub="gravidez de risco"),
            no("Passo 3", W("3,"), 900, top=560, sub="em casa"),
            carimbo("Salário-maternidade", W("salário", seg[3]), 830, 150, rot=-5, size=66)]},
        {"a": seg[4], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-gestante-trabalho2-0"), "blur": 8}, "veu": "rgba(26,21,17,.76)", "els": [
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:24px;font-weight:800;letter-spacing:3px;color:#8E6E2E"><span>CONTRACHEQUE</span><span>AFASTADA</span></div>'
                       '<div style="display:flex;justify-content:space-between;font-size:36px;margin-top:30px"><span>Salário base</span><b>mantido ✓</b></div>',
                       W("mantém") - .1, 410, 110, 860, cls="papel", transform="rotate(-2deg)"),
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:36px;color:#2B231C"><span>Adicional de insalubridade</span><b>✓</b></div>',
                       W("adicional"), 600, 110, 860, cls="papel", anim="desliza", transform="rotate(-2deg)", padding="24px 40px"),
            carimbo("Não perde nada", W("nada."), 800, 200, rot=-7, size=64)]},
        {"a": seg[5], "trans": "zoom", "particulas": 22, "els": [
            kick("Quem paga a conta", seg[5] + .05),
            no("Empresa", W("empresa", seg[5]), 260, top=520), no("Você", W("paga.", seg[5]), 820, top=520, sub="salário em dia"),
            traco('<path class="desenha" d="M10 30 L420 30 M380 5 L420 30 L380 55"/>', W("paga.", seg[5]), 487, 330, 430, 60, dur=.6),
            no("INSS", W("INSS"), 260, top=880, sub="devolve à empresa"),
            traco('<path class="desenha" d="M30 250 L30 10 M5 50 L30 10 L55 50"/>', W("INSS"), 615, 230, 60, 260, dur=.6)]},
        outro(fim, "Parte 3 · Mãe que amamenta", "uma gestante", gestante=True),
    ]


def g3(W, seg, fim):
    """Gestante e insalubridade 3/3 · lactante."""
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-amamenta-4"), "kb": [1.16, 1.04, 0, 0, 80, 140]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.4) 40%, rgba(26,21,17,.3) 60%, rgba(26,21,17,.9))", "els": [
            kick("Fim da licença", 0.05),
            texto("O bebê nasceu.|<em>E a volta?</em>", 0.08, 400, size=120)]},
        {"a": seg[1], "trans": "iris", "irisY": 42, "particulas": 22, "els": [
            pilula("STF · ADI 5938", seg[1] + .1, 360, left=0, style=centro(360)),
            traco(COLUNAS, seg[1] + .1, 440, 270, 540, 410, dur=1.2, stagger=.07),
            texto("Vale também para|<em>quem amamenta</em>", W("decisão"), 880, size=86, align="center")]},
        {"a": seg[2], "trans": "whip", "bg": {"src": foto("f-laboratorio-4"), "blur": 7}, "veu": "rgba(26,21,17,.76)", "els": [
            kick("Na volta ao trabalho", seg[2] + .05),
            texto("Setor insalubre?", W("insalubridade,"), 420, size=110),
            carimbo("Proibido", W("nenhum."), 640, 270, rot=-8, size=120),
            po("100% salubre", W("100%", seg[2]), 540, 960, size=130)]},
        {"a": seg[3], "trans": "tinta", "tdur": .7, "bg": {**preparar_seq("g3_mae", "v-mae-trabalho-0", 0.5, 12.5), "blur": 3, "kb": [1.04, 1.1, 0, 0, -170, -190]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.45) 45%, rgba(26,21,17,.9))", "els": [
            kick("Até o bebê fazer 6 meses", seg[3] + .05),
            po("2 pausas", W("2"), 540, 520, size=200),
            pilula("30 min", W("30"), 680, left=250, style={"fontSize": "40px"}),
            pilula("30 min", W("30") + .25, 680, left=580, style={"fontSize": "40px"}),
            carimbo("Sem desconto", W("desconto"), 820, 210, rot=-6, size=84)]},
        outro(fim, "Salve a série completa", "uma mãe que vai voltar", gestante=True),
    ]


def p13(W, seg, fim):
    """13º proporcional: o cálculo com exemplo."""
    meses = "".join(
        f'<div class="m{i}" style="text-align:center;padding:14px 0;border-radius:12px;font-size:28px;font-weight:800;'
        + ('background:linear-gradient(180deg,#F4E6BC,#C9A962);color:#231E1A' if i >= 7 else 'background:rgba(232,222,209,.14);color:#FAF6F0')
        + f'">{mm}</div>' for i, mm in enumerate("JFMAMJJASOND"))
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-novo-emprego-0"), "kb": [1.16, 1.04, 0, 0, 80, 120]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.4) 40%, rgba(26,21,17,.3) 60%, rgba(26,21,17,.9))", "els": [
            kick("13º proporcional", 0.05),
            texto("Começou no|<em>meio do ano</em>?", 0.08, 400, size=124),
            pilula("garantido por lei", W("garantido"), 690, left=90)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-calculadora-1"), "blur": 6}, "veu": "rgba(26,21,17,.74)", "els": [
            kick("Exemplo", seg[1] + .05),
            bloco_html('<div style="font-size:24px;font-weight:800;letter-spacing:3px;color:#8E6E2E">CONTRATO</div>'
                       '<div style="display:flex;justify-content:space-between;font-size:40px;margin-top:22px"><span>Salário</span><b>R$ 3.000</b></div>'
                       '<div style="display:flex;justify-content:space-between;font-size:40px;margin-top:12px"><span>Início</span><b>10 de agosto</b></div>',
                       W("salário") , 420, 110, 860, cls="papel", anim="pop", transform="rotate(-2deg)"),
            po("÷ 12", W("12"), 540, 860, size=200)]},
        {"a": seg[2], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-calendario-4"), "blur": 9}, "veu": "rgba(26,21,17,.78)", "els": [
            kick("E o mês quebrado?", seg[2] + .05),
            texto("Começou dia 10.|Agosto <em>conta</em>?", W("Como"), 420, size=100)]},
        {"a": seg[3], "trans": "zoom", "particulas": 22, "els": [
            kick("A regra dos 15 dias", seg[3] + .05),
            po("15 dias", W("15", seg[3]), 540, 500, size=200),
            carimbo("= mês inteiro", W("inteira."), 680, 250, rot=-6, size=84)]},
        {"a": seg[4], "trans": "luz", "bg": {"src": foto("f-calculadora-5"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            kick("Agosto a dezembro", seg[4] + .05),
            bloco_html(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px">{meses}</div>', seg[4] + .2, 430, 100, 880, anim="pop", padding="28px 30px"),
            po("5 fatias", W("cinco"), 540, 820, size=170)]},
        {"a": seg[5], "trans": "whipV", "particulas": 26, "els": [
            texto("R$ 3.000 ÷ 12 × 5", W("multiplicar"), 420, size=96, align="center", anim="sobe"),
            po("R$ 1.250", W("1.250"), 540, 720, size=230),
            pilula("no fim do ano", W("fim", seg[6]), 900, left=0, style=centro(400))]},
        outro(fim, "1ª parcela até 30/11", "quem começou este ano"),
    ]


def pensao(W, seg, fim):
    """Pensão: o mito dos 30%."""
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-crianca-escola-4"), "kb": [1.16, 1.04, 0, 0, 80, 140]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.4) 40%, rgba(26,21,17,.3) 60%, rgba(26,21,17,.9))", "els": [
            kick("Pensão alimentícia", 0.05),
            texto("Pensão é sempre|<em>30%</em>?", 0.08, 400, size=120),
            carimbo("Mito", W("mito"), 500, 330, rot=-12, size=120)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-crianca-escola-1"), "blur": 7, "kb": [1.06, 1.14, 0, 0, 100, 80]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.9), rgba(26,21,17,.4) 40%, rgba(26,21,17,.3) 60%, rgba(26,21,17,.9))", "els": [
            texto("Escola particular.|<em>E o valor?</em>", W("escola"), 400, size=104)]},
        {"a": seg[2], "trans": "iris", "irisY": 45, "particulas": 22, "els": [
            kick("Como a Justiça calcula", seg[2] + .05),
            traco(BALANCA, seg[2] + .1, 430, 340, 400, 400, dur=1.3),
            pilula("Necessidade", W("necessidade"), 860, left=90, style={"fontSize": "36px"}),
            pilula("Possibilidade", W("possibilidade."), 860, left=560, style={"fontSize": "36px"})]},
        {"a": seg[3], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-mercado-3"), "blur": 7, "kb": [1.05, 1.12, 0, 0, 160, 140]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.92), rgba(26,21,17,.5) 40%, rgba(26,21,17,.3) 60%, rgba(26,21,17,.9))", "els": [
            kick("Necessidade da criança", seg[3] + .05),
            pilula("Aluguel", W("aluguel,"), 410, left=90, style={"fontSize": "34px"}),
            pilula("Luz", W("luz,"), 410, left=330, style={"fontSize": "34px"}),
            pilula("Saúde", W("saúde,"), 410, left=490, style={"fontSize": "34px"}),
            pilula("Roupas", W("roupas"), 500, left=90, style={"fontSize": "34px"}),
            pilula("Lazer", W("lazer."), 500, left=330, style={"fontSize": "34px"})]},
        {"a": seg[4], "trans": "whipV", "bg": {"src": foto("f-balanca-0"), "blur": 8}, "veu": "rgba(26,21,17,.78)", "els": [
            kick("Possibilidade de quem paga", seg[4] + .05),
            texto("Não é só a|<em>carteira assinada</em>", W("não", seg[4]), 410, size=96),
            pilula("Rendas extras", W("rendas"), 680, left=90, style={"fontSize": "34px"}),
            pilula("Patrimônio", W("patrimônio"), 680, left=430, style={"fontSize": "34px"}),
            pilula("Padrão de vida", W("padrão"), 780, left=90, style={"fontSize": "34px"})]},
        {"a": seg[5], "trans": "corte", "bg": {**preparar_seq("p_martelo", "v-martelo-2", 0.5, 9.0), "blur": 4},
         "veu": "rgba(26,21,17,.74)", "els": [
            texto("Perdeu o emprego?|<em>Nada muda sozinho</em>", seg[5] + .1, 400, size=92),
            texto("Cortar por conta própria", W("Cortar"), 660, size=64, cg=False, anim="sobe"),
            carimbo("Pode dar prisão", W("prisão."), 790, 190, rot=-7, size=88)]},
        {"a": seg[6], "trans": "luz", "bg": {"src": foto("f-familia-negra-4"), "blur": 6}, "veu": "rgba(26,21,17,.74)", "els": [
            kick("O caminho certo", seg[6] + .05),
            po("Ação revisional", W("revisional."), 540, 520, size=130),
            linha_ok("Provas em documentos", W("provas"), 700),
            linha_ok("O juiz reequilibra", W("balança"), 830)]},
        outro(fim, "Pensão é direito do filho", "quem paga ou recebe pensão", area="Direito de Família"),
    ]


def regras13(W, seg, fim):
    """13º: as 4 regras (véspera da 1ª parcela)."""
    def regra(n, nome, at):
        return po(f"Regra {n}", at, 540, 470, size=150), pilula(nome, at + .5, 560, left=0, style=centro(700))
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-calculadora-1"), "kb": [1.2, 1.05, 0, 0, -40, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.86), rgba(26,21,17,.4) 45%, rgba(26,21,17,.9))", "els": [
            kick("13º salário", 0.05),
            texto("Seu 13º está|<em>correto</em>?", 0.08, 410, size=130),
            po("4 regras", W("quatro"), 540, 820, size=200)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-calendario-2"), "blur": 8}, "veu": "rgba(26,21,17,.78)", "els": [
            *regra(1, "Prazos e impostos", seg[1] + .05),
            linha_ok("1ª parcela até 30/11, sem desconto", W("30", seg[1]), 690),
            linha_ok("2ª até 18/12, com INSS e IR", W("Como", seg[1]), 820)]},
        {"a": seg[2], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-calendario-4"), "blur": 9}, "veu": "rgba(26,21,17,.78)", "els": [
            *regra(2, "Contagem dos meses", seg[2] + .05),
            carimbo("15 dias = 1 mês", W("15", seg[2]), 720, 220, rot=-6, size=84)]},
        {"a": seg[3], "trans": "luz", "bg": {"src": foto("f-noite-4"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            *regra(3, "O que soma e o que protege", seg[3] + .05),
            pilula("Horas extras", W("horas"), 680, left=90, style={"fontSize": "32px"}),
            pilula("Adicional noturno", W("adicional"), 680, left=440, style={"fontSize": "32px"}),
            pilula("Comissões", W("comissões"), 770, left=90, style={"fontSize": "32px"}),
            carimbo("Atestado e licença não reduzem", W("diminuem"), 880, 100, rot=-4, size=48)]},
        {"a": seg[4], "trans": "zoom", "bg": {"src": foto("f-rh-0"), "blur": 8}, "veu": "rgba(26,21,17,.8)", "els": [
            *regra(4, "Rescisão", seg[4] + .05),
            linha_ok("Pediu demissão: recebe", W("Pediu"), 690),
            linha_ok("Sem justa causa: recebe", W("justa", seg[4]), 820),
            carimbo("Justa causa: perde", W("zera"), 960, 230, rot=-6, size=64)]},
        outro(fim, "1ª parcela: até 30/11", "quem espera o 13º"),
    ]


REELS = {
    1: {**GEST, "trechos": [(137.65, 144.95), (186.35, 201.95), (209.6, 222.4), (228.12, 238.9)], "roteiro": g1,
        "serie": "Insalubridade · 1/3", "nome": "gestante-insalubridade-1"},
    2: {**GEST, "trechos": [(245.48, 251.2), (256.25, 262.7), (262.9, 264.2), (269.85, 281.3), (297.42, 312.5), (312.85, 324.6)],
        "roteiro": g2, "serie": "Insalubridade · 2/3", "nome": "gestante-insalubridade-2"},
    3: {**GEST, "trechos": [(335.9, 342.6), (346.7, 356.3), (356.75, 370.5), (374.0, 386.4)], "roteiro": g3,
        "serie": "Insalubridade · 3/3", "nome": "gestante-insalubridade-3"},
    4: {"src": F / "v6.mp4", "transcricao": F / "v6.json", "roteiro": p13, "serie": "13º proporcional", "nome": "13-proporcional-calculo",
        "trechos": [(0.0, 5.3), (10.38, 18.5), (23.0, 30.45), (30.92, 36.72), (37.2, 43.05), (43.55, 48.0), (48.32, 55.25)],
        "corrige": {"R": "R$", "$": "", "3": "3.000", ".000": "", "1250": "1.250"},
        "destaques": {"proporcional", "garantido", "3.000", "agosto.", "12", "15", "inteira.", "cinco", "1.250"}},
    5: {"src": F / "v3.mp4", "transcricao": F / "v3.json", "roteiro": pensao, "serie": "Pensão alimentícia", "nome": "pensao-mito-30",
        "trechos": [(0.0, 4.4), (5.0, 9.95), (10.8, 19.85), (20.6, 29.95), (30.35, 39.72), (40.5, 49.05), (49.6, 51.8), (52.3, 57.2)],
        "corrige": {"30": "30%", "%": ""}, "sem_legenda": [[0, 4.4]],  # o título já diz a frase; rosto da criança livre
        "destaques": {"mito", "30%", "necessidade", "possibilidade.", "aluguel,", "saúde,", "patrimônio", "automático.", "prisão.", "revisional.", "provas"}},
    6: {"src": F / "v4.mp4", "transcricao": F / "v4.json", "roteiro": regras13, "serie": "13º · as 4 regras", "nome": "13-quatro-regras",
        "trechos": [(0.0, 9.9), (10.4, 26.35), (26.9, 34.55), (36.4, 49.92), (50.9, 61.15)],
        "corrige": {"testados": "atestados", "a@44.88": "", "recisão.": "rescisão."},
        "destaques": {"correto?", "quatro", "30", "18.", "15", "extras,", "noturno", "comissões", "diminuem", "proporcional.", "zera"}},
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
