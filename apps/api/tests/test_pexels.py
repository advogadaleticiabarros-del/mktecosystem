import httpx
import pytest

from app.integrations.imagens.pexels import FotoBanco, Pexels
from app.services.chaves_api import PROVEDORES, ChaveRecusada, validar_pexels


def _foto(i):
    return {"id": i, "width": 4000, "height": 6000, "alt": f"Mulher no escritório {i}",
            "url": f"https://www.pexels.com/photo/{i}/", "photographer": "Ana Souza",
            "src": {"original": f"https://images.pexels.com/{i}.jpeg", "large2x": f"https://images.pexels.com/{i}-l.jpeg"}}


@pytest.mark.anyio
async def test_busca_fotos_verticais_com_credito_do_fotografo():
    pedidos = []

    def responder(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        return httpx.Response(200, json={"photos": [_foto(1), _foto(2)]})

    fotos = await Pexels("chave", transport=httpx.MockTransport(responder)).buscar("mulher trabalhando escritório", 2)

    req = pedidos[0]
    assert req.headers["Authorization"] == "chave"
    assert req.url.params["orientation"] == "portrait"
    assert req.url.params["locale"] == "pt-BR"
    assert req.url.params["per_page"] == "2"
    assert fotos[0] == FotoBanco(id=1, url="https://images.pexels.com/1.jpeg", autor="Ana Souza",
                                 pagina="https://www.pexels.com/photo/1/", descricao="Mulher no escritório 1",
                                 largura=4000, altura=6000)


@pytest.mark.anyio
async def test_chave_recusada_pelo_pexels():
    transporte = httpx.MockTransport(lambda r: httpx.Response(401, json={"error": "invalid"}))
    with pytest.raises(ChaveRecusada):
        await validar_pexels("ruim-ruim-ruim", transport=transporte)


def test_pexels_aparece_no_painel_de_chaves():
    assert PROVEDORES["pexels"]["nome"] == "Pexels"
