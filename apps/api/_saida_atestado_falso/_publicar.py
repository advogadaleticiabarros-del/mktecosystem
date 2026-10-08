"""Publica o artigo do atestado falso no blog (SFTP), no mesmo fluxo do
`blog_publisher._publicar_artigo`: página + capa + card no index + sitemap.

Uso (de apps/api): BLOG_SFTP_HOST=... BLOG_SFTP_PORT=... BLOG_SFTP_USER=...
BLOG_SFTP_PASSWORD=... python _saida_atestado_falso/_publicar.py
"""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.integrations.publish.sftp_client import SFTPClient  # noqa: E402
from app.services.blog_index_editor import inserir_card, inserir_sitemap_entry  # noqa: E402
from app.services.render_artigo_blog import estimar_tempo_leitura  # noqa: E402

D = Path(__file__).resolve().parent
BASE = "domains/advogadaleticiabarros.com.br/public_html/blog/"
SLUG = "atestado-medico-falso-justa-causa"
TITULO = "Atestado médico falso no trabalho: justa causa, crime e o que muda para quem é honesto"
RESUMO = (
    "Atestado falso dá justa causa e pode virar crime. Mas quem entrega atestado verdadeiro tem "
    "direitos, e a empresa não pode desconfiar sem prova. Veja como se proteger."
)
DATA_ISO = "2026-10-08"


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    index_atual = (await sftp.download(f"{BASE}index.html")).decode("utf-8")
    sitemap_atual = (await sftp.download(f"{BASE}../sitemap.xml")).decode("utf-8")
    (D / "index_atual.html").write_text(index_atual, encoding="utf-8")
    (D / "sitemap_atual.xml").write_text(sitemap_atual, encoding="utf-8")

    index_novo = inserir_card(
        index_atual,
        url=f"{SLUG}.html",
        imagem=f"capas/{SLUG}.png",
        categoria="Direito Trabalhista",
        categoria_slug="direito-trabalhista",
        titulo=TITULO,
        resumo=RESUMO,
        tempo_leitura=estimar_tempo_leitura((D / "corpo.html").read_text(encoding="utf-8")),
    )
    sitemap_novo = inserir_sitemap_entry(
        sitemap_atual, url=f"https://advogadaleticiabarros.com.br/blog/{SLUG}.html", data_iso=DATA_ISO
    )
    (D / "index_novo.html").write_text(index_novo, encoding="utf-8")
    (D / "sitemap_novo.xml").write_text(sitemap_novo, encoding="utf-8")

    await sftp.upload(f"{BASE}{SLUG}.html", (D / "artigo.html").read_bytes())
    await sftp.garantir_diretorio(f"{BASE}capas")
    await sftp.upload(f"{BASE}capas/{SLUG}.png", (D / "capa.png").read_bytes())
    await sftp.upload(f"{BASE}index.html", index_novo.encode("utf-8"))
    await sftp.upload(f"{BASE}../sitemap.xml", sitemap_novo.encode("utf-8"))
    await sftp.close()
    print(f"publicado: https://advogadaleticiabarros.com.br/blog/{SLUG}.html")


if __name__ == "__main__":
    asyncio.run(main())
