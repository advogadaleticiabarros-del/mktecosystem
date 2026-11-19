"""Carrossel "Decreto da escala 5x2 assinado" (19/11/2026). A Jessica mandou o carrossel do TST (@tstjus,
instagram.com/p/Df7ZFwQhh2r) e pediu "faça um desse, aplicando a Dra. Letícia". Segue a estrutura da referência
(capa-manchete, datas em cartões, números gigantes sobre foto, descanso), com cores, letras e faixas douradas da marca,
mais a página para salvar e o fecho com o retrato real da Dra. Nada de logo ou texto do TST.
Motor e acabamento: ../manchete/gerar.py. Uso: python gerar.py [prefixo]. Grava em pecas/ (fora do git).
Nunca sobrescreva peça pronta: versão nova = nome novo (ex.: escala-5x2-v2-1.jpg)."""
import asyncio
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "manchete"))
from gerar import ACAB, AREIA, CAFE, FOIL, FUNDO, MARCA, PAPEL, PERFIL, RAIZ, foto  # noqa: E402

FOTOS = AQUI / "fotos"
SAIDA = AQUI / "pecas"
RETRATO = RAIZ / "apps" / "api" / "_saida_producao_1510" / "_retratos" / "estudio-claro-cadeira.jpg"
VERSAO = "escala-5x2-v1"
TOTAL = 8

BASE = f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500&display=swap" rel=stylesheet>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
.c{{width:1080px;height:1440px;position:relative;overflow:hidden;color:{CAFE};font-family:Inter,sans-serif;font-variant-numeric:lining-nums}}
.abs{{position:absolute}}
.g{{font-family:'EB Garamond',serif;font-variant-numeric:lining-nums}}
.ouro{{background:{FOIL};-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 14px rgb(233 200 120/.35))}}
.fx{{background:{MARCA};color:{CAFE};box-shadow:0 0 22px rgb(233 200 120/.45)}}
.sub{{background:linear-gradient(transparent 70%,rgb(214 178 98/.75) 70%,rgb(249 239 194/.9) 86%,transparent 86%)}}
.vidro{{background:rgb(255 255 255/.55);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1.5px solid rgb(255 255 255/.85);box-shadow:0 18px 50px rgb(30 24 20/.16)}}
.fit{{white-space:nowrap;display:block}}
.grao::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:.14;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
</style></head><body><div class="c grao">CORPO</div>
<script>
// .fit: reduz a fonte até a linha caber na largura do bloco pai (manchete sempre de ponta a ponta).
document.fonts.ready.then(()=>{{
  document.querySelectorAll('.fit').forEach(e=>{{let s=parseFloat(getComputedStyle(e).fontSize);const w=e.parentElement.clientWidth;
    while(e.scrollWidth>w&&s>40){{s-=2;e.style.fontSize=s+'px'}}}});
  document.body.dataset.ok=1}})
