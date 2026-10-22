"""Reforço SEO de 2 artigos do blog (22/10/2026), a partir das buscas reais do Search Console.
Gera <slug>.v2.html a partir de <slug>.original.html; cada troca precisa existir exatamente 1 vez."""
import json
import sys
from pathlib import Path

PASTA = Path(__file__).parent


def trocar(texto: str, velho: str, novo: str) -> str:
    n = texto.count(velho)
    if n != 1:
        sys.exit(f"Trecho aparece {n} vezes (esperado 1): {velho[:90]!r}")
    return texto.replace(velho, novo)


def faq_jsonld(texto: str, perguntas: list[tuple[str, str]]) -> str:
    """Põe as perguntas novas no início do FAQPage (JSON-LD)."""
    marca = '"@type": "FAQPage",\n  "mainEntity": ['
    itens = "".join(
        "\n    " + json.dumps(
            {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}}, ensure_ascii=False
        ) + ","
        for p, r in perguntas
    )
    return trocar(texto, marca, marca + itens)


def faq_html(texto: str, perguntas: list[tuple[str, str]]) -> str:
    blocos = "".join(f"\n\n<h3>{p}</h3>\n<p>{r}</p>" for p, r in perguntas)
    return trocar(texto, "<h2>Perguntas frequentes</h2>", "<h2>Perguntas frequentes</h2>" + blocos)


ATUALIZADO = ' <span class="dot">•</span>\n            <span><i class="fa-solid fa-rotate"></i> Atualizado em 22 de outubro de 2026</span>'

# ---------------------------------------------------------------- Limpeza de banheiro
slug = "empresa-pode-obrigar-limpar-banheiro"
s = (PASTA / f"{slug}.original.html").read_text(encoding="utf-8")
titulo_velho = "Empresa pode obrigar funcionário a limpar banheiro?"
titulo = "Atendente ou recepcionista pode ser obrigada a lavar banheiro?"
descricao = ("Atendente, recepcionista ou operador de loja pode ser obrigado a lavar banheiro? Veja quando é "
             "desvio de função, o que diz a CLT e o que fazer.")
s = trocar(s, f"<title>{titulo_velho} | Dra. Letícia Barros</title>",
           "<title>Atendente pode lavar banheiro? Quando é desvio de função | Dra. Letícia Barros</title>")
s = trocar(s, 'content="Não. Obrigar funcionário a limpar banheiro fora da função é desvio de função e pode configurar assédio moral. Veja seus direitos e o que fazer. Advogada em Vitória-ES."',
           f'content="{descricao}"')
s = trocar(s, 'content="empresa pode obrigar limpar banheiro, desvio de função,',
           'content="atendente pode lavar banheiro, recepcionista pode fazer limpeza, lavar banheiro é desvio de função, empresa pode obrigar limpar banheiro, desvio de função,')
s = trocar(s, f'<meta property="og:title" content="{titulo_velho}">', f'<meta property="og:title" content="{titulo}">')
s = trocar(s, '<meta property="og:description" content="Obrigar funcionário a limpar banheiro fora da função pode ser desvio de função e assédio moral. Entenda seus direitos.">',
           f'<meta property="og:description" content="{descricao}">')
s = trocar(s, f'"headline": "{titulo_velho}"', f'"headline": "{titulo}"')
s = trocar(s, '"description": "Obrigar funcionário a limpar banheiro fora da função pode configurar desvio de função e assédio moral."',
           f'"description": "{descricao}"')
s = trocar(s, '"dateModified": "2026-10-10"', '"dateModified": "2026-10-22"')
s = trocar(s, f'"name": "{titulo_velho}"', f'"name": "{titulo}"')
s = trocar(s, '<h1>Empresa pode obrigar funcionário <span class="highlight">a limpar banheiro?</span></h1>',
           '<h1>Atendente ou recepcionista pode ser obrigada <span class="highlight">a lavar banheiro?</span></h1>')
s = trocar(s, '<span><i class="fa-regular fa-calendar"></i> 16 de abril de 2026</span>',
           '<span><i class="fa-regular fa-calendar"></i> 16 de abril de 2026</span>' + ATUALIZADO)
