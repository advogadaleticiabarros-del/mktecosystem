import json
import logging
from datetime import datetime, timezone

from app.integrations.ai.base import AIClient
from app.integrations.search.tavily_client import TavilyClient

logger = logging.getLogger(__name__)

ANALISE_PROMPT = """\
Você verifica se uma pauta/conteúdo jurídico continua atual, comparando o \
título com resultados de busca recentes.

TÍTULO/TEMA: {titulo}
ÁREA: {area}

RESULTADOS DE BUSCA:
{resultados}

Responda em JSON: {{"desatualizado": true/false, "alerta": "explicação curta \
em português, só se desatualizado=true, senão null"}}

Considere desatualizado apenas se os resultados indicarem claramente uma \
mudança de lei, decisão judicial definitiva, revogação ou fato novo que \
contradiz o tema. Não marque como desatualizado por falta de informação ou \
resultados genéricos/não relacionados.
"""


async def verificar_atualidade(
    titulo: str,
    area: str,
    ai_client: AIClient,
    tavily_client: TavilyClient,
) -> tuple[str | None, datetime]:
    """Busca o tema na web e usa IA pra avaliar se o conteúdo pode estar
    desatualizado. Retorna (texto_do_alerta_ou_none, quando_verificou).

    Nunca levanta exceção pra quem chama — falha de busca/IA não deve
    travar criação/aprovação de pauta, só faz a verificação ficar pra depois.
    """
    verificado_em = datetime.now(timezone.utc)
    try:
        resultados = await tavily_client.search(f"{titulo} {area} 2026")
        if not resultados:
            return None, verificado_em

        resumo = "\n\n".join(
            f"- {r.get('title', '')}: {r.get('content', '')[:400]}" for r in resultados[:5]
        )
        prompt = ANALISE_PROMPT.format(titulo=titulo, area=area, resultados=resumo)
        analise = await ai_client.generate_json(prompt)
        if analise.get("desatualizado"):
            return analise.get("alerta"), verificado_em
        return None, verificado_em
    except (json.JSONDecodeError, KeyError) as exc:
        logger.warning("Verificação de atualidade: resposta inesperada da IA (%s).", exc)
        return None, verificado_em
    except Exception:
        logger.exception("Verificação de atualidade falhou para %r.", titulo)
        return None, verificado_em
