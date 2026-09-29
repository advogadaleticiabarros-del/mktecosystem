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
        "texto": "Seu cachorro também pode ter guarda compartilhada agora. A lei mudou em 2026.",
        "foto": BANCO / "5482156.jpg",
        "posicao": "center 20%",
    },
    {
        "texto": "Se o pet viveu a maior parte da vida durante o casamento, a lei já considera ele propriedade comum dos dois.",
        "foto": BANCO / "7788910.jpg",
        "posicao": "center top",
    },
    {
        "texto": "Sem acordo entre o casal, o juiz define a guarda compartilhada como regra, e as despesas (veterinário, ração, remédio) são divididas igualmente.",
        "foto": BANCO / "6235049.jpg",
        "posicao": "center",
    },
    {
        "texto": "Exceção: se houver histórico de violência doméstica ou maus-tratos ao animal, a guarda compartilhada não é concedida.",
        "foto": BANCO / "10963815.jpg",
        "posicao": "center",
    },
    {
        "texto": "O processo da guarda do pet corre junto com o divórcio, na Vara de Família. Você não precisa abrir uma ação separada.",
        "foto": FOTO_LETICIA,
        "posicao": "center top",
    },
]


async def main():
    out_dir = Path("C:/Users/prosy/Desktop/Editorial/2026-09/30-09-2026/carrossel")
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
