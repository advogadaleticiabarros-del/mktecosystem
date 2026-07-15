from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.integrations.sources.tst import fetch_tst

SAMPLE_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry>
<title>Informativo TST: n. 300 (1 a 10 jul. 2026)</title>
<link href="https://hdl.handle.net/20.500.12178/999999" rel="alternate"/>
<published>2026-07-10T00:00:00Z</published>
</entry>
<entry>
<title>Informativo TST: n. 299 (20 a 30 jun. 2026)</title>
<link href="https://hdl.handle.net/20.500.12178/999998" rel="alternate"/>
<published>2026-06-30T00:00:00Z</published>
</entry>
</feed>
"""


@pytest.mark.anyio
async def test_fetch_tst_parses_atom_entries():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.text = SAMPLE_ATOM

    with patch("app.integrations.sources.tst.httpx.AsyncClient") as MockClient:
        instance = MockClient.return_value.__aenter__.return_value
        instance.get = AsyncMock(return_value=fake_response)

        doc = await fetch_tst(query="trabalhista")

    assert doc.fonte == "TST"
    assert "Informativo TST: n. 300" in doc.texto
    assert "Informativo TST: n. 299" in doc.texto
