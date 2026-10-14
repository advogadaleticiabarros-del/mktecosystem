"""Motor v2 dos Reels da Letícia (motion design + camada procedural).

Genérico: áudio (voz tratada, efeitos sintetizados, trilha própria com ducking), energia da voz,
legenda por frase, blocos de cena, pó de ouro, explosões, soco na palavra-chave, transições
(tinta, luz, whip, zoom, íris...), verificador da área limpa e da velocidade de leitura,
render quadro a quadro (Playwright) e codificação H.264 pronta para a API da Meta.

O roteiro de cada série fica em serie.py, que importa daqui e define REELS.
"""
import asyncio
import base64
import json
import os
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np
from playwright.async_api import async_playwright

AQUI = Path.cwd()
FF = Path(r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe")
ASSETS = Path(r"C:\Users\prosy\mktecosystem\apps\api\app\assets")
FPS = 30
OUTRO = 3.8
CFG = {"src": None, "destaques": set(), "corrige": {}, "serie": ""}


def ff(*args) -> None:
    subprocess.run([str(FF), "-v", "error", "-y", *map(str, args)], check=True)


# --------------------------------------------------------------------------- palavras e legenda
def palavras_do_reel(trechos, reel=None):
    reel = reel or {}
    corrige = {**CFG["corrige"], **reel.get("corrige", {})}
    destaques = CFG["destaques"] | set(reel.get("destaques", ()))
    r = json.loads(Path(reel.get("transcricao", AQUI / "transcricao.json")).read_text(encoding="utf-8"))
    todas = [w for s in r["segments"] for w in s["words"]]
    t, linha, ws = 0.0, [], []
    for a, b in trechos:
        dur = round(b - a, 3)
        linha.append({"ini_src": a, "fim_src": b, "ini": t, "fim": t + dur})
        for w in todas:
            if w["start"] >= a - 0.05 and w["start"] < b - 0.03 and w["end"] <= b + 0.15:
                txt = corrige.get(f'{w["word"].strip()}@{w["start"]:.2f}', corrige.get(w["word"].strip(), w["word"].strip()))
                if txt:
                    ws.append({"t": txt, "a": round(t + max(0, w["start"] - a), 3), "b": round(t + min(b, w["end"]) - a, 3),
                               "d": txt.lower().strip(".,?!“”") in destaques})
        t += dur
    return linha, ws, t


def blocos(ws, cortes):
    """Legenda por frase: no máximo 24 caracteres por bloco (leitura confortável no celular)."""
    saida, atual, n = [], [], 0
    for p in ws:
        quebra = atual and (n + len(p["t"]) > 24 or atual[-1]["t"][-1] in ".?!" or any(atual[-1]["b"] <= c <= p["a"] for c in cortes))
        if quebra:
            saida.append(atual); atual, n = [], 0
        atual.append(p); n += len(p["t"]) + 1
    if atual:
        saida.append(atual)
    return [{"a": b[0]["a"], "b": b[-1]["b"] + 0.3, "w": b} for b in saida]


def energia(trechos, total, src=None):
    """Energia da voz por quadro (0..1) para a camada procedural reagir à narração."""
    src = Path(src or CFG["src"])
    wav = src.with_suffix(".wav")
    if not wav.exists():
        ff("-i", src, "-vn", "-ac", "1", "-ar", "16000", wav)
    with wave.open(str(wav)) as f:
        sr = f.getframerate(); x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    jan, ev = sr // FPS, []
    for a, b in trechos:
        seg = x[int(a * sr):int(b * sr)]
        n = len(seg) // jan
        ev += list(np.sqrt((seg[:n * jan].reshape(n, jan) ** 2).mean(axis=1)))
    e = np.array(ev) / (np.percentile(ev, 95) + 1e-6)
    e = np.clip(e, 0, 1)
    sm, v = [], 0.0
    for k in e:  # ataque rápido, soltura lenta
        v = v + (k - v) * (0.6 if k > v else 0.12); sm.append(round(float(v), 3))
    sm += [0.0] * (int(total * FPS) + 2 - len(sm))
    return sm


# --------------------------------------------------------------------------- som
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
        # pó de ouro se formando: cintilação que sobe
        "po": ["-f", "lavfi", "-i", "aevalsrc='0.10*sin(2*PI*(900+1800*t)*t)*(0.5+0.5*sin(2*PI*31*t))*exp(-1.6*t)':d=1.3:s=48000",
               "-af", "highpass=f=600,aecho=0.8:0.5:45:0.3"],
    }
    for nome, args in defs.items():
        ff(*args, "-ac", "2", "-ar", "48000", pasta / f"{nome}.wav")
    return {n: pasta / f"{n}.wav" for n in defs}


