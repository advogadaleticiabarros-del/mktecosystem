import asyncio
from pathlib import Path
from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

caminho_saida = str(Path("_saida_assedio_eleitoral/carrossel_slides/slide-3.png").resolve()).replace("\\", "/")
foto_path = str(Path("_saida_assedio_eleitoral/foto-slide3-chatgpt.png").resolve()).replace("\\", "/")


async def main():
    await renderizar_slide(
        texto="Desde a Resolução do TSE de 2026, a simples propaganda política dentro da empresa já configura infração, nem precisa provar ameaça direta.",
        indice=2,
        total=5,
        identidade_visual=IDENTIDADE,
        caminho_saida=caminho_saida,
        foto_path=foto_path,
        foto_posicao="center 30%",
    )
    print("ok")


if __name__ == "__main__":
    asyncio.run(main())
