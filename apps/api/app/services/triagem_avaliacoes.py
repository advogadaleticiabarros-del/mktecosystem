"""Classifica avaliações do Google Meu Negócio sem resposta como urgente/normal.

Usa o Groq (rápido, gratuito) em vez do Gemini — é só classificação de uma
palavra, não geração de conteúdo. Falha na IA nunca derruba a listagem.
"""
import asyncio
import logging

from app.integrations.ai.base import AIClient

logger = logging.getLogger(__name__)

PROMPT = """\
Classifique esta avaliação de cliente de um escritório de advocacia como
"urgente" ou "normal".

Urgente: nota baixa (1-2 estrelas) OU comentário com reclamação explícita
sobre atendimento, erro ou injustiça — mesmo com nota mediana.
Normal: elogio, neutro, ou crítica leve sem reclamação grave.

Nota: {nota}
Comentário: {comentario}

Responda em JSON: {{"urgencia": "urgente"}} ou {{"urgencia": "normal"}}
"""


async def _classificar_uma(avaliacao: dict, groq: AIClient) -> str | None:
    if avaliacao.get("reviewReply") is not None:
        return None
    try:
        prompt = PROMPT.format(
            nota=avaliacao.get("starRating", ""),
            comentario=avaliacao.get("comment", "(sem comentário)"),
        )
        resultado = await groq.generate_json(prompt)
        urgencia = resultado.get("urgencia")
        return urgencia if urgencia in ("urgente", "normal") else None
    except Exception:
        logger.exception("Falha ao classificar avaliação %s via Groq", avaliacao.get("name"))
        return None


async def classificar_avaliacoes(avaliacoes: list[dict], groq: AIClient) -> list[dict]:
    urgencias = await asyncio.gather(*[_classificar_uma(a, groq) for a in avaliacoes])
    for avaliacao, urgencia in zip(avaliacoes, urgencias):
        avaliacao["urgencia"] = urgencia

    urgentes = [a for a in avaliacoes if a["urgencia"] == "urgente"]
    outras = [a for a in avaliacoes if a["urgencia"] != "urgente"]
    return urgentes + outras
