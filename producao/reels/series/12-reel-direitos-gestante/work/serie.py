"""Série "Direitos da gestante" em 3 Reels (09/10/2026), só com o áudio do vídeo do NotebookLM.

Para cada Reel: corta e trata a narração, gera efeitos sonoros e base instrumental próprios
(sem direitos de terceiros), prepara fotos e trechos de vídeo do Pexels, monta as cenas
(motion graphics contextual em engine.html), renderiza quadro a quadro e codifica em H.264.

Uso: py serie.py [1 2 3]
Fatos: ADCT art. 10 II b; STF Tema 497; CLT art. 392 §4º; Lei 11.770/2008; STF ADI 6327.
"""
import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
SRC = Path(r"C:\Users\prosy\Desktop\Direitos_da_Gestante_no_Brasil.mp4")
FF = Path(r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe")
ASSETS = Path(r"C:\Users\prosy\mktecosystem\apps\api\app\assets")
FPS = 30
OUTRO = 3.4
CORRIGE = {"validez": "vale desde", "-natal": "pré-natal", "pré": ""}
DESTAQUES = {"grávida", "emprego", "demissão", "justa", "causa", "concepção", "cinco", "meses", "parto", "não", "soubesse",
             "empregador", "seis", "consultas", "exames", "descontado", "salário", "120", "180", "dias", "cidadã", "poder",
             "mito", "justificada", "piso", "mínimo", "atestado", "obrigação", "internados", "hospital", "stf", "alta",
             "internação", "semanas", "garantido", "contrato", "ativo", "final", "licença"}


def ff(*args) -> None:
    subprocess.run([str(FF), "-v", "error", "-y", *map(str, args)], check=True)


# --------------------------------------------------------------------------- áudio e palavras
def palavras_do_reel(trechos: list[tuple[float, float]]):
    r = json.loads((AQUI / "transcricao.json").read_text(encoding="utf-8"))
    todas = [w for s in r["segments"] for w in s["words"]]
    t, linha, ws = 0.0, [], []
    for a, b in trechos:
        dur = round(b - a, 3)
        linha.append({"ini_src": a, "fim_src": b, "ini": t, "fim": t + dur})
        for w in todas:
            if w["start"] >= a - 0.05 and w["start"] < b - 0.03 and w["end"] <= b + 0.15:
                txt = CORRIGE.get(w["word"].strip(), w["word"].strip())
                if txt:
                    ws.append({"t": txt, "a": round(t + max(0, w["start"] - a), 3), "b": round(t + min(b, w["end"]) - a, 3),
                               "d": txt.lower().strip(".,?!“”") in DESTAQUES})
        t += dur
    return linha, ws, t


def blocos(ws, cortes):
    saida, atual, n = [], [], 0
    for p in ws:
        quebra = atual and (n + len(p["t"]) > 24 or atual[-1]["t"][-1] in ".?!" or any(atual[-1]["b"] <= c <= p["a"] for c in cortes))
        if quebra:
            saida.append(atual); atual, n = [], 0
        atual.append(p); n += len(p["t"]) + 1
    if atual:
        saida.append(atual)
    return [{"a": b[0]["a"], "b": b[-1]["b"] + 0.3, "w": b} for b in saida]


def sfx(pasta: Path) -> dict:
    """Efeitos sonoros sintetizados (sem direitos de terceiros)."""
    pasta.mkdir(exist_ok=True)
    defs = {
        "whoosh": ["-f", "lavfi", "-i", "anoisesrc=color=pink:d=0.55:a=0.6", "-af",
                   "highpass=f=350,lowpass=f=4200,afade=t=in:d=0.28:curve=exp,afade=t=out:st=0.3:d=0.25,volume=0.9"],
        "boom": ["-f", "lavfi", "-i", "aevalsrc='0.95*sin(2*PI*(45+60*exp(-9*t))*t)*exp(-3.5*t)':d=1.4:s=48000", "-af", "lowpass=f=900"],
        "pop": ["-f", "lavfi", "-i", "aevalsrc='0.55*sin(2*PI*(520+900*exp(-28*t))*t)*exp(-22*t)':d=0.25:s=48000"],
        "carimbo": ["-f", "lavfi", "-i", "aevalsrc='(0.9*sin(2*PI*85*t)+0.5*sin(2*PI*170*t))*exp(-16*t)':d=0.4:s=48000", "-af", "lowpass=f=1200"],
        "brilho": ["-f", "lavfi", "-i", "aevalsrc='0.16*(sin(2*PI*1760*t)+sin(2*PI*2637*t)+0.7*sin(2*PI*3520*t))*exp(-3*t)':d=1.6:s=48000",
                   "-af", "aecho=0.8:0.6:60:0.35"],
    }
    for nome, args in defs.items():
        ff(*args, "-ac", "2", "-ar", "48000", pasta / f"{nome}.wav")
    return {n: pasta / f"{n}.wav" for n in defs}


def trilha(dur: float, destino: Path) -> None:
    """Base instrumental discreta: pad Lá menor–Fá–Dó–Sol, um acorde a cada 4 s, sem cliques."""
    def nota(fs):  # frequência por acorde (m = posição no ciclo de 16 s)
        return "+".join(f"{f}*between(mod(t,16),{i*4},{i*4+4}-0.0001)" for i, f in enumerate(fs))
    vozes = [nota([110, 87.31, 130.81, 98.0]), nota([220, 174.61, 261.63, 196.0]),
             nota([261.63, 220.0, 329.63, 246.94]), nota([329.63, 261.63, 392.0, 293.66])]
    env = "pow(sin(PI*mod(t,4)/4),2)"
    soma = "+".join(f"{amp}*sin(2*PI*({v})*t)" for amp, v in zip([0.30, 0.22, 0.16, 0.12], vozes))
    ff("-f", "lavfi", "-i", f"aevalsrc='({soma})*{env}*0.5':d={dur + 1}:s=48000",
       "-af", "lowpass=f=1400,aecho=0.8:0.7:120|240:0.35|0.25,afade=t=in:d=1.5,afade=t=out:st=" + f"{dur - 1.5}:d=1.5",
       "-ac", "2", destino)


def audio(reel: dict, pasta: Path, eventos: list[tuple[float, str]], total: float, efeitos: dict) -> tuple[Path, Path]:
    # 1) narração: cortes com micro-fades, depois tratamento único da voz
    partes = []
    for i, (a, b) in enumerate(reel["trechos"]):
        d = round(b - a, 3)
        p = pasta / f"voz_{i}.wav"
        ff("-ss", a, "-t", d, "-i", SRC, "-vn", "-af", f"afade=t=in:d=0.03,afade=t=out:st={d - 0.05}:d=0.05,aresample=48000",
           "-ac", "2", p)
        partes.append(p)
    lista = pasta / "voz.txt"
    lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
    voz = pasta / "voz.wav"
    ff("-f", "concat", "-safe", "0", "-i", lista, "-af",
       f"highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,"
       f"acompressor=threshold=-20dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=9,apad=whole_dur={total}",
       "-ar", "48000", "-ac", "2", voz)
    # 2) efeitos no tempo das animações
    entradas, filtros = ["-i", voz], []
    for i, (t, nome) in enumerate(eventos):
        entradas += ["-i", efeitos[nome]]
        vol = {"whoosh": 0.22, "boom": 0.55, "pop": 0.28, "carimbo": 0.45, "brilho": 0.30}[nome]
        filtros.append(f"[{i + 1}:a]adelay={int(max(0, t) * 1000)}|{int(max(0, t) * 1000)},volume={vol}[e{i}]")
    mix = "".join(f"[e{i}]" for i in range(len(eventos)))
    filtros.append(f"[0:a]{mix}amix=inputs={len(eventos) + 1}:normalize=0:duration=first[vs]")
    sem = pasta / "sem_musica.wav"
    ff(*entradas, "-filter_complex", ";".join(filtros) + ";[vs]alimiter=limit=0.95[o]", "-map", "[o]", "-t", total, sem)
    # 3) base instrumental com ducking pela voz
    mus = pasta / "trilha.wav"
    trilha(total, mus)
    com = pasta / "com_musica.wav"
    ff("-i", sem, "-i", mus, "-i", voz, "-filter_complex",
       "[1:a]volume=0.32[m];[m][2:a]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=450[md];"
       "[0:a][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[o]", "-map", "[o]", "-t", total, com)
    return com, sem


# --------------------------------------------------------------------------- mídia
def preparar_seq(nome: str, clipe: str, ini: float, dur: float, vel: float = 1.0) -> dict:
    pasta = AQUI / "seq" / nome
    if not (pasta / "0001.jpg").exists():
        pasta.mkdir(parents=True, exist_ok=True)
        ff("-ss", ini, "-t", round(dur * vel + 0.6, 2), "-i", AQUI / "videos" / clipe,
           "-vf", f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
           "-q:v", "3", pasta / "%04d.jpg")
    n = len(list(pasta.glob("*.jpg")))
    return {"seq": f"seq/{nome}", "n": n, "vel": vel}


def foto(nome: str) -> str:
    destino = AQUI / "midia" / f"{nome}.jpg"
    if not destino.exists():
        destino.parent.mkdir(exist_ok=True)
        shutil.copy(next((AQUI / "fotos").glob(f"{nome}-*.jpg")), destino)
    return f"midia/{nome}.jpg"


# --------------------------------------------------------------------------- blocos de cena
def texto(html, at, top, size=96, left=70, right=70, anim="mascara", cg=True, align="left", **kw):
    st = {"top": f"{top}px", "left": f"{left}px", "right": f"{right}px", "fontSize": f"{size}px", "lineHeight": "1.02",
          "textAlign": align, "fontWeight": "700" if cg else "800", "textShadow": "0 6px 30px rgba(0,0,0,.55)"}
    st.update(kw.pop("style", {}))
    return {"tipo": "texto", "html": html, "at": at, "anim": anim, "cls": "cg" if cg else "", "style": st, **kw}


def kick(txt, at, top=330, left=70, **kw):
    return {"html": txt, "cls": "kick", "at": at, "anim": "sobe", "style": {"top": f"{top}px", "left": f"{left}px", **kw.pop("style", {})}, **kw}


def pilula(txt, at, top, left=70, anim="pop", **kw):
    return {"html": txt, "cls": "pill", "at": at, "anim": anim, "style": {"top": f"{top}px", "left": f"{left}px", **kw.pop("style", {})}, **kw}


def carimbo(txt, at, top, left, rot=-8, size=76):
    return {"html": txt, "cls": "carimbo", "at": at, "anim": "carimbo", "rot": rot, "style": {"top": f"{top}px", "left": f"{left}px", "fontSize": f"{size}px"}}


def traco(svg, at, top, left, w, h, dur=1.2, stagger=0.0):
    return {"tipo": "traco", "html": f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke="#C9A962" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 14px rgba(201,169,98,.55))">{svg}</svg>',
            "at": at, "durTraco": dur, "stagger": stagger, "style": {"top": f"{top}px", "left": f"{left}px"}}


