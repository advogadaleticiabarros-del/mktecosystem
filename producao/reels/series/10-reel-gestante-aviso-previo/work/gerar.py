import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from montar_reel_montagem import montar

CENAS = [
    {"kicker": "Gestante CLT", "texto": "Engravidou durante o <em>aviso prévio</em>? Isso muda alguma coisa", "tamanho_fonte": 58},
    {"kicker": "O que muda", "numero": "1", "texto": "A estabilidade da gestante começa na <em>confirmação da gravidez</em>, não na assinatura de um papel", "tamanho_fonte": 50},
    {"kicker": "O que muda", "numero": "2", "texto": "Vale <em>mesmo que a empresa já tenha avisado</em> que o contrato ia terminar", "tamanho_fonte": 52},
    {"kicker": "O que muda", "numero": "3", "texto": "A proteção vai até <em>5 meses após o parto</em>", "tamanho_fonte": 56},
    {"kicker": "", "texto": "Se isso é o seu caso,<br><em>procure uma advogada de confiança</em>", "tamanho_fonte": 52, "rodape": "Advogada Trabalhista | OAB/ES 39.948"},
]

DURACOES = [3.8, 4.6, 4.6, 4.2, 4.2]

if __name__ == "__main__":
    asyncio.run(montar(
        pasta_reel=str(Path(__file__).resolve().parent.parent),
        cenas=CENAS,
        durs=DURACOES,
        saida=str(Path(__file__).resolve().parent.parent / "reel.mp4"),
    ))
