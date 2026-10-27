"""Série 22 v2 · Demissão por vingança depois da eleição (assédio eleitoral), Reels animado sem a Dra. em cena (27/10/2026).
Pedido da Jessica: "reels completo sobre assédio eleitoral em vingança", "com animações", "toda aquela estratégia para
viralizar". A v1 (serie.py + roteiro.txt) fica intacta. Voz clonada da Dra. (fontes/roteiro-vinganca.txt → narrar.py).

Estratégia (docs/ESTRATEGIA_CRESCIMENTO_ORGANICO.md): gancho na tela no quadro 0 com a pergunta da pessoa; número em pó
de ouro aos 4 s (prova social: "não é só com você"); carimbo do nome na lei; virada "2x" perto de 65%; lista de provas
para salvar; "Salve e mande para quem precisa saber" (envio pesa 3 a 5x a curtida); cortes a cada 2-4 s; menos de 45 s.
Dois ganchos com o mesmo corpo: Reels 1 = gancho A (seguidores, terça/sexta 21h); Reels 2 = gancho B (Trial Reels).
Neutro: nenhum partido nem candidato (OAB). Fotos reais de urna (pedido "todos inclua fotos das urnas brasileiras").

Fatos (briefing producao/campanhas/2026-10-assedio-eleitoral/BRIEFING.md):
- 140 denúncias ao MPT em 26/10/2026, um dia depois do 2º turno, maior número num único dia em 2026.
- Voto secreto: CF, art. 14. Ninguém privado de direitos por convicção política: CF, art. 5º, VIII. Convenção 111 OIT.
- Dispensa discriminatória: Lei 9.029/1995, art. 1º; art. 4º: à escolha do empregado, reintegração com ressarcimento
  integral do período (I) ou o dobro da remuneração do período de afastamento (II); dano moral à parte.
- Denúncia sigilosa no site do MPT.
Banco: creditos-pexels.txt; urnas: producao/campanhas/2026-10-assedio-eleitoral/urnas/creditos.json.
Uso: NARRACAO=vinganca py serie_vinganca.py [1|2] [--amostras | --checar]
     (NARRACAO=vinganca-voz-provisoria monta a prévia com a voz antiga; o arquivo sai com PREVIA no nome)
"""
import json
import os
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, kick, outro, pilula, po, texto
import diagramas as dg
from serie import VEU, VEU_DG, cena

m.AQUI = Path(__file__).resolve().parent
NARRACAO = os.environ.get("NARRACAO", "vinganca")
FONTES = m.AQUI.parent / "fontes" / NARRACAO
PREVIA = "provisoria" in NARRACAO
m.CFG.update({"src": FONTES / "narracao.wav", "serie": "Demissão por causa do voto", "corrige": {},
              "destaques": {"vingança", "eleição", "emprego", "quarenta", "secreto", "votou:", "discriminatória",
                            "voltar", "dobro", "moral", "grupo", "testemunhas", "sigilosa"}})

CREDITO = {"urna-confirma": "Foto: Alejandro Zambrana/TSE",
           "urna-mao-teclado": "Foto: Marri Nogueira/Agência Senado (CC BY 2.0)"}


def cena_foto(i, a, foto, els, trans="corte", veu=VEU, blur=0, kb=(1.0, 1.08), dy=(0, -24)):
    """Foto real (urna) em tela cheia com Ken Burns, véu café e o crédito pequeno no rodapé da área limpa."""
    bg = {"src": m.foto(foto), "kb": [kb[0], kb[1], 0, 0, dy[0], dy[1]]}
    if blur:
        bg["blur"] = blur
    credito = {"html": CREDITO[foto], "at": a + .1, "anim": "sobe",
               "style": {"top": "1010px", "left": "90px", "fontSize": "27px", "color": "rgba(232,222,209,.72)",
                         "fontWeight": "500"}}
    return {"a": a, "trans": trans, "bg": bg, "veu": veu, "els": [*els, credito]}


def gancho_a(W):
    return cena(0, 0, W("No"), "caixa", ini=1.0, kb=(1.12, 1.04), dy=(-40, -10), els=[
        kick("Depois da eleição", -1, top=370),
        texto("Demitido por|<em>vingança?</em>", -1, 440, size=124),
    ])


def gancho_b(W):
    return cena_foto(0, 0, "urna-confirma", blur=4, veu=VEU_DG, kb=(1.14, 1.04), dy=(-30, 0), els=[
        kick("A eleição acabou", -1, top=370),
        texto("Seu voto não pode|custar o seu <em>emprego</em>", -1, 440, size=100),
    ])


def corpo(W, fim, gancho):
    """Mesmo corpo para os dois ganchos: número → regra → nome na lei → a escolha (2x) → provas → denúncia → fechamento."""
    a1 = W("No")
    a2 = W("O", a1)
    a3 = W("Demitir")
    a4 = W("A", a3)
    a5 = W("ou", a4)
    a6 = W("Antes")
    a7 = W("E", W("testemunhas."))
    return [
        gancho(W),
        cena(1, a1, a2, "celular", trans="whip", ini=2.0, blur=3, els=[
            kick("Um dia depois do 2º turno", a1 + .05, top=380),
            po("140", W("quarenta"), 540, 640, size=300),
            texto("denúncias ao|<em>Ministério Público</em>", W("denúncias"), 830, size=70, align="center", anim="sobe"),
            pilula("Recorde no ano", W("Trabalho.") + .2, 1010, left=0, style=centro(420)),
        ]),
        cena_foto(2, a2, "urna-mao-teclado", trans="tinta", blur=3, veu=VEU_DG, els=[
            texto("O voto é|<em>secreto</em>", a2 + .05, 420, size=120),
            texto("Não importa em|quem <em>você votou</em>", W("Não", a2), 700, size=76, anim="sobe"),
            pilula("Constituição, arts. 5º e 14", W("ninguém"), 900, left=90),
        ]),
        cena(3, a3, a4, "abatido", trans="corte", ini=0.5, blur=7, veu=VEU_DG, els=[
            texto("Demitir por <em>vingança</em>", a3 + .05, 430, size=92, align="center"),
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
            kick("Antes de sair do grupo da empresa", a6 + .05, top=360),
            *dg.etapas([("Mensagens e áudios", W("mensagens,")), ("Prints de grupos e posts", W("prints")),
                        ("Testemunhas", W("testemunhas."))], top=450, gap=160),
        ]),
        cena(7, a7, fim - .1, "notebook", trans="whip", ini=12.0, veu=VEU_DG, blur=4, els=[
            *dg.escudo(a7 + .1, "Denúncia sigilosa no MPT", top=400),
        ]),
        outro(fim - .1, "Passo a passo: link na bio", "quem precisa saber"),
    ]


def _reel(parte, gancho):
    trans = FONTES / "transcricao.json"
    seg = json.loads(trans.read_text(encoding="utf-8"))["segments"][parte]
    fim = min(seg["end"], seg["words"][-1]["end"] + 0.25)
    prefixo = "PREVIA-voz-provisoria-demissao-por-vinganca-" if PREVIA else "demissao-por-vinganca-motion-"
    return {"src": FONTES / "narracao.wav", "transcricao": trans, "trechos": [(seg["start"], round(fim, 2))],
            "roteiro": lambda W, s, f: corpo(W, f, gancho), "serie": "Demissão por causa do voto",
            "prefixo": prefixo, "punch": 1.0}


REELS = {1: _reel(0, gancho_a), 2: _reel(1, gancho_b)}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
