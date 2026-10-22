from datetime import date

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
async def test_buscar_metricas_envia_periodo_completo_dos_ultimos_30_dias():
    pedidos = []

    def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        return httpx.Response(200, json={})

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    await client.buscar_metricas("access_token", "locations/456", hoje=date(2026, 10, 22))

    params = pedidos[0].url.params
    assert params["dailyRange.start_date.year"] == "2026"
    assert params["dailyRange.start_date.month"] == "9"
    assert params["dailyRange.start_date.day"] == "22"
    assert params["dailyRange.end_date.year"] == "2026"
    assert params["dailyRange.end_date.month"] == "10"
    assert params["dailyRange.end_date.day"] == "21"
    assert "BUSINESS_IMPRESSIONS_MOBILE_MAPS" in params.get_list("dailyMetrics")


@pytest.mark.anyio
async def test_buscar_metricas_soma_visualizacoes_no_maps():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "multiDailyMetricTimeSeries": [
                    {
                        "dailyMetricTimeSeries": [
                            {
                                "dailyMetric": "BUSINESS_IMPRESSIONS_MOBILE_MAPS",
                                "timeSeries": {"datedValues": [{"value": "10"}, {}]},
                            },
                            {
                                "dailyMetric": "BUSINESS_IMPRESSIONS_DESKTOP_MAPS",
                                "timeSeries": {"datedValues": [{"value": "4"}]},
                            },
                        ]
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    metricas = await client.buscar_metricas("access_token", "locations/456")
    assert metricas["visualizacoes"] == 14


@pytest.mark.anyio
async def test_listar_avaliacoes():
    pedidos = []

    def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        return httpx.Response(
            200,
            json={
                "reviews": [
                    {
                        "name": "accounts/123/locations/456/reviews/789",
                        "reviewer": {"displayName": "Maria S."},
                        "starRating": "FIVE",
                        "comment": "Excelente atendimento",
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    avaliacoes = await client.listar_avaliacoes("access_token", "accounts/123", "locations/456")
    assert avaliacoes[0]["reviewer"]["displayName"] == "Maria S."
    # Avaliações só existem na API v4 (mybusiness.googleapis.com), com conta + local no caminho.
    assert str(pedidos[0].url).startswith(
        "https://mybusiness.googleapis.com/v4/accounts/123/locations/456/reviews"
    )


@pytest.mark.anyio
async def test_responder_avaliacao():
    chamadas = []

    def handler(request: httpx.Request) -> httpx.Response:
        chamadas.append(request)
        return httpx.Response(200, json={"comment": "Obrigada pela confiança!"})

    transport = httpx.MockTransport(handler)
    client = GoogleBusinessClient(client_id="id", client_secret="segredo", transport=transport)
    await client.responder_avaliacao(
        "access_token", "accounts/123/locations/456/reviews/789", "Obrigada pela confiança!"
    )
    assert len(chamadas) == 1
    assert chamadas[0].method == "PUT"
    assert str(chamadas[0].url) == (
        "https://mybusiness.googleapis.com/v4/accounts/123/locations/456/reviews/789/reply"
    )
