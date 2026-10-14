import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from montar_reel_montagem import montar

CENAS = [
    {"kicker": "Trabalhista", "texto": "Assédio moral no trabalho: <em>3 sinais</em> que ninguém te conta", "tamanho_fonte": 56},
    {"kicker": "Sinal 1", "numero": "1", "texto": "Não é só gritar. <em>Ironia constante</em> e humilhação silenciosa também contam", "tamanho_fonte": 50},
    {"kicker": "Sinal 2", "numero": "2", "texto": "<em>Isolar você</em> das reuniões e decisões também é assédio", "tamanho_fonte": 52},
    {"kicker": "Sinal 3", "numero": "3", "texto": "Metas impossíveis só pra te fazer <em>\"pedir pra sair\"</em> são estratégia, não acaso", "tamanho_fonte": 48},
    {"kicker": "", "texto": "Se você reconheceu algum desses sinais,<br><em>procure uma advogada de confiança</em>", "tamanho_fonte": 48, "rodape": "Advogada Trabalhista | OAB/ES 39.948"},
]

DURACOES = [3.6, 4.6, 4.6, 4.8, 4.2]

if __name__ == "__main__":
    asyncio.run(montar(
        pasta_reel=str(Path(__file__).resolve().parent.parent),
        cenas=CENAS,
        durs=DURACOES,
        saida=str(Path(__file__).resolve().parent.parent / "reel.mp4"),
    ))
