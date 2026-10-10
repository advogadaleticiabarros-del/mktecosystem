import io
import json
import re

from PIL import Image

from app.services.blog_seo import aplicar_seo, capa_para_jpg, cards_do_indice, escolher_relacionados

INDICE = (
    '<div id="blogGrid">'
    '<a class="blog-card" data-cat="trabalhista" href="fui-demitida-gravida.html"><div class="blog-card-body"><h3>Fui demitida grávida</h3></div></a>'
    '<a href="rescisao-indireta.html" class="blog-card" data-cat="trabalhista"><div><h3>Rescisão indireta</h3></div></a>'
    '<a class="blog-card" data-cat="familia" href="pensao.html"><h3>Pensão &amp; guarda</h3></a>'
    '<a class="blog-card" data-cat="trabalhista" href="horas-extras.html"><h3>Horas extras</h3></a>'
    '<a class="blog-card" data-cat="trabalhista" href="assedio.html"><h3>Assédio moral</h3></a>'
    "</div>"
)

ARTIGO = """<html><head><title>T</title>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "Título", "datePublished": "2026-10-12"}</script>
<style>.x{}</style></head><body><article><h1>Estabilidade da gestante</h1><div class="article-body">
<p>Texto.</p>
<h2>Perguntas frequentes</h2>
<h3>Quanto tempo dura?</h3><p>Até 5 meses após o parto.</p>
<h3>Vale no contrato de experiência?</h3><p>Sim, segundo o TST.</p>
<h2>Se essa é a sua situação</h2><p>Procure uma advogada de confiança.</p>
</div></article>
<div class="gold-line"></div>
<!-- Footer -->
<footer class="footer"></footer></body></html>"""


def _schemas(html: str) -> dict:
    blocos = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    return {b["@type"]: b for b in blocos}


def test_cards_do_indice_le_slug_categoria_e_titulo_em_qualquer_ordem_de_atributos():
    cards = cards_do_indice(INDICE)
    assert cards[0] == {"slug": "fui-demitida-gravida", "cat": "trabalhista", "titulo": "Fui demitida grávida"}
    assert {"slug": "rescisao-indireta", "cat": "trabalhista", "titulo": "Rescisão indireta"} in cards
    assert {"slug": "pensao", "cat": "familia", "titulo": "Pensão & guarda"} in cards


def test_relacionados_sao_da_mesma_area_sem_o_proprio_artigo():
    rel = escolher_relacionados(cards_do_indice(INDICE), slug="novo-artigo", categoria_slug="trabalhista")
    assert len(rel) == 3
    assert all(r["cat"] == "trabalhista" for r in rel)
    rel2 = escolher_relacionados(cards_do_indice(INDICE), slug="horas-extras", categoria_slug="trabalhista")
    assert "horas-extras" not in [r["slug"] for r in rel2]


def test_relacionados_completa_com_outras_areas_quando_faltam():
    rel = escolher_relacionados(cards_do_indice(INDICE), slug="x", categoria_slug="familia")
    assert rel[0]["slug"] == "pensao" and len(rel) == 3


def test_aplicar_seo_monta_schema_completo_com_faq_e_breadcrumb():
    html = aplicar_seo(ARTIGO, slug="estabilidade-gestante", relacionados=cards_do_indice(INDICE)[:3], data_iso="2026-10-12")
    s = _schemas(html)
    post = s["BlogPosting"]
    assert post["author"]["identifier"] == "OAB/ES 39.948"
    assert post["datePublished"] == "2026-10-12" and post["dateModified"] == "2026-10-12"
    assert post["image"].endswith("/blog/capas/estabilidade-gestante.jpg")
    assert post["mainEntityOfPage"].endswith("/blog/estabilidade-gestante.html")
    assert [q["name"] for q in s["FAQPage"]["mainEntity"]] == ["Quanto tempo dura?", "Vale no contrato de experiência?"]
    assert s["FAQPage"]["mainEntity"][0]["acceptedAnswer"]["text"] == "Até 5 meses após o parto."
    assert s["BreadcrumbList"]["itemListElement"][2]["name"] == "Estabilidade da gestante"
    assert html.count('application/ld+json') == 3


def test_aplicar_seo_sem_perguntas_frequentes_nao_cria_faq():
    sem_faq = ARTIGO.replace("Perguntas frequentes", "Outra seção")
    s = _schemas(aplicar_seo(sem_faq, slug="a", relacionados=[], data_iso="2026-10-12"))
    assert "FAQPage" not in s and "BlogPosting" in s


def test_aplicar_seo_insere_continue_lendo_antes_do_rodape():
    html = aplicar_seo(ARTIGO, slug="a", relacionados=cards_do_indice(INDICE)[:3], data_iso="2026-10-12")
    assert html.index('class="related-posts"') < html.index("<!-- Footer -->")
    assert 'href="fui-demitida-gravida.html"' in html and "Continue lendo" in html
    assert ".related-card" in html  # CSS do bloco garantido na página


def test_capa_para_jpg_converte_e_limita_largura():
    buf = io.BytesIO()
    Image.new("RGBA", (2400, 1260), (200, 150, 90, 255)).save(buf, "PNG")
    jpg = capa_para_jpg(buf.getvalue())
    assert jpg[:2] == b"\xff\xd8"
    assert Image.open(io.BytesIO(jpg)).size == (1200, 630)


def test_capa_para_jpg_devolve_original_quando_nao_e_imagem():
    assert capa_para_jpg(b"nao-e-imagem") == b"nao-e-imagem"
