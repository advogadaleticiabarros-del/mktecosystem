"""Carrossel "Demissão pelo voto?" (assédio eleitoral), 27/10/2026, no padrão v5 aprovado (capa Ouro editorial,
5 itens, checklist salvável e fechamento com retrato da Dra.). Reusa `carrossel_v5.renderizar` sem alterá-lo.

Fatos (conferidos em 27/10/2026, ver ../BRIEFING.md):
- MPT: 1.939 denúncias de assédio eleitoral no trabalho até 25/10/2026 (recorde); 140 só em 26/10.
- CF, art. 5º, VIII; Lei 9.029/1995, arts. 1º e 4º (reintegração com salários OU dobro da remuneração do período);
  dano moral à parte; Convenção 111 da OIT.
- Código Eleitoral, art. 301: coagir alguém a votar ou não votar, com violência ou grave ameaça: reclusão até 4 anos.
- Denúncia sigilosa no site do MPT.

Uso (de apps/api): python ../../producao/campanhas/2026-10-assedio-eleitoral/carrossel-stories/carrossel.py
Saída: apps/api/_saida_producao_1510/pecas/assedio-eleitoral-voto-v5-1..7.jpg
"""
import asyncio
import sys
from pathlib import Path

API = Path(__file__).resolve().parents[4] / "apps" / "api"
sys.path.insert(0, str(API))
sys.path.insert(0, str(API / "_saida_producao_1510"))

import carrossel_v5 as v5  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

CHAVE = "assedio-eleitoral-voto"

CARROSSEL = dict(
    tag="Assédio eleitoral", area="Trabalhista",
    capa=("Assédio eleitoral no trabalho", "Demissão<br>pelo voto?", "Isso tem nome na lei: discriminação.",
          'Não importa em quem você votou: <span class="mt">ninguém perde o emprego pela opinião política</span>.',
          "Lei 9.029/1995"),
    itens=[
        ("Quase <em>2 mil</em><br>denúncias em 2026",
         'Foram 1.939 denúncias de assédio eleitoral no MPT até o 2º turno, um recorde. <span class="mt">No dia seguinte, mais 140</span>.',
         "MPT, balanço de 26/10/2026"),
        ("Demitir pelo voto<br>é <em>discriminação</em>",
         'A lei proíbe dispensar alguém pela opinião política. <span class="mt">Não importa em quem você votou</span>.',
         "Lei 9.029/1995, art. 1º; CF, art. 5º, VIII"),
        ("A escolha<br>é <em>sua</em>",
         'Voltar ao emprego com os salários do período <span class="mt">ou receber em dobro</span> a remuneração desse tempo. E ainda pode caber dano moral.',
         "Lei 9.029/1995, art. 4º"),
        ("Ameaçar antes<br>do voto é <em>crime</em>",
         'Coagir alguém a votar ou a não votar em um candidato tem pena de <span class="mt">até 4 anos de reclusão</span>.',
         "Código Eleitoral, art. 301"),
        ("Aconteceu com você?<br><em>Guarde</em> as provas", "Antes de sair do grupo da empresa, salve:", "Denúncia sigilosa: site do MPT"),
    ],
    checklist=["Mensagens, áudios e prints", "Carta de dispensa e datas", "Nomes de testemunhas"],
    fecho=("Seu voto <em>não é</em><br>motivo de demissão.", "Cada caso tem detalhes.", "mande para quem precisa saber disso."),
    objetos=["nenhum", "ponte:7120126", "nenhum"], foto5=10155095,
)

RETRATO = "escritorio-cafe-blazer-preto"


async def main() -> None:
    v5.CARROSSEIS = {CHAVE: CARROSSEL}
    v5.RODIZIO = [RETRATO]
    v5.FOCO_CAPA[CHAVE] = None  # rosto detectado pelo OpenCV
    fecho = v5.capa_fecho.fecho
    v5.capa_fecho.fecho = lambda *a, **k: fecho(*a, cta="Procure uma advogada de confiança", **k)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 7560, "height": 1350}, device_scale_factor=2)
        await v5.renderizar(CHAVE, page)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
