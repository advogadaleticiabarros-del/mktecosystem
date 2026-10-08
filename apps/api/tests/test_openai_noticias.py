import json

import httpx
import pytest

from app.integrations.noticias.openai_noticias import OpenAINoticias


def _resposta(noticias, citadas):
    texto = json.dumps({"noticias": noticias})
    return {
        "output": [
            {"type": "web_search_call", "status": "completed"},
            {"type": "message", "content": [{
                "type": "output_text", "text": texto,
                "annotations": [{"type": "url_citation", "url": u} for u in citadas],
            }]},
        ]
    }


@pytest.mark.anyio
async def test_so_ficam_links_citados_de_verdade_pela_busca():
    pedidos = []

    def responder(request):
        pedidos.append(json.loads(request.content))
        return httpx.Response(200, json=_resposta(
            [
                {"titulo": "TST decide sobre gestante", "url": "https://www.tst.jus.br/n1", "veiculo": "TST",
                 "data": "2026-10-07", "trecho": "Decisão da SDI-1"},
                {"titulo": "Link inventado", "url": "https://inventado.com/x", "veiculo": "?", "data": None, "trecho": ""},
            ],
            citadas=["https://www.tst.jus.br/n1?utm_source=openai"],
        ))

    fonte = OpenAINoticias(api_key="k", model="gpt-4.1-mini", transport=httpx.MockTransport(responder))
    noticias = await fonte.buscar("gestante estabilidade", 7)

    assert [n.url for n in noticias] == ["https://www.tst.jus.br/n1"]
    assert noticias[0].fonte == "TST" and noticias[0].publicado_em.day == 7
    assert pedidos[0]["tools"] == [{"type": "web_search"}]
    assert "gestante estabilidade" in pedidos[0]["input"]


@pytest.mark.anyio
async def test_respeita_o_limite_de_buscas_por_ronda():
    chamadas = []

    def responder(request):
        chamadas.append(1)
        return httpx.Response(200, json=_resposta([], []))

    fonte = OpenAINoticias(api_key="k", model="m", transport=httpx.MockTransport(responder), max_buscas=2)
    for c in ["a", "b", "c", "d"]:
        await fonte.buscar(c, 7)
    assert len(chamadas) == 2
