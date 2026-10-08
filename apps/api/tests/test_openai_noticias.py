import json

import httpx
import pytest

from app.integrations.noticias.openai_noticias import OpenAINoticias

TEXTO = (
    "- O TST garantiu estabilidade à gestante em contrato temporário em 07/10 ([tst.jus.br](https://www.tst.jus.br/n1?utm_source=openai)).\n"
    "- O INSS mudou a perícia em 06/10 ([gov.br](https://www.gov.br/inss/n2?utm_source=openai)).\n"
    "- Um link solto sem citação: https://inventado.com/x"
)


def _resposta():
    def anot(url, titulo):
        i = TEXTO.index(url)
        return {"type": "url_citation", "url": url, "title": titulo, "start_index": i - 15, "end_index": i + len(url)}

    return {
        "output": [
            {"type": "web_search_call", "status": "completed"},
            {"type": "message", "content": [{
                "type": "output_text", "text": TEXTO,
                "annotations": [
                    anot("https://www.tst.jus.br/n1?utm_source=openai", "TST garante estabilidade à gestante"),
                    anot("https://www.gov.br/inss/n2?utm_source=openai", "INSS muda perícia"),
                ],
            }]},
        ]
    }


@pytest.mark.anyio
async def test_cada_citacao_vira_uma_noticia_e_link_sem_citacao_fica_de_fora():
    pedidos = []

    def responder(request):
        pedidos.append(json.loads(request.content))
        return httpx.Response(200, json=_resposta())

    fonte = OpenAINoticias(api_key="k", model="gpt-4.1-mini", transport=httpx.MockTransport(responder))
    noticias = await fonte.buscar("gestante estabilidade", 7)

    assert [n.url for n in noticias] == ["https://www.tst.jus.br/n1", "https://www.gov.br/inss/n2"]
    assert noticias[0].titulo == "TST garante estabilidade à gestante"
    assert noticias[0].fonte == "tst.jus.br"
    assert "estabilidade à gestante" in noticias[0].trecho
    assert pedidos[0]["tools"][0]["type"] == "web_search"
    assert pedidos[0]["tools"][0]["user_location"]["country"] == "BR"
    assert "gestante estabilidade" in pedidos[0]["input"]


@pytest.mark.anyio
async def test_respeita_o_limite_de_buscas_por_ronda():
    chamadas = []

    def responder(request):
        chamadas.append(1)
        return httpx.Response(200, json={"output": []})

    fonte = OpenAINoticias(api_key="k", model="m", transport=httpx.MockTransport(responder), max_buscas=2)
    for c in ["a", "b", "c", "d"]:
        await fonte.buscar(c, 7)
    assert len(chamadas) == 2
