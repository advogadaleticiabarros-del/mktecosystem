"""Integrações da lista public-apis (11/11/2026): cada uma testada pela própria interface, com MockTransport."""
from datetime import date, datetime, timedelta, timezone

import httpx
import pytest

from app.core.security import create_access_token, hash_password
from app.integrations.brasil import DadosBrasil, Empresa, Endereco, Feriado, cnpj_valido
from app.integrations.email.verificador import VerificadorEmail
from app.integrations.imagens.banco import BancoDeFotos
from app.integrations.imagens.outros_bancos import Openverse, Pixabay
from app.integrations.imagens.pexels import FotoBanco
from app.integrations.imagens.remove_bg import RemoveBg, SemCredito
from app.integrations.links.bitly import Bitly
from app.integrations.noticias.camara import CamaraProposicoes
from app.integrations.noticias.newsdata import NewsData
from app.integrations.site.pagespeed import PageSpeed
from app.integrations.site.safe_browsing import SafeBrowsing
from app.main import app
from app.models.tenant import Tenant
from app.models.user import User
from app.routers.ferramentas import get_transport
from app.services.chaves_api import PROVEDORES, ChaveRecusada, validar_bitly, validar_google, validar_pixabay
from app.services.datas_editoriais import datas_do_periodo

CNPJ_OK = "11.222.333/0001-81"


def mock(rotas: dict):
    """rotas: trecho da URL → (status, json | bytes). A primeira que bater responde."""
    pedidos = []

    def responder(request: httpx.Request) -> httpx.Response:
        pedidos.append(request)
        for trecho, (status, corpo) in rotas.items():
            if trecho in str(request.url):
                if isinstance(corpo, bytes):
                    return httpx.Response(status, content=corpo)
                return httpx.Response(status, json=corpo)
        return httpx.Response(500, json={"erro": "sem rota"})

    return httpx.MockTransport(responder), pedidos


# --- Dados do Brasil ---------------------------------------------------------------------------------------------

def test_cnpj_valido_confere_digitos():
    assert cnpj_valido(CNPJ_OK)
    assert not cnpj_valido("11.222.333/0001-82")
    assert not cnpj_valido("11111111111111")


@pytest.mark.anyio
async def test_feriados_da_brasilapi_em_ordem():
    t, _ = mock({"brasilapi.com.br/api/feriados/v1/2027": (200, [
        {"date": "2027-04-21", "name": "Tiradentes", "type": "national"},
        {"date": "2027-01-01", "name": "Confraternização mundial", "type": "national"}])})
    assert await DadosBrasil(t).feriados(2027) == [Feriado(date(2027, 1, 1), "Confraternização mundial"),
                                                   Feriado(date(2027, 4, 21), "Tiradentes")]


@pytest.mark.anyio
async def test_feriados_caem_no_nager_quando_brasilapi_falha_e_ignoram_regionais():
    t, _ = mock({"brasilapi": (503, {}), "date.nager.at/api/v3/PublicHolidays/2027/BR": (200, [
        {"date": "2027-12-25", "localName": "Natal", "name": "Christmas", "global": True},
        {"date": "2027-07-09", "localName": "Revolução Constitucionalista", "name": "x", "global": False}])})
    assert await DadosBrasil(t).feriados(2027) == [Feriado(date(2027, 12, 25), "Natal")]


@pytest.mark.anyio
async def test_cep_pela_brasilapi_e_inexistente_vira_none():
    t, _ = mock({"cep/v2/29055": (200, {"cep": "29055000", "state": "ES", "city": "Vitória",
                                        "neighborhood": "Praia do Canto", "street": "Rua Aleixo Netto"}),
                 "cep/v2/00000000": (404, {})})
    dados = DadosBrasil(t)
    assert await dados.cep("29055-000") == Endereco("29055000", "Rua Aleixo Netto", "Praia do Canto", "Vitória", "ES")
    assert await dados.cep("00000-000") is None
    assert await dados.cep("123") is None


@pytest.mark.anyio
async def test_cep_cai_no_viacep():
    t, _ = mock({"brasilapi": (500, {}), "viacep.com.br/ws/29055000": (200, {
        "logradouro": "Rua A", "bairro": "Centro", "localidade": "Vitória", "uf": "ES"})})
    assert (await DadosBrasil(t).cep("29055000")).cidade == "Vitória"


