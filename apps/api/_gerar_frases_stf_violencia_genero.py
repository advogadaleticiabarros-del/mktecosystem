import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_frase_impacto

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

FRASES = [
    ("01-familia-violencia-fora-de-casa", 'Violência não precisa acontecer dentro de casa<br>pra ser <em>violência doméstica aos olhos da lei</em>.'),
    ("02-familia-protecao-de-estranho", 'Você acha que só quem convive com você pode te agredir.<br>A lei te protege <em>até de um estranho</em>.'),
    ("03-familia-medida-protetiva-toda-mulher", 'Medida protetiva não é só<br>para quem tem relação com o agressor.<br>É para <em>toda mulher em situação de violência de gênero</em>.'),
]


async def main():
    out_dir = Path(__file__).parent / "_saida_frases_stf_violencia_genero"
    out_dir.mkdir(exist_ok=True)
    for nome, frase_html in FRASES:
        caminho = out_dir / f"frase-{nome}.png"
        await renderizar_frase_impacto(
            frase_html=frase_html,
            identidade_visual=IDENTIDADE,
            caminho_saida=str(caminho),
        )
        print(f"{nome} -> {caminho}")


if __name__ == "__main__":
    asyncio.run(main())
