"""Viraliza Fora da Caixa: mesmos temas, peças conceituais. Só prévia: não toca em peça, banco ou agenda."""
import asyncio
import base64
import io
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

API = Path(__file__).resolve().parents[3] / "apps" / "api"
AQUI = Path(__file__).resolve().parent
RET = API / "_saida_producao_1510/_retratos"
ACAB = next((API / "app/assets").glob("*dourad*"))
SAIDA = AQUI / "pecas"
LOGO = "data:image/png;base64," + base64.b64encode((API / "app/assets/logo-leticia.png").read_bytes()).decode()
PAPEL, OURO, CAFE, FUNDO = "#E8DFD2", "#C9A962", "#1E1814", "#231E1A"


def foto(nome, caixa=None, largura=700):
    f = Image.open(RET / nome).convert("RGB")
    if caixa:
        f = f.crop(caixa)
    f = f.resize((largura, round(f.height * largura / f.width)), Image.LANCZOS)
    b = io.BytesIO()
    f.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


BASE = """<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{margin:0;padding:0;box-sizing:border-box}
.c{width:1080px;height:1440px;position:relative;overflow:hidden;background:PAPEL;color:CAFE;font-family:Inter,sans-serif;font-variant-numeric:lining-nums;font-kerning:normal;isolation:isolate}
.c.esc{background:FUNDO;color:PAPEL}
.abs{position:absolute}
.cab{position:absolute;left:96px;right:96px;top:72px}
.ox1{height:4px;background:OURO}.ox2{height:2px;background:OURO;margin-top:4px}
.lin{display:flex;justify-content:space-between;align-items:baseline;font:500 24px Inter;margin-top:20px}
.lin span:first-child{font-weight:600;letter-spacing:.12em;text-transform:uppercase}
.g{font-family:'EB Garamond',serif;font-weight:500;letter-spacing:-.015em}
.g i{font-weight:400}
.corpo{font:400 36px/1.34 Inter}
.peq{font:500 24px/1.4 Inter}
.ass{position:absolute;left:96px;bottom:96px;display:flex;align-items:center;gap:16px;font:500 24px Inter}
.ass img{width:52px;height:52px}
.m{background:linear-gradient(OURO,OURO) 0 58%/100% 78% no-repeat;padding:0 .2em;margin-left:-.2em;color:CAFE;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.r{text-decoration:line-through OURO .055em}
CSS</style></head><body><div class="c CLASSE">CORPO</div>
<script>document.fonts.ready.then(()=>{document.body.dataset.ok=1})</script></body></html>""".replace("PAPEL", PAPEL).replace("OURO", OURO).replace("CAFE", CAFE).replace("FUNDO", FUNDO)


def cab(a, b="Letícia Barros · OAB/ES 39.948"):
    return f'<div class=cab><div class=ox1></div><div class=ox2></div><div class=lin><span>{a}</span><span>{b}</span></div></div>'


ASS = f'<div class=ass><img src="{LOGO}">Letícia Barros &nbsp;·&nbsp; OAB/ES 39.948</div>'
P = {}

# 1. A lei em forma de barriga: o texto do artigo desenha o perfil de uma gestante.
def perfil():
    pts, cont = [], []
    for y in range(0, 961, 20):
        t = y / 960
        barriga = 372 * math.exp(-((t - .58) / .25) ** 2)
        peito = 46 * math.exp(-((t - .14) / .09) ** 2)
        x = 470 + barriga + peito
        pts.append(f"{x:.0f}px {y}px")
        cont.append(f"{x + 96 + 18:.0f},{y + 262}")
    return "polygon(" + ",".join(pts) + ",888px 960px,888px 0px)", " ".join(cont)


