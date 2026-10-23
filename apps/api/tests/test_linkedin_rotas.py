import json
from datetime import date, datetime, timedelta, timezone
from unittest.mock import patch

import httpx
import pytest

from app.core.crypto import encrypt_token
from app.core.security import create_access_token, hash_password
from app.models.presenca_google import LinkedInPost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant
from app.models.user import User
from app.services import linkedin
from app.services.chaves_api import salvar_chave

ARTIGO = """<html><head><title>Artigo X | Dra. Letícia Barros</title>
<meta name="description" content="Descrição do artigo">
<meta property="og:image" content="https://advogadaleticiabarros.com.br/blog/capas/x.jpg"></head><body></body></html>"""


class SiteFalso:
    def __init__(self, arquivos):
        self.arquivos = arquivos
        self.binarios = {"blog/capas/x.jpg": b"capa"}

    async def ler(self, caminho):
        return self.arquivos.get(caminho)

    async def ler_bytes(self, caminho):
        return self.binarios.get(caminho)

    async def listar_html(self):
        return list(self.arquivos)


def _linkedin_falso(pedidos):
    def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        if request.url.path == "/oauth/v2/accessToken":
            return httpx.Response(200, json={"access_token": "tok-li", "expires_in": 5184000})
        if request.url.path == "/v2/userinfo":
            return httpx.Response(200, json={"sub": "abc123", "name": "Letícia Barros"})
        if request.url.path == "/rest/images":
            return httpx.Response(200, json={"value": {"uploadUrl": "https://up.linkedin/1", "image": "urn:li:image:9"}})
        if request.url.host == "up.linkedin":
            return httpx.Response(201)
        if request.url.path == "/rest/posts":
            return httpx.Response(201, headers={"x-restli-id": "urn:li:share:77"})
        return httpx.Response(404)

    return httpx.MockTransport(handler)


