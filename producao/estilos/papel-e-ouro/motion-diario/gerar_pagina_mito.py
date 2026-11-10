"""Gera mito-lei/aprovacao.html e mito_reels.json (dados para o mito_reels.py do Orbit).
Uso: python gerar_pagina_mito.py"""
import html
import json
from pathlib import Path

from mito_lei import TELA, conteudo_nov, itens

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI / "mito-lei"
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

# tema (MM-DD) -> dia novo (Reels 19h, segunda, quarta e sábado; pedido de 10/11/2026)
GRADE = {
    "11-12": "2026-11-11", "11-14": "2026-11-14", "11-16": "2026-11-16", "11-18": "2026-11-18",
    "11-20": "2026-11-21", "11-22": "2026-11-23", "11-08": "2026-11-25", "11-24": "2027-01-11", "11-26": "2026-11-28",
    "11-30": "2026-11-30", "12-02": "2026-12-02", "12-04": "2026-12-05", "12-06": "2026-12-07",
    "12-08": "2026-12-09", "12-12": "2026-12-12", "12-14": "2026-12-14", "12-18": "2026-12-16",
    "12-20": "2026-12-19", "12-22": "2026-12-21", "12-24": "2026-12-23", "12-26": "2026-12-26",
    "12-28": "2026-12-28", "12-30": "2026-12-30",
    "12-10": "2027-01-02", "11-28": "2027-01-04", "12-16": "2027-01-07", "11-10": "2027-01-09",
}


def episodios():
    from datetime import date
    out = []
    for md, m in itens():
        out.append((md, m, f"{md}-{m[1]}", RAIZ / f"{md}-{m[1]}", TELA[md][0], m[3]))
    out.sort(key=lambda e: GRADE[e[0]])
    return [(md, m, nome, pasta, frase, ver, date.fromisoformat(GRADE[md])) for md, m, nome, pasta, frase, ver in out]


def main():
    eps = episodios()
    cards, dados = "", []
    for i, (md, m, nome, pasta, frase, ver, dia) in enumerate(eps, 1):
        leg = json.loads((pasta / "legenda.json").read_text(encoding="utf-8"))
        video = f"mito-lei-{nome}-v3.mp4"
        dados.append({"tema": m[0], "dia": str(dia), "video": video, "legenda": leg["legenda"],
                      "primeiro_comentario": leg.get("primeiro_comentario", "")})
        cards += f'''<article class="ep"><div class="vid"><video src="videos/{video}" controls playsinline preload="metadata"></video></div>
<div class="txt"><p class="dia">{i:02d} · {DIAS[dia.weekday()]} {dia:%d/%m} · 19h</p><h2>{html.escape(frase)}</h2>
<p class="ver {ver.lower()}">{ver}</p><p class="lei">{html.escape(m[5])}</p>
<details><summary>Ver a legenda do post</summary><pre>{html.escape(leg["legenda"])}</pre></details></div></article>'''
    (AQUI.parents[3] / "apps/api/_saida_producao_1510/mito_reels.json").write_text(
        json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    pagina = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mito ou Lei · aprovação</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,400&family=Inter:wght@400;500;600&display=swap">
<style>
:root{{--bg:#1E1814;--card:#2A231E;--fg:#EFE6D9;--mute:#B8AC9C;--ouro:#D8B566;--linha:#4A3F35;--vinho:#C9786F;color-scheme:dark}}
:root[data-theme="light"]{{--bg:#F4EEE5;--card:#FFFDF9;--fg:#1E1814;--mute:#6B5D4E;--ouro:#8A6A24;--linha:#DDD2C2;--vinho:#8E2F2A;color-scheme:light}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#1E1814}}}}
:root[data-theme="dark"]{{--bg:#1E1814}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:400 16px/1.6 Inter,system-ui,sans-serif}}
main{{max-width:980px;margin:0 auto;padding:40px 16px 80px}}
h1{{font:500 44px/1.1 'EB Garamond',Georgia,serif;margin:0 0 8px}}
.intro{{color:var(--mute);max-width:66ch}}
.pede{{border-left:3px solid var(--ouro);padding:12px 16px;background:var(--card);margin:24px 0 32px;border-radius:0 8px 8px 0}}
.ep{{display:grid;grid-template-columns:260px 1fr;gap:28px;padding:28px 0;border-top:1px solid var(--linha)}}
.vid video{{width:100%;aspect-ratio:9/16;background:#000;border-radius:10px;display:block}}
.dia{{color:var(--ouro);font-weight:600;letter-spacing:.04em;margin:0}}
h2{{font:500 28px/1.2 'EB Garamond',Georgia,serif;margin:6px 0 10px}}
.ver{{display:inline-block;font-weight:600;letter-spacing:.08em;padding:2px 12px;border-radius:4px;margin:0;border:1px solid}}
.ver.mito{{color:var(--vinho)}}.ver.lei{{color:var(--ouro)}}
.lei{{color:var(--mute);font-size:14px}}
summary{{cursor:pointer;color:var(--ouro)}}
pre{{white-space:pre-wrap;font:400 14px/1.55 Inter,sans-serif;background:var(--card);padding:14px;border-radius:8px}}
@media (max-width:640px){{.ep{{grid-template-columns:1fr}}.vid{{max-width:300px}}}}
</style></head><body><main>
<h1>Mito ou Lei · Reels</h1>
<p class="intro">A série Mito ou Lei passa de post estático para Reels no estilo Flagrante. São {len(eps)} vídeos, às 19h de segunda, quarta e sábado, dias sem os outros Reels. O estático antigo de cada tema sai da agenda e fica guardado.</p>
<div class="pede"><b>O que precisamos:</b> aprovar, pedir ajuste ou descartar cada vídeo. Pode comentar nesta página ou mandar mensagem citando o número. Nada vai para o Orbit antes da aprovação. A Dra. confere as bases legais.</div>
{cards}
</main></body></html>'''
    (RAIZ / "aprovacao.html").write_text(pagina, encoding="utf-8")
    print(len(eps), "episódios")


if __name__ == "__main__":
    main()
