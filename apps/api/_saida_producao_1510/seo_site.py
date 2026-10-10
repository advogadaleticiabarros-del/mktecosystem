"""Frente A do plano de SEO (docs/SEO_PLANO_GOOGLE_IA.md), aplicada num espelho do site.

Uso: python seo_site.py <pasta-do-espelho> <pasta-de-saída>
Gera em <saída> só os arquivos alterados (mesmos caminhos) e `_relatorio.json` com renomeações e totais.

O que faz:
- textos de risco OAB ("especialista", "Fale comigo", "envie o seu caso", "análise gratuita",
  "sem compromisso") e palavras vetadas pela Letícia ("deficiência" e "ex");
- novos endereços para os 2 artigos com palavra vetada no endereço (301 no .htaccess);
- capas do blog em JPG (o PNG continua no servidor para links antigos);
- schema: BlogPosting completo (autora com OAB, editora, datas, imagem), FAQPage, BreadcrumbList;
- "Continue lendo" com 3 artigos do mesmo assunto em todo artigo (grupo gestante priorizado);
- links das páginas de área e da home para os artigos; títulos locais nas áreas;
- meta/canonical do /blog/, sitemap completo, llms.txt e bloqueio de arquivos ocultos.
"""
import html as H
import json
import re
import sys
from datetime import date
from pathlib import Path

BASE = "https://advogadaleticiabarros.com.br"
HOJE = date.today().isoformat()
ORIG, SAIDA = Path(sys.argv[1]), Path(sys.argv[2])

RENOMEAR = {
    "ex-nao-paga-pensao-o-que-fazer": "pai-nao-paga-pensao-o-que-fazer",
    "bpc-para-crianca-com-deficiencia-o-beneficio-de-r-1-621-que-muita-mae-nao-conhece":
        "bpc-para-crianca-com-necessidades-especiais-o-beneficio-de-r-1-621-que-muita-mae-nao-conhece",
}

# Grupo (cluster) da gestante: os "Continue lendo" deles apontam primeiro uns para os outros.
GESTANTE = ["fui-demitida-gravida-o-que-fazer", "gravida-demitida-sem-saber-estabilidade-gestante",
            "gravida-pode-pedir-demissao-riscos-e-validacao", "pedi-demissao-gravida-posso-reverter",
            "gravidez-e-trabalho-conheca-seus-direitos-essenciais-como-gestante-no-ambiente-profissional",
            "stf-licenca-maternidade-180-dias-o-que-mudou-de-verdade", "licenca-maternidade-mae-adotante-mesmos-direitos-stf",
            "aborto-espontaneo-direitos-da-trabalhadora-clt"]

