import httpx

TOKEN_URL = "https://oauth2.googleapis.com/token"
ACCOUNT_MGMT_URL = "https://mybusinessaccountmanagement.googleapis.com/v1"
BUSINESS_INFO_URL = "https://mybusinessbusinessinformation.googleapis.com/v1"
PERFORMANCE_URL = "https://businessprofileperformance.googleapis.com/v1"

METRICAS_DESEJADAS = {
    "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH": "buscas",
    "BUSINESS_IMPRESSIONS_MOBILE_SEARCH": "buscas",
    "CALL_CLICKS": "chamadas",
    "BUSINESS_DIRECTION_REQUESTS": "pedidos_rota",
}


class GoogleBusinessClient:
    def __init__(
        self, client_id: str, client_secret: str, transport: httpx.AsyncBaseTransport | None = None
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._transport = transport

    async def _post_token(self, data: dict) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.post(
                TOKEN_URL,
                data={"client_id": self._client_id, "client_secret": self._client_secret, **data},
            )
            response.raise_for_status()
            return response.json()

    async def _get(self, url: str, access_token: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.get(
                url, params=params or {}, headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()

    async def trocar_code_por_tokens(self, code: str, redirect_uri: str) -> dict:
        return await self._post_token(
            {"code": code, "redirect_uri": redirect_uri, "grant_type": "authorization_code"}
        )

    async def renovar_access_token(self, refresh_token: str) -> str:
        resultado = await self._post_token(
            {"refresh_token": refresh_token, "grant_type": "refresh_token"}
        )
        return resultado["access_token"]

    async def listar_contas(self, access_token: str) -> list[dict]:
        resultado = await self._get(f"{ACCOUNT_MGMT_URL}/accounts", access_token)
        return resultado.get("accounts", [])

    async def listar_locais(self, access_token: str, account_id: str) -> list[dict]:
        resultado = await self._get(
            f"{BUSINESS_INFO_URL}/{account_id}/locations",
            access_token,
            params={"readMask": "name,title"},
        )
        return resultado.get("locations", [])

    async def buscar_metricas(self, access_token: str, location_id: str) -> dict:
        resultado = await self._get(
            f"{PERFORMANCE_URL}/{location_id}:fetchMultiDailyMetricsTimeSeries",
            access_token,
            params={
                "dailyMetrics": list(METRICAS_DESEJADAS.keys()),
                "dailyRange.start_date.year": "2026",
            },
        )
        totais = {"buscas": 0, "chamadas": 0, "pedidos_rota": 0, "visualizacoes": 0}
        for bloco in resultado.get("multiDailyMetricTimeSeries", []):
            for serie in bloco.get("dailyMetricTimeSeries", []):
                metrica = serie.get("dailyMetric")
                chave = METRICAS_DESEJADAS.get(metrica)
                if chave is None:
                    continue
                valores = serie.get("timeSeries", {}).get("datedValues", [])
                totais[chave] += sum(int(v.get("value", 0)) for v in valores)
        return totais

    async def listar_avaliacoes(self, access_token: str, location_id: str) -> list[dict]:
        resultado = await self._get(f"{BUSINESS_INFO_URL}/{location_id}/reviews", access_token)
        return resultado.get("reviews", [])

    async def responder_avaliacao(self, access_token: str, review_name: str, texto: str) -> None:
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.put(
                f"{BUSINESS_INFO_URL}/{review_name}/reply",
                json={"comment": texto},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
