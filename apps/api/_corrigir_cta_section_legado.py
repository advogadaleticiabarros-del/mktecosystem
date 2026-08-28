"""Corrige o segundo bloco de CTA (<section class="cta-section">) nos artigos
legados do blog, que ainda linkava direto pro WhatsApp com mensagem
pré-preenchida e usava termos que violam a ética OAB (grátis, "fale comigo",
menção a honorários/valor). Mantém apenas reconhecimento da dor + link
impessoal pro contato/LP, sem falar de valor.
"""
import os
import asyncio
import re

from app.integrations.publish.sftp_client import SFTPClient

BASE = "domains/advogadaleticiabarros.com.br/public_html/blog/"

# slug -> (h2_html, paragrafo, link)
NOVOS = {
    "aposentadoria-hibrida-como-funciona": (
        "Quer saber se<br><span class=\"highlight\">já pode se aposentar?</span>",
        "Se você já contribuiu por tempos diferentes de vínculo, vale entender se a aposentadoria híbrida se aplica ao seu caso.",
        "../contato.html",
    ),
    "bpc-loas-como-funciona": (
        "Acha que tem direito<br><span class=\"highlight\">ao BPC/LOAS?</span>",
        "Muitos pedidos de BPC/LOAS são negados por erro na análise, e cabe recurso quando isso acontece.",
        "../contato.html",
    ),
    "carga-horaria-maxima-clt": (
        "Sua jornada está sendo<br><span class=\"highlight\">desrespeitada pela empresa?</span>",
        "Se sua empresa não paga hora extra ou te faz trabalhar além do limite legal, você pode ter direito a cobrar retroativamente.",
        "../contato.html",
    ),
    "compra-online-direitos-do-consumidor": (
        "Teve problema<br><span class=\"highlight\">em compra online?</span>",
        "Se seu direito como consumidor foi desrespeitado, vale buscar orientação sobre os caminhos possíveis, do Procon à Justiça.",
        "../contato.html",
    ),
    "divorcio-como-funciona-e-quanto-custa": (
        "Precisa se divorciar e<br><span class=\"highlight\">não sabe por onde começar?</span>",
        "Entender seus direitos antes de decidir evita erros que custam caro depois.",
        "../contato.html",
    ),
    "empresa-pode-obrigar-limpar-banheiro": (
        "Está sendo vítima<br><span class=\"highlight\">de desvio de função?</span>",
        "Situações assim são comuns em comércio e serviços, e podem configurar desvio de função.",
        "../contato.html",
    ),
    "ex-nao-paga-pensao-o-que-fazer": (
        "O genitor não paga pensão e<br><span class=\"highlight\">você está no limite?</span>",
        "Pensão atrasada pode ser cobrada com bloqueio de conta ou desconto em folha, dependendo da situação.",
        "../lp-v3/pensao-alimenticia.html",
    ),
    "fgts-trabalhador-temporario-direitos-e-como-cobrar": (
        "Empresa não recolheu seu FGTS<br><span class=\"highlight\">e você quer cobrar?</span>",
        "Esse dinheiro é seu, e existe prazo pra cobrar o que não foi recolhido corretamente.",
        "../contato.html",
    ),
    "fui-demitida-gravida-o-que-fazer": (
        "Você passou<br><span class=\"highlight\">por isso?</span>",
        "Se isso aconteceu com você, existe um caminho legal pra reverter a situação ou ser indenizada pelo período de estabilidade.",
        "../lp-v3/gestante-clt.html",
    ),
    "guarda-compartilhada-como-funciona": (
        "Separando e preocupada<br><span class=\"highlight\">com a guarda dos filhos?</span>",
        "Um acordo bem construído protege os filhos e os direitos de cada um dos pais.",
        "../contato.html",
    ),
    "insalubridade-quem-tem-direito": (
        "Quer saber se<br><span class=\"highlight\">tem direito ao adicional?</span>",
        "Quem trabalha exposto a agentes insalubres pode ter direito ao adicional correspondente.",
        "../contato.html",
    ),
    "nome-negativado-indevidamente-o-que-fazer": (
        "Seu nome foi negativado<br><span class=\"highlight\">sem você dever nada?</span>",
        "Negativação indevida pode gerar direito à indenização, dependendo do caso.",
        "../contato.html",
    ),
    "pensao-alimenticia-como-funciona": (
        "Filho sem<br><span class=\"highlight\">pensão alimentícia?</span>",
        "Toda criança tem direito à pensão alimentícia, e existem caminhos claros pra formalizar essa cobrança.",
        "../lp-v3/pensao-alimenticia.html",
    ),
    "plano-de-saude-negou-cobertura-o-que-fazer": (
        "Plano de saúde te deixou<br><span class=\"highlight\">na mão na hora que mais precisava?</span>",
        "Negativa de cobertura pode ser contestada, inclusive por via judicial urgente em casos que não podem esperar.",
        "../contato.html",
    ),
    "quanto-tempo-processar-apos-demissao": (
        "Seu direito foi<br><span class=\"highlight\">violado na demissão?</span>",
        "Alguns direitos trabalhistas têm prazo pra serem cobrados, por isso vale não deixar pra depois.",
        "../contato.html",
    ),
    "racismo-no-trabalho-como-provar-e-seus-direitos": (
        "Sofreu racismo no trabalho?<br><span class=\"highlight\">A lei está do seu lado</span>",
        "Você merece trabalhar com dignidade e respeito. Se passou por discriminação racial, isso não é normal.",
        "../contato.html",
    ),
    "rescisao-indireta-o-que-e-quando-tenho-direito": (
        "Sua empresa está te<br><span class=\"highlight\">prejudicando todos os dias?</span>",
        "Se o salário atrasa, o FGTS não é depositado ou você sofre assédio, pode ser hora de sair recebendo tudo a que tem direito.",
        "../contato.html",
    ),
    "rescisao-indireta-riscos-vale-a-pena": (
        "Antes de decidir,<br><span class=\"highlight\">conheça as suas chances de verdade</span>",
        "Vale entender com honestidade se a rescisão indireta faz sentido pro seu caso, antes de decidir.",
        "../contato.html",
    ),
    "trabalhei-sem-registro-posso-processar": (
        "Trabalhou<br><span class=\"highlight\">sem registro?</span>",
        "Trabalhar sem registro não tira seus direitos, mas exige provar o vínculo empregatício.",
        "../contato.html",
    ),
    "aborto-espontaneo-direitos-da-trabalhadora-clt": (
        "Seus direitos merecem ser<br><span class=\"highlight\">protegidos, mesmo nos dias mais difíceis</span>",
        "Se você está passando por isso e precisa de orientação, não precisa enfrentar isso sozinha.",
        "../contato.html",
    ),
}


