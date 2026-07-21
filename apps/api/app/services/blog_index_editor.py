import html as html_lib

from bs4 import BeautifulSoup


def inserir_card(
    html_atual: str,
    *,
    url: str,
    imagem: str,
    categoria: str,
    categoria_slug: str,
    titulo: str,
    resumo: str,
    tempo_leitura: int,
) -> str:
    soup = BeautifulSoup(html_atual, "html.parser")
    if soup.find("a", href=url) is not None:
        return str(soup)

    url_escapado = html_lib.escape(url)
    imagem_escapada = html_lib.escape(imagem)
    categoria_slug_escapado = html_lib.escape(categoria_slug)
    categoria_escapada = html_lib.escape(categoria)
    titulo_escapado = html_lib.escape(titulo)
    resumo_escapado = html_lib.escape(resumo)

    card_html = (
        f'<a href="{url_escapado}" class="blog-card" data-cat="{categoria_slug_escapado}" '
        'style="border-color: rgba(201,169,98,0.35);">'
        '<div class="blog-card-image" style="position:relative;">'
        f'<img src="{imagem_escapada}" alt="{titulo_escapado}" loading="lazy">'
        '<span style="position:absolute;top:12px;left:12px;background:var(--dourado);'
        "color:#231E1A;font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;"
        'letter-spacing:1.5px;text-transform:uppercase;padding:4px 10px;border-radius:999px;">Novo</span>'
        "</div>"
        '<div class="blog-card-body">'
        f'<span class="blog-card-cat">{categoria_escapada}</span>'
        f"<h3>{titulo_escapado}</h3>"
        f"<p>{resumo_escapado}</p>"
        '<div class="blog-card-meta">'
        f'<span><i class="fa-regular fa-clock"></i> {tempo_leitura} min de leitura</span>'
        '<span class="read-more">Ler artigo <i class="fa-solid fa-arrow-right"></i></span>'
        "</div></div></a>"
    )

    for grid_id in ("blogGridRecent", "blogGrid"):
        grid = soup.find(id=grid_id)
        if grid is not None:
            novo_card = BeautifulSoup(card_html, "html.parser")
            grid.insert(0, novo_card)
    return str(soup)


def inserir_sitemap_entry(xml_atual: str, *, url: str, data_iso: str) -> str:
    if f"<loc>{url}</loc>" in xml_atual:
        return xml_atual

    entrada = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{data_iso}</lastmod>\n  </url>\n"
    marcador = "<urlset"
    posicao_fim_tag = xml_atual.index(">", xml_atual.index(marcador)) + 1
    return xml_atual[:posicao_fim_tag] + "\n" + entrada + xml_atual[posicao_fim_tag:]
