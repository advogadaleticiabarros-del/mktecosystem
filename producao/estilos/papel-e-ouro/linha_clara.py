"""Viraliza Claro v2: mesmos formatos, assuntos e cores; disposição, espaçamento, alinhamento e peso refinados.
Só prévia: não toca em peça, banco ou agenda. A v1 continua em pecas/."""
import asyncio
import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter
from playwright.async_api import async_playwright

API = Path(__file__).resolve().parents[3] / "apps" / "api"
AQUI = Path(__file__).resolve().parent
RET = API / "_saida_producao_1510/_retratos"
ACAB = next((API / "app/assets").glob("*dourad*"))
SAIDA = AQUI / "pecas-v2"
PAPEL = "#E8DFD2"  # média do papel renderizado na v1, para a cor não mudar
OURO = "#C9A962"
CAFE = "#1E1814"


def data(im, q=93):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def com_parede(nome, largura, acima):
    """Dá respiro acima da cabeça estendendo só a parede; a pessoa fica intacta."""
    f = Image.open(RET / nome).convert("RGB")
    f = f.resize((largura, round(f.height * largura / f.width)), Image.LANCZOS)
    tela = f.crop((0, 0, largura, 24)).resize((largura, acima + 80)).filter(ImageFilter.GaussianBlur(30))
    saida = Image.new("RGB", (largura, f.height + acima))
    saida.paste(tela, (0, 0))
    mascara = Image.new("L", f.size, 255)
    for y in range(80):
        mascara.paste(int(255 * y / 80), (0, y, largura, y + 1))
    saida.paste(f, (0, acima), mascara)
    return saida


def foto(nome, largura):
    f = Image.open(RET / nome).convert("RGB")
    return f.resize((largura, round(f.height * largura / f.width)), Image.LANCZOS)


LOGO = "data:image/png;base64," + base64.b64encode((API / "app/assets/logo-leticia.png").read_bytes()).decode()
RUIDO = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='600'%3E%3Cfilter id='n'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix values='0 0 0 0 .35 0 0 0 0 .28 0 0 0 0 .2 0 0 0 .55 0'/%3E%3C/filter%3E"
         "%3Crect width='600' height='600' filter='url(%23n)'/%3E%3C/svg%3E")

BASE = """<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{margin:0;padding:0;box-sizing:border-box}
:root{--m:96px}
.c{width:1080px;height:1440px;position:relative;overflow:hidden;background:PAPEL;color:CAFE;font-family:Inter,sans-serif;font-variant-numeric:lining-nums;font-kerning:normal;isolation:isolate}
.grao{position:absolute;inset:0;background:url("RUIDO");mix-blend-mode:multiply;opacity:.05}
.cab{position:absolute;left:var(--m);right:var(--m);top:72px}
.ox1{height:4px;background:OURO}.ox2{height:2px;background:OURO;margin-top:4px}
.lin{display:flex;justify-content:space-between;align-items:baseline;font:500 24px Inter;margin-top:20px}
.lin span:first-child{font-weight:600;letter-spacing:.12em;text-transform:uppercase}
.col{position:absolute;left:var(--m);right:var(--m);top:176px;bottom:96px;display:flex;flex-direction:column}
.g{font-family:'EB Garamond',serif;font-weight:500;letter-spacing:-.015em}
.g i{font-weight:400}
.l{display:block;width:max-content;white-space:nowrap}
.corpo{font:400 36px/1.34 Inter}
.peq{font:500 24px/1.4 Inter}
.lei{font-family:'EB Garamond',serif;font-weight:500;font-size:52px;line-height:1.3}
.ass{margin-top:auto;display:flex;align-items:center;gap:16px;font:500 24px Inter}
.ass img{width:52px;height:52px;margin-left:-2px}
.m{background:linear-gradient(OURO,OURO) 0 58%/100% 78% no-repeat;padding:0 .2em;margin-left:-.2em;white-space:nowrap}
.s{text-decoration:underline OURO .05em;text-underline-offset:.14em;text-decoration-skip-ink:auto}
.r{text-decoration:line-through OURO .055em;text-decoration-skip-ink:none}
.t{height:20px;background:CAFE;margin-bottom:18px}
.ti{display:inline-block;height:.68em;background:CAFE;vertical-align:-.08em}
.pl{display:grid;grid-template-columns:1fr 1fr;border-top:2px solid OURO;border-bottom:2px solid OURO}
.pl>div{padding:28px 32px 32px 0}
.pl>div+div{padding-left:32px;padding-right:0;border-left:2px solid OURO}
.cap::first-letter{initial-letter:3;margin-right:14px;font-weight:500}
.fp{position:absolute;background-repeat:no-repeat}
CSS</style></head><body><div class=c><div class=grao></div>CORPO</div>
<script>
// Alinhamento óptico: a tinta da letra encosta na margem; aspas ficam penduradas fora dela.
document.fonts.ready.then(()=>{const cx=document.createElement('canvas').getContext('2d');
document.querySelectorAll('.l').forEach(l=>{const w=document.createTreeWalker(l,NodeFilter.SHOW_TEXT);const n=w.nextNode();if(!n)return;
const st=getComputedStyle(n.parentElement);cx.font=`${st.fontStyle} ${st.fontWeight} ${st.fontSize} ${st.fontFamily}`;
let t=n.textContent,d=0;if(t[0]==='“'){d=cx.measureText('“').width;t=t.slice(1)}
const cauda=st.fontStyle==='italic'&&'pfj'.includes(t[0]);const b=cauda?0:cx.measureText(t[0]).actualBoundingBoxLeft;l.style.transform=`translateX(${b-d}px)`;});document.body.dataset.ok=1;});
</script></body></html>""".replace("RUIDO", RUIDO).replace("PAPEL", PAPEL).replace("OURO", OURO).replace("CAFE", CAFE)


