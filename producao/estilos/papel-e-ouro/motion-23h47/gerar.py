"""Motion graphics do 23:47 (Papel e Ouro). Determinístico por tempo. Só prévia.
Uso: python gerar.py amostras "0.2,3.5" | python gerar.py video"""
import asyncio
import json
import math
import random
import struct
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, r"C:\Users\prosy\mktecosystem\producao\estilos\palavra-de-ouro")
from base import FOIL, LOGO, MARCA, ruido  # noqa: E402

DUR, FPS = 20.0, 30
FIO = FOIL
HTML = f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;background:#231E1A}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#231E1A;color:#EFE6D9;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
#g{{position:absolute;inset:0;background:url("{ruido('.95', '.9', '.9')}");mix-blend-mode:screen;opacity:.03}}
.fx{{position:absolute;left:0;right:0;height:19px;background:{FOIL}}}
#cena,#fim{{position:absolute;inset:0}}
#dia{{position:absolute;left:150px;right:150px;top:276px;text-align:center;font:500 30px Inter}}
#dia span{{position:absolute;left:0;right:0}}
#rel{{position:absolute;left:150px;right:150px;top:318px;height:250px;display:flex;justify-content:center;font-family:'EB Garamond',serif;font-size:240px;line-height:250px;letter-spacing:-.01em}}
.d{{position:relative;width:.5em;height:250px;overflow:hidden;-webkit-mask-image:linear-gradient(transparent,#000 14%,#000 86%,transparent);mask-image:linear-gradient(transparent,#000 14%,#000 86%,transparent)}}
.d span{{position:absolute;left:0;right:0;text-align:center;top:0}}
.dp{{width:.28em;text-align:center}}
.card{{position:absolute;left:150px;width:780px;background:#EFE6D9;color:#1E1814;border-radius:28px;padding:18px 30px 22px;box-shadow:0 14px 34px rgb(0 0 0/.35)}}
.card .t{{display:flex;justify-content:space-between;font:600 27px Inter}}
.card .t b{{font-weight:500}}
.card .m{{font:400 35px/1.28 Inter;margin-top:6px;white-space:nowrap}}
#ela{{position:absolute;left:150px;top:1004px;font:500 36px Inter}}
#marca{{position:absolute;left:138px;top:1060px;padding:6px 26px 14px 12px;font:italic 400 98px/1.12 'EB Garamond',serif;color:#1E1814;white-space:nowrap;background:{MARCA};background-size:220% 100%}}
#com{{position:absolute;left:150px;top:1196px;font:400 34px Inter}}
#fim{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:270px 150px 672px}}
#fim img{{width:130px;height:130px}}
#nome{{font:500 74px/1.05 'EB Garamond',serif;margin-top:22px}}
#oab{{font:500 30px Inter;margin-top:10px}}
#fio{{width:780px;height:3px;background:{FOIL};margin:40px 0}}
#salve{{font:italic 400 62px/1.14 'EB Garamond',serif}}
#caso{{font:400 31px/1.36 Inter;margin-top:30px}}
</style></head><body><div id=c>
<div id=cena><div id=dia><span id=d1>terça-feira</span><span id=d2>quarta-feira</span></div><div id=rel></div>
<div class=card id=c0><div class=t><span>Chefe</span><b></b></div><div class=m>Oi??</div></div>
<div class=card id=c1><div class=t><span>Chefe</span><b></b></div><div class=m>Preciso disso para amanhã cedo.</div></div>
<div class=card id=c2><div class=t><span>Chefe</span><b></b></div><div class=m>Viu o que te mandei?</div></div>
<div id=ela>Ela respondeu às 8h.</div><div id=marca>Quem está errado?</div><div id=com>Comente o que você acha.</div></div>
<div id=fim><img src="{LOGO}"><div id=nome>Letícia Barros</div><div id=oab>OAB/ES 39.948</div><div id=fio></div>
<div id=salve>Salve e mande para quem recebe mensagem fora de hora.</div><div id=caso>Cada caso tem detalhes. Procure uma advogada de confiança.</div></div>
<div id=g></div><div class=fx style="top:0"></div><div class=fx style="bottom:0"></div></div>
<script>
const $=i=>document.getElementById(i),cl=(x)=>Math.min(1,Math.max(0,x));
const io=x=>{{x=cl(x);return 1-Math.pow(1-x,3)}},ioo=x=>{{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}};
const mola=x=>{{x=cl(x);return 1-Math.exp(-6*x)*Math.cos(9*x)}};
const H=[[0,'2338'],[2.4,'2343'],[5.4,'2347'],[9.0,'0800']],RD=.6;
const NASC=[.5,3.0,6.0],MIN=[38,43,47],SLOT=137,Y0=572;
const rel=$('rel');rel.innerHTML=[0,1,'c',2,3].map(i=>i==='c'?'<div class=dp>:</div>':`<div class=d id=d${{i}}x><span></span><span></span></div>`).join('');
const mins=t=>t<2.4+RD/2?38:t<5.4+RD/2?43:47;
window.render=t=>{{
 let k=0;for(let i=0;i<H.length;i++)if(t>=H[i][0])k=i;
 const cur=H[k][1],prev=k?H[k-1][1]:cur,p=k?ioo((t-H[k][0])/RD):1;
 for(let i=0;i<4;i++){{const b=$(`d${{i}}x`),[a,n]=b.children;
  if(prev[i]===cur[i]){{a.textContent=cur[i];a.style.transform='';n.textContent=''}}
  else{{a.textContent=prev[i];n.textContent=cur[i];a.style.transform=`translateY(${{-p*100}}%)`;n.style.transform=`translateY(${{(1-p)*100}}%)`}}}}
 const m=mins(t);
 for(let i=0;i<3;i++){{const c=$('c'+i),e=t-NASC[i];
  c.style.opacity=e<0?0:cl(e/.18);
  let y=Y0-34*(1-mola(e/.7));for(let j=i+1;j<3;j++)y+=SLOT*ioo((t-NASC[j])/.45);
  c.style.top=y+'px';const dt=m-MIN[i];c.querySelector('b').textContent=dt<=0?'agora':'há '+dt+' min';}}
 const dim=1-.62*ioo((t-9.0)/.7);$('c0').style.filter=$('c1').style.filter=$('c2').style.filter=`brightness(${{dim}})`;
 const v=ioo((t-9.0)/.5);$('d1').style.opacity=1-v;$('d2').style.opacity=v;
 let sh=0;for(const n of NASC){{const e=t-n;if(e>=0&&e<.34)sh=Math.sin(e*95)*4*(1-e/.34)}}
 $('cena').style.transform=`translateX(${{sh}}px)`;
 const f=(el,a)=>{{$(el).style.opacity=cl(a);$(el).style.transform=`translateY(${{(1-io(a))*14}}px)`}};
 f('ela',(t-9.8)/.4);f('com',(t-13.0)/.4);
 const w=ioo((t-11.4)/.75);$('marca').style.clipPath=`inset(0 ${{(1-w)*100}}% 0 0)`;$('marca').style.backgroundPosition=`${{120-((t-11.4)*22)}}% 0`;
 const sai=cl((t-16)/.5);$('cena').style.opacity=1-sai;$('fim').style.opacity=sai;
 const pg=(el,s)=>{{$(el).style.opacity=cl((t-s)/.45);$(el).style.transform=`translateY(${{(1-io((t-s)/.45))*14}}px)`}};
 pg('nome',16.25);pg('oab',16.35);pg('salve',16.7);pg('caso',17.3);$('fio').style.clipPath=`inset(0 ${{(1-ioo((t-16.45)/.6))*100}}% 0 0)`;
 $('fim').querySelector('img').style.opacity=cl((t-16.1)/.4);
}};
window.medir=()=>{{const o=[];for(const q of ['#dia span','#rel','.card','#ela','#marca','#com','#nome','#oab','#fio','#salve','#caso','#fim img']){{document.querySelectorAll(q).forEach(e=>{{if(getComputedStyle(e).opacity==='0')return;const c=e.closest('#cena,#fim');if(c&&getComputedStyle(c).opacity==='0')return;const b=e.getBoundingClientRect();if(b.left<138||b.right>942||b.top<270||b.bottom>1248)o.push(q+' '+[b.left,b.right,b.top,b.bottom].map(Math.round))}})}}return o}};
document.fonts.ready.then(()=>{{document.body.dataset.ok=1}});
</script></body></html>"""


def som(arq):
    """Efeitos sintetizados discretos: vibração nas mensagens, tique no relógio, toque no marca-texto."""
    sr = 48000
    n = int(sr * DUR)
    s = [0.0] * n
    rnd = random.Random(7)

    def som_em(t, dur, fn):
        i0 = int(t * sr)
        for i in range(int(dur * sr)):
            if i0 + i < n:
                s[i0 + i] += fn(i / sr)

    def vibra(t):
        for g in (0, .23):
            som_em(t + g, .16, lambda x: .24 * math.sin(x * 1 * 2 * math.pi * 165) * math.sin(math.pi * x / .16) ** .5 * (1 + .4 * math.sin(2 * math.pi * 330 * x)))

    for t in (.5, 3.0, 6.0):
        vibra(t)
    for t in (2.4, 5.4, 9.0):
        for g in range(4 if t == 9.0 else 2):
            som_em(t + .12 + g * .09, .03, lambda x: .1 * rnd.uniform(-1, 1) * math.exp(-x * 140))
    som_em(11.45, .9, lambda x: .3 * math.sin(2 * math.pi * 78 * x) * math.exp(-x * 7))
    som_em(11.5, .9, lambda x: .05 * math.sin(2 * math.pi * 1760 * x) * math.exp(-x * 6))
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32000)) for v in s))


async def main():
    modo = sys.argv[1]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(HTML, wait_until="networkidle")
        await pg.wait_for_selector("body[data-ok]", state="attached")
        if modo == "amostras":
            ts = [float(x) for x in sys.argv[2].split(",")]
            fol = Image.new("RGB", (len(ts) * 300, 534), "white")
            for i, t in enumerate(ts):
                await pg.evaluate(f"render({t})")
                print(t, json.dumps(await pg.evaluate("medir()"), ensure_ascii=False))
                await pg.screenshot(path=str(AQUI / "_q.jpg"), type="jpeg", quality=90)
                fol.paste(Image.open(AQUI / "_q.jpg").resize((296, 526), Image.LANCZOS), (i * 300 + 2, 4))
            fol.save(AQUI / "amostras.jpg", quality=88)
            (AQUI / "_q.jpg").unlink()
        else:
            som(AQUI / "som.wav")
            ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", str(FPS), "-i", "-", "-i", str(AQUI / "som.wav"),
                                   "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(AQUI / "23h47-motion.mp4")], stdin=subprocess.PIPE)
            for i in range(int(DUR * FPS)):
                await pg.evaluate(f"render({i / FPS})")
                ff.stdin.write(await pg.screenshot(type="jpeg", quality=95))
            ff.stdin.close()
            ff.wait()
            print("ffmpeg", ff.returncode)
        await b.close()


asyncio.run(main())
