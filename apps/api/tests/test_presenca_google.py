import json
from datetime import date

import httpx
import pytest

from app.integrations.social.google_api import GoogleApi
from app.services.presenca_google import coletar_painel, dominio_raiz, secao_da_pagina

CONTA = "accounts/1"
LOCAL = "locations/2"
HOJE = date(2026, 10, 22)


def _desativada(servico: str) -> httpx.Response:
    return httpx.Response(
        403,
        json={
            "error": {
                "code": 403,
                "message": f"{servico} has not been used in project 1 before or it is disabled.",
                "status": "PERMISSION_DENIED",
                "details": [
                    {
                        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                        "reason": "SERVICE_DISABLED",
                        "metadata": {"activationUrl": f"https://console/{servico}"},
                    }
                ],
            }
        },
    )


def _google_falso(desativadas: set[str] = frozenset()):
    """Um Google de mentira que responde cada API pelo host da URL."""

    def handler(request: httpx.Request) -> httpx.Response:
        host, caminho = request.url.host, request.url.path
        if host in desativadas:
            return _desativada(host)
        if host == "mybusinessbusinessinformation.googleapis.com":
            if caminho.endswith("/attributes"):
                return httpx.Response(200, json={"attributes": [
                    {"name": "attributes/is_owned_by_women", "valueType": "BOOL", "values": [True]},
                    {"name": "attributes/url_whatsapp", "valueType": "URL", "uriValues": [{"uri": "https://wa.me/1"}]},
                ]})
            return httpx.Response(200, json={
                "name": LOCAL,
                "title": "Letícia Barros | Advocacia",
                "websiteUri": "https://contato.advogadaleticiabarros.com.br/",
                "categories": {"primaryCategory": {"displayName": "Advogado trabalhista"},
                               "additionalCategories": [{"displayName": "Advogado"}]},
                "storefrontAddress": {"addressLines": ["R. X, 160"], "locality": "Vitória", "administrativeArea": "ES"},
                "profile": {"description": "Advocacia trabalhista"},
                "serviceItems": [{"freeFormServiceItem": {"label": {"displayName": "Rescisão indireta", "description": "x"}}},
                                 {"structuredServiceItem": {"serviceTypeId": "job_type_id:will_writing"}}],
                "regularHours": {"periods": [{"openDay": "MONDAY", "openTime": {"hours": 8},
                                              "closeDay": "MONDAY", "closeTime": {"hours": 18, "minutes": 30}}]},
                "metadata": {"mapsUri": "https://maps/1", "newReviewUri": "https://review/1"},
            })
        if host == "businessprofileperformance.googleapis.com":
            if "searchkeywords" in caminho:
                return httpx.Response(200, json={"searchKeywordsCounts": [
                    {"searchKeyword": "leticia barros", "insightsValue": {"threshold": "15"}},
                    {"searchKeyword": "advogada gestante vitoria", "insightsValue": {"value": "40"}},
                ]})
            return httpx.Response(200, json={"multiDailyMetricTimeSeries": [{"dailyMetricTimeSeries": [
                {"dailyMetric": "CALL_CLICKS", "timeSeries": {"datedValues": [
                    {"date": {"year": 2026, "month": 10, "day": 20}, "value": "2"},
                    {"date": {"year": 2026, "month": 8, "day": 30}, "value": "5"},
                ]}},
                {"dailyMetric": "BUSINESS_IMPRESSIONS_MOBILE_MAPS", "timeSeries": {"datedValues": [
                    {"date": {"year": 2026, "month": 10, "day": 20}, "value": "7"},
                    {"date": {"year": 2026, "month": 10, "day": 21}},
                ]}},
            ]}]})
        if host == "mybusiness.googleapis.com":
            if caminho.endswith("/reviews"):
                if request.url.params.get("pageToken") is None:
                    return httpx.Response(200, json={
                        "reviews": [{"name": f"{CONTA}/{LOCAL}/reviews/a", "reviewer": {"displayName": "Ana"},
                                     "starRating": "FIVE", "comment": "Ótima", "createTime": "2026-10-10T10:00:00Z"}],
                        "averageRating": 4.9, "totalReviewCount": 2, "nextPageToken": "p2",
                    })
                return httpx.Response(200, json={"reviews": [
                    {"name": f"{CONTA}/{LOCAL}/reviews/b", "reviewer": {"displayName": "Bia"}, "starRating": "FOUR",
                     "createTime": "2026-01-10T10:00:00Z", "reviewReply": {"comment": "Obrigada"}}],
                    "averageRating": 4.9, "totalReviewCount": 2})
            if caminho.endswith("/localPosts"):
                return httpx.Response(200, json={"localPosts": [
                    {"name": "p1", "summary": "Post", "createTime": "2026-10-01T10:00:00Z", "state": "LIVE"}]})
            if caminho.endswith("/media"):
                return httpx.Response(200, json={"mediaItems": [
                    {"name": "m1", "mediaFormat": "PHOTO", "createTime": "2026-09-01T00:00:00Z",
                     "locationAssociation": {"category": "EXTERIOR"}, "googleUrl": "https://foto/1"}]})
        if host == "mybusinessverifications.googleapis.com":
            return httpx.Response(200, json={"hasVoiceOfMerchant": True})
        if host == "mybusinessplaceactions.googleapis.com":
            return httpx.Response(200, json={"placeActionLinks": [
                {"name": "l1", "placeActionType": "APPOINTMENT", "uri": "https://agendar"}]})
        if host == "analyticsadmin.googleapis.com":
            if caminho.endswith("/accountSummaries"):
                return httpx.Response(200, json={"accountSummaries": [{"propertySummaries": [
                    {"property": "properties/9", "displayName": "Outro"},
                    {"property": "properties/7", "displayName": "Site Letícia"}]}]})
            uri = "https://advogadaleticiabarros.com.br" if "properties/7" in caminho else "https://outro.com"
            return httpx.Response(200, json={"dataStreams": [{"webStreamData": {"defaultUri": uri}}]})
        if host == "analyticsdata.googleapis.com":
            assert "properties/7" in caminho
            dims = [d["name"] for d in json.loads(request.content)["dimensions"]]
            if dims == ["date"]:
                rows = [{"dimensionValues": [{"value": "20261020"}],
                         "metricValues": [{"value": "10"}, {"value": "8"}, {"value": "1"}]}]
            elif dims == ["hostName", "pagePath"]:
                rows = [
                    {"dimensionValues": [{"value": "advogadaleticiabarros.com.br"}, {"value": "/blog/x.html"}],
                     "metricValues": [{"value": "30"}, {"value": "20"}]},
                    {"dimensionValues": [{"value": "advogadaleticiabarros.com.br"}, {"value": "/"}],
                     "metricValues": [{"value": "12"}, {"value": "9"}]},
                ]
            elif dims == ["eventName", "pagePath"]:
                corpo = json.loads(request.content)
                assert set(corpo["dimensionFilter"]["filter"]["inListFilter"]["values"]) == {
                    "contato_whatsapp", "contato_ligacao", "generate_lead"}
                rows = [
                    {"dimensionValues": [{"value": "contato_whatsapp"}, {"value": "/blog/x.html"}], "metricValues": [{"value": "3"}]},
                    {"dimensionValues": [{"value": "generate_lead"}, {"value": "/blog/x.html"}], "metricValues": [{"value": "1"}]},
                    {"dimensionValues": [{"value": "contato_ligacao"}, {"value": "/"}], "metricValues": [{"value": "2"}]},
                ]
            elif dims == ["sessionSource", "sessionMedium"]:
                rows = [{"dimensionValues": [{"value": "google"}, {"value": "organic"}], "metricValues": [{"value": "50"}]}]
            elif dims == ["landingPage", "sessionCampaignName"]:
                corpo = json.loads(request.content)
                filtros = corpo["dimensionFilter"]["orGroup"]["expressions"]
                assert {f["filter"]["stringFilter"]["value"] for f in filtros} == {"linkedin", "lnkd.in"}
                rows = [
                    {"dimensionValues": [{"value": "/blog/x.html"}, {"value": "empresa-em-dia"}],
                     "metricValues": [{"value": "7"}, {"value": "1"}]},
                    {"dimensionValues": [{"value": "/"}, {"value": "(referral)"}],
                     "metricValues": [{"value": "2"}, {"value": "0"}]},
                ]
            else:
                rows = [
                    {"dimensionValues": [{"value": "chatgpt.com"}], "metricValues": [{"value": "4"}]},
                    {"dimensionValues": [{"value": "perplexity.ai"}], "metricValues": [{"value": "1"}]},
                    {"dimensionValues": [{"value": "google"}], "metricValues": [{"value": "80"}]},
                ]
            return httpx.Response(200, json={"rows": rows})
        if host == "www.googleapis.com":
            if caminho.endswith("/sites"):
                return httpx.Response(200, json={"siteEntry": [
                    {"siteUrl": "https://outro.com/", "permissionLevel": "siteOwner"},
                    {"siteUrl": "sc-domain:advogadaleticiabarros.com.br", "permissionLevel": "siteOwner"}]})
            assert "sc-domain%3Aadvogadaleticiabarros.com.br" in str(request.url)
            corpo = json.loads(request.content)
            assert corpo["endDate"] == "2026-10-19"  # 3 dias de atraso do Search Console
            dims = corpo["dimensions"]
            if dims == ["date"]:
                assert corpo["startDate"] == "2026-07-22"
            if dims == ["date"]:
                rows = [{"keys": ["2026-10-15"], "clicks": 3, "impressions": 100, "ctr": 0.03, "position": 8.0}]
            elif dims == ["query"]:
                rows = [{"keys": ["estabilidade gestante"], "clicks": 1, "impressions": 90, "ctr": 0.011, "position": 7.4}]
            else:
                rows = [{"keys": ["https://advogadaleticiabarros.com.br/blog/x.html"], "clicks": 2,
                         "impressions": 50, "ctr": 0.04, "position": 9}]
            return httpx.Response(200, json={"rows": rows})
        return httpx.Response(404, json={"error": {"message": f"rota não simulada: {request.url}"}})

    return httpx.MockTransport(handler)


