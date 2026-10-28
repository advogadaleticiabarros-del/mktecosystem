"""Refaz o "Continue lendo" dos artigos já publicados com a regra por assunto (blog_seo.escolher_relacionados,
28/10/2026). Antes, cada artigo indicava os 3 mais recentes da área (a licença de 180 dias indicava pet no divórcio).

Só troca a <section class="related-posts"> de quem já tem uma; páginas com leituras escolhidas à mão ficam de fora
(MANUAIS). Tudo ou nada, com backup .tgz dos originais. Sem --aplicar, só mostra o que mudaria.

Uso na VPS:
  docker compose cp scripts/renovar_relacionados.py api:/tmp/
  docker compose exec -T -e PYTHONPATH=/app api python /tmp/renovar_relacionados.py [--aplicar]
  docker compose cp api:/tmp/<backup>.tgz /root/orbit-backups/
"""
import asyncio
import io
import re
import sys
import tarfile
from datetime import datetime

from app.config import settings
from app.integrations.publish.sftp_client import SFTPClient
from app.services.blog_seo import _bloco_relacionados, cards_do_indice, escolher_relacionados
from app.services.site_descoberta import avisar_indexnow

SITE = "https://advogadaleticiabarros.com.br/blog/"
MANUAIS = {"empresa-pode-obrigar-limpar-banheiro", "stf-licenca-maternidade-180-dias-o-que-mudou-de-verdade"}
SECAO = re.compile(r'<section class="related-posts">.*?</section>\s*', re.S)


def relacionados_atuais(html: str) -> list[str]:
    secao = SECAO.search(html)
    return re.findall(r'href="([^"]+)\.html" class="related-card"', secao.group(0)) if secao else []


async def main(aplicar: bool) -> None:
    raiz = settings.BLOG_SFTP_PATH.rstrip("/") + "/"
    sftp = SFTPClient(host=settings.BLOG_SFTP_HOST, port=settings.BLOG_SFTP_PORT,
                      user=settings.BLOG_SFTP_USER, password=settings.BLOG_SFTP_PASSWORD)
    prontas: list[tuple[str, bytes, str]] = []
    try:
        cards = cards_do_indice((await sftp.download(raiz + "index.html")).decode("utf-8"))
        categoria = {}
        for c in cards:
            categoria.setdefault(c["slug"], c["cat"])
        for slug, cat in categoria.items():
            if slug in MANUAIS:
                continue
            try:
                original = await sftp.download(f"{raiz}{slug}.html")
            except Exception:
                print(f"SEM ARQUIVO {slug}")
                continue
            html = original.decode("utf-8")
            if not SECAO.search(html):
                continue
            antes = relacionados_atuais(html)
            novos = escolher_relacionados(cards, slug=slug, categoria_slug=cat, reserva=antes)
            if [r["slug"] for r in novos] == antes:
                continue
            bloco = _bloco_relacionados(novos)
            if "\r\n" in html:
                bloco = bloco.replace("\n", "\r\n")
            depois = SECAO.sub(lambda _: bloco, html, count=1)
            print(f"{slug[:50]}\n   antes: {', '.join(s[:28] for s in antes)}\n   agora: {', '.join(r['slug'][:28] for r in novos)}")
            prontas.append((slug, original, depois))
        if not aplicar:
            print(f"SIMULAÇÃO: {len(prontas)} artigo(s) mudariam")
            return
        backup = f"/tmp/site-relacionados-{datetime.now():%Y%m%d-%H%M}.tgz"
        with tarfile.open(backup, "w:gz") as tar:
            for slug, original, _ in prontas:
                info = tarfile.TarInfo(f"blog/{slug}.html")
                info.size = len(original)
                tar.addfile(info, io.BytesIO(original))
        print(f"BACKUP {backup}")
        for slug, _, depois in prontas:
            await sftp.upload(f"{raiz}{slug}.html", depois.encode("utf-8"))
    finally:
        await sftp.close()
    if aplicar and prontas:
        await avisar_indexnow([f"{SITE}{slug}.html" for slug, *_ in prontas])
        print(f"APLICADO {len(prontas)} artigos")


if __name__ == "__main__":
    asyncio.run(main("--aplicar" in sys.argv[1:]))
