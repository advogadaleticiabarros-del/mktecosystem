"""(19/11/2026, artigo do decreto da 5x2; cópia do montador de 16/11 com o bloco FAQPage.) Converte os rascunhos .md desta pasta no spec.json que o publicador do Orbit usa.

Regras do blog: blockquote com **Título** vira .callout-box, tabela vira .prova-table,
link /blog/x.html vira x.html (relativo), H1 e frontmatter saem do corpo.
"""
import html as H
import json
import re
import sys
from pathlib import Path

PASTA = Path(__file__).parent
ARTIGOS = [
    ("escala-5x2-decreto-duvidas", "Escala 5x2: 12 dúvidas sobre o decreto",
     "O decreto da 5x2 saiu: quando a 6x1 acaba, se o salário cai, como fica a hora extra, a doméstica e a 12x36."),
]


def inline(t: str) -> str:
    t = H.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    def link(m):
        url = m.group(2)
        url = re.sub(r"^/blog/", "", url)
        return f'<a href="{url}">{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)


def md_para_html(md: str) -> tuple[dict, str]:
    meta = {}
    if md.startswith("---"):
        _, fm, md = md.split("---", 2)
        for linha in fm.strip().splitlines():
            k, v = linha.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    linhas = md.strip().splitlines()
    out, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            i += 1; continue
        if l.startswith("# "):
            i += 1; continue
        if l.startswith("### "):
            out.append(f"<h3>{inline(l[4:])}</h3>"); i += 1; continue
        if l.startswith("## "):
            out.append(f"<h2>{inline(l[3:])}</h2>"); i += 1; continue
        if l.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i][1:].strip()); i += 1
            titulo = re.fullmatch(r"\*\*(.+)\*\*", bloco[0])
            assert titulo, bloco
            corpo = " ".join(b for b in bloco[1:] if b)
            out.append(f'<div class="callout-box">\n<h4>{titulo.group(1)}</h4>\n<p>{inline(corpo)}</p>\n</div>')
            continue
        if l.startswith("|"):
            rows = []
            while i < len(linhas) and linhas[i].startswith("|"):
                cel = [c.strip() for c in linhas[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cel):
                    rows.append(cel)
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            trs = "\n".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<table class="prova-table">\n<tr>{th}</tr>\n{trs}\n</table>')
            continue
        if re.match(r"^- ", l):
            itens = []
            while i < len(linhas) and linhas[i].startswith("- "):
                itens.append(f"<li>{inline(linhas[i][2:])}</li>"); i += 1
            out.append("<ul>\n" + "\n".join(itens) + "\n</ul>"); continue
        if re.match(r"^\d+\. ", l):
            itens = []
            while i < len(linhas) and re.match(r"^\d+\. ", linhas[i]):
                itens.append(f"<li>{inline(re.sub(r'^\d+\. ', '', linhas[i]))}</li>"); i += 1
            out.append("<ol>\n" + "\n".join(itens) + "\n</ol>"); continue
        par = []
        while i < len(linhas) and linhas[i].strip() and not re.match(r"^(#|>|\||- |\d+\. )", linhas[i]):
            par.append(linhas[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(par))}</p>")
    return meta, "\n\n".join(out) + faq(out)


def faq(blocos: list[str]) -> str:
    """JSON-LD FAQPage: cada H2 "N. pergunta?" vira pergunta e o primeiro parágrafo seguinte, resposta (Google e IAs)."""
    def limpo(t):
        return H.unescape(re.sub(r"<[^>]+>", "", t))
    itens = []
    for i, b in enumerate(blocos):
        m = re.fullmatch(r"<h2>\d+\. (.+\?)</h2>", b)
        if m and i + 1 < len(blocos) and blocos[i + 1].startswith("<p>"):
            itens.append({"@type": "Question", "name": limpo(m.group(1)),
                          "acceptedAnswer": {"@type": "Answer", "text": limpo(blocos[i + 1])}})
    if not itens:
        return ""
    dados = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": itens}, ensure_ascii=False)
    return f'\n\n<script type="application/ld+json">{dados}</script>'


def main():
    spec = []
    for slug, google, resumo in ARTIGOS:
        meta, corpo = md_para_html((PASTA / f"{slug}.md").read_text(encoding="utf-8"))
        assert meta["slug"] == slug
        assert "deficiência" not in corpo.lower() and "R$" not in meta["meta_description"]
        spec.append({"slug": slug, "titulo": meta["titulo"], "titulo_google": google,
                     "meta_description": meta["meta_description"], "resumo": resumo,
                     "html": corpo, "capa": f"capa-{slug}.jpg"})
    destino = PASTA / "spec.json"
    destino.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    for a in spec:
        print(a["slug"], len(a["html"]), "chars", len(a["meta_description"]), "desc", len(a["titulo_google"]), "google")


if __name__ == "__main__":
    sys.exit(main())
