"""Arquivo de conferência com os criativos (regra da Jessica, 11/11/2026: "Me mande um arquivo para conferência sempre
e já com os criativos"). Para cada peça: a arte (ou a capa do Reels, com link do vídeo), data e hora, legenda,
primeiro comentário e base legal, em seções por prioridade de revisão. Lê os JSON do editorial e baixa as miniaturas da
mídia pública do Orbit.

Uso: python pagina_conferencia.py <pasta_saida> <editorial.json> [<editorial.json> ...]
     → <pasta_saida>/index.html + img/ (publicar como Artifact)"""
import hashlib
import html
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

MIDIA = "https://api.orbit.advogadaleticiabarros.com.br/media/"
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
SECOES = [  # (chave, título, explicação)
    ("novo", "Textos novos: conferir a lei", "Escritos agora, nunca revisados pela Dra. Conferir afirmação, explicação e base legal."),
    ("manchete", "Manchetes: citações escritas de memória", "Arte e legenda aprovadas pela Jessica; a base legal precisa da conferência da Dra."),
    ("arte", "Arte nova, texto já aprovado", "Só conferir a imagem: o texto é o mesmo que a Dra. já aprovou."),
]


def secao(a):
    if a["acao"] == "agendar":
        return "arte" if a.get("nova_imagem") else None  # frase da reserva sem mudança: já aprovada
    if a["acao"] == "dra":
        return "arte"
    if a["acao"] == "mover":
        return None
    if a.get("estilo") == "manchete":
        return "manchete"
    if a.get("estilo") == "flagrante":
        return None  # aprovados em 09/11/2026
    if a.get("estilo") == "mito-ou-lei" and a["dia"] < "2027-02-01":
        return None  # afirmações já aprovadas como estático
    return "novo"


def miniatura(arq, pasta, w=540):
    nome = hashlib.sha1(arq.encode()).hexdigest()[:12] + ".jpg"
    alvo = pasta / "img" / nome
    if not alvo.exists():
        req = urllib.request.Request(MIDIA + arq, headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(urllib.request.urlopen(req, timeout=40)).convert("RGB")
        ImageOps.fit(im, (w, w * 4 // 3), Image.LANCZOS, centering=(.5, .5)).save(alvo, quality=80)
    return f"img/{nome}"


def cartao(a, pasta):
    d = date.fromisoformat(a["dia"])
    img = a.get("capa") or a.get("arquivo") or a.get("nova_imagem")
    fig = f'<img src="{miniatura(img, pasta)}" alt="Arte de {html.escape(a.get("titulo", ""))}" loading="lazy">' if img else ""
    tipo = "Reels" if a.get("formato") == "reels" else "Post"
    video = (f'<a class=vid href="{MIDIA}{a["video"]}" target="_blank" rel="noreferrer">▶ Assistir o vídeo</a>'
             if a.get("video") else "")
    leg = html.escape(a.get("legenda", "")) or "<i>Texto já aprovado (mesma legenda de antes).</i>"
    com = html.escape(a.get("primeiro_comentario", ""))
    titulo = html.escape(a.get("titulo") or a.get("titulo_contem") or "Pergunta (arte clara)")
    return f"""<article class=c id="p-{a['dia']}-{a.get('hora','').replace(':','')}">
<figure>{fig}{video}</figure>
<div class=tx><p class=meta>{DIAS[d.weekday()]} {d:%d/%m/%Y} · {a.get('hora','')} · {tipo}</p><h3>{titulo}</h3>
<details open><summary>Legenda</summary><pre>{leg}</pre></details>
{f'<details open><summary>Primeiro comentário</summary><pre>{com}</pre></details>' if com else ''}
</div></article>"""


def main(pasta, arquivos):
    (pasta / "img").mkdir(parents=True, exist_ok=True)
    acoes = []
    for f in arquivos:
        acoes += json.loads(Path(f).read_text(encoding="utf-8"))
    grupos = {k: [] for k, _, _ in SECOES}
    for a in sorted(acoes, key=lambda x: (x.get("dia", ""), x.get("hora", ""))):
        s = secao(a)
        if s:
            grupos[s].append(a)
    corpo, indice = [], []
    for k, tit, exp in SECOES:
        itens = grupos[k]
        if not itens:
            continue
        indice.append(f'<a href="#s-{k}">{tit} <b>{len(itens)}</b></a>')
        corpo.append(f'<section id="s-{k}"><h2>{tit}</h2><p class=exp>{exp}</p>'
                     + "".join(cartao(a, pasta) for a in itens) + "</section>")
    modelo = Path(__file__).with_name("pagina_conferencia.html").read_text(encoding="utf-8")
    total = sum(len(v) for v in grupos.values())
    out = modelo.replace("{{INDICE}}", "".join(indice)).replace("{{CORPO}}", "".join(corpo)).replace("{{TOTAL}}", str(total))
    (pasta / "index.html").write_text(out, encoding="utf-8")
    print("ok", total, {k: len(v) for k, v in grupos.items()})


if __name__ == "__main__":
    main(Path(sys.argv[1]), sys.argv[2:])
