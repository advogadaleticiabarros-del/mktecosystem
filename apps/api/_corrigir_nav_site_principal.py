import os
import asyncio
import re

from app.integrations.publish.sftp_client import SFTPClient

BASE = "domains/advogadaleticiabarros.com.br/public_html/"

PAGES = ["index.html", "faq.html", "contato.html", "blog/index.html"]

PATTERNS = [
    (re.compile(r'(<li><a href="[^"]*contato\.html">Contato</a></li>\s*)'
                r'<li><a href="([^"]*contato\.html)" class="nav-cta">Fale Comigo</a></li>'),
     lambda m: f'{m.group(1)}<li><a href="{m.group(2)}" class="nav-cta">Contato</a></li>'),
    (re.compile(r'<li><a href="([^"]*contato\.html)" class="active">Contato</a></li>\s*'
                r'<li><a href="[^"]*contato\.html" class="nav-cta">Fale Comigo</a></li>'),
     lambda m: f'<li><a href="{m.group(1)}" class="active nav-cta">Contato</a></li>'),
    (re.compile(r'<li><a class="nav-cta" href="([^"]*contato\.html)">Fale Comigo</a></li>'),
     lambda m: ""),
]


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for page in PAGES:
        caminho = f"{BASE}{page}"
        conteudo = (await sftp.download(caminho)).decode("utf-8")
        novo = conteudo
        total = 0
        for pat, repl in PATTERNS:
            novo, n = pat.subn(repl, novo)
            total += n
        if total == 0:
            print(f"{page}: nenhum padrão bateu, pulando")
            continue
        await sftp.upload(caminho, novo.encode("utf-8"))
        print(f"{page}: corrigido ({total} substituições)")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
