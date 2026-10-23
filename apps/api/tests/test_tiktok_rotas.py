from datetime import date
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from app.core.security import create_access_token, hash_password
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant
from app.models.user import User
from app.services.chaves_api import salvar_chave


def _tiktok_falso(pedidos):
    def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        if request.url.path == "/v2/oauth/token/":
            return httpx.Response(200, json={"access_token": "act.1", "expires_in": 86400, "open_id": "oid-9",
                                             "refresh_token": "rt.1", "refresh_expires_in": 31536000})
        if request.url.path == "/v2/user/info/":
            return httpx.Response(200, json={"data": {"user": {"open_id": "oid-9", "display_name": "Letícia Barros"}},
                                             "error": {"code": "ok"}})
        return httpx.Response(404)

    return httpx.MockTransport(handler)


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    user = User(tenant_id=tenant.id, email="l@example.com", nome="L", hashed_password=hash_password("s"), role="owner")
    db.add(user)
    await db.commit()

    async def aceita(_chave):
        return None

    await salvar_chave(db, tenant.id, "tiktok", "awkey123 segredoabc456", validar=aceita)
    return tenant, user, {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.mark.anyio
async def test_conectar_ver_rascunho_e_marcar_publicado(client, db_session):
    tenant, user, auth = await _setup(db_session)
    token = create_access_token(user.id)
    inicio = await client.get(f"/integracoes/tiktok/iniciar?token={token}", follow_redirects=False)
    assert inicio.status_code == 307
    q = parse_qs(urlparse(inicio.headers["location"]).query)
    assert q["client_key"] == ["awkey123"] and q["scope"] == ["user.info.basic,video.upload,video.publish"]
    assert q["redirect_uri"][0].endswith("/integracoes/tiktok/callback")

    pedidos = []
    with patch("app.routers.integracoes.tiktok_transport", return_value=_tiktok_falso(pedidos)):
        cb = await client.get(f"/integracoes/tiktok/callback?code=c1&state={token}", follow_redirects=False)
    assert cb.status_code == 307 and cb.headers["location"].endswith("conectado=tiktok")
    assert b"client_secret=segredoabc456" in next(p for p in pedidos if p.url.path == "/v2/oauth/token/").content

    situacao = (await client.get("/tiktok", headers=auth)).json()
    assert situacao["conectado"] is True and situacao["nome"] == "Letícia Barros" and situacao["no_rascunho"] == []

    pauta = Pauta(tenant_id=tenant.id, titulo="Tema", angulo="reels", area="Família", origem="manual", fonte="manual",
                  relevante_para_conteudo=True)
    db_session.add(pauta)
    await db_session.flush()
    piece = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo="reels", status="aprovado", versao=1,
                         corpo={"video": "https://x/v.mp4", "legenda": "Legenda", "tiktok": {"status": "no_rascunho"}})
    db_session.add(piece)
    await db_session.flush()
    db_session.add(ScheduledPost(tenant_id=tenant.id, content_piece_id=piece.id, titulo="Reels X", canal="instagram",
                                 formato="reels", data_agendada=date.today(), horario="21:00", status="publicado"))
    await db_session.commit()

    rascunhos = (await client.get("/tiktok", headers=auth)).json()["no_rascunho"]
    assert [(r["titulo"], r["legenda"]) for r in rascunhos] == [("Reels X", "Legenda")]
    assert (await client.post(f"/tiktok/{piece.id}/publicado", headers=auth)).status_code == 204
    assert (await client.get("/tiktok", headers=auth)).json()["no_rascunho"] == []
    assert (await client.post(f"/tiktok/{piece.id}/publicado", headers=auth)).status_code == 404
    # já enviado: não dá mais para remarcar
    assert (await client.put(f"/tiktok/{piece.id}/agenda", headers=auth,
                             json={"data": "2026-11-01", "horario": "10:00"})).status_code == 404

    outro = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo="tiktok", status="aprovado", versao=1,
                         corpo={"video": "https://x/c.mp4", "titulo": "Corte"})
    db_session.add(outro)
    await db_session.commit()
    assert (await client.put(f"/tiktok/{outro.id}/agenda", headers=auth,
                             json={"data": "2026-11-01", "horario": "10:00"})).status_code == 204
    fila = (await client.get("/tiktok", headers=auth)).json()["fila"]
    assert [(f["titulo"], f["data"], f["horario"]) for f in fila] == [("Corte", "2026-11-01", "10:00")]
    assert (await client.put(f"/tiktok/{outro.id}/agenda", headers=auth, json={"data": None})).status_code == 204
    assert (await client.get("/tiktok", headers=auth)).json()["fila"] == []

    assert (await client.delete("/integracoes/tiktok", headers=auth)).status_code == 204
    assert (await client.get("/tiktok", headers=auth)).json()["conectado"] is False


@pytest.mark.anyio
async def test_recusa_na_autorizacao_volta_com_erro(client, db_session):
    _, user, _ = await _setup(db_session)
    r = await client.get(f"/integracoes/tiktok/callback?error=access_denied&state={create_access_token(user.id)}",
                         follow_redirects=False)
    assert r.headers["location"].endswith("erro=tiktok")