# Trocas de texto (ordem importa: as mais específicas primeiro).
TROCAS = [
    # OAB: "especialista"
    (r"Advogada especialista em", "Advogada com atuação em"),
    (r"advogada especialista em", "advogada com atuação em"),
    (r"Especialista em Direito Trabalhista e de Família", "Atuação em Direito Trabalhista e de Família"),
    (r"Especialista em Tribunal do Júri e Direito Criminal", "Atua em Tribunal do Júri e Direito Criminal"),
    (r"Especialista em Direito Trabalhista, de Família e Previdenci", "Atua em Direito Trabalhista, de Família e Previdenci"),
    (r"Especialista em Direito Criminal", "Atuação em Direito Criminal"),
    (r"Especialista em Direito Trabalhista", "Atuação em Direito Trabalhista"),
    (r"\(especialista em ", "(atuação em "),
    (r"com especialistas dedicados a cada segmento", "com advogadas dedicadas a cada segmento"),
    (r"Clique aqui e fale com um especialista para ter", "Procure uma advogada de confiança para ter"),
    (r"Um advogado especialista em direito trabalhista poderá analisar seu caso e", "Uma advogada de confiança poderá analisar a situação e"),
    (r"Um advogado especialista pode analisar seu caso, orientar", "Uma advogada de confiança pode orientar"),
    # OAB: convites diretos
    (r"envie o seu caso para análise", "procure uma advogada de confiança"),
    (r"Envie seu caso para análise\.", "Procure uma advogada de confiança."),
    (r"Entre em contato com nosso escritório e agende uma consulta personalizada\.", "Entre em contato com o escritório."),
    (r"Fale comigo agora e dê o primeiro passo", "Procure orientação jurídica e dê o primeiro passo"),
    (r"Fale comigo e descubra como posso ajudar a proteger", "Conheça o escritório e entenda como proteger"),
    (r"Fale comigo diretamente pelo WhatsApp para uma análise gratuita", "Entre em contato com o escritório pelo WhatsApp"),
    (r"para uma análise gratuita", "para orientação"),
    (r"Fale [Cc]omigo agora", "Entrar em contato"),
    (r"Fale [Cc]omigo", "Entrar em contato"),
    (r"\s*<[^>]+>\s*Sem compromisso\s*</[^>]+>", ""),
    (r" ?· ?Sem compromisso", ""),
    # Palavra vetada: "deficiência" (regra fixa da Letícia)
    (r"Crianças com Deficiência", "Crianças com Necessidades Especiais"),
    (r"Filho com deficiência", "Filho com necessidades especiais"),
    (r"Filhos com deficiência", "Filhos com necessidades especiais"),
    (r"pessoas com deficiência", "pessoas com necessidades especiais"),
    (r"criança com deficiência", "criança com necessidades especiais"),
    (r"crianças com deficiência", "crianças com necessidades especiais"),
    (r"tem deficiência", "tem necessidades especiais"),
    (r"\(se for por deficiência\)", "(se for por necessidades especiais)"),
    (r"Deficiência em sentido amplo", "Necessidades especiais, em sentido amplo"),
    (r"a deficiência impede", "a condição impede"),
    (r"idade/deficiência", "idade/necessidades especiais"),
    # Palavra vetada: "ex" (regra fixa: genitor)
    (r"Seu ex parou de pagar", "O pai parou de pagar"),
    (r"o que fazer se o ex não paga", "o que fazer se o genitor não paga"),
    (r"O ex havia mudado", "O genitor havia mudado"),
    (r"se o ex não cumpre", "se o genitor não cumpre"),
    (r"Meu ex-marido está desempregado", "O pai do meu filho está desempregado"),
    (r"Ex não paga pensão", "Pai não paga pensão"),
    (r"ex não paga pensão", "pai não paga pensão"),
    # Valor antigo do salário mínimo no BPC
    (r"R\$ ?1\.412", "R$ 1.621"),
]

TITULOS_AREA = {
    "areas/direito-trabalhista.html": "Advogada Trabalhista em Vitória-ES | Letícia Barros Advocacia",
    "areas/direito-familia.html": "Advogada de Pensão Alimentícia e Família em Vitória-ES | Letícia Barros",
    "areas/direito-previdenciario.html": "BPC/LOAS para Crianças com Necessidades Especiais | Advogada em Vitória-ES",
    "areas/direito-consumidor.html": "Advogada do Consumidor em Vitória-ES | Letícia Barros Advocacia",
    "areas/direito-civil.html": "Advogada Cível em Vitória-ES | Letícia Barros Advocacia",
}
AREA_CAT = {"areas/direito-trabalhista.html": ("trabalhista", "Direito Trabalhista"), "areas/direito-familia.html": ("familia", "Direito de Família"),
            "areas/direito-previdenciario.html": ("previdenciario", "Direito Previdenciário"),
            "areas/direito-consumidor.html": ("consumidor", "Direito do Consumidor")}
NOME_CAT = {"trabalhista": "Trabalhista", "familia": "Família", "previdenciario": "Previdenciário", "consumidor": "Consumidor"}

