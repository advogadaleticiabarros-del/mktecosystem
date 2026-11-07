"""Gestante e insalubridade 1/3, 2/3, 3/3 e Pensão: o mito dos 30%, versão 2 (07/11/2026, pedido da Jessica: "agora
faça os de gestante e também substitua pelo que já está programado, faça a série inteira" + "pensao-mito-30 esse
também" + "procure efeitos sonoros melhores").
Mesmo tratamento aprovado nos Reels do 13º (eixo central x=540, rosto sem texto nítido por cima), com os efeitos
sonoros v3 (som3.py, gravações reais da Mixkit). Narração, trechos e fatos iguais à v1 (serie2.py).
Uso: py serie_gest_v2.py 11 12 13 15 [--checar | --amostras]. Saída: ../<nome>-v2.mp4 (a v1 fica intacta)."""
import sys

import motor as m
import serie2
import som3
from motor import BALANCA, COLUNAS, LINHA_HTML, bloco_html, foto, no, outro, pilula, po, preparar_seq, traco
from serie2 import linha_ok, niveis
from v2base import CX, VEU_ROSTO, cc, kc, pc, tc

m.sfx = lambda pasta: som3.efeitos_v3(m.AQUI / "sfx3")


def par(a, at_a, b, at_b, top, w=400, fs="30px"):
    """Duas pílulas lado a lado, simétricas em relação ao eixo central."""
    st = {"width": f"{w}px", "textAlign": "center", "fontSize": fs}
    return pilula(a, at_a, top, left=CX - w - 12, style=st), pilula(b, at_b, top, left=CX + 12, style=st)


def g1v2(W, seg, fim):
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("g1_fabrica", "v-fabrica-mulher-1", 0.5, 7.5), "kb": [1.2, 1.05, 0, 0, -40, 0], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            kc("Gestante e insalubridade", 0.05),
            tc("Grávida em|<em>local insalubre</em>?", 0.08, 420, size=118),
            *par("esforço físico", W("esforço"), "produtos nocivos", W("produtos"), 740)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-fabrica-2"), "blur": 8, "kb": [1.06, 1.14, 0, 0, 0, -20]},
         "veu": "rgba(26,21,17,.8)", "els": [
            kc("Como era desde 2017", seg[1] + .1),
            niveis(W("máxima.") - .6, top=430),
            pc("só o máximo afastava", W("máxima."), 880),
            cc("Só com atestado", W("atestado"), 980, size=60, rot=-5)]},
        {"a": seg[2], "trans": "iris", "irisY": 40, "particulas": 24, "els": [
            pc("STF · ADI 5938", seg[2] + .1, 360, 360),
            traco(COLUNAS, seg[2] + .1, 440, 270, 540, 410, dur=1.3, stagger=.07),
            cc("Inconstitucional", W("inconstitucional."), 900, size=68, rot=-5)]},
        {"a": W("Hoje,"), "trans": "tinta", "tdur": .7, "bg": {**preparar_seq("g1_gest", "v-gestante-negra-0", 0.5, 7.0), "blur": 8},
         "veu": VEU_ROSTO, "els": [
            kc("Hoje", W("Hoje,") + .05),
            po("100%", W("100%"), CX, 560, size=280),
            tc("<em>automático</em>, em qualquer grau", W("automático."), 760, size=72, anim="sobe"),
            pc("sem atestado médico", W("Não", W("automático.")), 900, 520)]},
        {"a": seg[3], "trans": "luz", "bg": {"src": foto("f-gestante-negra-3"), "kb": [1.05, 1.12, 0, 0, 120, 100], "blur": 8},
         "veu": VEU_ROSTO, "els": [
            tc("Quem age agora|é a <em>empresa</em>", W("empregador"), 400, size=100),
            pc("assim que sabe da gravidez", W("sabendo"), 640, 600, fontSize="32px")]},
        outro(fim, "Parte 2 · O salário não cai", "uma gestante", gestante=True),
    ]


