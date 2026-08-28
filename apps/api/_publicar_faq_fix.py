import os
import asyncio
from pathlib import Path

from app.integrations.publish.sftp_client import SFTPClient

LOCAL = Path(r"C:\Users\prosy\blogautomaticoleticia\lp-v3")
BASE = "domains/advogadaleticiabarros.com.br/public_html/"

# slug -> lista de pastas onde essa página também foi publicada
DESTINOS = {
    "bpc-loas-criancas": ["lp-v3", "lp"],
    "gestante-clt": ["lp-v3", "lp"],
    "insalubridade-clt": ["lp-v3", "lp"],
    "pensao-alimenticia": ["lp-v3", "lp", "areas/direito-familia"],
}


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for slug, pastas in DESTINOS.items():
        conteudo = (LOCAL / f"{slug}.html").read_bytes()
        for pasta in pastas:
            if pasta == "areas/direito-familia":
                dest = f"{BASE}areas/direito-familia.html"
            else:
                dest = f"{BASE}{pasta}/{slug}.html"
            await sftp.upload(dest, conteudo)
            print(f"{slug} -> {dest}")
    # BPC/LOAS também alimenta areas/direito-previdenciario.html
    conteudo_bpc = (LOCAL / "bpc-loas-criancas.html").read_bytes()
    await sftp.upload(f"{BASE}areas/direito-previdenciario.html", conteudo_bpc)
    print("bpc-loas-criancas -> areas/direito-previdenciario.html")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
