"""NewsData.io: notícias em português de veículos brasileiros (chave grátis em newsdata.io; o plano grátis cobre as
últimas 48 horas). Mesma interface das outras fontes do Jornalista."""
from datetime import datetime, timedelta, timezone

import httpx

from app.integrations.noticias.base import Noticia

URL = "https://newsdata.io/api/1/latest"


class NewsData:
    def __init__(self, chave: str, limite: int = 10, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._chave = chave
        self._limite = limite
        self._transport = transport

    async def buscar(self, consulta: str, dias: int) -> list[Noticia]:
        params = {"apikey": self._chave, "q": consulta[:100], "language": "pt", "country": "br",
                  "size": min(self._limite, 10)}
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as c:
            r = await c.get(URL, params=params)
        r.raise_for_status()
        limite = datetime.now(timezone.utc) - timedelta(days=dias)
        noticias = []
        for n in r.json().get("results") or []:
            publicado = None
            if n.get("pubDate"):
                try:
                    publicado = datetime.strptime(n["pubDate"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                except ValueError:
                    publicado = None
            if publicado and publicado < limite:
                continue
            noticias.append(Noticia(
                titulo=(n.get("title") or "").strip(), url=n.get("link") or "",
                fonte=n.get("source_name") or n.get("source_id") or "web",
                trecho=(n.get("description") or "")[:600], publicado_em=publicado, site=n.get("source_url") or "",
            ))
        return noticias
