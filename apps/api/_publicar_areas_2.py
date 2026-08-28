import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3")
BASE = "domains/advogadaleticiabarros.com.br/public_html/areas/"

MAPA = {
    "direito-previdenciario.html": "bpc-loas-criancas.html",
    "direito-familia.html": "pensao-alimenticia.html",
}


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for dest, origem in MAPA.items():
        conteudo = (LOCAL / origem).read_bytes()
        await sftp.upload(f"{BASE}{dest}", conteudo)
        print(f"{dest}: publicado (conteúdo de {origem})")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
