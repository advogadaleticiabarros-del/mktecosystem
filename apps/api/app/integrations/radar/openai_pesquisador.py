"""Adapter do Radar: OpenAI Responses API com a ferramenta web_search.

O modelo pesquisa na web sozinho e devolve os achados já com link."""
from datetime import date

import httpx

from app.services.radar_juridico import Achado, montar_prompt, parse_achados

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


class OpenAIPesquisador:
    def __init__(self, api_key: str, model: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._api_key = api_key
        self._model = model
        self._transport = transport

    async def pesquisar(self, areas: list[str], evitar: list[str], hoje: date) -> list[Achado]:
        # Pesquisa com várias buscas encadeadas leva de 30s a alguns minutos.
        async with httpx.AsyncClient(transport=self._transport, timeout=300) as client:
            response = await client.post(
                OPENAI_RESPONSES_URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "model": self._model,
                    "tools": [{"type": "web_search"}],
                    "input": montar_prompt(areas, evitar, hoje),
                },
            )
            response.raise_for_status()

        texto = "".join(
            parte.get("text", "")
            for item in response.json().get("output", [])
            if item.get("type") == "message"
            for parte in item.get("content", [])
            if parte.get("type") == "output_text"
        )
        return parse_achados(texto)
