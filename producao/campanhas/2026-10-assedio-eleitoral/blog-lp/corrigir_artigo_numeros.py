"""Roda no container: corrige os números do artigo da campanha do voto no ar (28/10/2026).
Sai "1.939, um recorde, quase dez vezes 2022" (não confere com o MPT: 2022 teve 3.373 no ano); entram os números de
27/10 e o link para a parte do Espírito Santo da LP. Backup em /tmp/bkp_artigo_voto_v1.html.
"""
import asyncio
from app.services.central_google import _site_padrao
from app.services.site_descoberta import avisar_indexnow

SLUG = "demitido-por-causa-do-voto-o-que-a-lei-garante"
URL = f"https://advogadaleticiabarros.com.br/blog/{SLUG}.html"
LP_ES = ("https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html?utm_source=blog&amp;utm_medium=artigo"
         "&amp;utm_campaign=assedio-eleitoral-2026&amp;utm_content=numeros-es#espirito-santo")

TROCAS = [
    ('<p>Até o fim do 2º turno, em 25 de outubro, o MPT tinha recebido <strong>1.939 denúncias</strong> de assédio '
     'eleitoral no trabalho em 2026. É um recorde: quase dez vezes o número de 2022.</p>',
     '<p>Até 27 de outubro, o MPT contava <strong>2.364 denúncias</strong> de assédio eleitoral no trabalho em 2026. '
     'Mais de 500 delas chegaram em menos de dois dias depois do 2º turno, entre a noite de 25 e a tarde de 27 de '
     'outubro. No Espírito Santo, já são <strong>47</strong>, 57% a mais em uma semana. Se você está no estado, veja '
     f'<a href="{LP_ES}">como denunciar no MPT-ES</a>.</p>'),
    ('<p>E tem uma diferença importante. Em 2022, o pico de denúncias veio entre o 1º e o 2º turno, com a pressão para '
     'votar. Agora, o pico veio <strong>depois</strong> da votação: 140 denúncias só no dia 26 de outubro, quando '
     'começaram as ameaças e as demissões de quem "votou errado".</p>',
     '<p>E tem uma diferença importante: desta vez, boa parte das denúncias veio <strong>depois</strong> da votação. '
     'Foram 140 só no dia 26 de outubro, quando começaram as ameaças e as demissões de quem "votou errado".</p>'),
    ('"dateModified": "2026-10-27"', '"dateModified": "2026-10-28"'),
]


async def main():
    s = _site_padrao(); sftp = s._sftp; raiz = s._raiz
    html = await s.ler(f"blog/{SLUG}.html")
    open("/tmp/bkp_artigo_voto_v1.html", "w", encoding="utf-8", newline="").write(html)
    for antigo, novo in TROCAS:
        assert html.count(antigo) == 1, f"trecho não encontrado uma única vez: {antigo[:50]!r}"
        html = html.replace(antigo, novo)
    await sftp.upload(f"{raiz}/blog/{SLUG}.html", html.encode("utf-8"))
    await sftp.close()
    print("artigo corrigido; backup em /tmp/bkp_artigo_voto_v1.html")
    print("indexnow:", await avisar_indexnow([URL]))

asyncio.run(main())