FORMA, CONTORNO = perfil()
P["01-lei-barriga"] = (f""".z{{float:right;width:888px;height:960px;shape-outside:{FORMA}}}""",
 f"""{cab('Está na CLT', 'Art. 391')}
<div class="abs g" style="left:96px;top:166px;font-size:74px;line-height:1">Grávida? <i>Leia.</i></div>
<div class="abs g" style="left:96px;top:262px;width:888px;height:960px;font-size:55px;line-height:1.17;text-align:justify;hyphens:auto;letter-spacing:0"><div class=z></div>Art. 391. Não constitui justo motivo para a rescisão do contrato de trabalho da mulher o fato de haver contraído matrimônio ou de encontrar-se em estado de <span class=m>gravidez.</span> Parágrafo único. Não serão permitidos em regulamentos de qualquer natureza contratos coletivos ou individuais de trabalho, restrições ao direito da mulher ao seu emprego, por motivo de casamento ou de gravidez.</div>
<svg class=abs style="left:0;top:0" width=1080 height=1440><polyline points="{CONTORNO}" fill=none stroke="{OURO}" stroke-width=3 stroke-linecap=round /></svg>
{ASS}""", "")

# 2. Verbete de dicionário: o nome com a definição que queremos fixar.
P["02-verbete"] = ("", f"""{cab('Dicionário', 'L')}
<div class="abs g" style="left:96px;top:176px;font-size:128px;line-height:1">Letícia Barros</div>
<div class="abs g" style="left:96px;top:318px;font-size:42px;line-height:1.2;letter-spacing:0"><i>le.tí.ci.a bar.ros · substantivo próprio, feminino</i></div>
<div class=abs style="left:96px;right:96px;top:396px;height:2px;background:{OURO}"></div>
<div class=abs style="left:96px;width:500px;top:444px">
<div class=g style="font-size:80px;line-height:1.08"><span style="font-size:36px;vertical-align:.5em;margin-right:8px">1.</span>A advogada da mulher que trabalha.</div>
<div class=corpo style="margin-top:56px;font-size:32px"><b style="font-weight:600">2.</b> Atua em direito do trabalho, direito das gestantes e das famílias.</div>
<div class=g style="margin-top:56px;font-size:42px;line-height:1.2;letter-spacing:0"><i>Ex.: “Foi a Letícia Barros que explicou o art. 391.”</i></div></div>
<div class=abs style="left:640px;right:96px;top:452px"><img src="{foto('estudio-claro-cadeira.jpg',(250,240,850,1140),560)}" style="width:344px;display:block"><div class=peq style="margin-top:14px">Fig. 1. Em atividade.</div></div>
{ASS}""", "")

# 3. Teste de gravidez: duas linhas douradas, e a estabilidade começa.
P["03-positivo"] = ("", f"""{cab('Gestante', 'ADCT, art. 10')}
<div class="abs g" style="left:96px;top:170px;font-size:156px;line-height:1.02">Deu <i>positivo.</i></div>
<div class=abs style="left:-90px;top:470px;width:1320px;height:230px;transform:rotate(-9deg);background:{PAPEL};border-radius:115px;box-shadow:0 2px 4px rgb(0 0 0/.4),0 26px 50px rgb(0 0 0/.42)">
<div class=abs style="left:420px;top:64px;width:330px;height:102px;background:#D8CDBC;border-radius:51px;box-shadow:inset 0 3px 7px rgb(30 24 20/.3)">
<div class=abs style="left:112px;top:12px;width:14px;height:78px;background:{OURO}"></div><div class=abs style="left:204px;top:12px;width:14px;height:78px;background:{OURO}"></div></div>
<div class=abs style="left:850px;top:82px;width:66px;height:66px;background:#D8CDBC;border-radius:50%;box-shadow:inset 0 3px 7px rgb(30 24 20/.3)"></div></div>
<div class="abs g" style="left:96px;right:96px;top:850px;font-size:100px;line-height:1.08;color:{OURO}"><i>A estabilidade também.</i></div>
<div class="abs corpo" style="left:96px;width:800px;top:1088px">Vale da confirmação da gravidez até 5 meses após o parto.</div>
<div class="abs peq" style="left:96px;top:1212px">ADCT, art. 10, II, b. Cada caso precisa ser avaliado.</div>
{ASS}""", "esc")

