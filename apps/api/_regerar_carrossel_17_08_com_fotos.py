import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide
from _gerar_carrosseis_calendario_agosto import CARROSSEIS, IDENTIDADE

BANCO = Path(r"C:\Users\prosy\Desktop\PROJETOS\ecosystemmkt\BANCO IMAGENS\gesntante novas")

FOTOS = [
    BANCO / "663c8361bcf7744dc367997058381195.jpg",
    BANCO / "1dc69ebea434ef847baa5397b2d7a0e6.jpg",
    BANCO / "3c7f7df378f843174943eb15bc2fe810.jpg",
    BANCO / "747e38a8ff5bb09d2b9fb964820df5b1.jpg",
    BANCO / "71765fefd45736692335cf26f0c24d91.jpg",
]


async def main():
    nome = "17-08-gestante-aviso-previo"
    slides = CARROSSEIS[nome]
    out_dir = Path(__file__).parent / "_saida_carrosseis_calendario_agosto" / nome
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, texto in enumerate(slides):
        caminho = out_dir / f"slide-{i + 1}.png"
        await renderizar_slide(
            texto=texto,
            indice=i,
            total=len(slides),
            identidade_visual=IDENTIDADE,
            caminho_saida=str(caminho),
            foto_path=str(FOTOS[i]),
            foto_posicao="center top",
        )
        print(f"slide {i + 1} -> {caminho} (foto: {FOTOS[i].name})")


if __name__ == "__main__":
    asyncio.run(main())