</script></body></html>"""


def topo(cor, dir="DIREITO DO TRABALHO"):
    return (f'<div class=abs style="left:72px;right:72px;top:58px;display:flex;justify-content:space-between;'
            f'font:600 22px Inter;letter-spacing:.14em;color:{cor}"><span>LETÍCIA BARROS</span><span>{dir}</span></div>')


def rodape(n, cor, arraste=True):
    seta = '<span>Arraste pro lado ›</span>' if arraste else '<span></span>'
    return (f'<div class=abs style="left:72px;right:72px;top:1352px;display:flex;justify-content:space-between;'
            f'font:600 24px Inter;color:{cor}">{seta}<span style="letter-spacing:.1em">0{n} / 0{TOTAL}</span></div>')


def fonte(txt, cor, y=1290, alinhar="left"):
    return (f'<div class=abs style="left:72px;right:72px;top:{y}px;text-align:{alinhar};font:italic 400 24px/1.35 Inter;'
            f'color:{cor}">Fonte: {txt}</div>')


def fundo_foto(arq, pos="center", extra="", esmaece=0):
    m = (f"-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 {esmaece}px);mask-image:linear-gradient(180deg,transparent 0,#000 {esmaece}px);"
         if esmaece else "")
    return f'<div class=abs style="inset:0;background:url({foto(arq, 2200)}) {pos}/cover no-repeat;{m}{extra}"></div>'


# 1 · Capa: manchete gigante no topo (papel), foto do tema embaixo. Ref.: "Decreto da ESCALA 5X2 ASSINADO!"
def p1_capa():
    return f"""
{fundo_foto(FOTOS / '3801439.jpg', '80% 50%', 'top:470px', 260)}
<div class=abs style="inset:0;background:linear-gradient(180deg,{PAPEL} 0,{PAPEL} 40%,rgb(247 241 231/.0) 52%,rgb(30 24 20/0) 82%,rgb(30 24 20/.55) 100%)"></div>
{topo(CAFE)}
<div class=abs style="left:64px;right:64px;top:150px">
  <div style="display:flex;align-items:center;gap:22px;white-space:nowrap">
    <span style="font:400 66px/1 Inter;letter-spacing:-.02em">Decreto da</span>
    <span class=fx style="font:900 70px/1 Inter;letter-spacing:-.03em;padding:8px 20px 12px;border-radius:10px">ESCALA 5X2</span>
  </div>
  <div class=fit style="font:900 214px/1 Inter;letter-spacing:-.055em;word-spacing:.18em;margin-top:14px">ASSINADO.</div>
  <div style="font:500 40px/1.3 Inter;letter-spacing:-.01em;margin-top:26px;max-width:640px">O que muda na sua jornada e o que os números mostram sobre <span class=sub style="font-weight:700">quem mais precisa de descanso</span>.</div>
</div>
{rodape(1, '#fff')}"""


# 2 · Datas: título grande e as duas etapas em cartões. Ref.: "DOIS DIAS de descanso remunerado" + 16/12/2026 e 16/12/2027.
def p2_datas():
    cartao = ("flex:1;border-radius:26px;padding:34px 30px 38px;text-align:center;position:relative;overflow:hidden")
    faixa = f'<div class=abs style="left:0;right:0;top:0;height:10px;background:{FOIL}"></div>'
    return f"""
<div class=abs style="inset:0;background:radial-gradient(90% 70% at 50% 40%,#fbf6ee 0,{PAPEL} 55%,{AREIA} 100%)"></div>
<div class="abs g ouro" style="right:-40px;top:250px;font-size:520px;font-weight:700;line-height:1;opacity:.22">5x2</div>
{topo(CAFE)}
<div class=abs style="left:64px;right:64px;top:230px;text-align:center">
  <div style="font:900 150px/1 Inter;letter-spacing:-.05em;word-spacing:.18em">DOIS DIAS</div>
  <div class=g style="font-size:84px;font-weight:500;line-height:1.05;margin-top:6px">de descanso <i class=sub>remunerado</i></div>
  <div style="font:400 44px/1.3 Inter;margin-top:56px">Em regra, a jornada máxima<br>cai em <b style="font-weight:800">duas etapas:</b></div>
  <div style="display:flex;gap:28px;margin-top:40px;text-align:center">
    <div class=vidro style="{cartao}">{faixa}<div style="font:800 58px Inter;letter-spacing:-.02em">16/12/2026</div>
      <div style="font:400 36px/1.3 Inter;margin-top:16px">Até <b>42 horas</b> por semana, com <b>duas folgas</b></div></div>
    <div class=vidro style="{cartao}">{faixa}<div style="font:800 58px Inter;letter-spacing:-.02em">16/12/2027</div>
      <div style="font:400 36px/1.3 Inter;margin-top:16px">Até <b>40 horas</b><br>por semana</div></div>
  </div>
  <div style="margin-top:64px"><span class=fx style="display:inline-block;font:800 40px Inter;padding:14px 30px;border-radius:12px">A jornada diminui. O salário, não.</span></div>
