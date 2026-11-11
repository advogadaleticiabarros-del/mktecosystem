"""Carrossel V2 (panorama contínuo com dourado metálico) como MODELO para qualquer tema (11/11/2026: a Jessica escolheu
o V2 para os carrosséis: "quero o formato V2 que fizemos juntos").

Mesmo desenho do V2 aprovado (gerar.py + gerar_v2.py + gerar_v2_brilho.py, exemplo "Mãe por adoção"): 7 páginas de
1080×1440 renderizadas como um panorama e fatiadas, com pontes entre as divisas (diagonal café 2|3 e 5|6, foto vazando
3|4, arcos dourados 4|5, palavra em pé na divisa 6|7) e todo o ouro em degradê metálico com brilho.

Entrada: os dados do carrossel no formato v5 (capa, itens, checklist, fecho, tag) + fotos + uma palavra curta.
  1 capa: foto do tema, título serif com itálico dourado       2 item 1: papel, barra lateral, palavra-fantasma
  3 item 2: café com moldura de cantos                           4 item 3: papel, foto em cartão vazando para a 3
  5 item 4: papel centralizado sobre os arcos                    6 item 5 + checklist: café, palavra em pé na divisa
  7 fechamento: retrato real da Dra.

Uso: from v2_modelo import renderizar; await renderizar(page, dados, fotos, palavra, destino_prefixo)
"""
import base64
import io
import re
from pathlib import Path

from PIL import Image

