"""Gera lp/assedio-eleitoral-es.html a partir de lp/demissao-por-voto.html (28/10/2026).

Mesmo visual, formulário e regras do BRIEFING.md; conteúdo próprio do Espírito Santo (números do MPT-ES, denúncia na
PRT da 17ª Região, perguntas locais), para não concorrer com a LP nacional no Google. O guia de provas fica só na LP
nacional; esta aponta para ele.
Uso: py gerar_lp_es.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
ORIGEM = RAIZ / "lp" / "demissao-por-voto.html"
DESTINO = RAIZ / "lp" / "assedio-eleitoral-es.html"
URL = "https://advogadaleticiabarros.com.br/lp/assedio-eleitoral-es.html"
GUIA = "https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html"

FAQ = [
    ("Fui demitido por causa do voto no Espírito Santo. Onde denuncio?",
     "No Ministério Público do Trabalho do Espírito Santo (Procuradoria Regional do Trabalho da 17ª Região), pelo site "
     "prt17.mpt.mp.br ou em uma unidade do MPT. A denúncia pode ser anônima, e quem se identifica pode pedir sigilo dos dados."),
    ("A empresa pode me demitir por causa do meu voto?",
     "Não. A Constituição garante que ninguém perde direitos por convicção política, e a Lei 9.029/1995 proíbe a dispensa "
     "discriminatória. O trabalhador pode escolher entre voltar ao emprego com os salários do período ou receber o dobro da "
     "remuneração do período de afastamento, além de indenização por dano moral."),
    ("Quantas denúncias de assédio eleitoral o Espírito Santo teve em 2026?",
     "O MPT-ES registrou 47 denúncias até 27 de outubro de 2026, 57% a mais que as 30 contadas uma semana antes. No ano, "
     "foram 19 termos de ajustamento de conduta e 3 ações na Justiça."),
    ("Preciso ter provas para denunciar?",
     "Ajudam muito: mensagens, áudios, prints de grupos, posts e nomes de testemunhas. Mas a falta de prova no momento da "
     "denúncia não impede o MPT de investigar."),
    ("Onde corre a ação trabalhista no Espírito Santo?",
     "Na Justiça do Trabalho do Espírito Santo, o TRT da 17ª Região, que tem varas em Vitória e no interior. O prazo é de "
     "até 2 anos depois do fim do contrato (Constituição, art. 7º, XXIX)."),
    ("Eu só fui ameaçado de demissão. Isso também é proibido?",
     "Sim. Ameaçar, pressionar ou prometer vantagem pelo voto é assédio eleitoral, proibido pela Resolução TSE 23.755/2026, "
     "e a coação pode ser crime (Código Eleitoral, art. 301)."),
]


def faq_schema() -> str:
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in FAQ]},
        ensure_ascii=False, indent=2)


def faq_html() -> str:
    return "\n".join(f"      <details><summary>{p}</summary><p>{r}</p></details>" for p, r in FAQ)


def trocar(html: str, antigo: str, novo: str) -> str:
    assert html.count(antigo) == 1, f"trecho não encontrado uma única vez: {antigo[:60]!r}"
    return html.replace(antigo, novo)


def entre(html: str, inicio: str, fim: str, novo: str) -> str:
    a = html.index(inicio)
    b = html.index(fim, a) + len(fim)
    return html[:a] + novo + html[b:]


def main() -> None:
    h = ORIGEM.read_text(encoding="utf-8")
    h = trocar(h, "<title>Demitido por causa do voto? Seus direitos e como juntar as provas | Letícia Barros Advocacia</title>",
               "<title>Assédio eleitoral no ES: demitido pelo voto? Como denunciar | Letícia Barros Advocacia</title>")
    h = entre(h, '<meta name="description"', ">",
              '<meta name="description" content="O Espírito Santo já tem 47 denúncias de assédio eleitoral no trabalho em 2026. '
              'Veja o que a lei garante a quem foi demitido ou ameaçado por causa do voto e como denunciar no MPT-ES.">')
    h = h.replace("https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html", URL)
    h = trocar(h, '<meta property="og:title" content="Fui demitido por causa do meu voto. E agora?">',
               '<meta property="og:title" content="Demitido pelo voto no Espírito Santo? Seus direitos e como denunciar">')
    h = entre(h, '<meta property="og:description"', ">",
              '<meta property="og:description" content="47 denúncias no MPT-ES em 2026. Demitir por opinião política é dispensa '
              'discriminatória, não importa em quem você votou.">')
    h = entre(h, '<script type="application/ld+json">', "</script>",
              f'<script type="application/ld+json">\n{faq_schema()}\n  </script>')

    h = trocar(h, '<span class="badge"><i></i>Alerta do MPT · outubro de 2026</span>',
               '<span class="badge"><i></i>Espírito Santo · MPT-ES · outubro de 2026</span>')
    h = trocar(h, "<h1>Fui demitido por causa do meu voto. <em>E agora?</em></h1>",
               "<h1>Demitido ou ameaçado pelo voto <em>no Espírito Santo?</em></h1>")
    h = entre(h, '<p class="sub">', "</p>",
              '<p class="sub">O MPT-ES já recebeu <strong>47 denúncias de assédio eleitoral</strong> no trabalho em 2026, '
              '57% a mais em uma semana. Demitir por opinião política é <strong>dispensa discriminatória</strong>, proibida '
              'por lei, em Vitória, Vila Velha, Serra, Cariacica ou em qualquer cidade. <strong>Não importa em quem você '
              'votou.</strong></p>')
    h = trocar(h, '<a class="link-provas" href="#provas">Veja como juntar as provas, passo a passo ↓</a>',
               '<a class="link-provas" href="#denuncia">Veja como denunciar no MPT-ES ↓</a>')

    h = entre(h, "<h2>Isso está acontecendo <em>agora</em>, em todo o Brasil</h2>", '<p class="fonte">',
              '<h2>Os números do <em>Espírito Santo</em></h2>\n'
              '    <p class="subtitulo-secao">Depois do 2º turno, as denúncias de pressão e retaliação por causa do voto '
              'cresceram no estado e no país. Elas incluem ameaça de demissão, demissão e recusa de contratação.</p>\n'
              '    <div class="numeros">\n'
              '      <div class="numero"><b>47</b><span>denúncias de assédio eleitoral no trabalho no ES em 2026, até 27/10</span></div>\n'
              '      <div class="numero"><b>+57%</b><span>em uma semana: eram 30 em 21/10</span></div>\n'
              '      <div class="numero"><b>19</b><span>acordos (TACs) firmados pelo MPT-ES no ano, além de 3 ações na Justiça</span></div>\n'
              '    </div>\n    <p class="fonte">')
    h = trocar(h, "Fonte: balanços do Ministério Público do Trabalho divulgados em outubro de 2026.",
               "Fonte: MPT no Espírito Santo, balanço de 27/10/2026 divulgado por A Gazeta. Em todo o Brasil, o MPT "
               "contava 2.364 denúncias no ano até a mesma data.")

    # O guia de provas e o bloco de empresa ficam só na LP nacional (evita conteúdo duplicado).
    h = entre(h, '<section id="provas">', "</section>",
              '<section id="provas">\n    <h2>As provas que <em>mais ajudam</em></h2>\n'
              '    <div class="lei">\n'
              '      <div><strong>Mensagens e áudios</strong> do chefe ou do dono falando de voto, candidato ou da sua opinião.</div>\n'
              '      <div><strong>Prints de grupos da empresa</strong> com data, hora, quem mandou e o nome do grupo.</div>\n'
              '      <div><strong>Carta de dispensa e termo de rescisão</strong>, com a data. Demissão logo depois da eleição pesa como indício.</div>\n'
              '      <div><strong>Testemunhas:</strong> nome, contato e o que cada pessoa viu ou ouviu.</div>\n'
              '    </div>\n'
              f'    <div class="cta-meio"><a class="btn-meio" href="{GUIA}#provas">Guia completo das provas, passo a passo</a></div>\n'
              '  </section>')
    h = entre(h, '<h2>Como denunciar no <em>MPT</em>, passo a passo</h2>', "</div>\n    </div>\n",
              '<h2>Como denunciar no <em>MPT-ES</em>, passo a passo</h2>\n'
              '    <p class="subtitulo-secao">No Espírito Santo, quem recebe a denúncia é a Procuradoria Regional do Trabalho '
              'da 17ª Região. É gratuito, pode ser anônimo e não substitui a ação trabalhista: o MPT investiga a empresa; os '
              'seus direitos individuais você busca com orientação jurídica.</p>\n'
              '    <div class="passos">\n'
              '      <div class="passo"><div class="n">1</div><div><h3>Entre no site do MPT-ES</h3><p>Acesse <a href="https://prt17.mpt.mp.br" target="_blank" rel="noopener">prt17.mpt.mp.br</a> e procure a área de denúncia. Também dá para ir a uma unidade do MPT ou usar o aplicativo MPT Pardal.</p></div></div>\n'
              '      <div class="passo"><div class="n">2</div><div><h3>Conte o que aconteceu</h3><p>Nome da empresa, cidade, o que foi dito ou feito, quando e por quem.</p></div></div>\n'
              '      <div class="passo"><div class="n">3</div><div><h3>Anexe o que tiver</h3><p>Prints, áudios e nomes de testemunhas ajudam. Sem prova no momento, o MPT ainda pode investigar.</p></div></div>\n'
              '      <div class="passo"><div class="n">4</div><div><h3>Escolha anonimato ou sigilo</h3><p>A denúncia pode ser anônima. Se você se identificar, pode pedir que o seu nome fique em sigilo. Guarde o número do protocolo.</p></div></div>\n'
              '    </div>\n')
    h = entre(h, "<section>\n    <h2>Se você é <em>empresa</em></h2>", "</section>",
              "<section>\n    <h2>E a <em>ação trabalhista</em>, no Espírito Santo</h2>\n"
              '    <div class="empresa">\n'
              '      <p style="margin-top:0">A denúncia ao MPT e a ação trabalhista são caminhos diferentes, e podem andar juntos. '
              "A ação corre na Justiça do Trabalho do Espírito Santo (TRT da 17ª Região), que tem varas em Vitória e no interior, "
              "e o prazo é de até 2 anos depois do fim do contrato.</p>\n"
              '      <p>A Dra. Letícia Barros atende presencialmente em Vitória e on-line em todo o estado. '
              f'Se você é empresa, veja o <a href="{GUIA}">guia nacional</a>, que tem um bloco para empregadores.</p>\n'
              "    </div>\n  </section>")
    h = entre(h, "<h2>Perguntas frequentes</h2>\n    <div style=\"margin-top:22px\">", "</div>\n    <div class=\"sobre\"",
              f'<h2>Perguntas frequentes</h2>\n    <div style="margin-top:22px">\n{faq_html()}\n    </div>\n    <div class="sobre"')
    h = trocar(h, "'[LP demissao-por-voto]'", "'[LP assedio-eleitoral-es]'")
    h = trocar(h, "corpo.utm_campaign = 'assedio-eleitoral-2026'", "corpo.utm_campaign = 'assedio-eleitoral-es-2026'")
    # O guia de provas (botão copiar modelo) não existe nesta página.
    h = entre(h, "    document.getElementById('copiar-modelo')", "});\n", "")
    h = trocar(h, "Veja <a href=\"#denuncia\">como denunciar, passo a passo</a>.", "Veja <a href=\"#denuncia\">como denunciar no MPT-ES</a>.")
    h = trocar(h, "Logo abaixo está o <a href=\"#provas\">passo a passo de como juntar cada prova</a>.",
               f"Veja <a href=\"#provas\">as provas que mais ajudam</a> e o <a href=\"{GUIA}#provas\">guia completo</a>.")
    assert "demissao-por-voto" not in h.replace(GUIA, ""), "sobrou referência à LP nacional"
    DESTINO.write_text(h, encoding="utf-8")
    print(DESTINO)


if __name__ == "__main__":
    main()