s = trocar(s, "<h2>Quando vira assédio moral?</h2>", """<h2>Atendente, recepcionista ou operador de loja: pode ser obrigado a lavar banheiro?</h2>
<p>Essa é a dúvida que mais chega aqui, então vou direto ao ponto, função por função:</p>
<ul>
    <li><strong>Atendente</strong> (de loja, lanchonete, clínica): foi contratada para atender cliente. Deixar o balcão em ordem faz parte; lavar banheiro todo dia, não. Se virou rotina, é desvio de função.</li>
    <li><strong>Recepcionista</strong>: a função é receber pessoas, agendar e atender telefone. Limpar banheiro não combina com isso. Uma ajuda pontual, num dia de imprevisto, é diferente de uma obrigação diária.</li>
    <li><strong>Operador de loja, de caixa ou vendedor</strong>: organizar a própria área de trabalho pode fazer parte. Limpar banheiro de forma fixa, não.</li>
    <li><strong>Auxiliar de limpeza ou de serviços gerais</strong>: aqui, sim, limpar banheiro é parte do trabalho. E pode existir direito ao <a href="insalubridade-quem-tem-direito.html">adicional de insalubridade</a> quando o banheiro é de uso público ou de grande circulação (Súmula 448 do TST).</li>
</ul>
<p>O que decide não é só o nome do cargo na carteira: é o que você faz <strong>todo dia</strong> e o que foi combinado na contratação. Por isso a carteira, o contrato e as mensagens com as ordens são tão importantes.</p>

<h2>Quando vira assédio moral?</h2>""")
perguntas = [
    ("Lavar banheiro é desvio de função?",
     "Para quem não foi contratado para limpeza, sim: quando lavar banheiro vira rotina ou obrigação, é desvio de função, porque a tarefa não é compatível com o cargo (art. 456, parágrafo único, da CLT). Para auxiliar de limpeza ou de serviços gerais, faz parte da função."),
    ("Recepcionista pode fazer limpeza?",
     "Manter a própria recepção organizada, sim. Limpar banheiro ou fazer a faxina do local de forma fixa, não: isso foge da função de recepcionista e pode ser desvio de função."),
    ("Quem deve limpar o banheiro da empresa?",
     "Quem foi contratado para isso: auxiliar de limpeza, de serviços gerais ou uma empresa terceirizada de limpeza. A empresa não pode resolver a falta desse profissional passando a tarefa, de forma fixa, para quem tem outra função."),
]
s = faq_jsonld(s, perguntas)
s = faq_html(s, perguntas)
(PASTA / f"{slug}.v2.html").write_text(s, encoding="utf-8")
print("ok", slug)

# ---------------------------------------------------------------- Licença de 180 dias
slug = "stf-licenca-maternidade-180-dias-o-que-mudou-de-verdade"
s = (PASTA / f"{slug}.original.html").read_text(encoding="utf-8")
titulo_velho = "STF deu 180 dias de licença-maternidade pra todo mundo? Entenda o que mudou de verdade"
titulo = "Licença-maternidade mudou para 180 dias? Entenda o que o STF decidiu de verdade"
desc_velha = "O STF decidiu sobre licença-maternidade em 23/09/2026, mas não criou 180 dias automáticos pra toda trabalhadora. Entenda a regra real da ADI 7.495."
descricao = ("A licença-maternidade mudou para 180 dias? Não para todas. Veja quem tem direito aos 180 dias e o "
             "que o STF decidiu na ADI 7.495.")
s = trocar(s, f"<title>{titulo_velho} | Dra. Letícia Barros</title>",
           "<title>Licença-maternidade mudou para 180 dias? O que o STF decidiu | Dra. Letícia Barros</title>")
