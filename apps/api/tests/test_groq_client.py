import json

import httpx
import pytest

from app.integrations.ai.groq_client import GroqClient


@pytest.mark.anyio
async def test_generate_text():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "groq.com/openai/v1/chat/completions" in str(request.url)
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Olá!"}}]},
        )

    transport = httpx.MockTransport(handler)
    client = GroqClient(api_key="chave", transport=transport)
    resultado = await client.generate_text("diga oi")
    assert resultado == "Olá!"


@pytest.mark.anyio
async def test_generate_json():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"urgencia": "normal"}'}}]},
        )

    transport = httpx.MockTransport(handler)
    client = GroqClient(api_key="chave", transport=transport)
    resultado = await client.generate_json("classifique")
    assert resultado == {"urgencia": "normal"}


@pytest.mark.anyio
async def test_generate_text_sem_api_key_levanta_erro():
    client = GroqClient(api_key="")
    with pytest.raises(ValueError):
        await client.generate_text("oi")
