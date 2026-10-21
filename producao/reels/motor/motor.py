"""Motor v2 dos Reels da Letícia (motion design + camada procedural).

Genérico: áudio (voz tratada e efeitos sintetizados; sem música nem ambiência desde 21/10/2026), energia da voz,
legenda por frase, blocos de cena, pó de ouro, explosões, soco na palavra-chave, transições
(tinta, luz, whip, zoom, íris...), punch-in alternado nas emendas do rosto, verificador da área limpa e da
velocidade de leitura, render quadro a quadro (Playwright) e codificação H.264 pronta para a API da Meta.

Padrão premium (21/10/2026, skill leticia-reels-premium): uma entrega por vídeo, sem trilha; mix final a -14 LUFS
e pico -1 dBTP; H.264 a 11 Mbps (10 a 12); efeitos com 3 a 4 variações por tipo, sorteadas com semente fixa,
8 a 12 dB abaixo da voz e abaixados enquanto ela fala; sem ambiência (o ruído de fundo virou chiado).

O roteiro de cada série fica em serie.py, que importa daqui e define REELS. Cenas de rosto marcam "rosto": True
no bg; as emendas vêm de fala.py (fala-rN.emendas.json ao lado do src).
"""
import asyncio
import base64
import json
import os
import random
import re
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
def _variacoes() -> dict[str, list[list[str]]]:
    """3 a 4 versões de cada efeito (mesma família, timbre e duração diferentes), todas sintetizadas aqui."""
    def whoosh(cor, d, hp, lp):
        return ["-f", "lavfi", "-i", f"anoisesrc=color={cor}:d={d}:a=0.6:seed=7", "-af",
                f"highpass=f={hp},lowpass=f={lp},afade=t=in:d={d / 2}:curve=exp,afade=t=out:st={d / 2}:d={d / 2}"]

    def ev(expr, d, af=None):
        return ["-f", "lavfi", "-i", f"aevalsrc='{expr}':d={d}:s=48000", *(["-af", af] if af else [])]
    return {
        "whoosh": [whoosh("pink", 0.55, 350, 4200), whoosh("brown", 0.5, 200, 3000), whoosh("white", 0.45, 700, 6500),
                   whoosh("pink", 0.65, 250, 3400)],
        "boom": [ev(f"0.95*sin(2*PI*({f0}+60*exp(-9*t))*t)*exp(-{k}*t)", 1.4, "lowpass=f=900") for f0, k in ((45, 3.5), (38, 3.0), (52, 4.2), (42, 3.8))],
        "pop": [ev(f"0.55*sin(2*PI*({f0}+900*exp(-28*t))*t)*exp(-{k}*t)", 0.25) for f0, k in ((520, 22), (640, 26), (430, 20))],
        "carimbo": [ev(f"(0.9*sin(2*PI*{f0}*t)+0.5*sin(2*PI*{2 * f0}*t))*exp(-{k}*t)", 0.4, "lowpass=f=1200") for f0, k in ((85, 16), (72, 14), (98, 18))],
        "brilho": [ev(f"0.16*(sin(2*PI*{a}*t)+sin(2*PI*{b}*t)+0.7*sin(2*PI*{c}*t))*exp(-3*t)", 1.6, "aecho=0.8:0.6:60:0.35")
                   for a, b, c in ((1760, 2637, 3520), (1568, 2349, 3136), (1976, 2960, 3951))],
        # pó de ouro se formando: cintilação que sobe
        "po": [ev(f"0.10*sin(2*PI*({f0}+{sobe}*t)*t)*(0.5+0.5*sin(2*PI*{tr}*t))*exp(-1.6*t)", 1.3, "highpass=f=600,aecho=0.8:0.5:45:0.3")
               for f0, sobe, tr in ((900, 1800, 31), (750, 2200, 27), (1100, 1500, 37))],
    }


# pico de cada efeito em dBFS; a voz chega a -1,5 dBTP, então o efeito fica 8 a 12 dB abaixo dela
NIVEL_DB = {"whoosh": -13, "boom": -10, "pop": -12, "carimbo": -10, "brilho": -13, "po": -13}


