import httpx
import pytest

from app.integrations.search.tavily_client import TavilyClient


@pytest.mark.anyio
async def test_search():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "api.tavily.com/search" in str(request.url)
        assert request.headers["authorization"] == "Bearer chave"
        return httpx.Response(
            200,
            json={"results": [{"title": "Título", "content": "Conteúdo", "url": "https://x.com"}]},
        )

    transport = httpx.MockTransport(handler)
    client = TavilyClient(api_key="chave", transport=transport)
    resultado = await client.search("revisão da vida toda")
    assert resultado == [{"title": "Título", "content": "Conteúdo", "url": "https://x.com"}]


@pytest.mark.anyio
async def test_search_sem_api_key_levanta_erro():
    client = TavilyClient(api_key="")
    with pytest.raises(ValueError):
        await client.search("qualquer coisa")
