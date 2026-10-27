"""Stories "Demissão pelo voto?" (assédio eleitoral), 8 telas 1080×1920, 27/10/2026. Foco: ensinar a juntar provas.

Tela 1 no padrão da capa Ouro editorial (mesmo do Story "Leia no link" de producao_out.py); telas 2 a 8 tipográficas
no café/dourado. Área segura: nada crítico fora de y 250–1670. Tela 2 tem espaço para a enquete; tela 8, para o
adesivo de link.

Fatos (conferidos em 27/10/2026, ver ../BRIEFING.md): MPT 1.939 denúncias até 25/10 e 140 em 26/10; Lei 9.029/1995,
arts. 1º e 4º; STF, RE 583.937, Tema 237 (gravação feita por um dos interlocutores, sem o outro saber, é prova lícita);
Código Eleitoral, art. 301; denúncia sigilosa no site do MPT.

Uso (de apps/api): python ../../producao/campanhas/2026-10-assedio-eleitoral/carrossel-stories/stories.py
Saída: apps/api/_saida_producao_1510/pecas/story-assedio-eleitoral-1..8.jpg
"""
import asyncio
import sys
from pathlib import Path

API = Path(__file__).resolve().parents[4] / "apps" / "api"
sys.path.insert(0, str(API))
sys.path.insert(0, str(API / "_saida_producao_1510"))

import capa_fecho  # noqa: E402
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from app.services import render_criativo as rc  # noqa: E402

AQUI = API / "_saida_producao_1510"
PECAS = AQUI / "pecas"
TOTAL = 8

FONTES = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;0,800;1,500;1,600'
          '&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

CSS = """*{margin:0;padding:0;box-sizing:border-box} body{width:1080px;height:1920px;font-family:Inter,sans-serif;font-variant-numeric:lining-nums}
.tela{position:relative;width:1080px;height:1920px;overflow:hidden;background:#1A1511}
.fundo{position:absolute;inset:0;z-index:1;background:radial-gradient(ellipse at 88% 8%,rgba(201,169,98,.22),transparent 45%),
  radial-gradient(ellipse at 0% 100%,rgba(201,169,98,.14),transparent 50%),linear-gradient(180deg,#231E1A,#1A1511 60%,#15110E)}
.moldura{position:absolute;top:208px;bottom:208px;left:38px;right:38px;border:1.5px solid rgba(233,211,152,.45);border-radius:6px;z-index:12}
.cab{position:absolute;top:262px;left:84px;right:84px;display:flex;justify-content:space-between;z-index:20;font-size:22px;font-weight:700;
  letter-spacing:5px;text-transform:uppercase;color:#F4EADB}
.cab span:last-child{color:#E9D398}
.marca{position:absolute;right:40px;top:300px;z-index:2;font-family:'EB Garamond',serif;font-weight:700;font-size:520px;line-height:1;color:rgba(201,169,98,.07)}
.miolo{position:absolute;left:84px;right:84px;top:340px;bottom:340px;z-index:20;display:flex;flex-direction:column;justify-content:center}
.kick{font-size:28px;font-weight:800;letter-spacing:5px;text-transform:uppercase;color:#E9D398}
.tit{font-family:'EB Garamond',serif;font-weight:700;font-size:108px;line-height:1.0;color:#FAF6F0;margin-top:24px;text-wrap:balance}
.tit em{font-style:italic;font-weight:600;color:#E9C878}
.txt{font-size:46px;line-height:1.45;color:#EFE6D8;margin-top:44px;text-wrap:pretty}
.mt{background:linear-gradient(transparent 58%,rgba(201,169,98,.5) 58%);font-weight:700;color:#FFF}
.lista{margin-top:52px;display:flex;flex-direction:column;gap:38px}
.item{display:flex;gap:28px;align-items:flex-start;font-size:44px;line-height:1.38;color:#EFE6D8}
.item b{color:#FFF}
.ic{flex:0 0 58px;height:58px;border-radius:50%;border:2.5px solid #C9A962;color:#E9D398;display:flex;align-items:center;justify-content:center;
  font-size:26px;font-weight:800;margin-top:2px}
.pil{align-self:flex-start;margin-top:52px;font-size:26px;font-weight:700;letter-spacing:1px;padding:10px 18px;border-radius:5px;background:#C9A962;color:#231E1A}
.rod{position:absolute;bottom:262px;left:84px;right:84px;display:flex;justify-content:space-between;z-index:20;font-size:24px;font-weight:600;color:#E8DED1}
.rod .pg{letter-spacing:3px;color:#E9D398}
.vazio{margin-top:56px;height:300px;border-radius:24px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:18px;
  font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:rgba(233,211,152,.0)}
"""