CSS_REL = """
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

relatorio = {"trocas": {}, "alterados": [], "renomeados": RENOMEAR, "capas_jpg": []}


def ler(rel: str) -> str:
    return (ORIG / rel).read_text(encoding="utf-8")


def slug_novo(s: str) -> str:
    return RENOMEAR.get(s, s)


def aplicar_trocas(rel: str, h: str) -> str:
    for padrao, novo in TROCAS:
        h, n = re.subn(padrao, novo, h)
        if n:
            relatorio["trocas"][padrao] = relatorio["trocas"].get(padrao, 0) + n
    for velho, novo in RENOMEAR.items():
        h = h.replace(velho, novo)
    return h


# ---------- índice de artigos (do blog/index.html) ----------
indice = ler("blog/index.html")
ARTIGOS = []
for m in re.finditer(r'<a class="blog-card" data-cat="(\w+)" href="([^"]+)\.html".*?<h3>(.*?)</h3>', indice, re.S):
    cat, slug, titulo = m.group(1), m.group(2), H.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
    ARTIGOS.append({"cat": cat, "slug": slug_novo(slug), "titulo": aplicar_trocas("", titulo)})
POR_SLUG = {a["slug"]: a for a in ARTIGOS}


def relacionados(slug: str, n: int = 3) -> list[dict]:
    base = slug if slug in POR_SLUG else None
    cat = POR_SLUG[base]["cat"] if base else "trabalhista"
    candidatos = []
    if slug in GESTANTE:
        candidatos += [POR_SLUG[s] for s in GESTANTE if s != slug and s in POR_SLUG]
    candidatos += [a for a in ARTIGOS if a["cat"] == cat and a["slug"] != slug and a not in candidatos]
    # rodízio estável para não repetir sempre os mesmos 3
    k = sum(map(ord, slug)) % max(1, len(candidatos))
    return (candidatos[k:] + candidatos[:k])[:n]


def bloco_relacionados(itens: list[dict], titulo: str, tag: str, prefixo: str = "") -> str:
    cards = "\n".join(
        f'            <a href="{prefixo}{a["slug"]}.html" class="related-card">\n'
        f'                <span class="cat">{NOME_CAT.get(a["cat"], "Direito")}</span>\n'
        f'                <h4>{H.escape(a["titulo"])}</h4>\n            </a>' for a in itens)
    return (f'<section class="related-posts">\n    <div class="container">\n        <div class="section-header">\n'
            f'            <span class="section-tag">{tag}</span>\n            <h2>{titulo}</h2>\n        </div>\n'
            f'        <div class="related-grid">\n{cards}\n        </div>\n    </div>\n</section>\n\n')


def garantir_css(h: str) -> str:
    if ".related-card {" in h or ".related-card{" in h:
        return h
    return h.replace("</style>", CSS_REL + "    </style>", 1) if "</style>" in h else h.replace("</head>", f"<style>{CSS_REL}</style>\n</head>", 1)


def faq(h: str) -> list[tuple[str, str]]:
    m = re.search(r'<h2[^>]*>\s*Perguntas frequentes\s*</h2>(.*?)(?=<h2|<div class="article-cta|</article>|<section)', h, re.S | re.I)
    if not m:
        return []
    pares = re.findall(r"<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|$)", m.group(1), re.S)
    limpo = lambda t: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
    return [(limpo(q), limpo(r)) for q, r in pares if limpo(q) and limpo(r)]


def schema_artigo(h: str, slug: str) -> str:
    blocos = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    post = {}
    for b in blocos:
        try:
            d = json.loads(b)
        except Exception:
            continue
        if isinstance(d, dict) and d.get("@type") == "BlogPosting":
            post = d
    titulo = H.unescape(re.sub(r"<[^>]+>", "", (re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S) or [None, slug])[1])).strip()
    desc = H.unescape((re.search(r'<meta name="description" content="([^"]*)"', h) or [None, ""])[1])
    url = f"{BASE}/blog/{slug}.html"
    capa = re.search(r'capas/([^"\']+)\.(?:png|jpg)', h)
    imagem = f"{BASE}/blog/capas/{capa.group(1)}.jpg" if capa else f"{BASE}/assets/logo/logo-800x800.png"
    post.update({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": post.get("headline") or titulo,
        "description": post.get("description") or desc, "inLanguage": "pt-BR", "mainEntityOfPage": url, "url": url, "image": imagem,
        "author": {"@type": "Person", "name": "Dra. Letícia Barros", "jobTitle": "Advogada", "identifier": "OAB/ES 39.948",
                   "url": f"{BASE}/sobre.html", "sameAs": ["https://www.instagram.com/adv.leticiabarros2/"]},
        "publisher": {"@type": "LegalService", "name": "Letícia Barros Advocacia", "url": f"{BASE}/",
                      "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/logo/logo-800x800.png"}},
        "datePublished": post.get("datePublished") or HOJE, "dateModified": HOJE,
    })
    grafo = [post, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
        {"@type": "ListItem", "position": 3, "name": titulo, "item": url}]}]
    perguntas = faq(h)
    if perguntas:
        grafo.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in perguntas]})
    novo = "".join(f'    <script type="application/ld+json">\n{json.dumps(g, ensure_ascii=False, indent=2)}\n    </script>\n' for g in grafo)
    h = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", h, flags=re.S)
    return h.replace("</head>", novo + "</head>", 1), len(perguntas)


def artigo(rel: str) -> str:
    slug_velho = Path(rel).stem
    slug = slug_novo(slug_velho)
    h = aplicar_trocas(rel, ler(rel))
    h = re.sub(r'(capas/[^"\']+)\.png', r"\1.jpg", h)
    h, nfaq = schema_artigo(h, slug)
    rel_bloco = bloco_relacionados(relacionados(slug), "Outros artigos que podem<br>te interessar", "Continue lendo")
    if '<section class="related-posts">' in h:
        h = re.sub(r'<section class="related-posts">.*?</section>\s*', rel_bloco, h, count=1, flags=re.S)
    else:
        alvo = re.search(r'(<div class="gold-line"></div>\s*)?<!-- Footer -->|<footer', h)
        h = h[:alvo.start()] + rel_bloco + h[alvo.start():]
    h = garantir_css(h)
    relatorio.setdefault("faq", {})[slug] = nfaq
    return f"blog/{slug}.html", h


def pagina_area(rel: str, h: str) -> str:
    if rel in TITULOS_AREA:
        h = re.sub(r"<title>.*?</title>", f"<title>{TITULOS_AREA[rel]}</title>", h, count=1, flags=re.S)
    if rel in AREA_CAT and "artigos-do-tema" not in h:
        cat, nome = AREA_CAT[rel]
        itens = [a for a in ARTIGOS if a["cat"] == cat][:6]
        bloco = bloco_relacionados(itens, f"Artigos sobre {nome}", "Do blog", "../blog/").replace(
            '<section class="related-posts">', '<section class="related-posts" id="artigos-do-tema">').replace(
            '<span class="section-tag">', '<span class="section-tag" style="display:block;text-align:center;font-size:0.75rem;font-weight:600;'
            'letter-spacing:2px;text-transform:uppercase;color:var(--dourado);margin-bottom:8px;">')
        alvo = re.search(r'(<div class="gold-line"></div>\s*)?<!-- Footer -->|<footer', h)
        h = garantir_css(h[:alvo.start()] + bloco + h[alvo.start():])
    return h


CSS_HOME = """
        .home-blog { padding: 90px 0; }
        .home-blog-head { text-align: center; margin-bottom: 40px; }
        .home-blog-head span { display: block; font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--dourado); margin-bottom: 10px; }
        .home-blog-head h2 { font-family: 'Playfair Display', serif; font-size: 2.2rem; line-height: 1.2; color: var(--texto-claro); margin: 0; }
        .home-blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
        .home-blog-card { display: block; background: var(--fundo-alt); border: 1px solid rgba(201,169,98,0.12); border-radius: var(--radius-md);
            padding: 24px 22px; text-decoration: none; color: inherit; transition: transform .3s ease, border-color .3s ease; }
        .home-blog-card:hover { transform: translateY(-4px); border-color: rgba(201,169,98,0.35); }
        .home-blog-card small { display: block; font-size: 0.72rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--dourado); margin-bottom: 10px; }
        .home-blog-card strong { font-family: 'Playfair Display', serif; font-size: 1.1rem; line-height: 1.35; font-weight: 600; color: var(--texto-claro); }
        .home-blog-mais { text-align: center; margin-top: 32px; }
        @media (max-width: 1024px) { .home-blog-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 640px) { .home-blog-grid { grid-template-columns: 1fr; } .home-blog-head h2 { font-size: 1.7rem; } }
