from app.services.blog_index_editor import inserir_card, inserir_sitemap_entry

INDEX_FIXTURE = """
<div class="blog-grid" id="blogGridRecent">
    <a href="antigo.html" class="blog-card" data-cat="trabalhista">
        <h3>Artigo antigo</h3>
    </a>
</div>
<div class="blog-grid" id="blogGrid">
    <a href="antigo.html" class="blog-card" data-cat="trabalhista">
        <h3>Artigo antigo</h3>
    </a>
</div>
"""

SITEMAP_FIXTURE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    "  <url><loc>https://advogadaleticiabarros.com.br/blog/antigo.html</loc></url>\n"
    "</urlset>\n"
)


def test_insere_card_nas_duas_grades():
    resultado = inserir_card(
        INDEX_FIXTURE,
        url="novo-artigo.html",
        imagem="https://images.unsplash.com/foto.jpg",
        categoria="Trabalhista",
        categoria_slug="trabalhista",
        titulo="Novo artigo",
        resumo="Resumo do novo artigo",
        tempo_leitura=6,
    )
    assert resultado.count("Novo artigo") == 2
    assert resultado.count('href="novo-artigo.html"') == 2
    assert resultado.count("Artigo antigo") == 2


def test_card_novo_vem_antes_do_antigo_em_cada_grade():
    resultado = inserir_card(
        INDEX_FIXTURE,
        url="novo-artigo.html",
        imagem="https://images.unsplash.com/foto.jpg",
        categoria="Trabalhista",
        categoria_slug="trabalhista",
        titulo="Novo artigo",
        resumo="Resumo do novo artigo",
        tempo_leitura=6,
    )
    assert resultado.index("Novo artigo") < resultado.index("Artigo antigo")


def test_insere_entrada_no_sitemap():
    resultado = inserir_sitemap_entry(
        SITEMAP_FIXTURE, url="https://advogadaleticiabarros.com.br/blog/novo-artigo.html", data_iso="2026-07-21"
    )
    assert "<loc>https://advogadaleticiabarros.com.br/blog/novo-artigo.html</loc>" in resultado
    assert "<lastmod>2026-07-21</lastmod>" in resultado
    assert "<loc>https://advogadaleticiabarros.com.br/blog/antigo.html</loc>" in resultado
