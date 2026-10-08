import httpx
import pytest

from app.integrations.social.instagram_api import InstagramAPI


@pytest.mark.anyio
async def test_carrossel_envia_legenda_no_container_pai():
    enviados = []

    def responder(request: httpx.Request) -> httpx.Response:
        dados = dict(httpx.QueryParams(request.content.decode()))
        enviados.append((request.url.path, dados))
        return httpx.Response(200, json={"id": f"c{len(enviados)}"})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    post_id = await api.publicar_carrossel("999", ["https://x/1.png", "https://x/2.png"], legenda="Minha legenda")

    pai = next(d for p, d in enviados if d.get("media_type") == "CAROUSEL")
    assert pai["caption"] == "Minha legenda"
    assert pai["children"] == "c1,c2"
    assert enviados[-1][0].endswith("/999/media_publish")
    assert post_id == "c4"
