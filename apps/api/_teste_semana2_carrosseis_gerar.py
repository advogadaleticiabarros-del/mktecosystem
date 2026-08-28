import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
BANCO = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS")
BANCO_MAE = BANCO / "mae e filhos"
BANCO_GESTANTE = BANCO / "GESTANTE CLT"

CARROSSEIS = {
    "trabalhista-vale-transporte-refeicao": {
        "fotos": [str(BANCO_GESTANTE / "8f5eafe589fb46527e807f3a01f18136.jpg"), None, None, None, None],
        "slides": [
            "Vale-transporte e vale-refeição são obrigatórios? A resposta não é a mesma pros dois.",
            "O vale-transporte é obrigatório por lei, desde que você peça por escrito à empresa. Ela não pode se recusar.",
            "Já o vale-refeição ou vale-alimentação não tem lei geral obrigando. Só é devido se estiver previsto em convenção coletiva, acordo ou contrato.",
            "Empresa que já paga e decide cortar sem negociação pode estar reduzindo um direito adquirido, o que é proibido.",
            "Confira a convenção coletiva da sua categoria. Ela costuma definir esse benefício, mesmo quando a lei geral não obriga.",
        ],
        "foto_posicao": "center top",
    },
    "previdenciario-auxilio-doenca-negado": {
        "fotos": [str(BANCO_GESTANTE / "WhatsApp Image 2026-07-22 at 13.04.31.jpeg"), None, None, None, None],
        "slides": [
            "Auxílio-doença negado pelo INSS? Isso não significa que você não tem direito.",
            "A negativa mais comum é a perícia entender que você está apto pro trabalho, mesmo com atestado médico dizendo o contrário.",
            "Você tem 30 dias pra recorrer administrativamente, direto pelo Meu INSS, juntando laudos e exames que reforcem o diagnóstico.",
            "Se o recurso administrativo também for negado, ainda existe o caminho judicial, com nova perícia feita por médico da Justiça.",
            "Reúna todos os exames, laudos e receituários antes de recorrer. Isso muda o resultado da nova perícia.",
        ],
        "foto_posicao": "center top",
    },
    "familia-revisao-pensao": {
        "fotos": [
            str(BANCO_MAE / "pexels-ekaterina-bolovtsova-4866874.jpg"),
            str(BANCO_MAE / "pexels-ekaterina-bolovtsova-4867895.jpg"),
            str(BANCO_MAE / "pexels-ekaterina-bolovtsova-4866887.jpg"),
            str(BANCO_MAE / "pexels-ekaterina-bolovtsova-4867985.jpg"),
            str(BANCO_MAE / "pexels-helenalopes-4409245.jpg"),
        ],
        "slides": [
            "Meu ex aumentou o salário. Posso pedir revisão do valor da pensão?",
            "Sim. A pensão não é fixa pra sempre, ela pode ser revisada quando a capacidade financeira de quem paga muda.",
            "Aumento de salário, novo emprego ou uma herança podem justificar o pedido de revisão pra cima.",
            "O contrário também vale: quem paga pode pedir redução se perder renda de forma comprovada.",
            "Reúna comprovantes do novo padrão de vida dele, além da renda formal. Isso ajuda o pedido.",
        ],
        "foto_posicao": "center top",
    },
}


async def main():
    for nome, dados in CARROSSEIS.items():
        out_dir = Path(__file__).parent / f"_teste_semana2_{nome}_output"
        out_dir.mkdir(exist_ok=True)
        slides = dados["slides"]
        for i, texto in enumerate(slides):
            foto_path = dados["fotos"][i]
            caminho = out_dir / f"carrossel-slide-{i + 1}.png"
            await renderizar_slide(
                texto=texto,
                indice=i,
                total=len(slides),
                identidade_visual=IDENTIDADE,
                caminho_saida=str(caminho),
                foto_path=foto_path,
                foto_posicao=dados["foto_posicao"],
            )
            print(f"{nome} slide {i + 1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
