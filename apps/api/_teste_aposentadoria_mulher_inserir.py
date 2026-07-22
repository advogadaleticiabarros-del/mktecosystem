import os

if "DATABASE_URL" not in os.environ:
    raise SystemExit(
        "Defina DATABASE_URL (postgresql+asyncpg://...) no ambiente antes de rodar este script."
    )

import asyncio
from datetime import date
from pathlib import Path

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant, TenantConfig
from app.services.render_artigo_blog import renderizar_artigo_html
from app.services.render_criativo import renderizar_slide

TITULO = "Aposentadoria da mulher em 2026: a idade mínima subiu de novo, veja se você já pode pedir"
META_DESCRIPTION = "A idade mínima da aposentadoria por tempo de contribuição da mulher mudou outra vez em 2026. Veja se você se encaixa na regra de transição e quanto tempo falta."
RESUMO = "Em 2026 a mulher precisa ter 59 anos e 6 meses, além de 30 anos de contribuição, pra se aposentar pela regra de transição da idade mínima progressiva. Veja quem tem direito e como é calculado o valor."
CATEGORIA = "Previdenciário"
SLUG = "aposentadoria-mulher-2026-idade-minima-regra-transicao"
DATA_ALVO = date(2026, 7, 24)
HORARIO_ALVO = "19:00"

CORPO_HTML = """
<p>Você trabalha desde nova. Contribuiu com o INSS a vida inteira, contando os anos, esperando o dia de parar. E quando finalmente ia se aposentar, veio a notícia: a idade mudou de novo.</p>

<p>Isso não é sua imaginação. E não é a primeira vez que isso acontece com você.</p>

<p><strong>Neste artigo eu explico, sem juridiquês, o que mudou na aposentadoria da mulher em 2026, quem já pode pedir e como é calculado o valor que você vai receber.</strong></p>

<h2>Por que a idade não para de subir</h2>

<p>A aposentadoria por tempo de contribuição, do jeito que existia antes, acabou em 2019, com a reforma da Previdência. Quem já contribuía com o INSS antes de 13 de novembro de 2019 não perdeu o direito, mas passou a se aposentar por uma regra de transição — e uma delas é a da idade mínima progressiva.</p>

<p>O nome já explica o funcionamento. O tempo de contribuição não muda, continua em 30 anos pra mulher. Mas a idade mínima sobe 6 meses a cada 1º de janeiro, até estabilizar. Em 2026, a idade mínima da mulher chegou a <strong>59 anos e 6 meses</strong>.</p>

<h2>Quando você tem direito</h2>

<p>Pra se aposentar por essa regra em 2026, você precisa reunir três coisas ao mesmo tempo:</p>

<h3>1. Ter contribuído com o INSS antes de 13 de novembro de 2019</h3>
<p>Se você começou a trabalhar com carteira assinada ou a contribuir como autônoma antes dessa data, esse primeiro requisito já está resolvido.</p>

<h3>2. Ter 30 anos de contribuição</h3>
<p>Não precisam ser 30 anos seguidos, nem no mesmo emprego. Períodos como empregada, autônoma, contribuinte individual — tudo isso soma.</p>

<h3>3. Ter 59 anos e 6 meses de idade em 2026</h3>
<p>Se você já tem os 30 anos de contribuição e completa essa idade este ano, a partir da data do aniversário você já pode dar entrada no pedido.</p>

<h2>O que você recebe</h2>

<p>Aqui está o ponto que mais gera confusão — e é justamente o que decide se vale a pena esperar mais um pouco ou pedir agora.</p>

<p>O valor não é um salário mínimo fixo, nem a média dos seus últimos salários. É calculado pela média de todos os seus salários de contribuição desde julho de 1994, incluindo os mais baixos.</p>

<p>Sobre essa média, você recebe 60%, mais 2% pra cada ano de contribuição que passar de 15 anos. Ou seja, quanto mais tempo você contribuiu além do mínimo, maior o percentual da sua aposentadoria.</p>

<div class="callout-box">
<h4><i class="fa-solid fa-lightbulb"></i> Esperar compensa?</h4>
<p>Em alguns casos, esperar um pouco mais pra somar tempo de contribuição pode aumentar bastante o valor final. Em outros, esperar não muda nada e só atrasa o benefício. Isso precisa ser calculado caso a caso, no seu histórico real.</p>
</div>

<h2>Como provar (essa é a parte que mais importa)</h2>

<p>De nada adianta ter direito na teoria se o seu tempo de contribuição não está certo no sistema do INSS.</p>

<p>É muito comum aparecer buraco no Cadastro Nacional de Informações Sociais, o CNIS, principalmente de quem trabalhou muito tempo atrás, mudou de emprego várias vezes ou teve período como autônoma sem guia paga corretamente.</p>

<p>Se o seu CNIS tiver um período sem registro, isso pode te tirar da regra de transição sem você nem saber o motivo. Por isso, antes de dar entrada, vale reunir carteira de trabalho antiga, contracheques, guias de recolhimento como autônoma e qualquer documento que comprove os anos que faltam no sistema.</p>

<h2>O que fazer hoje</h2>

<p>Não espera a data do pedido chegar pra descobrir se tem algo errado no seu tempo de contribuição.</p>

<ul>
<li>Acesse o Meu INSS e confira o seu CNIS agora.</li>
<li>Separe carteira de trabalho, contracheques e guias antigas, principalmente de períodos mais distantes.</li>
<li>Se encontrar algum período sem registro, comece a reunir a prova desde já — isso evita atraso na hora do pedido.</li>
</ul>

<h2>Perguntas frequentes</h2>

<h3>A idade mínima vai continuar subindo?</h3>
<p>Sim, a regra prevê aumento de 6 meses por ano até estabilizar. Quem ainda não chegou na idade precisa acompanhar o próprio caso ano a ano.</p>

<h3>Vale mais a pena esperar pra me aposentar com um valor maior?</h3>
<p>Depende do seu histórico de contribuição. Em alguns casos sim, em outros o valor não muda o suficiente pra compensar a espera. Isso precisa ser calculado no seu caso.</p>

<h3>E se o INSS negar meu pedido?</h3>
<p>Dá pra recorrer administrativamente ou entrar com ação na Justiça, principalmente quando a negativa é por erro no tempo de contribuição que já foi corrigido depois.</p>

<p>Se você já está perto dessa idade, ou já passou dela e nunca conferiu seu tempo de contribuição, me conta a sua situação. Estamos aqui para ajudar.</p>
"""

