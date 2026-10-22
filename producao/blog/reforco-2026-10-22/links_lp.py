"""Quadro "Para ir além" com a LP do assunto no fim de cada artigo do blog. Uso: python links_lp.py [aplicar]"""
import asyncio, os, re, sys
from app.services.central_google import _site_padrao

LPS = {
    "gestante": [("../lp/gestante-clt.html", "Direitos da gestante CLT"),
                 ("../lp/guia-direitos-gestante-trabalhadora.html", "Guia completo dos direitos da gestante trabalhadora")],
    "insalubridade": [("../lp/insalubridade-clt.html", "Adicional de insalubridade: quem tem direito")],
    "pensao": [("../lp/pensao-alimenticia.html", "Pensão alimentícia: como pedir, cobrar e revisar")],
    "bpc": [("../lp/bpc-loas-criancas.html", "BPC/LOAS para crianças com necessidades especiais")],
}
REGRAS = [
    (r"gestante|gravid|maternidade|aborto|fui-demitida", "gestante"),
    (r"insalubridade|limpar-banheiro|saude-no-trabalho", "insalubridade"),
    (r"pensao|alimenticia|alimentos", "pensao"),
    (r"bpc|loas", "bpc"),
]
FIM = re.compile(r"</div>\s*</section>\s*</article>")
FIM_ALTERNATIVO = re.compile(r'<div class="article-cta">')
ANTIGO_BPC = "bpc-para-crianca-com-deficiencia-o-beneficio-de-r-1-621-que-muita-mae-nao-conhece.html"
NOVO_BPC = "https://advogadaleticiabarros.com.br/blog/bpc-para-crianca-com-necessidades-especiais-o-beneficio-de-r-1-621-que-muita-mae-nao-conhece.html"
CTA_ERRADO = re.compile(r'<a href="https://wa\.me/5527997789948[^"]*" class="btn-cta">[^<]*</a>')
CTA_PADRAO = '<a href="../contato.html" class="btn-cta">Busque orientação jurídica</a>'


def bloco(links, nl):
    itens = " e ".join(f'<a href="{u}">{t}</a>' for u, t in links)
    return (f'<div class="callout-box">{nl}    <h4><i class="fa-solid fa-book-open"></i> Para ir além</h4>{nl}'
            f'    <p>Se o tema deste artigo é a sua situação, veja também: {itens}.</p>{nl}</div>{nl}{nl}')


async def main(aplicar):
    s = _site_padrao()
    arqs = [a for a in await s._sftp.listar_recursivo(s._raiz + "/blog", ".html", profundidade=0)
            if a not in ("index.html", "jornal.html", ANTIGO_BPC) and not a.startswith("_")]
    os.makedirs("/tmp/bkp_links", exist_ok=True)
    feitos = []
    for a in sorted(arqs):
        temas = [t for padrao, t in REGRAS if re.search(padrao, a)]
        if not temas:
            continue
        h = await s.ler("blog/" + a) or ""
        if re.search(r'http-equiv=["\']refresh', h, re.I) or "Para ir além" in h:
            continue
        links = [l for t in temas for l in LPS[t] if l[0].split("/")[-1] not in h]
        if not links:
            continue
        m = list(FIM.finditer(h)) or list(FIM_ALTERNATIVO.finditer(h))
        if len(m) != 1:
            print("SEM PONTO DE INSERÇÃO:", a, len(m)); continue
        nl = "\r\n" if "\r\n" in h else "\n"
        novo = h[:m[0].start()] + bloco(links, nl) + h[m[0].start():]
        novo = CTA_ERRADO.sub(CTA_PADRAO, novo)
        feitos.append((a, [t for _, t in links]))
        if aplicar:
            open("/tmp/bkp_links/" + a, "w", encoding="utf-8", newline="").write(h)
            await s._sftp.upload(f"{s._raiz}/blog/{a}", novo.encode("utf-8"))
    # Versão antiga do BPC (URL com palavra que não usamos): aponta o Google para a versão nova.
    h = await s.ler("blog/" + ANTIGO_BPC) or ""
    canon = re.search(r'<link rel="canonical" href="[^"]*">', h)
    if canon and NOVO_BPC not in canon.group(0):
        feitos.append((ANTIGO_BPC, ["canonical -> versão nova"]))
        if aplicar:
            open("/tmp/bkp_links/" + ANTIGO_BPC, "w", encoding="utf-8", newline="").write(h)
            novo = h.replace(canon.group(0), f'<link rel="canonical" href="{NOVO_BPC}">')
            await s._sftp.upload(f"{s._raiz}/blog/{ANTIGO_BPC}", novo.encode("utf-8"))
    for a, ls in feitos:
        print(("GRAVADO " if aplicar else "faria ") + a, "->", "; ".join(ls))
    print(len(feitos), "artigos")
    await s._sftp.close()

asyncio.run(main(len(sys.argv) > 1 and sys.argv[1] == "aplicar"))
