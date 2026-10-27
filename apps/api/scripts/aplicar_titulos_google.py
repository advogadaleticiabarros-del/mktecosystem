"""Troca o <title> e a meta description das páginas do site da Letícia (o que aparece no Google).

Lê a lista de producao/seo/<data>-titulos-google.json. Antes de mudar, guarda o original de cada
página num .tgz. Sem --aplicar, só mostra o que mudaria.

Uso na VPS:
  docker compose cp <json> api:/tmp/titulos.json
  docker compose cp scripts/aplicar_titulos_google.py api:/tmp/
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/aplicar_titulos_google.py /tmp/titulos.json [--aplicar]
  docker compose cp api:/tmp/<backup>.tgz /root/orbit-backups/
"""
import asyncio
import io
import json
import sys
import tarfile
from datetime import datetime

from app.config import settings
from app.integrations.publish.sftp_client import SFTPClient
from app.services.blog_seo import trocar_titulo_e_descricao
from app.services.site_descoberta import avisar_indexnow

SITE = "https://advogadaleticiabarros.com.br/"


def arquivo_da_pagina(caminho: str) -> str:
    return caminho + "index.html" if caminho == "" or caminho.endswith("/") else caminho


async def main(lista: str, aplicar: bool) -> None:
    paginas = json.load(open(lista, encoding="utf-8"))["paginas"]
    raiz = f"{settings.BLOG_SFTP_PATH}../"
    sftp = SFTPClient(host=settings.BLOG_SFTP_HOST, port=settings.BLOG_SFTP_PORT,
                      user=settings.BLOG_SFTP_USER, password=settings.BLOG_SFTP_PASSWORD)
    backup = f"/tmp/site-titulos-{datetime.now():%Y%m%d-%H%M}.tgz"
    mudadas: list[str] = []
    try:
        with tarfile.open(backup, "w:gz") as tar:
            for p in paginas:
                arquivo = arquivo_da_pagina(p["caminho"])
                original = await sftp.download(raiz + arquivo)
                info = tarfile.TarInfo(arquivo)
                info.size = len(original)
                tar.addfile(info, io.BytesIO(original))
                antes = original.decode("utf-8")
                depois = trocar_titulo_e_descricao(antes, titulo=p["titulo"], descricao=p["descricao"])
                if depois == antes:
                    print(f"IGUAL  {arquivo}")
                    continue
                print(f"{'TROCA ' if aplicar else 'TROCARIA'} {arquivo}\n  T: {p['titulo']}\n  D: {p['descricao']}")
                if aplicar:
                    await sftp.upload(raiz + arquivo, depois.encode("utf-8"))
                    mudadas.append(SITE + p["caminho"])
    finally:
        await sftp.close()
    print(f"BACKUP {backup}")
    if mudadas:
        await avisar_indexnow(mudadas)
        print(f"APLICADO {len(mudadas)} páginas; IndexNow avisado")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], "--aplicar" in sys.argv[2:]))
