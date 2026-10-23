import json
from datetime import date

import httpx
import pytest

from app.integrations.social import linkedin_api as li


def test_escapar_texto_mantem_hashtags_clicaveis():
    texto = "Lei 15.371 (licença) e o art. 477 [CLT] #RH #DireitoDoTrabalho"
    assert li.escapar_texto(texto) == (
        "Lei 15.371 \\(licença\\) e o art. 477 \\[CLT\\] {hashtag|\\#|RH} {hashtag|\\#|DireitoDoTrabalho}"
    )
    assert li.escapar_texto("e-mail@exemplo_x") == "e-mail\\@exemplo\\_x"


def test_escapar_texto_mantem_mencao_da_pagina():
    texto = "Siga @[Letícia Barros Advocacia e Consultoria Jurídica](urn:li:organization:123) (página) #RH"
    assert li.escapar_texto(texto) == (
        "Siga @[Letícia Barros Advocacia e Consultoria Jurídica](urn:li:organization:123) \\(página\\) "
        "{hashtag|\\#|RH}")


def test_url_autorizacao_pede_os_escopos_do_perfil():
    url = li.url_autorizacao("abc", "https://api/cb", "estado")
    assert url.startswith("https://www.linkedin.com/oauth/v2/authorization?")
    assert "scope=openid+profile+w_member_social" in url and "state=estado" in url


@pytest.mark.anyio
async def test_credenciais_validas_so_recusa_invalid_client():
    def recusa(request):
        return httpx.Response(401, json={"error": "invalid_client", "error_description": "Client authentication failed"})

    def app_comum(request):
        return httpx.Response(401, json={"error": "access_denied",
                                         "error_description": "This application is not allowed to create application tokens"})

    assert await li.credenciais_validas("x", "y", transport=httpx.MockTransport(recusa)) is False
    assert await li.credenciais_validas("x", "y", transport=httpx.MockTransport(app_comum)) is True


@pytest.mark.anyio
async def test_publicar_com_card_do_artigo_e_capa():
    pedidos = []

    def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        if request.url.path == "/rest/images":
            return httpx.Response(200, json={"value": {"uploadUrl": "https://upload.linkedin/x", "image": "urn:li:image:C1"}})
        if request.url.host == "upload.linkedin":
            return httpx.Response(201)
        if request.url.path == "/rest/posts":
            return httpx.Response(201, headers={"x-restli-id": "urn:li:share:99"})
        return httpx.Response(404)

    api = li.LinkedInApi("tok", transport=httpx.MockTransport(handler), hoje=date(2026, 10, 22))
    urn = await api.publicar("urn:li:person:abc", "Texto (com parênteses) #RH", {
        "link": "https://site/blog/x.html", "titulo": "Título", "descricao": "Desc", "capa": b"jpg"})
    assert urn == "urn:li:share:99"
    post = next(p for p in pedidos if p.url.path == "/rest/posts")
    corpo = json.loads(post.content)
    assert post.headers["LinkedIn-Version"] == "202608"
    assert post.headers["X-Restli-Protocol-Version"] == "2.0.0"
    assert corpo["author"] == "urn:li:person:abc" and corpo["visibility"] == "PUBLIC"
    assert corpo["commentary"] == "Texto \\(com parênteses\\) {hashtag|\\#|RH}"
    assert corpo["content"]["article"] == {"source": "https://site/blog/x.html", "title": "Título",
                                           "description": "Desc", "thumbnail": "urn:li:image:C1"}
    envio = next(p for p in pedidos if p.url.host == "upload.linkedin")
    assert envio.method == "PUT" and envio.content == b"jpg"


@pytest.mark.anyio
async def test_versao_inexistente_recua_um_mes():
    versoes = []

    def handler(request):
        versoes.append(request.headers["LinkedIn-Version"])
        if len(versoes) < 3:
            return httpx.Response(426, json={"code": "NONEXISTENT_VERSION"})
        return httpx.Response(201, headers={"x-restli-id": "urn:li:share:1"})

    api = li.LinkedInApi("tok", transport=httpx.MockTransport(handler), hoje=date(2026, 1, 15))
    assert await api.publicar("urn:li:person:a", "oi") == "urn:li:share:1"
    assert versoes == ["202511", "202510", "202509"]
    assert api.versao == "202509"


@pytest.mark.anyio
async def test_token_vencido_pede_reconexao():
    api = li.LinkedInApi("tok", transport=httpx.MockTransport(lambda r: httpx.Response(401, json={})))
    with pytest.raises(li.LinkedInErro) as erro:
        await api.publicar("urn:li:person:a", "oi")
    assert erro.value.reconectar is True
