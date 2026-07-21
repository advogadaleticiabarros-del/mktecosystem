import json

import httpx

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


class GroqClient:
    def __init__(self, api_key: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._api_key = api_key
        self._transport = transport

    async def _chat(self, prompt: str, forcar_json: bool) -> str:
        if not self._api_key:
            raise ValueError("GROQ_API_KEY não configurada")

        body = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
        if forcar_json:
            body["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            response = await client.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=body,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def generate_text(self, prompt: str) -> str:
        return await self._chat(prompt, forcar_json=False)

    async def generate_json(self, prompt: str) -> dict:
        texto = await self._chat(prompt, forcar_json=True)
        return json.loads(texto)
