"""Publica o artigo da campanha de assédio eleitoral (27/10/2026) no mesmo fluxo do blog_publisher."""
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

SLUG = "demitido-por-causa-do-voto-o-que-a-lei-garante"
TITULO = "Demitido por causa do voto? O que a lei garante e como juntar as provas"
DESC = ("Demissão por causa do voto é dispensa discriminatória. Veja o que a lei garante (reintegração ou o dobro, "
        "além de dano moral), quais provas servem e como denunciar no MPT.")
RESUMO = ("Demitir por causa do voto é dispensa discriminatória. A lei garante reintegração ou o dobro da remuneração, "
          "além de dano moral. Veja como juntar as provas.")
CAT, CAT_SLUG = "Trabalhista", "trabalhista"
HOJE = date(2026, 10, 27)
URL = f"https://advogadaleticiabarros.com.br/blog/{SLUG}.html"
LP = "https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html"
CTA_LP = (f'{LP}?utm_source=blog&amp;utm_medium=artigo&amp;utm_campaign=assedio-eleitoral-2026&amp;utm_content=cta-final#form')

async def main():
    corpo = open("/tmp/artigo-voto.html", encoding="utf-8").read()
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs("/tmp/bkp_artigo_voto", exist_ok=True)
    indice = await s.ler("blog/index.html")
    sitemap = await s.ler("sitemap.xml")
    for nome, txt in [("blog__index.html", indice), ("sitemap.xml", sitemap), ("llms.txt", await s.ler("llms.txt") or ""),
                      (f"blog__{SLUG}.html", await s.ler(f"blog/{SLUG}.html") or "")]:
        open(f"/tmp/bkp_artigo_voto/{nome}", "w", encoding="utf-8", newline="").write(txt)
    html = renderizar_artigo_html(titulo=TITULO, meta_description=DESC, categoria=CAT, resumo=RESUMO,
                                  corpo_html=corpo, slug=SLUG, data_publicacao=HOJE)
    rel = escolher_relacionados(cards_do_indice(indice), slug=SLUG, categoria_slug=CAT_SLUG)
    html = aplicar_seo(html, slug=SLUG, relacionados=rel, data_iso=HOJE.isoformat())
    # CTA final do modelo aponta para a LP da campanha (formulário), não para a página de contato genérica.
    antigo = '<a href="../contato.html" class="btn-primary"><i class="fa-solid fa-arrow-right"></i> Busque orientação jurídica</a>'
    assert html.count(antigo) == 1, "cta"
    html = html.replace(antigo, f'<a href="{CTA_LP}" class="btn-primary"><i class="fa-solid fa-arrow-right"></i> Busque orientação jurídica</a>')
    await sftp.upload(f"{raiz}/blog/{SLUG}.html", html.encode("utf-8"))
    await sftp.garantir_diretorio(f"{raiz}/blog/capas")
    await sftp.upload(f"{raiz}/blog/capas/{SLUG}.jpg", capa_para_jpg(open("/tmp/capa-blog.jpg", "rb").read()))
    indice_novo = inserir_card(indice, url=f"{SLUG}.html", imagem=f"capas/{SLUG}.jpg", categoria=CAT, categoria_slug=CAT_SLUG,
                               titulo=TITULO, resumo=RESUMO, tempo_leitura=estimar_tempo_leitura(corpo))
    await sftp.upload(f"{raiz}/blog/index.html", indice_novo.encode("utf-8"))
    sm = inserir_sitemap_entry(sitemap, url=URL, data_iso=HOJE.isoformat())
    sm = inserir_sitemap_entry(sm, url=LP, data_iso=HOJE.isoformat())
    await sftp.upload(f"{raiz}/sitemap.xml", sm.encode("utf-8"))
    await sftp.upload(f"{raiz}/llms.txt", gerar_llms_txt(indice_novo).encode("utf-8"))
    await sftp.close()
    print("publicado", URL, "relacionados:", [r["titulo"][:40] for r in rel])
    print("indexnow:", await avisar_indexnow([URL, LP, "https://advogadaleticiabarros.com.br/blog/"]))
    async with SessionLocal() as db:
        t = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one()
        chave = await obter_chave(db, t.id, "bing")
    if chave:
        print("bing:", await avisar_bing(chave, [URL, LP, "https://advogadaleticiabarros.com.br/blog/"]))

asyncio.run(main())
