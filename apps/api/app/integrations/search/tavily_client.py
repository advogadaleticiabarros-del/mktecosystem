import httpx

TAVILY_URL = "https://api.tavily.com/search"


class TavilyClient:
    def __init__(self, api_key: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._api_key = api_key
        self._transport = transport

    async def search(self, query: str, max_results: int = 5) -> list[dict]:
        if not self._api_key:
            raise ValueError("TAVILY_API_KEY não configurada")

        async with httpx.AsyncClient(transport=self._transport, timeout=20) as client:
            response = await client.post(
                TAVILY_URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"query": query, "max_results": max_results, "search_depth": "basic"},
            )
            response.raise_for_status()
            return response.json().get("results", [])
