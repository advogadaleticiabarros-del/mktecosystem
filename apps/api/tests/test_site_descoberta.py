import json

import httpx
import pytest

from app.services.site_descoberta import INDEXNOW_CHAVE, avisar_indexnow, gerar_llms_txt


def _card(slug, cat, titulo, resumo):
    return (
        f'<a class="blog-card" data-cat="{cat}" href="{slug}.html"><div class="blog-card-body">'
        f'<span class="blog-card-cat">X</span><h3>{titulo}</h3><p>{resumo}</p></div></a>'
    )


INDICE = (
    '<div class="blog-grid" id="blogGridRecent">'
    + _card("fim-da-escala-6x1", "trabalhista", "Fim da escala 6x1", "O que muda e quando.")
    + _card("pensao-pais-idosos", "familia", "Pensão para pais idosos", "Quando o filho paga.")
    + "</div>"
    '<div class="blog-grid" id="blogGrid">'
    + _card("fim-da-escala-6x1", "trabalhista", "Fim da escala 6x1", "O que muda e quando.")
    + _card("atestado-falso", "direito-trabalhista", "Atestado falso &amp; justa causa", "Riscos.")
    + _card("bpc-loas", "previdenciario", "BPC para criança", "Quem tem direito.")
    + _card("compra-online", "consumidor", "Compra online", "Arrependimento.")
    + _card("jornal", "novidades", "Radar Jurídico", "Edição da semana.")
    + "</div>"
)
BLOG = "https://advogadaleticiabarros.com.br/blog/"


def test_llms_txt_lista_cada_artigo_uma_vez_na_area_certa():
    texto = gerar_llms_txt(INDICE)

    assert texto.count(f"({BLOG}fim-da-escala-6x1.html)") == 1
    trabalhista = texto.split("## Artigos: Trabalhista")[1].split("\n## ")[0]
    assert f"- [Atestado falso & justa causa]({BLOG}atestado-falso.html): Riscos." in trabalhista
    assert f"- [Fim da escala 6x1]({BLOG}fim-da-escala-6x1.html): O que muda e quando." in trabalhista
    assert f"{BLOG}pensao-pais-idosos.html" in texto.split("## Artigos: Família")[1].split("\n## ")[0]
    assert f"{BLOG}bpc-loas.html" in texto.split("## Artigos: Previdenciário")[1].split("\n## ")[0]
    assert f"{BLOG}compra-online.html" in texto.split("## Artigos: Consumidor")[1].split("\n## ")[0]
    assert f"{BLOG}jornal.html" in texto.split("## Outros conteúdos")[1]


def test_llms_txt_tem_identificacao_e_todas_as_paginas_de_area():
    texto = gerar_llms_txt(INDICE)

    assert texto.startswith("# Letícia Barros Advocacia\n\n> ")
    assert "OAB/ES 39.948" in texto.split("\n## ")[0]
    areas = texto.split("## Áreas de atuação")[1].split("\n## ")[0]
    for pagina in ["direito-trabalhista", "direito-familia", "direito-previdenciario", "direito-consumidor",
                   "direito-civil", "assessoria-juridica", "extrajudiciais"]:
        assert f"/areas/{pagina}.html)" in areas


@pytest.mark.anyio
async def test_indexnow_envia_urls_com_chave_e_local_da_chave():
    pedidos = []

    def responder(request):
        pedidos.append(request)
        return httpx.Response(202)

    status = await avisar_indexnow([f"{BLOG}novo.html"], transport=httpx.MockTransport(responder))

    assert status == 202
    corpo = json.loads(pedidos[0].content)
    assert str(pedidos[0].url) == "https://api.indexnow.org/indexnow"
    assert corpo == {
        "host": "advogadaleticiabarros.com.br",
        "key": INDEXNOW_CHAVE,
        "keyLocation": f"https://advogadaleticiabarros.com.br/{INDEXNOW_CHAVE}.txt",
        "urlList": [f"{BLOG}novo.html"],
    }


@pytest.mark.anyio
async def test_indexnow_fora_do_ar_nao_derruba_a_publicacao():
    def falhar(request):
        raise httpx.ConnectError("sem rede")

    assert await avisar_indexnow([f"{BLOG}novo.html"], transport=httpx.MockTransport(falhar)) is None
