import httpx
import pytest

from app.integrations.email.resend_client import ResendClient, montar_rodape


@pytest.mark.anyio
async def test_send_retorna_resend_id():
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["auth"] = request.headers.get("authorization")
        return httpx.Response(200, json={"id": "re_123"})

    transport = httpx.MockTransport(handler)
    client = ResendClient(api_key="key", sender="Teste <t@example.com>", transport=transport)
    resend_id = await client.send(
        to="dest@example.com", subject="Oi", html="<p>Oi</p>", text="Oi"
    )
    assert resend_id == "re_123"
    assert captured["url"] == "https://api.resend.com/emails"
    assert captured["auth"] == "Bearer key"


@pytest.mark.anyio
async def test_send_sem_api_key_e_noop():
    client = ResendClient(api_key="", sender="Teste <t@example.com>")
    resend_id = await client.send(to="d@example.com", subject="Oi", html="x", text="x")
    assert resend_id is None


@pytest.mark.anyio
async def test_send_erro_http_levanta():
    transport = httpx.MockTransport(lambda req: httpx.Response(422, json={"message": "bad"}))
    client = ResendClient(api_key="key", sender="T <t@example.com>", transport=transport)
    with pytest.raises(httpx.HTTPStatusError):
        await client.send(to="d@example.com", subject="Oi", html="x", text="x")


def test_montar_rodape_inclui_oab_e_descadastro():
    rodape = montar_rodape(
        assinatura="Letícia Barros — OAB/ES 39.948",
        unsubscribe_url="https://api.example.com/public/unsubscribe?token=abc",
    )
    assert "OAB/ES 39.948" in rodape
    assert "unsubscribe?token=abc" in rodape