def g2v2(W, seg, fim):
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-gestante-negra-5"), "kb": [1.16, 1.04, 0, 0, 60, 120], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            kc("Gestante afastada", 0.05),
            tc("Meu salário|<em>vai cair</em>?", 0.08, 420, size=130)]},
        {"a": seg[1], "trans": "whipV", "bg": {"src": foto("f-laboratorio-1"), "blur": 9}, "veu": "rgba(26,21,17,.8)", "els": [
            kc("O caminho na lei", seg[1] + .05),
            {"tipo": "linha", "html": LINHA_HTML, "at": seg[1] + .2, "ateFim": W("casa,", seg[3]) + .2,
             "style": {"top": "560px", "left": "180px", "width": "720px"}},
            no("Passo 1", W("Passo"), 180, top=560, sub="outra função segura"),
            no("Passo 2", W("passo", seg[3]), CX, top=560, sub="gravidez de risco"),
            no("Passo 3", W("3,"), 900, top=560, sub="em casa"),
            cc("Salário-maternidade", W("salário", seg[3]), 840, size=48, rot=-4)]},
        {"a": seg[4], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-gestante-trabalho2-0"), "blur": 8}, "veu": VEU_ROSTO, "els": [
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:27px;font-weight:800;letter-spacing:3px;color:#8E6E2E"><span>CONTRACHEQUE</span><span>AFASTADA</span></div>'
                       '<div style="display:flex;justify-content:space-between;font-size:36px;margin-top:30px"><span>Salário base</span><b>mantido ✓</b></div>',
                       W("mantém") - .1, 410, 110, 860, cls="papel"),
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:36px;color:#2B231C"><span>Adicional de insalubridade</span><b>✓</b></div>',
                       W("adicional"), 600, 110, 860, cls="papel", anim="sobe", padding="24px 40px"),
            cc("Não perde nada", W("nada."), 800, size=64, rot=-5)]},
        {"a": seg[5], "trans": "zoom", "particulas": 22, "els": [
            kc("Quem paga a conta", seg[5] + .05),
            no("Empresa", W("empresa", seg[5]), 260, top=520), no("Você", W("paga.", seg[5]), 820, top=520, sub="salário em dia"),
            traco('<path class="desenha" d="M10 30 L420 30 M380 5 L420 30 L380 55"/>', W("paga.", seg[5]), 487, 330, 430, 60, dur=.6),
            no("INSS", W("INSS"), 260, top=880, sub="devolve à empresa"),
            traco('<path class="desenha" d="M30 250 L30 10 M5 50 L30 10 L55 50"/>', W("INSS"), 615, 230, 60, 260, dur=.6)]},
        outro(fim, "Parte 3 · Mãe que amamenta", "uma gestante", gestante=True),
    ]


def g3v2(W, seg, fim):
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-amamenta-4"), "kb": [1.16, 1.04, 0, 0, 80, 140], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            kc("Fim da licença", 0.05),
            tc("O bebê nasceu.|<em>E a volta?</em>", 0.08, 420, size=120)]},
        {"a": seg[1], "trans": "iris", "irisY": 42, "particulas": 22, "els": [
            pc("STF · ADI 5938", seg[1] + .1, 360, 360),
            traco(COLUNAS, seg[1] + .1, 440, 270, 540, 410, dur=1.2, stagger=.07),
            tc("Vale também para|<em>quem amamenta</em>", W("decisão"), 880, size=86)]},
        {"a": seg[2], "trans": "whip", "bg": {"src": foto("f-laboratorio-4"), "blur": 8}, "veu": "rgba(26,21,17,.8)", "els": [
            kc("Na volta ao trabalho", seg[2] + .05),
            tc("Setor insalubre?", W("insalubridade,"), 430, size=110),
            cc("Proibido", W("nenhum."), 640, size=120, rot=-6),
            po("100% salubre", W("100%", seg[2]), CX, 960, size=130)]},
        {"a": seg[3], "trans": "tinta", "tdur": .7, "bg": {**preparar_seq("g3_mae", "v-mae-trabalho-0", 0.5, 12.5), "blur": 8, "kb": [1.04, 1.1, 0, 0, -170, -190]},
         "veu": VEU_ROSTO, "els": [
            kc("Até o bebê fazer 6 meses", seg[3] + .05),
            po("2 pausas", W("2"), CX, 520, size=200),
            *par("30 min", W("30"), "30 min", W("30") + .25, 680, w=240, fs="40px"),
            cc("Sem desconto", W("desconto"), 830, size=84, rot=-5)]},
        outro(fim, "Salve a série completa", "uma mãe que vai voltar", gestante=True),
    ]


