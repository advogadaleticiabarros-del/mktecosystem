"""Capa e fechamento de carrossel SEM recorte (pedido da Letícia, 09/10/2026).

- Capa: foto inteira de alguém ou algo ligado ao tema (nunca a Letícia), descendo da base
  e fundindo no café; título no alto, fora do rosto. Mesmo recurso aprovado na pergunta v6.
- Fechamento: único slide com a Letícia, foto inteira (sem fundo transparente), em rodízio
  entre os retratos de `_retratos/` para não repetir a mesma imagem nos carrosséis.

Os trechos usam as classes do CSS do carrossel v4 (`.s`, `.escuro`, `.cab`, `.rod`, `.cg`, `.mt`, `.btn`).
"""
import base64
import io
from pathlib import Path

from PIL import Image, ImageOps

AQUI = Path(__file__).resolve().parent
RETRATOS = AQUI / "_retratos"
# Ordem do rodízio: alterna escritório com logo, estúdio, janela, poltrona e a foto real.
ORDEM_RETRATOS = [
    "escritorio-logo-blusa-branca", "estudio-escuro-banco", "janela-cafe", "real-perfil", "poltrona-terno-cinza",
    "escritorio-logo-escrevendo", "estudio-claro-cadeira", "tablet-blazer-marrom", "escritorio-cafe-blazer-preto",
    "lendo-documentos", "escritorio-cafe-blazer-bege", "escritorio-documentos",
]
# Onde fica o rosto em cada retrato (object-position), para o enquadramento do fechamento.
FOCO = {"real-perfil": "50% 20%", "estudio-escuro-banco": "50% 12%", "poltrona-terno-cinza": "50% 10%", "estudio-livros": "50% 8%",
        "lendo-documentos": "50% 0%", "tablet-blazer-marrom": "50% 5%", "estudio-claro-cadeira": "50% 8%"}

CSS = """
.capa-foto { position:absolute; left:0; width:1080px; object-fit:cover; z-index:1;
  filter: sepia(.18) saturate(.85) contrast(1.05) brightness(.92);
  -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 30%); }
.capa-base { position:absolute; left:0; right:0; bottom:0; height:400px; z-index:2;
  background: linear-gradient(180deg, transparent, rgba(30,24,20,.82) 60%, rgba(30,24,20,.95)); }
.capa-txt { position:absolute; left:84px; right:84px; z-index:5; }
.fecho-foto { position:absolute; inset:0; width:1080px; height:1350px; object-fit:cover; z-index:1;
  filter: saturate(.92) contrast(1.03); }
.fecho-veu { position:absolute; inset:0; z-index:2;
  background: linear-gradient(180deg, rgba(30,24,20,.55) 0%, rgba(30,24,20,0) 16%, rgba(30,24,20,0) 40%, rgba(30,24,20,.82) 60%, rgba(30,24,20,.97) 76%); }
.fecho-txt { position:absolute; left:84px; right:84px; bottom:150px; z-index:5; }
"""


def foto_uri(caminho: Path, w: int = 1080, h: int = 1350, foco: tuple[float, float] = (0.5, 0.3)) -> str:
    img = ImageOps.fit(Image.open(caminho).convert("RGB"), (w, h), Image.LANCZOS, centering=foco)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def retrato(indice: int | str) -> tuple[str, str]:
    """(data URI, object-position) do retrato da vez no rodízio, ou de um retrato pelo nome."""
    nome = indice if isinstance(indice, str) else ORDEM_RETRATOS[indice % len(ORDEM_RETRATOS)]
    caminho = RETRATOS / f"{nome}.jpg"
    return "data:image/jpeg;base64," + base64.b64encode(caminho.read_bytes()).decode(), FOCO.get(nome, "50% 15%")


def capa(foto: str, *, area: str, linha1: str, titulo: str, linha3: str, apoio: str, total: str,
         desce: int = 330, posicao: str = "50% 30%", titulo_px: int = 104, left: int = 0) -> str:
    return f"""
<div class="s escuro textura" style="left:{left}px">
  <img class="capa-foto" src="{foto}" style="top:{desce}px; height:{1350 - desce}px; object-position:{posicao};">
  <div class="capa-base"></div>
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>{area}</span></div>
  <div class="capa-txt" style="top:170px;">
    <div class="cg" style="font-style:italic; font-size:52px; color:#E8DED1; line-height:1.08;">{linha1}</div>
    <div class="cg" id="big" style="font-size:{titulo_px}px; white-space:nowrap; font-weight:700; line-height:.95; color:#C9A962; margin-top:14px; text-shadow:0 8px 40px rgba(0,0,0,.5);">{titulo}</div>
    <div class="cg" style="font-style:italic; font-size:52px; color:#E8DED1; line-height:1.1; margin-top:14px;">{linha3}</div>
  </div>
  <div class="capa-txt" style="bottom:150px;">
    <div style="width:120px; height:2px; background:#C9A962; margin-bottom:24px;"></div>
    <div style="font-size:33px; line-height:1.45; color:#FAF6F0; max-width:820px; text-wrap:pretty;">{apoio}</div>
  </div>
  <div class="rod"><span>Arraste pro lado ›</span><span class="pg">01 / {total}</span></div>
</div>"""