</div>
{fonte('Emenda Constitucional 141/2026 e decreto de 19/11/2026', '#6b5a4a', 1268, 'center')}
{rodape(2, CAFE)}"""


# 3 · Número gigante sobre foto. Ref.: "Quem trabalha 6 dias por semana? 14,8 MILHÕES de vínculos estavam na escala 6x1".
def p3_milhoes():
    return f"""
{fundo_foto(FOTOS / '37330783.jpg', '50% 70%')}
<div class=abs style="inset:0;background:linear-gradient(180deg,rgb(30 24 20/.92) 0,rgb(30 24 20/.86) 40%,rgb(30 24 20/.35) 52%,rgb(30 24 20/0) 64%,rgb(30 24 20/.7) 100%)"></div>
{topo(AREIA)}
<div class=abs style="left:64px;right:64px;top:190px;color:#fff">
  <div style="font:400 62px/1.12 Inter;letter-spacing:-.02em">Quem trabalha<br>6 dias por semana?</div>
  <div class="fit ouro" style="font:900 176px/1.05 Inter;letter-spacing:-.05em;word-spacing:.18em;margin-top:22px">14,8 MILHÕES</div>
  <div style="font:500 62px/1.1 Inter;letter-spacing:-.025em;margin-top:6px">de vínculos estavam<br>na escala 6x1</div>
</div>
{fonte('Ministério do Trabalho e Emprego,<br>com dados do eSocial (2026)', AREIA, 1222, 'right')}
{rodape(3, '#fff')}"""


# 4 · Ref.: "Quem tem menos tempo para descansar? AS MULHERES" (6,8 horas a mais). O público da Dra.
def p4_mulheres():
    return f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
{fundo_foto(FOTOS / '7901545.jpg', '38% 40%', 'top:600px', 200)}
<div class=abs style="left:0;right:0;bottom:0;height:260px;background:linear-gradient(180deg,rgb(30 24 20/0),rgb(30 24 20/.7))"></div>
{topo(CAFE)}
<div class=abs style="left:64px;right:64px;top:170px">
  <div style="font:400 54px/1.12 Inter;letter-spacing:-.02em;color:#6b5a4a">Quem tem menos tempo<br>para descansar?</div>
  <div class=fit style="font:900 190px/1.02 Inter;letter-spacing:-.055em;word-spacing:.18em;margin-top:14px">AS MULHERES</div>
  <div style="font:400 40px/1.3 Inter;margin-top:18px;max-width:900px">dedicavam, em média, <span class=fx style="font-weight:800;padding:0 12px 2px;border-radius:6px">6,8 horas a mais</span> por semana que os homens ocupados às tarefas da casa e ao cuidado de pessoas.</div>
</div>
{fonte('IBGE, PNAD Contínua 2022', '#fff', 1290)}
{rodape(4, '#fff')}"""