def cantos(top: int = 200, bottom: int = 200) -> str:
    return "".join(
        f'<div style="position:absolute; {p} width:60px; height:60px; border-{x}:3px solid #E9D398; border-{y}:3px solid #E9D398; z-index:13;"></div>'
        for p, x, y in [(f"top:{top}px; left:30px;", "top", "left"), (f"top:{top}px; right:30px;", "top", "right"),
                        (f"bottom:{bottom}px; left:30px;", "bottom", "left"), (f"bottom:{bottom}px; right:30px;", "bottom", "right")])


def pagina(corpo: str) -> str:
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}<style>{CSS}{capa_fecho.CSS_OURO}</style></head><body>{corpo}</body></html>'


def tela_capa() -> str:
    foto = capa_fecho.enquadrar(AQUI / "_fotos_pexels" / "original-assedio-eleitoral-voto.jpg", alvo_x=0.55, alvo_y=0.2,
                                w=1080, h=1920, escala=1)
    return pagina(f"""
<div class="tela">
  <img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; z-index:1; filter:sepia(.18) saturate(.9) contrast(1.08) brightness(.86);">
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(180deg, rgba(20,15,12,.85) 0%, rgba(20,15,12,.5) 14%, rgba(20,15,12,0) 24%, rgba(20,15,12,.15) 30%, rgba(20,15,12,.8) 40%, rgba(20,15,12,.95) 52%, rgba(20,15,12,.98) 100%);"></div>
  <div style="position:absolute; inset:0; z-index:3; mix-blend-mode:screen; background:radial-gradient(ellipse at 92% 12%, rgba(255,214,140,.42), transparent 40%), radial-gradient(ellipse at 0% 88%, rgba(201,169,98,.25), transparent 45%);"></div>
  <div class="moldura" style="border-color:rgba(233,211,152,.55)"></div>{cantos()}
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Assédio eleitoral</span></div>
  <div style="position:absolute; left:84px; right:84px; bottom:470px; z-index:20;">
    <div class="kick">Assédio eleitoral no trabalho</div>
    <div class="co-ouro" id="big" style="display:inline-block; font-family:'EB Garamond',serif; font-size:170px; font-weight:800; line-height:.92; margin-top:20px; white-space:nowrap;">Demissão<br>pelo voto?</div>
    <div style="font-family:'EB Garamond',serif; font-style:italic; font-size:60px; font-weight:500; color:#FAF6F0; margin-top:18px; line-height:1.08; text-wrap:balance;">Isso tem nome na lei. E a prova faz toda a diferença.</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:30px 0 22px;"></div>
    <div style="font-size:36px; line-height:1.45; color:#FAF6F0;">Veja o que a lei garante e como guardar as provas. <span class="co-lei" style="font-size:24px">Lei 9.029/1995</span></div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:330px; text-align:center; z-index:20; font-size:28px; font-weight:800; letter-spacing:4px; text-transform:uppercase; color:#E9D398;">Toque para ver o passo a passo ›</div>
  <div class="co-brilho" style="right:150px; bottom:1180px;"></div><div class="co-brilho" style="right:210px; bottom:1270px; transform:scale(.6)"></div>
  <div class="co-grao"></div>
</div>""")


def tela(n: int, kicker: str, titulo: str, miolo: str, rodape: str = "Toque para continuar ›") -> str:
    return pagina(f"""
<div class="tela">
  <div class="fundo"></div>
  <div class="marca">0{n}</div>
  <div class="moldura"></div>{cantos()}
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>Assédio eleitoral</span></div>
  <div class="miolo">
    <div class="kick">{kicker}</div>
    <div class="tit">{titulo}</div>
    {miolo}
  </div>
  <div class="rod"><span>{rodape}</span><span class="pg">0{n} / 0{TOTAL}</span></div>
  <div class="co-grao"></div>
</div>""")


def itens(lista: list[tuple[str, str]]) -> str:
    return '<div class="lista">' + "".join(f'<div class="item"><div class="ic">{i}</div><div>{t}</div></div>' for i, t in lista) + "</div>"


V = "✓"

