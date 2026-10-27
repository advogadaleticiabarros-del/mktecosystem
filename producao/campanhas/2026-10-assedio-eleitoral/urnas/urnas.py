"""Fotos reais da urna eletrônica brasileira para a campanha "demissão pelo voto" (pedido de 27/10/2026: "Todos
inclua fotos das urnas brasileiras").

Fotos do Wikimedia Commons com licença que permite uso com crédito (créditos em creditos.json). Ficaram de fora as
CC BY-SA (obrigariam a arte a sair com a mesma licença) e as fotos com camisas verde e amarela (leitura política).
Nenhuma mostra candidato, número ou partido na tela.
"""
import base64
import io
from pathlib import Path

from PIL import Image, ImageEnhance

API = Path(__file__).resolve().parents[4] / "apps" / "api"
FOTOS = API / "_saida_producao_1510" / "_fotos_pexels"

# arquivo, foco (x, y) do objeto principal, crédito curto para a arte
URNAS = {
    "teclado": ("urna-mao-teclado.jpg", (0.60, 0.50), "Foto: Marri Nogueira/Agência Senado (CC BY 2.0)"),
    "confirma": ("urna-confirma.jpg", (0.72, 0.50), "Foto: Alejandro Zambrana/TSE"),
    "luz": ("urna-presidente-luz.jpg", (0.42, 0.62), "Foto: Antonio Cruz/Agência Brasil (CC BY 3.0 BR)"),
    "ue2020": ("urna-ue2020-tse.jpg", (0.50, 0.60), "Foto: Antonio Augusto/TSE"),
}


def recorte(chave: str, w: int, h: int, foco: tuple[float, float] | None = None, zoom: float = 1.0,
            brilho: float = 1.0) -> str:
    """Maior recorte w:h possível centrado no objeto (com `zoom` opcional), como data URI JPEG em w×h."""
    arquivo, foco_padrao, _ = URNAS[chave]
    im = Image.open(FOTOS / arquivo).convert("RGB")
    W, H = im.size
    fx, fy = foco or foco_padrao
    proporcao = w / h
    cw, ch = (W, W / proporcao) if W / H < proporcao else (H * proporcao, H)
    cw, ch = cw / zoom, ch / zoom
    x0 = min(max(fx * W - cw / 2, 0), W - cw)
    y0 = min(max(fy * H - ch / 2, 0), H - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)
    if brilho != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brilho)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def credito(chave: str) -> str:
    return URNAS[chave][2]
