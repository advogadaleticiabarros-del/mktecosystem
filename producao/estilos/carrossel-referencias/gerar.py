"""Carrossel "Mãe por adoção" refeito nos modelos das referências enviadas em 09/11/2026.

Textos e fontes conferidos de apps/api/_saida_producao_1510/carrosseis_v5_dados.py
(chave licenca-adotante). Cores da marca: café, papel, ouro; faixas douradas em todo slide.
Cada slide usa um layout de referência diferente:
1 capa retrato + título serif (ref. "Abogados caros")   2 papel com palavra-fantasma (ref. juros)
3 moldura de cantos (ref. "numerosos relatos")         4 foto em cartão + texto (ref. Revalida)
5 caixas em fluxo (ref. advocacia séria)               6 palavra vertical gigante (ref. "ABOGADOS")
7 fechamento com retrato (ref. "Você não contrata resultado mágico")

Uso: python gerar.py   (saída em ./saida/)
"""
import asyncio
import base64
from pathlib import Path

from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
RETRATOS = RAIZ / "apps/api/_saida_producao_1510/_retratos"
SAIDA = AQUI / "saida"


def uri(p: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1440px;overflow:hidden;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}
.s{position:relative;width:1080px;height:1440px;overflow:hidden}
.cafe{background:#231E1A;color:#E8DED1}
.papel{background:#F7F1E7;color:#231E1A}
.s::before,.s::after{content:"";position:absolute;left:0;right:0;height:14px;z-index:20;
  background:linear-gradient(90deg,#8F7032,#C9A962 30%,#E6CF94 50%,#C9A962 70%,#8F7032)}
.s::before{top:0}.s::after{bottom:0}
.cab{position:absolute;top:56px;left:80px;right:80px;display:flex;justify-content:space-between;z-index:10;
  font-size:22px;font-weight:600;letter-spacing:3px;text-transform:uppercase;opacity:.85}
.serif{font-family:'EB Garamond',serif}
em{font-style:italic}
.cafe em{color:#C9A962}
.papel em{color:#231E1A;text-decoration:underline;text-decoration-color:#C9A962;text-decoration-thickness:5px;text-underline-offset:10px}
.selo{display:inline-block;font-size:22px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  background:#C9A962;color:#231E1A;padding:10px 18px;border-radius:4px}
.txt{font-size:34px;line-height:1.45}
.txt b{font-weight:700}
.cafe .txt b{color:#E6CF94}
.seta{position:absolute;right:80px;bottom:64px;z-index:10;width:64px;height:64px;border-radius:50%;
  border:2px solid #C9A962;display:flex;align-items:center;justify-content:center;font-size:30px;color:#C9A962}
"""

FONTES = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500;1,600'
          '&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">')


def slides(f):
    cab = '<div class="cab"><span>Letícia Barros · Advocacia</span><span>Trabalhista</span></div>'
    return [
        # 1 capa: retrato real, título em serifa com itálico dourado
        f"""<div class="s cafe">
  <img src="{f['capa']}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 20%">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(35,30,26,.55) 0%,rgba(35,30,26,0) 30%,rgba(35,30,26,.2) 50%,#231E1A 80%)"></div>
  {cab}
  <div style="position:absolute;left:80px;right:80px;bottom:130px;z-index:5">
    <div style="font-size:30px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:#E6CF94">Mãe por adoção</div>
    <div class="serif" style="font-size:150px;line-height:.95;margin-top:18px"><em>5 direitos</em></div>
    <div class="serif" style="font-size:64px;line-height:1.1;margin-top:14px">iguais aos da mãe biológica</div>
    <div class="txt" style="margin-top:30px;opacity:.9">O STF fechou em setembro <b>uma diferença antiga</b> entre as mães.</div>
    <div style="margin-top:30px"><span class="selo">STF · ADI 7495</span></div>
  </div>
  <div class="seta">→</div></div>""",

        # 2 papel com barra lateral e palavra-fantasma ao fundo
        f"""<div class="s papel">{cab}
  <div class="serif" style="position:absolute;right:-60px;bottom:120px;font-size:330px;font-style:italic;color:#231E1A;opacity:.06;line-height:1">adoção</div>
  <div style="position:absolute;left:80px;right:90px;top:300px">
    <div class="serif" style="font-size:44px;color:#8F7032;font-weight:600">01</div>
    <div style="border-left:6px solid #C9A962;padding-left:36px;margin-top:20px">
      <div class="serif" style="font-size:112px;line-height:1"><em>120 dias</em>,</div>
      <div class="serif" style="font-size:66px;line-height:1.12;margin-top:16px">qualquer que seja a idade da criança</div>
    </div>
    <div class="txt" style="margin-top:56px">A mãe adotante tem a mesma licença da mãe biológica, <b>de bebê ou de criança maior</b>.</div>
    <div style="margin-top:40px"><span class="selo">CLT, art. 392-A</span></div>
  </div></div>""",

        # 3 café com moldura de cantos quadrados
        f"""<div class="s cafe">{cab}
  <div style="position:absolute;left:110px;right:110px;top:300px;bottom:300px;border:2px solid rgba(201,169,98,.7)"></div>
  {''.join(f'<div style="position:absolute;width:30px;height:30px;background:#C9A962;{p}"></div>' for p in ('left:95px;top:285px','right:95px;top:285px','left:95px;bottom:285px','right:95px;bottom:285px'))}
  <div style="position:absolute;left:180px;right:180px;top:400px">
    <div class="serif" style="font-size:44px;color:#C9A962;font-weight:600">02</div>
    <div class="serif" style="font-size:96px;line-height:1.05;margin-top:24px">Igual em <em>todos</em> os regimes</div>
    <div class="txt" style="margin-top:44px">O STF acabou com prazos menores para <b>servidoras federais e militares</b>.</div>
    <div class="txt" style="margin-top:28px;opacity:.8">CLT, serviço público ou carreira militar: a licença é a mesma.</div>
    <div style="margin-top:44px"><span class="selo">STF · ADI 7495 (23/09/2026)</span></div>
  </div></div>""",

        # 4 papel com foto em cartão arredondado
        f"""<div class="s papel">{cab}
  <div style="position:absolute;left:80px;right:80px;top:140px;height:640px;border-radius:28px;overflow:hidden;box-shadow:0 30px 60px rgba(35,30,26,.25)">
    <img src="{f['foto']}" style="width:100%;height:100%;object-fit:cover;object-position:center 35%;filter:sepia(.12) saturate(.9)">
    <div style="position:absolute;left:28px;bottom:28px;background:#231E1A;color:#E6CF94;font-size:22px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:10px 18px;border-radius:4px">Desde o primeiro dia</div>
  </div>
  <div style="position:absolute;left:80px;right:80px;top:850px">
    <div class="serif" style="font-size:44px;color:#8F7032;font-weight:600">03</div>
    <div class="serif" style="font-size:92px;line-height:1.05;margin-top:12px">A licença começa na <em>guarda</em></div>
    <div class="txt" style="margin-top:36px">Conta da adoção ou da <b>guarda para fins de adoção</b>. Não precisa esperar a sentença.</div>
    <div style="margin-top:32px"><span class="selo">CLT, art. 392-A, § 4º</span></div>
  </div></div>""",

        # 5 papel com caixas em fluxo
        f"""<div class="s papel">{cab}
  <div style="position:absolute;left:80px;right:80px;top:250px;text-align:center">
    <div class="serif" style="font-size:44px;color:#8F7032;font-weight:600">04</div>
    <div class="serif" style="font-size:96px;line-height:1.05;margin-top:12px">Mais <em>60 dias</em> em empresas cidadãs</div>
    <div class="txt" style="margin-top:36px">Se a empresa aderiu ao Empresa Cidadã, <b>a prorrogação vale igual</b> para quem adota.</div>
  </div>
  <div style="position:absolute;left:190px;right:190px;top:840px;display:flex;flex-direction:column;align-items:center;gap:0">
    <div style="width:100%;border:2px solid #8F7032;border-radius:14px;padding:24px;text-align:center;font-size:34px;font-weight:600">120 dias · licença da CLT</div>
    <div style="width:2px;height:44px;background:#8F7032"></div>
    <div style="width:100%;border:2px solid #8F7032;border-radius:14px;padding:24px;text-align:center;font-size:34px;font-weight:600">+ 60 dias · Empresa Cidadã</div>
    <div style="width:2px;height:44px;background:#8F7032"></div>
    <div class="serif" style="width:100%;background:#231E1A;color:#E6CF94;border-radius:14px;padding:20px;text-align:center;font-size:54px"><em style="color:#C9A962;text-decoration:none">180 dias</em> com a criança</div>
  </div>
  <div style="position:absolute;left:0;right:0;bottom:70px;text-align:center"><span class="selo">Lei 11.770/2008</span></div></div>""",

        # 6 café com palavra vertical gigante + checklist
        f"""<div class="s cafe">{cab}
  <div class="serif" style="position:absolute;right:-40px;top:50%;transform:translateY(-50%) rotate(90deg);transform-origin:center;
    font-size:250px;font-weight:600;letter-spacing:10px;color:#C9A962;opacity:.9;white-space:nowrap;width:250px;height:250px;
    display:flex;align-items:center;justify-content:center">ADOÇÃO</div>
  <div style="position:absolute;left:80px;width:700px;top:250px">
    <div class="serif" style="font-size:44px;color:#C9A962;font-weight:600">05</div>
    <div class="serif" style="font-size:88px;line-height:1.05;margin-top:12px">Licenças em curso <em>já</em> entram</div>
    <div class="txt" style="margin-top:32px">Quem estava de licença em 23/09/2026 já segue a regra nova.</div>
    <div style="margin-top:44px;font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#E6CF94">Separe · salve para conferir</div>
    {''.join(f'<div style="display:flex;gap:22px;align-items:flex-start;margin-top:28px;font-size:34px;line-height:1.35"><span style="flex:none;width:34px;height:34px;border:3px solid #C9A962;border-radius:5px;margin-top:6px"></span>{t}</div>' for t in ('Termo de guarda ou sentença de adoção','Aviso ao RH com a data de início','Confirmar se a empresa é Empresa Cidadã'))}
  </div></div>""",

        # 7 fechamento com retrato
        f"""<div class="s cafe">
  <img src="{f['fecho']}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 25%">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(35,30,26,.5) 0%,rgba(35,30,26,0) 25%,rgba(35,30,26,.15) 45%,#231E1A 76%)"></div>
  {cab}
  <div style="position:absolute;left:80px;right:80px;bottom:110px;z-index:5">
    <div class="serif" style="font-size:100px;line-height:1.02">Família se forma de muitos <em>jeitos</em>.</div>
    <div class="serif" style="font-size:56px;margin-top:18px;color:#E6CF94"><em>O direito é o mesmo.</em></div>
    <div class="txt" style="margin-top:34px">Salve e <b>mande para quem está adotando.</b> Na dúvida, procure uma advogada.</div>
    <div style="margin-top:34px;padding-top:24px;border-top:1px solid rgba(201,169,98,.5);font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#C9A962">Letícia Barros · OAB/ES 39.948</div>
  </div></div>""",
    ]


async def main():
    SAIDA.mkdir(exist_ok=True)
    f = {"capa": uri(RETRATOS / "estudio-escuro-banco.jpg"), "fecho": uri(RETRATOS / "escritorio-cafe-blazer-bege.jpg"),
         "foto": uri(AQUI / "fotos/p10557890.jpg")}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for i, html in enumerate(slides(f), 1):
            await pg.set_content(f'<!doctype html><html><head><meta charset="utf-8">{FONTES}<style>{CSS}</style></head><body>{html}</body></html>')
            await pg.wait_for_load_state("networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(SAIDA / f"adocao-{i:02d}.png"))
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
