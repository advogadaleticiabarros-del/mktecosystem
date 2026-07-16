import json

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"


class GeminiClient:
    def __init__(self, api_key: str) -> None:
        self._client = genai.Client(api_key=api_key)

    async def generate_json(self, prompt: str) -> dict:
        response = await self._client.aio.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(response.text)

    async def generate_text(self, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        return response.text
