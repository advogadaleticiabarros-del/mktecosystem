"""Página do Caderno da marca + feed planejado (até o último dia agendado em FIM) (pedido da Jessica em 10/11/2026), para publicar como
Artifact. Lê a saída de ver_feed.py (TSV, rodado no container) e as peças de exemplo de cada estilo no repositório.

Uso: python pagina_caderno.py <feed.tsv> <pasta_saida>   → <pasta_saida>/index.html + img/*.jpg (miniaturas)"""
import hashlib
import html
import subprocess
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[3]
EST = RAIZ / "producao" / "estilos"
MOT = EST / "papel-e-ouro" / "motion-diario"
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
FIM = date(2027, 2, 28)

ESTILOS = [
    ("Manchete", "O padrão do estático avulso desde 09/11. Título como manchete, faixa de ouro, objeto ou foto forte.",
     ["manchete/pecas/manchete-13-doar-sangue.jpg", "manchete/pecas/manchete-04-cabelo.jpg", "manchete/pecas/manchete-09-exame.jpg"]),
    ("Papel e Ouro", "Revista em papel fosco, ouro em poucos pontos. Peças de marca e fora da caixa.",
     ["papel-e-ouro/pecas/clara-05-gritar.jpg", "papel-e-ouro/pecas/fora-04-errata.jpg", "papel-e-ouro/pecas/clara-07-rapidinho.jpg"]),
    ("Verbete e Palavra de Ouro", "Dicionário em papel claro para a marca; palavra em ouro sobre foto P&B como acento escuro.",
     ["verbete/pecas/01-leticia-barros.jpg", "palavra-de-ouro/pecas/01-hora-extra.jpg", "papel-e-ouro/pecas/clara-02-capa-nome.jpg"]),
    ("Flagrante", "Reels motion: a cena do dia a dia pega no flagra, sons reais, sem voz. Capa textura.",
     ["papel-e-ouro/motion-diario/05-ferias/capa-textura.jpg", "papel-e-ouro/motion-diario/01-atestado/capa-textura.jpg",
      "papel-e-ouro/motion-diario/03-ponto/capa-textura.jpg"]),
    ("Mito ou Lei", "Reels com roleta e carimbo. Capa Moldura Viva: papel claro e a foto do tema saindo da moldura.",
     ["papel-e-ouro/motion-diario/mito-lei/01-13-demitido-13/capa-moldura-viva.jpg",
      "papel-e-ouro/motion-diario/mito-lei/01-20-cancer-inss/capa-moldura-viva.jpg",
      "papel-e-ouro/motion-diario/mito-lei/01-30-casamento-70/capa-moldura-viva.jpg"]),
    ("Domingo com a Dra.", "Vídeo gravado por ela, domingo 15h30. Capa com retrato real dela sentada, em quadro dourado 3D.",
     ["../../apps/api/_saida_producao_1510/envio_jan/dra-capa-2026-11-15.jpg",
      "../../apps/api/_saida_producao_1510/envio_jan/dra-capa-2026-11-29.jpg",
      "../../apps/api/_saida_producao_1510/envio_jan/dra-capa-2026-12-27.jpg"]),
]