# 5 · Ref.: "JORNADAS MAIS LONGAS >> REMUNERAÇÕES MENORES". Página café (acento escuro), sem "R$": comparação em barras.
def p5_salario():
    barra = "height:84px;border-radius:12px;display:flex;align-items:center;padding:0 26px;font:800 34px Inter"
    return f"""
<div class=abs style="inset:0;background:radial-gradient(80% 60% at 30% 30%,#3a3029 0,{FUNDO} 60%,#17120f 100%)"></div>
{topo(AREIA)}
<div class=abs style="left:64px;right:64px;top:200px;color:{AREIA}">
  <div style="display:flex;align-items:center;gap:26px">
    <div class=ouro style="font:900 64px/1 Inter;letter-spacing:-.03em">JORNADAS<br>MAIS LONGAS</div>
    <div class=ouro style="font:900 90px/1 Inter">»</div>
    <div class=ouro style="font:900 64px/1 Inter;letter-spacing:-.03em">SALÁRIOS<br>MENORES</div>
  </div>
  <div style="font:400 42px/1.3 Inter;margin-top:64px">Em 2023, quem trabalhava <b style="color:#fff">44 horas</b> por semana ganhava, em média,</div>
  <div class=fit style="font:900 150px/1.05 Inter;letter-spacing:-.05em;word-spacing:.18em;color:#fff;margin-top:14px">MENOS DA METADE</div>
  <div style="font:400 42px/1.3 Inter">de quem trabalhava <b style="color:#fff">até 40 horas</b>.</div>
  <div style="margin-top:90px;font:500 26px Inter;letter-spacing:.12em;color:#b9a891">REMUNERAÇÃO MÉDIA NO MÊS</div>
  <div style="margin-top:22px;display:flex;flex-direction:column;gap:20px">
    <div style="{barra};width:42%;background:rgb(239 230 217/.16);color:#fff;border:1.5px solid rgb(239 230 217/.35)">44 horas</div>
    <div class=fx style="{barra};width:100%">Até 40 horas</div>
  </div>
  <div class=g style="font-size:54px;font-style:italic;font-weight:500;line-height:1.15;margin-top:70px;color:#fff">Mais horas de trabalho<br>não querem dizer <span class=ouro>salário maior</span>.</div>
</div>
{fonte('Ipea, com dados da RAIS 2023 (vínculos formais analisados)', '#b9a891', 1268)}
{rodape(5, AREIA)}"""


# 6 · Ref.: "DESCANSO E PRODUTIVIDADE" (OIT), família junta embaixo.
def p6_descanso():
    return f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
{fundo_foto(FOTOS / '4545202.jpg', '50% 30%', 'top:700px', 200)}
{topo(CAFE)}
<div class=abs style="left:64px;right:64px;top:170px">
  <div style="font:900 128px/.96 Inter;letter-spacing:-.05em;word-spacing:.18em">DESCANSO E</div><div class=fit style="font:900 128px/.96 Inter;letter-spacing:-.05em">PRODUTIVIDADE</div>
  <div style="font:400 42px/1.28 Inter;margin-top:40px"><b style="font-weight:800">Jornadas mais curtas e bem organizadas</b> podem reduzir o cansaço e favorecer a produtividade por hora trabalhada.</div>
  <div style="font:400 32px/1.35 Inter;margin-top:22px;color:#6b5a4a">O resultado depende de como cada atividade organiza as equipes, os horários e as tarefas.</div>
</div>
<div class=abs style="left:72px;top:1290px"><span style="font:italic 400 24px Inter;color:#fff;background:rgb(30 24 20/.45);padding:6px 14px;border-radius:8px">Fonte: Organização Internacional do Trabalho (OIT)</span></div>
{rodape(6, '#fff')}"""


# 7 · Página para salvar (padrão da Dra.): o que fazer se a escala não mudar.
def p7_guarde():
    item = (f'<div style="display:flex;align-items:center;gap:22px;font:500 42px Inter;padding:32px 0;border-bottom:1.5px solid rgb(30 24 20/.12)">'
            f'<span style="flex:none;width:40px;height:40px;border-radius:8px;border:3px solid #8F7032"></span>TXT</div>')
    itens = "".join(item.replace("TXT", t) for t in ["Foto da escala de dezembro", "Espelho de ponto", "Holerite de novembro e de janeiro"])
    return f"""
<div class=abs style="inset:0;background:radial-gradient(90% 70% at 50% 30%,#fbf6ee 0,{PAPEL} 60%,{AREIA} 100%)"></div>
{topo(CAFE)}
<div class=abs style="right:64px;top:150px;display:flex;align-items:center;gap:12px;background:{FUNDO};color:{AREIA};font:700 23px Inter;letter-spacing:.14em;padding:12px 20px;border-radius:8px">
  <i style="display:inline-block;width:18px;height:24px;background:{FOIL};clip-path:polygon(0 0,100% 0,100% 100%,50% 75%,0 100%)"></i>SALVE PARA CONFERIR</div>
