"""Google Notícias via RSS público (sem chave): manchetes reais com veículo e data."""
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape

import httpx

from app.integrations.noticias.base import Noticia

URL = "https://news.google.com/rss/search"


class GoogleNewsRSS:
    def __init__(self, transport: httpx.AsyncBaseTransport | None = None, limite: int = 15) -> None:
        self._transport = transport
        self._limite = limite

    async def buscar(self, consulta: str, dias: int) -> list[Noticia]:
        params = {"q": f"{consulta} when:{dias}d", "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419"}
        async with httpx.AsyncClient(transport=self._transport, timeout=20, follow_redirects=True) as client:
            resposta = await client.get(URL, params=params, headers={"User-Agent": "Mozilla/5.0 OrbitJornalista"})
            resposta.raise_for_status()
        raiz = ET.fromstring(resposta.content)
        corte = datetime.now(timezone.utc) - timedelta(days=dias)
        noticias = []
        for item in raiz.iter("item"):
            titulo = (item.findtext("title") or "").strip()
            origem = item.find("source")
            fonte = (origem.text or "").strip() if origem is not None else ""
            site = origem.get("url", "") if origem is not None else ""
            if fonte and titulo.endswith(f" - {fonte}"):
                titulo = titulo[: -len(fonte) - 3].strip()
            try:
                publicado = parsedate_to_datetime(item.findtext("pubDate") or "")
            except (TypeError, ValueError):
                publicado = None
            if publicado and publicado < corte:
                continue
            trecho = re.sub(r"<[^>]+>", " ", unescape(item.findtext("description") or ""))
            noticias.append(Noticia(
                titulo=titulo, url=(item.findtext("link") or "").strip(), fonte=fonte or "Google Notícias",
                trecho=" ".join(trecho.split())[:400], publicado_em=publicado, site=site,
            ))
            if len(noticias) >= self._limite:
                break
        return noticias
