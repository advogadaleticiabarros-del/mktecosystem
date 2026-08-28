import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
BANCO = Path(r"C:\Users\prosy\Desktop\LETÍCIA\banco de imagens")

FOTOS = [
    str(BANCO / "SOGIMIG.jpg"),
    str(BANCO / "mulher-gravida-em-ambiente-de-trabalho-moderno-768x512.jpg"),
    str(BANCO / "gravida-trabalhando-diante-do-computador-e-um-tabu-gigante-no-mercado-de-trabalho-escreveu-uma-mulher-que-foi-contratada-durante-a-gestacao-1630792534194_v2_3x4.jpg"),
    str(BANCO / "gravida.jpg"),
    str(Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\Advogada\ChatGPT Image 24_07_2026, 20_25_54.png")),
]

SLIDES = [
    "Gestante: cuidado antes de assinar um pedido de demissão.",
    "Você tem garantia de emprego durante a gravidez. Por isso, o pedido de demissão só é válido com a assistência do sindicato ou da autoridade competente, conforme o artigo 500 da CLT.",
    "Se essa assistência não aconteceu, o pedido pode ser questionado na Justiça. Mas isso não quer dizer que a anulação é automática.",
    "Cada caso é analisado de forma individual: quando a gravidez começou, como o desligamento aconteceu, o que foi assinado, se houve pressão, e o que já foi pago.",
    "Antes de assinar qualquer documento, entenda seus direitos e as consequências da decisão. Procure uma advogada de confiança para analisar o seu caso.",
]


async def main():
    out_dir = Path(__file__).parent / "_saida_carrossel_gestante"
    out_dir.mkdir(exist_ok=True)
    for i, texto in enumerate(SLIDES):
        caminho = out_dir / f"slide-{i + 1}.png"
        await renderizar_slide(
            texto=texto,
            indice=i,
            total=len(SLIDES),
            identidade_visual=IDENTIDADE,
            caminho_saida=str(caminho),
            foto_path=FOTOS[i],
            foto_posicao="center top",
        )
        print(f"slide {i + 1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