def trilha(dur: float, destino: Path) -> None:
    """Base instrumental própria: pad Lá menor–Fá–Dó–Sol com pulso leve (a cada 4 s), sem cliques."""
    def nota(fs):
        return "+".join(f"{f}*between(mod(t,16),{i*4},{i*4+4}-0.0001)" for i, f in enumerate(fs))
    vozes = [nota([110, 87.31, 130.81, 98.0]), nota([220, 174.61, 261.63, 196.0]),
             nota([261.63, 220.0, 329.63, 246.94]), nota([329.63, 261.63, 392.0, 293.66])]
    env = "pow(sin(PI*mod(t,4)/4),2)"
    soma = "+".join(f"{amp}*sin(2*PI*({v})*t)" for amp, v in zip([0.30, 0.22, 0.16, 0.12], vozes))
    pulso = "0.18*sin(2*PI*55*t)*exp(-9*mod(t,0.5))"
    ff("-f", "lavfi", "-i", f"aevalsrc='(({soma})*{env}*0.5)+{pulso}':d={dur + 1}:s=48000",
       "-af", "lowpass=f=1400,aecho=0.8:0.7:120|240:0.35|0.25,afade=t=in:d=1.0,afade=t=out:st=" + f"{dur - 1.5}:d=1.5",
       "-ac", "2", destino)


def audio(reel, pasta: Path, eventos, total: float, efeitos: dict):
    partes = []
    for i, (a, b) in enumerate(reel["trechos"]):
        d = round(b - a, 3)
        p = pasta / f"voz_{i}.wav"
        ff("-ss", a, "-t", d, "-i", reel.get("src", CFG["src"]), "-vn", "-af", f"afade=t=in:d=0.03,afade=t=out:st={d - 0.05}:d=0.05,aresample=48000",
           "-ac", "2", p)
        partes.append(p)
    lista = pasta / "voz.txt"
    lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
    voz = pasta / "voz.wav"
    ff("-f", "concat", "-safe", "0", "-i", lista, "-af",
       "highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,"
       f"acompressor=threshold=-20dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-1.5:LRA=9,apad=whole_dur={total}",
       "-ar", "48000", "-ac", "2", voz)
    entradas, filtros = ["-i", voz], []
    vols = {"whoosh": 0.22, "boom": 0.55, "pop": 0.26, "carimbo": 0.45, "brilho": 0.30, "po": 0.5}
    for i, (t, nome) in enumerate(eventos):
        entradas += ["-i", efeitos[nome]]
        ms = int(max(0, t) * 1000)
        filtros.append(f"[{i + 1}:a]adelay={ms}|{ms},volume={vols[nome]}[e{i}]")
    mix = "".join(f"[e{i}]" for i in range(len(eventos)))
    filtros.append(f"[0:a]{mix}amix=inputs={len(eventos) + 1}:normalize=0:duration=first[vs]")
    sem = pasta / "sem_musica.wav"
    ff(*entradas, "-filter_complex", ";".join(filtros) + ";[vs]alimiter=limit=0.95[o]", "-map", "[o]", "-t", total, sem)
    mus = pasta / "trilha.wav"
    trilha(total, mus)
    com = pasta / "com_musica.wav"
    ff("-i", sem, "-i", mus, "-i", voz, "-filter_complex",
       "[1:a]volume=0.30[m];[m][2:a]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=450[md];"
       "[0:a][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[o]", "-map", "[o]", "-t", total, com)
    return com, sem


# --------------------------------------------------------------------------- mídia
def preparar_seq(nome, clipe, ini, dur, vel=1.0):
    pasta = AQUI / "seq" / nome
    if not (pasta / "0001.jpg").exists():
        pasta.mkdir(parents=True, exist_ok=True)
        ff("-ss", ini, "-t", round(dur * vel + 0.6, 2), "-i", next((AQUI / "videos").glob(f"{clipe}*.mp4")),
           "-vf", f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
           "-q:v", "3", pasta / "%04d.jpg")
    return {"seq": f"seq/{nome}", "n": len(list(pasta.glob("*.jpg"))), "vel": vel}