<div class=abs style="left:64px;right:64px;top:300px">
  <div style="font:700 26px Inter;letter-spacing:.16em;color:#8F7032">E SE A ESCALA NÃO MUDAR?</div>
  <div class=g style="font-size:112px;font-weight:600;line-height:1;margin-top:18px">Guarde<br><i class=sub>desde já</i></div>
  <div style="font:400 40px/1.38 Inter;margin-top:40px">Sem acordo da categoria, a empresa pode fazer 5 dias de até 8h24. <b style="font-weight:800">Seis dias com uma folga, não.</b></div>
  <div style="margin-top:34px">{itens}</div>
  <div style="display:inline-block;margin-top:56px;font:700 24px Inter;letter-spacing:.08em;background:{MARCA};padding:10px 18px;border-radius:6px">EC 141/2026 · STF, ADIs 8.041 E 8.042</div>
</div>
{rodape(7, CAFE)}"""


# 8 · Fecho com o retrato real da Dra. (regra desde 09/11/2026), sem filtro no rosto.
def p8_fecho():
    return f"""
<div class=abs style="inset:0;background:{PAPEL}"></div>
<img class=abs src="{foto(RETRATO, 1300)}" style="left:400px;top:0;width:1080px;height:1440px;object-fit:cover;object-position:50% 20%">
<div class=abs style="inset:0;background:linear-gradient(90deg,{PAPEL} 0,{PAPEL} 40%,rgb(247 241 231/.85) 48%,rgb(247 241 231/0) 62%)"></div>
{topo(CAFE, 'OAB/ES 39.948')}
<div class=abs style="left:64px;top:300px;width:500px">
  <div class=g style="font-size:96px;font-weight:600;line-height:1.0">A jornada<br>diminui.<br><i class=sub>O salário,<br>não.</i></div>
  <div style="font:500 34px/1.35 Inter;margin-top:44px">Salve e mande para quem trabalha na 6x1.</div>
  <div style="font:400 30px/1.4 Inter;margin-top:24px;color:#6b5a4a">Cada caso tem detalhes. Procure uma advogada de confiança.</div>
  <div style="margin-top:56px;width:120px;height:3px;background:{FOIL}"></div>
  <div class=g style="font-size:44px;font-weight:600;margin-top:22px">Letícia Barros</div>
  <div style="font:500 24px Inter;letter-spacing:.12em;margin-top:6px">ADVOGADA · OAB/ES 39.948</div>
  <div style="font:600 28px Inter;margin-top:14px">{PERFIL}</div>
</div>
{rodape(8, CAFE, arraste=False)}"""


LOTE = [p1_capa, p2_datas, p3_milhoes, p4_mulheres, p5_salario, p6_descanso, p7_guarde, p8_fecho]


async def main():
    so = sys.argv[1:]
    SAIDA.mkdir(exist_ok=True)
    ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for i, fn in enumerate(LOTE, 1):
            nome = f"{VERSAO}-{i}"
            if so and str(i) not in so:
                continue
            destino = SAIDA / f"{nome}.jpg"
            await pg.set_content(BASE.replace("CORPO", fn()), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(destino, quality=92)
            print(destino.name)
        await b.close()
    fs = [SAIDA / f"{VERSAO}-{i}.jpg" for i in range(1, TOTAL + 1)]
    if all(f.exists() for f in fs):
        grade = Image.new("RGB", (4 * 488 - 8, 2 * 648 - 8), "white")
        for i, f in enumerate(fs):
            grade.paste(Image.open(f).resize((480, 640), Image.LANCZOS), ((i % 4) * 488, (i // 4) * 648))
        grade.save(AQUI / "grade.jpg", quality=86)


if __name__ == "__main__":
    asyncio.run(main())