TELAS = [
    tela_capa(),
    tela(2, "Os números", "Quase <em>2 mil</em> denúncias",
         '<div class="txt">O Ministério Público do Trabalho recebeu <span class="mt">1.939 denúncias</span> de assédio eleitoral '
         'até o 2º turno, um recorde. No dia seguinte à eleição, foram <span class="mt">mais 140 em um único dia</span>.</div>'
         '<div class="pil">MPT, balanço de 26/10/2026</div>'
         '<div class="txt" style="margin-top:70px; font-family:\'EB Garamond\',serif; font-style:italic; font-size:52px; color:#E9D398;">'
         'Você já viu isso acontecer?</div><div style="height:260px"></div>'),
    tela(3, "O que a lei garante", "Demitir pelo voto é <em>discriminação</em>",
         itens([(V, '<b>Não importa em quem você votou.</b> A opinião política não pode ser motivo de demissão.'),
                (V, 'Você escolhe: <b>voltar ao emprego</b> com os salários do período <b>ou receber em dobro</b> a remuneração desse tempo.'),
                (V, 'E ainda pode caber <b>indenização por dano moral</b>.')])
         + '<div class="pil">Lei 9.029/1995, arts. 1º e 4º</div>'),
    tela(4, "Junte as provas", "O que <em>conta</em> como prova",
         itens([("1", "Mensagens e <b>áudios</b> do chefe ou do RH"),
                ("2", "<b>Prints</b> do grupo da empresa"),
                ("3", "<b>Posts</b> da empresa ou do chefe sobre o voto"),
                ("4", "<b>Carta de dispensa</b>, com a data"),
                ("5", "Nomes e contatos de <b>testemunhas</b>")])),
    tela(5, "Como guardar", "Guarde <em>do jeito certo</em>",
         itens([(V, "O print precisa mostrar <b>data, hora, quem mandou</b> e o nome do grupo."),
                (V, "No WhatsApp, use <b>Exportar conversa</b> (no menu da conversa) e inclua as mídias."),
                (V, "<b>Baixe os áudios</b> e salve uma cópia no e-mail ou na nuvem."),
                (V, "Faça isso <b>antes de sair do grupo</b> ou de devolver o celular da empresa.")])),
    tela(6, "Gravação vale?", "Pode <em>gravar</em> o chefe?",
         itens([(V, "Gravar a conversa <b>da qual você participa</b> vale como prova, mesmo sem o outro saber."),
                ("✕", "Gravar conversa <b>de outras pessoas</b>, sem você participar, não vale."),
                ("✕", "<b>Não apague nem edite</b> nada: prova cortada perde força.")])
         + '<div class="pil">STF, RE 583.937 (Tema 237)</div>'),
    tela(7, "Onde denunciar", "Denuncie <em>em sigilo</em>",
         itens([(V, 'No site do <b>MPT</b> (mpt.mp.br), em "Denuncie". Você pode pedir sigilo.'),
                (V, "O <b>sindicato</b> da sua categoria também recebe a denúncia."),
                (V, "Ameaçar alguém para votar ou não votar em um candidato é <b>crime</b>.")])
         + '<div class="pil">Código Eleitoral, art. 301</div>'),
    tela(8, "Passo a passo completo", "Tudo explicado <em>no link</em>",
         '<div class="txt">Provas, prazos e o que fazer agora, com calma e em linguagem simples.</div>'
         '<div style="margin-top:60px; text-align:center; font-size:30px; font-weight:800; letter-spacing:4px; text-transform:uppercase; color:#E9D398;">Toque no link abaixo ↓</div>'
         '<div style="margin-top:300px; font-size:34px; line-height:1.45; color:#E8DED1; text-align:center;">'
         'Cada caso tem detalhes.<br>Procure uma advogada de confiança.</div>',
         rodape="@adv.leticiabarros2 · OAB/ES 39.948"),
]


async def main() -> None:
    PECAS.mkdir(exist_ok=True)
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={"width": 1080, "height": 1920})
        for i, html in enumerate(TELAS, 1):
            await pg.set_content(html, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.evaluate("() => { const b = document.getElementById('big'); if (!b) return; let s = 170;"
                              " while (b.getBoundingClientRect().width > 900 && s > 90) { s -= 4; b.style.fontSize = s + 'px'; } }")
            await pg.wait_for_timeout(200)
            destino = PECAS / f"story-assedio-eleitoral-{i}.png"
            await pg.screenshot(path=str(destino))
            rc._aplicar_acabamento_dourado(str(destino))
            Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=90)
            print("ok", destino.with_suffix(".jpg").name)
        await nav.close()


if __name__ == "__main__":
    asyncio.run(main())
