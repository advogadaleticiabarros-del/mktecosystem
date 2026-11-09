"""Publica o link na bio (09/11/2026) em /bio/. Roda no container da API, com os arquivos em /tmp/bio/."""
import asyncio
from app.services.central_google import _site_padrao
ARQUIVOS = ["bio/index.html", "bio/leticia-bio.webp"]
async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    await sftp.garantir_diretorio(f"{raiz}/bio")
    for arq in ARQUIVOS:
        await sftp.upload(f"{raiz}/{arq}", open(f"/tmp/bio/{arq}", "rb").read()); print("publicado", arq)
    await sftp.close()
asyncio.run(main())
