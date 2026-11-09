"""Capas dos Reels Flagrante (1080×1920), feitas para a grade: o Instagram mostra o recorte central 1080×1440,
então faixas douradas, tema, fala e pergunta ficam entre y=240 e y=1680. Papel claro, como os estáticos Manchete.
Uso: python capas.py [prefixo ...]  → <episódio>/capa.jpg (arquivo novo; não toca nos vídeos)."""
import asyncio
import html
import importlib.util
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

sys.path.insert(0, r"C:\Users\prosy\mktecosystem\producao\estilos\palavra-de-ouro")
from base import FOIL, LOGO, MARCA, ruido  # noqa: E402

AQUI = Path(__file__).resolve().parent


# Tema curto, para ler na grade de relance (a docstring do episódio tem anotações internas).
TEMAS = {
    "01-atestado": "Atestado recusado", "02-holerite": "Holerite", "03-ponto": "Ponto", "04-demissao": "Pedido de demissão",
    "05-ferias": "Vender as férias", "06-almoco": "Almoço de 20 minutos", "07-experiencia": "Experiência sem fim",
    "08-por-fora": "Salário por fora", "09-sem-carteira": "Sem carteira", "10-salario-atrasado": "Salário atrasado",
    "11-fgts": "FGTS não depositado", "12-sem-folga": "Sem folga", "13-aviso-previo": "Aviso prévio",
    "14-banheiro": "Desvio de função", "15-pensao": "Pensão atrasada", "16-guarda": "Guarda compartilhada",
    "17-ferias-natal": "Natal com pais separados", "18-decimo-terceiro": "13º salário", "19-temporario": "Trabalho temporário",
    "20-pausa-banheiro": "Pausa para o banheiro", "21-licenca-180": "Licença-maternidade", "22-fim-6x1": "Fim da escala 6x1",
    "23-gestante": "Gestante dispensada", "24-assinou": "Gestante e pedido de demissão", "25-cabelo": "Cabelo no trabalho",
    "26-amigo-secreto": "Amigo secreto da firma", "27-preco": "Preço diferente no caixa", "28-estacionamento": "Furto no estacionamento",
    "29-revista": "Revista íntima", "30-exame": "Exame preventivo", "31-story": "Story no dia do atestado",
    "32-avo": "Pensão paga pela avó", "33-doar-sangue": "Doação de sangue",
}


def dados(arquivo):
    """Tema (docstring), fala de quem pressiona (último balão de fora) e pergunta (marca-texto) do episódio."""
    spec = importlib.util.spec_from_file_location(arquivo.stem, arquivo)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ep, doc = mod.EP, (mod.__doc__ or "")
    tema = re.split(r"\s*[·.]\s*", doc.split("·", 1)[-1].strip(), maxsplit=1)[0] if "·" in doc else ep["nome"]
    texto = lambda h: html.unescape(re.sub(r"<small>.*?</small>|<[^>]+>", " ", h)).split()
    pergunta = " ".join(texto(re.search(r"class=marca[^>]*>(.*?)</div>", ep["html"], re.S).group(1)))
    falas = [" ".join(texto(m)) for m in re.findall(r'class="bo ele"[^>]*>(.*?)</div>', ep["html"], re.S)]
    if not falas:  # episódios de notificação: a mensagem do cartão (chefe, gerente, banco)
        falas = [" ".join(texto(m)) for m in re.findall(r"<div class=m>(.*?)</div>", ep["html"], re.S)]
    tema = TEMAS.get(ep["nome"], tema)
    return {"nome": ep["nome"], "tema": tema, "fala": max(falas[-2:], key=len) if falas else "", "pergunta": pergunta}


def pagina(d):
    grao = ruido(".95", ".25", ".9")
    return f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,400&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:#EFE6D9}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#EFE6D9;color:#1E1814;font-family:Inter,sans-serif}}
#c::before{{content:"";position:absolute;inset:0;background:url("{grao}");mix-blend-mode:multiply;opacity:.08}}
.fx{{position:absolute;left:0;right:0;height:14px;background:{FOIL}}}
.cab{{position:absolute;left:72px;right:72px;top:290px;display:flex;justify-content:space-between;font:500 24px Inter;letter-spacing:.12em;text-transform:uppercase}}
.tema{{position:absolute;left:72px;right:72px;top:420px;font:600 30px Inter;letter-spacing:.14em;text-transform:uppercase;color:#8A6420}}
.fala{{position:absolute;left:72px;max-width:936px;top:500px;background:#2B2520;color:#EFE6D9;border-radius:30px 30px 30px 8px;padding:34px 40px;font:400 54px/1.25 Inter;box-shadow:0 18px 40px rgb(30 24 20/.18)}}
.perg{{position:absolute;left:0;right:0;top:880px;text-align:center}}
.perg span{{display:inline-block;max-width:980px;padding:10px 34px 22px;font:italic 400 150px/1.05 'EB Garamond',serif;background:{MARCA};-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.ver{{position:absolute;left:0;right:0;top:1520px;display:flex;justify-content:center;align-items:center;gap:16px;font:600 26px Inter;letter-spacing:.14em;text-transform:uppercase}}
.ver b{{width:54px;height:54px;border-radius:50%;background:#1E1814;display:grid;place-items:center}}
.ver b::after{{content:"";border-left:18px solid #E8D08A;border-top:11px solid transparent;border-bottom:11px solid transparent;margin-left:5px}}
.ass{{position:absolute;left:72px;bottom:290px;display:flex;align-items:center;gap:14px;font:500 24px Inter}}
.ass img{{width:44px;height:44px}}
</style></head><body><div id=c>
<div class=fx style="top:240px"></div><div class=fx style="top:1666px"></div>
<div class=cab><span>Letícia Barros</span><span>Direito do Trabalho</span></div>
<div class=tema>{html.escape(d["tema"])}</div>
{f'<div class=fala>“{html.escape(d["fala"])}”</div>' if d["fala"] else ""}
<div class=perg><span>{html.escape(d["pergunta"])}</span></div>
<div class=ver><b></b>Assista e comente</div>
<div class=ass><img src="{LOGO}">Letícia Barros · OAB/ES 39.948</div>
</div><script>document.fonts.ready.then(()=>{{
 // tema, fala e pergunta formam um bloco centrado na área que aparece na grade (y 340 a 1480)
 const tm=document.querySelector('.tema'),p=document.querySelector('.perg'),f=document.querySelector('.fala');
 const alt=tm.offsetHeight+40+(f?f.offsetHeight+80:0)+p.offsetHeight, topo=340+(1140-alt)/2;
 tm.style.top=topo+'px'; let y=topo+tm.offsetHeight+40;
 if(f){f.style.top=y+'px';y+=f.offsetHeight+80} p.style.top=y+'px';
 document.body.dataset.ok=1}})</script></body></html>"""


async def main():
    so = sys.argv[1:]
    eps = sorted(p for p in AQUI.glob("[0-9][0-9]_*.py") if not so or any(p.stem.startswith(s) for s in so))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for arq in eps:
            d = dados(arq)
            await pg.set_content(pagina(d), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            destino = AQUI / d["nome"] / "capa.jpg"
            destino.parent.mkdir(exist_ok=True)
            await pg.screenshot(path=str(destino), type="jpeg", quality=92)
            print(d["nome"], "|", d["tema"], "|", d["fala"], "|", d["pergunta"])
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
