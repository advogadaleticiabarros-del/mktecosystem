import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_slide

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

SLIDES = [
    "⚖️ Feliz Dia da Advocacia.\n\nOu melhor: das 7 profissões.",
    "🔮 VIDENTE\n\nCliente: \"Doutora, mas eu vou ganhar, né?\"\n\nEu, tentando acessar o sistema do Tribunal… e também o futuro. 🔮",
    "🛋️ PSICÓLOGA\n\nA consulta jurídica:\n10% documentos. 20% estratégia. 70%:\n\n\"Doutora, deixa eu te contar desde o começo…\"\n\nE o começo foi em 2014. 😂",
    "🕵️ DETETIVE\n\nCliente: \"Eu não tenho nenhuma prova.\"\n\nCinco minutos depois: \"Só tenho uns prints, três áudios, duas testemunhas, um vídeo e a localização dele naquele dia.\"\n\n👀 PERFEITO. CONTINUE.",
    "🔍 CENTRAL DE DÚVIDAS 24H\n\n\"Doutora, é só uma perguntinha rápida…\"\n\nA perguntinha envolve 3 contratos, 2 processos, uma jurisprudência nova e começa com:\n\n\"hipoteticamente…\" 😂",
    "🏎️ PILOTO DE F1\n\nCliente: \"Doutora, não tem como dar uma aceleradinha no processo?\"\n\nClaro. Vou só entrar no fórum, pegar o processo e gritar:\n\nBOX! BOX! BOX! 🏎️💨",
    "🤝 CONSELHEIRA OFICIAL\n\n\"Doutora… juridicamente eu entendi.\"\n\"Mas se fosse a senhora... o que faria no meu lugar?\"\n\nE de repente a OAB virou também Conselho de Decisões da Vida. 😂",
    "No fim das contas, a gente é:\n⚖️🔮🕵️🛋️🏎️📚🤝\n\numa profissão… e sete funções extras. ❤️\n\nFeliz Dia da Advocacia a todas as colegas!\n\nMarque uma advogada que se reconhece em pelo menos 5 dessas. 😂",
]

CTA_FINAL = "❤️ Marque uma colega"


async def main():
    out_dir = Path(__file__).parent / "_saida_carrossel_dia_advocacia"
    out_dir.mkdir(exist_ok=True)
    for i, texto in enumerate(SLIDES):
        caminho = out_dir / f"slide-{i + 1}.png"
        await renderizar_slide(
            texto=texto,
            indice=i,
            total=len(SLIDES),
            identidade_visual=IDENTIDADE,
            caminho_saida=str(caminho),
            cta_texto=CTA_FINAL,
        )
        print(f"slide {i + 1} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
