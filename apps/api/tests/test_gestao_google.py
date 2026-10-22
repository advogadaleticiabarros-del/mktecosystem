import json

import httpx
import pytest

from app.integrations.social.google_api import GoogleApi
from app.services import gestao_google as g


def _api(handler) -> GoogleApi:
    return GoogleApi("t", transport=httpx.MockTransport(handler))


@pytest.mark.anyio
async def test_publicar_post_com_botao_e_foto():
    pedidos = []

    def handler(request):
        pedidos.append(request)
        return httpx.Response(200, json={"name": "accounts/1/locations/2/localPosts/9", "searchUrl": "https://g/p"})

    resultado = await g.publicar_post(_api(handler), "accounts/1", "locations/2", "A lei prevê estabilidade.",
                                      "LEARN_MORE", "https://site/blog", "https://api/media/a.jpg")
    assert resultado == {"name": "accounts/1/locations/2/localPosts/9", "link": "https://g/p"}
    corpo = json.loads(pedidos[0].content)
    assert str(pedidos[0].url) == "https://mybusiness.googleapis.com/v4/accounts/1/locations/2/localPosts"
    assert corpo["callToAction"] == {"actionType": "LEARN_MORE", "url": "https://site/blog"}
    assert corpo["media"] == [{"mediaFormat": "PHOTO", "sourceUrl": "https://api/media/a.jpg"}]


@pytest.mark.anyio
async def test_texto_proibido_pela_oab_nao_chega_no_google():
    def handler(request):
        raise AssertionError("não deveria chamar o Google")

    with pytest.raises(g.TextoBloqueadoOab):
        await g.publicar_post(_api(handler), "a", "l", "Consulta grátis, ganhe sua causa!")
    with pytest.raises(g.TextoBloqueadoOab):
        await g.responder_avaliacao(_api(handler), "a/l/reviews/1", "Que bom que ganhamos seu processo!")


@pytest.mark.anyio
async def test_editar_perfil_so_muda_o_que_foi_passado_e_preserva_servicos_estruturados():
    pedidos = []

    def handler(request):
        pedidos.append(request)
        if request.method == "GET":
            return httpx.Response(200, json={
                "categories": {"primaryCategory": {"name": "categories/gcid:labor_relations_attorney"}},
                "serviceItems": [{"structuredServiceItem": {"serviceTypeId": "job_x"}},
                                 {"freeFormServiceItem": {"label": {"displayName": "Velho"}}}],
            })
        return httpx.Response(200, json={})

    mascara = await g.editar_perfil(_api(handler), "locations/2", site="https://s/?utm_source=google",
                                    servicos=[{"nome": "Rescisão indireta", "descricao": "Quando a empresa erra."}])
    assert mascara == ["websiteUri", "serviceItems"]
    patch = pedidos[-1]
    assert patch.method == "PATCH" and patch.url.params["updateMask"] == "websiteUri,serviceItems"
    itens = json.loads(patch.content)["serviceItems"]
    assert itens[0] == {"structuredServiceItem": {"serviceTypeId": "job_x"}}
    assert itens[1]["freeFormServiceItem"]["category"] == "categories/gcid:labor_relations_attorney"
    assert itens[1]["freeFormServiceItem"]["label"]["displayName"] == "Rescisão indireta"
    assert len(itens) == 2


@pytest.mark.anyio
async def test_definir_botao_atualiza_o_existente():
    pedidos = []

    def handler(request):
        pedidos.append(request)
        if request.method == "GET":
            return httpx.Response(200, json={"placeActionLinks": [
                {"name": "locations/2/placeActionLinks/5", "placeActionType": "APPOINTMENT", "isEditable": True}]})
        return httpx.Response(200, json={"name": "locations/2/placeActionLinks/5"})

    await g.definir_botao(_api(handler), "locations/2", "APPOINTMENT", "https://wa.me/1")
    assert pedidos[-1].method == "PATCH"
    assert str(pedidos[-1].url).startswith("https://mybusinessplaceactions.googleapis.com/v1/locations/2/placeActionLinks/5")


class IaFalsa:
    def __init__(self, respostas):
        self.respostas = list(respostas)
        self.prompts = []

    async def generate_text(self, prompt):
        self.prompts.append(prompt)
        return self.respostas.pop(0)

    async def generate_json(self, prompt):
        return {}


@pytest.mark.anyio
async def test_rascunho_da_ia_e_refeito_quando_fere_a_oab():
    ia = IaFalsa(["Obrigada! Que bom que seu processo deu certo.", "Obrigada pela confiança, Ana!"])
    texto = await g.sugerir_resposta(ia, {"autor": "Ana", "nota": 5, "comentario": "Ótima"})
    assert texto == "Obrigada pela confiança, Ana!"
    assert "recusada" in ia.prompts[1]