# 4. Errata de jornal: a internet erra e a coluna corrige.
P["04-errata"] = ("", f"""{cab('Correção', 'Lei 4.090/62, art. 3º')}
<div class="abs g" style="left:92px;top:166px;font-size:212px;line-height:1">Errata</div>
<div class=abs style="left:96px;right:96px;top:402px;height:2px;background:{OURO}"></div>
<div class="abs peq" style="left:96px;top:452px;font-weight:600">Onde se lê:</div>
<div class="abs g" style="left:96px;top:496px;font-size:104px;line-height:1.14"><span class=r>Foi demitido,</span><br><span class=r>perdeu o 13º.</span></div>
<div class="abs peq" style="left:96px;top:806px;font-weight:600">Leia-se:</div>
<div class="abs g" style="left:96px;right:96px;top:850px;font-size:74px;line-height:1.3;white-space:nowrap"><i>Na dispensa sem justa causa,</i><br><span class=m>o 13º proporcional é devido.</span></div>
<div class="abs corpo" style="left:96px;top:1100px;font-size:30px">A internet pede desculpas aos leitores pelo engano.</div>
{ASS}""", "")

# 5. O grito ocupa a peça; a palavra certa fica pequena.
P["05-grito"] = ("", f"""<div class="abs g" style="left:72px;top:1344px;width:1290px;font-size:322px;line-height:1;white-space:nowrap;color:{OURO};transform-origin:0 0;transform:rotate(-90deg);letter-spacing:.015em">GRITAR</div>
<div class=abs style="left:520px;right:96px;top:720px">
<div class=g style="font-size:132px;line-height:1.04">não é<br><i>cobrar.</i></div>
<div class=corpo style="margin-top:56px">Humilhação repetida no trabalho pode ser assédio moral.</div></div>
<div class=abs style="left:520px;right:96px;top:96px;display:flex;flex-direction:column;gap:14px;font:600 24px Inter;letter-spacing:.12em"><span>ASSÉDIO MORAL</span><span style="letter-spacing:0;font-weight:500">Letícia Barros<br>OAB/ES 39.948</span></div>""", "esc")

# 6. Recibo: o favor do patrão não consta.
DENTE = ",".join(f"{i * 3.333:.2f}% {100 if i % 2 else 98.4}%" for i in range(30, -1, -1))
P["06-recibo"] = (f""".rc{{position:absolute;left:150px;top:-10px;width:780px;height:1150px;background:{PAPEL};color:{CAFE};padding:110px 60px 0;transform:rotate(1.4deg);clip-path:polygon(0 0,100% 0,{DENTE})}}
.sb{{position:absolute;left:150px;top:-10px;width:780px;height:1150px;transform:rotate(1.4deg);filter:blur(30px);background:#000;opacity:.42}}
.li{{display:flex;justify-content:space-between;align-items:baseline;font:500 32px Inter;padding:20px 0;border-bottom:2px dashed #B9AD9B}}""",
 f"""<div class=sb></div><div class=rc>
<div style="font:600 24px Inter;letter-spacing:.12em;text-align:center">RECIBO · 13º SALÁRIO</div>
<div class=g style="font-size:108px;line-height:1.02;margin-top:48px">O 13º não é <i>favor.</i></div>
<div style="margin-top:52px;border-top:2px dashed #B9AD9B">
<div class=li><span>1ª parcela</span><span>até 30/11</span></div>
<div class=li><span>2ª parcela</span><span>até 18/12</span></div>
<div class=li><span>Base</span><span>Leis 4.090 e 4.749</span></div>
<div class=li style="font-weight:600;border-bottom:0"><span class=m>Favor do patrão</span><span class=m>não consta</span></div></div>
<div class=peq style="margin-top:44px;text-align:center">Em 2026, o dia 20/12 cai num domingo.</div>
<div style="display:flex;gap:5px;justify-content:center;margin-top:44px;height:64px">{"".join(f'<i style="display:block;width:{w}px;background:{CAFE}"></i><i style="display:block;width:{g}px"></i>' for w, g in [(4,3),(9,4),(3,6),(6,3),(12,4),(3,3),(7,6),(4,3),(10,3),(3,5),(8,3),(4,4),(11,3),(3,7),(6,3),(9,4),(3,3),(5,5)])}</div></div>
<div class=ass style="color:{PAPEL};left:150px"><img src="{LOGO}">Letícia Barros &nbsp;·&nbsp; OAB/ES 39.948</div>""", "esc")

