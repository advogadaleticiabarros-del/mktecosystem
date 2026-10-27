"""Carrossel "Demissão pelo voto?" v2, 9 slides (pedido de 27/10/2026: "bem explicativo e estruturado, 8 a 10 slides,
com slide de provas"). Mesma linguagem do v5 aprovado (capa Ouro editorial, papel claro, slide escuro com logo, cartão
sobre foto, checklist "Salve para conferir", fechamento com retrato da Dra.), estendida para 9 slides com dois slides
de provas. Reaproveita CSS e funções de `carrossel_v5`/`capa_fecho` sem alterá-los.

Fatos (conferidos em 27/10/2026, ver ../BRIEFING.md): MPT 1.939 denúncias até 25/10 e 140 em 26/10; CF, art. 5º, VIII;
Lei 9.029/1995, arts. 1º e 4º; Código Eleitoral, art. 301; STF, RE 583.937 (Tema 237); denúncia sigilosa no MPT.

Uso (de apps/api): python ../../producao/campanhas/2026-10-assedio-eleitoral/carrossel-stories/carrossel9.py
Saída: apps/api/_saida_producao_1510/pecas/assedio-eleitoral-voto-v9-1..9.jpg
"""
import asyncio
import io
import sys
from pathlib import Path

API = Path(__file__).resolve().parents[4] / "apps" / "api"
sys.path.insert(0, str(API))
sys.path.insert(0, str(API / "_saida_producao_1510"))

import carrossel_v5 as v5  # noqa: E402
from jinja2 import Template  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

capa_fecho, v4, rc = v5.capa_fecho, v5.v4, v5.render_criativo

CHAVE = "assedio-eleitoral-voto"
N = 9
W = N * 1080
TAG, AREA = "Assédio eleitoral", "Trabalhista"
RETRATO = "escritorio-cafe-blazer-preto"

EXTRA9 = f"""
body, .pano {{ width:{W}px !important; }}
.lista9 {{ margin-top:40px; display:flex; flex-direction:column; gap:28px; max-width:860px; }}
.lista9 .it {{ display:flex; gap:22px; align-items:flex-start; font-size:37px; line-height:1.36; }}
.lista9 .ic {{ flex:0 0 50px; height:50px; border-radius:50%; border:2.5px solid #B8943F; display:flex; align-items:center;
  justify-content:center; font-size:23px; font-weight:800; margin-top:1px; }}
.claro .lista9 .it {{ color:#3D2B1F; }} .claro .lista9 .ic {{ color:#8F7032; }} .claro .lista9 b {{ color:#231E1A; }}
.escuro .lista9 .it {{ color:#E8DED1; }} .escuro .lista9 .ic {{ border-color:#C9A962; color:#E9D398; }} .escuro .lista9 b {{ color:#FAF6F0; }}
"""


def cab() -> str:
    return f'<div class="cab"><span>Letícia Barros · Advocacia</span><span>{AREA}</span></div>'


def rod(n: int) -> str:
    return f'<div class="rod"><span>Arraste pro lado ›</span><span class="pg">{n:02d} / {N:02d}</span></div>'


def lista(itens: list[tuple[str, str]]) -> str:
    return '<div class="lista9">' + "".join(f'<div class="it"><div class="ic">{i}</div><div>{t}</div></div>' for i, t in itens) + "</div>"


def claro(n: int, num: str, tit: str, corpo: str, top: int = 300, guarde: bool = False) -> str:
    return f"""<div class="s claro textura" style="left:{(n - 1) * 1080}px">{cab()}
  {'<div class="guarde"><i></i>Salve para conferir</div>' if guarde else ''}
  <div class="marca" style="right:20px; top:{150 if not guarde else 250}px; font-size:560px;">{num}</div>
  <div class="bloco" style="top:{top}px;"><div class="num">{num}</div><div class="tit">{tit}</div>{corpo}</div>{rod(n)}</div>"""


def escuro(n: int, num: str, tit: str, corpo: str, logo: str, top: int = 300) -> str:
    return f"""<div class="s escuro textura" style="left:{(n - 1) * 1080}px">{cab()}
  <img class="marca-logo" src="{logo}" style="right:-300px; top:330px; width:980px;">
  <div class="bloco" style="top:{top}px;"><div class="num">{num}</div><div class="tit">{tit}</div>{corpo}</div>{rod(n)}</div>"""


def foto_cartao(n: int, num: str, tit: str, txt: str, selo: str, foto: str) -> str:
    tit = tit.replace("<em>", '<em style="font-style:italic; border-bottom:4px solid #C9A962;">')
    return f"""<div class="s foto" style="left:{(n - 1) * 1080}px">
  <img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1350px;">
  <div style="position:absolute; inset:0; background:linear-gradient(180deg, rgba(35,30,26,.55), rgba(35,30,26,.35) 40%, rgba(35,30,26,.75));"></div>
  {cab()}
  <div class="papel" style="left:120px; top:360px; width:760px; transform:rotate(-3deg);">
    <div class="num" style="color:#8F7032;">{num}</div>
    <div class="cg" style="font-size:72px; font-weight:600; line-height:1.04; margin-top:6px;">{tit}</div>
    <div style="font-size:32px; line-height:1.45; margin-top:26px; color:#3D2B1F;">{txt}</div>
    <div class="selo" style="background:#231E1A; color:#E8DED1;">{selo}</div>
  </div>{rod(n)}</div>"""


