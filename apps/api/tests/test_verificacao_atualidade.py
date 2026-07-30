import httpx
import pytest

from app.integrations.search.tavily_client import TavilyClient
from app.services.verificacao_atualidade import verificar_atualidade


class FakeAI:
    def __init__(self, resposta: dict) -> None:
        self._resposta = resposta

    async def generate_json(self, prompt: str) -> dict:
        return self._resposta

    async def generate_text(self, prompt: str) -> str:
        return ""


def _tavily_com_resultados(resultados: list[dict]) -> TavilyClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"results": resultados})

    return TavilyClient(api_key="chave", transport=httpx.MockTransport(handler))


@pytest.mark.anyio
async def test_marca_alerta_quando_ia_diz_desatualizado():
    tavily = _tavily_com_resultados([{"title": "STF encerra tema", "content": "..."}])
    ai = FakeAI({"desatualizado": True, "alerta": "Tema encerrado pelo STF."})

    alerta, verificado_em = await verificar_atualidade("Tema X", "Previdenciário", ai, tavily)

    assert alerta == "Tema encerrado pelo STF."
    assert verificado_em is not None


@pytest.mark.anyio
async def test_sem_alerta_quando_ia_diz_atualizado():
    tavily = _tavily_com_resultados([{"title": "Notícia qualquer", "content": "..."}])
    ai = FakeAI({"desatualizado": False, "alerta": None})

    alerta, _ = await verificar_atualidade("Tema X", "Previdenciário", ai, tavily)

    assert alerta is None


@pytest.mark.anyio
async def test_sem_resultados_de_busca_nao_gera_alerta():
    tavily = _tavily_com_resultados([])
    ai = FakeAI({"desatualizado": True, "alerta": "não deveria chamar a IA"})

    alerta, _ = await verificar_atualidade("Tema X", "Previdenciário", ai, tavily)

    assert alerta is None


@pytest.mark.anyio
async def test_falha_na_busca_nao_levanta_excecao():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    tavily = TavilyClient(api_key="chave", transport=httpx.MockTransport(handler))
    ai = FakeAI({"desatualizado": True, "alerta": "x"})

    alerta, verificado_em = await verificar_atualidade("Tema X", "Previdenciário", ai, tavily)

    assert alerta is None
    assert verificado_em is not None
