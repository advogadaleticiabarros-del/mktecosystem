from unittest.mock import AsyncMock

import pytest

from app.services.triagem_avaliacoes import classificar_avaliacoes


def _avaliacao(name: str, comment: str, star: str = "FIVE", respondida: bool = False) -> dict:
    item = {
        "name": name,
        "reviewer": {"displayName": "Cliente"},
        "starRating": star,
        "comment": comment,
    }
    if respondida:
        item["reviewReply"] = {"comment": "Obrigada!"}
    return item


@pytest.mark.anyio
async def test_classifica_e_ordena_urgentes_primeiro():
    avaliacoes = [
        _avaliacao("r1", "Muito bom, recomendo", star="FIVE"),
        _avaliacao("r2", "Péssimo atendimento, nunca mais volto", star="ONE"),
        _avaliacao("r3", "Ok", star="THREE"),
    ]

    groq = AsyncMock()
    groq.generate_json.side_effect = [
        {"urgencia": "normal"},
        {"urgencia": "urgente"},
        {"urgencia": "normal"},
    ]

    resultado = await classificar_avaliacoes(avaliacoes, groq)

    assert resultado[0]["name"] == "r2"
    assert resultado[0]["urgencia"] == "urgente"
    assert [a["name"] for a in resultado[1:]] == ["r1", "r3"]


@pytest.mark.anyio
async def test_avaliacao_respondida_nao_chama_groq():
    avaliacoes = [_avaliacao("r1", "Ótimo", respondida=True)]
    groq = AsyncMock()

    resultado = await classificar_avaliacoes(avaliacoes, groq)

    assert resultado[0]["urgencia"] is None
    groq.generate_json.assert_not_called()


@pytest.mark.anyio
async def test_falha_do_groq_vira_urgencia_nula():
    avaliacoes = [_avaliacao("r1", "Comentário qualquer")]
    groq = AsyncMock()
    groq.generate_json.side_effect = Exception("erro de rede")

    resultado = await classificar_avaliacoes(avaliacoes, groq)

    assert resultado[0]["urgencia"] is None
