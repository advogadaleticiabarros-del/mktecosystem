"""Bitly: link curto com contagem de cliques (bio, stories, LinkedIn, newsletter).

Interface: `Bitly(token)`
- `await encurtar(url)` → link curto (o Bitly devolve o mesmo link se a URL já foi encurtada antes);
- `await cliques(link_curto)` → total de cliques desde a criação.
Token em bitly.com → Settings → Developer settings → API → Generate token.
"""
import httpx

API = "https://api-ssl.bitly.com/v4"


class Bitly:
    def __init__(self, token: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._token = token
        self._transport = transport

    def _cliente(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=self._transport, timeout=20,
                                 headers={"Authorization": f"Bearer {self._token}"})

    async def encurtar(self, url: str) -> str:
        async with self._cliente() as c:
            r = await c.post(f"{API}/shorten", json={"long_url": url})
        r.raise_for_status()
        return r.json()["link"]

    async def cliques(self, link_curto: str) -> int:
        bitlink = link_curto.removeprefix("https://").removeprefix("http://")
        async with self._cliente() as c:
            r = await c.get(f"{API}/bitlinks/{bitlink}/clicks/summary", params={"unit": "day", "units": -1})
        r.raise_for_status()
        return int(r.json().get("total_clicks", 0))
