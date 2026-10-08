import json

import httpx
import pytest

from app.integrations.ai.fabrica import IAComReserva, criar_ia
from app.integrations.ai.openai_client import OpenAIClient


class IAFalsa:
    def __init__(self, resposta=None, erro=None):
        self.resposta, self.erro, self.chamadas = resposta, erro, 0

    async def generate_text(self, prompt):
        self.chamadas += 1
        if self.erro:
            raise self.erro
        return self.resposta

    async def generate_json(self, prompt):
        self.chamadas += 1
        if self.erro:
            raise self.erro
        return self.resposta


@pytest.mark.anyio
async def test_usa_a_principal_quando_ela_responde():
    principal, reserva = IAFalsa("gemini"), IAFalsa("openai")
    assert await IAComReserva(principal, reserva).generate_text("p") == "gemini"
    assert reserva.chamadas == 0


@pytest.mark.anyio
async def test_cota_estourada_na_principal_passa_para_a_reserva():
    principal = IAFalsa(erro=RuntimeError("429 RESOURCE_EXHAUSTED"))
    reserva = IAFalsa({"ok": True})
    assert await IAComReserva(principal, reserva).generate_json("p") == {"ok": True}
    assert principal.chamadas == 1 and reserva.chamadas == 1


def test_fabrica_escolhe_conforme_as_chaves(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "g")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    assert not isinstance(criar_ia(), IAComReserva)
    assert isinstance(criar_ia("sk-x"), IAComReserva)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    assert isinstance(criar_ia("sk-x"), OpenAIClient)
    assert criar_ia(None) is None


@pytest.mark.anyio
async def test_cliente_openai_texto_e_json():
    pedidos = []

    def responder(request):
        corpo = json.loads(request.content)
        pedidos.append(corpo)
        conteudo = '{"a": 1}' if corpo.get("response_format") else "olá"
        return httpx.Response(200, json={"choices": [{"message": {"content": conteudo}}]})

    ia = OpenAIClient("sk-x", model="gpt-4.1-mini", transport=httpx.MockTransport(responder))
    assert await ia.generate_text("diga olá") == "olá"
    assert await ia.generate_json("responda em JSON") == {"a": 1}
    assert pedidos[1]["response_format"] == {"type": "json_object"}
    assert pedidos[0]["messages"][0]["content"] == "diga olá"
