"""Publica uma versão nova do /js/conversoes.js do site da Letícia e troca a versão (?v=) em todas as páginas.

A hospedagem guarda o .js por 30 dias, então sem trocar o ?v= as páginas continuam com o antigo. Guarda o .js
antigo e as páginas alteradas num .tgz. Sem --aplicar, só mostra o que mudaria.

Uso na VPS:
  docker compose cp ../../producao/site/conversoes.js api:/tmp/conversoes.js
  docker compose cp ../../apps/api/scripts/publicar_conversoes.py api:/tmp/
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/publicar_conversoes.py /tmp/conversoes.js 20261027 [--aplicar]
  docker compose cp api:/tmp/<backup>.tgz /root/orbit-backups/
"""
import asyncio
import io
import re
import sys
import tarfile
from datetime import datetime

from app.config import settings
from app.integrations.publish.sftp_client import SFTPClient

TAG = re.compile(r"conversoes\.js\?v=[\w.-]+")


async def main(arquivo_js: str, versao: str, aplicar: bool) -> None:
    raiz = f"{settings.BLOG_SFTP_PATH}../"
    sftp = SFTPClient(host=settings.BLOG_SFTP_HOST, port=settings.BLOG_SFTP_PORT,
                      user=settings.BLOG_SFTP_USER, password=settings.BLOG_SFTP_PASSWORD)
    backup = f"/tmp/site-conversoes-{datetime.now():%Y%m%d-%H%M}.tgz"
    novo_js = open(arquivo_js, "rb").read()
    trocas: list[tuple[str, bytes]] = []
    try:
        with tarfile.open(backup, "w:gz") as tar:
            def guardar(nome: str, conteudo: bytes) -> None:
                info = tarfile.TarInfo(nome)
                info.size = len(conteudo)
                tar.addfile(info, io.BytesIO(conteudo))

            guardar("js/conversoes.js", await sftp.download(raiz + "js/conversoes.js"))
            for pagina in await sftp.listar_recursivo(raiz, ".html", profundidade=2):
                original = await sftp.download(raiz + pagina)
                texto = original.decode("utf-8", errors="surrogateescape")
                novo = TAG.sub(f"conversoes.js?v={versao}", texto)
                if novo != texto:
                    guardar(pagina, original)
                    trocas.append((pagina, novo.encode("utf-8", errors="surrogateescape")))
        print(f"{'TROCA' if aplicar else 'TROCARIA'} js/conversoes.js e o ?v= em {len(trocas)} páginas")
        if aplicar:
            await sftp.upload(raiz + "js/conversoes.js", novo_js)
            for pagina, conteudo in trocas:
                await sftp.upload(raiz + pagina, conteudo)
    finally:
        await sftp.close()
    print(f"BACKUP {backup}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2], "--aplicar" in sys.argv[3:]))
