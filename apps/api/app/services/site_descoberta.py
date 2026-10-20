"""Como buscadores e IAs descobrem o site da Letícia (20/10/2026).

Uma interface pequena para o publicador do blog:
- `gerar_llms_txt(indice_html)`: o `/llms.txt` inteiro (identificação, páginas, áreas e todos os
  artigos do índice do blog, sem repetição, agrupados por área);
- `avisar_indexnow(urls)`: avisa Bing (e outros buscadores do IndexNow) que as URLs mudaram.
  O ChatGPT busca pelo índice do Bing, então artigo novo aparece lá em horas, não semanas.
  Nunca derruba a publicação: falha de rede só vira log.

A chave do IndexNow é pública por definição (fica em `/{chave}.txt` na raiz do site).
"""
import logging
import re

import httpx

from app.services.blog_seo import _texto

logger = logging.getLogger(__name__)

SITE = "https://advogadaleticiabarros.com.br"
INDEXNOW_CHAVE = "6bc7d2f33225bd1d3c4af27b891f2ac6"
INDEXNOW_API = "https://api.indexnow.org/indexnow"

DESCRICAO = (
    "Dra. Letícia Barros, advogada em Vitória-ES (OAB/ES 39.948). Atuação em Direito Trabalhista "
    "(com foco nos direitos da gestante CLT), Direito de Família e Direito Previdenciário. Atendimento "
    "em Vitória e online. O conteúdo do blog explica direitos em linguagem simples, com a base legal citada."
)
PAGINAS = [
    ("Início", "/"),
    ("Sobre a Dra. Letícia Barros", "/sobre.html"),
    ("Escritório Santiago Prado & Barros Advogados", "/escritorio.html"),
    ("Contato", "/contato.html"),
    ("Perguntas frequentes", "/faq.html"),
    ("Blog", "/blog/"),
]
AREAS = [
    ("Direito Trabalhista", "/areas/direito-trabalhista.html"),
    ("Direito de Família e pensão alimentícia", "/areas/direito-familia.html"),
    ("Direito Previdenciário e BPC/LOAS", "/areas/direito-previdenciario.html"),
    ("Direito do Consumidor", "/areas/direito-consumidor.html"),
    ("Direito Civil", "/areas/direito-civil.html"),
    ("Assessoria Jurídica", "/areas/assessoria-juridica.html"),
    ("Soluções Extrajudiciais", "/areas/extrajudiciais.html"),
]
GUIAS = [
    ("Direitos da gestante CLT", "/lp/gestante-clt.html"),
    ("Guia completo: direitos da gestante trabalhadora (CLT)", "/lp/guia-direitos-gestante-trabalhadora.html"),
    ("Pensão alimentícia", "/lp/pensao-alimenticia.html"),
    ("BPC/LOAS para crianças com necessidades especiais", "/lp/bpc-loas-criancas.html"),
    ("Adicional de insalubridade", "/lp/insalubridade-clt.html"),
    ("Assessoria jurídica para empresas", "/lp/assessoria-empresarial.html"),
]
SECOES_ARTIGOS = [
    ("trabalhista", "Artigos: Trabalhista"),
    ("familia", "Artigos: Família"),
    ("previdenciario", "Artigos: Previdenciário"),
    ("consumidor", "Artigos: Consumidor"),
]


def _area(data_cat: str) -> str:
    return re.sub(r"^direito-(de-|do-)?", "", data_cat)


def _artigos(indice_html: str) -> list[dict]:
    vistos, artigos = set(), []
    for m in re.finditer(r'<a\b([^>]*class="blog-card"[^>]*)>(.*?)</a>', indice_html, re.S):
        atributos, corpo = m.group(1), m.group(2)
        href = re.search(r'href="([^"/]+\.html)"', atributos)
        titulo = re.search(r"<h3[^>]*>(.*?)</h3>", corpo, re.S)
        if not href or not titulo or href.group(1) in vistos:
            continue
        vistos.add(href.group(1))
        cat = re.search(r'data-cat="([^"]+)"', atributos)
        resumo = re.search(r"<p[^>]*>(.*?)</p>", corpo, re.S)
        artigos.append({
            "url": f"{SITE}/blog/{href.group(1)}",
            "titulo": _texto(titulo.group(1)),
            "resumo": _texto(resumo.group(1)) if resumo else "",
            "area": _area(cat.group(1)) if cat else "",
        })
    return artigos


def _linha(titulo: str, url: str, resumo: str = "") -> str:
    return f"- [{titulo}]({url}): {resumo}" if resumo else f"- [{titulo}]({url})"


def gerar_llms_txt(indice_html: str) -> str:
    artigos = _artigos(indice_html)
    blocos = [f"# Letícia Barros Advocacia\n\n> {DESCRICAO}"]
    blocos.append("## Páginas principais\n\n" + "\n".join(_linha(t, SITE + c) for t, c in PAGINAS))
    blocos.append("## Áreas de atuação\n\n" + "\n".join(_linha(t, SITE + c) for t, c in AREAS))
    blocos.append("## Guias por tema\n\n" + "\n".join(_linha(t, SITE + c) for t, c in GUIAS))
    conhecidas = {area for area, _ in SECOES_ARTIGOS}
    for area, titulo_secao in SECOES_ARTIGOS:
        da_area = [a for a in artigos if a["area"] == area]
        if da_area:
            blocos.append(f"## {titulo_secao}\n\n" + "\n".join(_linha(a["titulo"], a["url"], a["resumo"]) for a in da_area))
    outros = [a for a in artigos if a["area"] not in conhecidas]
    if outros:
        blocos.append("## Outros conteúdos\n\n" + "\n".join(_linha(a["titulo"], a["url"], a["resumo"]) for a in outros))
    return "\n\n".join(blocos) + "\n"


async def avisar_indexnow(urls: list[str], *, transport: httpx.AsyncBaseTransport | None = None) -> int | None:
    corpo = {
        "host": SITE.removeprefix("https://"),
        "key": INDEXNOW_CHAVE,
        "keyLocation": f"{SITE}/{INDEXNOW_CHAVE}.txt",
        "urlList": urls,
    }
    try:
        async with httpx.AsyncClient(transport=transport, timeout=20) as client:
            resposta = await client.post(INDEXNOW_API, json=corpo)
    except httpx.HTTPError:
        logger.warning("IndexNow indisponível; %d URL(s) não avisadas", len(urls), exc_info=True)
        return None
    if resposta.status_code >= 300:
        logger.warning("IndexNow respondeu %s: %s", resposta.status_code, resposta.text[:200])
    return resposta.status_code
