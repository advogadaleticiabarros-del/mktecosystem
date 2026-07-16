from typing import Protocol


class AIClient(Protocol):
    async def generate_json(self, prompt: str) -> dict: ...

    async def generate_text(self, prompt: str) -> str: ...
