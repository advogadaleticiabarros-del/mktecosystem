"""Tavily (modo notícias): traz o texto da matéria, não só a manchete."""
from datetime import datetime
from urllib.parse import urlparse

from app.integrations.noticias.base import Noticia
from app.integrations.search.tavily_client import TavilyClient


def _veiculo(url: str) -> str:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    return host or "web"


class TavilyNoticias:
    def __init__(self, tavily: TavilyClient, limite: int = 8) -> None:
        self._tavily = tavily
        self._limite = limite

    async def buscar(self, consulta: str, dias: int) -> list[Noticia]:
        resultados = await self._tavily.search(consulta, max_results=self._limite, topic="news", days=dias)
        noticias = []
        for r in resultados:
            publicado = None
            if r.get("published_date"):
                try:
                    publicado = datetime.strptime(r["published_date"], "%a, %d %b %Y %H:%M:%S %Z")
                except ValueError:
                    publicado = None
            noticias.append(Noticia(
                titulo=(r.get("title") or "").strip(), url=r.get("url", ""), fonte=_veiculo(r.get("url", "")),
                trecho=(r.get("content") or "")[:600], publicado_em=publicado, site=r.get("url", ""),
            ))
        return noticias