def pensaov2(W, seg, fim):
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("f-crianca-escola-4"), "kb": [1.16, 1.04, 0, 0, 80, 140], "blur": 7},
         "veu": VEU_ROSTO, "els": [
            kc("Pensão alimentícia", 0.05),
            tc("Pensão é sempre|<em>30%</em>?", 0.08, 420, size=120),
            cc("Mito", W("mito"), 720, size=130, rot=-8)]},
        {"a": seg[1], "trans": "whip", "bg": {"src": foto("f-crianca-escola-1"), "blur": 8, "kb": [1.06, 1.14, 0, 0, 100, 80]},
         "veu": VEU_ROSTO, "els": [
            tc("Escola particular.|<em>E o valor?</em>", W("escola"), 430, size=104)]},
        {"a": seg[2], "trans": "iris", "irisY": 45, "particulas": 22, "els": [
            kc("Como a Justiça calcula", seg[2] + .05),
            traco(BALANCA, seg[2] + .1, 430, 340, 400, 400, dur=1.3),
            *par("Necessidade", W("necessidade"), "Possibilidade", W("possibilidade."), 860, fs="36px")]},
        {"a": seg[3], "trans": "tinta", "tdur": .7, "bg": {"src": foto("f-mercado-3"), "blur": 8, "kb": [1.05, 1.12, 0, 0, 160, 140]},
         "veu": VEU_ROSTO, "els": [
            kc("Necessidade da criança", seg[3] + .05),
            *par("Aluguel", W("aluguel,"), "Luz", W("luz,"), 440, w=300),
            *par("Saúde", W("saúde,"), "Roupas", W("roupas"), 540, w=300),
            pc("Lazer", W("lazer."), 640, 300, fontSize="34px")]},
        {"a": seg[4], "trans": "whipV", "bg": {"src": foto("f-balanca-0"), "blur": 8}, "veu": "rgba(26,21,17,.8)", "els": [
            kc("Possibilidade de quem paga", seg[4] + .05),
            tc("Não é só a|<em>carteira assinada</em>", W("não", seg[4]), 420, size=96),
            *par("Rendas extras", W("rendas"), "Patrimônio", W("patrimônio"), 690),
            pc("Padrão de vida", W("padrão"), 790, 370, fontSize="34px")]},
        {"a": seg[5], "trans": "corte", "bg": {**preparar_seq("p_martelo", "v-martelo-2", 0.5, 9.0), "blur": 5},
         "veu": "rgba(26,21,17,.78)", "els": [
            tc("Perdeu o emprego?|<em>Nada muda sozinho</em>", seg[5] + .1, 400, size=92),
            tc("Cortar por conta própria", W("Cortar"), 660, size=64, cg=False, anim="sobe"),
            cc("Pode dar prisão", W("prisão."), 800, size=74, rot=-5)]},
        {"a": seg[6], "trans": "luz", "bg": {"src": foto("f-familia-negra-4"), "blur": 8}, "veu": VEU_ROSTO, "els": [
            kc("O caminho certo", seg[6] + .05),
            po("Ação revisional", W("revisional."), CX, 520, size=130),
            linha_ok("Provas em documentos", W("provas"), 700),
            linha_ok("O juiz reequilibra", W("balança"), 830)]},
        outro(fim, "Pensão é direito do filho", "quem paga ou recebe pensão", area="Direito de Família"),
    ]


REELS = {
    11: {**serie2.REELS[1], "roteiro": g1v2, "nome": "gestante-insalubridade-1-v2"},
    12: {**serie2.REELS[2], "roteiro": g2v2, "nome": "gestante-insalubridade-2-v2"},
    13: {**serie2.REELS[3], "roteiro": g3v2, "nome": "gestante-insalubridade-3-v2"},
    15: {**serie2.REELS[5], "roteiro": pensaov2, "nome": "pensao-mito-30-v2"},
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
