"""Revisão pontual de páginas já publicadas no site da Letícia (texto, CTA, CSS, script), por trocas exatas.

Lê producao/seo/<data>-trocas-site.json: {"paginas": [{"caminho": "blog/x.html", "trocas": [{"de", "para", "todas"?}]}]}.
Tudo ou nada: baixa todas as páginas e aplica as trocas na memória (blog_seo.aplicar_trocas); se uma falhar,
nada é enviado. Antes de enviar, guarda o original de cada página num .tgz. Sem --aplicar, só simula.

Uso na VPS:
  docker compose cp <json> api:/tmp/trocas.json
  docker compose cp scripts/aplicar_trocas_site.py api:/tmp/
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/aplicar_trocas_site.py /tmp/trocas.json [--aplicar]
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
from app.services.blog_seo import TrocaInvalida, aplicar_trocas
from app.services.site_descoberta import avisar_indexnow

SITE = "https://advogadaleticiabarros.com.br/"


def arquivo_da_pagina(caminho: str) -> str:
    return caminho + "index.html" if caminho == "" or caminho.endswith("/") else caminho


async def main(lista: str, aplicar: bool) -> None:
    paginas = json.load(open(lista, encoding="utf-8"))["paginas"]
    raiz = f"{settings.BLOG_SFTP_PATH}../"
    sftp = SFTPClient(host=settings.BLOG_SFTP_HOST, port=settings.BLOG_SFTP_PORT,
                      user=settings.BLOG_SFTP_USER, password=settings.BLOG_SFTP_PASSWORD)
    backup = f"/tmp/site-trocas-{datetime.now():%Y%m%d-%H%M}.tgz"
    prontas: list[tuple[str, str, bytes, str]] = []
    erros = 0
    try:
        for p in paginas:
            arquivo = arquivo_da_pagina(p["caminho"])
            original = await sftp.download(raiz + arquivo)
            try:
                depois = aplicar_trocas(original.decode("utf-8"), p["trocas"])
            except TrocaInvalida as erro:
                print(f"ERRO   {arquivo}: {erro}")
                erros += 1
                continue
            mudou = depois != original.decode("utf-8")
            print(f"{'MUDA ' if mudou else 'IGUAL'}  {arquivo} ({len(p['trocas'])} trocas)")
            if mudou:
                prontas.append((p["caminho"], arquivo, original, depois))
        if erros:
            print(f"NADA ENVIADO: {erros} página(s) com erro")
            return
        if not aplicar:
            print(f"SIMULAÇÃO: {len(prontas)} página(s) mudariam")
            return
        with tarfile.open(backup, "w:gz") as tar:
            for _, arquivo, original, _ in prontas:
                info = tarfile.TarInfo(arquivo)
                info.size = len(original)
                tar.addfile(info, io.BytesIO(original))
        print(f"BACKUP {backup}")
        for _, arquivo, _, depois in prontas:
            await sftp.upload(raiz + arquivo, depois.encode("utf-8"))
    finally:
        await sftp.close()
    if aplicar and prontas:
        await avisar_indexnow([SITE + caminho for caminho, *_ in prontas])
        print(f"APLICADO {len(prontas)} páginas; IndexNow avisado")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], "--aplicar" in sys.argv[2:]))