def cab(chapeu, direita="Letícia Barros · OAB/ES 39.948"):
    return f'<div class=cab><div class=ox1></div><div class=ox2></div><div class=lin><span>{chapeu}</span><span>{direita}</span></div></div>'


def tarjas(*ws):
    return "".join(f'<div class=t style="width:{w}%"></div>' for w in ws)


def l(*linhas):
    return "".join(f"<span class=l>{x}</span>" for x in linhas)


ASS = f'<div class=ass><img src="{LOGO}">Letícia Barros &nbsp;·&nbsp; OAB/ES 39.948</div>'

P = {}
P["01-lei-tarjada"] = ("", f"""{cab('Está na CLT', 'Art. 391')}<div class=col>
<div class=g style="font-size:124px;line-height:1.04">{l('Grávida?', '<i>Leia esta linha.</i>')}</div>
<div style="margin-top:80px">{tarjas(100,92,96,58)}</div>
<div class=lei style="margin:20px 0 38px">Art. 391. Não constitui justo motivo para a rescisão do contrato de trabalho da mulher o fato de <span class=ti style="width:230px"></span> ou de <span class=m>encontrar-se em estado de gravidez.</span></div>
<div>{tarjas(88,62)}</div>{ASS}</div>""")

P["02-capa-nome"] = (lambda: f""".foto{{position:absolute;inset:0;background:url({data(com_parede('estudio-claro-cadeira.jpg',1080,300).crop((0,0,1080,1440)))}) 0 0/1080px 1440px no-repeat}}""",
 f"""<div class=foto></div>{cab('Quem é', 'OAB/ES 39.948')}<div class=col>
<div class=g style="font-size:136px;line-height:1">{l('Letícia Barros')}</div>
<div class=g style="font-size:50px;line-height:1.2;margin-top:18px">{l('<i>a advogada da mulher que trabalha</i>')}</div></div>""")

P["03-cinco-meses"] = ("", f"""{cab('Gestante', 'ADCT, art. 10')}<div class=col>
<div style="display:flex;align-items:last baseline;gap:56px;margin-top:56px">
<div class=g style="font-size:760px;line-height:.78">{l('5')}</div>
<div class=g style="font-size:104px;line-height:1.08">{l('meses', '<i>depois</i>', '<i class=s>do parto.</i>')}</div></div>
<div class=corpo style="margin-top:104px;max-width:820px">A estabilidade da gestante vai da confirmação da gravidez até 5 meses após o parto.</div>
<div class=peq style="margin-top:24px">ADCT, art. 10, II, b. Cada caso precisa ser avaliado.</div>{ASS}</div>""")