def contador(de, para, at, top, left=70, size=300, sufixo="dias", dur=1.4):
    return {"tipo": "contador", "de": de, "para": para, "at": at, "durConta": dur, "anim": "fade", "dur": 0.15,
            "html": f'<span class="cg num" style="font-size:{size}px;font-weight:700;line-height:.9;color:#E2C77F;text-shadow:0 10px 50px rgba(0,0,0,.6)">{de}</span>'
                    f'<span class="cg" style="font-size:{int(size * .3)}px;font-weight:600;font-style:italic;color:#FAF6F0;margin-left:18px">{sufixo}</span>',
            "style": {"top": f"{top}px", "left": f"{left}px"}}


def risco(at, top, left, largura, cor="#C9A962", alt=6):
    return {"tipo": "risco", "at": at, "largura": largura, "html": "",
            "style": {"top": f"{top}px", "left": f"{left}px", "height": f"{alt}px", "width": "0px", "background": cor,
                      "borderRadius": "3px", "boxShadow": "0 0 18px rgba(201,169,98,.6)"}}


def bloco_html(html, at, top, left, w, anim="sobe", cls="cartao", dx=None, transform="none", padding="34px 40px"):
    interno = f'<div class="{cls}" style="padding:{padding};transform:{transform}">{html}</div>'
    d = {"html": interno, "at": at, "anim": anim, "style": {"top": f"{top}px", "left": f"{left}px", "width": f"{w}px"}}
    if dx is not None:
        d["dx"] = dx
    return d


