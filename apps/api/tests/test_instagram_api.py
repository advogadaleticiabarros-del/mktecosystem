import httpx
import pytest

from app.integrations.social.instagram_api import InstagramAPI


@pytest.mark.anyio
async def test_carrossel_envia_legenda_no_container_pai():
    enviados = []

    def responder(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(200, json={"status_code": "FINISHED"})
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


@pytest.mark.anyio
async def test_listar_publicacoes_pagina_e_junta_insights():
    def responder(request: httpx.Request) -> httpx.Response:
        path, q = request.url.path, dict(request.url.params)
        if path.endswith("/999/media") and "after" not in q:
            return httpx.Response(200, json={
                "data": [{"id": "m1", "media_type": "VIDEO", "media_product_type": "REELS",
                          "timestamp": "2026-05-28T23:00:00+0000", "caption": "Grávida", "permalink": "p1"}],
                "paging": {"cursors": {"after": "X"}, "next": "https://graph.facebook.com/v21.0/999/media?after=X"},
            })
        if path.endswith("/999/media"):
            return httpx.Response(200, json={"data": [{"id": "m2", "media_type": "CAROUSEL_ALBUM",
                                                       "media_product_type": "FEED",
                                                       "timestamp": "2026-08-10T15:00:00+0000"}]})
        if path.endswith("/m1/insights"):
            return httpx.Response(200, json={"data": [{"name": "reach", "values": [{"value": 900}]},
                                                      {"name": "shares", "values": [{"value": 5}]}]})
        if path.endswith("/m2/insights"):
            return httpx.Response(200, json={"data": [{"name": "reach", "values": [{"value": 100}]},
                                                      {"name": "follows", "values": [{"value": 3}]}]})
        return httpx.Response(404, json={})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    posts = await api.listar_publicacoes("999")

    assert [p["id"] for p in posts] == ["m1", "m2"]
    assert posts[0]["insights"] == {"reach": 900, "shares": 5}
    assert posts[1]["insights"]["follows"] == 3


@pytest.mark.anyio
async def test_insight_que_falha_nao_derruba_a_lista():
    def responder(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/999/media"):
            return httpx.Response(200, json={"data": [{"id": "m1", "media_type": "IMAGE", "media_product_type": "FEED",
                                                       "timestamp": "2026-08-10T15:00:00+0000"}]})
        return httpx.Response(400, json={"error": {"message": "metric not supported"}})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    posts = await api.listar_publicacoes("999")
    assert posts[0]["insights"] == {}


@pytest.mark.anyio
async def test_raio_x_da_conta_junta_perfil_series_totais_e_publico():
    def responder(request: httpx.Request) -> httpx.Response:
        path, q = request.url.path, dict(request.url.params)
        if path.endswith("/999") :
            return httpx.Response(200, json={"followers_count": 416, "follows_count": 442, "media_count": 295})
        if path.endswith("/999/insights"):
            m = q["metric"]
            if m == "follower_demographics":
                bd = q["breakdown"]
                chave = {"city": "Vitória, Espírito Santo", "age": "25-34", "gender": "F"}[bd]
                return httpx.Response(200, json={"data": [{"total_value": {"breakdowns": [
                    {"results": [{"dimension_values": [chave], "value": 10}]}]}}]})
            if q.get("metric_type") == "total_value":
                return httpx.Response(200, json={"data": [{"name": n, "total_value": {"value": 7}} for n in m.split(",")]})
            return httpx.Response(200, json={"data": [{"name": m, "values": [
                {"value": 3, "end_time": "2026-10-07T07:00:00+0000"}]}]})
        return httpx.Response(404, json={})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    raio_x = await api.buscar_raio_x("999")

    assert raio_x["perfil"]["followers_count"] == 416
    assert raio_x["totais_30d"]["reach"] == 7
    assert raio_x["serie_alcance"][-1] == ["2026-10-07", 3]
    assert raio_x["serie_seguidores"] == [["2026-10-07", 3]]
    assert raio_x["demografia"]["cidades"] == {"Vitória, Espírito Santo": 10}
    assert raio_x["demografia"]["genero"] == {"F": 10}


@pytest.mark.anyio
async def test_espera_a_meta_processar_antes_de_publicar(monkeypatch):
    estados = iter(["IN_PROGRESS", "IN_PROGRESS", "FINISHED"])
    ordem = []

    def responder(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            ordem.append("status")
            return httpx.Response(200, json={"status_code": next(estados)})
        ordem.append(request.url.path.rsplit("/", 1)[-1])
        return httpx.Response(200, json={"id": "c1"})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    monkeypatch.setattr(api, "_espera_segundos", 0)
    await api.publicar_imagem_unica("999", "https://x/1.jpg", legenda="L")

    assert ordem == ["media", "status", "status", "status", "media_publish"]


@pytest.mark.anyio
async def test_imagem_recusada_pela_meta_vira_erro(monkeypatch):
    def responder(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(200, json={"status_code": "ERROR"})
        return httpx.Response(200, json={"id": "c1"})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    monkeypatch.setattr(api, "_espera_segundos", 0)
    with pytest.raises(RuntimeError):
        await api.publicar_imagem_unica("999", "https://x/1.jpg")


@pytest.mark.anyio
async def test_comentar_publica_comentario_no_proprio_post():
    enviados = []

    def responder(request: httpx.Request) -> httpx.Response:
        enviados.append((request.url.path, dict(httpx.QueryParams(request.content.decode()))))
        return httpx.Response(200, json={"id": "coment_1"})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    comentario_id = await api.comentar("post_123", "Base legal: art. 7º da CF.")

    caminho, dados = enviados[0]
    assert caminho.endswith("/post_123/comments")
    assert dados["message"] == "Base legal: art. 7º da CF."
    assert comentario_id == "coment_1"


@pytest.mark.anyio
async def test_reels_cria_container_de_video_espera_processar_e_publica(monkeypatch):
    """Reels pela Graph API: container media_type=REELS com video_url e legenda,
    espera o vídeo ficar FINISHED (demora mais que imagem) e só então publica."""
    estados = iter(["IN_PROGRESS", "FINISHED"])
    enviados = []

    def responder(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(200, json={"status_code": next(estados)})
        enviados.append((request.url.path, dict(httpx.QueryParams(request.content.decode()))))
        return httpx.Response(200, json={"id": f"r{len(enviados)}"})

    api = InstagramAPI("tok", transport=httpx.MockTransport(responder))
    monkeypatch.setattr(api, "_espera_segundos", 0)
    post_id = await api.publicar_reels("999", "https://x/reel.mp4", legenda="Legenda do reel")

    caminho, dados = enviados[0]
    assert caminho.endswith("/999/media")
    assert dados["media_type"] == "REELS"
    assert dados["video_url"] == "https://x/reel.mp4"
    assert dados["caption"] == "Legenda do reel"
    assert dados["share_to_feed"] == "true"
    assert enviados[-1] == ("/v21.0/999/media_publish", {"creation_id": "r1", "access_token": "tok"})
    assert post_id == "r2"
