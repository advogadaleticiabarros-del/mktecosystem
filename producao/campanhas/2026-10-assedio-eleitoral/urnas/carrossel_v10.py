"""Carrossel v10 "Demissão pelo voto?" com fotos reais da urna (27/10/2026, pedido "Todos inclua fotos das urnas").

Mesmo texto e ordem da v9 (`../carrossel-stories/carrossel9.py`, intacta). Muda:
- capa Ouro editorial com a urna (teclado à direita, título à esquerda, sem cobrir o teclado);
- slides 03 e 04: sai o celular recortado de borda borrada (regra de não usar recorte); entra foto inteira da urna em
  moldura dourada, com crédito;
- slide 05 (cartão "Ameaçar antes do voto é crime"): fundo com a urna.
Uso (de apps/api): python ../../producao/campanhas/2026-10-assedio-eleitoral/urnas/carrossel_v10.py
Saída: apps/api/_saida_producao_1510/pecas/assedio-eleitoral-voto-v10-1..9.jpg
"""
import asyncio
import io
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "carrossel-stories"))

import carrossel9 as c9  # noqa: E402
import urnas  # noqa: E402
from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

N, W = c9.N, c9.W
v5, v4, rc, capa_fecho = c9.v5, c9.v4, c9.rc, c9.capa_fecho


def moldura_foto(n: int, chave: str, top: int, altura: int = 400, foco: tuple[float, float] | None = None) -> str:
    """Foto inteira da urna (sem recorte de objeto) em moldura dourada, com o crédito sobre um degradê escuro."""
    foto = urnas.recorte(chave, 1800, altura * 2, foco=foco)
    return f"""<div style="position:absolute; left:{(n - 1) * 1080 + 90}px; top:{top}px; width:900px; height:{altura}px; z-index:30;
  border-radius:14px; overflow:hidden; border:2px solid #C9A962; box-shadow:0 18px 40px rgba(0,0,0,.28);">
  <img src="{foto}" style="width:900px; height:{altura}px; display:block; filter:sepia(.12) contrast(1.04);">
  <div style="position:absolute; left:0; right:0; bottom:0; height:70px; background:linear-gradient(180deg, transparent, rgba(20,15,12,.78));"></div>
  <div style="position:absolute; right:18px; bottom:12px; font-family:Inter,sans-serif; font-size:22px; font-weight:500; color:rgba(250,246,240,.9);">{urnas.credito(chave)}</div>
</div>"""


