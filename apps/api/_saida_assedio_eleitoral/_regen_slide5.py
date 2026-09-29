import asyncio
from pathlib import Path
from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

caminho_saida = str(Path("_saida_assedio_eleitoral/carrossel_slides/slide-5.png").resolve()).replace("\\", "/")
foto_path = str(Path("_saida_assedio_eleitoral/foto-slide5-leticia-votando.png").resolve()).replace("\\", "/")


async def main():
    await renderizar_slide(
        texto="Seu voto é livre e secreto. Ninguém no seu trabalho tem o direito de tentar mudar isso.",
        indice=4,
        total=5,
        identidade_visual=IDENTIDADE,
        caminho_saida=caminho_saida,
        foto_path=foto_path,
        foto_posicao="center top",
    )
    print("ok")


if __name__ == "__main__":
    asyncio.run(main())
