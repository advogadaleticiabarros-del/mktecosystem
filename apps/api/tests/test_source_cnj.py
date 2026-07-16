from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.integrations.sources.cnj import fetch_cnj

SAMPLE_HTML = """
<html><head><title>Notícias do Judiciário</title></head>
<body>
<article><h2>CNJ divulga nova resolução sobre prazos processuais</h2></article>
</body></html>
"""


@pytest.mark.anyio
async def test_fetch_cnj_cleans_html():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.text = SAMPLE_HTML

    with patch("app.integrations.sources.cnj.httpx.AsyncClient") as MockClient:
        instance = MockClient.return_value.__aenter__.return_value
        instance.get = AsyncMock(return_value=fake_response)

        doc = await fetch_cnj()

    assert doc.fonte == "CNJ"
    assert "nova resolução sobre prazos processuais" in doc.texto
