"""Frase v3 e estático v2 com foto real da urna de fundo (27/10/2026, pedido "Todos inclua fotos das urnas").

A v2 da frase e a v1 do estático (`../frase-estatico/gerar.py`) continuam intactas. Aqui o mesmo HTML ganha a foto
da urna sob um véu café forte (mais escuro atrás do texto) e o crédito da foto.
Uso (de apps/api): py ../../producao/campanhas/2026-10-assedio-eleitoral/urnas/frase_estatico_v.py
Saída: ../frase-estatico/pecas/assedio-eleitoral-frase-v3.jpg e assedio-eleitoral-estatico-provas-v2.jpg
"""
import asyncio
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
API = AQUI.parents[3] / "apps" / "api"
sys.path.insert(0, str(API))
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "frase-estatico"))

import gerar as v1  # noqa: E402
import urnas  # noqa: E402

from app.services.render_criativo import _env, _fotografar, _logo_data_uri  # noqa: E402

SAIDA = AQUI.parent / "frase-estatico" / "pecas"
CREDITO = ('<div style="position:absolute; left:0; right:0; bottom:46px; z-index:7; text-align:center; font-family:Inter,sans-serif;'
           ' font-size:22px; font-weight:500; color:rgba(232,222,209,.72);">{}</div>')


def camada(chave: str, foco: tuple[float, float], veu_centro: float, veu_borda: float, centro_y: str = "48%") -> str:
    foto = urnas.recorte(chave, 1080, 1350, foco=foco)
    return (f'<img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1350px; z-index:0;'
            f' filter:sepia(.22) saturate(.85) contrast(1.05) blur(1px);">'
            f'<div style="position:absolute; inset:0; z-index:0; background:radial-gradient(ellipse 75% 55% at 50% {centro_y},'
            f' rgba(26,21,17,{veu_centro}) 0%, rgba(26,21,17,{veu_centro}) 45%, rgba(26,21,17,{veu_borda}) 100%);"></div>')


def html_frase() -> str:
    html = _env.get_template("frase_impacto.html").render(
        frase=v1.FRASE, fundo="#231E1A", dourado="#C9A962", areia="#E8DED1", tamanho_fonte=72,
        nome_conta="Letícia Barros", oab="OAB/ES 39.948", logo_src=_logo_data_uri())
    html = html.replace('<div class="mancha"></div>', camada("confirma", (0.70, 0.5), .86, .6), 1)
    return html.replace('<div class="grao"></div>', '<div class="grao"></div>' + CREDITO.format(urnas.credito("confirma")), 1)


def html_estatico() -> str:
    html = v1.html_estatico()
    html = html.replace('<img class="marca"', camada("teclado", (0.62, 0.5), .9, .7, centro_y="52%") + '<img class="marca"', 1)
    return html.replace('<div class="grao"></div>', '<div class="grao"></div>' + CREDITO.format(urnas.credito("teclado")), 1)


async def main():
    SAIDA.mkdir(exist_ok=True)
    frase = SAIDA / "assedio-eleitoral-frase-v3.png"
    await _fotografar(html_frase(), str(frase))
    print("ok", v1.jpg(frase))
    est = SAIDA / "assedio-eleitoral-estatico-provas-v2.png"
    await _fotografar(html_estatico(), str(est))
    print("ok", v1.jpg(est))


if __name__ == "__main__":
    asyncio.run(main())
