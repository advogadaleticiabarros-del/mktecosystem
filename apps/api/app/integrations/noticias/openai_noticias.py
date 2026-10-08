"""Pesquisa web da OpenAI (Responses API + web_search) como fonte do Jornalista.

Acha páginas que o Google Notícias não lista (sites de tribunais, gov.br).
A resposta é pedida em texto corrido com citações: cada citação (`url_citation`)
é uma página que a busca de fato abriu, e vira uma `Noticia` com o título da
página, o link e o trecho do texto que a cita. Link escrito pelo modelo sem
citação não entra. Cada instância faz no máximo `max_buscas` pesquisas.
"""
from urllib.parse import urlparse

import httpx

from app.integrations.noticias.base import Noticia

URL = "https://api.openai.com/v1/responses"

PROMPT = """\
Pesquise na web as notícias e publicações dos últimos {dias} dias, no Brasil, sobre: {consulta}.
Priorize fontes oficiais (sites .jus.br, .gov.br, Planalto, INSS) e veículos de imprensa confiáveis.
Escreva uma lista curta (até 6 itens): para cada notícia, uma frase dizendo o fato, quem decidiu ou \
publicou e a data, citando a fonte. Ignore páginas institucionais antigas, PDFs de anos anteriores e \
painéis de dados: só fatos novos do período.
"""


def _sem_rastreio(url: str) -> str:
    return url.split("?utm_")[0].split("&utm_")[0].rstrip("/")


def _veiculo(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.") or "web"


class OpenAINoticias:
    def __init__(
        self, api_key: str, model: str, transport: httpx.AsyncBaseTransport | None = None, max_buscas: int = 8
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._transport = transport
        self._restantes = max_buscas

    async def buscar(self, consulta: str, dias: int) -> list[Noticia]:
        if self._restantes <= 0:
            return []
        self._restantes -= 1
        async with httpx.AsyncClient(transport=self._transport, timeout=180) as client:
            resposta = await client.post(
                URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "model": self._model,
                    "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "BR"}}],
                    "input": PROMPT.format(dias=dias, consulta=consulta),
                },
            )
            resposta.raise_for_status()

        noticias: list[Noticia] = []
        vistas: set[str] = set()
        for item in resposta.json().get("output", []):
            if item.get("type") != "message":
                continue
            for parte in item.get("content", []):
                texto = parte.get("text", "")
                for a in parte.get("annotations", []):
                    if a.get("type") != "url_citation" or not a.get("url"):
                        continue
                    url = _sem_rastreio(a["url"])
                    if url in vistas:
                        continue
                    vistas.add(url)
                    inicio = texto.rfind("\n", 0, a.get("start_index", 0)) + 1
                    trecho = texto[inicio : a.get("start_index", 0)].strip(" -*•()[]")
                    noticias.append(Noticia(
                        titulo=(a.get("title") or trecho[:120]).strip(),
                        url=url,
                        fonte=_veiculo(url),
                        trecho=trecho[:600],
                        publicado_em=None,
                        site=url,
                    ))
        return noticias
