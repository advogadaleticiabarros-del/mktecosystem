"""Série 23 · Novos Reels 3 (16/11/2026), estilo INTEIRO COM BANCO (Jessica: "inteiro com banco"), com as animações da
tela dividida descidas para o quadro cheio, como a série 19 inteiro-motion (motor/ + engine.html, fx.js e diagramas.py
da motor-dividida/). Pedido: "faça todas as animações e deixe o vídeo dinâmico, com cenas, gancho inicial com efeito
(mesmo que a cena se repita), efeito sonoro; não mexa no som nem na qualidade da imagem".
R1 (IMG_2092) Intermitente: o 13º e as férias já vêm no valor da diária.
R2 (IMG_2093) Intermitente de fachada: todo dia, por anos, sem poder recusar -> o contrato pode ser questionado.
Fala: ../fontes/falas.py (fatos, base legal e cortes no docstring de lá). 3D: motor3d/clip3d.py (semana, cofre, livro).
Banco: Pexels já baixado em séries anteriores (créditos em creditos-pexels.txt).
Uso: py serie.py [1 2] [--amostras | --checar]
"""
import subprocess
import sys
from pathlib import Path

import motor as m
from motor import carimbo, centro, contador, outro, pilula, preparar_seq, texto
import diagramas as dg

m.AQUI = Path(__file__).resolve().parent
m.CFG.update({"src": m.AQUI / "videos" / "fala-r1.mp4", "serie": "Contrato intermitente", "corrige": {},
              "destaques": {"intermitente.", "intermitente?", "bico,", "nome.", "diária.", "terço", "150", "subordinado,",
                            "testemunhas", "questionado,", "443,", "julgados,", "diferença.", "férias."}})

FACE_VEU = "linear-gradient(180deg, rgba(26,21,17,0) 0%, rgba(26,21,17,0) 52%, rgba(26,21,17,.45) 62%, rgba(26,21,17,.8) 100%)"  # rosto intacto
HOOK_VEU = "linear-gradient(180deg, rgba(26,21,17,.6) 0%, rgba(26,21,17,0) 22%, rgba(26,21,17,0) 52%, rgba(26,21,17,.45) 62%, rgba(26,21,17,.8) 100%)"
DIAGRAMA_VEU = "linear-gradient(180deg, rgba(26,21,17,.9) 0%, rgba(26,21,17,.76) 25%, rgba(26,21,17,.74) 60%, rgba(26,21,17,.92) 100%)"
DY = {1: -220, 2: -110}  # rosto baixo e perto nesta gravação: sobe o vídeo para o queixo ficar acima dos textos
ZB = 1.06
DESCE = 150
CORRIGE = {  # erros do Whisper na legenda (o áudio está certo)
    # R1
    "R@52.18": "", "$150,": "R$ 150,", "o@27.78": "um", "os@59.06": "",
    # R2
    "ali": "ele", "decimo": "décimo", "no@5.24": "não tinha", "no@17.40": "não tinha", "Trabalhador@6.16": "O trabalhador",
    "em@24.24": "dessa não", "vale": "válido", "do@52.08": "o", "10": "13º,", ".3.,": "", "para@59.54": "pra", "a@59.70": "",
    "receberia@69.02": "Receberia"}
FFPROBE = str(m.FF).replace("ffmpeg.exe", "ffprobe.exe")


def duracao(stock):
    arq = m.AQUI / "videos" / f"stock-{stock}.mp4"
    return float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def desce(els, dy=DESCE):
    for e in els:
        st = e.get("style", {})
        if str(st.get("top", "")).endswith("px"):
            st["top"] = f"{float(st['top'][:-2]) + dy:g}px"
        if "burst" in e:
            e["burst"]["y"] += dy
    return els