W, H, N = 1080, 1440, 7
METAL = "linear-gradient(100deg,#7d5f24 0%,#c9a962 18%,#fff3c8 34%,#e2c172 48%,#9c7a34 64%,#f2dc9a 82%,#a8843c 100%)"
GLOW = "0 0 22px rgba(255,214,130,.75),0 0 6px rgba(255,236,180,.9)"
METAL_TXT = "linear-gradient(100deg,#d9b866 0%,#fff3c8 30%,#e8c978 55%,#fff0bd 80%,#d4b064 100%)"
TXT_GLOW = "drop-shadow(0 0 10px rgba(255,210,120,.55))"
FAIXA = ("height:24px;background:linear-gradient(180deg,#7d5f24 0%,#d9b866 22%,#fff8dc 46%,#fffbe8 52%,#e8c978 70%,#8a6a2a 100%);"
         "box-shadow:0 0 30px 8px rgba(255,214,130,.85),0 0 70px 14px rgba(255,200,100,.35)")
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500;1,600'
          '&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">')

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{position:relative;width:{W * N}px;height:{H}px;overflow:hidden;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
.s{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.cafe{{background:#231E1A;color:#E8DED1}}
.papel{{background:#F7F1E7;color:#231E1A}}
.s::before,.s::after{{content:"";position:absolute;left:0;right:0;z-index:20;{FAIXA}}}
.s::before{{top:0}}.s::after{{bottom:0}}
.cab{{position:absolute;top:56px;left:80px;right:80px;display:flex;justify-content:space-between;z-index:10;
  font-size:22px;font-weight:600;letter-spacing:3px;text-transform:uppercase;opacity:.85}}
.serif{{font-family:'EB Garamond',serif}}
em{{font-style:italic}}
.cafe em{{background:{METAL_TXT};-webkit-background-clip:text;background-clip:text;color:transparent;filter:{TXT_GLOW}}}
.papel em{{background:{METAL} no-repeat left bottom/100% 7px;padding-bottom:6px}}
.ouro{{background:{METAL_TXT};-webkit-background-clip:text;background-clip:text;color:transparent;filter:{TXT_GLOW}}}
.selo{{display:inline-block;font-size:22px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  background:{METAL};color:#231E1A;padding:10px 18px;border-radius:4px;box-shadow:{GLOW}}}
.txt{{font-size:34px;line-height:1.45}}
.txt b,.txt .mt{{font-weight:700}}
.cafe .txt b,.cafe .txt .mt{{color:#E6CF94}}
.seta{{position:absolute;right:80px;bottom:64px;z-index:10;width:64px;height:64px;border-radius:50%;
  border:2px solid #f2dc9a;box-shadow:{GLOW};display:flex;align-items:center;justify-content:center;font-size:30px;color:#C9A962}}
"""


def uri(p: Path, w: int = 1600) -> str:
    im = Image.open(p).convert("RGB")
    im.thumbnail((w, w * 2))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def _sem_br(t):
    return re.sub(r"<br\s*/?>", " ", t)


def _selo(lei):
    return f'<div style="margin-top:36px"><span class="selo">{lei}</span></div>' if lei else ""


def slides(d, f, palavra):
    cab = f'<div class="cab"><span>Letícia Barros · Advocacia</span><span>{d.get("area", "")}</span></div>'
    kicker, titulo, sub, apoio, lei = d["capa"]
    it = d["itens"]
    num = lambda n, cor: f'<div class="serif" style="font-size:44px;color:{cor};font-weight:600">{n:02d}</div>'  # noqa: E731
    fecho_t, fecho_s, fecho_a = d["fecho"]
    caixa = "".join(
        f'<div style="display:flex;gap:22px;align-items:flex-start;margin-top:26px;font-size:34px;line-height:1.35">'
        f'<span style="flex:none;width:34px;height:34px;border:3px solid #f2dc9a;box-shadow:{GLOW};border-radius:5px;margin-top:6px"></span>{t}</div>'
        for t in d["checklist"])
    return [
        f"""<div class="s cafe">
  <img src="{f['capa']}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{f.get('capa_pos', 'center 25%')}">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(35,30,26,.55) 0%,rgba(35,30,26,0) 30%,rgba(35,30,26,.25) 48%,#231E1A 80%)"></div>
  {cab}
  <div style="position:absolute;left:80px;right:80px;bottom:130px;z-index:5">
    <div style="font-size:30px;font-weight:600;letter-spacing:4px;text-transform:uppercase"><span class="ouro">{kicker}</span></div>
    <div class="serif" data-max=170 style="font-size:150px;line-height:.95;margin-top:18px"><em>{titulo}</em></div>
    <div class="serif" style="font-size:64px;line-height:1.1;margin-top:14px">{sub}</div>
    <div class="txt" style="margin-top:30px;opacity:.92">{apoio}</div>
    {_selo(lei)}
  </div>
  <div class="seta">→</div></div>""",
        f"""<div class="s papel">{cab}
  <div class="serif" style="position:absolute;left:40px;bottom:40px;font-size:300px;font-style:italic;color:#231E1A;opacity:.06;line-height:1;white-space:nowrap">{palavra.lower()}</div>
  <div style="position:absolute;left:80px;right:90px;top:300px">
    {num(1, '#8F7032')}
    <div style="border-left:6px solid #C9A962;padding-left:36px;margin-top:20px">
      <div class="serif" data-max=330 style="font-size:104px;line-height:1.05">{it[0][0]}</div>
    </div>
    <div class="txt" style="margin-top:56px">{it[0][1]}</div>
    {_selo(it[0][2])}
  </div></div>""",
        f"""<div class="s cafe">{cab}
  <div style="position:absolute;left:110px;right:220px;top:300px;bottom:300px;border:3px solid #f2dc9a;box-shadow:{GLOW}"></div>
  {''.join(f'<div style="position:absolute;width:30px;height:30px;background:{METAL};box-shadow:{GLOW};{p}"></div>' for p in ('left:95px;top:285px', 'right:205px;top:285px', 'left:95px;bottom:285px', 'right:205px;bottom:285px'))}
  <div style="position:absolute;left:180px;right:290px;top:390px">
    {num(2, '#C9A962')}
    <div class="serif" data-max=300 style="font-size:92px;line-height:1.05;margin-top:24px">{_sem_br(it[1][0])}</div>
    <div class="txt" style="margin-top:44px">{it[1][1]}</div>
    {_selo(it[1][2])}
  </div></div>""",
        f"""<div class="s papel" style="overflow:visible;z-index:5">{cab}
  <div style="position:absolute;left:-160px;right:80px;top:140px;height:640px;border-radius:28px;overflow:hidden;box-shadow:0 30px 60px rgba(35,30,26,.25)">
    <img src="{f['foto']}" style="width:100%;height:100%;object-fit:cover;object-position:center 35%;filter:sepia(.1) saturate(.92)">
  </div>
  <div style="position:absolute;left:80px;right:80px;top:850px">
    {num(3, '#8F7032')}
    <div class="serif" data-max=210 style="font-size:88px;line-height:1.05;margin-top:12px">{_sem_br(it[2][0])}</div>
    <div class="txt" style="margin-top:30px">{it[2][1]}</div>
    {_selo(it[2][2])}
  </div></div>""",
        f"""<div class="s papel">{cab}
  <div style="position:absolute;left:90px;right:90px;top:330px;text-align:center">
    {num(4, '#8F7032')}
    <div class="serif" data-max=320 style="font-size:100px;line-height:1.05;margin-top:12px">{_sem_br(it[3][0])}</div>
    <div class="txt" style="margin-top:40px">{it[3][1]}</div>
    {_selo(it[3][2])}
  </div></div>""",
        f"""<div class="s cafe">{cab}
  <div style="position:absolute;left:80px;width:720px;top:240px">
    {num(5, '#C9A962')}
    <div class="serif" data-max=220 style="font-size:88px;line-height:1.05;margin-top:12px">{_sem_br(it[4][0])}</div>
    <div class="txt" style="margin-top:28px">{it[4][1]}</div>
    <div style="margin-top:36px;font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#E6CF94">Separe · salve para conferir</div>
    {caixa}
    {_selo(it[4][2])}
  </div></div>""",
        f"""<div class="s cafe">
  <img src="{f['fecho']}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 25%">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(35,30,26,.5) 0%,rgba(35,30,26,0) 25%,rgba(35,30,26,.15) 45%,#231E1A 76%)"></div>
  {cab}
  <div style="position:absolute;left:200px;right:80px;bottom:110px;z-index:5">
    <div class="serif" data-max=320 style="font-size:96px;line-height:1.02">{fecho_t}</div>
    <div class="serif" style="font-size:52px;margin-top:18px"><em class="ouro">{fecho_s}</em></div>
    <div class="txt" style="margin-top:30px">Salve e <b>{fecho_a}</b> Na dúvida, procure uma advogada.</div>
    <div style="margin-top:30px;padding-top:22px;border-top:1px solid rgba(201,169,98,.5);font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase"><span class="ouro">Letícia Barros · OAB/ES 39.948</span></div>
  </div></div>""",
    ]


def pontes(palavra):
    def diagonal(x):
        return (f'<div style="position:absolute;z-index:15;left:{x - 366}px;top:964px;width:366px;height:476px;background:{METAL};clip-path:polygon(100% 0,100% 100%,0 100%)"></div>'
                f'<div style="position:absolute;z-index:16;left:{x - 340}px;top:1000px;width:340px;height:440px;background:#231E1A;clip-path:polygon(100% 0,100% 100%,0 100%)"></div>')
    tam = 250 if len(palavra) <= 6 else 200 if len(palavra) <= 8 else 160
    return (diagonal(2 * W) + diagonal(5 * W)
            + "".join(f'<div style="position:absolute;z-index:15;left:{4 * W - r}px;top:{H - r}px;width:{2 * r}px;height:{2 * r}px;border:4px solid #f2dc9a;box-shadow:{GLOW};border-radius:50%"></div>' for r in (230, 160))
            + f'''<div class="serif" style="position:absolute;z-index:15;left:{6 * W - 125}px;top:{H // 2 - 125}px;width:250px;height:250px;display:flex;align-items:center;justify-content:center;
      transform:rotate(90deg);font-size:{tam}px;font-weight:600;letter-spacing:10px;white-space:nowrap"><span class="ouro">{palavra.upper()}</span></div>''')


AJUSTA = """<script>document.fonts.ready.then(()=>{document.querySelectorAll('[data-max]').forEach(e=>{
 let s=parseFloat(getComputedStyle(e).fontSize);const m=+e.dataset.max;
 while(e.offsetHeight>m&&s>40){s-=4;e.style.fontSize=s+'px'}});document.body.dataset.ok=1})</script>"""


async def renderizar(page, d, fotos, palavra, prefixo: Path):
    """Gera prefixo-1.jpg … prefixo-7.jpg (1080×1440). Peça pronta nunca é sobrescrita."""
    destinos = [prefixo.with_name(f"{prefixo.name}-{i}.jpg") for i in range(1, N + 1)]
    if all(x.exists() for x in destinos):
        return destinos
    corpo = "".join(f'<div style="position:absolute;top:0;left:{i * W}px">{h}</div>' for i, h in enumerate(slides(d, fotos, palavra)))
    html = f'<!doctype html><html><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{corpo}{pontes(palavra)}{AJUSTA}</body></html>'
    await page.set_content(html, wait_until="networkidle")
    await page.wait_for_selector("body[data-ok]", state="attached")
    pano = Image.open(io.BytesIO(await page.screenshot(type="png", timeout=240000))).convert("RGB")
    for i, x in enumerate(destinos):
        pano.crop((i * W, 0, (i + 1) * W, H)).save(x, "JPEG", quality=90, optimize=True)
    return destinos