def fecho(indice_retrato: int | str, *, area: str, titulo: str, sub: str, apoio: str, cta: str = "Procure uma advogada", left: int = 0) -> str:
    foto, posicao = retrato(indice_retrato)
    return f"""
<div class="s escuro textura" style="left:{left}px">
  <img class="fecho-foto" src="{foto}" style="object-position:{posicao};">
  <div class="fecho-veu"></div>
  <div class="cab"><span>Letícia Barros · Advocacia</span><span>{area}</span></div>
  <div class="fecho-txt">
    <div class="tit" style="font-size:78px; margin:0; color:#FAF6F0;">{titulo}</div>
    <div class="cg" style="font-style:italic; font-size:44px; color:#E8DED1; margin-top:18px; line-height:1.15;">{sub}</div>
    <div style="font-size:30px; line-height:1.45; color:#E8DED1; margin-top:26px; text-wrap:pretty;">{apoio}</div>
    <div style="margin-top:34px;"><span class="btn">{cta}</span></div>
  </div>
  <div class="rod"><span>@adv.leticiabarros2</span><span class="pg">OAB/ES 39.948</span></div>
</div>"""


# --------------------------------------------------------------------------- capa "Ouro editorial"
# PADRÃO APROVADO pela Letícia em 09/10/2026 (opção 1 de capas_opcoes.py): foto em tela cheia
# com tratamento de cinema, título em ouro metalizado embaixo à esquerda, moldura fina com
# cantoneiras, luz dourada e grão. A foto é enquadrada pelo rosto detectado (OpenCV) para a
# pessoa ficar à direita e nunca ser cortada de forma feia.

CSS_OURO = """
.co-ouro { background: linear-gradient(100deg,#8E6E2E 0%,#D9BC74 18%,#FFF1C7 32%,#E2C77F 44%,#B8943F 58%,#F4E2AE 74%,#9C7B3A 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  filter: drop-shadow(0 2px 0 rgba(58,40,14,.55)) drop-shadow(0 14px 34px rgba(0,0,0,.45)); }
.co-brilho { position:absolute; z-index:15; width:26px; height:26px; }
.co-brilho::before { content:''; position:absolute; inset:0; background:#FFF6DA;
  clip-path: polygon(50% 0, 58% 42%, 100% 50%, 58% 58%, 50% 100%, 42% 58%, 0 50%, 42% 42%);
  filter: drop-shadow(0 0 6px #FFE7A8) drop-shadow(0 0 14px #E9C878); }
.co-mt { background: linear-gradient(transparent 58%, rgba(201,169,98,.55) 58%); font-weight:700; }
.co-lei { display:inline-block; margin-left:10px; font-size:22px; font-weight:700; letter-spacing:1px; padding:6px 12px;
  border-radius:4px; background:#C9A962; color:#231E1A; vertical-align:middle; }
.co-grao { position:absolute; inset:0; z-index:40; pointer-events:none; opacity:.12; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.25' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>"); }
"""


def _rosto(im: Image.Image) -> tuple[float, float] | None:
    """Centro do maior rosto (fração da imagem), ou None se não houver rosto."""
    import cv2
    import numpy as np

    peq = im.copy()
    peq.thumbnail((900, 900))
    cinza = cv2.cvtColor(np.array(peq), cv2.COLOR_RGB2GRAY)
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    rostos = det.detectMultiScale(cinza, scaleFactor=1.08, minNeighbors=6, minSize=(40, 40))
    if len(rostos) == 0:
        return None
    x, y, w, h = max(rostos, key=lambda r: r[2] * r[3])
    return (x + w / 2) / peq.width, (y + h / 2) / peq.height


