import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3\direito-trabalhista.html")
IMG_LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\assets\images\mulher-demitida-removebg.png")


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    await sftp.upload(
        "domains/advogadaleticiabarros.com.br/public_html/areas/direito-trabalhista.html",
        LOCAL.read_bytes(),
    )
    print("direito-trabalhista.html: publicado em areas/")
    await sftp.upload(
        "domains/advogadaleticiabarros.com.br/public_html/assets/images/mulher-demitida-removebg.png",
        IMG_LOCAL.read_bytes(),
    )
    print("mulher-demitida-removebg.png: publicado")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
