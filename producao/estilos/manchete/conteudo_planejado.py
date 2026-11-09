"""Manchete para o conteúdo já planejado (09/11/2026, pedido da Jessica: "pegue tudo que temos produzido e coloque nesses
novos estilos, principalmente os estáticos"). Lê os dados de apps/api/_saida_producao_1510/conteudo_<mes>.py e monta,
com o mesmo texto aprovado, três modelos: pergunta (foto da peça, pergunta empilhada à esquerda), frase (papel, frase
com o fecho em faixa dourada) e Mito ou Lei (afirmação, carimbo do veredito, explicação e lei).
Uso: python conteudo_planejado.py dez [prefixo ...]  → pecas/<mes>-<data>-<tipo>-<chave>.jpg (arquivo novo)."""
import asyncio
import os
import html
import io
import re
import sys

from PIL import Image
from playwright.async_api import async_playwright

from fora_da_caixa import rodape, topo
from gerar import ACAB, AREIA, BANCO, BASE, CAFE, FOIL, FUNDO, MARCA, PAPEL, RAIZ, SAIDA, foto

sys.path.insert(0, str(RAIZ / "apps" / "api" / "_saida_producao_1510"))

# Cada bloco com data-max encolhe até caber na altura indicada (textos aprovados têm tamanhos diferentes).
AJUSTA = """<script>document.fonts.ready.then(()=>{document.querySelectorAll('[data-max]').forEach(e=>{
 let s=parseFloat(getComputedStyle(e).fontSize);const m=+e.dataset.max,min=+(e.dataset.min||40);
 while(e.offsetHeight>m&&s>min){s-=2;e.style.fontSize=s+'px'}});document.body.dataset.ajustado=1})</script>"""

AREAS = {"Trabalhista": "DIREITO TRABALHISTA", "Família": "DIREITO DE FAMÍLIA", "Previdenciário": "DIREITO PREVIDENCIÁRIO",
         "Consumidor": "DIREITO DO CONSUMIDOR"}


def partes(texto):
    """'Contexto. <em>Pergunta?</em>' → ('Contexto.', 'Pergunta?')."""
    m = re.match(r"(.*?)<em>(.*?)</em>(.*)", texto, re.S)
    if not m:
        return "", texto
    return m.group(1).strip(), (m.group(2) + m.group(3)).strip()


def pergunta(t, p):
    contexto, perg = partes(p["html"])
    pos = p.get("pos", "50% 50%")
    return ("", f"""
<div class=abs style="left:300px;right:-40px;top:-40px;bottom:-40px;background:url({foto(BANCO / f'{p["foto"]}.jpg', 1500)}) {pos}/cover;filter:brightness({p.get('brilho', 1)});-webkit-mask-image:linear-gradient(90deg,transparent,#000 32%);mask-image:linear-gradient(90deg,transparent,#000 32%)"></div>
<div class=abs style="inset:0;background:linear-gradient(90deg,rgb(30 24 20/.9) 0,rgb(30 24 20/.78) 48%,rgb(30 24 20/.1) 78%),linear-gradient(180deg,rgb(30 24 20/.5) 0,rgb(30 24 20/0) 16%,rgb(30 24 20/0) 76%,rgb(30 24 20/.88) 100%)"></div>
<div class=topo style="color:{AREIA}"><span>LETÍCIA BARROS</span><span>{AREAS.get(t["area"], "OAB/ES 39.948")}</span></div>
<div class=abs style="left:72px;top:300px;width:700px;height:900px;display:flex;flex-direction:column;justify-content:center;color:#fff">
  <div data-max=210 data-min=30 style="font:300 42px/1.3 Inter;letter-spacing:.01em">{contexto}</div>
  <div class=p data-max=560 data-min=70 style="font-size:118px;line-height:1.06;font-style:italic;font-weight:400;margin-top:26px">{perg}</div>
  <div style="margin-top:40px;width:120px;height:4px;background:{FOIL}"></div>
</div>
{rodape(AREIA)}""")


