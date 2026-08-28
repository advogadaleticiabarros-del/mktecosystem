import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\tmp\escritorio.html")
DEST = "domains/advogadaleticiabarros.com.br/public_html/escritorio.html"


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    await sftp.upload(DEST, LOCAL.read_bytes())
    print("escritorio.html: publicado")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
