"""Corrige os CTAs antigos (grátis/sem compromisso/Falar agora) que violam
a ética OAB, em artigos legados do blog fora do pipeline oficial.
"""
import os
import asyncio
import re

from app.integrations.publish.sftp_client import SFTPClient

BASE = "domains/advogadaleticiabarros.com.br/public_html/blog/"

NOVOS_CTAS = {
    "aposentadoria-hibrida-como-funciona": (
        "Sabe se já pode se aposentar?",
        "Se você já contribuiu por tempos diferentes de vínculo, vale entender se a aposentadoria híbrida se aplica ao seu caso.",
        "../contato.html",
    ),
    "bpc-loas-como-funciona": (
        "Acha que tem direito ao BPC/LOAS?",
        "Muitos pedidos de BPC/LOAS são negados por erro na análise, e cabe recurso quando isso acontece.",
        "../contato.html",
    ),
    "carga-horaria-maxima-clt": (
        "Está fazendo hora extra sem receber?",
        "Se a empresa está desrespeitando sua jornada, você pode ter direito a cobrar horas extras retroativas.",
        "../contato.html",
    ),
    "compra-online-direitos-do-consumidor": (
        "Seu direito foi desrespeitado?",
        "Se seu direito como consumidor foi desrespeitado, vale buscar orientação sobre os caminhos possíveis, do Procon à Justiça.",
        "../contato.html",
    ),
    "divorcio-como-funciona-e-quanto-custa": (
        "Quer entender seus direitos antes de decidir?",
        "Entender seus direitos antes de decidir evita erros que custam caro depois.",
        "../contato.html",
    ),
    "empresa-pode-obrigar-limpar-banheiro": (
        "Está passando por isso?",
        "Situações assim são comuns em comércio e serviços, e podem configurar desvio de função.",
        "../contato.html",
    ),
    "ex-nao-paga-pensao-o-que-fazer": (
        "O genitor está deixando seus filhos sem pensão?",
        "Pensão atrasada pode ser cobrada com bloqueio de conta ou desconto em folha, dependendo da situação.",
        "../lp-v3/pensao-alimenticia.html",
    ),
    "fgts-trabalhador-temporario-direitos-e-como-cobrar": (
        "Empresa não recolheu seu FGTS?",
        "Esse dinheiro é seu, e existe prazo pra cobrar o que não foi recolhido corretamente.",
        "../contato.html",
    ),
    "fui-demitida-gravida-o-que-fazer": (
        "Você passou por isso?",
        "Se isso aconteceu com você, existe um caminho legal pra reverter a situação ou ser indenizada pelo período de estabilidade.",
        "../lp-v3/gestante-clt.html",
    ),
    "guarda-compartilhada-como-funciona": (
        "Preocupada com a guarda dos seus filhos?",
        "Um acordo bem construído protege os filhos e os direitos de cada um dos pais.",
        "../contato.html",
    ),
    "insalubridade-quem-tem-direito": (
        "Acha que tem direito ao adicional?",
        "Quem trabalha exposto a agentes insalubres pode ter direito ao adicional correspondente.",
        "../contato.html",
    ),
    "nome-negativado-indevidamente-o-que-fazer": (
        "Seu nome foi negativado sem motivo?",
        "Negativação indevida pode gerar direito à indenização, dependendo do caso.",
        "../contato.html",
    ),
    "pensao-alimenticia-como-funciona": (
        "Filho sem pensão alimentícia?",
        "Toda criança tem direito à pensão alimentícia, e existem caminhos claros pra formalizar essa cobrança.",
        "../lp-v3/pensao-alimenticia.html",
    ),
    "plano-de-saude-negou-cobertura-o-que-fazer": (
        "Plano negou sua cirurgia ou cancelou sem aviso?",
        "Negativa de cobertura pode ser contestada, inclusive por via judicial urgente em casos que não podem esperar.",
        "../contato.html",
    ),
    "quanto-tempo-processar-apos-demissao": (
        "Você foi demitido e acha injusto?",
        "Alguns direitos trabalhistas têm prazo pra serem cobrados, por isso vale não deixar pra depois.",
        "../contato.html",
    ),
    "racismo-no-trabalho-como-provar-e-seus-direitos": (
        "Você não precisa enfrentar isso sozinha",
        "Se você viveu ou está vivendo racismo no trabalho, isso não é normal, e a lei está do seu lado.",
        "../contato.html",
    ),
    "rescisao-indireta-o-que-e-quando-tenho-direito": (
        "Sua empresa está te prejudicando?",
        "Se sua empresa está descumprindo obrigações básicas, vale entender se o seu caso permite pedir rescisão indireta.",
        "../contato.html",
    ),
    "rescisao-indireta-riscos-vale-a-pena": (
        "Quer uma avaliação honesta do seu caso?",
        "Vale entender com honestidade se a rescisão indireta faz sentido pro seu caso, antes de decidir.",
        "../contato.html",
    ),
    "trabalhei-sem-registro-posso-processar": (
        "Acha que pode ter direito?",
        "Trabalhar sem registro não tira seus direitos, mas exige provar o vínculo empregatício.",
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
    for slug, (titulo, texto, link) in NOVOS_CTAS.items():
        caminho = f"{BASE}{slug}.html"
        conteudo = (await sftp.download(caminho)).decode("utf-8")
        novo_cta = montar_cta(titulo, texto, link)
        novo_conteudo, n = re.subn(
            r'<div class="article-cta">.*?</div>', novo_cta, conteudo, count=1, flags=re.S
        )
        if n == 0:
            print(f"{slug}: NAO ENCONTRADO article-cta, pulando")
            continue
        await sftp.upload(caminho, novo_conteudo.encode("utf-8"))
        print(f"{slug}: corrigido")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
