import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\assets\images\lp\lp-bpc.jpg")


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    await sftp.upload(
        "domains/advogadaleticiabarros.com.br/public_html/assets/images/lp/lp-bpc.jpg",
        LOCAL.read_bytes(),
    )
    print("lp-bpc.jpg: publicado")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
