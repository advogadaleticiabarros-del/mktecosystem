import asyncio
from pathlib import Path
from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

BANCO = Path("_saida_editorial_29_30_set")
FOTO_LETICIA = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/Advogada/"
    "Gemini_Generated_Image_rrg4ylrrg4ylrrg4.png"
)

SLIDES = [
    {
        "texto": "Pai ausente não é só mágoa. Desde 2025, pode virar indenização.",
        "foto": BANCO / "17024734.jpg",
        "posicao": "center top",
    },
    {
        "texto": "A Lei 15.240/2025 reconhece o abandono afetivo de crianças e adolescentes como ato ilícito civil, sujeito a reparação.",
        "foto": BANCO / "11082888.jpg",
        "posicao": "center",
    },
    {
        "texto": "Não é só sobre pensão. É sobre presença, contato, apoio nas decisões da vida do filho, o que a lei chama de assistência afetiva.",
        "foto": BANCO / "18094977.jpg",
        "posicao": "center",
    },
    {
        "texto": "A negligência afetiva sistemática pode gerar ação judicial e indenização por dano moral contra o pai ou mãe ausente.",
        "foto": BANCO / "6698319.jpg",
        "posicao": "center",
    },
    {
        "texto": "Amor não se obriga por lei. Mas presença e cuidado, quando negados de forma sistemática, agora têm consequência jurídica.",
        "foto": FOTO_LETICIA,
        "posicao": "center top",
    },
]


async def main():
    out_dir = Path("C:/Users/prosy/Desktop/Editorial/2026-10/02-10-2026/carrossel")
    total = len(SLIDES)
    for i, s in enumerate(SLIDES):
        caminho = str((out_dir / f"slide-{i+1}.png").resolve()).replace("\\", "/")
        foto_path = str(s["foto"].resolve()).replace("\\", "/")
        await renderizar_slide(
            texto=s["texto"],
            indice=i,
            total=total,
            identidade_visual=IDENTIDADE,
            caminho_saida=caminho,
            foto_path=foto_path,
            foto_posicao=s["posicao"],
        )
        print(f"slide {i+1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