@pytest.mark.anyio
async def test_coletar_painel_completo():
    api = GoogleApi("token", transport=_google_falso())
    painel = await coletar_painel(api, CONTA, LOCAL, HOJE)

    assert painel["erros"] == {}
    assert painel["dominio"] == "advogadaleticiabarros.com.br"

    perfil = painel["perfil"]
    assert perfil["titulo"] == "Letícia Barros | Advocacia"
    assert perfil["categorias_adicionais"] == ["Advogado"]
    assert perfil["servicos"] == [{"nome": "Rescisão indireta", "descricao": "x"}]
    assert perfil["servicos_padrao"] == ["will writing"]
    assert perfil["horarios"] == [{"dia": "Segunda", "abre": "08:00", "fecha": "18:30"}]
    assert painel["atributos"] == {"is_owned_by_women": True, "url_whatsapp": ["https://wa.me/1"]}

    desempenho = painel["desempenho"]
    assert desempenho["totais_30d"]["ligacoes"] == 2
    assert desempenho["totais_30d"]["maps"] == 7
    assert desempenho["totais_30d_anterior"]["ligacoes"] == 5
    assert painel["palavras_chave"][0] == {"termo": "advogada gestante vitoria", "valor": 40, "abaixo_de": None}

    avaliacoes = painel["avaliacoes"]
    assert avaliacoes["total"] == 2 and avaliacoes["media"] == 4.9
    assert avaliacoes["sem_resposta"] == 1
    assert avaliacoes["ultimos_30d"] == 1
    assert avaliacoes["lista"][0]["nota"] == 5

    assert painel["posts"]["total"] == 1 and painel["posts"]["ultimos_30d"] == 1
    assert painel["midia"]["fotos"] == 1 and painel["midia"]["por_categoria"] == {"EXTERIOR": 1}
    assert painel["botoes"] == [{"name": "l1", "tipo": "APPOINTMENT", "url": "https://agendar"}]

    analytics = painel["analytics"]
    assert analytics["propriedade"] == "properties/7"
    assert analytics["serie"][0] == {"data": "2026-10-20", "sessoes": 10, "usuarios": 8, "conversoes": 1}
    assert analytics["por_secao"] == {"blog": 30, "site": 12}
    assert analytics["ia"] == {"total_90d": 5, "por_fonte": [
        {"fonte": "chatgpt.com", "sessoes": 4}, {"fonte": "perplexity.ai", "sessoes": 1}]}

    assert analytics["contatos"]["total_30d"] == 6
    assert analytics["contatos"]["por_tipo"] == {"whatsapp": 3, "ligacao": 2, "formulario": 1}
    assert analytics["contatos"]["por_pagina"][0] == {"caminho": "/blog/x.html", "whatsapp": 3, "ligacao": 0, "formulario": 1}
    assert analytics["linkedin"] == {"sessoes_90d": 9, "contatos_90d": 1, "por_pagina": [
        {"pagina": "/blog/x.html", "campanha": "empresa-em-dia", "sessoes": 7, "contatos": 1},
        {"pagina": "/", "campanha": None, "sessoes": 2, "contatos": 0}]}

    gsc = painel["search_console"]
    assert gsc["site"] == "sc-domain:advogadaleticiabarros.com.br"
    assert gsc["consultas"][0] == {"termo": "estabilidade gestante", "cliques": 1, "impressoes": 90, "ctr": 1.1, "posicao": 7.4}
    assert gsc["totais_28d"]["impressoes"] == 100