"""


def home(h: str) -> str:
    h = re.sub(r'(<meta name="description" content=")[^"]*"',
               r'\1Advogada em Vitória-ES com atuação em Direito Trabalhista, Família e Previdenciário. Direitos da gestante CLT, pensão alimentícia e INSS explicados sem juridiquês. OAB/ES 39.948."', h, count=1)
    if "home-blog" not in h:
        destaque = [POR_SLUG[s] for s in GESTANTE[:3] if s in POR_SLUG] + [a for a in ARTIGOS if a["cat"] in ("familia", "previdenciario")][:3]
        cards = "\n".join(f'            <a class="home-blog-card" href="blog/{a["slug"]}.html"><small>{NOME_CAT.get(a["cat"], "Direito")}</small>'
                          f'<strong>{H.escape(a["titulo"])}</strong></a>' for a in destaque)
        bloco = ('<section class="home-blog" id="artigos-do-blog">\n    <div class="container">\n'
                 '        <div class="home-blog-head"><span>Do blog</span><h2>Direitos explicados sem juridiquês</h2></div>\n'
                 f'        <div class="home-blog-grid">\n{cards}\n        </div>\n'
                 '        <p class="home-blog-mais"><a href="blog/" class="btn-primary">Ver todos os artigos</a></p>\n    </div>\n</section>\n\n')
        alvo = re.search(r'<section[^>]*id="contato"', h) or re.search(r"</main>", h)
        h = h[:alvo.start()] + bloco + h[alvo.start():]
        h = h.replace("</style>", CSS_HOME + "    </style>", 1) if "</style>" in h else h.replace("</head>", f"<style>{CSS_HOME}</style>\n</head>", 1)
    return h


def blog_indice(h: str) -> str:
    h = re.sub(r'(capas/[^"\']+)\.png', r"\1.jpg", h)
    if 'name="description"' not in h:
        h = h.replace("</title>", '</title>\n    <meta name="description" content="Artigos da Dra. Letícia Barros, advogada em Vitória-ES: direitos da gestante CLT, rescisão, pensão alimentícia, guarda e INSS, explicados sem juridiquês.">', 1)
    if 'rel="canonical"' not in h:
        h = h.replace("</title>", f'</title>\n    <link rel="canonical" href="{BASE}/blog/">', 1)
    return h


def sitemap(paginas: list[tuple[str, str]]) -> str:
    linhas = "\n".join(f"  <url><loc>{BASE}/{p}</loc><lastmod>{d}</lastmod></url>" for p, d in paginas)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n'


def llms() -> str:
    por_cat = {}
    for a in ARTIGOS:
        por_cat.setdefault(NOME_CAT.get(a["cat"], "Outros"), []).append(a)
    partes = [f"# Letícia Barros Advocacia\n\n> Dra. Letícia Barros, advogada em Vitória-ES (OAB/ES 39.948). Atuação em Direito Trabalhista "
              "(com foco nos direitos da gestante CLT), Direito de Família e Direito Previdenciário. Atendimento em Vitória e online. "
              "O conteúdo do blog explica direitos em linguagem simples, com a base legal citada.\n",
              f"## Páginas principais\n\n- [Início]({BASE}/)\n- [Sobre a Dra. Letícia Barros]({BASE}/sobre.html)\n- [Contato]({BASE}/contato.html)\n"
              f"- [Perguntas frequentes]({BASE}/faq.html)\n- [Direito Trabalhista]({BASE}/areas/direito-trabalhista.html)\n"
              f"- [Direito de Família]({BASE}/areas/direito-familia.html)\n- [Direito Previdenciário]({BASE}/areas/direito-previdenciario.html)\n"
              f"- [Blog]({BASE}/blog/)\n"]
    for nome, itens in por_cat.items():
        partes.append(f"## Artigos: {nome}\n\n" + "\n".join(f"- [{a['titulo']}]({BASE}/blog/{a['slug']}.html)" for a in itens) + "\n")
    return "\n".join(partes)


def htaccess(h: str) -> str:
    if "# SEO 10/10/2026" in h:
        return h
    regras = ["# SEO 10/10/2026: arquivos ocultos fora do ar e endereços novos (palavras vetadas)",
              "RedirectMatch 404 /\\.(?!well-known)"]
    regras += [f"Redirect 301 /blog/{v}.html {BASE}/blog/{n}.html" for v, n in RENOMEAR.items()]
    return "\n".join(regras) + "\n\n" + h


def gravar(rel: str, conteudo: str) -> None:
    destino = SAIDA / rel
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    relatorio["alterados"].append(rel)


def main() -> None:
    paginas = []
    for f in sorted(ORIG.rglob("*.html")):
        rel = f.relative_to(ORIG).as_posix()
        if rel.startswith(".claude/") or rel.startswith("google"):
            continue
        original = ler(rel)
        if rel.startswith("blog/") and rel != "blog/index.html":
            rel_novo, h = artigo(rel)
            gravar(rel_novo, h)
            paginas.append((rel_novo, HOJE))
            continue
        h = aplicar_trocas(rel, original)
        if rel == "blog/index.html":
            h = blog_indice(h)
        elif rel == "index.html":
            h = home(h)
        elif rel.startswith("areas/"):
            h = pagina_area(rel, h)
        if h != original:
            gravar(rel, h)
        if not rel.startswith("lp-v3/") and rel not in ("blog/index.html",):
            paginas.append((rel if rel != "index.html" else "", HOJE if h != original else "2026-10-01"))
    paginas.insert(1, ("blog/", HOJE))
    gravar("sitemap.xml", sitemap(paginas))
    gravar("llms.txt", llms())
    gravar(".htaccess", htaccess(ler(".htaccess")))
    (SAIDA / "_relatorio.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=1), encoding="utf-8")
    print("alterados:", len(relatorio["alterados"]), "| trocas:", sum(relatorio["trocas"].values()),
          "| artigos com FAQ:", sum(1 for v in relatorio["faq"].values() if v), "de", len(relatorio["faq"]))


main()
