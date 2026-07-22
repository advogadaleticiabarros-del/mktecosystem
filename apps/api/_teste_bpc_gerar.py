import asyncio
from datetime import date
from pathlib import Path

from app.services.render_artigo_blog import renderizar_artigo_html
from app.services.render_criativo import renderizar_slide

TITULO = "BPC para criança com deficiência: o benefício de R$ 1.621 que muita mãe não conhece"
META_DESCRIPTION = "Seu filho tem deficiência e a rotina pesa no bolso? O BPC/LOAS paga 1 salário mínimo por mês, sem precisar ter contribuído com o INSS. Veja quem tem direito."
RESUMO = "O BPC paga 1 salário mínimo por mês a crianças com deficiência de famílias de baixa renda, sem precisar ter contribuído ao INSS. Veja se seu filho tem direito."
CATEGORIA = "Previdenciário"
SLUG = "bpc-crianca-deficiencia-quem-tem-direito"

CORPO_HTML = """
<p>A rotina de mãe de criança com deficiência não para. São consultas, terapias, escola, remédio, deslocamento — e no meio de tudo isso, a conta que não fecha no fim do mês. Muitas vezes ela precisa reduzir o trabalho, ou parar de trabalhar, pra dar conta.</p>

<p>E o medo de pedir ajuda, ou a vergonha de não saber por onde começar, faz muita mãe carregar esse peso sozinha — sem saber que existe um benefício pensado exatamente pra essa situação.</p>

<p><strong>Neste artigo eu explico, sem juridiquês, o que é o BPC para criança com deficiência, quem tem direito e como comprovar.</strong></p>

<h2>O que é o BPC (e por que não é aposentadoria)</h2>

<p>Você já deve ter ouvido falar em aposentadoria por invalidez. O BPC não é isso.</p>

<p>Aposentadoria exige que a pessoa tenha contribuído com o INSS. O BPC é o contrário: é assistência social — e a criança <strong>NÃO PRECISA TER CONTRIBUÍDO COM NADA</strong> pra ter direito.</p>

<p>O nome técnico é Benefício de Prestação Continuada, previsto na LOAS (Lei Orgânica da Assistência Social). Na prática, ele existe pra garantir que uma família de baixa renda com uma criança com deficiência tenha, pelo menos, uma renda mínima garantida todo mês.</p>

<h2>Quando seu filho tem direito</h2>

<p>Pra ter direito ao BPC, dois requisitos precisam estar presentes ao mesmo tempo:</p>

<h3>1. Deficiência de longo prazo</h3>

<p>Não precisa ser uma deficiência "grave" ou "visível". A lei considera deficiência de longo prazo qualquer impedimento físico, mental, intelectual ou sensorial que dure pelo menos 2 anos e que, em contato com as barreiras do dia a dia, dificulte a participação plena da criança na vida em sociedade — na escola, no brincar, na convivência.</p>

<p>Autismo, síndrome de Down, paralisia cerebral, deficiência intelectual, doenças raras, TDAH severo com laudo — tudo isso pode se enquadrar, dependendo da avaliação.</p>

<h3>2. Renda baixa</h3>

<p>A renda de todas as pessoas que moram na mesma casa, somada e dividida pelo número de moradores, precisa ser de até 1/4 do salário mínimo por pessoa — em 2026, isso é <strong>R$ 405,25 por pessoa</strong>.</p>

<div class="callout-box">
<h4><i class="fa-solid fa-lightbulb"></i> E se a renda passar um pouco disso?</h4>
<p>Ainda assim vale a pena avaliar o caso. Existem formas de comprovar que a família não tem condições de sustentar a criança mesmo com renda um pouco acima do limite — a Justiça já reconhece isso em muitos casos.</p>
</div>

<h2>O que a família recebe</h2>

<p>O BPC paga <strong>1 salário mínimo por mês — R$ 1.621,00 em 2026</strong> — direto pra família, enquanto durar a deficiência e a condição de baixa renda. Não tem 13º salário. E não pode ser somado a outro benefício da Previdência (como pensão ou aposentadoria de outro membro da família) — mas não atrapalha o direito à saúde, então o tratamento da criança continua garantido do mesmo jeito.</p>

<h2>Como provar (essa é a parte que mais importa)</h2>

<p>É aqui que a maioria das famílias desiste — e eu não quero que você desista.</p>

<p>O INSS não aceita só um laudo do médico. Ele exige uma <strong>avaliação biopsicossocial</strong>: uma perícia feita por um médico do INSS e, depois, por um assistente social, que analisa não só o diagnóstico, mas como a deficiência afeta a vida da criança no dia a dia — na escola, em casa, na convivência.</p>

<p>Por isso, quanto mais documentado estiver o dia a dia da criança, mais forte fica o pedido:</p>

<div class="callout-box">
<h4><i class="fa-solid fa-lightbulb"></i> Documentos que fazem diferença</h4>
<p>Laudos médicos detalhados (não só a receita), relatórios de terapeutas (fono, terapia ocupacional, psicólogo), relatório da escola sobre as dificuldades observadas, receituários e comprovantes de tratamento contínuo, e o CadÚnico da família atualizado.</p>
</div>

<p>Se o INSS negar na avaliação — o que acontece com frequência, principalmente quando a perícia é rápida e não capta toda a rotina da criança —, ainda existe o caminho de recorrer administrativamente ou entrar com uma ação na Justiça, levando essa mesma documentação reforçada.</p>

<h2>Um caso que ilustra bem isso</h2>

<p>Recentemente atendi uma mãe que já tinha ido duas vezes ao INSS sozinha e voltado com o pedido negado. Ela achava que não tinha mais o que fazer. Quando reunimos os relatórios da escola, da terapia ocupacional e organizamos tudo antes da nova perícia, o resultado foi diferente — o benefício foi concedido. A diferença não foi o diagnóstico do filho dela, que já existia desde o início. Foi a forma como a rotina dele foi documentada e apresentada.</p>

<h2>O que fazer hoje</h2>

<p>Não espera a situação apertar mais pra começar. Comece assim:</p>

<ul>
<li>Confirme se o CadÚnico da família está atualizado — isso é pré-requisito pro pedido.</li>
<li>Separe os laudos e relatórios que você já tem, mesmo que estejam espalhados.</li>
<li>Peça pra escola e pros terapeutas um relatório simples sobre as dificuldades do dia a dia da criança.</li>
</ul>

<p>Isso já coloca você muito à frente de quem só descobre o que precisa na hora da perícia.</p>

<h2>Perguntas frequentes</h2>

<h3>Preciso ter carteira assinada pra pedir o BPC do meu filho?</h3>
<p>Não. O BPC não tem relação com carteira assinada, nem da criança, nem dos pais. O que importa é a renda da família e a deficiência da criança.</p>

<h3>Posso pedir se meu filho ainda não tem diagnóstico fechado?</h3>
<p>É mais difícil, mas vale conversar com um advogado antes de desistir — às vezes já existe documentação suficiente pra iniciar o processo enquanto o diagnóstico é aprofundado.</p>

<h3>Se o INSS negar, acabou?</h3>
<p>Não. Dá pra recorrer administrativamente ou entrar com ação na Justiça — e muitos pedidos negados no INSS são revertidos depois, com a documentação certa.</p>
"""