@pytest.mark.anyio
async def test_cnpj_traz_empresa_e_recusa_invalido_sem_chamar():
    t, pedidos = mock({"cnpj/v1/11222333000181": (200, {
        "razao_social": "ACME LTDA", "nome_fantasia": "Acme", "descricao_situacao_cadastral": "ATIVA",
        "cnae_fiscal_descricao": "Comércio varejista", "cnae_fiscal": 4711302, "porte": "MICRO EMPRESA",
        "municipio": "VITORIA", "uf": "ES", "ddd_telefone_1": "27 3333-4444", "email": "CONTATO@ACME.COM",
        "data_inicio_atividade": "2015-03-02"})})
    empresa = await DadosBrasil(t).cnpj(CNPJ_OK)
    assert empresa == Empresa("11222333000181", "ACME LTDA", "Acme", "ATIVA", "Comércio varejista", "4711302",
                              "MICRO EMPRESA", "VITORIA", "ES", "2733334444", "contato@acme.com", date(2015, 3, 2))
    with pytest.raises(ValueError):
        await DadosBrasil(t).cnpj("11.222.333/0001-00")
    assert len(pedidos) == 1


# --- Datas editoriais --------------------------------------------------------------------------------------------

def test_datas_do_periodo_junta_feriados_fixas_e_moveis_sem_repetir():
    feriados = [Feriado(date(2027, 5, 1), "Dia do Trabalho"), Feriado(date(2027, 4, 21), "Tiradentes")]
    datas = datas_do_periodo(date(2027, 4, 20), date(2027, 5, 31), feriados)
    nomes = [d.nome for d in datas]
    assert nomes == ["Tiradentes", "Dia da Trabalhadora Doméstica", "Dia em Memória das Vítimas de Acidentes de Trabalho",
                     "Dia do Trabalho", "Dia das Mães"]
    assert datas[-1].data == date(2027, 5, 9)  # 2º domingo de maio
    assert datas[3].tipo == "feriado"


def test_datas_atravessam_o_ano():
    datas = datas_do_periodo(date(2026, 12, 15), date(2027, 1, 31), [])
    assert [d.nome for d in datas] == ["Prazo da 2ª parcela do 13º salário", "Dia Nacional do Aposentado"]


# --- Fotos ---------------------------------------------------------------------------------------------------------

def _foto(i, fonte="pexels", url=None):
    return FotoBanco(id=i, url=url or f"https://{fonte}/{i}.jpg", autor="", pagina=f"https://{fonte}/p/{i}",
                     descricao="", largura=1, altura=2, fonte=fonte)


class FonteFixa:
    def __init__(self, fotos=None, erro=False):
        self.fotos, self.erro = fotos or [], erro

    async def buscar(self, consulta, quantidade=15, orientacao="portrait"):
        if self.erro:
            raise httpx.ConnectError("fora")
        return self.fotos


@pytest.mark.anyio
async def test_banco_intercala_fontes_evita_usadas_e_duplicadas():
    a = FonteFixa([_foto(1), _foto(2), _foto(3)])
    b = FonteFixa([_foto(9, "pixabay"), _foto(8, "pixabay", url="https://pexels/3.jpg")])
    fotos = await BancoDeFotos([a, b, FonteFixa(erro=True)]).buscar("x", 10, evitar=["https://pexels/2.jpg"])
    assert [f.url for f in fotos] == ["https://pexels/1.jpg", "https://pixabay/9.jpg", "https://pexels/3.jpg"]


@pytest.mark.anyio
async def test_banco_sem_nenhuma_fonte_respondendo_avisa():
    with pytest.raises(RuntimeError):
        await BancoDeFotos([FonteFixa(erro=True)]).buscar("x")


@pytest.mark.anyio
async def test_openverse_so_dominio_publico_e_pixabay_vertical():
    t, pedidos = mock({
        "api.openverse.org": (200, {"results": [{"id": "abc", "url": "https://o/1.jpg", "creator": "Ana",
                                                 "foreign_landing_url": "https://o/p", "title": "Escritório",
                                                 "width": 800, "height": 1200, "license": "cc0"}]}),
        "pixabay.com/api": (200, {"hits": [{"id": 7, "largeImageURL": "https://px/7.jpg", "user": "Bia",
                                            "pageURL": "https://px/p/7", "tags": "trabalho", "imageWidth": 3000,
                                            "imageHeight": 4000}]})})
    ov = await Openverse(t).buscar("escritório", 5)
    pb = await Pixabay("k", t).buscar("escritório", 5)
    assert pedidos[0].url.params["license"] == "cc0,pdm"
    assert pedidos[1].url.params["orientation"] == "vertical" and pedidos[1].url.params["lang"] == "pt"
    assert (ov[0].fonte, ov[0].licenca, pb[0].fonte, pb[0].url) == ("openverse", "CC0", "pixabay", "https://px/7.jpg")


