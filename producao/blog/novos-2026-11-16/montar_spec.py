"""Converte os rascunhos .md desta pasta no spec.json que o publicador do Orbit usa.

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
    ("o-que-muda-na-clt-em-2027", "O que muda na CLT em 2027: calendário completo",
     "Jornada de 42 e 40 horas, fim da 6x1, licença-paternidade de 10 dias e o que ainda está em aberto, com as datas certas."),
    ("escala-42-horas-16-de-dezembro-e-se-a-empresa-nao-mudar", "Escala de 42 horas em 16/12: e se a empresa não mudar?",
     "O STF manteve o fim da 6x1 em 16/12. Veja a regra das 8h24, as convenções e o que fazer se a escala não mudar."),
    ("hora-extra-jornada-42-horas-como-calcular", "Hora extra com jornada de 42 horas: como calcular",
     "Com a jornada menor e o mesmo salário, a sua hora vale mais. A conta do divisor 210 e 200, passo a passo."),
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
    return meta, "\n\n".join(out)


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
