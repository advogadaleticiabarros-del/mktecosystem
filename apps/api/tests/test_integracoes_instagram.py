import httpx
import pytest

from app.integrations.social.meta_client import MetaClient


@pytest.mark.anyio
async def test_trocar_code_por_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "code=abc123" in str(request.url)
        return httpx.Response(200, json={"access_token": "user_token_curto", "token_type": "bearer"})

    transport = httpx.MockTransport(handler)
    client = MetaClient(app_id="123", app_secret="segredo", transport=transport)
    resultado = await client.trocar_code_por_token("abc123", "https://api.example.com/callback")
    assert resultado["access_token"] == "user_token_curto"


@pytest.mark.anyio
async def test_buscar_paginas():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"data": [{"id": "111", "name": "Advogada Letícia Barros", "access_token": "page_token"}]},
        )

    transport = httpx.MockTransport(handler)
    client = MetaClient(app_id="123", app_secret="segredo", transport=transport)
    paginas = await client.buscar_paginas("user_token")
    assert paginas[0]["id"] == "111"
    assert paginas[0]["access_token"] == "page_token"


@pytest.mark.anyio
async def test_buscar_conta_instagram():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"instagram_business_account": {"id": "999"}, "id": "111"}
        )

    transport = httpx.MockTransport(handler)
    client = MetaClient(app_id="123", app_secret="segredo", transport=transport)
    conta = await client.buscar_conta_instagram("111", "page_token")
    assert conta["id"] == "999"
