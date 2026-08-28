import asyncio
from pathlib import Path

from app.services.render_criativo import renderizar_frase_impacto

IDENTIDADE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

FRASES = [
    ("17-08-gestante-aviso-previo", 'Aviso prévio <em>não cancela</em><br>a estabilidade da grávida.'),
    ("18-08-familia-pensao-ex-conjuge", 'Pensão para genitor(a) não é regra.<br>É <em>exceção com prazo de validade</em>.'),
    ("19-08-gestante-descoberta-apos-rescisao", 'Descobrir a gravidez depois de já ter assinado<br><em>não apaga o seu direito</em>.'),
    ("20-08-familia-guarda-compartilhada", 'Guarda compartilhada não é dividir a semana ao meio.<br>É <em>dividir a responsabilidade</em>.'),
    ("21-08-gestante-distrato-sem-saber", 'Um acordo assinado sem saber da gravidez<br><em>não é definitivo</em>.'),
    ("24-08-familia-pensao-atrasada", 'Pensão atrasada não é "combinado entre vocês".<br>É <em>dívida que pode virar prisão</em>.'),
    ("25-08-gestante-ambiente-insalubre", 'Ambiente insalubre não vira "normal"<br>só porque você engravidou <em>depois de contratada</em>.'),
    ("26-08-familia-revisao-pensao", 'Pensão fixada há anos e nunca mais revista?<br>Isso <em>também se corrige</em>.'),
    ("27-08-gestante-tst-contrato-temporario", 'O contrato temporário pode ter prazo para acabar.<br>A <em>proteção da gravidez</em>, não.'),
    ("28-08-familia-guarda-unilateral", 'Seu filho não é moeda de troca.<br><em>Visita e pensão são direitos separados</em>.'),
    ("29-08-familia-cobrar-pensao-fds", 'Pedir ajuda pra cobrar pensão<br>não é <em>fraqueza</em>. É cuidado com seu filho.'),
    ("31-08-gestante-volta-licenca", 'Volta ao trabalho depois da licença<br>não é favor da empresa. É <em>direito garantido</em>.'),
]


async def main():
    out_dir = Path(__file__).parent / "_saida_frases_calendario_agosto"
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