def foto(nome):
    destino = AQUI / "midia" / f"{nome}.jpg"
    if not destino.exists():
        destino.parent.mkdir(exist_ok=True)
        shutil.copy(next((AQUI / "fotos").glob(f"{nome}*.jpg")), destino)
    return f"midia/{nome}.jpg"


def data_url(caminho: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(caminho.read_bytes()).decode()


# --------------------------------------------------------------------------- blocos de cena
def texto(html, at, top, size=96, left=90, right=90, anim="mascara", cg=True, align="left", **kw):
    st = {"top": f"{top}px", "left": f"{left}px", "right": f"{right}px", "fontSize": f"{size}px", "lineHeight": "1.02",
          "textAlign": align, "fontWeight": "700" if cg else "800", "textShadow": "0 6px 30px rgba(0,0,0,.55)"}
    st.update(kw.pop("style", {}))
    return {"tipo": "texto", "html": html, "at": at, "anim": anim, "cls": "cg" if cg else "", "style": st, **kw}


def kick(txt, at, top=350, left=90, **kw):
    return {"html": txt, "cls": "kick", "at": at, "anim": "sobe", "style": {"top": f"{top}px", "left": f"{left}px", **kw.pop("style", {})}, **kw}


def pilula(txt, at, top, left=90, anim="pop", **kw):
    return {"html": txt, "cls": "pill", "at": at, "anim": anim, "style": {"top": f"{top}px", "left": f"{left}px", **kw.pop("style", {})}, **kw}


def centro(w):
    return {"left": "50%", "marginLeft": f"-{w // 2}px", "width": f"{w}px", "textAlign": "center"}


def carimbo(txt, at, top, left, rot=-8, size=76, burst=True):
    w = len(txt) * size * 0.66 + 70
    d = {"html": txt, "cls": "carimbo", "at": at, "anim": "carimbo", "rot": rot, "style": {"top": f"{top}px", "left": f"{left}px", "fontSize": f"{size}px"}}
    if burst:
        d["burst"] = {"x": left + w / 2, "y": top + size * 0.62, "n": 80, "raio": 480}
    return d


def traco(svg, at, top, left, w, h, dur=1.2, stagger=0.0):
    return {"tipo": "traco", "html": f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" stroke="#C9A962" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 14px rgba(201,169,98,.55))">{svg}</svg>',
            "at": at, "durTraco": dur, "stagger": stagger, "style": {"top": f"{top}px", "left": f"{left}px"}}


def contador(de, para, at, top, left=70, size=300, sufixo="dias", dur=1.4):
    return {"tipo": "contador", "de": de, "para": para, "at": at, "durConta": dur, "anim": "fade", "dur": 0.15,
            "html": f'<span class="cg num ouro" style="font-size:{size}px;font-weight:700;line-height:.9">{de}</span>'
                    f'<span class="cg" style="font-size:{int(size * .3)}px;font-weight:600;font-style:italic;color:#FAF6F0;margin-left:18px">{sufixo}</span>',
            "style": {"top": f"{top}px", "left": f"{left}px"}}


def risco(at, top, left, largura, cor="#C9A962", alt=6):
    return {"tipo": "risco", "at": at, "largura": largura, "html": "",
            "style": {"top": f"{top}px", "left": f"{left}px", "height": f"{alt}px", "width": "0px", "background": cor,
                      "borderRadius": "3px", "boxShadow": "0 0 18px rgba(201,169,98,.6)"}}


def bloco_html(html, at, top, left, w, anim="sobe", cls="cartao", dx=None, transform="none", padding="34px 40px", **kw):
    interno = f'<div class="{cls}" style="padding:{padding};transform:{transform}">{html}</div>'
    d = {"html": interno, "at": at, "anim": anim, "style": {"top": f"{top}px", "left": f"{left}px", "width": f"{w}px"}, **kw}
    if dx is not None:
        d["dx"] = dx
    return d


def po(txt, at, cx, cy, size=260, dur=1.15, ate=None, img=None, burst=True):
    """Pó de ouro que se junta e forma o texto (ou imagem); assenta nítido, com brilho metálico."""
    d = {"tipo": "po", "texto": txt, "at": at, "x": cx, "y": cy, "size": size, "durPo": dur, "html": ""}
    if ate is not None:
        d["ate"] = ate
    if img:
        d["img"] = img
    if burst:
        d["burst"] = {"x": cx, "y": cy, "n": 60, "raio": 360, "dt": dur + .3}
    return d


def foto_card(src, rotulo, at, top, left, w=430, h=300):
    """Foto em cartão com moldura dourada e rótulo (grade de perfis, comparação)."""
    return {"html": f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:24px;overflow:hidden;border:2px solid #C9A962;'
                    f'box-shadow:0 26px 60px rgba(0,0,0,.55)"><img src="{src}" style="width:100%;height:100%;object-fit:cover">'
                    f'<div style="position:absolute;inset:auto 0 0 0;height:45%;background:linear-gradient(0deg,rgba(26,21,17,.92),rgba(26,21,17,0))"></div>'
                    f'<div style="position:absolute;left:22px;bottom:16px;font-size:34px;font-weight:800;letter-spacing:1px;color:#F4E6BC">{rotulo}</div></div>',
            "at": at, "anim": "pop", "style": {"top": f"{top}px", "left": f"{left}px"},
            "burst": {"x": left + w / 2, "y": top + h / 2, "n": 26, "raio": 220}}


ESCUDO = '<path class="desenha" d="M200 20 L360 80 L360 220 C360 330 290 400 200 440 C110 400 40 330 40 220 L40 80 Z"/><path class="desenha" d="M130 230 L185 285 L280 175"/>'
ECG = '<path class="desenha" d="M0 90 L250 90 L290 90 L315 20 L345 160 L370 60 L390 90 L560 90 L590 90 L615 30 L640 150 L662 90 L940 90"/>'
COLUNAS = ('<path class="desenha" d="M30 120 L270 30 L510 120 Z"/><path class="desenha" d="M60 150 L480 150"/>'
           '<path class="desenha" d="M100 170 L100 360"/><path class="desenha" d="M200 170 L200 360"/><path class="desenha" d="M340 170 L340 360"/>'
           '<path class="desenha" d="M440 170 L440 360"/><path class="desenha" d="M40 390 L500 390"/>')
HOSPITAL = '<rect class="desenha" x="20" y="20" width="200" height="200" rx="30"/><path class="desenha" d="M120 60 L120 180 M60 120 L180 120"/>'
CORACAO = '<path class="desenha" d="M60 100 C20 60 30 15 70 15 C95 15 105 35 110 45 C115 35 125 15 150 15 C190 15 200 60 160 100 L110 150 Z"/>'
BALANCA = ('<path class="desenha" d="M200 30 L200 380 M120 380 L280 380 M60 110 L340 110"/>'
           '<path class="desenha" d="M60 110 L20 220 L100 220 Z M340 110 L300 220 L380 220 Z"/>')

LINHA_HTML = ('<div style="position:relative;height:8px;background:rgba(232,222,209,.22);border-radius:4px">'
              '<div class="fill" style="height:100%;width:0;background:linear-gradient(90deg,#B8943F,#F4E6BC);border-radius:4px;box-shadow:0 0 22px #C9A962"></div></div>')


def no(rotulo, at, x, top=700, sub=""):
    return {"html": f'<div style="width:34px;height:34px;border-radius:50%;background:#F4E6BC;box-shadow:0 0 0 8px rgba(201,169,98,.25),0 0 30px #C9A962;margin:0 auto"></div>'
                    f'<div style="margin-top:22px;font-size:30px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#FAF6F0;text-align:center;white-space:nowrap">{rotulo}</div>'
                    + (f'<div style="font-size:24px;color:#E8DED1cc;text-align:center;white-space:nowrap">{sub}</div>' if sub else ""),
            "at": at, "anim": "pop", "style": {"top": f"{top - 13}px", "left": f"{x - 120}px", "width": "240px"}}


def outro(a, proxima, publico="quem precisa saber", gestante=False, area="Direito Trabalhista"):
    """Fechamento: logo formado por pó de ouro, pedido de envio (sends), próxima parte, CTA OAB, assinatura.
    Tudo entre y=360 e y=1240 (área limpa do Reels)."""
    els = [
        po("", a + .05, 540, 450, size=190, dur=.9, img=data_url(AQUI / "midia" / "logo.png"), burst=True),
        texto(f"Salve e mande para|<em>{publico}</em>.", a + .35, 600, size=84, align="center"),
        pilula(proxima, a + .75, 800, left=0, style=centro(700)),
        {"html": "Cada caso tem detalhes.<br>Procure uma advogada de confiança.", "at": a + .95, "anim": "sobe",
         "style": {"top": "905px", "left": "90px", "right": "90px", "textAlign": "center", "fontSize": "34px", "fontWeight": "600", "lineHeight": "1.4", "color": "#E8DED1"}},
    ]
    if gestante:
        els.append(texto("Dra. Letícia Barros,|a advogada da <em>Gestante trabalhadora</em>", a + 1.15, 1015, size=44, align="center", anim="sobe"))
    else:
        els.append(texto(f"Dra. Letícia Barros|<em>{area}</em>", a + 1.15, 1015, size=44, align="center", anim="sobe"))
    els.append({"html": "OAB/ES 39.948 · @adv.leticiabarros2", "cls": "kick", "at": a + 1.3, "anim": "sobe",
                "style": {"top": "1140px", "left": "0", "right": "0", "textAlign": "center"}})
    return {"a": a, "trans": "tinta", "particulas": 18, "outro": True, "els": els}


# --------------------------------------------------------------------------- montagem
def montar_cfg(n: int, REELS: dict):
    reel = REELS[n]
    linha, ws, fala = palavras_do_reel(reel["trechos"], reel)
    seg = [tr["ini"] for tr in linha]

    def W(txt, depois=-1.0):
        for w in ws:
            if w["a"] > depois and w["t"].lower() == txt.lower():
                return w["a"]
        for w in ws:
            if w["a"] > depois and w["t"].lower().strip(".,?!") == txt.lower().strip(".,?!"):
                return w["a"]
        raise KeyError(f"reel {n}: palavra '{txt}' depois de {depois}")

    cenas = reel["roteiro"](W, seg, round(fala, 3))
    oc = next((c for c in cenas if c.get("outro")), None)
    # o fechamento pode começar durante a fala final (CTA narrado); senão, vem depois da fala
    total = round(max(fala + 0.8, oc["a"] + OUTRO) if oc else fala + OUTRO, 3)
    eventos, bursts, punches = [], [], []
    for c in cenas:
        if c["trans"] in ("whip", "whipV", "zoom", "iris", "sobe", "tinta", "luz"):
            eventos.append((c["a"] - .12, "whoosh"))
        for e in c.get("els", []):
            if e.get("anim") == "carimbo":
                eventos.append((e["at"] + .14, "carimbo")); punches.append(e["at"] + .1)
            elif e.get("anim") == "pop":
                eventos.append((e["at"], "pop"))
            if e.get("tipo") == "po":
                eventos.append((e["at"], "po"))
            if e.get("burst"):
                b = e["burst"]
                bursts.append({"t": e["at"] + b.get("dt", .12), "x": b["x"], "y": b["y"], "n": b.get("n", 70), "raio": b.get("raio", 420)})
    # soco nas palavras-chave: quebra de padrão a cada 2–4 s, nunca colado em outro soco
    for w in ws:
        if w["d"]:
            punches.append(w["a"])
    punches.sort()
    socos = []
    for p in punches:
        if not socos or p - socos[-1] >= 2.2:
            socos.append(p)
    eventos.append((0.0, "boom"))
    eventos.append(((oc["a"] if oc else fala) + .2, "brilho"))
    flashes = [c["a"] for c in cenas if c["trans"] == "corte" and c["a"] > 0]
    sem_leg = oc["a"] if oc else fala
    rotulo = reel.get("serie") or f"{CFG['serie']} · {n}/{len(REELS)}"
    cfg = {"serie": rotulo, "total": total, "cenas": cenas, "leg": blocos(ws, seg[1:]),
           "flashes": flashes, "semLegenda": [[sem_leg, total + 1], *reel.get("sem_legenda", [])], "energia": energia(reel["trechos"], total, reel.get("src")),
           "bursts": bursts, "punches": socos, "poeira": reel.get("poeira", 200)}
    (AQUI / f"cfg_r{n}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    return cfg, sorted(eventos)


def checar_leitura(cfg) -> list[str]:
    """Títulos precisam ficar na tela o bastante para serem lidos (≤ 15 caracteres por segundo)."""
    avisos, cenas = [], cfg["cenas"]
    for i, c in enumerate(cenas):
        fim = cenas[i + 1]["a"] if i + 1 < len(cenas) else cfg["total"]
        for e in c.get("els", []):
            if e.get("tipo") != "texto":
                continue
            limpo = __import__("re").sub(r"<[^>]+>", "", e["html"]).replace("|", " ")
            dur = (e.get("ate") or fim) - e["at"]
            if dur > 0 and len(limpo) / dur > 15:
                avisos.append(f"cena {i} '{limpo[:40]}': {len(limpo)} caracteres em {dur:.1f}s ({len(limpo) / dur:.0f}/s)")
    return avisos


async def renderizar(n, cfg, so_amostras=None, checar=False):
    pasta = AQUI / f"quadros_r{n}"
    if pasta.exists() and not so_amostras and not checar and not os.environ.get("DESDE_QUADRO"):
        shutil.rmtree(pasta)
    pasta.mkdir(exist_ok=True)
    problemas = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--allow-file-access-from-files"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.goto((AQUI / "engine.html").as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.evaluate("cfg => init(cfg)", cfg)
        if checar:
            tempos = [i * .2 for i in range(int(cfg["total"] / .2))]
        else:
            tempos = so_amostras or [i / FPS for i in range(int(round(cfg["total"] * FPS)))]
        desde = int(os.environ.get("DESDE_QUADRO", "0"))
        for i, t in enumerate(tempos):
            if not so_amostras and not checar and i < desde:
                continue
            await page.evaluate(f"render({t:.4f})")
            if checar:
                problemas += await page.evaluate(f"checar({t:.4f})")
                continue
            nome = f"amostra_r{n}_{t:05.2f}.jpg" if so_amostras else f"{i:05d}.jpg"
            await page.screenshot(path=str((AQUI if so_amostras else pasta) / nome), type="jpeg", quality=92)
            if not so_amostras and i % 300 == 0:
                print(f"r{n} quadro {i}/{len(tempos)}", flush=True)
        await browser.close()
    if checar:
        vistos = {}
        for pb in problemas:
            vistos.setdefault((pb["cena"], pb["el"]), pb)
        return list(vistos.values())
    return pasta


def codificar(n, pasta, total, com, sem, prefixo="reel", nome=None):
    saidas, base = [], nome or f"{prefixo}{n}"
    for audio_, nome in [(com, f"{base}.mp4"), (sem, f"{base}_sem_musica.mp4")]:
        destino = AQUI.parent / nome
        ff("-framerate", FPS, "-i", pasta / "%05d.jpg", "-i", audio_, "-map", "0:v", "-map", "1:a", "-t", total,
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", FPS,
           "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", destino)
        saidas.append(destino)
    return saidas


async def principal(REELS: dict, numeros, modo: str):
    (AQUI / "midia").mkdir(exist_ok=True)
    shutil.copy(ASSETS / "logo-leticia.png", AQUI / "midia" / "logo.png")
    efeitos = sfx(AQUI / "sfx")
    for n in numeros:
        cfg, eventos = montar_cfg(n, REELS)
        for a in checar_leitura(cfg):
            print("LEITURA:", a)
        if modo == "checar":
            pbs = await renderizar(n, cfg, checar=True)
            print(f"r{n} área limpa:", "ok" if not pbs else "")
            for pb in pbs:
                print("  INVADE", pb)
            continue
        if modo == "amostras":
            cs = cfg["cenas"]
            ts = [float(x) for x in os.environ.get("TS", "").split(",") if x] or [
                round(c["a"] + 0.7 * ((cs[i + 1]["a"] if i + 1 < len(cs) else cfg["total"]) - c["a"]), 2) for i, c in enumerate(cs)]
            await renderizar(n, cfg, ts)
            print("amostras r", n, [round(t, 2) for t in ts])
            continue
        pasta_audio = AQUI / f"audio_r{n}"
        pasta_audio.mkdir(exist_ok=True)
        com, sem = audio(REELS[n], pasta_audio, eventos, cfg["total"], efeitos)
        pasta = await renderizar(n, cfg)
        print("ok", codificar(n, pasta, cfg["total"], com, sem, REELS[n].get("prefixo", "reel"), REELS[n].get("nome")), flush=True)


def rodar(REELS: dict, argv):
    modo = "amostras" if "--amostras" in argv else "checar" if "--checar" in argv else "render"
    nums = [int(a) for a in argv if a.isdigit()] or list(REELS)
    asyncio.run(principal(REELS, nums, modo))
