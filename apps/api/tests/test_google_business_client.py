import httpx
import pytest

from app.integrations.social.google_business_client import GoogleBusinessClient


@pytest.mark.anyio
async def test_trocar_code_por_tokens():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "oauth2.googleapis.com/token" in str(request.url)
        return httpx.Response(
            200,
            json={
                "access_token": "access_curto",
                "refresh_token": "refresh_longo",
                "expires_in": 3599,
                "token_type": "Bearer",
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    resultado = await client.trocar_code_por_tokens("codigo123", "https://api.example.com/callback")
    assert resultado["access_token"] == "access_curto"
    assert resultado["refresh_token"] == "refresh_longo"


@pytest.mark.anyio
async def test_renovar_access_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "grant_type=refresh_token" in str(request.content)
        return httpx.Response(200, json={"access_token": "access_novo", "expires_in": 3599})

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    novo_token = await client.renovar_access_token("refresh_longo")
    assert novo_token == "access_novo"


@pytest.mark.anyio
async def test_listar_contas():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"accounts": [{"name": "accounts/123", "accountName": "Advogada Letícia Barros"}]},
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    contas = await client.listar_contas("access_token")
    assert contas[0]["name"] == "accounts/123"


@pytest.mark.anyio
async def test_listar_locais():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"locations": [{"name": "locations/456", "title": "Escritório Letícia Barros"}]},
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    locais = await client.listar_locais("access_token", "accounts/123")
    assert locais[0]["name"] == "locations/456"


@pytest.mark.anyio
async def test_buscar_metricas():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "multiDailyMetricTimeSeries": [
                    {
                        "dailyMetricTimeSeries": [
                            {
                                "dailyMetric": "CALL_CLICKS",
                                "timeSeries": {"datedValues": [{"value": "3"}, {"value": "5"}]},
                            },
                            {
                                "dailyMetric": "BUSINESS_DIRECTION_REQUESTS",
                                "timeSeries": {"datedValues": [{"value": "2"}]},
                            },
                        ]
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    metricas = await client.buscar_metricas("access_token", "locations/456")
    assert metricas["chamadas"] == 8
    assert metricas["pedidos_rota"] == 2
    assert metricas["buscas"] == 0


@pytest.mark.anyio
async def test_listar_avaliacoes():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "reviews": [
                    {
                        "name": "locations/456/reviews/789",
                        "reviewer": {"displayName": "Maria S."},
                        "starRating": "FIVE",
                        "comment": "Excelente atendimento",
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    avaliacoes = await client.listar_avaliacoes("access_token", "locations/456")
    assert avaliacoes[0]["reviewer"]["displayName"] == "Maria S."


@pytest.mark.anyio
async def test_responder_avaliacao():
    chamadas = []

    def handler(request: httpx.Request) -> httpx.Response:
        chamadas.append(request)
        return httpx.Response(200, json={"comment": "Obrigada pela confiança!"})

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    await client.responder_avaliacao(
        "access_token", "locations/456/reviews/789", "Obrigada pela confiança!"
    )
    assert len(chamadas) == 1
    assert chamadas[0].method == "PUT"
