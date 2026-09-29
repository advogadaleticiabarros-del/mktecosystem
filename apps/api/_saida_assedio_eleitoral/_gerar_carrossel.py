import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

BANCO = Path("_saida_assedio_eleitoral")
FOTO_LETICIA = Path(
    "C:/Users/prosy/Desktop/PROJETOS/ecosystemmkt/BANCO IMAGENS/Advogada/"
    "Gemini_Generated_Image_rrg4ylrrg4ylrrg4.png"
)

SLIDES = [
    {
        "texto": "Seu chefe está fazendo campanha política pra você. Isso tem nome: assédio eleitoral.",
        "foto": BANCO / "8297215.jpg",
        "posicao": "center top",
    },
    {
        "texto": "Comentário sobre 'em quem todo mundo devia votar' não é opinião. É pressão sobre você, e a lei mudou em 2026 pra isso ficar mais claro.",
        "foto": BANCO / "6632498.jpg",
        "posicao": "center",
    },
    {
        "texto": "Desde a Resolução do TSE de 2026, a simples propaganda política dentro da empresa já configura infração, nem precisa provar ameaça direta.",
        "foto": BANCO / "4088463.jpg",
        "posicao": "center",
    },
    {
        "texto": "Isso pode gerar rescisão indireta: você sai como se tivesse sido demitida, com todos os seus direitos garantidos.",
        "foto": BANCO / "8560661.jpg",
        "posicao": "center",
    },
    {
        "texto": "Seu voto é livre e secreto. Ninguém no seu trabalho tem o direito de tentar mudar isso.",
        "foto": FOTO_LETICIA,
        "posicao": "center top",
    },
]


async def main():
    out_dir = BANCO / "carrossel_slides"
    out_dir.mkdir(exist_ok=True)
    total = len(SLIDES)
    for i, s in enumerate(SLIDES):
        caminho = out_dir / f"slide-{i+1}.png"
        await renderizar_slide(
            texto=s["texto"],
            indice=i,
            total=total,
            identidade_visual=IDENTIDADE,
            caminho_saida=str(caminho),
            foto_path=str(s["foto"]),
            foto_posicao=s["posicao"],
        )
        print(f"slide {i+1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