def rosto(n, i, a, b, kb=(1.0, 1.04), els=(), trans="corte"):
    z = ZB - 1.0
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_rosto{i}", f"fala-r{n}", a, b - a + 0.4), "rosto": True,
                                           "kb": [kb[0] + z, kb[1] + z, 0, 0, DY[n], DY[n] - 20]},
            "veu": FACE_VEU, "els": list(els)}


def gancho(n, b, els, kb=(1.2, 1.06)):
    """Gancho: a frase forte da Dra. (que volta depois na fala), entrando com zoom e a câmera recuando sobre o rosto."""
    z = ZB - 1.0
    return {"a": 0, "trans": "zoom", "bg": {**preparar_seq(f"r{n}_gancho", f"fala-r{n}", 0, b + 0.4), "rosto": True,
                                            "kb": [kb[0] + z, kb[1] + z, 0, 0, DY[n], DY[n] - 20]},
            "veu": HOOK_VEU, "els": list(els)}


def diagrama(n, i, a, b, stock, els, trans="corte", ini=0.3):
    precisa, tem = ini + (b - a) + 0.4, duracao(stock)
    assert precisa <= tem, f"r{n} cena {i}: {precisa:.1f}s sobre o vídeo '{stock}' de {tem:.1f}s (a imagem congelaria)"
    return {"a": a, "trans": trans, "bg": {**preparar_seq(f"r{n}_dg{i}_{stock}", f"stock-{stock}", ini, b - a + 0.4), "kb": [1.0, 1.06, 0, 0, 0, -20]},
            "veu": DIAGRAMA_VEU, "els": desce(list(els))}


def chip(txt, at, w):
    return pilula(txt, at, 1005, left=0, style=centro(w))


def baixo(html, at):
    """Texto de uma linha nas cenas de rosto, abaixo do queixo e acima da legenda."""
    return texto(html, at, 985, size=52, align="center", anim="sobe")


def topo(html, at, size=64):
    """Título do gancho no alto do quadro, acima do rosto."""
    return texto(html, at, 200, size=size, align="center", anim="sobe")