ESCUDO = '<path class="desenha" d="M200 20 L360 80 L360 220 C360 330 290 400 200 440 C110 400 40 330 40 220 L40 80 Z"/><path class="desenha" d="M130 230 L185 285 L280 175"/>'
ECG = '<path class="desenha" d="M0 90 L250 90 L290 90 L315 20 L345 160 L370 60 L390 90 L560 90 L590 90 L615 30 L640 150 L662 90 L940 90"/>'
COLUNAS = ('<path class="desenha" d="M30 120 L270 30 L510 120 Z"/><path class="desenha" d="M60 150 L480 150"/>'
           '<path class="desenha" d="M100 170 L100 360"/><path class="desenha" d="M200 170 L200 360"/><path class="desenha" d="M340 170 L340 360"/>'
           '<path class="desenha" d="M440 170 L440 360"/><path class="desenha" d="M40 390 L500 390"/>')
HOSPITAL = '<rect class="desenha" x="20" y="20" width="200" height="200" rx="30"/><path class="desenha" d="M120 60 L120 180 M60 120 L180 120"/>'
CORACAO = '<path class="desenha" d="M60 100 C20 60 30 15 70 15 C95 15 105 35 110 45 C115 35 125 15 150 15 C190 15 200 60 160 100 L110 150 Z"/>'

