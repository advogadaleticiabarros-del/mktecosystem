import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.integrations.ai.gemini import GeminiClient


@pytest.mark.anyio
async def test_generate_json_parses_model_response():
    fake_response = MagicMock()
    fake_response.text = json.dumps({"titulo": "Teste", "corpo": "Conteúdo gerado"})

    with patch("app.integrations.ai.gemini.genai.Client") as MockClient:
        instance = MockClient.return_value
        instance.aio.models.generate_content = AsyncMock(return_value=fake_response)

        client = GeminiClient(api_key="fake-key")
        result = await client.generate_json("gere um json de teste")

    assert result == {"titulo": "Teste", "corpo": "Conteúdo gerado"}


@pytest.mark.anyio
async def test_generate_text_returns_raw_text():
    fake_response = MagicMock()
    fake_response.text = "texto gerado livre"

    with patch("app.integrations.ai.gemini.genai.Client") as MockClient:
        instance = MockClient.return_value
        instance.aio.models.generate_content = AsyncMock(return_value=fake_response)

        client = GeminiClient(api_key="fake-key")
        result = await client.generate_text("escreva um texto")

    assert result == "texto gerado livre"
