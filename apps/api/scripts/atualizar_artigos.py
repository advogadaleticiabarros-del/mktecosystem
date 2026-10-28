"""Corrige artigos já publicados no site da Letícia: texto novo (.article-body), H1, título da aba, descrição,
dados estruturados e trocas pontuais de frase.

Lê producao/seo/<data>-*/artigos.json (os arquivos de corpo ficam na mesma pasta). Guarda os originais num
.tgz. Sem --aplicar, só confere e mostra o que mudaria.

Uso na VPS:
  docker compose cp ../../producao/seo/artigos-corrigidos-2026-10-27/. api:/tmp/artigos/
  docker compose cp ../../apps/api/scripts/atualizar_artigos.py api:/tmp/
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/atualizar_artigos.py /tmp/artigos/artigos.json [--aplicar]
  docker compose cp api:/tmp/<backup>.tgz /root/orbit-backups/
"""
import asyncio
import io
import json
import sys
import tarfile
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.integrations.publish.sftp_client import SFTPClient
from app.services.blog_seo import atualizar_corpo_do_artigo, trocar_titulo_e_descricao
from app.services.site_descoberta import avisar_indexnow

SITE = "https://advogadaleticiabarros.com.br/"


def corrigir(html: str, artigo: dict, pasta: Path, data_iso: str) -> str:
    if artigo.get("corpo"):
        corpo = (pasta / artigo["corpo"]).read_text(encoding="utf-8")
        html = atualizar_corpo_do_artigo(html, corpo=corpo, titulo=artigo["titulo_h1"],
                                         descricao=artigo["descricao"], data_iso=data_iso)
    for antigo, novo in artigo.get("trocas", []):
        if antigo not in html:
            raise ValueError(f"{artigo['arquivo']}: trecho não encontrado: {antigo[:70]}")
        html = html.replace(antigo, novo)
    return trocar_titulo_e_descricao(html, titulo=artigo.get("titulo_aba"), descricao=artigo.get("descricao"))


async def main(lista: str, aplicar: bool) -> None:
    pasta = Path(lista).parent
    dados = json.loads(Path(lista).read_text(encoding="utf-8"))
    raiz = f"{settings.BLOG_SFTP_PATH}../"
    sftp = SFTPClient(host=settings.BLOG_SFTP_HOST, port=settings.BLOG_SFTP_PORT,
                      user=settings.BLOG_SFTP_USER, password=settings.BLOG_SFTP_PASSWORD)
    backup = f"/tmp/site-artigos-{datetime.now():%Y%m%d-%H%M}.tgz"
    novos: list[tuple[str, str]] = []
    try:
        with tarfile.open(backup, "w:gz") as tar:
            for artigo in dados["artigos"]:
                original = await sftp.download(raiz + artigo["arquivo"])
                info = tarfile.TarInfo(artigo["arquivo"])
                info.size = len(original)
                tar.addfile(info, io.BytesIO(original))
                novo = corrigir(original.decode("utf-8"), artigo, pasta, dados["data"])
                print(f"{'CORRIGE' if aplicar else 'CORRIGIRIA'} {artigo['arquivo']} ({len(original)} -> {len(novo.encode())} bytes)")
                novos.append((artigo["arquivo"], novo))
        if aplicar:
            for arquivo, novo in novos:
                await sftp.upload(raiz + arquivo, novo.encode("utf-8"))
    finally:
        await sftp.close()
    print(f"BACKUP {backup}")
    if aplicar and novos:
        await avisar_indexnow([SITE + arquivo for arquivo, _ in novos])
        print(f"APLICADO {len(novos)} artigos; IndexNow avisado")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], "--aplicar" in sys.argv[2:]))