def frase(t, f):
    abre, fecho = partes(f["html"])
    return ("", f"""
<div class=abs style="inset:0;background:linear-gradient(170deg,#fff 0,{PAPEL} 45%,{AREIA} 100%)"></div>
<div class=abs style="inset:0;background-image:radial-gradient(rgb(30 24 20/.08) 1.4px,transparent 1.5px);background-size:30px 30px"></div>
{topo(CAFE)}
<div class=abs style="left:80px;right:80px;top:180px;height:1080px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">
  <div style="font:600 24px Inter;letter-spacing:.16em;color:#8A6420">{AREAS.get(t["area"], t["area"].upper())}</div>
  <div class=p data-max=520 data-min=56 style="font-size:104px;line-height:1.12;font-weight:400;margin-top:40px">{abre}</div>
  <div class=p data-max=360 data-min=52 style="display:inline-block;background:{MARCA};font-size:92px;line-height:1.2;font-style:italic;font-weight:700;padding:8px 34px 16px;margin-top:34px;transform:rotate(-1deg)">{fecho}</div>
</div>
{rodape(CAFE)}""")


def mito(m):
    data, _chave, afirmacao, veredito, explicacao, lei = m[:6]
    carimbo = "MITO" if veredito == "MITO" else "É LEI"
    risco = "text-decoration:line-through;text-decoration-thickness:3px;text-decoration-color:rgb(232 208 138/.85)" if veredito == "MITO" else ""
    return ("", f"""
<div class=abs style="inset:0;background:{FUNDO}"></div>
<div class=abs style="inset:0;background:radial-gradient(70% 45% at 50% 34%,#4a3d32 0,rgb(35 30 26/0) 70%)"></div>
<div class=topo style="color:{AREIA}"><span>LETÍCIA BARROS</span><span>OAB/ES 39.948</span></div>
<div class=abs style="left:0;right:0;top:150px;text-align:center"><span class=p style="display:inline-block;background:{MARCA};color:{CAFE};font-size:58px;font-style:italic;font-weight:700;padding:4px 30px 10px">Mito ou Lei?</span></div>
<div class=abs style="left:90px;right:90px;top:300px;height:440px;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff">
  <div class=p data-max=440 data-min=56 style="font-size:96px;line-height:1.14;font-weight:400;{risco}">“{afirmacao}”</div>
</div>
<div class=abs style="left:0;right:0;top:770px;text-align:center">
  <span style="display:inline-block;border:6px solid #e8d08a;color:#e8d08a;font:800 92px Inter;letter-spacing:.08em;padding:6px 40px;transform:rotate(-4deg);border-radius:10px">{carimbo}</span>
</div>
<div class=abs style="left:110px;right:110px;top:960px;height:2px;background:{FOIL}"></div>
<div class=abs data-max=250 data-min=28 style="left:110px;right:110px;top:996px;text-align:center;font:300 38px/1.38 Inter;color:#fff">{explicacao}</div>
<div class=abs style="left:0;right:0;top:1280px;text-align:center;font:500 26px Inter;color:#e8d08a">{lei}</div>
{rodape(AREIA)}""")


def pecas(mes):
    dados = __import__(f"conteudo_{mes}")
    saida = {}
    for t in dados.TEMAS:
        base = f"{mes}-{t['data'][5:]}"
        if t.get("pergunta", {}).get("foto"):
            saida[f"{base}-pergunta-{t['chave']}"] = pergunta(t, t["pergunta"])
        if t.get("frase"):
            saida[f"{base}-frase-{t['chave']}"] = frase(t, t["frase"])
    for m in dados.MITO_OU_LEI:
        saida[f"{mes}-{m[0][5:]}-mito-{m[1]}"] = mito(m)
    return saida


async def main():
    mes, so = sys.argv[1], sys.argv[2:]
    todas = pecas(mes)
    SAIDA.mkdir(exist_ok=True)
    ac = Image.open(ACAB).convert("RGBA").resize((1080, 1440))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1440})
        for nome, (css, corpo) in todas.items():
            if so and not any(nome.startswith(x) for x in so):
                continue
            destino = SAIDA / f"{nome}.jpg"
            if destino.exists() and not os.environ.get("EDITOR_IMPORTA"):  # peça pronta nunca é sobrescrita
                print("já existe:", nome)
                continue
            await pg.set_content(BASE.replace("CSS</style>", css + "</style>").replace("CORPO", corpo).replace("</body>", AJUSTA + "</body>"),
                                 wait_until="networkidle")
            await pg.wait_for_selector("body[data-ajustado]", state="attached")
            bruto = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1080, "height": 1440})
            Image.alpha_composite(Image.open(io.BytesIO(bruto)).convert("RGBA"), ac).convert("RGB").save(destino, quality=90)
            print(nome)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
