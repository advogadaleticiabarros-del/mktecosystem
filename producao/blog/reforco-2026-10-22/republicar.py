"""Republica 2 artigos reforçados no modelo atual do blog, mesma URL e data original."""
import asyncio, io, json, os, re
from datetime import date
import httpx
from PIL import Image
from sqlalchemy import select
from app.db import SessionLocal
from app.models.tenant import Tenant
from app.services.central_google import _site_padrao
from app.services.chaves_api import obter_chave
from app.services.render_artigo_blog import renderizar_artigo_html, estimar_tempo_leitura
from app.services.blog_seo import aplicar_seo, cards_do_indice, escolher_relacionados, capa_para_jpg
from app.services.site_descoberta import gerar_llms_txt, avisar_bing

ATUALIZADO = '<span class="dot">•</span>\n            <span><i class="fa-solid fa-rotate"></i> Atualizado em 22 de outubro de 2026</span>'

async def main():
    spec = json.load(open("/tmp/spec_reforco.json", encoding="utf-8"))
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs("/tmp/bkp_reforco", exist_ok=True)
    indice = await s.ler("blog/index.html")
    open("/tmp/bkp_reforco/blog__index.html", "w", encoding="utf-8", newline="").write(indice)
    open("/tmp/bkp_reforco/llms.txt", "w", encoding="utf-8", newline="").write(await s.ler("llms.txt") or "")
    urls = []
    for a in spec:
        slug = a["slug"]
        antigo = await s.ler(f"blog/{slug}.html")
        open(f"/tmp/bkp_reforco/blog__{slug}.html", "w", encoding="utf-8", newline="").write(antigo)
        if a["capa_url"]:
            async with httpx.AsyncClient(timeout=60, follow_redirects=True) as c:
                im = Image.open(io.BytesIO((await c.get(a["capa_url"])).content)).convert("RGB")
            r = max(1200 / im.width, 630 / im.height); im = im.resize((round(im.width * r), round(im.height * r)))
            x, y = (im.width - 1200) // 2, int((im.height - 630) * 0.35); im = im.crop((x, y, x + 1200, y + 630))
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
            await sftp.upload(f"{raiz}/blog/capas/{slug}.jpg", capa_para_jpg(buf.getvalue()))
        html = renderizar_artigo_html(titulo=a["h1"], meta_description=a["desc"], categoria=a["cat"], resumo=a["resumo"],
                                      corpo_html=a["html"], slug=slug, data_publicacao=date.fromisoformat(a["data"]))
        relacionados = escolher_relacionados(cards_do_indice(indice), slug=slug, categoria_slug=a["cat_slug"])
        html = aplicar_seo(html, slug=slug, relacionados=relacionados, data_iso="2026-10-22")
        velho = f"<title>{a['h1']} | Dra. Letícia Barros</title>"
        assert html.count(velho) == 1, "title"
        html = html.replace(velho, f"<title>{a['google']} | Dra. Letícia Barros</title>")
        cal = re.search(r'<span><i class="fa-regular fa-calendar"></i>[^<]*</span>', html)
        html = html[:cal.end()] + "\n            " + ATUALIZADO + html[cal.end():]
        await sftp.upload(f"{raiz}/blog/{slug}.html", html.encode("utf-8"))
        # cards do índice (2 grades): título, resumo, tempo e capa
        def novo_card(m):
            card = m.group(0)
            card = re.sub(r"<h3>.*?</h3>", f"<h3>{a['h1']}</h3>", card, count=1, flags=re.S)
            card = re.sub(r"<p>.*?</p>", f"<p>{a['resumo']}</p>", card, count=1, flags=re.S)
            card = re.sub(r'alt="[^"]*"', f'alt="{a["h1"]}"', card, count=1)
            card = re.sub(r'src="[^"]*"', f'src="capas/{slug}.jpg"', card, count=1)
            card = re.sub(r"\d+ min de leitura", f"{estimar_tempo_leitura(a['html'])} min de leitura", card, count=1)
            return card
        indice, n = re.subn(r'<a class="blog-card"[^>]*href="' + re.escape(slug) + r'\.html".*?</a>', novo_card, indice, flags=re.S)
        print(slug, "publicado; cards atualizados:", n)
        urls.append(f"https://advogadaleticiabarros.com.br/blog/{slug}.html")
    await sftp.upload(f"{raiz}/blog/index.html", indice.encode("utf-8"))
    await sftp.upload(f"{raiz}/llms.txt", gerar_llms_txt(indice).encode("utf-8"))
    await sftp.close()
    async with SessionLocal() as db:
        t = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one()
        chave = await obter_chave(db, t.id, "bing")
    print("bing:", await avisar_bing(chave, urls + ["https://advogadaleticiabarros.com.br/blog/"]))

asyncio.run(main())
