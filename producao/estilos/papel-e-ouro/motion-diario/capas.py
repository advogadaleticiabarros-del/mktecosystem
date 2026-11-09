"""Capas dos Reels Flagrante (1080×1920), feitas para a grade: o Instagram mostra o recorte central 1080×1440,
então faixas douradas, tema, fala e pergunta ficam entre y=240 e y=1680. Papel claro, como os estáticos Manchete.
Uso: python capas.py [--clara|--cafe|--dividida|--textura|--cena] [prefixo ...]  → <episódio>/capa-<estilo>.jpg (não toca nos vídeos)."""
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


ESTILOS = {
    # fundo, texto, cor do tema, balão (fundo, texto), parte de cima (só na dividida)
    "clara": dict(fundo="#EFE6D9", cor="#1E1814", tema="#8A6420", balao=("#2B2520", "#EFE6D9"), grao=("multiply", ".08", ".25")),
    "cafe": dict(fundo="#231E1A", cor="#EFE6D9", tema="#C9A962", balao=("#EFE6D9", "#1E1814"), grao=("screen", ".04", ".9")),
    "textura": dict(fundo="#231E1A", cor="#EFE6D9", tema="#C9A962", balao=("#EFE6D9", "#1E1814"), grao=("overlay", ".5", ".9"),
                    luz="radial-gradient(ellipse 70% 45% at 75% 30%,rgb(201 169 98/.28),transparent 70%),radial-gradient(ellipse 60% 40% at 15% 85%,rgb(201 169 98/.16),transparent 70%)"),
    "cena": dict(fundo="#231E1A", cor="#EFE6D9", tema="#C9A962", balao=("#EFE6D9", "#1E1814"), grao=("screen", ".04", ".9"),
                 luz="linear-gradient(#231E1A 0 19%,rgb(35 30 26/.55) 30%,rgb(35 30 26/.2) 50%,rgb(35 30 26/.55) 70%,#231E1A 84%)"),
    "dividida": dict(fundo="#EFE6D9", cor="#1E1814", tema="#C9A962", balao=("#EFE6D9", "#1E1814"), grao=("multiply", ".08", ".25"), topo="#231E1A"),
}
EIXO = 96  # todo o texto começa nesta margem: tema, fala, pergunta e rodapé