# --- Notícias ------------------------------------------------------------------------------------------------------

@pytest.mark.anyio
async def test_newsdata_descarta_noticia_fora_da_janela():
    agora = datetime.now(timezone.utc)
    t, pedidos = mock({"newsdata.io": (200, {"results": [
        {"title": "Nova regra do INSS", "link": "https://g1/a", "source_name": "g1", "description": "texto",
         "pubDate": agora.strftime("%Y-%m-%d %H:%M:%S"), "source_url": "https://g1.globo.com"},
        {"title": "Velha", "link": "https://g1/b", "source_name": "g1",
         "pubDate": (agora - timedelta(days=9)).strftime("%Y-%m-%d %H:%M:%S")}]})})
    noticias = await NewsData("k", transport=t).buscar("INSS", 3)
    assert [n.titulo for n in noticias] == ["Nova regra do INSS"]
    assert pedidos[0].url.params["country"] == "br"


@pytest.mark.anyio
async def test_camara_vira_noticia_com_link_da_proposta():
    t, pedidos = mock({"dadosabertos.camara.leg.br": (200, {"dados": [
        {"id": 2501, "siglaTipo": "PL", "numero": 123, "ano": 2026, "ementa": "Altera a CLT"}]})})
    [n] = await CamaraProposicoes(transport=t).buscar("CLT", 30)
    assert (n.titulo, n.fonte, n.url) == ("PL 123/2026", "Câmara dos Deputados",
                                          "https://www.camara.leg.br/propostas-legislativas/2501")
    assert pedidos[0].url.params.get_list("siglaTipo") == ["PL", "PLP", "PEC", "MPV"]


def test_jornalista_inclui_newsdata_com_chave_e_camara_so_sob_encomenda(monkeypatch):
    from app.config import settings
    from app.services.jornalista import criar_jornalista

    monkeypatch.setattr(settings, "GEMINI_API_KEY", "g")
    monkeypatch.setattr(settings, "TAVILY_API_KEY", "")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    monkeypatch.setattr(settings, "NEWSDATA_API_KEY", "n")
    diaria, _ = criar_jornalista()
    sob_encomenda, _ = criar_jornalista(pedido=True)
    assert [type(f).__name__ for f in diaria._buscadores] == ["GoogleNewsRSS", "NewsData"]
    assert [type(f).__name__ for f in sob_encomenda._buscadores][-1] == "CamaraProposicoes"


# --- Site, e-mail, links, recorte ----------------------------------------------------------------------------------

@pytest.mark.anyio
async def test_pagespeed_traduz_notas_e_metricas():
    t, pedidos = mock({"pagespeedonline": (200, {"lighthouseResult": {
        "categories": {"performance": {"score": 0.87}, "seo": {"score": 1}, "accessibility": {"score": 0.95},
                       "best-practices": {"score": 0.78}},
        "audits": {"largest-contentful-paint": {"numericValue": 2412.6},
                   "cumulative-layout-shift": {"numericValue": 0.0213}, "total-blocking-time": {"numericValue": 120.4}}}})})
    m = await PageSpeed("k", t).medir("https://advogadaleticiabarros.com.br")
    assert m.notas == {"desempenho": 87, "seo": 100, "acessibilidade": 95, "boas_praticas": 78}
    assert (m.lcp_s, m.cls, m.tbt_ms) == (2.41, 0.021, 120)
    assert pedidos[0].url.params["key"] == "k"


@pytest.mark.anyio
async def test_safe_browsing_so_devolve_os_perigosos():
    t, _ = mock({"safebrowsing": (200, {"matches": [
        {"threat": {"url": "http://golpe.test"}, "threatType": "SOCIAL_ENGINEERING"}]})})
    assert await SafeBrowsing("k", t).conferir(["https://ok.test", "http://golpe.test"]) == {
        "http://golpe.test": "golpe (phishing)"}
    assert await SafeBrowsing("k", t).conferir([]) == {}