@pytest.mark.anyio
async def test_api_desativada_nao_derruba_as_outras_secoes():
    api = GoogleApi("token", transport=_google_falso({"mybusiness.googleapis.com", "analyticsdata.googleapis.com"}))
    painel = await coletar_painel(api, CONTA, LOCAL, HOJE)

    assert painel["avaliacoes"] is None and painel["posts"] is None and painel["analytics"] is None
    assert painel["erros"]["avaliacoes"]["tipo"] == "api_desativada"
    assert painel["erros"]["avaliacoes"]["ativar_em"] == "https://console/mybusiness.googleapis.com"
    assert painel["perfil"]["titulo"]
    assert painel["search_console"]["site"]


@pytest.mark.anyio
async def test_falta_de_permissao_pede_reconexao():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"error": {"code": 403, "message": "Request had insufficient authentication scopes.",
                                                   "details": [{"reason": "ACCESS_TOKEN_SCOPE_INSUFFICIENT"}]}})

    painel = await coletar_painel(GoogleApi("t", transport=httpx.MockTransport(handler)), CONTA, LOCAL, HOJE)
    assert {e["tipo"] for e in painel["erros"].values()} == {"reconectar"}


def test_dominio_raiz():
    assert dominio_raiz("https://contato.advogadaleticiabarros.com.br/") == "advogadaleticiabarros.com.br"
    assert dominio_raiz("https://www.exemplo.com/x") == "exemplo.com"
    assert dominio_raiz(None) is None


def test_secao_da_pagina():
    assert secao_da_pagina("advogadaleticiabarros.com.br", "/blog/a.html") == "blog"
    assert secao_da_pagina("advogadaleticiabarros.com.br", "/lp/guia.html") == "lp"
    assert secao_da_pagina("contato.advogadaleticiabarros.com.br", "/") == "contato"
    assert secao_da_pagina("advogadaleticiabarros.com.br", "/") == "site"
