"""Pesquisa web da OpenAI (Responses API + web_search) como fonte do Jornalista.

Acha páginas que o Google Notícias não lista (sites de tribunais, gov.br).
Só ficam as notícias cujo link a própria busca citou (anotações
`url_citation`): link que o modelo escreveu sem ter visitado é descartado.
Cada instância faz no máximo `max_buscas` pesquisas (custo por ronda).
"""
import json
from datetime import datetime

import httpx

from app.integrations.noticias.base import Noticia

URL = "https://api.openai.com/v1/responses"

PROMPT = """\
Pesquise na web notícias e publicações dos últimos {dias} dias, no Brasil, sobre: {consulta}.
Priorize fontes oficiais (sites .jus.br, .gov.br, Planalto, INSS) e veículos de imprensa confiáveis.
Traga até 6 itens reais que você abriu nesta pesquisa. Não invente nada.
Responda SOMENTE com JSON: {{"noticias": [{{"titulo": str, "url": str, "veiculo": str, \
"data": "AAAA-MM-DD" ou null, "trecho": "2 a 3 frases com o fato"}}]}}
"""


def _sem_rastreio(url: str) -> str:
    return url.split("?utm_")[0].split("&utm_")[0].rstrip("/")


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
                json={"model": self._model, "tools": [{"type": "web_search"}],
                      "input": PROMPT.format(dias=dias, consulta=consulta)},
            )
            resposta.raise_for_status()

        texto, citadas = "", set()
        for item in resposta.json().get("output", []):
            if item.get("type") != "message":
                continue
            for parte in item.get("content", []):
                if parte.get("type") == "output_text":
                    texto += parte.get("text", "")
                    citadas |= {_sem_rastreio(a["url"]) for a in parte.get("annotations", []) if a.get("url")}

        inicio, fim = texto.find("{"), texto.rfind("}")
        try:
            itens = json.loads(texto[inicio : fim + 1]).get("noticias", []) if inicio != -1 else []
        except json.JSONDecodeError:
            itens = []

        noticias = []
        for i in itens:
            url = _sem_rastreio(str(i.get("url") or ""))
            if not url or url not in citadas:
                continue
            try:
                publicado = datetime.fromisoformat(i["data"]) if i.get("data") else None
            except ValueError:
                publicado = None
            noticias.append(Noticia(
                titulo=str(i.get("titulo") or "").strip(), url=url, fonte=str(i.get("veiculo") or "web"),
                trecho=str(i.get("trecho") or "")[:600], publicado_em=publicado, site=url,
            ))
        return noticias