LINHA_HTML = ('<div style="position:relative;height:8px;background:rgba(232,222,209,.22);border-radius:4px">'
              '<div class="fill" style="height:100%;width:0;background:linear-gradient(90deg,#B8943F,#F4E6BC);border-radius:4px;box-shadow:0 0 22px #C9A962"></div></div>')


def no(rotulo, at, x, top=700, sub=""):
    return {"html": f'<div style="width:34px;height:34px;border-radius:50%;background:#F4E6BC;box-shadow:0 0 0 8px rgba(201,169,98,.25),0 0 30px #C9A962;margin:0 auto"></div>'
                    f'<div style="margin-top:22px;font-size:30px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#FAF6F0;text-align:center;white-space:nowrap">{rotulo}</div>'
                    + (f'<div style="font-size:24px;color:#E8DED1cc;text-align:center;white-space:nowrap">{sub}</div>' if sub else ""),
            "at": at, "anim": "pop", "style": {"top": f"{top - 13}px", "left": f"{x - 120}px", "width": "240px"}}


def outro(a, proxima):
    # área segura do Reels: nada abaixo de y=1248 (legenda do post, perfil e botões)
    return {"a": a, "trans": "dissolve", "particulas": 18, "els": [
        {"html": '<img src="midia/logo.png" style="width:180px">', "at": a + .15, "anim": "pop", "style": {"top": "360px", "left": "450px"}},
        texto("Salve e mande para|<em>uma gestante</em>.", a + .3, 580, size=92, align="center"),
        pilula(proxima, a + .7, 790, left=0, style={"left": "50%", "marginLeft": "-330px", "width": "660px", "textAlign": "center"}),
        {"html": "Cada caso tem detalhes.<br>Procure uma advogada de confiança.", "at": a + .9, "anim": "sobe",
         "style": {"top": "900px", "left": "70px", "right": "70px", "textAlign": "center", "fontSize": "34px", "fontWeight": "600", "lineHeight": "1.4", "color": "#E8DED1"}},
        texto("Dra. Letícia Barros,|a advogada da <em>Gestante trabalhadora</em>", a + 1.1, 1010, size=44, align="center", anim="sobe"),
        {"html": "OAB/ES 39.948 · @adv.leticiabarros2", "cls": "kick", "at": a + 1.25, "anim": "sobe",
         "style": {"top": "1130px", "left": "0", "right": "0", "textAlign": "center"}},
    ]}


