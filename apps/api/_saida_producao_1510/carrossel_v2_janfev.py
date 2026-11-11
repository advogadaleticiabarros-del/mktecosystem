"""Carrosséis de janeiro e fevereiro de 2027 no formato V2 (11/11/2026, Jessica: "quero mudar também os carrosséis, quero
o formato V2 que fizemos juntos"). Mesmos textos de carrosseis_jan_fev.py, desenho de
producao/estilos/carrossel-referencias/v2_modelo.py. A versão v5 (pecas/<chave>-v5-*.jpg) fica guardada.

Uso: python carrossel_v2_janfev.py [chave ...]   → pecas/<chave>-v2-1.jpg … -7.jpg (1080×1440)"""
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

import capa_fecho
import carrosseis_jan_fev as JF

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "producao" / "estilos" / "carrossel-referencias"))
import v2_modelo  # noqa: E402

# palavra curta que fica em pé na divisa 6|7 e de fantasma na página 2
PALAVRA = {"ferias-regras": "férias", "rescisao-tipos": "saída", "atestado-medico": "atestado", "contrato-experiencia": "prazo",
           "salario-maternidade-quem": "mãe", "pensao-duvidas": "pensão", "fgts-saque": "FGTS", "hora-extra-calculo": "horas",
           "volta-as-aulas": "escola", "gestante-6-direitos": "gestante", "carnaval-trabalho": "folia", "direitos-dos-pais": "pai",
           "pedido-demissao": "contas", "holerite-conferir": "holerite", "trabalho-domestico": "casa", "aviso-previo-tudo": "aviso"}
RETRATO_FECHO = capa_fecho.ORDEM_RETRATOS


async def main(filtro):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": v2_modelo.W * v2_modelo.N, "height": v2_modelo.H})
        for i, t in enumerate(JF.TEMAS):
            k = t["chave"]
            if filtro and k not in filtro:
                continue
            fotos = {"capa": v2_modelo.uri(AQUI / "_fotos_pexels" / f"original-{k}.jpg"),
                     "foto": v2_modelo.uri(AQUI / "_fotos_pexels" / f"{JF.FOTO5[k]}.jpg"),
                     "fecho": v2_modelo.uri(AQUI / "_retratos" / f"{RETRATO_FECHO[i % len(RETRATO_FECHO)]}.jpg")}
            await v2_modelo.renderizar(pg, t["carrossel"], fotos, PALAVRA[k], AQUI / "pecas" / f"{k}-v2")
            print("ok", k, flush=True)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
