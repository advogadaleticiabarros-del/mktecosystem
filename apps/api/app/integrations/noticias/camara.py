"""Projetos de lei na Câmara dos Deputados (dados abertos, sem chave), como fonte do Jornalista.

Cada proposição vira uma `Noticia` com fonte "Câmara dos Deputados": título "PL 1234/2026", trecho = ementa, link para
a página da proposta. Projeto de lei não é lei: a peça que sair daqui precisa dizer que ainda está em tramitação.
"""
from datetime import date, timedelta

import httpx

from app.integrations.noticias.base import Noticia

URL = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
PAGINA = "https://www.camara.leg.br/propostas-legislativas/{id}"


class CamaraProposicoes:
    def __init__(self, limite: int = 10, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._limite = limite
        self._transport = transport

    async def buscar(self, consulta: str, dias: int) -> list[Noticia]:
        params = {"keywords": consulta, "siglaTipo": ["PL", "PLP", "PEC", "MPV"],
                  "dataApresentacaoInicio": (date.today() - timedelta(days=dias)).isoformat(),
                  "ordem": "DESC", "ordenarPor": "id", "itens": self._limite}
        async with httpx.AsyncClient(transport=self._transport, timeout=30,
                                     headers={"Accept": "application/json"}) as c:
            r = await c.get(URL, params=params)
        r.raise_for_status()
        return [
            Noticia(titulo=f"{p['siglaTipo']} {p['numero']}/{p['ano']}", url=PAGINA.format(id=p["id"]),
                    fonte="Câmara dos Deputados", trecho=(p.get("ementa") or "")[:600], publicado_em=None,
                    site="https://www.camara.leg.br")
            for p in r.json().get("dados", [])
        ]