def miniatura(origem, pasta, w=360):
    """Baixa (URL) ou abre (arquivo) e grava uma miniatura 3:4; devolve o caminho relativo ou None."""
    nome = hashlib.sha1(str(origem).encode()).hexdigest()[:12] + ".jpg"
    alvo = pasta / "img" / nome
    if alvo.exists():
        return f"img/{nome}"
    try:
        if str(origem).startswith("http"):
            base = str(origem).split("?")[0]
            if base.endswith(".mp4"):
                tmp = pasta / "img" / "_q.jpg"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.2", "-i", base, "-frames:v", "1", str(tmp)], check=True)
                im = Image.open(tmp)
            else:
                req = urllib.request.Request(base, headers={"User-Agent": "Mozilla/5.0"})
                im = Image.open(urllib.request.urlopen(req, timeout=40))
        else:
            im = Image.open(origem)
        im = ImageOps.fit(im.convert("RGB"), (w, w * 4 // 3), Image.LANCZOS, centering=(.5, .5))
        im.save(alvo, quality=82)
        return f"img/{nome}"
    except Exception as e:  # noqa: BLE001
        print("sem imagem:", origem, e)
        return None


def classe(fmt, tipo, titulo, status):
    if fmt == "reels":
        if titulo.startswith("Mito ou Lei"):
            k = "mito"
        elif "Flagrante" in titulo:
            k = "flag"
        else:
            k = "dra"
    elif fmt == "carrossel":
        k = "carr"
    elif tipo == "frase":
        k = "frase"
    else:
        k = "est"
    return k + (" pausado" if status == "pausado" else "")


ROTULO = {"mito": "Reels · Mito ou Lei", "flag": "Reels · Flagrante", "dra": "Reels · Domingo com a Dra.",
          "carr": "Carrossel", "frase": "Frase", "est": "Estático"}


def main(tsv, pasta):
    (pasta / "img").mkdir(parents=True, exist_ok=True)
    linhas = []
    for l in Path(tsv).read_text(encoding="utf-8").splitlines():
        c = l.split("\t")
        if len(c) < 8 or c[2] != "instagram" or c[3] in ("story", "trial"):
            continue
        d = date.fromisoformat(c[0])
        if d > FIM:
            continue
        linhas.append((d, c[1], c[3], c[5], c[4], c[6], c[7]))
    linhas.sort()
    itens = []
    for d, hora, fmt, tipo, status, titulo, img in linhas:
        k = classe(fmt, tipo, titulo, status)
        itens.append({"d": d, "hora": hora, "k": k, "titulo": titulo, "status": status, "img": miniatura(img, pasta) if img else None})
    ativos = [i for i in itens if i["status"] != "pausado" and i["status"] != "publicado"]
    cont = Counter(i["k"].split()[0] for i in ativos)
    # grade: do mais novo para o mais antigo, como no perfil
    grade = []
    for i in sorted(itens, key=lambda x: (x["d"], x["hora"]), reverse=True):
        img = f'<img src="{i["img"]}" alt="" loading="lazy">' if i["img"] else '<div class=sem>sem imagem</div>'
        ico = "▶" if i["k"].split()[0] in ("mito", "flag", "dra") else ("❐" if i["k"].startswith("carr") else "")
        grade.append(f'<figure class="g {i["k"]}">{img}<span class=ico>{ico}</span>'
                     f'<figcaption>{DIAS[i["d"].weekday()]} {i["d"]:%d/%m} · {i["hora"]}</figcaption></figure>')
    # lista por semana
    semanas, atual = [], None
    for i in itens:
        seg = i["d"].toordinal() - i["d"].weekday()
        if seg != atual:
            semanas.append((date.fromordinal(seg), []))
            atual = seg
        semanas[-1][1].append(i)
    lista = []
    for ini, its in semanas:
        dias = {}
        for i in its:
            dias.setdefault(i["d"], []).append(i)
        blocos = []
        for d in sorted(dias):
            lis = "".join(
                f'<li class="{i["k"]}">' + (f'<img src="{i["img"]}" alt="" class=th loading="lazy">' if i["img"] else '<span class="th sem"></span>')
                + f'<div><b>{i["hora"]}</b> <span class=tag>{ROTULO[i["k"].split()[0]]}</span>'
                + (' <span class=pa>pausado</span>' if i["status"] == "pausado" else "")
                + (' <span class=pa>publicado</span>' if i["status"] == "publicado" else "")
                + f'<p>{html.escape(i["titulo"])}</p></div></li>' for i in sorted(dias[d], key=lambda x: x["hora"]))
            blocos.append(f'<div class=dia><div class=dt><b>{DIAS[d.weekday()]}</b>{d:%d/%m}</div><ul>{lis}</ul></div>')
        lista.append(f'<section><h3>Semana de {ini:%d/%m}</h3>{"".join(blocos)}</section>')
    estilos = []
    for nome, desc, arqs in ESTILOS:
        figs = "".join(f'<img src="{m}" alt="" loading="lazy">' for m in (miniatura(EST / a, pasta) for a in arqs) if m)
        estilos.append(f'<article class=est><div class=tx><h3>{nome}</h3><p>{desc}</p></div><div class=ex>{figs}</div></article>')
    sem = max(1, len({(i["d"].isocalendar()[1]) for i in ativos}))
    total = len(ativos)
    modelo = (Path(__file__).with_name("pagina_caderno.html")).read_text(encoding="utf-8")
    out = (modelo.replace("{{ESTILOS}}", "".join(estilos)).replace("{{GRADE}}", "".join(grade))
           .replace("{{LISTA}}", "".join(lista)).replace("{{TOTAL}}", str(total))
           .replace("{{CONT}}", " · ".join(f"{ROTULO[k]}: {v}" for k, v in cont.most_common())))
    (pasta / "index.html").write_text(out, encoding="utf-8")
    print("ok", total, cont, sem)


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
