import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
BANCO_IDOSOS = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\IDOSAS APOSENTADORIA E BEM ESTAR")

CARROSSEIS = {
    "familia-mudanca-cidade": {
        "fotos": [None] * 5,
        "slides": [
            "Posso mudar de cidade com meu filho sem autorização do pai? Depende de como está a guarda e da distância. Não é uma decisão que você toma sozinha na maioria dos casos.",
            "Na guarda compartilhada, mudar de cidade sem prejudicar a convivência do outro pai exige concordância dele ou autorização judicial.",
            "Mesmo com guarda só sua, mudanças que dificultem o convívio podem ser questionadas na Justiça.",
            "Mudar sem avisar pode ser visto como alienação parental e prejudicar seu pedido mais adiante.",
            "Antes de fazer as malas, formalize: acordo por escrito ou autorização judicial evitam dor de cabeça depois.",
        ],
    },
    "previdenciario-desconto-inss": {
        "fotos": [
            "pexels-lis-163347222-36792488.jpg",
            "pexels-mike-art-visual-creator-photography-and-video-2159421235-36477131.jpg",
            "pexels-tkirkgoz-19331189.jpg",
            "pexels-isabela-catao-257775660-36810446.jpg",
            "pexels-lis-163347222-36792499.jpg",
        ],
        "slides": [
            "Associações descontaram uma mensalidade do seu benefício do INSS sem pedir sua autorização. Mais de 4 milhões de pessoas foram afetadas.",
            "O prazo administrativo pra contestar terminou em 20 de junho. Mas isso não significa que acabou o seu direito de reaver o dinheiro.",
            "Você ainda pode aderir ao acordo de ressarcimento ou entrar com ação judicial, inclusive com honorários pagos pelo próprio INSS em alguns casos.",
            "Olhe seu extrato no Meu INSS. Procure descontos de associações ou entidades que você não reconhece.",
            "Reaver o que é seu ainda é possível. Quanto antes você agir, mais rápido recupera o valor.",
        ],
    },
    "consumidor-produto-defeito": {
        "fotos": [None] * 5,
        "slides": [
            "Comprou um produto com defeito? A loja não pode simplesmente dizer 'não trocamos'. A lei garante seus direitos.",
            "Você tem 30 dias pra produtos não duráveis e 90 dias pra duráveis, contados da descoberta do defeito.",
            "A loja tem até 30 dias pra consertar. Se não resolver, você escolhe: troca, devolução do dinheiro ou abatimento no preço.",
            "Defeito que só apareceu depois da compra também conta. O prazo começa a contar da data em que você percebeu o problema.",
            "Guarde a nota fiscal e o print da conversa com a loja. Sem prova, fica mais difícil exigir seus direitos.",
        ],
    },
    "trabalhista-assedio-moral": {
        "fotos": [None] * 5,
        "slides": [
            "Humilhação no trabalho não é 'estilo de liderança'. Chamar atenção na frente de todos, cobrar de forma humilhante, isolar. Isso é assédio moral.",
            "Não é um dia ruim isolado. Assédio moral é um padrão que se repete e mina sua dignidade aos poucos.",
            "A empresa também é responsável. Mesmo quando quem assedia é um colega ou chefe direto, ela responde por não agir.",
            "Mensagens, e-mails, áudios e o relato de colegas que presenciaram ajudam a provar o assédio.",
            "O que você sente tem nome jurídico. E pode gerar direito a indenização por dano moral.",
        ],
    },
}


async def main():
    for nome, dados in CARROSSEIS.items():
        out_dir = Path(__file__).parent / f"_teste_semana_{nome}_output"
        out_dir.mkdir(exist_ok=True)
        slides = dados["slides"]
        for i, texto in enumerate(slides):
            foto = dados["fotos"][i]
            foto_path = str(BANCO_IDOSOS / foto) if foto else None
            caminho = out_dir / f"carrossel-slide-{i + 1}.png"
            await renderizar_slide(
                texto=texto,
                indice=i,
                total=len(slides),
                identidade_visual=IDENTIDADE,
                caminho_saida=str(caminho),
                foto_path=foto_path,
                foto_posicao="center top",
            )
            print(f"{nome} slide {i + 1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
