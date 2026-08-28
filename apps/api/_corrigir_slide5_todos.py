import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide
from _gerar_carrosseis_calendario_agosto import CARROSSEIS, IDENTIDADE, FOTO_ADVOGADA_PADRAO


async def main():
    out_root = Path(__file__).parent / "_saida_carrosseis_calendario_agosto"
    for nome, slides in CARROSSEIS.items():
        i = len(slides) - 1
        texto = slides[i]
        caminho = out_root / nome / f"slide-{i + 1}.png"
        await renderizar_slide(
            texto=texto,
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