SLIDES = [
    "A rotina do seu filho pesa no bolso todo mês — e você nem sabe que existe um benefício pra isso.",
    "O BPC paga 1 salário mínimo por mês pra família de criança com deficiência. Não precisa ter contribuído com o INSS.",
    "Direito se: a renda por pessoa da casa for até R$ 405,25, e a deficiência durar pelo menos 2 anos.",
    "Autismo, Down, paralisia cerebral, deficiência intelectual, TDAH severo — cada caso é avaliado, mas muitos têm direito.",
    "Como provar? Reúna laudos, relatórios da escola e da terapia. Isso decide o pedido. Me chama, eu te ajudo a organizar tudo.",
]

IDENTIDADE_VISUAL = {
    "cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"},
}

OUT_DIR = Path(__file__).parent / "_teste_bpc_output"


async def main():
    OUT_DIR.mkdir(exist_ok=True)

    html = renderizar_artigo_html(
        titulo=TITULO,
        meta_description=META_DESCRIPTION,
        categoria=CATEGORIA,
        resumo=RESUMO,
        corpo_html=CORPO_HTML,
        slug=SLUG,
        data_publicacao=date.today(),
    )
    (OUT_DIR / "artigo.html").write_text(html, encoding="utf-8")
    print(f"Artigo salvo em {OUT_DIR / 'artigo.html'}")

    for i, texto in enumerate(SLIDES):
        caminho = OUT_DIR / f"carrossel-slide-{i + 1}.png"
        await renderizar_slide(
            texto=texto,
            indice=i,
            total=len(SLIDES),
            identidade_visual=IDENTIDADE_VISUAL,
            caminho_saida=str(caminho),
        )
        print(f"Slide {i + 1} salvo em {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