# --------------------------------------------------------------------------- os 3 roteiros
# Área segura (Meta): topo 14% (269 px), base 35% (672 px), laterais 65 px. Gráficos entre
# y=350 e y≈1085; legenda (engine) entre 1100 e 1240; nada encosta na coluna de botões.
def reel1(W, seg, fim):
    s = seg
    return [
        {"a": 0, "trans": "corte", "bg": {"src": foto("gestante-preocupada-5"), "kb": [1.24, 1.05, 0, 0, -60, 0]},
         "cam": [1.0, 1.03, 0, 0], "els": [
            texto("Grávida?", 0.06, 380, size=170),
            texto("<em>E agora?</em>", W("agora") - .08, 560, size=150)]},
        {"a": W("O"), "trans": "whip", "bg": {**preparar_seq("r1_escritorio", "v-gestante-escritorio-0-7572251.mp4", 1.0, 3.0), "kb": [1.04, 1.14, 0, -40, 0, 0]},
         "els": [texto("O que muda no|<em>meu emprego</em>?", W("O") + .12, 380, size=104)]},
        {"a": s[1], "trans": "iris", "irisY": 40, "bg": {"src": foto("gestante-negra-2"), "blur": 3, "kb": [1.12, 1.2, 60, 20, 0, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.86), rgba(26,21,17,.55) 45%, rgba(26,21,17,.92))", "cam": [1.0, 1.05, 0, 0], "els": [
            kick("01 · Estabilidade", s[1] + .1, top=360),
            traco(ESCUDO, s[1] + .15, 420, 150, 400, 460, dur=1.3),
            texto("A lei protege|o seu <em>emprego</em>", s[1] + .55, 905, size=84),
            bloco_html('<div style="font-size:24px;font-weight:800;letter-spacing:3px;color:#8E6E2E">COMUNICADO</div>'
                       '<div class="cg" style="font-size:54px;font-weight:700;line-height:1;margin-top:8px">Aviso de<br>demissão</div>'
                       '<div style="margin-top:16px;height:8px;background:#2B231C22;border-radius:4px"></div><div style="margin-top:10px;height:8px;width:70%;background:#2B231C22;border-radius:4px"></div>',
                       W("demissão") - .15, 520, 590, 360, anim="desliza", cls="papel", dx=500, transform="rotate(4deg)"),
            carimbo("Bloqueada", W("justa"), 660, 545, rot=-12, size=64)]},
        {"a": W("E", W("causa.")), "trans": "zoom", "bg": {**preparar_seq("r1_janela", "v-gestante-janela-0-6967764.mp4", 0.5, 8.5), "blur": 7},
         "veu": "rgba(26,21,17,.84)", "cam": [1.0, 1.04, 30, -30], "els": [
            kick("Quando começa e quando termina", W("E", W("causa.")) + .1, top=360),
            pilula("mesmo descobrindo depois", W("descoberta"), 470, left=100),
            {"tipo": "linha", "html": LINHA_HTML, "at": W("concepção,"), "ateFim": W("parto.") + .25, "style": {"top": "660px", "left": "160px", "width": "760px"}},
            no("Concepção", W("concepção,"), 177, top=660), no("Parto", W("parto.") - .05, 600, top=660), no("+5 meses", W("cinco"), 903, top=660),
            texto("até <em>5 meses</em>|após o parto", W("cinco"), 860, size=100)]},
        {"a": s[2], "trans": "corte", "particulas": 28, "els": [
            {"html": '<div class="cg" style="width:250px;height:250px;border:6px solid #C9A962;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:190px;font-weight:700;color:#E2C77F;box-shadow:0 0 60px rgba(201,169,98,.35)">!</div>',
             "at": s[2] + .05, "anim": "pop", "pulso": True, "style": {"top": "440px", "left": "415px"}},
            texto("Um detalhe que|<em>muita gente</em> não sabe", W("detalhe"), 780, size=96, align="center")]},
        {"a": W("Esse"), "trans": "sobe", "bg": {**preparar_seq("r1_tablet", "v-gestante-negra-1-6974514.mp4", 0.5, 7.5), "kb": [1.04, 1.12, 0, 0, 0, -40]},
         "els": [
            bloco_html('<div class="kick">Na hora da demissão</div><div class="cg" style="font-size:72px;font-weight:700;line-height:1.02;margin-top:14px">A empresa sabia<br>da gravidez?</div>',
                       W("Esse") + .15, 620, 90, 900),
            pilula("Não", W("soubesse"), 895, left=110, style={"fontSize": "40px"}),
            carimbo("Vale igual", W("demissão.", W("soubesse")), 880, 360, rot=-8, size=66),
            pilula("Proteção objetiva · STF, Tema 497", s[3] + .05, 1010, left=90, anim="desliza")]},
        {"a": W("Basta"), "trans": "dissolve", "bg": {**preparar_seq("r1_janela2", "v-gestante-janela-0-6967764.mp4", 9.5, 7.5), "kb": [1.0, 1.14, 0, 0, 0, -50]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.6) 0%, rgba(26,21,17,.15) 22%, rgba(26,21,17,.78) 40%, rgba(26,21,17,.93) 100%)",
         "els": [
            kick("Para ter o direito", W("Basta") + .1, top=700),
            texto("A gravidez começou|com o <em>contrato ativo</em>.", W("provar"), 745, size=84),
            carimbo("Direito garantido", W("garantido."), 960, 90, rot=-6, size=58)]},
        outro(fim, "Parte 2 · Pré-natal sem desconto"),
    ]


