import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3\pensao-alimenticia.html")
DEST = "domains/advogadaleticiabarros.com.br/public_html/lp/pensao-alimenticia.html"


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    await sftp.upload(DEST, LOCAL.read_bytes())
    print("lp/pensao-alimenticia.html: publicado (conteúdo novo)")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