def reel1(W, seg, fim):
    """Intermitente: o 13º e as férias já vêm na diária."""
    a1 = W("A", 3.0)
    ele, entao, esse1 = W("Ele"), W("Então", 12.0), W("Esse", 15.6)
    esse2 = W("Esse", esse1 + 1)
    nao, final = W("Não", esse2 + 1), W("final", esse2)
    porque = W("porque", final)
    assim = W("Assim")
    porque2 = W("porque", assim)
    se, meu = W("Se", porque2), W("Meu")
    return [
        gancho(1, a1, els=[
            topo("Trabalha por <em>diária</em>?", 0.05, size=68),
            baixo("Em dezembro, <em>o 13º não vem</em>.", W("décimo") - .2),
            carimbo("Cadê o 13º?", W("tem.") - .1, 360, 280, rot=-8, size=68)]),
        diagrama(1, 1, a1, ele, "3d-semana", ini=0.0, trans="whip", els=dg.titulo("A maioria não sabe que está no", a1 + .05,
                 "contrato intermitente") + [pilula("CLT, art. 452-A", W("intermitente.") + .1, 420, left=0, style=centro(420))]),
        diagrama(1, 2, ele, entao, "celular", els=dg.calendario(ele + .05, W("recusar"), W("24"))),
        rosto(1, 3, entao, esse1, kb=(1.06, 1.1), els=[chip("Recusou? Não recebe o dia", W("receberia"), 640)]),
        diagrama(1, 4, esse1, esse2, "trabalhador", trans="whip", els=dg.titulo("É o antigo", esse1 + .1, "bico")
                 + dg.relogio(W("hora,") - .3, 540, 640, acesas=1, size=260)
                 + [pilula("Pago pela hora ou pelo dia", W("hora,"), 830, left=0, style=centro(620))]),
        rosto(1, 5, esse2, nao, kb=(1.04, 1.08), els=[baixo("Agora tem nome: <em>intermitente</em>", esse2 + .1)]),
        rosto(1, 6, nao, final, kb=(1.08, 1.12), els=[chip("Não tira seus direitos", W("retira"), 560)]),
        diagrama(1, 7, final, porque, "espera", trans="luz", els=dg.dezembro(final + .05, W("tem,", final))),
        diagrama(1, 8, porque, assim, "calculadora", els=dg.contracheque([porque + .3, W("incluso"), W("diária.") + .1, W("diária.") + .5])),
        rosto(1, 9, assim, porque2, kb=(1.06, 1.1), els=[chip("Férias + ⅓ também vêm junto", W("terço"), 680)]),
        diagrama(1, 10, porque2, se, "3d-livro", ini=0.0, els=dg.titulo("Já está", porque2 + .05, "no valor da hora")
                 + [pilula("CLT, art. 452-A, §6º", W("inserido.") - .3, 430, left=0, style=centro(460))]),
        diagrama(1, 11, se, meu, "3d-cofre9", ini=0.0, trans="whip", els=[
            contador(0, 150, se + .1, 300, left=170, size=230, sufixo="reais/dia", dur=1.0),
            pilula("13º ✓", W("décimo", se), 640, left=0, style=centro(260)),
            pilula("Férias + ⅓ ✓", W("férias.", se), 740, left=0, style=centro(360))]
            + dg.fgts_deposito(W("férias.", se) + .5, top=840)),
        rosto(1, 12, meu, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", meu + .05, 520)]),
        outro(fim, "Parte 2 · Intermitente de fachada", "quem trabalha por diária"),
    ]


def reel2(W, seg, fim):
    """Intermitente de fachada: todo dia, por anos."""
    t2 = W("O trabalhador", 4.5)
    ia = W("Ia", t2)
    rep = W("trabalhou", ia)
    cheg = W("chegava", rep)
    tendo = W("Tendo")
    alt = W("alternância", tendo)
    test = W("testemunhas")
    claro, existe, mas = W("Claro"), W("Existe"), W("Mas", 40.0)
    inc, rec = W("Inclusive"), W("Receberia")
    ent1 = W("Então", rec)
    ent2 = W("Então", ent1 + .5)
    meu = W("Meu")
    return [
        gancho(2, t2, els=[
            topo("Todo dia, <em>por anos</em>…", 0.05, size=68),
            baixo("E o contrato era <em>intermitente</em>?", W("dias") - .3),
            carimbo("Sem 13º", W("terceiro") - .05, 360, 350, rot=-8, size=74)]),
        diagrama(2, 1, t2, ia, "3d-semana", ini=0.0, trans="whip", els=dg.titulo("E quando o intermitente", t2 + .05, "é só no papel?")
                 + [pilula("Nem sabia que era intermitente", W("sabia", t2), 420, left=0, style=centro(700))]),
        rosto(2, 2, ia, rep, kb=(1.06, 1.1), els=[chip("Trabalhava todos os dias", W("todos", ia), 600)]),
        diagrama(2, 3, rep, cheg, "trabalhador", els=dg.meses([rep + .1, W("4", rep), W("dias", rep)], W("dias", rep) + .5)),
        diagrama(2, 4, cheg, tendo, "espera", trans="luz", els=[
            texto("No fim do ano…", cheg + .05, 330, size=70, align="center", anim="sobe"),
            carimbo("Sem 13º", W("terceiro,", cheg) - .05, 520, 170, rot=-7, size=78),
            carimbo("Sem férias", W("férias", cheg) - .05, 700, 330, rot=6, size=78)]),
        rosto(2, 5, tendo, alt - .35, kb=(1.08, 1.12), els=[chip("Provas de subordinação", W("subordinado,", tendo), 600)]),
        diagrama(2, 6, alt - .35, test, "notebook", els=dg.papel_pratica(alt - .25, W("todos", alt))
                 + [pilula("Intermitente", alt + .2, 640, left=0, style={"left": "150px", "width": "300px", "textAlign": "center"}),
                    pilula("Todo dia", W("todos", alt) + .2, 580, left=0, style={"left": "640px", "width": "300px", "textAlign": "center"})]),
        diagrama(2, 7, test, claro, "assinatura", trans="whip", els=dg.etapas([("Ia todos os dias", test + .05), ("Recebia ordens", test + .35),
                                                                              ("Testemunhas confirmam", test + .65)], top=280)
                 + [carimbo("Pode ser questionado", W("questionado", test) - .1, 760, 170, rot=-6, size=64)]),
        rosto(2, 16, claro, W("previsto", claro), kb=(1.04, 1.08), els=[chip("O intermitente é legal", W("CLT,", claro), 520)]),
        diagrama(2, 8, W("previsto", claro), existe, "3d-livro", ini=0.0, els=dg.titulo("Está na lei", W("previsto", claro) + .05, "CLT, art. 443, §3º")
                 + [pilula("Reforma Trabalhista de 2017", W("parágrafo"), 430, left=0, style=centro(620))]),
        rosto(2, 9, existe, mas, kb=(1.04, 1.08), els=[chip("Muitos juízes validam o contrato", W("juiz"), 700)]),
        diagrama(2, 10, mas, inc, "chefe", trans="whip", els=dg.titulo("Mas há julgados", mas + .05, "que questionam")
                 + [pilula("Dá para levar ao Judiciário", W("judiciário", mas), 430, left=0, style=centro(620))]),
        diagrama(2, 11, inc, rec, "abatido", els=dg.etapas([("Vai todos os dias", W("vai", inc)), ("É subordinado", W("subordinado,", inc)),
                                                         ("Não pode recusar", W("recusar", inc))], top=300)),
        diagrama(2, 12, rec, ent1, "calculadora", trans="whip", els=dg.titulo("E aí, o que acontece?", rec + .02, "a diária vira salário")
                 + [pilula("CLT, art. 9º", W("diária,", rec), 430, left=0, style=centro(320))]),
        diagrama(2, 13, ent1, ent2, "contas", els=[
            texto("Fora do salário,|<em>cobrados à parte</em>:", ent1 + .05, 300, size=62, align="center", anim="sobe"),
            pilula("13º", W("13º", ent1), 560, left=0, style=centro(220)),
            pilula("Férias + ⅓", W("férias,", ent1), 660, left=0, style=centro(340)),
            pilula("FGTS", W("FGTS", ent1), 760, left=0, style=centro(220))]),
        rosto(2, 14, ent2, meu, kb=(1.06, 1.1), els=[chip("A diferença se cobra na Justiça", W("cobrar", ent2), 700)]),
        rosto(2, 15, meu, fim, kb=(1.02, 1.06), els=[chip("Dra. Letícia Barros", meu + .05, 520)]),
        outro(fim, "Parte 1 · O 13º já vem na diária", "quem trabalha todo dia"),
    ]


def _reel(n, roteiro, serie, prefixo):
    fim = m.fim_da_fala(m.AQUI / "videos" / f"fala-r{n}.transcricao.json", m.AQUI / "videos" / f"fala-r{n}.mp4")
    return {"src": m.AQUI / "videos" / f"fala-r{n}.mp4", "transcricao": m.AQUI / "videos" / f"fala-r{n}.transcricao.json",
            "trechos": [(0.0, round(fim, 2))], "roteiro": roteiro, "serie": serie, "prefixo": prefixo, "corrige": CORRIGE}


REELS = {
    1: _reel(1, reel1, "Contrato intermitente · 1/2", "intermitente-13-na-diaria-"),
    2: _reel(2, reel2, "Contrato intermitente · 2/2", "intermitente-de-fachada-"),
}

if __name__ == "__main__":
    m.rodar(REELS, sys.argv[1:])