s = trocar(s, f'<meta name="description" content="{desc_velha}">', f'<meta name="description" content="{descricao}">')
s = trocar(s, f'<meta property="og:title" content="{titulo_velho}">', f'<meta property="og:title" content="{titulo}">')
s = trocar(s, f'<meta property="og:description" content="{desc_velha}">', f'<meta property="og:description" content="{descricao}">')
s = trocar(s, f'"headline": "{titulo_velho}"', f'"headline": "{titulo}"')
s = trocar(s, f'"description": "{desc_velha}"', f'"description": "{descricao}"')
s = trocar(s, '"dateModified": "2026-10-10"', '"dateModified": "2026-10-22"')
s = trocar(s, f'"name": "{titulo_velho}"', f'"name": "{titulo}"')
s = trocar(s, f"<h1>{titulo_velho}</h1>", f"<h1>{titulo}</h1>")
s = trocar(s, '<span><i class="fa-regular fa-calendar"></i> 24 de setembro de 2026</span>',
           '<span><i class="fa-regular fa-calendar"></i> 24 de setembro de 2026</span>' + ATUALIZADO)
s = trocar(s, "<h2>Como era antes de 23/09/2026</h2>", """<h2>Resposta rápida: a licença-maternidade mudou para 180 dias?</h2>
<p><strong>Não para todas.</strong> A regra geral da CLT continua sendo <strong>120 dias</strong>. Os 180 dias de licença-maternidade (120 + 60 de prorrogação) valem para quem trabalha em empresa do Programa Empresa Cidadã, para servidoras que têm a prorrogação no seu regime e para quem tem acordo coletivo ou política da empresa mais benéfica. O que o STF mudou foi outra coisa: a mãe adotante não pode ter licença menor que a mãe biológica.</p>

<h2>Como era antes de 23/09/2026</h2>""")
s = trocar(s, "<h2>Então o que mudou de fato, do antes pro agora</h2>", """<h2>Quem tem direito a 180 dias de licença-maternidade</h2>
<ul>
    <li><strong>Empregada de empresa do Programa Empresa Cidadã</strong> (Lei 11.770/2008): precisa pedir a prorrogação até o fim do primeiro mês depois do parto. Nos 60 dias a mais, recebe o salário integral, não pode trabalhar em outro lugar e a criança fica sob os seus cuidados (não pode ir para creche).</li>
    <li><strong>Servidora pública federal</strong>: a prorrogação de 60 dias existe desde o Decreto 6.690/2008. Muitos estados e municípios têm regra própria, vale conferir a do seu órgão.</li>
    <li><strong>Quem tem acordo ou convenção coletiva, ou política interna da empresa</strong>, que garanta os 180 dias.</li>
    <li><strong>Mãe adotante, nesses mesmos casos</strong>: depois da ADI 7.495, ela tem exatamente o mesmo período da mãe biológica.</li>
</ul>
<p>Não sabe se a sua empresa é do Empresa Cidadã? Pergunte ao RH antes do parto: o pedido tem prazo.</p>

<h2>Então o que mudou de fato, do antes pro agora</h2>""")
perguntas = [
    ("A licença-maternidade mudou para 180 dias?",
     "Não para todas. A regra geral da CLT continua sendo 120 dias. Os 180 dias valem para empregadas de empresas do Programa Empresa Cidadã, para servidoras que têm a prorrogação no seu regime e quando existe norma coletiva ou política da empresa mais benéfica."),
    ("Quem tem direito a 180 dias de licença-maternidade?",
     "Empregada de empresa do Programa Empresa Cidadã que pede a prorrogação até o fim do primeiro mês após o parto, servidora pública federal (Decreto 6.690/2008) e de órgãos que preveem a prorrogação, e quem tem acordo coletivo ou política interna que garanta os 180 dias. A mãe adotante tem o mesmo direito nesses casos."),
    ("Quando começa a valer a decisão do STF sobre a licença-maternidade?",
     "A decisão vale para as licenças futuras e para as que estavam em andamento em 23/09/2026. Licenças que já tinham terminado não são reabertas."),
]
s = faq_jsonld(s, perguntas)
s = faq_html(s, perguntas)
(PASTA / f"{slug}.v2.html").write_text(s, encoding="utf-8")
print("ok", slug)
