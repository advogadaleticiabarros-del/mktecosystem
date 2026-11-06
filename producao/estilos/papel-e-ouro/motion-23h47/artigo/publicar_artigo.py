"""Publica o artigo do WhatsApp fora do horário (06/11/2026) no mesmo fluxo do blog_publisher.
Precisa de /tmp/artigo-23h47.html (corpo) e /tmp/capa-23h47.jpg (quadro do Reels 23:47)."""
import asyncio, os
from datetime import date
from sqlalchemy import select
from app.db import SessionLocal
from app.models.tenant import Tenant
from app.services.central_google import _site_padrao
from app.services.chaves_api import obter_chave
from app.services.render_artigo_blog import renderizar_artigo_html, estimar_tempo_leitura
from app.services.blog_seo import aplicar_seo, cards_do_indice, escolher_relacionados, capa_para_jpg
from app.services.blog_index_editor import inserir_card, inserir_sitemap_entry
from app.services.site_descoberta import gerar_llms_txt, avisar_bing, avisar_indexnow

SLUG = "chefe-manda-mensagem-no-whatsapp-fora-do-horario-preciso-responder"
TITULO = "Chefe mandou mensagem no WhatsApp fora do horário: preciso responder? Conta como hora extra?"
DESC = ("Mensagem do chefe às 23h é obrigação de responder? Veja o que diz a CLT, quando vira hora extra ou "
        "sobreaviso e como guardar a prova.")
RESUMO = ("Fora da jornada você não é obrigada a responder. Veja quando a mensagem do chefe vira hora extra ou "
          "sobreaviso, se pode dar justa causa e como provar.")
CAT, CAT_SLUG = "Trabalhista", "trabalhista"
HOJE = date(2026, 11, 6)
URL = f"https://advogadaleticiabarros.com.br/blog/{SLUG}.html"

async def main():
    corpo = open("/tmp/artigo-23h47.html", encoding="utf-8").read()
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs("/tmp/bkp_artigo_23h47", exist_ok=True)
    indice = await s.ler("blog/index.html")
    sitemap = await s.ler("sitemap.xml")
    existente = await s.ler(f"blog/{SLUG}.html") or ""
    assert not existente, "artigo já existe no site; não sobrescrever"
    for nome, txt in [("blog__index.html", indice), ("sitemap.xml", sitemap), ("llms.txt", await s.ler("llms.txt") or "")]:
        open(f"/tmp/bkp_artigo_23h47/{nome}", "w", encoding="utf-8", newline="").write(txt)
    html = renderizar_artigo_html(titulo=TITULO, meta_description=DESC, categoria=CAT, resumo=RESUMO,
                                  corpo_html=corpo, slug=SLUG, data_publicacao=HOJE)
    rel = escolher_relacionados(cards_do_indice(indice), slug=SLUG, categoria_slug=CAT_SLUG)
    html = aplicar_seo(html, slug=SLUG, relacionados=rel, data_iso=HOJE.isoformat())
    await sftp.upload(f"{raiz}/blog/{SLUG}.html", html.encode("utf-8"))
    await sftp.garantir_diretorio(f"{raiz}/blog/capas")
    await sftp.upload(f"{raiz}/blog/capas/{SLUG}.jpg", capa_para_jpg(open("/tmp/capa-23h47.jpg", "rb").read()))
    indice_novo = inserir_card(indice, url=f"{SLUG}.html", imagem=f"capas/{SLUG}.jpg", categoria=CAT, categoria_slug=CAT_SLUG,
                               titulo=TITULO, resumo=RESUMO, tempo_leitura=estimar_tempo_leitura(corpo))
    await sftp.upload(f"{raiz}/blog/index.html", indice_novo.encode("utf-8"))
    sm = inserir_sitemap_entry(sitemap, url=URL, data_iso=HOJE.isoformat())
    await sftp.upload(f"{raiz}/sitemap.xml", sm.encode("utf-8"))
    await sftp.upload(f"{raiz}/llms.txt", gerar_llms_txt(indice_novo).encode("utf-8"))
    await sftp.close()
    print("publicado", URL, "relacionados:", [r["titulo"][:40] for r in rel])
    print("indexnow:", await avisar_indexnow([URL, "https://advogadaleticiabarros.com.br/blog/"]))
    async with SessionLocal() as db:
        t = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one()
        chave = await obter_chave(db, t.id, "bing")
    if chave:
        print("bing:", await avisar_bing(chave, [URL, "https://advogadaleticiabarros.com.br/blog/"]))

asyncio.run(main())
