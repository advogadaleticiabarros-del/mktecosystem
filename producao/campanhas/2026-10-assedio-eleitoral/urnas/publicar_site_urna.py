"""Roda DENTRO do container da API: publica o fundo da LP com a urna (arquivo novo; o antigo fica no servidor), a LP
que aponta para ele e a capa nova do artigo (díptico urna + trabalhador). Antes, guarda em /tmp/bkp_urna_site/ a LP
e a capa que estavam no ar. Arquivos de entrada em /tmp/urna-site/.
Uso: docker compose exec -T -e PYTHONPATH=/app api python - < publicar_site_urna.py
"""
import asyncio
import os

from app.services.blog_seo import capa_para_jpg
from app.services.central_google import _site_padrao

SLUG = "demitido-por-causa-do-voto-o-que-a-lei-garante"
ENT, BKP = "/tmp/urna-site", "/tmp/bkp_urna_site"


async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    os.makedirs(BKP, exist_ok=True)
    open(f"{BKP}/demissao-por-voto.html", "w", encoding="utf-8").write(await s.ler("lp/demissao-por-voto.html"))
    open(f"{BKP}/capa-{SLUG}.jpg", "wb").write(await sftp.download(f"{raiz}/blog/capas/{SLUG}.jpg"))
    print("backup feito em", BKP, sorted(os.listdir(BKP)))
    await sftp.upload(f"{raiz}/assets/images/lp/lp-demissao-voto-urna.jpg", open(f"{ENT}/lp-demissao-voto-urna.jpg", "rb").read())
    await sftp.upload(f"{raiz}/lp/demissao-por-voto.html", open(f"{ENT}/demissao-por-voto.html", "rb").read())
    await sftp.upload(f"{raiz}/blog/capas/{SLUG}.jpg", capa_para_jpg(open(f"{ENT}/capa-blog-urna.jpg", "rb").read()))
    await sftp.close()
    print("publicado: fundo da LP, LP e capa do artigo")


asyncio.run(main())