def sfx(pasta: Path) -> dict[str, list[Path]]:
    """Biblioteca de efeitos sintetizados (sem direitos de terceiros), cada versão com pico em 0 dBFS."""
    pasta.mkdir(exist_ok=True)
    saida = {}
    for tipo, versoes in _variacoes().items():
        saida[tipo] = []
        for k, args in enumerate(versoes):
            destino = pasta / f"{tipo}_{k}.wav"
            if not destino.exists():
                bruto = pasta / f"_{tipo}_{k}.wav"
                ff(*args, "-ac", "2", "-ar", "48000", bruto)
                log = subprocess.run([str(FF), "-hide_banner", "-nostats", "-i", str(bruto), "-af", "volumedetect", "-f", "null", "-"],
                                     capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
                pico = float(re.search(r"max_volume: (-?[\d.]+) dB", log).group(1))
                ff("-i", bruto, "-af", f"volume={-pico}dB", destino)
                bruto.unlink()
            saida[tipo].append(destino)
    return saida


def sortear_efeitos(eventos, versoes: dict[str, int], semente: int) -> list[tuple[float, str, int]]:
    """Escolhe a versão de cada efeito com semente fixa (o mesmo Reel sai sempre igual), sem repetir a mesma versão
    duas vezes seguidas no mesmo tipo."""
    rnd, ultima, saida = random.Random(semente), {}, []
    for t, tipo in eventos:
        opcoes = [k for k in range(versoes[tipo]) if k != ultima.get(tipo)] or [0]
        k = rnd.choice(opcoes)
        ultima[tipo] = k
        saida.append((t, tipo, k))
    return saida


def _lufs(arq) -> float:
    log = subprocess.run([str(FF), "-hide_banner", "-nostats", "-i", str(arq), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", log[log.rfind("Summary:"):]).group(1))


def _loudnorm(entrada: Path, destino: Path, alvo=-14.0, pico=-1.5, total=None) -> None:
    """Crava o volume integrado: ganho + limitador de pico, reajustado em até 4 rodadas até ficar a 0,2 LU do alvo.
    (O loudnorm linear não sobe o ganho quando há pico alto, e a voz tratada tem picos de consoante: a validação de
    21/10/2026 saiu em -15 LUFS.) O limitador corta a amostra em pico - 0,5 dB; a entrega fica abaixo de -1 dBTP
    mesmo depois do AAC."""
    limite = 10 ** ((pico - 0.5) / 20)
    ganho = alvo - _lufs(entrada)
    for _ in range(4):
        ff("-i", entrada, "-af", f"volume={ganho:.2f}dB,alimiter=limit={limite:.4f}:attack=3:release=60:level=disabled,aresample=48000",
           *(["-t", total] if total else []), "-ar", "48000", "-ac", "2", destino)
        erro = alvo - _lufs(destino)
        if abs(erro) <= 0.2:
            break
        ganho += erro


def audio(reel, pasta: Path, eventos, total: float, efeitos: dict, semente: int = 21) -> Path:
    """Voz tratada + efeitos (abaixados sob a voz), normalizado a -14 LUFS / -1 dBTP."""
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
    # voz limpa (16/10/2026): RNNoise (modelo aberto em modelos/) tira o ruído de fundo (~11 dB a menos no teste da
    # série Guarda), afftdn leve no que sobra, de-esser, corte de 250 Hz (som abafado), presença em 3,2 kHz e brilho em 10 kHz
    modelo = (AQUI / "modelos" / "voz-sh.rnnn").as_posix().replace(":", r"\:")
    ff("-f", "concat", "-safe", "0", "-i", lista, "-af",
       f"highpass=f=80,arnndn=m='{modelo}':mix=0.9,afftdn=nr=8:nf=-35,deesser=i=0.4,"
       "equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=10000:t=h:w=0.7:g=1.5,"
       f"acompressor=threshold=-20dB:ratio=3:attack=8:release=120,loudnorm=I=-14:TP=-1.5:LRA=9,apad=whole_dur={total}",
       "-ar", "48000", "-ac", "2", voz)
    # sem ambiência: o "ar de sala" (ruído marrom a -32 LUFS) virou chiado que abafava a voz (Jessica, 21/10/2026);
    # as pausas ficam no silêncio da voz tratada
    entradas, filtros = ["-i", voz], []
    sorteio = sortear_efeitos(eventos, {k: len(v) for k, v in efeitos.items()}, semente)
    for i, (t, tipo, k) in enumerate(sorteio):
        entradas += ["-i", efeitos[tipo][k]]
        ms = int(max(0, t) * 1000)
        filtros.append(f"[{i + 1}:a]adelay={ms}|{ms},volume={NIVEL_DB[tipo]}dB[e{i}]")
    if sorteio:
        fx = "".join(f"[e{i}]" for i in range(len(sorteio)))
        # o efeito nunca cobre palavra: o barramento de efeitos abaixa ~8 dB enquanto a voz soa
        filtros += ["[0:a]asplit=2[v1][v2]",
                    f"{fx}amix=inputs={len(sorteio)}:normalize=0:duration=longest,apad=whole_dur={total}[fx]",
                    "[fx][v2]sidechaincompress=threshold=0.03:ratio=6:attack=5:release=250:makeup=1[fxd]",
                    "[v1][fxd]amix=inputs=2:normalize=0:duration=first[o]"]
    else:
        filtros.append("[0:a]anull[o]")
    bruto = pasta / "mix_bruto.wav"
    ff(*entradas, "-filter_complex", ";".join(filtros), "-map", "[o]", "-t", total, "-ar", "48000", bruto)
    mix = pasta / "mix.wav"
    _loudnorm(bruto, mix, total=total)
    return mix


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
                    + (f'<div style="font-size:27px;color:#E8DED1cc;text-align:center;white-space:nowrap">{sub}</div>' if sub else ""),
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
    return {"a": a, "trans": "tinta", "outro": True, "els": els}


def fim_da_fala(transcricao, src) -> float:
    """Onde a fala termina no Reel: fim da última palavra + 0,25 s, sem passar do último quadro do vídeo da fala
    (passando, a última cena de rosto congelava antes do fechamento: série 18 v2)."""
    d = json.loads(Path(transcricao).read_text(encoding="utf-8"))
    ultima = max(w["end"] for s in d["segments"] for w in s["words"])
    dur = float(subprocess.run([str(FF).replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(src)], capture_output=True, text=True, check=True).stdout)
    return round(min(ultima + 0.25, dur - 1 / FPS), 3)


# --------------------------------------------------------------------------- punch-in
def emendas_no_reel(emendas_src, linha) -> list[float]:
    """Emendas da fala (tempo do src) no tempo do Reel; as que caem fora dos trechos usados somem."""
    saida = []
    for e in emendas_src:
        for tr in linha:
            if tr["ini_src"] < e < tr["fim_src"]:
                saida.append(round(tr["ini"] + e - tr["ini_src"], 3))
    return saida


def punch_in(cenas, emendas, fator=1.12, colada=0.15) -> None:
    """Toda emenda no rosto ganha punch-in alternado (normal / fator): grava bg["zooms"] = [[t na cena, zoom], ...]
    nas cenas com bg["rosto"]. A alternância continua de uma cena de rosto para a próxima; emenda colada no início
    ou no fim da cena é ignorada (o corte de cena já cobre)."""
    estado = fator
    for i, c in enumerate(cenas):
        bg = c.get("bg") or {}
        if not bg.get("rosto"):
            continue
        fim = cenas[i + 1]["a"] if i + 1 < len(cenas) else float("inf")
        estado = 1.0 if estado != 1.0 else fator
        zooms = [[0.0, estado]]
        for e in emendas:
            if c["a"] + colada < e < fim - colada:
                estado = 1.0 if estado != 1.0 else fator
                zooms.append([round(e - c["a"], 3), estado])
        bg["zooms"] = zooms


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
    emendas = reel.get("emendas")
    arq_emendas = Path(reel.get("src", CFG["src"])).with_suffix(".emendas.json")
    if emendas is None and arq_emendas.exists():
        emendas = json.loads(arq_emendas.read_text())
    punch_in(cenas, emendas_no_reel(emendas or [], linha), reel.get("punch", 1.12))
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
           "bursts": bursts, "punches": socos, "poeira": reel.get("poeira", 0)}
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
            tempos = [i * .1 for i in range(int(cfg["total"] / .1))]
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


def codificar(n, pasta, total, audio_, prefixo="reel", nome=None) -> Path:
    """Uma entrega por vídeo: H.264 a 11 Mbps (10 a 12, exportação do manual), AAC 128 kbps a 48 kHz."""
    destino = AQUI.parent / f"{nome or f'{prefixo}{n}'}.mp4"
    if destino.exists():
        raise FileExistsError(f"{destino} já existe: versão nova é arquivo novo (-v2)")
    # taxa constante (CBR): com taxa média, o x264 entrega 4 a 9 Mbps quando a imagem é simples (motion graphics),
    # nem com duas passadas chega a 10; o CBR completa com enchimento e crava os 11 Mbps
    ff("-framerate", FPS, "-i", pasta / "%05d.jpg", "-i", audio_, "-map", "0:v", "-map", "1:a", "-t", total,
       "-c:v", "libx264", "-preset", "slow", "-b:v", "11M", "-minrate", "11M", "-maxrate", "11M", "-bufsize", "11M",
       "-x264-params", "nal-hrd=cbr:force-cfr=1", "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", FPS,
       "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", destino)
    return destino


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
        mix = audio(REELS[n], pasta_audio, eventos, cfg["total"], efeitos, REELS[n].get("semente", 20 + n))
        pasta = await renderizar(n, cfg)
        print("ok", codificar(n, pasta, cfg["total"], mix, REELS[n].get("prefixo", "reel"), REELS[n].get("nome")), flush=True)


def rodar(REELS: dict, argv):
    modo = "amostras" if "--amostras" in argv else "checar" if "--checar" in argv else "render"
    nums = [int(a) for a in argv if a.isdigit()] or list(REELS)
    asyncio.run(principal(REELS, nums, modo))