SLIDES = [
    "Você contribuiu a vida inteira esperando o dia de se aposentar. E a idade mudou de novo.",
    "Em 2026, a idade mínima da mulher na regra de transição chegou a 59 anos e 6 meses, com 30 anos de contribuição.",
    "Só vale pra quem já contribuía com o INSS antes de 13 de novembro de 2019.",
    "O valor não é fixo. É a média de todos os seus salários desde 1994, mais um percentual que cresce com o tempo de contribuição.",
    "Antes de pedir, confira o CNIS no Meu INSS. Um buraco no cadastro pode te tirar da regra sem você saber. Me chama e eu te ajudo a conferir.",
]

LEGENDA = (
    "Você contribuiu a vida inteira esperando o dia de se aposentar. E descobriu que a idade mudou de novo.\n\n"
    "Em 2026, a idade mínima da mulher na regra de transição chegou a 59 anos e 6 meses, com 30 anos de contribuição.\n\n"
    "📌 Só vale pra quem já contribuía com o INSS antes de 13 de novembro de 2019.\n"
    "📌 O valor não é fixo, é calculado pela média de todos os seus salários desde 1994.\n"
    "📌 Um buraco no seu CNIS pode te tirar da regra sem você nem saber o motivo.\n\n"
    "Já conferiu seu tempo de contribuição no Meu INSS? Me conta a sua situação, estamos aqui para ajudar.\n\n"
    "#aposentadoria #direitoprevidenciario #inss #aposentadoriadamulher #direitosdamulher"
)