def pagina(d, estilo="clara", fundo_img=None):
    e = ESTILOS[estilo]
    grao = ruido(".95", e["grao"][2], ".9")
    topo = e.get("topo")
    # Na dividida, tema e fala ficam no café (alto) e a pergunta no papel (baixo); a divisão segue a fala.
    return f"""<!doctype html><html lang=pt-BR><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,400&family=Inter:wght@400;500;600&display=swap" rel=stylesheet>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:{e["fundo"]}}}
#c{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{e["fundo"]};color:{e["cor"]};font-family:Inter,sans-serif}}
#topo{{position:absolute;left:0;right:0;top:0;height:0;background:{topo or "transparent"}}}
#img{{position:absolute;inset:-60px;background:{f'url({fundo_img}) center/cover' if fundo_img else 'none'};filter:blur(14px) brightness(.55) saturate(.7)}}
#luz{{position:absolute;inset:0;background:{e.get("luz", "none")}}}
#c::after{{content:"";position:absolute;inset:0;background:url("{grao}");mix-blend-mode:{e["grao"][0]};opacity:{e["grao"][1]};pointer-events:none}}
.fx{{position:absolute;left:0;right:0;height:14px;background:{FOIL};z-index:2}}
.cab,.rod{{position:absolute;left:{EIXO}px;right:{EIXO}px;display:flex;justify-content:space-between;align-items:center;font:500 24px Inter}}
.cab{{top:290px;letter-spacing:.12em;text-transform:uppercase;color:{topo and "#EFE6D9" or e["cor"]}}}
.rod{{bottom:290px}}
.rod .ass{{display:flex;align-items:center;gap:14px}}
.rod img{{width:44px;height:44px}}
.ver{{display:flex;align-items:center;gap:14px;font:600 22px Inter;letter-spacing:.14em;text-transform:uppercase}}
.ver b{{width:46px;height:46px;border-radius:50%;background:{FOIL};display:grid;place-items:center}}
.ver b::after{{content:"";border-left:15px solid #1E1814;border-top:9px solid transparent;border-bottom:9px solid transparent;margin-left:4px}}
.tema{{position:absolute;left:{EIXO}px;right:{EIXO}px;font:600 30px Inter;letter-spacing:.14em;text-transform:uppercase;color:{e["tema"]}}}
.tema::after{{content:"";display:block;width:120px;height:3px;background:{FOIL};margin-top:22px}}
.fala{{position:absolute;left:{EIXO}px;max-width:{1080-2*EIXO}px;text-wrap:balance;background:{e["balao"][0]};color:{e["balao"][1]};border-radius:30px 30px 30px 8px;padding:32px 40px;font:400 52px/1.25 Inter;box-shadow:0 18px 40px rgb(0 0 0/.22)}}
.perg{{position:absolute;left:{EIXO - 26}px;right:{EIXO - 26}px}}
.perg span{{display:inline;padding:4px 26px 14px;font:italic 400 150px/1.18 'EB Garamond',serif;color:#1E1814;background:{MARCA};-webkit-box-decoration-break:clone;box-decoration-break:clone}}
</style></head><body><div id=c>
<div id=img></div><div id=luz></div><div id=topo></div>
<div class=fx style="top:240px"></div><div class=fx style="top:1666px"></div>
<div class=cab><span>Letícia Barros</span><span>Direito do Trabalho</span></div>
<div class=tema>{html.escape(d["tema"])}</div>
{f'<div class=fala>“{html.escape(d["fala"])}”</div>' if d["fala"] else ""}
<div class=perg><span>{html.escape(d["pergunta"])}</span></div>
<div class=rod><span class=ass><img src="{LOGO}">Letícia Barros · OAB/ES 39.948</span><span class=ver><b></b>Assista</span></div>
</div><script>document.fonts.ready.then(()=>{{
 // a pergunta encolhe até caber entre as margens (o marca-texto avança 26 px de cada lado)
 const sp=document.querySelector('.perg span');
 const lim=1080-2*(96-26)+1, cabe=()=>[...sp.getClientRects()].every(q=>q.width<=lim);
 let s=150; for(;s>=104;s-=4){{sp.style.fontSize=s+'px';if(sp.getClientRects().length===1&&cabe())break}}
 if(s<104){{document.querySelector('.perg').style.textWrap='balance';for(s=150;s>84;s-=4){{sp.style.fontSize=s+'px';if(sp.getClientRects().length<=2&&cabe())break}}}}
 // tema, fala e pergunta formam um bloco centrado entre o cabeçalho e o rodapé da área da grade
 const tm=document.querySelector('.tema'),p=document.querySelector('.perg'),f=document.querySelector('.fala');
 const alt=tm.offsetHeight+56+(f?f.offsetHeight+96:0)+p.offsetHeight, topo=360+(1180-alt)/2;
 tm.style.top=topo+'px'; let y=topo+tm.offsetHeight+56;
 if(f){{f.style.top=y+'px';y+=f.offsetHeight+96}} p.style.top=y+'px';
 const t=document.getElementById('topo'); if({'true' if topo else 'false'}) t.style.height=(f?y-48:topo+tm.offsetHeight+28)+'px';
 document.body.dataset.ok=1}})</script></body></html>"""


def quadro(pasta):
    """Quadro do clímax do próprio Reels (70% da duração), para a variação cena."""
    import base64, subprocess
    video = max(pasta.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout)
    jpg = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{dur * .7:.2f}", "-i", str(video), "-frames:v", "1",
                          "-vf", "scale=540:-1", "-f", "image2", "-c:v", "mjpeg", "-"], capture_output=True).stdout
    return "data:image/jpeg;base64," + base64.b64encode(jpg).decode()


async def main():
    args = sys.argv[1:]
    estilo = args.pop(0)[2:] if args and args[0].startswith("--") else "clara"
    so = args
    eps = sorted(p for p in AQUI.glob("[0-9][0-9]_*.py") if not so or any(p.stem.startswith(s) for s in so))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for arq in eps:
            d = dados(arq)
            fundo_img = quadro(arq.parent / d["nome"]) if estilo == "cena" else None
            await pg.set_content(pagina(d, estilo, fundo_img), wait_until="networkidle")
            await pg.wait_for_selector("body[data-ok]", state="attached")
            destino = AQUI / d["nome"] / f"capa-{estilo}.jpg"
            await pg.screenshot(path=str(destino), type="jpeg", quality=92)
            print(d["nome"], estilo)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
