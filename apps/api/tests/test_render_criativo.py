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


@pytest.mark.anyio
async def test_renderiza_card_de_pergunta_1080x1350(tmp_path):
    from app.services.render_criativo import renderizar_pergunta

    saida = tmp_path / "pergunta.png"
    await renderizar_pergunta(
        pergunta="Fui demitida grávida. E agora?",
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)


def test_pergunta_segue_o_padrao_aprovado_caixa_centralizada_sobre_foto():
    """Padrão aprovado em 09/10/2026 (pergunta v6): foto inteira de fundo, caixa de vidro
    centralizada com faixa "Me faça uma pergunta", destaque em itálico dourado, perfil no
    rodapé da caixa, área no cabeçalho e "A resposta está na legenda"."""
    from app.services.render_criativo import html_pergunta

    html = html_pergunta("Fui demitida grávida. <em>E agora?</em>", IDENTIDADE_VISUAL_TESTE,
                         area="Trabalhista", foto_src="data:image/jpeg;base64,AAA")

    assert "translate(-50%,-50%)" in html
    assert "Me faça uma pergunta" in html
    assert "<em>E agora?</em>" in html
    assert "adv.leticiabarros2" in html
    assert "Trabalhista" in html
    assert "A resposta está na" in html
    assert 'class="foto" src="data:image/jpeg;base64,AAA"' in html


def test_pergunta_sem_foto_usa_fundo_cafe_com_marca_dagua():
    from app.services.render_criativo import html_pergunta

    html = html_pergunta("Posso ser demitida?", IDENTIDADE_VISUAL_TESTE)

    assert 'class="foto"' not in html
    assert 'class="marca"' in html


@pytest.mark.anyio
async def test_renderiza_pergunta_com_foto(tmp_path):
    from app.services.render_criativo import renderizar_pergunta

    foto = tmp_path / "foto.jpg"
    Image.new("RGB", (800, 1200), "#6B4F35").save(foto)
    saida = tmp_path / "pergunta.png"
    await renderizar_pergunta("Tenho direito? <em>Pode?</em>", IDENTIDADE_VISUAL_TESTE, str(saida),
                              foto_path=str(foto), area="Consumidor")
    with Image.open(saida) as img:
        assert img.size == (1080, 1350)
