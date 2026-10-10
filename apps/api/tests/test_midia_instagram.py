import pytest

from app.models.content_piece import ContentPiece
from app.services.midia_instagram import PecaSemConteudo, montar_midia, publicavel
from tests.fakes import RenderizadorFalso


def _piece(tipo: str, corpo: dict) -> ContentPiece:
    return ContentPiece(tipo=tipo, corpo=corpo, status="aprovado", versao=1)


async def _montar(piece, tmp_path, renderizador=None):
    return await montar_midia(
        piece,
        identidade_visual={},
        pasta=tmp_path,
        base_url="https://api.exemplo/media",
        prefixo="ag1",
        renderizador=renderizador or RenderizadorFalso(),
    )


@pytest.mark.anyio
async def test_carrossel_vira_uma_imagem_por_slide_com_legenda(tmp_path):
    render = RenderizadorFalso()
    piece = _piece("carrossel", {"slides": ["capa", "meio", "fim"], "legenda": "Legenda do carrossel"})

    midia = await _montar(piece, tmp_path, render)

    assert midia.imagens == [
        "https://api.exemplo/media/ag1-0.png",
        "https://api.exemplo/media/ag1-1.png",
        "https://api.exemplo/media/ag1-2.png",
    ]
    assert midia.legenda == "Legenda do carrossel"
    assert render.chamadas == [("slide", "capa"), ("slide", "meio"), ("slide", "fim")]
    assert (tmp_path / "ag1-2.png").exists()


@pytest.mark.anyio
async def test_carrossel_antigo_sem_legenda_publica_com_legenda_vazia(tmp_path):
    midia = await _montar(_piece("carrossel", {"slides": ["a", "b"]}), tmp_path)
    assert midia.legenda == ""


@pytest.mark.anyio
async def test_frase_vira_imagem_unica(tmp_path):
    render = RenderizadorFalso()
    piece = _piece("frase", {"frase": "Pensão não é <em>ajuda</em>.", "legenda": "Texto"})

    midia = await _montar(piece, tmp_path, render)

    assert midia.imagens == ["https://api.exemplo/media/ag1-0.png"]
    assert midia.legenda == "Texto"
    assert render.chamadas == [("frase", "Pensão não é <em>ajuda</em>.")]


@pytest.mark.anyio
async def test_pergunta_vira_card_de_pergunta(tmp_path):
    render = RenderizadorFalso()
    piece = _piece("pergunta", {"pergunta": "Fui demitida grávida. E agora?", "legenda": "Resposta"})

    midia = await _montar(piece, tmp_path, render)

    assert render.chamadas == [("pergunta", "Fui demitida grávida. E agora?")]
    assert midia.legenda == "Resposta"


@pytest.mark.anyio
async def test_estatico_usa_o_texto_de_overlay_como_card(tmp_path):
    render = RenderizadorFalso()
    piece = _piece(
        "estatico",
        {"conceito_visual": "x", "texto_overlay": "Atestado verdadeiro protege você", "legenda": "L", "cta": "C"},
    )

    midia = await _montar(piece, tmp_path, render)

    assert render.chamadas == [("frase", "Atestado verdadeiro protege você")]
    assert len(midia.imagens) == 1


@pytest.mark.anyio
async def test_cta_separado_e_anexado_ao_fim_da_legenda(tmp_path):
    piece = _piece("estatico", {"texto_overlay": "T", "legenda": "Legenda.", "cta": "Salve este post."})
    midia = await _montar(piece, tmp_path)
    assert midia.legenda == "Legenda.\n\nSalve este post."


@pytest.mark.anyio
async def test_peca_sem_texto_da_imagem_falha_com_erro_proprio(tmp_path):
    with pytest.raises(PecaSemConteudo):
        await _montar(_piece("frase", {"legenda": "só legenda"}), tmp_path)
    with pytest.raises(PecaSemConteudo):
        await _montar(_piece("carrossel", {"slides": []}), tmp_path)


def test_publicavel_so_aceita_tipos_do_feed():
    """Imagem própria ou Reels com vídeo pronto (desde 09/10/2026)."""
    for tipo in ("carrossel", "frase", "pergunta", "estatico", "reels"):
        assert publicavel(tipo)
    for tipo in ("legenda", "stories", "artigo", "jornal"):
        assert not publicavel(tipo)


@pytest.mark.anyio
async def test_arte_ja_enviada_e_usada_sem_renderizar(tmp_path):
    render = RenderizadorFalso()
    pergunta = _piece("pergunta", {"pergunta": "P?", "imagem": "https://api/media/arte.png", "legenda": "L"})
    carrossel = _piece("carrossel", {"slides": ["a", "b"], "imagens": ["https://api/media/1.png", "https://api/media/2.png"]})

    m1 = await _montar(pergunta, tmp_path, render)
    m2 = await _montar(carrossel, tmp_path, render)

    assert m1.imagens == ["https://api/media/arte.png"]
    assert m2.imagens == ["https://api/media/1.png", "https://api/media/2.png"]
    assert render.chamadas == []


@pytest.mark.anyio
async def test_primeiro_comentario_vem_do_corpo(tmp_path):
    piece = _piece("frase", {"frase": "Frase", "legenda": "L", "primeiro_comentario": "  Base legal: art. 1º.  "})

    midia = await _montar(piece, tmp_path)

    assert midia.primeiro_comentario == "Base legal: art. 1º."


@pytest.mark.anyio
async def test_peca_sem_primeiro_comentario_fica_vazia(tmp_path):
    piece = _piece("carrossel", {"imagens": ["https://x/1.png", "https://x/2.png"], "legenda": "L"})

    midia = await _montar(piece, tmp_path)

    assert midia.primeiro_comentario == ""


@pytest.mark.anyio
async def test_reels_com_video_pronto_vira_midia_de_video(tmp_path):
    piece = _piece("reels", {"video": "https://api.exemplo/media/reel.mp4", "legenda": "Legenda",
                             "primeiro_comentario": "📚 Base legal"})

    midia = await _montar(piece, tmp_path)

    assert publicavel("reels")
    assert midia.video == "https://api.exemplo/media/reel.mp4"
    assert midia.imagens == []
    assert midia.legenda == "Legenda"
    assert midia.primeiro_comentario == "📚 Base legal"


@pytest.mark.anyio
async def test_reels_sem_video_nao_publica(tmp_path):
    with pytest.raises(PecaSemConteudo):
        await _montar(_piece("reels", {"roteiro": []}), tmp_path)