def enquadrar(caminho: Path, alvo_x: float = 0.64, alvo_y: float = 0.34, w: int = 1080, h: int = 1350,
              escala: int = 2, foco: tuple[float, float] | None = None) -> str:
    """Recorte w×h (em `escala`x) que põe o rosto em (alvo_x, alvo_y) do quadro, com o mínimo de zoom."""
    im = Image.open(caminho).convert("RGB")
    W, H = im.size
    fx, fy = foco or _rosto(im) or (0.5, 0.4)
    proporcao = w / h
    cw, ch = (W, W / proporcao) if W / H < proporcao else (H * proporcao, H)
    # zoom só o necessário para o rosto chegar à posição alvo na horizontal (máx. 1,35)
    zoom = 1.0
    while zoom < 1.35 and not (0 <= fx * W - alvo_x * cw / zoom <= W - cw / zoom):
        zoom += 0.01
    cw, ch = cw / zoom, ch / zoom
    x0 = min(max(fx * W - alvo_x * cw, 0), W - cw)
    y0 = min(max(fy * H - alvo_y * ch, 0), H - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w * escala, h * escala), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=93)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def capa_ouro(foto: str, *, area: str, kicker: str, titulo: str, subtitulo: str, apoio: str, total: str,
              left: int = 0) -> str:
    """Capa no padrão Ouro editorial. `titulo` pode ter <br>; o ajuste de largura fica a cargo do id="big" (620 px)."""
    cantos = "".join(
        f'<div style="position:absolute; {p} width:60px; height:60px; border-{a}:3px solid #E9D398; border-{b}:3px solid #E9D398; z-index:13;"></div>'
        for p, a, b in [("top:30px; left:30px;", "top", "left"), ("top:30px; right:30px;", "top", "right"),
                        ("bottom:30px; left:30px;", "bottom", "left"), ("bottom:30px; right:30px;", "bottom", "right")])
    return f"""
<div class="s" style="left:{left}px; background:#1A1511; overflow:hidden;">
  <img src="{foto}" style="position:absolute; inset:0; width:1080px; height:1350px; object-fit:cover; z-index:1; filter:sepia(.18) saturate(.9) contrast(1.08) brightness(.86);">
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(180deg, rgba(20,15,12,.7) 0%, rgba(20,15,12,0) 22%, rgba(20,15,12,0) 48%, rgba(20,15,12,.82) 72%, rgba(20,15,12,.95) 100%);"></div>
  <div style="position:absolute; inset:0; z-index:2; background:linear-gradient(90deg, rgba(20,15,12,.8) 0%, rgba(20,15,12,.35) 45%, rgba(20,15,12,0) 65%);"></div>
  <div style="position:absolute; inset:0; z-index:3; mix-blend-mode:screen; background:radial-gradient(ellipse at 92% 6%, rgba(255,214,140,.42), transparent 42%), radial-gradient(ellipse at 0% 100%, rgba(201,169,98,.25), transparent 45%);"></div>
  <div style="position:absolute; inset:38px; border:1.5px solid rgba(233,211,152,.55); border-radius:6px; z-index:12;"></div>
  {cantos}
  <div style="position:absolute; top:78px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20; font-size:22px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#F4EADB;">
    <span>Letícia Barros · Advocacia</span><span style="color:#E9D398">{area}</span></div>
  <div style="position:absolute; left:84px; bottom:170px; width:640px; z-index:20;">
    <div style="font-size:24px; font-weight:800; letter-spacing:5px; text-transform:uppercase; color:#E9D398; line-height:1.3;">{kicker}</div>
    <div class="cg co-ouro" id="big" style="display:inline-block; font-family:'EB Garamond',serif; font-size:150px; font-weight:800; line-height:.9; margin-top:16px; white-space:nowrap;">{titulo}</div>
    <div style="font-family:'EB Garamond',serif; font-style:italic; font-size:52px; font-weight:500; color:#FAF6F0; margin-top:14px; line-height:1.08; text-wrap:balance;">{subtitulo}</div>
    <div style="width:96px; height:2px; background:#E9D398; margin:28px 0 20px;"></div>
    <div style="font-size:30px; line-height:1.45; color:#FAF6F0; text-wrap:pretty;">{apoio}</div>
  </div>
  <div class="co-brilho" style="left:700px; bottom:560px;"></div><div class="co-brilho" style="left:650px; bottom:650px; transform:scale(.6)"></div>
  <div style="position:absolute; bottom:72px; left:84px; right:84px; display:flex; justify-content:space-between; z-index:20; font-size:22px; font-weight:600; color:#F4EADB;">
    <span>Arraste pro lado ›</span><span style="letter-spacing:3px">01 / {total}</span></div>
  <div class="co-grao"></div>
</div>"""
