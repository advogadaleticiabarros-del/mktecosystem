"""Motor dos Reels motion diários (Papel e Ouro), no molde do 23:47 (09/11/2026, pedido da Jessica: "pelo menos 1
motion original desse por dia"). Cada episódio entrega só a cena (HTML, CSS, função JS `cena(t)`) e os eventos de som;
o motor cuida do fundo café, fios de ouro, grão, fechamento com logo, conferência de área segura, efeitos reais da
Mixkit (licença livre para uso comercial, sem atribuição) e volume -14 LUFS. Sem narração: rótulo de IA desligado.

Uso: python <episodio>.py amostras "0.5,4,9,12,17" | python <episodio>.py video"""
import asyncio
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

sys.path.insert(0, r"C:\Users\prosy\mktecosystem\producao\estilos\palavra-de-ouro")
from base import FOIL, LOGO, MARCA, ruido  # noqa: E402

AQUI = Path(__file__).resolve().parent
SFX = AQUI / "sfx"
FPS, SR = 30, 48000
EXTRA = 2.0  # v2: o fechamento ganhou 2 s (leia a legenda + seguir e compartilhar)
VERSAO = "v2"
CTA = "Quer ficar por dentro dos seus direitos? Clique em seguir e compartilhe com quem precisa saber disso."

# nome: (id Mixkit, início s, duração máx. s, ganho)
SONS = {
    "pop": (2574, 0, .5, .55),          # Message pop alert
    "bolha": (2575, 0, .5, .5),         # Bubble pop up alert notification
    "digita": (1377, 0, 3.0, .35),      # Typing text on a smartphone
    "tique": (1045, 0, .35, .45),       # Tick tock clock close up
    "relogio": (1046, 0, 4.0, .35),     # Fast wall clock ticking
    "pagina": (1107, 0, .9, .5),        # Page turn single
    "escreve": (1103, 0, 1.2, .5),      # Writing scribble on paper
    "assina": (1099, 0, 1.2, .5),       # Signing on a paper
    "moedas": (1999, 0, 1.2, .45),      # Clinking coins
    "erro": (2310, 0, 1.0, .4),         # Wrong answer fail notification
    "whoosh": (1491, 0, .9, .45),       # Cinematic whoosh fast transition
    "boom": (788, 0, 1.8, .55),         # Cinematic whoosh deep impact
    "carimbo": (2589, 0, .7, .6),       # Wood hard hit
    "brilho": (866, 0, 1.6, .35),       # Fairy magic sparkle
    "sino": (2357, 0, 1.2, .4),         # Bell notification
}


def baixar(i):
    SFX.mkdir(exist_ok=True)
    arq = SFX / f"mixkit-{i}.mp3"
    if not arq.exists():
        req = urllib.request.Request(f"https://assets.mixkit.co/active_storage/sfx/{i}/{i}-preview.mp3",
                                     headers={"User-Agent": "Mozilla/5.0"})
        arq.write_bytes(urllib.request.urlopen(req).read())
    return arq


def amostra(nome):
    i, ini, dur, ganho = SONS[nome]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ini), "-t", str(dur), "-i", str(baixar(i)),
                          "-af", f"afade=t=out:st={max(dur - .2, 0)}:d=0.2", "-ac", "2", "-ar", str(SR),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, "<i2").reshape(-1, 2) / 32768
    return x / (np.abs(x).max() + 1e-9) * ganho


def vibracao(dur=.16):
    """Vibração de celular sintetizada (a do 23:47, aprovada): dois zumbidos curtos."""
    t = np.arange(int(SR * (.23 + dur))) / SR
    z = np.zeros_like(t)
    for g in (0, .23):
        m = (t >= g) & (t < g + dur)
        x = t[m] - g
        z[m] = .5 * np.sin(2 * np.pi * 165 * x) * np.sin(np.pi * x / dur) ** .5 * (1 + .4 * np.sin(2 * np.pi * 330 * x))
    return np.stack([z, z], 1)


