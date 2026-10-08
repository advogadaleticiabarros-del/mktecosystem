"""De onde o Orbit tira a IA que escreve: um só lugar para todas as partes.

`criar_ia(openai_key)` devolve um `AIClient`:
- Gemini e OpenAI configurados → Gemini como principal e OpenAI como reserva
  automática (cota do Gemini estourada ou falha → a mesma pergunta vai para a
  OpenAI, sem a pessoa perceber);
- só um dos dois → esse;
- nenhum → None.
`openai_key` vem do painel de Chaves de IA; sem ela, usa OPENAI_API_KEY.
"""
import logging

from app.config import settings
from app.integrations.ai.base import AIClient

logger = logging.getLogger(__name__)


class IAComReserva:
    def __init__(self, principal: AIClient, reserva: AIClient) -> None:
        self._principal = principal
        self._reserva = reserva

    async def generate_text(self, prompt: str) -> str:
        try:
            return await self._principal.generate_text(prompt)
        except Exception as erro:
            logger.warning("IA principal falhou (%s); usando a reserva.", str(erro)[:120])
            return await self._reserva.generate_text(prompt)

    async def generate_json(self, prompt: str) -> dict:
        try:
            return await self._principal.generate_json(prompt)
        except Exception as erro:
            logger.warning("IA principal falhou (%s); usando a reserva.", str(erro)[:120])
            return await self._reserva.generate_json(prompt)


def criar_ia(openai_key: str | None = None) -> AIClient | None:
    openai_key = openai_key or settings.OPENAI_API_KEY
    gemini = None
    if settings.GEMINI_API_KEY:
        from app.integrations.ai.gemini import GeminiClient

        gemini = GeminiClient(api_key=settings.GEMINI_API_KEY)
    openai = None
    if openai_key:
        from app.integrations.ai.openai_client import OpenAIClient

        openai = OpenAIClient(api_key=openai_key, model=settings.OPENAI_RADAR_MODEL)
    if gemini and openai:
        return IAComReserva(gemini, openai)
    return gemini or openai
