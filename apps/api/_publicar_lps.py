import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

BASE = "domains/advogadaleticiabarros.com.br/public_html/lp-v3/"
LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3")
SLUGS = ["assessoria-empresarial", "bpc-loas-criancas", "gestante-clt", "insalubridade-clt", "pensao-alimenticia"]


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for slug in SLUGS:
        conteudo = (LOCAL / f"{slug}.html").read_bytes()
        await sftp.upload(f"{BASE}{slug}.html", conteudo)
        print(f"{slug}: publicado")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