def montar_cta_section(h2: str, paragrafo: str, link: str) -> str:
    return (
        '<section class="cta-section">\n'
        '    <div class="container">\n'
        '        <div class="cta-box reveal">\n'
        f"            <h2>{h2}</h2>\n"
        f'            <p>{paragrafo} Se essa é a sua situação, procure uma advogada de confiança.</p>\n'
        '            <div class="cta-buttons">\n'
        f'                <a href="{link}" class="btn-primary"><i class="fa-solid fa-arrow-right"></i> Busque orientação jurídica</a>\n'
        "            </div>\n"
        "        </div>\n"
        "    </div>\n"
        "</section>"
    )


async def main() -> None:
    sftp = SFTPClient(
        host=os.environ["BLOG_SFTP_HOST"],
        port=int(os.environ["BLOG_SFTP_PORT"]),
        user=os.environ["BLOG_SFTP_USER"],
        password=os.environ["BLOG_SFTP_PASSWORD"],
    )
    for slug, (h2, paragrafo, link) in NOVOS.items():
        caminho = f"{BASE}{slug}.html"
        conteudo = (await sftp.download(caminho)).decode("utf-8")
        novo_cta = montar_cta_section(h2, paragrafo, link)
        novo_conteudo, n = re.subn(
            r'<section class="cta-section">.*?</section>', novo_cta, conteudo, count=1, flags=re.S
        )
        if n == 0:
            print(f"{slug}: NAO ENCONTRADO cta-section, pulando")
            continue
        await sftp.upload(caminho, novo_conteudo.encode("utf-8"))
        print(f"{slug}: corrigido")
    await sftp.close()


if __name__ == "__main__":
    asyncio.run(main())