# 7. Conversa: o "rapidinho" e um áudio que ocupa a peça.
random.seed(7)
ONDA = "".join(f'<i style="display:block;width:7px;height:{random.randint(14, 92)}px;background:{CAFE};border-radius:4px"></i>' for _ in range(40))
P["07-audio"] = (f""".b{{position:absolute;background:{PAPEL};color:{CAFE};border-radius:30px}}""",
 f"""{cab('Na vida real')}
<div class="b g" style="left:96px;top:190px;padding:30px 48px 40px;font-size:112px;line-height:1.04;border-bottom-left-radius:6px">“Doutora,<br><i>é rapidinho.”</i></div>
<div class=b style="left:96px;right:96px;top:540px;padding:34px 40px 26px;border-top-left-radius:6px">
<div style="display:flex;align-items:center;gap:26px"><div style="flex:none;width:84px;height:84px;border-radius:50%;background:{CAFE};position:relative"><span style="position:absolute;left:32px;top:24px;border-left:28px solid {PAPEL};border-top:18px solid transparent;border-bottom:18px solid transparent"></span></div>
<div style="flex:1;display:flex;align-items:center;justify-content:space-between;height:104px">{ONDA}</div></div>
<div style="display:flex;justify-content:space-between;font:500 26px Inter;margin-top:14px"><span>0:00</span><span>4:00</span></div></div>
<div class="abs g" style="left:96px;top:856px;font-size:92px;line-height:1.1;color:{OURO}"><i>O áudio tinha<br>4 minutos.</i></div>
<div class=abs style="left:96px;right:96px;top:1120px;display:flex;align-items:center;justify-content:flex-end;gap:22px">
<div style="background:{OURO};color:{CAFE};font:500 36px Inter;padding:24px 36px;border-radius:30px;border-bottom-right-radius:6px">Ouvi até o fim.</div>
<img src="{foto('lendo-documentos.jpg',(330,10,1020,700),220)}" style="width:110px;height:110px;border-radius:50%;object-fit:cover"></div>
{ASS}""", "esc")

# 8. O papel que ela não assina.
P["08-nao-assino"] = ("", f"""{cab('Termo de promessa', 'Cláusula única')}
<div class=abs style="left:96px;width:520px;top:186px">
<div class=peq style="font-weight:600">A advogada declara:</div>
<div class=g style="font-size:112px;line-height:1.04;margin-top:28px">“Prometo que você vai <i>ganhar.”</i></div></div>
<img class=abs src="{foto('janela-cafe.jpg',(120,130,920,1100),640)}" style="left:656px;right:0;top:186px;width:424px;height:540px;object-fit:cover">
<div class=abs style="left:96px;right:96px;top:870px;height:2px;background:{CAFE}"></div>
<div class="abs g" style="left:96px;top:800px;font-size:64px;line-height:1">✕</div>
<div class="abs peq" style="left:96px;top:888px">Assinatura</div>
<div class="abs g" style="left:96px;right:96px;top:960px;font-size:88px;line-height:1.08;white-space:nowrap"><span class=m><i>Este papel eu não assino.</i></span></div>
<div class="abs corpo" style="left:96px;top:1090px;font-size:32px">Advocacia informa o caminho, não garante o resultado.</div>
{ASS}""", "")

