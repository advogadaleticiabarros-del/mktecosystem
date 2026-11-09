"""SEO da calculadora do 13º (09/11/2026). Roda dentro do container da API, com os arquivos em /tmp/calc13/.
Publica a LP com schema e og:image, a imagem de compartilhamento, um link no artigo do 13º da gestante, a entrada no
sitemap e avisa IndexNow/Bing. Guarda o que existia em /tmp/bkp_calc13_seo/ antes de trocar."""
import asyncio, os
from datetime import date
from sqlalchemy import select
from app.db import SessionLocal
from app.models.tenant import Tenant
from app.services.central_google import _site_padrao
from app.services.chaves_api import obter_chave
from app.services.blog_index_editor import inserir_sitemap_entry
from app.services.site_descoberta import avisar_bing, avisar_indexnow

SITE = "https://advogadaleticiabarros.com.br"
URL = f"{SITE}/lp/calculadora-13-salario.html"
ARTIGO = "blog/13-salario-gestante-licenca-maternidade.html"
MARCA = "<p>Se a empresa insistir que a licença reduz o 13º"
LINK = ('<p>Para ter um valor de referência antes de falar com o RH, use a '
        '<a href="/lp/calculadora-13-salario.html?utm_source=blog&amp;utm_medium=artigo&amp;utm_campaign=calculadora-13-2026">'
        'calculadora do 13º salário 2026</a>. A licença-maternidade não conta como falta nem como afastamento: '
        'deixe esses campos em branco.</p>\n\n')
BKP = "/tmp/bkp_calc13_seo"


async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs(BKP, exist_ok=True)
    lp = await s.ler("lp/calculadora-13-salario.html")
    artigo = await s.ler(ARTIGO)
    sitemap = await s.ler("sitemap.xml")
    for nome, txt in [("lp.html", lp), ("artigo.html", artigo), ("sitemap.xml", sitemap)]:
        open(f"{BKP}/{nome}", "w", encoding="utf-8", newline="").write(txt or "")

    await sftp.upload(f"{raiz}/lp/calculadora-13-salario.html", open("/tmp/calc13/lp/calculadora-13-salario.html", "rb").read())
    await sftp.garantir_diretorio(f"{raiz}/assets/images/lp")
    await sftp.upload(f"{raiz}/assets/images/lp/og-calculadora-13-1200x630.jpg", open("/tmp/calc13/og-calculadora-13-1200x630.jpg", "rb").read())
    print("lp e imagem publicadas")

    if "calculadora-13-salario" in artigo:
        print("artigo já tem o link")
    else:
        assert artigo.count(MARCA) == 1, "ponto de inserção não encontrado no artigo"
        await sftp.upload(f"{raiz}/{ARTIGO}", artigo.replace(MARCA, LINK + MARCA).encode("utf-8"))
        print("link inserido no artigo")

    if URL in sitemap:
        print("sitemap já tem a LP")
    else:
        await sftp.upload(f"{raiz}/sitemap.xml", inserir_sitemap_entry(sitemap, url=URL, data_iso=date(2026, 11, 9).isoformat()).encode("utf-8"))
        print("sitemap atualizado")
    await sftp.close()

    urls = [URL, f"{SITE}/{ARTIGO}"]
    print("indexnow:", await avisar_indexnow(urls))
    async with SessionLocal() as db:
        t = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one()
        chave = await obter_chave(db, t.id, "bing")
    if chave:
        print("bing:", await avisar_bing(chave, urls))

asyncio.run(main())
