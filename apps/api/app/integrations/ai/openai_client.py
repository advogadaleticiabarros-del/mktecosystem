import json

import httpx

URL = "https://api.openai.com/v1/chat/completions"


class OpenAIClient:
    """Mesma interface do GeminiClient (AIClient), via Chat Completions."""

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini", transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._api_key = api_key
        self._model = model
        self._transport = transport

    async def _completar(self, prompt: str, json_mode: bool) -> str:
        corpo: dict = {"model": self._model, "messages": [{"role": "user", "content": prompt}]}
        if json_mode:
            corpo["response_format"] = {"type": "json_object"}
        async with httpx.AsyncClient(transport=self._transport, timeout=180) as client:
            resposta = await client.post(URL, headers={"Authorization": f"Bearer {self._api_key}"}, json=corpo)
            resposta.raise_for_status()
        return resposta.json()["choices"][0]["message"]["content"]

    async def generate_text(self, prompt: str) -> str:
        return await self._completar(prompt, json_mode=False)

    async def generate_json(self, prompt: str) -> dict:
        return json.loads(await self._completar(prompt, json_mode=True))
