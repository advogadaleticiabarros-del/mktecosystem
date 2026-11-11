"""Google Safe Browsing: confere se algum link é conhecido como golpe, vírus ou programa indesejado.

Interface: `SafeBrowsing(chave).conferir(urls)` → `dict[url, motivo]` só com os links perigosos (vazio = todos ok).
Usa a mesma `GOOGLE_API_KEY` do PageSpeed (ativar "Safe Browsing API" no Google Cloud).
"""
import httpx

URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
MOTIVOS = {"MALWARE": "vírus", "SOCIAL_ENGINEERING": "golpe (phishing)", "UNWANTED_SOFTWARE": "programa indesejado",
           "POTENTIALLY_HARMFUL_APPLICATION": "aplicativo perigoso"}


class SafeBrowsing:
    def __init__(self, chave: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._chave = chave
        self._transport = transport

    async def conferir(self, urls: list[str]) -> dict[str, str]:
        urls = list(dict.fromkeys(u for u in urls if u))
        if not urls:
            return {}
        corpo = {
            "client": {"clientId": "orbit", "clientVersion": "1.0"},
            "threatInfo": {"threatTypes": list(MOTIVOS), "platformTypes": ["ANY_PLATFORM"],
                           "threatEntryTypes": ["URL"], "threatEntries": [{"url": u} for u in urls[:500]]},
        }
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as c:
            r = await c.post(URL, params={"key": self._chave}, json=corpo)
        r.raise_for_status()
        return {m["threat"]["url"]: MOTIVOS.get(m["threatType"], m["threatType"]) for m in r.json().get("matches", [])}
