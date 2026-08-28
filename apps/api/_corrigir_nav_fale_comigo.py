"""Troca o botão de menu 'Fale Comigo' (oferta pessoal direta) por 'Contato',
mantendo o mesmo link, em todas as páginas do blog (artigos legados +
pipeline), removendo a duplicidade de link ../contato.html quando presente.
"""
import os
import asyncio
import re

from app.integrations.publish.sftp_client import SFTPClient

BASE = "domains/advogadaleticiabarros.com.br/public_html/blog/"

SLUGS = [
    "aposentadoria-hibrida-como-funciona", "bpc-loas-como-funciona", "carga-horaria-maxima-clt",
    "compra-online-direitos-do-consumidor", "divorcio-como-funciona-e-quanto-custa",
    "empresa-pode-obrigar-limpar-banheiro", "ex-nao-paga-pensao-o-que-fazer",
    "fgts-trabalhador-temporario-direitos-e-como-cobrar", "fui-demitida-gravida-o-que-fazer",
    "guarda-compartilhada-como-funciona", "insalubridade-quem-tem-direito",
    "nome-negativado-indevidamente-o-que-fazer", "pensao-alimenticia-como-funciona",
    "plano-de-saude-negou-cobertura-o-que-fazer", "quanto-tempo-processar-apos-demissao",
    "racismo-no-trabalho-como-provar-e-seus-direitos", "rescisao-indireta-o-que-e-quando-tenho-direito",
    "rescisao-indireta-riscos-vale-a-pena", "trabalhei-sem-registro-posso-processar",
    "aborto-espontaneo-direitos-da-trabalhadora-clt", "gravida-pode-pedir-demissao-riscos-e-validacao",
    "pedi-demissao-gravida-posso-reverter",
    # artigos do pipeline oficial
    "inss-desconto-indevido-como-recuperar", "aposentadoria-mulher-regras-2026",
    "pix-pensao-alimenticia-o-que-muda", "bpc-crianca-necessidades-especiais",
    "gravidez-e-trabalho-seus-direitos",
]

PADRAO_DUP = re.compile(
    r'<li><a href="\.\./contato\.html">Contato</a></li>\s*'
    r'<li><a href="\.\./contato\.html" class="nav-cta">Fale Comigo</a></li>',
)
PADRAO_SIMPLES = re.compile(r'(<a href="\.\./contato\.html"[^>]*class="nav-cta"[^>]*>)Fale Comigo(</a>)')


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for slug in SLUGS:
        caminho = f"{BASE}{slug}.html"
        try:
            conteudo = (await sftp.download(caminho)).decode("utf-8")
        except Exception as e:
            print(f"{slug}: erro ao baixar ({e})")
            continue

        novo = PADRAO_DUP.sub('<li><a href="../contato.html" class="nav-cta">Contato</a></li>', conteudo)
        n = 1 if novo != conteudo else 0
        if n == 0:
            novo, n = PADRAO_SIMPLES.subn(r"\1Contato\2", conteudo)

        if n == 0:
            print(f"{slug}: nenhum padrão encontrado, pulando")
            continue

        await sftp.upload(caminho, novo.encode("utf-8"))
        print(f"{slug}: corrigido")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
