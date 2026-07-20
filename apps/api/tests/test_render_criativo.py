import pytest
from PIL import Image

from app.services.render_criativo import renderizar_slide

IDENTIDADE_VISUAL_TESTE = {
    "cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"},
}


@pytest.mark.anyio
async def test_renderiza_slide_1080x1350(tmp_path):
    saida = tmp_path / "slide-1.png"
    await renderizar_slide(
        texto="Direitos da gestante no trabalho",
        indice=0,
        total=5,
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    assert saida.exists()
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)
