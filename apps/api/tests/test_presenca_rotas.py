import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import httpx
import pytest

from app.core.crypto import encrypt_token
from app.core.security import create_access_token, hash_password
from app.models.presenca_google import GooglePost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant
from app.models.user import User
from app.services import central_google
from tests.test_presenca_google import CONTA, LOCAL, _google_falso


class SiteVazio:
    async def ler(self, caminho):
        return None

    async def listar_html(self):
        return []


def _google_com_escrita(pedidos: list):
    leitura = _google_falso()

    async def handler(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        if request.url.host == "oauth2.googleapis.com":
            return httpx.Response(200, json={"access_token": "novo", "expires_in": 3599})
        if request.method == "POST" and request.url.path.endswith("/localPosts"):
            return httpx.Response(200, json={"name": f"{CONTA}/{LOCAL}/localPosts/9", "searchUrl": "https://g/p9"})
        if request.method in ("PUT", "PATCH", "DELETE"):
            return httpx.Response(200, json={})
        return await leitura.handle_async_request(request)

    return httpx.MockTransport(handler)


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(SocialConnection(tenant_id=tenant.id, plataforma="google_business", page_id=CONTA, ig_user_id=LOCAL,
                            nome_conta="Escritório", access_token_encrypted=encrypt_token("refresh"), status="ativo"))
    user = User(tenant_id=tenant.id, email="l@example.com", nome="L", hashed_password=hash_password("s"), role="owner")
    db.add(user)
    await db.commit()
    return tenant, {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.fixture
def google():
    pedidos: list = []
    transporte = _google_com_escrita(pedidos)
    original = central_google._site_padrao
    with patch("app.routers.presenca.google_transport", return_value=transporte), \
            patch.object(central_google, "_site_padrao", return_value=SiteVazio()):
        yield pedidos
    central_google._site_padrao = original


@pytest.mark.anyio
async def test_atualizar_mostra_painel_e_melhorias_com_status(client, db_session, google):
    _, auth = await _setup(db_session)

    vazio = await client.get("/presenca", headers=auth)
    assert vazio.json() == {"painel": None, "coletado_em": None, "recomendacoes": []}

    resp = await client.post("/presenca/atualizar", headers=auth)
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["painel"]["perfil"]["titulo"] == "Letícia Barros | Advocacia"
    assert dados["painel"]["sitemap_enviado"] is True
    chaves = {r["chave"]: r for r in dados["recomendacoes"]}
    assert chaves["avaliacoes-sem-resposta"]["status"] == "pendente"

    await client.put("/presenca/recomendacoes/avaliacoes-sem-resposta", json={"status": "feita"}, headers=auth)
    depois = {r["chave"]: r for r in (await client.get("/presenca", headers=auth)).json()["recomendacoes"]}
    assert depois["avaliacoes-sem-resposta"]["status"] == "feita"


@pytest.mark.anyio
async def test_responder_avaliacao_atualiza_o_painel(client, db_session, google):
    _, auth = await _setup(db_session)
    await client.post("/presenca/atualizar", headers=auth)

    proibida = await client.post("/presenca/avaliacoes/responder", headers=auth,
                                 json={"name": f"{CONTA}/{LOCAL}/reviews/a", "texto": "Que bom que ganhamos seu processo!"})
    assert proibida.status_code == 422

    ok = await client.post("/presenca/avaliacoes/responder", headers=auth,
                           json={"name": f"{CONTA}/{LOCAL}/reviews/a", "texto": "Obrigada pela confiança, Ana!"})
    assert ok.status_code == 200
    assert google[-1].method == "PUT"
    painel = (await client.get("/presenca", headers=auth)).json()["painel"]
    assert painel["avaliacoes"]["sem_resposta"] == 0

    outro_perfil = await client.post("/presenca/avaliacoes/responder", headers=auth,
                                     json={"name": "accounts/x/locations/y/reviews/z", "texto": "Obrigada!"})
    assert outro_perfil.status_code == 422


@pytest.mark.anyio
async def test_editar_perfil(client, db_session, google):
    _, auth = await _setup(db_session)
    resp = await client.patch("/presenca/perfil", headers=auth, json={"site": "https://a.com.br/?utm_source=google"})
    assert resp.status_code == 200
    assert resp.json()["alterados"] == ["websiteUri"]
    patch_req = next(r for r in google if r.method == "PATCH")
    assert json.loads(patch_req.content) == {"websiteUri": "https://a.com.br/?utm_source=google"}


@pytest.mark.anyio
async def test_posts_fila_aprovacao_e_publicacao(client, db_session, google):
    _, auth = await _setup(db_session)

    bloqueado = await client.post("/presenca/posts", headers=auth,
                                  json={"texto": "Consulta grátis para gestantes!", "status": "aprovado"})
    assert bloqueado.status_code == 422

    rascunho = (await client.post("/presenca/posts", headers=auth, json={
        "texto": "Grávida e demitida? A lei prevê estabilidade.", "botao": "LEARN_MORE", "link": "https://site/blog",
    })).json()
    assert rascunho["status"] == "rascunho"

    publicado = await client.post(f"/presenca/posts/{rascunho['id']}/publicar-agora", headers=auth)
    assert publicado.status_code == 200
    assert publicado.json()["status"] == "publicado"
    assert publicado.json()["link_publicado"] == "https://g/p9"


@pytest.mark.anyio
async def test_job_publica_so_aprovados_no_horario(db_session, google):
    tenant, _ = await _setup(db_session)
    agora = datetime.now(timezone.utc)
    devido = GooglePost(tenant_id=tenant.id, texto="Post devido", status="aprovado", publicar_em=agora - timedelta(minutes=5))
    futuro = GooglePost(tenant_id=tenant.id, texto="Post futuro", status="aprovado", publicar_em=agora + timedelta(days=1))
    rascunho = GooglePost(tenant_id=tenant.id, texto="Rascunho", status="rascunho", publicar_em=agora - timedelta(days=1))
    db_session.add_all([devido, futuro, rascunho])
    await db_session.commit()

    transporte = _google_com_escrita([])
    assert await central_google.publicar_posts_prontos(db_session, agora, transporte) == 1
    assert (devido.status, futuro.status, rascunho.status) == ("publicado", "aprovado", "rascunho")


class SiteComArtigos:
    def __init__(self, caminhos):
        self.caminhos = set(caminhos)

    async def ler(self, caminho):
        return "<html></html>" if caminho in self.caminhos else None

    async def listar_html(self):
        return sorted(self.caminhos)


@pytest.mark.anyio
async def test_post_espera_o_artigo_ir_ao_ar(db_session, google):
    tenant, auth = await _setup(db_session)
    agora = datetime.now(timezone.utc)
    from app.models.social_metric import SocialMetric
    db_session.add(SocialMetric(tenant_id=tenant.id, tipo="google_painel", metricas={"dominio": "a.com.br", "erros": {}}))
    no_ar = GooglePost(tenant_id=tenant.id, texto="Artigo no ar", status="aprovado", botao="LEARN_MORE",
                       link="https://a.com.br/blog/no-ar.html?utm_source=google", publicar_em=agora - timedelta(minutes=1))
    futuro = GooglePost(tenant_id=tenant.id, texto="Artigo ainda não publicado", status="aprovado", botao="LEARN_MORE",
                        link="https://a.com.br/blog/rascunho.html", publicar_em=agora - timedelta(minutes=1))
    db_session.add_all([no_ar, futuro])
    await db_session.commit()

    site = SiteComArtigos(["blog/no-ar.html"])
    assert await central_google.publicar_posts_prontos(db_session, agora, _google_com_escrita([]), site) == 1
    assert no_ar.status == "publicado"
    assert futuro.status == "aprovado" and futuro.erro == central_google.AGUARDANDO_ARTIGO

    site.caminhos.add("blog/rascunho.html")
    assert await central_google.publicar_posts_prontos(db_session, agora, _google_com_escrita([]), site) == 1
    assert futuro.status == "publicado" and futuro.erro is None
