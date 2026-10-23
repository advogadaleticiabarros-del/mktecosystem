import json
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from app.integrations.social.tiktok_api import (
    ErroTikTok,
    TikTokAPI,
    TokensTikTok,
    partes_do_envio,
    renovar_tokens,
    trocar_code_por_tokens,
    url_autorizacao,
)


def test_url_de_autorizacao_tem_escopos_redirect_e_state():
    url = url_autorizacao("ck123", "https://api.x/integracoes/tiktok/callback", "estado")
    q = parse_qs(urlparse(url).query)
    assert url.startswith("https://www.tiktok.com/v2/auth/authorize/")
    assert q["client_key"] == ["ck123"] and q["response_type"] == ["code"] and q["state"] == ["estado"]
    assert "video.publish" in q["scope"][0] and "user.info.basic" in q["scope"][0]
    assert q["redirect_uri"] == ["https://api.x/integracoes/tiktok/callback"]


def _token_ok(request):
    corpo = parse_qs(request.content.decode())
    assert request.url.path == "/v2/oauth/token/"
    if corpo["grant_type"] == ["authorization_code"]:
        assert corpo["code"] == ["codigo"]
    else:
        assert corpo["refresh_token"] == ["rt-velho"]
    return httpx.Response(200, json={"access_token": "act.novo", "expires_in": 86400, "open_id": "oid-1",
                                     "refresh_token": "rt-novo", "refresh_expires_in": 31536000, "scope": "x"})


@pytest.mark.anyio
async def test_trocar_code_e_renovar_devolvem_tokens_com_validade():
    t = httpx.MockTransport(_token_ok)
    tok = await trocar_code_por_tokens("ck", "cs", "codigo", "https://api.x/cb", transport=t)
    assert isinstance(tok, TokensTikTok)
    assert tok.access_token == "act.novo" and tok.refresh_token == "rt-novo" and tok.open_id == "oid-1"
    assert tok.expira_em > tok.refresh_expira_em.replace(year=tok.refresh_expira_em.year - 2)
    novo = await renovar_tokens("ck", "cs", "rt-velho", transport=t)
    assert novo.access_token == "act.novo"
    assert TokensTikTok.de_json(novo.para_json()) == novo


@pytest.mark.anyio
async def test_erro_da_tiktok_vira_erro_legivel():
    t = httpx.MockTransport(lambda r: httpx.Response(200, json={"error": "invalid_grant", "error_description": "Code expired"}))
    with pytest.raises(ErroTikTok, match="Code expired"):
        await trocar_code_por_tokens("ck", "cs", "codigo", "https://api.x/cb", transport=t)


def test_partes_do_envio_seguem_a_regra_da_tiktok():
    assert partes_do_envio(3_000_000) == (3_000_000, 1)
    assert partes_do_envio(25_000_000) == (10_000_000, 2)  # a sobra de 5 MB vai na última parte
    assert partes_do_envio(82_000_000) == (10_000_000, 8)


def _tiktok(publico_permitido=True, auditado=True, finais=("PROCESSING_UPLOAD", "PUBLISH_COMPLETE")):
    chamadas, envios = [], []
    status = iter(finais)
    ok = {"error": {"code": "ok", "message": ""}}

    def responder(request):
        if request.url.host == "upload.tiktok":
            envios.append((request.headers["Content-Range"], len(request.content)))
            return httpx.Response(201)
        chamadas.append(request.url.path)
        assert request.headers["Authorization"] == "Bearer act.x"
        if request.url.path == "/v2/post/publish/creator_info/query/":
            opcoes = ["PUBLIC_TO_EVERYONE", "SELF_ONLY"] if publico_permitido else ["SELF_ONLY"]
            return httpx.Response(200, json={"data": {"privacy_level_options": opcoes}, **ok})
        if request.url.path == "/v2/post/publish/video/init/":
            if not auditado:
                return httpx.Response(403, json={"error": {"code": "unaudited_client_can_only_post_to_private_accounts",
                                                           "message": "Please review our integration guidelines"}})
            corpo = json.loads(request.content)
            assert corpo["post_info"]["privacy_level"] == "PUBLIC_TO_EVERYONE" and corpo["post_info"]["title"] == "Legenda"
            assert corpo["post_info"]["is_aigc"] is True
            assert corpo["source_info"] == {"source": "FILE_UPLOAD", "video_size": 25_000_000,
                                            "chunk_size": 10_000_000, "total_chunk_count": 2}
            return httpx.Response(200, json={"data": {"publish_id": "p-1", "upload_url": "https://upload.tiktok/u"}, **ok})
        if request.url.path == "/v2/post/publish/inbox/video/init/":
            assert json.loads(request.content)["source_info"]["source"] == "FILE_UPLOAD"
            return httpx.Response(200, json={"data": {"publish_id": "p-2", "upload_url": "https://upload.tiktok/u"}, **ok})
        if request.url.path == "/v2/post/publish/status/fetch/":
            return httpx.Response(200, json={"data": {"status": next(status), "publicaly_available_post_id": [123]}, **ok})
        raise AssertionError(request.url.path)

    return httpx.MockTransport(responder), chamadas, envios


@pytest.mark.anyio
async def test_app_auditado_publica_direto_e_publico_enviando_o_arquivo_em_partes():
    transporte, chamadas, envios = _tiktok()
    api = TikTokAPI("act.x", transport=transporte, espera=0)
    r = await api.publicar_video(b"v" * 25_000_000, "Legenda", ia=True)
    assert r == {"modo": "publico", "publish_id": "p-1", "privacidade": "PUBLIC_TO_EVERYONE", "post_id": "123"}
    assert envios == [("bytes 0-9999999/25000000", 10_000_000), ("bytes 10000000-24999999/25000000", 15_000_000)]


@pytest.mark.anyio
async def test_app_sem_auditoria_manda_para_a_caixa_de_rascunhos_do_tiktok():
    transporte, chamadas, envios = _tiktok(auditado=False, finais=("PROCESSING_UPLOAD", "SEND_TO_USER_INBOX"))
    api = TikTokAPI("act.x", transport=transporte, espera=0)
    r = await api.publicar_video(b"v" * 25_000_000, "Legenda", ia=True)
    assert r["modo"] == "rascunho" and r["publish_id"] == "p-2" and r["privacidade"] is None
    assert "/v2/post/publish/inbox/video/init/" in chamadas and len(envios) == 2


@pytest.mark.anyio
async def test_conta_sem_opcao_publica_tambem_vai_para_o_rascunho():
    transporte, chamadas, _ = _tiktok(publico_permitido=False, finais=("SEND_TO_USER_INBOX",))
    r = await TikTokAPI("act.x", transport=transporte, espera=0).publicar_video(b"v" * 1000, "Legenda")
    assert r["modo"] == "rascunho" and "/v2/post/publish/video/init/" not in chamadas


@pytest.mark.anyio
async def test_outros_erros_da_tiktok_nao_viram_rascunho():
    def recusa(request):
        if request.url.path.endswith("creator_info/query/"):
            return httpx.Response(401, json={"error": {"code": "access_token_invalid", "message": "expired"}})
        raise AssertionError(request.url.path)

    with pytest.raises(ErroTikTok, match="access_token_invalid"):
        await TikTokAPI("act.x", transport=httpx.MockTransport(recusa), espera=0).publicar_video(b"v", "L")