# 9. Os 120 dias, um a um.
PONTOS = "".join(f'<i style="display:block;width:40px;height:40px;border-radius:50%;background:{OURO}"></i>' for _ in range(120))
P["09-120-dias"] = ("", f"""{cab('Licença-maternidade', 'CLT, art. 392')}
<div class="abs g" style="left:96px;top:170px;font-size:190px;line-height:1">120 <i>dias.</i></div>
<div class=abs style="left:96px;right:96px;top:420px;display:grid;grid-template-columns:repeat(15,40px);justify-content:space-between;row-gap:20px">{PONTOS}</div>
<div class="abs g" style="left:96px;right:96px;top:930px;font-size:88px;line-height:1.1;color:{PAPEL}">Todos sem prejuízo <i style="color:{OURO}">do emprego e do salário.</i></div>
<div class="abs peq" style="left:96px;top:1230px">Licença-maternidade de 120 dias, como manda a lei.</div>
{ASS}""", "esc")

# 10. Tela de celular às 23h47.
def aviso(t, msg, x=96, w=888):
    return f'<div style="margin-left:{x - 96}px;width:{w}px;background:{PAPEL};color:{CAFE};border-radius:30px;padding:24px 34px 28px;margin-bottom:18px;box-shadow:0 12px 30px rgb(0 0 0/.3)"><div style="display:flex;justify-content:space-between;font:600 26px Inter"><span>Chefe</span><span style="font-weight:500">{t}</span></div><div style="font:400 36px/1.3 Inter;margin-top:8px">{msg}</div></div>'


P["10-23h47"] = ("", f"""<div class="abs peq" style="left:0;right:0;top:92px;text-align:center;font-size:30px">terça-feira</div>
<div class="abs g" style="left:0;right:0;top:128px;text-align:center;font-size:270px;line-height:1;font-weight:400;letter-spacing:-.02em">23:47</div>
<div class=abs style="left:96px;right:96px;top:440px">
{aviso('agora', 'Viu o que te mandei?')}{aviso('há 4 min', 'Preciso disso para amanhã cedo.')}{aviso('há 9 min', 'Oi??')}</div>
<div class="abs g" style="left:96px;right:96px;top:964px;font-size:112px;line-height:1.08"><span class=m><i>Quem está errado?</i></span></div>
<div class="abs corpo" style="left:96px;width:860px;top:1120px;font-size:32px">Ela respondeu às 8h. Comente o que você acha. Cada caso precisa ser avaliado.</div>
{ASS}""", "esc")

AUDITA = """()=>{const f=new Set(),p=[],o=[];const W=document.createTreeWalker(document.querySelector('.c'),NodeFilter.SHOW_TEXT);let n;
while(n=W.nextNode()){if(!n.textContent.trim())continue;const s=getComputedStyle(n.parentElement),z=parseFloat(s.fontSize);f.add(z);if(z<22)p.push(n.textContent.trim().slice(0,20));
const r=document.createRange();r.selectNodeContents(n);const b=r.getBoundingClientRect();if(b.left<60||b.right>1020||b.top<20||b.bottom>1400)o.push(n.textContent.trim().slice(0,22)+' '+[b.left,b.right,b.top,b.bottom].map(Math.round));}
return {fontes:[...f].sort((a,b)=>b-a),pequenos:p,fora:o}}"""


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
        for nome, (css, corpo, classe) in P.items():
            if so and not any(nome.startswith(s) for s in so):
                continue
            html = BASE.replace("CSS</style>", css + "</style>").replace("CORPO", corpo).replace("CLASSE", classe)
            await pg.set_content(html, wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            print(nome, json.dumps(await pg.evaluate(AUDITA), ensure_ascii=False))
            s = SAIDA / f"{nome}.jpg"
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(s, quality=91)
        await b.close()
    arqs = sorted(SAIDA.glob("*.jpg"))
    folha = Image.new("RGB", (5 * 400, 2 * 533), "white")
    for i, a in enumerate(arqs[:10]):
        folha.paste(Image.open(a).resize((396, 528), Image.LANCZOS), ((i % 5) * 400 + 2, (i // 5) * 533 + 2))
    folha.save(AQUI / "conferencia.jpg", quality=88)


asyncio.run(main())