def html() -> str:
    logo = rc._logo_data_uri()
    capa = capa_fecho.capa_ouro(
        urnas.recorte("teclado", 2160, 2700, foco=(0.47, 0.5)), area=c9.TAG,
        kicker="Assédio eleitoral no trabalho", titulo="Demissão<br>pelo voto?",
        subtitulo="Isso tem nome na lei: discriminação.",
        apoio='Não importa em quem você votou: <span class="mt">ninguém perde o emprego pela opinião política</span>.'
              '<span class="co-lei">Lei 9.029/1995</span>', total=f"{N:02d}")
    capa = capa.replace('<div class="co-grao"></div>',
                        '<div style="position:absolute; right:70px; bottom:112px; z-index:20; font-size:22px; font-weight:500;'
                        f' color:rgba(250,246,240,.85);">{urnas.credito("teclado")}</div><div class="co-grao"></div>', 1)
    luz = urnas.recorte("luz", 2160, 2700, foco=(0.55, 0.6))
    slides = [
        capa,
        c9.claro(2, "01", "Quase <em>2 mil</em><br>denúncias em 2026",
                 c9.txt('O MPT recebeu 1.939 denúncias de assédio eleitoral no trabalho até o 2º turno, um recorde. '
                        '<span class="mt">No dia seguinte, mais 140</span>.') + c9.selo("MPT, balanço de 26/10/2026")),
        c9.escuro(3, "02", "Demitir pelo voto<br>é <em>discriminação</em>",
                  c9.txt('A lei proíbe dispensar alguém pela opinião política. <span class="mt">Não importa em quem você votou</span>.')
                  + c9.selo("Lei 9.029/1995, art. 1º; CF, art. 5º, VIII"), logo),
        c9.claro(4, "03", "A escolha<br>é <em>sua</em>",
                 c9.txt('Voltar ao emprego com os salários do período <span class="mt">ou receber em dobro</span> a remuneração '
                        'desse tempo. E ainda pode caber dano moral.') + c9.selo("Lei 9.029/1995, art. 4º")),
        c9.foto_cartao(5, "04", "Ameaçar antes<br>do voto é <em>crime</em>",
                       'Coagir alguém a votar ou a não votar em um candidato tem pena de <span class="mt">até 4 anos de reclusão</span>.',
                       "Código Eleitoral, art. 301", luz).replace(
            '<div class="papel"', '<div style="position:absolute; right:70px; bottom:110px; z-index:20; font-size:22px;'
            f' font-weight:500; color:rgba(250,246,240,.9);">{urnas.credito("luz")}</div><div class="papel"', 1),
        c9.claro(6, "05", "O que <em>conta</em><br>como prova",
                 c9.lista([("1", "Mensagens e <b>áudios</b> do chefe ou do RH"), ("2", "<b>Prints</b> do grupo da empresa"),
                           ("3", "<b>Posts</b> da empresa ou do chefe sobre o voto"), ("4", "<b>Carta de dispensa</b>, com a data"),
                           ("5", "Nomes de <b>testemunhas</b>")]), top=270, guarde=True),
        c9.escuro(7, "06", "Guarde <em>do jeito</em><br><em>certo</em>",
                  c9.lista([("✓", "O print mostra <b>data, hora, quem mandou</b> e o nome do grupo"),
                            ("✓", "No WhatsApp, <b>Exportar conversa</b> com as mídias"),
                            ("✓", "<b>Baixe os áudios</b> e salve uma cópia no e-mail ou na nuvem"),
                            ("✓", "Tudo isso <b>antes de sair do grupo</b> ou devolver o celular da empresa")]), logo, top=270),
        c9.claro(8, "07", "Gravar o chefe<br><em>vale</em>?",
                 c9.lista([("✓", "Gravar a conversa <b>da qual você participa</b> vale, mesmo sem o outro saber"),
                           ("✕", "Gravar conversa <b>de outras pessoas</b> não vale"),
                           ("✕", "<b>Não apague nem edite</b> nada"),
                           ("✓", "A denúncia ao <b>MPT</b> pode ser sigilosa")]) + c9.selo("STF, RE 583.937 (Tema 237)"), top=270),
        capa_fecho.fecho(c9.RETRATO, area=c9.TAG, titulo="Seu voto <em>não é</em><br>motivo de demissão.", sub="Cada caso tem detalhes.",
                         apoio='<span class="mt">Salve este post</span> e mande para quem precisa saber disso.',
                         cta="Procure uma advogada de confiança", left=(N - 1) * 1080),
    ]
    fotos = moldura_foto(3, "ue2020", top=880, altura=330, foco=(0.5, 0.55)) + moldura_foto(4, "confirma", top=948, altura=280, foco=(0.72, 0.5))
    corpo = "\n".join(slides) + f"""
<div class="arco" style="left:4950px; top:-620px; width:1000px; height:1000px;"></div>
<div class="arco" style="left:7150px; top:1150px; width:1000px; height:1000px;"></div>
{fotos}
<div class="fosco grao"></div><div class="fosco veu"></div>"""
    pagina = (f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=EB+Garamond:'
              f'ital,wght@0,500;0,600;0,700;0,800;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
              f'<style>{v5.CSS}{v5.EXTRA}{capa_fecho.CSS}{capa_fecho.CSS_OURO}{c9.EXTRA9}</style></head><body><div class="pano">{corpo}</div></body></html>')
    return Template(pagina).render(grao=v4.GRAO, mancha=v4.MANCHA, fibra=v4.FIBRA, ruido=v4.RUIDO)


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": 1350}, device_scale_factor=2)
        await page.set_content(html(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.evaluate("""() => { const el=document.getElementById('big'); let fs=150; el.style.fontSize=fs+'px';
            while (el.offsetWidth > 620 && fs > 70) { fs -= 4; el.style.fontSize = fs + 'px'; } }""")
        pano = Image.open(io.BytesIO(await page.screenshot(type="png"))).convert("RGB")
        await browser.close()
    for i in range(N):
        destino = c9.API / "_saida_producao_1510" / "pecas" / f"{c9.CHAVE}-v10-{i + 1}.png"
        pano.crop((i * 2160, 0, (i + 1) * 2160, 2700)).resize((1080, 1350), Image.LANCZOS).save(destino)
        rc._aplicar_acabamento_dourado(str(destino))
        Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
        destino.unlink()
    print("ok", c9.CHAVE, N)


if __name__ == "__main__":
    asyncio.run(main())