def reel2(W, seg, fim):
    s = seg
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("r2_consulta", "v-medica-1-7089939.mp4", 1.0, 3.2), "blur": 2},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.45) 50%, rgba(26,21,17,.9))", "els": [
            texto("<em>Mito</em>", 0.05, 380, size=200),
            texto("“Faltar pro pré-natal|dá desconto no salário”", W("quebrar") - .3, 620, size=70, anim="sobe"),
            risco(W("comum."), 690, 70, 900, alt=7)]},
        {"a": s[1], "trans": "whip", "bg": {**preparar_seq("r2_ultra", "v-ultrassom-2-7088945.mp4", 1.0, 6.5), "blur": 9},
         "veu": "rgba(26,21,17,.6)", "cam": [1.0, 1.06, 0, 0], "els": [
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:24px;font-weight:800;letter-spacing:3px;color:#8E6E2E"><span>CONTRACHEQUE</span><span>OUTUBRO</span></div>'
                       '<div style="display:flex;justify-content:space-between;font-size:34px;margin-top:34px"><span>Salário</span><b>R$ ••••••</b></div>',
                       s[1] + .1, 400, 110, 860, cls="papel", transform="rotate(-2deg)"),
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:34px;color:#2B231C"><span>Consulta pré-natal</span><b>Falta justificada ✓</b></div>',
                       W("justificada"), 590, 110, 860, cls="papel", anim="desliza", transform="rotate(-2deg)", padding="22px 40px"),
            bloco_html('<div style="display:flex;justify-content:space-between;font-size:40px;color:#2B231C"><span>Desconto</span><b style="background:#E9D398;padding:0 12px">R$ 0,00</b></div>',
                       W("descontado"), 720, 110, 860, cls="papel", anim="pop", transform="rotate(-2deg)", padding="24px 40px"),
            carimbo("Sem desconto", W("salário.", W("descontado")), 900, 260, rot=-7, size=70)]},
        {"a": s[2], "trans": "zoom", "bg": {"src": foto("consulta-4"), "kb": [1.06, 1.18, 0, -40, 0, 0]}, "els": [
            kick("03 · Pré-natal", s[2] + .1, top=360),
            texto("Você pode sair para|<em>consultas e exames</em>", W("ausentar"), 410, size=86),
            traco(ECG, s[2] + .3, 620, 70, 940, 180, dur=2.4),
            *[pilula(str(i + 1), W("seis") + i * .14, 830, left=90 + i * 150, style={"fontSize": "44px", "width": "120px", "textAlign": "center"}) for i in range(6)],
            texto("no mínimo <em>6 consultas</em>", W("consultas", W("seis")), 950, size=76, anim="sobe")]},
        {"a": s[3], "trans": "dissolve", "bg": {**preparar_seq("r2_ultra2", "v-ultrassom-1-7088947.mp4", 1.0, 11.5), "blur": 10},
         "veu": "rgba(26,21,17,.74)", "els": [
            {"html": '<span class="cg" style="font-size:440px;font-weight:700;line-height:.8;color:#E2C77F;text-shadow:0 20px 80px rgba(0,0,0,.6)">6</span>',
             "at": W("Seis", s[3] - .01), "anim": "pop", "style": {"top": "380px", "left": "130px"}},
            risco(W("piso,"), 760, 90, 420, alt=8),
            texto("é o <em>piso</em>,|não o teto", W("piso,"), 480, size=88, left=470, right=60),
            pilula("+ consultas, se o médico pedir", W("mais"), 840, left=90, anim="desliza"),
            pilula("com atestado ✓", W("atestado"), 960, left=90)]},
        {"a": s[4], "trans": "sobe", "bg": {**preparar_seq("r2_negra", "v-gestante-negra-0-6967705.mp4", 1.0, 7.5), "kb": [1.04, 1.12, 0, 0, 0, -30]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.55) 0%, rgba(26,21,17,.1) 25%, rgba(26,21,17,.7) 45%, rgba(26,21,17,.92) 100%)",
         "els": [
            bloco_html('<div class="kick">A empresa pediu</div><div class="cg" style="font-size:70px;font-weight:700;line-height:1.02;margin-top:12px">para compensar<br>as horas?</div>',
                       s[4] + .15, 500, 90, 900),
            carimbo("Não é obrigatório", W("obrigação"), 755, 150, rot=-7, size=56),
            texto("Falta justificada|e <em>ponto final</em>.", W("falta", W("isso.")), 905, size=76)]},
        outro(fim, "Parte 3 · Licença e bebê internado"),
    ]


