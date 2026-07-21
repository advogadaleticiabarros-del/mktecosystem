from datetime import date

import pytest
from PIL import Image

from app.services.render_artigo_blog import (
    estimar_tempo_leitura,
    renderizar_artigo_html,
    renderizar_capa_artigo,
)

IDENTIDADE_VISUAL_TESTE = {
    "cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"},
}


def test_estima_tempo_leitura_por_contagem_de_palavras():
    html = "<p>" + ("palavra " * 400) + "</p>"
    assert estimar_tempo_leitura(html) == 2


def test_estima_tempo_leitura_minimo_de_1_minuto():
    assert estimar_tempo_leitura("<p>texto curto</p>") == 1


def test_renderiza_html_do_artigo_com_campos_principais():
    html = renderizar_artigo_html(
        titulo="Carga horária máxima CLT",
        meta_description="Descrição para SEO",
        categoria="Trabalhista",
        resumo="Resumo curto",
        corpo_html="<p>Conteúdo do artigo</p>",
        slug="carga-horaria-maxima-clt",
        data_publicacao=date(2026, 7, 21),
    )
    assert "Carga horária máxima CLT" in html
    assert "Descrição para SEO" in html
    assert "Trabalhista" in html
    assert "Conteúdo do artigo" in html
    assert "carga-horaria-maxima-clt.html" in html
    assert "21 de julho de 2026" in html
    assert (
        '<meta property="og:image" '
        'content="https://advogadaleticiabarros.com.br/blog/capas/carga-horaria-maxima-clt.png">'
        in html
    )


def test_renderiza_html_escapa_titulo_com_caracteres_especiais():
    html = renderizar_artigo_html(
        titulo='Título <script>alert("x")</script> "perigoso"',
        meta_description="Descrição para SEO",
        categoria="Trabalhista",
        resumo="Resumo curto",
        corpo_html="<p>Conteúdo do artigo</p>",
        slug="titulo-perigoso",
        data_publicacao=date(2026, 7, 21),
    )
    assert "<script>alert(" not in html
    assert "&lt;script&gt;" in html
    # o corpo do artigo continua renderizado como HTML confiável (|safe)
    assert "<p>Conteúdo do artigo</p>" in html


@pytest.mark.anyio
async def test_renderiza_capa_1200x630(tmp_path):
    saida = tmp_path / "capa.png"
    await renderizar_capa_artigo(
        titulo="Carga horária máxima CLT",
        categoria="Trabalhista",
        identidade_visual=IDENTIDADE_VISUAL_TESTE,
        caminho_saida=str(saida),
    )
    assert saida.exists()
    with Image.open(saida) as img:
        assert img.size == (1200, 630)
