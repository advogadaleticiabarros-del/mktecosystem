import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3")
BASE = "domains/advogadaleticiabarros.com.br/public_html/"
SLUGS = ["direito-consumidor", "direito-civil", "assessoria-juridica", "extrajudiciais"]


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for slug in SLUGS:
        conteudo = (LOCAL / f"{slug}.html").read_bytes()
        await sftp.upload(f"{BASE}lp-v3/{slug}.html", conteudo)
        await sftp.upload(f"{BASE}areas/{slug}.html", conteudo)
        print(f"{slug}: publicado (lp-v3 + areas)")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