P["04-mito-13"] = ("", f"""{cab('Mito', 'Lei 4.090/62, art. 3º')}<div class=col>
<div class=g style="font-size:270px;line-height:1">{l('<i>Mito.</i>')}</div>
<div class=g style="font-size:116px;line-height:1.16;margin-top:64px">{l('<span class=r>Foi demitido,</span>', '<span class=r>perdeu o 13º.</span>')}</div>
<div class=corpo style="margin-top:112px;line-height:1.6">Na dispensa sem justa causa,<br><span class=m>o 13º proporcional é devido.</span></div>{ASS}</div>""")

P["05-gritar"] = ("", f"""{cab('Assédio moral')}<div class=col>
<div class=g style="font-size:232px;line-height:1.02;margin-top:32px">{l('Gritar', 'não é', '<i class=s>cobrar.</i>')}</div>
<div class=corpo style="margin-top:72px;max-width:640px">Humilhação repetida no trabalho pode ser assédio moral.</div>{ASS}</div>""")

JANELA = "".join(
    f'<div style="position:absolute;left:{x}px;top:{y}px;width:330px;height:430px;background:#7A6650"></div>'
    for x in (0, 370) for y in (0, 470))
P["06-13-nao-e-favor"] = ("", f"""<div style="position:absolute;left:400px;top:-60px;width:700px;height:900px;transform:rotate(14deg) skewX(-16deg);filter:blur(22px);mix-blend-mode:multiply;opacity:.24">{JANELA}</div>
{cab('13º salário', 'Prazos de 2026')}<div class=col>
<div class=g style="font-size:196px;line-height:1.04;margin-top:16px">{l('O 13º', 'não é', '<i class=s>favor.</i>')}</div>
<div class=pl style="margin-top:auto">
<div><div class=peq>1ª parcela</div><div class=g style="font-size:76px;line-height:1.15;margin-top:8px">até 30/11</div></div>
<div><div class=peq>2ª parcela</div><div class=g style="font-size:76px;line-height:1.15;margin-top:8px">até 18/12</div></div></div>
<div class=peq style="margin-top:24px">Leis 4.090/62 e 4.749/65. Em 2026, o dia 20/12 cai num domingo.</div>
<div class=ass style="margin-top:64px">{ASS[len('<div class=ass>'):]}</div>""")

P["07-rapidinho"] = (lambda: f""".foto{{flex:1;margin-top:48px;background-image:url({data(com_parede('lendo-documentos.jpg',888,84))});background-size:888px auto;background-position:0 0;background-repeat:no-repeat}}""",
 f"""{cab('Na vida real')}<div class=col>
<div class=g style="font-size:116px;line-height:1.04">{l('“Doutora,', '<i>é rapidinho.”</i>')}</div>
<div class=foto></div>
<div style="font:500 36px/1.3 Inter;margin-top:32px"><span class=m>O áudio tinha 4 minutos.</span></div></div>""")

P["08-nunca-prometo"] = (lambda: f""".foto{{position:absolute;left:0;right:0;top:0;height:736px;background-image:url({data(foto('janela-cafe.jpg',1080))});background-size:1080px auto;background-position:0 -128px;background-repeat:no-repeat}}""",
 f"""<div class=foto></div><div class=col style="top:792px">
<div class=g style="font-size:92px;line-height:1.1">{l('Por que eu nunca vou', 'te <i class=s>prometer</i> que você', 'vai ganhar.')}</div>
<div class=corpo style="margin-top:28px;font-size:30px">Advocacia informa o caminho, não garante o resultado.</div>{ASS}</div>""")

