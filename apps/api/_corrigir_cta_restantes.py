"""Corrige os article-cta restantes (segunda ocorrência no meio do texto, ou
única ocorrência que ficou de fora do primeiro lote) que ainda linkavam
direto pro WhatsApp com copy não compliant.
"""
import os
import asyncio
import re

from app.integrations.publish.sftp_client import SFTPClient

BASE = "domains/advogadaleticiabarros.com.br/public_html/blog/"

FIXES = {
    "racismo-no-trabalho-como-provar-e-seus-direitos": (
        "Sofreu racismo no trabalho? A lei está do seu lado",
        "Você merece trabalhar com dignidade e respeito. Se passou por discriminação racial, isso não é normal.",
        "../contato.html",
    ),
    "rescisao-indireta-riscos-vale-a-pena": (
        "Sua situação merece uma análise franca",
        "Advogada trabalhista em Vitória-ES, atendendo todo o Brasil online.",
        "../contato.html",
    ),
    "aborto-espontaneo-direitos-da-trabalhadora-clt": (
        "Você foi demitida após um aborto espontâneo?",
        "Isso pode ser demissão ilegal. Você não precisa enfrentar isso sozinha.",
        "../contato.html",
    ),
}


def montar_cta(titulo: str, texto: str, link: str) -> str:
    return (
        '<div class="article-cta">\n'
        f"    <h3>{titulo}</h3>\n"
        f'    <p style="color: var(--texto-claro);">{texto} Se essa é a sua situação, procure uma advogada de confiança.</p>\n'
        f'    <a href="{link}" class="btn-primary"><i class="fa-solid fa-arrow-right"></i> Busque orientação jurídica</a>\n'
        "</div>"
    )


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for slug, (titulo, texto, link) in FIXES.items():
        caminho = f"{BASE}{slug}.html"
        conteudo = (await sftp.download(caminho)).decode("utf-8")
        n_before = len(re.findall(r'<div class="article-cta"', conteudo))
        novo_cta = montar_cta(titulo, texto, link)

        # Substitui apenas o bloco article-cta que ainda contém btn-whatsapp
        # (o já corrigido no primeiro lote não tem esse marcador).
        novo_conteudo, n = re.subn(
            r'<div class="article-cta"[^>]*>(?:(?!</div>).)*?btn-whatsapp(?:(?!</div>).)*?</div>',
            novo_cta,
            conteudo,
            flags=re.S,
        )
        if n == 0:
            print(f"{slug}: NAO ENCONTRADO, pulando")
            continue
        await sftp.upload(caminho, novo_conteudo.encode("utf-8"))
        print(f"{slug}: corrigido ({n_before} -> substituídas {n})")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
