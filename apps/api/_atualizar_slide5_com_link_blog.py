import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide
from _gerar_carrosseis_calendario_agosto import CARROSSEIS, IDENTIDADE, FOTO_ADVOGADA_PADRAO

DIAS_COM_ARTIGO = [
    "17-08-gestante-aviso-previo",
    "19-08-gestante-descoberta-apos-rescisao",
    "21-08-gestante-distrato-sem-saber",
    "25-08-gestante-ambiente-insalubre",
    "27-08-gestante-tst-contrato-temporario",
    "31-08-gestante-volta-licenca",
]


async def main():
    out_root = Path(__file__).parent / "_saida_carrosseis_calendario_agosto"
    for nome in DIAS_COM_ARTIGO:
        slides = CARROSSEIS[nome]
        i = len(slides) - 1
        caminho = out_root / nome / f"slide-{i + 1}.png"
        await renderizar_slide(
            texto=slides[i],
            indice=i,
            total=len(slides),
            identidade_visual=IDENTIDADE,
            caminho_saida=str(caminho),
            foto_path=str(FOTO_ADVOGADA_PADRAO),
            foto_posicao="center top",
        )
        print(f"{nome} slide {i + 1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
