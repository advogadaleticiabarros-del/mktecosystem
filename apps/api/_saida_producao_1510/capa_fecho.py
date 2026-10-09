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
