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


def test_trocar_titulo_e_descricao_mexe_so_na_aba_e_na_meta():
    from app.services.blog_seo import trocar_titulo_e_descricao

    pagina = (
        '<html><head><title>Antigo | Dra. Letícia Barros</title>\n'
        '<meta name="description" content="Descrição antiga">\n'
        '<meta property="og:title" content="Antigo"></head><body><h1>Antigo</h1></body></html>'
    )
    nova = trocar_titulo_e_descricao(pagina, titulo="Novo & certo", descricao='Diz "isto" aqui')
    assert "<title>Novo &amp; certo</title>" in nova
    assert '<meta name="description" content="Diz &quot;isto&quot; aqui">' in nova
    assert '<meta property="og:title" content="Antigo">' in nova
    assert "<h1>Antigo</h1>" in nova


def test_trocar_titulo_e_descricao_cria_a_meta_quando_falta():
    from app.services.blog_seo import trocar_titulo_e_descricao

    nova = trocar_titulo_e_descricao("<head><title>Blog</title></head>", titulo=None, descricao="Artigos")
    assert '<title>Blog</title>\n<meta name="description" content="Artigos">' in nova


def test_trocar_titulo_e_descricao_sem_title_avisa():
    import pytest

    from app.services.blog_seo import trocar_titulo_e_descricao

    with pytest.raises(ValueError):
        trocar_titulo_e_descricao("<head></head>", titulo="X", descricao=None)


def test_trocar_titulo_e_descricao_junta_metas_repetidas_em_qualquer_ordem_de_atributos():
    from app.services.blog_seo import trocar_titulo_e_descricao

    pagina = (
        '<head><title>Blog</title>\n<meta content="Uma" name="description"/>\n'
        '<meta content="Outra" name="description"/>\n</head>'
    )
    nova = trocar_titulo_e_descricao(pagina, titulo=None, descricao="Só esta")
    assert nova.count('name="description"') == 1
    assert '<meta name="description" content="Só esta">' in nova


ARTIGO_PUBLICADO = """<html><head><title>Velho</title>
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "Velho", "description": "Desc velha",
 "image": "https://x/logo.png", "datePublished": "2026-04-16", "dateModified": "2026-10-10"}
</script>
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
 {"@type": "ListItem", "position": 1, "name": "Início"}, {"@type": "ListItem", "position": 3, "name": "Velho"}]}
</script>
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Antiga?"}]}
</script>
</head><body><article><section class="article-hero"><h1>Velho: <span class="highlight">título</span></h1>
<span><i class="fa-regular fa-clock"></i> 7 min de leitura</span></section>
<section>
<div class="article-body">
<p>Texto antigo.</p>
</div>
</section>
</article><section class="related-posts">relacionados</section></body></html>"""


def test_atualizar_corpo_do_artigo_troca_texto_h1_e_dados_estruturados():
    from app.services.blog_seo import atualizar_corpo_do_artigo

    corpo = ("<p>Texto novo.</p>\n<h2>Perguntas frequentes</h2>\n<h3>Conta?</h3>\n<p>Sim, conta.</p>\n"
             "<h2>Leia também</h2><p>x</p>")
    novo = atualizar_corpo_do_artigo(ARTIGO_PUBLICADO, corpo=corpo, titulo="Novo: com destaque",
                                     descricao="Desc nova", data_iso="2026-10-27")
    assert "Texto antigo" not in novo and "<p>Texto novo.</p>" in novo
    assert '<h1>Novo: <span class="highlight">com destaque</span></h1>' in novo
    assert "relacionados" in novo
    blocos = _schemas(novo)
    assert blocos["BlogPosting"]["headline"] == "Novo: com destaque"
    assert blocos["BlogPosting"]["description"] == "Desc nova"
    assert blocos["BlogPosting"]["dateModified"] == "2026-10-27"
    assert blocos["BlogPosting"]["datePublished"] == "2026-04-16"
    assert blocos["BlogPosting"]["image"] == "https://x/logo.png"
    assert blocos["BreadcrumbList"]["itemListElement"][-1]["name"] == "Novo: com destaque"
    assert blocos["FAQPage"]["mainEntity"] == [
        {"@type": "Question", "name": "Conta?", "acceptedAnswer": {"@type": "Answer", "text": "Sim, conta."}}]
    assert "1 min de leitura" in novo


def test_atualizar_corpo_do_artigo_sem_corpo_avisa():
    import pytest

    from app.services.blog_seo import atualizar_corpo_do_artigo

    with pytest.raises(ValueError):
        atualizar_corpo_do_artigo("<html></html>", corpo="<p>x</p>", titulo="T", descricao="D", data_iso="2026-10-27")


def test_aplicar_trocas_troca_trecho_unico():
    from app.services.blog_seo import aplicar_trocas

    novo = aplicar_trocas("<p>Enviar para análise</p><p>fim</p>", [{"de": "Enviar para análise", "para": "Quero orientação"}])
    assert novo == "<p>Quero orientação</p><p>fim</p>"


def test_aplicar_trocas_recusa_trecho_ausente_ou_repetido():
    import pytest

    from app.services.blog_seo import TrocaInvalida, aplicar_trocas

    with pytest.raises(TrocaInvalida, match="não encontrado"):
        aplicar_trocas("<p>a</p>", [{"de": "b", "para": "c"}])
    with pytest.raises(TrocaInvalida, match="2 vezes"):
        aplicar_trocas("<p>a</p><p>a</p>", [{"de": "a", "para": "c"}])


def test_aplicar_trocas_todas_e_reaplicar_sem_erro():
    from app.services.blog_seo import aplicar_trocas

    trocas = [{"de": "análise", "para": "orientação", "todas": True}, {"de": "<b>x</b>", "para": "<b>y</b>"}]
    uma = aplicar_trocas("análise, análise <b>x</b>", trocas)
    assert uma == "orientação, orientação <b>y</b>"
    assert aplicar_trocas(uma, trocas) == uma  # já aplicada: o "para" está lá, nada muda


def test_relacionados_preferem_o_mesmo_assunto_dentro_da_area():
    # Antes: os 3 mais recentes da área (o artigo da licença de 180 dias indicava pet no divórcio e Pix da pensão).
    rel = escolher_relacionados(cards_do_indice(INDICE), slug="hora-extra-nao-paga-como-calcular", categoria_slug="trabalhista")
    assert rel[0]["slug"] == "horas-extras"
    assert all(r["cat"] == "trabalhista" for r in rel)
    rel2 = escolher_relacionados(cards_do_indice(INDICE), slug="gestante-demitida-gravida-direitos", categoria_slug="trabalhista")
    assert rel2[0]["slug"] == "fui-demitida-gravida"


def test_relacionados_sem_repetir_artigo_do_indice():
    indice = INDICE.replace("</div>", '<a class="blog-card" data-cat="trabalhista" href="horas-extras.html"><h3>Horas extras</h3></a></div>')
    rel = escolher_relacionados(cards_do_indice(indice), slug="hora-extra-como-provar", categoria_slug="trabalhista")
    assert [r["slug"] for r in rel].count("horas-extras") == 1


def test_relacionados_do_mesmo_assunto_vem_de_outra_area_antes_de_artigo_sem_relacao():
    rel = escolher_relacionados(cards_do_indice(INDICE), slug="pensao-alimenticia-atrasada", categoria_slug="trabalhista")
    assert rel[0]["slug"] == "pensao"