def batida():
    """Batida seca de carimbo (10/11/2026): grave com queda de afinação + estalo curto do papel."""
    t = np.arange(int(SR * .5)) / SR
    f = 45 + 95 * np.exp(-t * 28)
    grave = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    rng = np.random.default_rng(7)
    ruido = rng.standard_normal(len(t))
    ruido = np.convolve(ruido, np.ones(6) / 6, "same") * np.exp(-t * 90)
    z = .9 * grave + .55 * ruido
    z = np.tanh(z * 1.8) / np.tanh(1.8)
    return np.stack([z, z], 1) * .95


def vento(dur=.72):
    """Deslocamento de ar que cresce até a batida (10/11/2026): ruído filtrado com corte e volume subindo."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)
    r = rng.standard_normal((n, 2))
    corte = 300 + 5200 * (t / dur) ** 2
    a = 1 - np.exp(-2 * np.pi * corte / SR)
    y = np.zeros_like(r)
    acc = np.zeros(2)
    for i in range(n):
        acc += a[i] * (r[i] - acc)
        y[i] = acc
    env = (t / dur) ** 2.2
    env[-int(SR * .015):] *= np.linspace(1, 0, int(SR * .015))
    y = y * env[:, None]
    return y / (np.abs(y).max() + 1e-9) * .6


def clique():
    """Clique da lingueta da roleta (10/11/2026): estalo curto de plástico com um 'tic' agudo."""
    t = np.arange(int(SR * .06)) / SR
    rng = np.random.default_rng(11)
    z = (.7 * rng.standard_normal(len(t)) * np.exp(-t * 400) + .6 * np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 160)
         + .4 * np.sin(2 * np.pi * 900 * t) * np.exp(-t * 90))
    z = z / (np.abs(z).max() + 1e-9) * .5
    return np.stack([z, z], 1)


def mixar(eventos, dur, arq):
    """eventos: lista de (tempo, nome[, ganho extra]). Grava wav e normaliza a -14 LUFS."""
    s = np.zeros((int(SR * dur), 2))
    cache = {}
    for ev in eventos:
        t, nome = ev[0], ev[1]
        g = ev[2] if len(ev) > 2 else 1.0
        if nome not in cache:
            cache[nome] = vibracao() if nome == "vibra" else batida() if nome == "batida" else vento() if nome == "vento" else clique() if nome == "clique" else amostra(nome)
        x = cache[nome] * g
        i0 = int(t * SR)
        n = min(len(x), len(s) - i0)
        if n > 0:
            s[i0:i0 + n] += x[:n]
    bruto = arq.with_suffix(".bruto.wav")
    import wave
    with wave.open(str(bruto), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(s, -1, 1) * 32000).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", str(SR), str(arq)], check=True)
    bruto.unlink()


CSS_BASE = f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:#231E1A}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#231E1A;color:#EFE6D9;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
#g{{position:absolute;inset:0;background:url("{ruido('.95', '.9', '.9')}");mix-blend-mode:screen;opacity:.03}}
.fx{{position:absolute;left:0;right:0;height:19px;background:{FOIL}}}
#cena,#fim{{position:absolute;inset:0}}
.rot{{position:absolute;left:150px;right:150px;text-align:center;font:500 30px Inter}}
.big{{position:absolute;left:150px;right:150px;text-align:center;font:400 220px/1 'EB Garamond',serif;letter-spacing:-.01em}}
.card{{position:absolute;left:150px;width:780px;background:#EFE6D9;color:#1E1814;border-radius:28px;padding:18px 30px 22px;box-shadow:0 14px 34px rgb(0 0 0/.35)}}
.card .t{{display:flex;justify-content:space-between;font:600 27px Inter}}
.card .t b{{font-weight:500}}
.card .m{{font:400 35px/1.28 Inter;margin-top:6px}}
.bo{{position:absolute;max-width:640px;padding:18px 28px 20px;border-radius:30px;font:400 35px/1.3 Inter;box-shadow:0 10px 26px rgb(0 0 0/.3)}}
.bo.ele{{left:150px;background:#EFE6D9;color:#1E1814;border-bottom-left-radius:8px}}
.bo.eu{{right:150px;background:#4A3F35;color:#EFE6D9;border-bottom-right-radius:8px}}
.bo small{{display:block;font:500 24px Inter;opacity:.6;margin-top:4px;text-align:right}}
.pts span{{display:inline-block;width:16px;height:16px;border-radius:50%;background:#1E1814;margin:0 5px;opacity:.35}}
.marca{{position:absolute;left:0;right:0;text-align:center}}
.marca span{{display:inline-block;padding:6px 26px 14px;font:italic 400 92px/1.12 'EB Garamond',serif;color:#1E1814;white-space:nowrap;background:{MARCA};background-size:220% 100%}}
.sub{{position:absolute;left:150px;right:150px;text-align:center;font:400 34px/1.35 Inter}}
.ouro{{background:{FOIL};-webkit-background-clip:text;background-clip:text;color:transparent}}
#fim{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:270px 150px 672px}}
#fim img{{width:110px;height:110px}}
#nome{{font:500 66px/1.05 'EB Garamond',serif;margin-top:22px}}
#oab{{font:500 30px Inter;margin-top:10px}}
#fio{{width:780px;height:3px;background:{FOIL};margin:30px 0}}
#leia{{display:inline-block;padding:4px 22px 10px;font:italic 400 58px/1.12 'EB Garamond',serif;color:#1E1814;background:{MARCA};margin-bottom:30px}}
#seg{{font:400 31px/1.36 Inter;margin-top:16px}}
#salve{{font:italic 400 54px/1.14 'EB Garamond',serif}}
#caso{{font:400 27px/1.36 Inter;margin-top:26px;opacity:.75}}"""

