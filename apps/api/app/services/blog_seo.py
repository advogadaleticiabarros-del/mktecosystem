"""SEO dos artigos do blog (plano docs/SEO_PLANO_GOOGLE_IA.md, 10/10/2026).

Uma interface pequena para o publicador:
- `cards_do_indice(html)`: os artigos já publicados, lidos do índice do blog;
- `escolher_relacionados(cards, slug, categoria_slug)`: 3 artigos para o "Continue lendo";
- `aplicar_seo(html, slug, relacionados, data_iso)`: schema completo (BlogPosting com autora e OAB,
  BreadcrumbList e FAQPage a partir de "Perguntas frequentes") e o bloco "Continue lendo";
- `capa_para_jpg(bytes)`: capa leve (JPG até 1200 px) no lugar do PNG de ~1 MB.
"""
import html as html_lib
import io
import json
import re

from PIL import Image

SITE = "https://advogadaleticiabarros.com.br"
NOMES_AREA = {"trabalhista": "Trabalhista", "familia": "Família", "previdenciario": "Previdenciário", "consumidor": "Consumidor"}

CSS_RELACIONADOS = """
        .related-posts { padding: 80px 0; }
        .related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 40px; }
        .related-card { background: var(--fundo-alt); border: 1px solid rgba(201,169,98,0.08); border-radius: var(--radius-md);
            padding: 24px 22px; text-decoration: none; color: inherit; transition: all 0.3s ease; display: block; }
        .related-card:hover { transform: translateY(-4px); border-color: rgba(201,169,98,0.3); }
        .related-card .cat { font-size: 0.72rem; font-weight: 600; letter-spacing: 1.5px; color: var(--dourado);
            text-transform: uppercase; display: block; margin-bottom: 10px; }
        .related-card h4 { font-family: 'Playfair Display', serif; font-size: 1.1rem; line-height: 1.35; color: var(--texto-claro); }
        @media (max-width: 1024px) { .related-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 640px) { .related-grid { grid-template-columns: 1fr; } }
"""


def _texto(fragmento: str) -> str:
    return re.sub(r"\s+", " ", html_lib.unescape(re.sub(r"<[^>]+>", " ", fragmento))).strip()


def cards_do_indice(indice_html: str) -> list[dict]:
    cards = []
    for m in re.finditer(r'<a\b([^>]*class="blog-card"[^>]*)>(.*?)</a>', indice_html, re.S):
        atributos, corpo = m.group(1), m.group(2)
        href = re.search(r'href="([^"]+)\.html"', atributos)
        cat = re.search(r'data-cat="([^"]+)"', atributos)
        titulo = re.search(r"<h3[^>]*>(.*?)</h3>", corpo, re.S)
        if href and titulo:
            cards.append({"slug": href.group(1), "cat": cat.group(1) if cat else "", "titulo": _texto(titulo.group(1))})
    return cards


def escolher_relacionados(cards: list[dict], *, slug: str, categoria_slug: str, n: int = 3) -> list[dict]:
    outros = [c for c in cards if c["slug"] != slug]
    mesma_area = [c for c in outros if c["cat"] == categoria_slug]
    resto = [c for c in outros if c not in mesma_area]
    return (mesma_area + resto)[:n]


def _faq(html: str) -> list[tuple[str, str]]:
    m = re.search(r"<h2[^>]*>\s*Perguntas frequentes\s*</h2>(.*?)(?=<h2|<div class=\"article-cta|</article>|<section)", html, re.S | re.I)
    if not m:
        return []
    pares = re.findall(r"<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|$)", m.group(1), re.S)
    return [(_texto(q), _texto(r)) for q, r in pares if _texto(q) and _texto(r)]


def _schemas(html: str, slug: str, data_iso: str) -> list[dict]:
    post = {}
    for bloco in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            dado = json.loads(bloco)
        except ValueError:
            continue
        if isinstance(dado, dict) and dado.get("@type") == "BlogPosting":
            post = dado
    titulo = _texto((re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S) or [None, slug])[1])
    url = f"{SITE}/blog/{slug}.html"
    post.update({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": post.get("headline") or titulo,
        "inLanguage": "pt-BR", "mainEntityOfPage": url, "url": url, "image": f"{SITE}/blog/capas/{slug}.jpg",
        "author": {"@type": "Person", "name": "Dra. Letícia Barros", "jobTitle": "Advogada", "identifier": "OAB/ES 39.948",
                   "url": f"{SITE}/sobre.html", "sameAs": ["https://www.instagram.com/adv.leticiabarros2/"]},
        "publisher": {"@type": "LegalService", "name": "Letícia Barros Advocacia", "url": f"{SITE}/",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo/logo-800x800.png"}},
        "datePublished": post.get("datePublished") or data_iso, "dateModified": data_iso,
    })
    grafo = [post, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
        {"@type": "ListItem", "position": 3, "name": titulo, "item": url}]}]
    perguntas = _faq(html)
    if perguntas:
        grafo.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in perguntas]})
    return grafo


def _bloco_relacionados(relacionados: list[dict]) -> str:
    cards = "\n".join(
        f'            <a href="{html_lib.escape(r["slug"])}.html" class="related-card">\n'
        f'                <span class="cat">{NOMES_AREA.get(r["cat"], "Direito")}</span>\n'
        f'                <h4>{html_lib.escape(r["titulo"])}</h4>\n            </a>' for r in relacionados)
    return ('<section class="related-posts">\n    <div class="container">\n        <div class="section-header">\n'
            '            <span class="section-tag">Continue lendo</span>\n            <h2>Outros artigos que podem<br>te interessar</h2>\n'
            f'        </div>\n        <div class="related-grid">\n{cards}\n        </div>\n    </div>\n</section>\n\n')


def aplicar_seo(html: str, *, slug: str, relacionados: list[dict], data_iso: str) -> str:
    novo_schema = "".join(f'    <script type="application/ld+json">\n{json.dumps(g, ensure_ascii=False, indent=2)}\n    </script>\n'
                          for g in _schemas(html, slug, data_iso))
    html = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", html, flags=re.S)
    html = html.replace("</head>", novo_schema + "</head>", 1)
    if relacionados:
        bloco = _bloco_relacionados(relacionados)
        if '<section class="related-posts">' in html:
            html = re.sub(r'<section class="related-posts">.*?</section>\s*', bloco, html, count=1, flags=re.S)
        else:
            alvo = re.search(r'(<div class="gold-line"></div>\s*)?<!-- Footer -->|<footer', html)
            posicao = alvo.start() if alvo else html.index("</body>")
            html = html[:posicao] + bloco + html[posicao:]
        if ".related-card {" not in html:
            html = html.replace("</style>", CSS_RELACIONADOS + "    </style>", 1)
    return html


def capa_para_jpg(conteudo: bytes, largura_max: int = 1200) -> bytes:
    try:
        imagem = Image.open(io.BytesIO(conteudo))
        imagem.load()
    except Exception:
        return conteudo
    imagem = imagem.convert("RGB")
    if imagem.width > largura_max:
        imagem = imagem.resize((largura_max, round(imagem.height * largura_max / imagem.width)), Image.LANCZOS)
    saida = io.BytesIO()
    imagem.save(saida, "JPEG", quality=82, optimize=True, progressive=True)
    return saida.getvalue()
