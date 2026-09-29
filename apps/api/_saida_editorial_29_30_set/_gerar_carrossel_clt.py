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
        "texto": "3 direitos que sua empresa espera que você nunca descubra.",
        "foto": BANCO / "7793993.jpg",
        "posicao": "center top",
    },
    {
        "texto": "Substituiu um colega de férias ou licença, mesmo por poucos dias? Você tem direito ao salário dele durante esse período.",
        "foto": BANCO / "7793993.jpg",
        "posicao": "center",
    },
    {
        "texto": "Trabalha digitando o dia todo? Tem direito a 10 minutos de pausa a cada 90 minutos, e isso conta como hora extra se a empresa não cumprir.",
        "foto": BANCO / "5185158.jpg",
        "posicao": "center",
    },
    {
        "texto": "Uniforme obrigatório estragou de uso normal? A empresa não pode descontar de você, só se provar dano proposital.",
        "foto": BANCO / "6223004.jpg",
        "posicao": "center",
    },
    {
        "texto": "Conhecer seus direitos não é exagero. É proteção pro seu bolso e pra sua saúde no trabalho.",
        "foto": FOTO_LETICIA,
        "posicao": "center top",
    },
]


async def main():
    out_dir = Path("C:/Users/prosy/Desktop/Editorial/2026-10/04-10-2026/carrossel")
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