P["09-lei-comentada"] = ("", f"""{cab('Licença-maternidade', 'CLT, art. 392')}<div class=col>
<div class=g style="font-size:148px;line-height:1.06">{l('Sem', '<i>prejuízo.</i>')}</div>
<div style="display:grid;grid-template-columns:1fr 244px;gap:40px;margin-top:80px;align-items:start">
<div class="lei cap" style="font-size:50px">A empregada gestante<br>tem direito à<br>licença-maternidade<br>de 120 (cento e vinte) dias,<br>sem prejuízo<br><span class=m>do emprego e do salário.</span></div>
<div style="border-left:2px solid {OURO};padding-left:24px;font:400 24px/1.45 Inter;margin-top:8px"><div style="font-weight:600;margin-bottom:10px">Na prática</div>Durante os 120 dias, o emprego e o salário seguem garantidos.</div></div>{ASS}</div>""")

P["10-quem-errou"] = ("", f"""{cab('Situação')}<div class=col>
<div class=g style="font-size:112px;line-height:1.08">{l('Mensagem do', 'chefe às <i>23h.</i>')}</div>
<div class=pl style="margin-top:88px">
<div><div class=peq style="font-weight:600">A funcionária</div><div class=g style="font-size:50px;line-height:1.16;margin-top:14px;letter-spacing:0">Viu e só respondeu às 8h.</div></div>
<div><div class=peq style="font-weight:600">O chefe</div><div class=g style="font-size:50px;line-height:1.16;margin-top:14px;letter-spacing:0">Cobrou resposta na mesma noite.</div></div></div>
<div class=g style="font-size:112px;line-height:1.1;margin-top:112px"><i class=m>Quem está errado?</i></div>
<div class=peq style="margin-top:28px">Comente o que você acha. Cada caso precisa ser avaliado.</div>{ASS}</div>""")

AUDITA = """()=>{const out={fontes:new Set(),pequenos:[],fora:[]};const W=document.createTreeWalker(document.querySelector('.c'),NodeFilter.SHOW_TEXT);
let n;while(n=W.nextNode()){if(!n.textContent.trim())continue;const e=n.parentElement,s=getComputedStyle(e),z=parseFloat(s.fontSize);out.fontes.add(z);
if(z<22)out.pequenos.push(n.textContent.trim().slice(0,20));
const r=document.createRange();r.selectNodeContents(n);const b=r.getBoundingClientRect();
if(b.right>1080-88||b.left<60||b.bottom>1440-88)out.fora.push(n.textContent.trim().slice(0,24)+' '+[b.left,b.right,b.bottom].map(Math.round));}
const col=document.querySelector('.col');const a=col&&col.lastElementChild;
return {fontes:[...out.fontes].sort((x,y)=>y-x),pequenos:out.pequenos,fora:out.fora,estouro:col?col.scrollHeight>col.clientHeight+1:false}}"""


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
        for nome, (css, corpo) in P.items():
            if so and not any(nome.startswith(s) for s in so):
                continue
            css = css() if callable(css) else css
            await pg.set_content(BASE.replace("/*X*/", "").replace("CSS</style>", css + "</style>").replace("CORPO", corpo), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            print(nome, json.dumps(await pg.evaluate(AUDITA), ensure_ascii=False))
            s = SAIDA / f"{nome}.png"
            await pg.screenshot(path=str(s), clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(s).convert("RGBA"), ac).convert("RGB").save(s)
        await b.close()
    arqs = sorted(SAIDA.glob("*.png"))
    folha = Image.new("RGB", (5 * 400, 2 * 533), "white")
    for i, a in enumerate(arqs[:10]):
        folha.paste(Image.open(a).resize((396, 528), Image.LANCZOS), ((i % 5) * 400 + 2, (i // 5) * 533 + 2))
    folha.save(AQUI / "conferencia-v2.jpg", quality=90)
    if len(arqs) == 10:
        grade = Image.new("RGB", (3 * 360 + 8, 3 * 480 + 8), "white")
        for i, n in enumerate(["02", "03", "07", "01", "08", "05", "06", "09", "10"]):
            a = next(SAIDA.glob(f"{n}-*.png"))
            grade.paste(Image.open(a).resize((360, 480), Image.LANCZOS), ((i % 3) * 364, (i // 3) * 484))
        grade.save(AQUI / "grade-v2.jpg", quality=90)


asyncio.run(main())