def reel3(W, seg, fim):
    s = seg
    return [
        {"a": 0, "trans": "corte", "bg": {**preparar_seq("r3_cama", "v-mae-recem-nascido-3-7280809.mp4", 0.5, 7.6), "kb": [1.2, 1.04, 0, 0, -40, 0]},
         "veu": "linear-gradient(180deg, rgba(26,21,17,.85), rgba(26,21,17,.35) 50%, rgba(26,21,17,.9))", "els": [
            texto("E se o bebê|ficar <em>internado</em>?", 0.06, 380, size=128),
            pilula("A licença-maternidade espera?", W("licença"), 670, left=70),
            traco(HOSPITAL, W("internados"), 800, 70, 240, 240, dur=1.0)]},
        {"a": s[1], "trans": "whip", "bg": {**preparar_seq("r3_calendario", "v-calendario-0-35332817.mp4", 0.2, 4.2), "blur": 4},
         "veu": "rgba(26,21,17,.62)", "els": [
            kick("A regra", s[1] + .1, top=360),
            contador(0, 120, W("120"), 430, size=320),
            pilula("com salário", W("salário,"), 830, left=80)]},
        {"a": s[2], "trans": "whipV", "bg": {**preparar_seq("r3_amamenta", "v-mae-recem-nascido-1-6391713.mp4", 0.5, 8.3), "kb": [1.04, 1.13, 0, 0, 0, -40]},
         "els": [
            {"html": '<div style="width:300px;height:300px;border-radius:50%;background:radial-gradient(circle at 35% 28%,#FFF3CF,#DCC385 30%,#C3A25A 60%,#8E6E2E);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 0 8px rgba(26,21,17,.8),0 0 0 10px #C9A962,0 30px 60px rgba(0,0,0,.5);color:#3A2A14"><span style="font-size:24px;font-weight:800;letter-spacing:3px">PROGRAMA</span><span class="cg" style="font-size:58px;font-weight:700;line-height:1;text-align:center">Empresa<br>Cidadã</span></div>',
             "at": W("Cidadã"), "anim": "carimbo", "rot": -10, "style": {"top": "380px", "left": "640px"}},
            pilula("+60 dias", W("180") + .6, 690, left=80),
            contador(120, 180, W("180"), 770, size=290, dur=1.0)]},
        {"a": s[3], "trans": "iris", "irisY": 38, "particulas": 22, "els": [
            pilula("ADI 6327", W("STF."), 360, left=0, style={"left": "50%", "marginLeft": "-110px"}),
            traco(COLUNAS, s[3] + .05, 440, 270, 540, 410, dur=1.4, stagger=.08),
            texto("Decisão do|<em>STF</em>", W("decisão"), 870, size=100, align="center")]},
        {"a": s[4], "trans": "zoom", "bg": {**preparar_seq("r3_cama2", "v-mae-recem-nascido-2-7279091.mp4", 0.5, 8.4), "blur": 8},
         "veu": "rgba(26,21,17,.7)", "els": [
            texto("A licença começa|<em>depois da alta</em>", W("relógio"), 380, size=92),
            {"tipo": "linha", "html": LINHA_HTML.replace("#B8943F,#F4E6BC", "#8C7F72,#B7AA9C").replace("box-shadow:0 0 22px #C9A962", ""),
             "at": W("internação"), "ateFim": W("semanas,") + .2, "style": {"top": "740px", "left": "90px", "width": "380px"}},
            {"html": '<div style="font-size:28px;font-weight:800;letter-spacing:2px;color:#E8DED1">INTERNAÇÃO</div><div style="font-size:26px;color:#E8DED1cc">mais de 2 semanas</div>',
             "at": W("internação"), "anim": "sobe", "style": {"top": "640px", "left": "90px"}},
            no("Alta", W("alta"), 500, top=744),
            {"tipo": "linha", "html": LINHA_HTML, "at": W("alta") + .15, "ateFim": W("alta") + 1.3, "style": {"top": "740px", "left": "530px", "width": "460px"}},
            {"html": '<div class="cg" style="font-size:66px;font-weight:700;color:#E2C77F">120 dias</div><div style="font-size:26px;color:#E8DED1">contam daqui</div>',
             "at": W("alta") + .5, "anim": "pop", "style": {"top": "830px", "left": "640px"}}]},
        {"a": s[5], "trans": "dissolve", "bg": {**preparar_seq("r3_mao", "v-mao-bebe-0-6392156.mp4", 0.5, 5.2), "kb": [1.02, 1.16, 0, 0, 0, 0]},
         "els": [texto("Tempo em casa com o bebê,|<em>protegido</em>.", W("precioso"), 400, size=84)]},
        {"a": s[6], "trans": "dissolve", "bg": {"src": foto("recem-nascido-5"), "blur": 6, "kb": [1.1, 1.18, 0, 0, 0, 0]},
         "veu": "rgba(26,21,17,.7)", "els": [texto("Informação|<em>é poder</em>.", s[6] + .05, 600, size=150, align="center")]},
        outro(fim, "Salve a série completa"),
    ]


REELS = {
    1: {"trechos": [(25.45, 29.95), (59.40, 71.55), (91.45, 101.05), (104.45, 112.75)], "roteiro": reel1},
    2: {"trechos": [(145.05, 147.55), (147.75, 154.00), (125.70, 133.70), (133.85, 144.70), (154.15, 160.98)], "roteiro": reel2},
    3: {"trechos": [(216.50, 223.95), (192.55, 196.55), (197.58, 205.70), (225.75, 230.75), (235.25, 243.50), (243.65, 248.55), (368.95, 370.45)],
        "roteiro": reel3},
}