def txt(t: str, largura: int = 640) -> str:
    return f'<div class="txt" style="max-width:{largura}px;">{t}</div>'


def selo(t: str) -> str:
    return f'<div class="selo">{t}</div>'


def html() -> str:
    logo = rc._logo_data_uri()
    capa = capa_fecho.capa_ouro(
        capa_fecho.enquadrar(API / "_saida_producao_1510" / "_fotos_pexels" / f"original-{CHAVE}.jpg"), area=TAG,
        kicker="Assédio eleitoral no trabalho", titulo="Demissão<br>pelo voto?",
        subtitulo="Isso tem nome na lei: discriminação.",
        apoio='Não importa em quem você votou: <span class="mt">ninguém perde o emprego pela opinião política</span>.'
              '<span class="co-lei">Lei 9.029/1995</span>', total=f"{N:02d}")
    slides = [
        capa,
        claro(2, "01", "Quase <em>2 mil</em><br>denúncias em 2026",
              txt('O MPT recebeu 1.939 denúncias de assédio eleitoral no trabalho até o 2º turno, um recorde. '
                  '<span class="mt">No dia seguinte, mais 140</span>.') + selo("MPT, balanço de 26/10/2026")),
        escuro(3, "02", "Demitir pelo voto<br>é <em>discriminação</em>",
               txt('A lei proíbe dispensar alguém pela opinião política. <span class="mt">Não importa em quem você votou</span>.')
               + selo("Lei 9.029/1995, art. 1º; CF, art. 5º, VIII"), logo),
        claro(4, "03", "A escolha<br>é <em>sua</em>",
              txt('Voltar ao emprego com os salários do período <span class="mt">ou receber em dobro</span> a remuneração '
                  'desse tempo. E ainda pode caber dano moral.') + selo("Lei 9.029/1995, art. 4º")),
        foto_cartao(5, "04", "Ameaçar antes<br>do voto é <em>crime</em>",
                    'Coagir alguém a votar ou a não votar em um candidato tem pena de <span class="mt">até 4 anos de reclusão</span>.',
                    "Código Eleitoral, art. 301", v4.foto(v4.FOTOS / "10155095.jpg", foco=0.25)),
        claro(6, "05", "O que <em>conta</em><br>como prova",
              lista([("1", "Mensagens e <b>áudios</b> do chefe ou do RH"), ("2", "<b>Prints</b> do grupo da empresa"),
                     ("3", "<b>Posts</b> da empresa ou do chefe sobre o voto"), ("4", "<b>Carta de dispensa</b>, com a data"),
                     ("5", "Nomes de <b>testemunhas</b>")]), top=270, guarde=True),
        escuro(7, "06", "Guarde <em>do jeito</em><br><em>certo</em>",
               lista([("✓", "O print mostra <b>data, hora, quem mandou</b> e o nome do grupo"),
                      ("✓", "No WhatsApp, <b>Exportar conversa</b> com as mídias"),
                      ("✓", "<b>Baixe os áudios</b> e salve uma cópia no e-mail ou na nuvem"),
                      ("✓", "Tudo isso <b>antes de sair do grupo</b> ou devolver o celular da empresa")]), logo, top=270),
        claro(8, "07", "Gravar o chefe<br><em>vale</em>?",
              lista([("✓", "Gravar a conversa <b>da qual você participa</b> vale, mesmo sem o outro saber"),
                     ("✕", "Gravar conversa <b>de outras pessoas</b> não vale"),
                     ("✕", "<b>Não apague nem edite</b> nada"),
                     ("✓", "A denúncia ao <b>MPT</b> pode ser sigilosa")]) + selo("STF, RE 583.937 (Tema 237)"), top=270),
        capa_fecho.fecho(RETRATO, area=TAG, titulo="Seu voto <em>não é</em><br>motivo de demissão.", sub="Cada caso tem detalhes.",
                         apoio='<span class="mt">Salve este post</span> e mande para quem precisa saber disso.',
                         cta="Procure uma advogada de confiança", left=(N - 1) * 1080),
    ]
    ponte = v5.objetos_html(["nenhum", "ponte:7120126", "nenhum"])
    corpo = "\n".join(slides) + f"""
<div class="arco" style="left:1700px; top:860px; width:1150px; height:1150px;"></div>
<div class="arco" style="left:4950px; top:-620px; width:1000px; height:1000px;"></div>
<div class="arco" style="left:7150px; top:1150px; width:1000px; height:1000px;"></div>
{ponte}
<div class="fosco grao"></div><div class="fosco veu"></div>"""
    pagina = (f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=EB+Garamond:'
              f'ital,wght@0,500;0,600;0,700;0,800;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
              f'<style>{v5.CSS}{v5.EXTRA}{capa_fecho.CSS}{capa_fecho.CSS_OURO}{EXTRA9}</style></head><body><div class="pano">{corpo}</div></body></html>')
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
        destino = API / "_saida_producao_1510" / "pecas" / f"{CHAVE}-v9-{i + 1}.png"
        pano.crop((i * 2160, 0, (i + 1) * 2160, 2700)).resize((1080, 1350), Image.LANCZOS).save(destino)
        rc._aplicar_acabamento_dourado(str(destino))
        Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
        destino.unlink()
    print("ok", CHAVE, N)


if __name__ == "__main__":
    asyncio.run(main())
