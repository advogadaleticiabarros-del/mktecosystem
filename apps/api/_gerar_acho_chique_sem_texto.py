"""Gera os 16 fundos do Acho Chique (foto + filtro retrô + rodapé com logo),
sem nenhuma frase/título sobreposta, para a usuária inserir o texto em outro
app. Reusa o mesmo template e as mesmas fotos já escolhidas, só omite os
blocos de texto do .conteudo.
"""
import asyncio
import base64
from pathlib import Path

from jinja2 import Template
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
LOGO = Path(r"C:\Users\prosy\Desktop\PROJETOS\modelo-visual-site\assets\logo\logo-800x800.png")
OUT = BASE / "_saida_acho_chique"
OUT_SEM_TEXTO = BASE / "_saida_acho_chique_sem_texto"

TEMPLATE_SEM_TEXTO = """
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { margin: 0; }
  .card {
    width: 1080px; height: 1350px;
    position: relative; overflow: hidden;
    font-family: sans-serif;
  }
  .foto {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    filter: grayscale(0.05) contrast(1.1) saturate(1.2) sepia(0.28) brightness(0.96);
  }
  .grao {
    position: absolute; inset: -2px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='3' stitchTiles='stitch' seed='7'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3CfeComponentTransfer%3E%3CfeFuncA type='linear' slope='2.2' intercept='-0.15'/%3E%3C/feComponentTransfer%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    mix-blend-mode: overlay;
    opacity: 0.85;
  }
  .vinheta {
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at center, transparent 32%, rgba(12,8,4,0.75) 100%);
    z-index: 1;
  }
  .tom-quente {
    position: absolute; inset: 0;
    background: linear-gradient(160deg, rgba(150,85,25,0.28) 0%, transparent 45%, rgba(35,20,8,0.32) 100%);
    mix-blend-mode: multiply;
    z-index: 1;
  }
  .escurecimento {
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(25,17,10,0.4) 0%, rgba(25,17,10,0.18) 35%, rgba(25,17,10,0.58) 100%);
  }
  .escurecimento.forte {
    background: linear-gradient(180deg, rgba(18,12,6,0.65) 0%, rgba(18,12,6,0.52) 35%, rgba(18,12,6,0.75) 100%);
  }
  .seta {
    position: absolute; top: 50%; transform: translateY(-50%);
    width: 56px; height: 56px;
    border-radius: 50%;
    background: rgba(255,255,255,0.28);
    display: flex; align-items: center; justify-content: center;
    z-index: 3;
    color: #fff; font-size: 26px; font-weight: 700;
  }
  .seta.esq { left: 28px; }
  .seta.dir { right: 28px; }
  .rodape {
    position: absolute; left: 0; right: 0; bottom: 46px;
    z-index: 3;
    display: flex; align-items: center; justify-content: center; gap: 14px;
  }
  .rodape img { width: 58px; height: 58px; object-fit: contain; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.4)); }
  .rodape .textos { text-align: left; }
  .rodape .nome { font-weight: 800; font-size: 21px; color: #fff; letter-spacing: 0.3px; }
  .rodape .sub { font-weight: 600; font-size: 14px; color: #F5E3A8; letter-spacing: 1.5px; text-transform: uppercase; }
</style>
</head>
<body>
  <div class="card">
    <img class="foto" src="{{ foto_src }}" alt="">
    <div class="tom-quente"></div>
    <div class="grao"></div>
    <div class="vinheta"></div>
    <div class="escurecimento {{ 'forte' if fechamento_forte else '' }}"></div>
    <div class="seta esq">&#8249;</div>
    <div class="seta dir">&#8250;</div>
    <div class="rodape">
      <img src="{{ logo_src }}" alt="">
      <div class="textos">
        <div class="nome">Letícia Barros</div>
        <div class="sub">Advocacia</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# Só precisamos saber quantos slides e qual é o fechamento (escurecimento
# forte) de cada carrossel — reaproveita a contagem já usada nos originais.
SLIDES_POR_CARROSSEL = {
    "trabalhista": 8,
    "familia": 8,
}
INDICE_FECHAMENTO = 8  # último slide de cada carrossel usa escurecimento forte


def _data_uri(caminho: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(caminho.read_bytes()).decode()


async def gerar_sem_texto(nome_pasta: str, total_slides: int) -> None:
    tpl = Template(TEMPLATE_SEM_TEXTO)
    logo_src = _data_uri(LOGO, "image/png")
    pasta_fotos_origem = OUT / nome_pasta
    pasta_destino = OUT_SEM_TEXTO / nome_pasta
    pasta_destino.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for i in range(1, total_slides + 1):
            foto_path = pasta_fotos_origem / f"foto_{i}.jpg"
            foto_src = _data_uri(foto_path, "image/jpeg")
            fechamento_forte = i == INDICE_FECHAMENTO
            html = tpl.render(logo_src=logo_src, foto_src=foto_src, fechamento_forte=fechamento_forte)
            await page.set_content(html)
            caminho = pasta_destino / f"slide-{i}-sem-texto.png"
            await page.screenshot(path=str(caminho))
            print(f"{nome_pasta} slide {i} -> {caminho}")
        await browser.close()


async def main():
    for nome_pasta, total in SLIDES_POR_CARROSSEL.items():
        await gerar_sem_texto(nome_pasta, total)


if __name__ == "__main__":
    asyncio.run(main())
