"""Adapter reserva do Radar: busca notícias recentes na Tavily (uma consulta
por área + uma geral de tribunais superiores) e deixa o Gemini selecionar e
resumir. Funciona só com as chaves que o Orbit já tem."""
from datetime import date

from app.integrations.ai.base import AIClient
from app.integrations.search.tavily_client import TavilyClient
from app.services.radar_juridico import Achado, montar_prompt, parse_achados

DIAS_RECENTES = 7


class TavilyGeminiPesquisador:
    def __init__(self, tavily: TavilyClient, ai: AIClient) -> None:
        self._tavily = tavily
        self._ai = ai

    def _consultas(self, areas: list[str], hoje: date) -> list[str]:
        mes = hoje.strftime("%m/%Y")
        consultas = [f"direito {area} decisão tribunal nova regra {mes}" for area in areas]
        consultas.append(f"STF STJ TST decisão tese repercussão geral {mes}")
        return consultas

    async def pesquisar(self, areas: list[str], evitar: list[str], hoje: date) -> list[Achado]:
        resultados: dict[str, dict] = {}
        for consulta in self._consultas(areas, hoje):
            try:
                for r in await self._tavily.search(consulta, max_results=6, topic="news", days=DIAS_RECENTES):
                    resultados.setdefault(r.get("url", ""), r)
            except Exception:
                continue  # uma consulta falhar não derruba o radar
        if not resultados:
            return []

        material = "\n\n".join(
            f"- {r.get('title', '')} ({r.get('url', '')}): {r.get('content', '')[:600]}"
            for r in resultados.values()
        )
        prompt = (
            montar_prompt(areas, evitar, hoje)
            + "\nUse SOMENTE as notícias abaixo como fonte (não invente links):\n"
            + material
        )
        return parse_achados(await self._ai.generate_text(prompt))
