from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.integrations.sources.stf import fetch_stf

SAMPLE_HTML = """
<html><head><title>Informativo STF</title></head>
<body>
<h3>Informativo STF</h3>
<p>Tema: Prazo prescricional em ação de revisão de benefício previdenciário.</p>
<script>console.log('ignore me')</script>
</body></html>
"""


@pytest.mark.anyio
async def test_fetch_stf_sends_browser_user_agent_and_cleans_html():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.text = SAMPLE_HTML

    with patch("app.integrations.sources.stf.httpx.AsyncClient") as MockClient:
        instance = MockClient.return_value.__aenter__.return_value
        instance.get = AsyncMock(return_value=fake_response)

        doc = await fetch_stf()

        call_kwargs = instance.get.call_args.kwargs
        assert "User-Agent" in call_kwargs["headers"]
        assert "Mozilla" in call_kwargs["headers"]["User-Agent"]

    assert doc.fonte == "STF"
    assert "Prazo prescricional" in doc.texto
    assert "console.log" not in doc.texto
    assert "<script>" not in doc.texto