@pytest.mark.anyio
async def test_verificador_de_email():
    t, _ = mock({"disify.com/api/email/a@temp.com": (200, {"format": True, "disposable": True, "dns": True}),
                 "disify.com/api/email/b@semmx.com": (200, {"format": True, "disposable": False, "dns": False}),
                 "disify.com/api/email/c@gmail.com": (200, {"format": True, "disposable": False, "dns": True})})
    v = VerificadorEmail(t)
    assert (await v.verificar("a@temp.com")).situacao == "descartavel"
    assert (await v.verificar("b@semmx.com")).situacao == "sem_caixa"
    assert (await v.verificar(" C@gmail.com ")).situacao == "ok"
    assert (await v.verificar("sem-arroba")).situacao == "invalido"


@pytest.mark.anyio
async def test_verificador_cai_no_kickbox_e_depois_aceita_sem_conferir():
    t, _ = mock({"disify": (500, {}), "open.kickbox.com/v1/disposable/temp.com": (200, {"disposable": True})})
    assert (await VerificadorEmail(t).verificar("x@temp.com")).situacao == "descartavel"
    fora, _ = mock({})
    r = await VerificadorEmail(fora).verificar("x@gmail.com")
    assert (r.situacao, r.conferido) == ("ok", False)


@pytest.mark.anyio
async def test_bitly_encurta_e_conta_cliques():
    t, pedidos = mock({"/v4/shorten": (200, {"link": "https://bit.ly/abc"}),
                       "/v4/bitlinks/bit.ly/abc/clicks/summary": (200, {"total_clicks": 42})})
    b = Bitly("tok", t)
    assert await b.encurtar("https://advogadaleticiabarros.com.br") == "https://bit.ly/abc"
    assert await b.cliques("https://bit.ly/abc") == 42
    assert pedidos[0].headers["Authorization"] == "Bearer tok"


@pytest.mark.anyio
async def test_remove_bg_devolve_png_e_avisa_sem_credito():
    t, pedidos = mock({"removebg": (200, b"PNG")})
    assert await RemoveBg("k", t).recortar(b"jpg") == b"PNG"
    assert pedidos[0].headers["X-Api-Key"] == "k"
    sem, _ = mock({"removebg": (402, {})})
    with pytest.raises(SemCredito):
        await RemoveBg("k", sem).recortar(b"jpg")


# --- Chaves no painel ----------------------------------------------------------------------------------------------

def test_novas_chaves_aparecem_no_painel():
    assert {"pixabay", "newsdata", "google", "bitly", "removebg"} <= set(PROVEDORES)


@pytest.mark.anyio
@pytest.mark.parametrize("validar,status", [(validar_pixabay, 400), (validar_google, 400), (validar_bitly, 403)])
async def test_validadores_recusam_chave_ruim(validar, status):
    with pytest.raises(ChaveRecusada):
        await validar("ruim-ruim", transport=httpx.MockTransport(lambda r: httpx.Response(status, json={})))


# --- Rotas ---------------------------------------------------------------------------------------------------------

async def _login(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    user = User(tenant_id=tenant.id, email="l@x.com", nome="L", hashed_password=hash_password("x"), role="owner")
    db.add(user)
    await db.commit()
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


@pytest.mark.anyio
async def test_rotas_de_ferramentas(client, db_session, monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "BITLY_TOKEN", "")
    headers = await _login(db_session)
    t, _ = mock({"feriados/v1/2027": (200, [{"date": "2027-05-01", "name": "Dia do Trabalho"}]),
                 "cep/v2/29055000": (200, {"state": "ES", "city": "Vitória", "neighborhood": "", "street": ""}),
                 "cnpj/v1": (404, {})})
    app.dependency_overrides[get_transport] = lambda: t
    try:
        r = await client.get("/ferramentas/datas?inicio=2027-04-30&fim=2027-05-02", headers=headers)
        assert r.json() == {"aviso": None, "datas": [{"data": "2027-05-01", "nome": "Dia do Trabalho", "tipo": "feriado",
                                                      "area": "trabalhista",
                                                      "ideia": "Direitos que muita gente não conhece"}]}
        assert (await client.get("/ferramentas/cep/29055-000", headers=headers)).json()["cidade"] == "Vitória"
        assert (await client.get(f"/ferramentas/cnpj/{CNPJ_OK.replace('/', '')}", headers=headers)).status_code == 404
        assert (await client.get("/ferramentas/cnpj/123", headers=headers)).status_code == 422
        sem_chave = await client.post("/ferramentas/encurtar", json={"url": "https://x.com"}, headers=headers)
        assert sem_chave.status_code == 409 and "Bitly" in sem_chave.json()["detail"]
        assert (await client.get("/ferramentas/datas")).status_code == 401
    finally:
        app.dependency_overrides.pop(get_transport, None)
