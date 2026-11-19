"""(19/11/2026) O publicador tira <script> do corpo do artigo; este script põe o JSON-LD FAQPage no <head> da página
publicada, pelo mesmo SFTP do Orbit. Roda dentro do contêiner vps-api-1: python faq_no_head.py /tmp/spec5x2.json
Guarda cópia do HTML antes em /tmp."""
import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from app.services.central_google import _site_padrao


async def main(caminho_spec: str) -> None:
    site = _site_padrao()
    for a in json.load(open(caminho_spec, encoding="utf-8")):
        m = re.search(r'<script type="application/ld\+json">.*?</script>', a["html"], re.S)
        assert m, "spec sem FAQPage"
        arq = f"blog/{a['slug']}.html"
        html = await site.ler(arq)
        if '"FAQPage"' in html:
            print("já tem FAQPage", a["slug"])
            continue
        Path(f"/tmp/bkp_{a['slug']}_{datetime.now():%Y%m%d-%H%M%S}.html").write_text(html, encoding="utf-8")
        assert html.count("</head>") == 1
        novo = html.replace("</head>", f"    {m.group(0)}\n</head>")
        await site._sftp.upload(f"{site._raiz}/{arq}", novo.encode("utf-8"))
        print("FAQPage no head", a["slug"])


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
