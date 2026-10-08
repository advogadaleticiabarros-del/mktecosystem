import httpx
import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.chave_api import ChaveApi
from app.models.tenant import Tenant
from app.models.user import User
from app.services.chaves_api import ChaveRecusada, obter_chave, salvar_chave, status_chaves, validar_openai


async def _tenant(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    user = User(tenant_id=tenant.id, email="l@x.com", nome="L", hashed_password=hash_password("x"), role="owner")
    db.add(user)
    await db.commit()
    return tenant, {"Authorization": f"Bearer {create_access_token(user.id)}"}


async def aceita(*_):
    return None


async def recusa(*_):
    raise ChaveRecusada("A OpenAI recusou essa chave.")


@pytest.mark.anyio
async def test_salva_criptografada_e_so_mostra_o_final(db_session):
    tenant, _ = await _tenant(db_session)

    status = await salvar_chave(db_session, tenant.id, "openai", "  sk-proj-abc123XYZ9  ", validar=aceita)

    assert status["configurada"] and status["final"] == "XYZ9"
    linha = (await db_session.execute(select(ChaveApi))).scalar_one()
    assert "sk-proj" not in linha.chave_criptografada
    assert await obter_chave(db_session, tenant.id, "openai") == "sk-proj-abc123XYZ9"
    [s] = await status_chaves(db_session, tenant.id)
    assert s["provedor"] == "openai" and s["final"] == "XYZ9" and "chave" not in s


@pytest.mark.anyio
async def test_chave_recusada_nao_e_salva(db_session):
    tenant, _ = await _tenant(db_session)
    with pytest.raises(ChaveRecusada):
        await salvar_chave(db_session, tenant.id, "openai", "sk-ruim", validar=recusa)
    assert (await db_session.execute(select(ChaveApi))).scalars().all() == []


@pytest.mark.anyio
async def test_trocar_a_chave_substitui_a_anterior(db_session):
    tenant, _ = await _tenant(db_session)
    await salvar_chave(db_session, tenant.id, "openai", "sk-antiga-1111", validar=aceita)
    await salvar_chave(db_session, tenant.id, "openai", "sk-nova-2222", validar=aceita)
    assert len((await db_session.execute(select(ChaveApi))).scalars().all()) == 1
    assert await obter_chave(db_session, tenant.id, "openai") == "sk-nova-2222"


@pytest.mark.anyio
async def test_validar_openai_consulta_a_lista_de_modelos():
    def responder(request):
        assert request.url.path == "/v1/models"
        ok = request.headers["Authorization"] == "Bearer boa"
        return httpx.Response(200 if ok else 401, json={})

    t = httpx.MockTransport(responder)
    await validar_openai("boa", transport=t)
    with pytest.raises(ChaveRecusada):
        await validar_openai("ruim", transport=t)


@pytest.mark.anyio
async def test_rotas_salvam_listam_e_removem_sem_devolver_a_chave(client, db_session, monkeypatch):
    tenant, headers = await _tenant(db_session)
    monkeypatch.setitem(__import__("app.services.chaves_api", fromlist=["x"]).PROVEDORES["openai"], "validar", aceita)

    r = await client.put("/chaves/openai", json={"chave": "sk-proj-zzz-ABCD"}, headers=headers)
    assert r.status_code == 200 and r.json()["final"] == "ABCD"
    lista = await client.get("/chaves", headers=headers)
    assert "sk-proj" not in lista.text and lista.json()[0]["configurada"]
    assert (await client.delete("/chaves/openai", headers=headers)).status_code == 204
    assert not (await client.get("/chaves", headers=headers)).json()[0]["configurada"]


@pytest.mark.anyio
async def test_rota_com_chave_recusada_responde_422_com_explicacao(client, db_session, monkeypatch):
    tenant, headers = await _tenant(db_session)
    monkeypatch.setitem(__import__("app.services.chaves_api", fromlist=["x"]).PROVEDORES["openai"], "validar", recusa)
    r = await client.put("/chaves/openai", json={"chave": "sk-ruim-123456"}, headers=headers)
    assert r.status_code == 422 and "recusou" in r.json()["detail"]
