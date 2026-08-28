import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia")
BASE = "domains/advogadaleticiabarros.com.br/public_html/"


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    img = (LOCAL / "assets/images/lp/lp-assessoria-juridica.jpg").read_bytes()
    await sftp.upload(f"{BASE}assets/images/lp/lp-assessoria-juridica.jpg", img)
    print("lp-assessoria-juridica.jpg: publicado")

    html = (LOCAL / "lp-v3/assessoria-juridica.html").read_bytes()
    await sftp.upload(f"{BASE}lp-v3/assessoria-juridica.html", html)
    await sftp.upload(f"{BASE}areas/assessoria-juridica.html", html)
    print("assessoria-juridica.html: publicado (lp-v3 + areas)")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
