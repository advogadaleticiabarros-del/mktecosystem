"""Avisa o Google da calculadora do 13º (09/11/2026) pela conta conectada no Orbit (escopo webmasters):
reenvia o sitemap no Search Console e consulta a URL na Inspeção de URL. Roda dentro do container da API.
O botão "Solicitar indexação" não existe na API; o reenvio do sitemap é o caminho oficial por programa."""
import asyncio
from urllib.parse import quote
from sqlalchemy import select
from app.db import SessionLocal
from app.models.tenant import Tenant
from app.services.central_google import abrir
from app.services.presenca_google import GSC_URL, _site_search_console

SITEMAP = "https://advogadaleticiabarros.com.br/sitemap.xml"
URLS = ["https://advogadaleticiabarros.com.br/lp/calculadora-13-salario.html",
        "https://advogadaleticiabarros.com.br/blog/13-salario-gestante-licenca-maternidade.html"]
INSPECAO = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"


async def main():
    async with SessionLocal() as db:
        t = (await db.execute(select(Tenant).where(Tenant.slug == "leticia-barros"))).scalar_one()
        api, _ = await abrir(db, t.id)
    site = await _site_search_console(api, "advogadaleticiabarros.com.br")
    print("propriedade:", site)
    base = f"{GSC_URL}/sites/{quote(site, safe='')}/sitemaps"
    await api.chamar("PUT", f"{base}/{quote(SITEMAP, safe='')}")
    info = await api.get(f"{base}/{quote(SITEMAP, safe='')}")
    print("sitemap reenviado:", info.get("lastSubmitted"), "| última leitura:", info.get("lastDownloaded"),
          "| pendente:", info.get("isPending"))
    for url in URLS:
        r = (await api.chamar("POST", INSPECAO, json={"inspectionUrl": url, "siteUrl": site, "languageCode": "pt-BR"}))
        idx = r.get("inspectionResult", {}).get("indexStatusResult", {})
        print(url.rsplit("/", 1)[-1], "->", idx.get("verdict"), "|", idx.get("coverageState"),
              "| último rastreio:", idx.get("lastCrawlTime"))

asyncio.run(main())