def montar_cfg(n: int) -> tuple[dict, list]:
    reel = REELS[n]
    linha, ws, fala = palavras_do_reel(reel["trechos"])
    seg = [tr["ini"] for tr in linha]

    def W(txt, depois=-1.0):
        for w in ws:
            if w["a"] > depois and w["t"].lower() == txt.lower():
                return w["a"]
        for w in ws:  # sem pontuação
            if w["a"] > depois and w["t"].lower().strip(".,?!") == txt.lower().strip(".,?!"):
                return w["a"]
        raise KeyError(f"reel {n}: palavra '{txt}' depois de {depois}")

    total = round(fala + OUTRO, 3)
    cenas = reel["roteiro"](W, seg, round(fala, 3))
    eventos = []
    for c in cenas:
        if c["trans"] in ("whip", "whipV", "zoom", "iris", "sobe"):
            eventos.append((c["a"] - .12, "whoosh"))
        for e in c.get("els", []):
            if e.get("anim") == "carimbo":
                eventos.append((e["at"] + .14, "carimbo"))
            elif e.get("anim") == "pop":
                eventos.append((e["at"], "pop"))
    eventos.append((0.0, "boom"))
    eventos.append((fala + .2, "brilho"))
    flashes = [c["a"] for c in cenas if c["trans"] == "corte" and c["a"] > 0]
    cfg = {"serie": f"Série gestante · {n}/3", "total": total, "cenas": cenas, "leg": blocos(ws, seg[1:]),
           "flashes": flashes, "semLegenda": [[fala, total + 1]]}
    (AQUI / f"cfg_r{n}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    return cfg, sorted(eventos)


async def renderizar(n: int, cfg: dict, so_amostras: list[float] | None = None) -> Path:
    pasta = AQUI / f"quadros_r{n}"
    if pasta.exists() and not so_amostras and not __import__("os").environ.get("DESDE_QUADRO"):
        shutil.rmtree(pasta)
    pasta.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--allow-file-access-from-files"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.goto((AQUI / "engine.html").as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.evaluate("cfg => init(cfg)", cfg)
        tempos = so_amostras or [i / FPS for i in range(int(round(cfg["total"] * FPS)))]
        desde = int(__import__("os").environ.get("DESDE_QUADRO", "0"))
        for i, t in enumerate(tempos):
            if not so_amostras and i < desde:
                continue
            await page.evaluate(f"render({t:.4f})")
            nome = f"amostra_r{n}_{t:05.2f}.jpg" if so_amostras else f"{i:05d}.jpg"
            await page.screenshot(path=str((AQUI if so_amostras else pasta) / nome), type="jpeg", quality=92)
            if not so_amostras and i % 300 == 0:
                print(f"r{n} quadro {i}/{len(tempos)}", flush=True)
        await browser.close()
    return pasta


def codificar(n: int, pasta: Path, total: float, com: Path, sem: Path) -> list[Path]:
    saidas = []
    for audio_, nome in [(com, f"reel{n}.mp4"), (sem, f"reel{n}_sem_musica.mp4")]:
        destino = AQUI.parent / nome
        ff("-framerate", FPS, "-i", pasta / "%05d.jpg", "-i", audio_, "-map", "0:v", "-map", "1:a", "-t", total,
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", FPS,
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", destino)
        saidas.append(destino)
    return saidas


async def main(numeros: list[int], amostras: bool) -> None:
    (AQUI / "midia").mkdir(exist_ok=True)
    shutil.copy(ASSETS / "logo-leticia.png", AQUI / "midia" / "logo.png")
    efeitos = sfx(AQUI / "sfx")
    for n in numeros:
        cfg, eventos = montar_cfg(n)
        if amostras:
            ts = [float(x) for x in __import__("os").environ.get("TS", "").split(",") if x] or [c["a"] + 1.2 for c in cfg["cenas"]]
            await renderizar(n, cfg, ts)
            print("amostras r", n, [round(t, 2) for t in ts])
            continue
        pasta_audio = AQUI / f"audio_r{n}"
        pasta_audio.mkdir(exist_ok=True)
        com, sem = audio(REELS[n], pasta_audio, eventos, cfg["total"], efeitos)
        pasta = await renderizar(n, cfg)
        print("ok", codificar(n, pasta, cfg["total"], com, sem), flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    amostras = "--amostras" in args
    nums = [int(a) for a in args if a.isdigit()] or [1, 2, 3]
    asyncio.run(main(nums, amostras))
