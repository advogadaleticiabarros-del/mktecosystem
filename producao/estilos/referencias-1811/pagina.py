"""Página de conferência das peças feitas a partir das referências de 18/11/2026 (regra de 11/11/2026: toda entrega vai
com arquivo de conferência já com os criativos). Mostra a referência ao lado da peça, legenda, primeiro comentário,
base legal e texto alternativo. Uso: python pagina.py → conferencia/index.html + conferencia/img/ (publicar como Artifact)."""
import html
import json
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "conferencia"
REFS = {"01": [1], "02": [2], "03": [3], "04": [4], "05": [5], "06": [6], "07": [7], "08": [8], "09": [9], "10": [10],
        "11": [11], "12": [11], "13": [12, 13, 14], "14": [15, 16]}


def mini(origem, nome, w):
    alvo = OUT / "img" / nome
    im = Image.open(origem).convert("RGB")
    im.thumbnail((w, w * 2), Image.LANCZOS)
    im.save(alvo, quality=82)
    return f"img/{nome}"


def main():
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    itens = json.loads((AQUI / "conteudo.json").read_text(encoding="utf-8"))
    cards = []
    for it in itens:
        e = html.escape
        peca = mini(AQUI / "pecas" / f"{it['peca']}.jpg", f"{it['peca']}.jpg", 720)
        refs = "".join(f'<img src="{mini(AQUI / "referencias" / f"{r}.png", f"ref-{r}.jpg", 300)}" alt="Referência {r}" loading="lazy">' for r in REFS[it["n"]])
        conferir = '<span class="tag">conferir</span>' if "CONFERIR" in it["base_legal"] else ""
        cards.append(f"""<article class="peca" id="p{it['n']}">
<figure class="arte"><img src="{peca}" alt="{e(it['alt'])}" loading="lazy"></figure>
<div class="texto">
  <p class="num">Peça {it['n']}</p>
  <h2>{e(it['titulo'])}</h2>
  <div class="ref"><div class="ref-imgs">{refs}</div><p><b>Referência:</b> {e(it['referencia'])}</p></div>
  <section><div class="cab"><h3>Legenda</h3><button type="button" data-copy="leg{it['n']}">Copiar</button></div><pre id="leg{it['n']}">{e(it['legenda'])}</pre></section>
  <section><div class="cab"><h3>Primeiro comentário</h3><button type="button" data-copy="com{it['n']}">Copiar</button></div><pre id="com{it['n']}">{e(it['primeiro_comentario'])}</pre></section>
  <dl>
    <dt>Base legal {conferir}</dt><dd>{e(it['base_legal'])}</dd>
    <dt>Texto alternativo</dt><dd>{e(it['alt'])}</dd>
    <dt>Foto</dt><dd>{e(it['foto'])}</dd>
  </dl>
</div></article>""")
    indice = "".join(f'<a href="#p{it["n"]}"><b>{it["n"]}</b> {html.escape(it["titulo"])}</a>' for it in itens)
    modelo = (AQUI / "pagina_modelo.html").read_text(encoding="utf-8")
    (OUT / "index.html").write_text(modelo.replace("{{INDICE}}", indice).replace("{{CORPO}}", "".join(cards))
                                    .replace("{{TOTAL}}", str(len(itens))), encoding="utf-8")
    print("ok", len(itens))


if __name__ == "__main__":
    main()