OUT_DIR = Path(__file__).parent / "_teste_aposentadoria_mulher_output"


async def main():
    OUT_DIR.mkdir(exist_ok=True)

    async with SessionLocal() as db:
        tenant = (await db.execute(select(Tenant))).scalars().first()
        if tenant is None:
            raise SystemExit("Nenhum tenant encontrado no banco.")

        tenant_config = (
            await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == tenant.id))
        ).scalar_one_or_none()
        identidade_visual = tenant_config.identidade_visual if tenant_config else {}

        pauta = Pauta(
            tenant_id=tenant.id,
            titulo="Aposentadoria da mulher: nova idade mínima em 2026",
            angulo="direitos",
            area="Previdenciário",
            origem="manual",
            fonte="Claude (teste assistido)",
            relevante_para_conteudo=True,
            status="aprovada",
        )
        db.add(pauta)
        await db.flush()

        artigo = ContentPiece(
            tenant_id=tenant.id,
            pauta_id=pauta.id,
            tipo="artigo",
            corpo={
                "titulo": TITULO,
                "html": CORPO_HTML,
                "meta_description": META_DESCRIPTION,
                "resumo": RESUMO,
            },
            status="aprovado",
            versao=1,
        )
        db.add(artigo)

        carrossel = ContentPiece(
            tenant_id=tenant.id,
            pauta_id=pauta.id,
            tipo="carrossel",
            corpo={"slides": SLIDES},
            status="aprovado",
            versao=1,
        )
        db.add(carrossel)

        legenda = ContentPiece(
            tenant_id=tenant.id,
            pauta_id=pauta.id,
            tipo="legenda",
            corpo={"texto": LEGENDA},
            status="aprovado",
            versao=1,
        )
        db.add(legenda)

        await db.flush()

        agendamento_blog = ScheduledPost(
            tenant_id=tenant.id,
            content_piece_id=artigo.id,
            titulo=pauta.titulo,
            canal="blog",
            formato="artigo",
            data_agendada=DATA_ALVO,
            horario=HORARIO_ALVO,
            status="pronto",
        )
        db.add(agendamento_blog)

        agendamento_ig = ScheduledPost(
            tenant_id=tenant.id,
            content_piece_id=None,
            titulo=f"{pauta.titulo} (carrossel — Instagram/Facebook, publicação manual)",
            canal="instagram",
            formato="carrossel",
            data_agendada=DATA_ALVO,
            horario=HORARIO_ALVO,
            status="pronto",
        )
        db.add(agendamento_ig)

        await db.commit()

        print(f"Pauta: {pauta.id}")
        print(f"ContentPiece artigo: {artigo.id}")
        print(f"ContentPiece carrossel: {carrossel.id}")
        print(f"ContentPiece legenda: {legenda.id}")
        print(f"ScheduledPost blog: {agendamento_blog.id} -> {agendamento_blog.data_agendada} {agendamento_blog.horario}")
        print(f"ScheduledPost instagram: {agendamento_ig.id} -> {agendamento_ig.data_agendada} {agendamento_ig.horario}")

    html = renderizar_artigo_html(
        titulo=TITULO,
        meta_description=META_DESCRIPTION,
        categoria=CATEGORIA,
        resumo=RESUMO,
        corpo_html=CORPO_HTML,
        slug=SLUG,
        data_publicacao=DATA_ALVO,
    )
    (OUT_DIR / "artigo.html").write_text(html, encoding="utf-8")
    print(f"Preview do artigo salvo em {OUT_DIR / 'artigo.html'}")

    for i, texto in enumerate(SLIDES):
        caminho = OUT_DIR / f"carrossel-slide-{i + 1}.png"
        await renderizar_slide(
            texto=texto,
            indice=i,
            total=len(SLIDES),
            identidade_visual=identidade_visual,
            caminho_saida=str(caminho),
        )
        print(f"Slide {i + 1} salvo em {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
