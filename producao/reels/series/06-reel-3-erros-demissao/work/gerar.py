import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from montar_reel_montagem import montar

CENAS = [
    {"kicker": "Trabalhista", "texto": "3 erros que fazem você <em>perder direitos</em> na demissão", "tamanho_fonte": 60},
    {"kicker": "Erro 1", "numero": "1", "texto": "Assinar tudo sem ler, só porque a empresa disse que é <em>\"padrão\"</em>", "tamanho_fonte": 52},
    {"kicker": "Erro 2", "numero": "2", "texto": "Não guardar <em>prints, e-mails ou testemunhas</em> de irregularidades", "tamanho_fonte": 52},
    {"kicker": "Erro 3", "numero": "3", "texto": "Esperar demais pra buscar orientação. <em>Alguns direitos têm prazo</em>", "tamanho_fonte": 52},
    {"kicker": "", "texto": "Se isso já aconteceu com você,<br><em>procure uma advogada de confiança</em>", "tamanho_fonte": 52, "rodape": "Advogada Trabalhista | OAB/ES 39.948"},
]

DURACOES = [3.6, 4.6, 4.6, 4.6, 4.2]

if __name__ == "__main__":
    asyncio.run(montar(
        pasta_reel=str(Path(__file__).resolve().parent.parent),
        cenas=CENAS,
        durs=DURACOES,
        saida=str(Path(__file__).resolve().parent.parent / "reel.mp4"),
    ))