JS_BASE = """const $=i=>document.getElementById(i),cl=x=>Math.min(1,Math.max(0,x));
const io=x=>{x=cl(x);return 1-Math.pow(1-x,3)},ioo=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const mola=x=>{x=cl(x);return 1-Math.exp(-6*x)*Math.cos(9*x)};
// entra subindo 14px; d = duração
const sobe=(el,t,s,d=.4)=>{const e=typeof el==='string'?$(el):el;const a=(t-s)/d;e.style.opacity=cl(a);e.style.transform=`translateY(${(1-io(a))*14}px)`};
// bolha/cartão que nasce com mola
const nasce=(el,t,s)=>{const e=typeof el==='string'?$(el):el;const a=t-s;e.style.opacity=a<0?0:cl(a/.18);e.style.transform=`translateY(${-34*(1-mola(a/.7))}px) scale(${.96+.04*mola(a/.7)})`};
// marca-texto dourado
const marca=(el,t,s)=>{const sp=$(el).firstElementChild,w=ioo((t-s)/.75);$(el).style.opacity=t<s?0:1;sp.style.clipPath=`inset(0 ${(1-w)*100}% 0 0)`;sp.style.backgroundPosition=`${120-((t-s)*22)}% 0`};
// tremida curta em instantes
const treme=(t,ins,amp=4)=>{let sh=0;for(const n of ins){const e=t-n;if(e>=0&&e<.34)sh=Math.sin(e*95)*amp*(1-e/.34)}return sh};
const pad=(n,k=2)=>String(n).padStart(k,'0');"""