async def _setup(db, conectado=True, expira_em=None):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    user = User(tenant_id=tenant.id, email="l@example.com", nome="L", hashed_password=hash_password("s"), role="owner")
    db.add(user)
    if conectado:
        db.add(SocialConnection(tenant_id=tenant.id, plataforma="linkedin", page_id="urn:li:person:abc123", ig_user_id="",
                                nome_conta="Letícia Barros", access_token_encrypted=encrypt_token("tok-li"), status="ativo",
                                expira_em=expira_em or datetime.now(timezone.utc) + timedelta(days=50)))
    await db.commit()

    async def aceita(_chave):
        return None

    await salvar_chave(db, tenant.id, "linkedin", "77ke7bdixbp3dw segredoxyz12345", validar=aceita)
    return tenant, user, {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.mark.anyio
async def test_conectar_pelo_oauth_guarda_o_perfil(client, db_session):
    tenant, user, auth = await _setup(db_session, conectado=False)
    token = create_access_token(user.id)
    inicio = await client.get(f"/integracoes/linkedin/iniciar?token={token}", follow_redirects=False)
    assert inicio.status_code == 307
    assert "client_id=77ke7bdixbp3dw" in inicio.headers["location"]
    assert "integracoes%2Flinkedin%2Fcallback" in inicio.headers["location"]

    pedidos = []
    with patch("app.routers.integracoes.linkedin_transport", return_value=_linkedin_falso(pedidos)):
        cb = await client.get(f"/integracoes/linkedin/callback?code=c1&state={token}", follow_redirects=False)
    assert cb.status_code == 307 and cb.headers["location"].endswith("conectado=linkedin")
    troca = next(p for p in pedidos if p.url.path == "/oauth/v2/accessToken")
    assert b"client_secret=segredoxyz12345" in troca.content

    situacao = (await client.get("/linkedin", headers=auth)).json()
    assert situacao["conectado"] is True and situacao["nome"] == "Letícia Barros"
    assert situacao["dias_para_vencer"] in (59, 60)


@pytest.mark.anyio
async def test_fila_oab_e_publicar_agora_com_card_do_artigo(client, db_session):
    _, _, auth = await _setup(db_session)
    bloqueado = await client.post("/linkedin/posts", headers=auth,
                                  json={"texto": "Consulta grátis para sua empresa!", "status": "aprovado"})
    assert bloqueado.status_code == 422

    post = (await client.post("/linkedin/posts", headers=auth, json={
        "texto": "A escala 6x1 acabou. Veja o que muda (prazos) #RH",
        "link": "https://advogadaleticiabarros.com.br/blog/x.html"})).json()
    assert post["status"] == "rascunho"

    pedidos = []
    site = SiteFalso({"blog/x.html": ARTIGO})
    with patch("app.routers.linkedin.linkedin_transport", return_value=_linkedin_falso(pedidos)), \
            patch("app.routers.linkedin._site_padrao", return_value=site):
        r = await client.post(f"/linkedin/posts/{post['id']}/publicar-agora", headers=auth)
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "publicado"
    assert r.json()["link_publicado"] == "https://www.linkedin.com/feed/update/urn:li:share:77/"
    corpo = json.loads(next(p for p in pedidos if p.url.path == "/rest/posts").content)
    assert corpo["author"] == "urn:li:person:abc123"
    assert corpo["commentary"] == "A escala 6x1 acabou. Veja o que muda \\(prazos\\) {hashtag|\\#|RH}"
    card = corpo["content"]["article"]
    assert card["source"].startswith("https://advogadaleticiabarros.com.br/blog/x.html?utm_source=linkedin"
                                     "&utm_medium=social&utm_campaign=empresa-em-dia&utm_content=")
    assert {k: card[k] for k in ("title", "description", "thumbnail")} == {
        "title": "Artigo X", "description": "Descrição do artigo", "thumbnail": "urn:li:image:9"}


def test_link_com_utm_so_no_proprio_site():
    quando = datetime(2026, 10, 27, 11, tzinfo=timezone.utc)
    assert linkedin.link_com_utm("https://advogadaleticiabarros.com.br/lp/x.html?a=1", quando) == (
        "https://advogadaleticiabarros.com.br/lp/x.html?a=1&utm_source=linkedin&utm_medium=social"
        "&utm_campaign=empresa-em-dia&utm_content=2026-10-27")
    assert linkedin.link_com_utm("https://www.tst.jus.br/noticia", quando) == "https://www.tst.jus.br/noticia"
    ja = "https://advogadaleticiabarros.com.br/?utm_source=x"
    assert linkedin.link_com_utm(ja, quando) == ja


@pytest.mark.anyio
async def test_situacao_traz_visitas_e_contatos_do_linkedin(client, db_session):
    from app.services.central_google import TIPO_PAINEL
    from app.models.social_metric import SocialMetric

    tenant, _, auth = await _setup(db_session)
    db_session.add(SocialMetric(tenant_id=tenant.id, tipo=TIPO_PAINEL, metricas={
        "analytics": {"linkedin": {"sessoes_90d": 9, "contatos_90d": 1, "por_pagina": []}}}))
    await db_session.commit()
    resultados = (await client.get("/linkedin", headers=auth)).json()["resultados"]
    assert resultados["sessoes_90d"] == 9 and resultados["contatos_90d"] == 1 and resultados["coletado_em"]


@pytest.mark.anyio
async def test_job_espera_artigo_e_conexao_vencida(db_session):
    tenant, _, _ = await _setup(db_session, expira_em=datetime.now(timezone.utc) - timedelta(days=1))
    agora = datetime.now(timezone.utc)
    sem_artigo = LinkedInPost(tenant_id=tenant.id, texto="Post de artigo futuro", status="aprovado",
                              link="https://advogadaleticiabarros.com.br/blog/futuro.html", publicar_em=agora)
    vencido = LinkedInPost(tenant_id=tenant.id, texto="Post sem link", status="aprovado", publicar_em=agora)
    db_session.add_all([sem_artigo, vencido])
    await db_session.commit()

    publicados = await linkedin.publicar_prontos(db_session, agora, _linkedin_falso([]), SiteFalso({}))
    assert publicados == 0
    assert sem_artigo.status == "aprovado" and "Aguardando o artigo" in sem_artigo.erro
    assert vencido.status == "aprovado" and "venceu" in vencido.erro


def test_aviso_de_reconexao_a_partir_de_7_dias():
    c = SocialConnection(expira_em=datetime(2026, 11, 5, tzinfo=timezone.utc))
    assert linkedin.aviso_conexao(c, date(2026, 10, 22)) is None
    aviso = linkedin.aviso_conexao(c, date(2026, 10, 30))
    assert aviso["titulo"] == "A conexão com o LinkedIn vence em 6 dia(s)" and aviso["prioridade"] == "media"
    assert linkedin.aviso_conexao(c, date(2026, 11, 6))["titulo"] == "A conexão com o LinkedIn venceu"