def montar(ep):
    fim0 = ep["dur"] - 4.0
    return f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>{CSS_BASE}
{ep['css']}</style></head><body><div id=c>
<div id=cena>{ep['html']}</div>
<div id=fim><img src="{LOGO}"><div id=nome>Letícia Barros</div><div id=oab>OAB/ES 39.948</div><div id=fio></div>
<div id=leia>Leia a legenda</div><div id=salve>Quer ficar por dentro dos seus direitos?</div><div id=seg>Clique em seguir e compartilhe com quem precisa saber disso.</div><div id=caso>Cada caso tem detalhes. Procure uma advogada de confiança.</div></div>
<div id=g></div><div class=fx style="top:0"></div><div class=fx style="bottom:0"></div></div>
<script>{JS_BASE}
{ep['js']}
window.render=t=>{{
 cena(t);
 const sai=cl((t-{fim0})/.5);$('cena').style.opacity=1-sai;$('fim').style.opacity=sai;
 $('fim').querySelector('img').style.opacity=cl((t-{fim0 + .1})/.4);
 sobe('nome',t,{fim0 + .25},.45);sobe('oab',t,{fim0 + .35},.45);sobe('leia',t,{fim0 + .7},.45);sobe('salve',t,{fim0 + 2.0},.45);sobe('seg',t,{fim0 + 2.5},.45);sobe('caso',t,{fim0 + 3.4},.45);
 $('fio').style.clipPath=`inset(0 ${{(1-ioo((t-{fim0 + .45})/.6))*100}}% 0 0)`;
}};
window.medir=()=>{{const o=[];document.querySelectorAll('#cena *,#fim *').forEach(e=>{{
 if(e.children.length&&!e.dataset.m)return;let p=e;while(p&&p.id!=='c'){{if(+getComputedStyle(p).opacity<.05)return;p=p.parentElement}}
 const b=e.getBoundingClientRect();if(!b.width)return;
 if(b.left<130||b.right>950||b.top<262||b.bottom>1262)o.push((e.id||e.className||e.tagName)+' '+[b.left,b.right,b.top,b.bottom].map(Math.round))}});return o}};
document.fonts.ready.then(()=>{{document.body.dataset.ok=1}});
</script></body></html>"""


async def _rodar(ep, pasta, modo, ts):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(montar(ep), wait_until="networkidle")
        await pg.wait_for_selector("body[data-ok]", state="attached")
        if modo == "amostras":
            fol = Image.new("RGB", (len(ts) * 300, 534), "white")
            for i, t in enumerate(ts):
                await pg.evaluate(f"render({t})")
                fora = await pg.evaluate("medir()")
                print(t, "ok" if not fora else json.dumps(fora, ensure_ascii=False))
                await pg.screenshot(path=str(pasta / "_q.jpg"), type="jpeg", quality=90)
                fol.paste(Image.open(pasta / "_q.jpg").resize((296, 526), Image.LANCZOS), (i * 300 + 2, 4))
            fol.save(pasta / "amostras.jpg", quality=88)
            (pasta / "_q.jpg").unlink()
        else:
            dur = ep["dur"] + EXTRA
            som = pasta / "som.wav"
            f0 = ep["dur"] - 4.0
            mixar(ep["sons"] + [(f0 + .7, "escreve", .7), (f0 + 2.0, "brilho", .5), (f0 + 2.5, "bolha", .7)], dur, som)
            saida = pasta / f"{ep['nome']}-{VERSAO}.mp4"
            ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", str(FPS),
                                   "-i", "-", "-i", str(som), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                                   "-c:a", "aac", "-b:a", "160k", "-ar", str(SR), "-shortest", "-movflags", "+faststart",
                                   str(saida)], stdin=subprocess.PIPE)
            avisos = set()
            for i in range(int(dur * FPS)):
                await pg.evaluate(f"render({i / FPS})")
                if i % 15 == 0:
                    avisos.update(await pg.evaluate("medir()"))
                ff.stdin.write(await pg.screenshot(type="jpeg", quality=95))
            ff.stdin.close()
            ff.wait()
            print("ffmpeg", ff.returncode, "| área segura:", "ok" if not avisos else sorted(avisos)[:8])
        await b.close()


def rodar(ep, arquivo):
    pasta = Path(arquivo).resolve().parent / ep["nome"]
    pasta.mkdir(exist_ok=True)
    leg = dict(ep["legenda"])
    if CTA not in leg["legenda"]:
        leg["legenda"] = leg["legenda"].replace("Cada caso tem detalhes.", CTA + "\n\nCada caso tem detalhes.", 1)
    (pasta / "legenda.json").write_text(json.dumps(leg, ensure_ascii=False, indent=2), encoding="utf-8")
    modo = sys.argv[1] if len(sys.argv) > 1 else "amostras"
    ts = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0.6, 3, 6, 9, 11, 13, 17, 21.5]
    asyncio.run(_rodar(ep, pasta, modo, ts))
