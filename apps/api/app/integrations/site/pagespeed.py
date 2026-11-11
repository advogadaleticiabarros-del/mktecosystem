"""Google PageSpeed Insights: notas do Lighthouse (0 a 100) e as métricas que pesam no Google.

Interface: `PageSpeed(chave=None).medir(url, estrategia="mobile")` → `Medicao`.
Funciona sem chave, mas com cota pequena compartilhada; com `GOOGLE_API_KEY` a cota é de 25 mil por dia.
Uma medição demora de 20 a 60 segundos (o Google abre a página de verdade).
"""
from dataclasses import dataclass

import httpx

URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CATEGORIAS = {"performance": "desempenho", "seo": "seo", "accessibility": "acessibilidade",
              "best-practices": "boas_praticas"}


@dataclass(frozen=True)
class Medicao:
    url: str
    estrategia: str
    notas: dict[str, int]  # desempenho, seo, acessibilidade, boas_praticas
    lcp_s: float | None  # maior elemento visível (bom: até 2,5 s)
    cls: float | None  # quanto a página "pula" (bom: até 0,1)
    tbt_ms: float | None  # tempo bloqueado (bom: até 200 ms)


class PageSpeed:
    def __init__(self, chave: str | None = None, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._chave = chave
        self._transport = transport

    async def medir(self, url: str, estrategia: str = "mobile") -> Medicao:
        params: list[tuple[str, str]] = [("url", url), ("strategy", estrategia), ("locale", "pt_BR")]
        params += [("category", c.upper().replace("-", "_")) for c in CATEGORIAS]
        if self._chave:
            params.append(("key", self._chave))
        async with httpx.AsyncClient(transport=self._transport, timeout=120) as c:
            r = await c.get(URL, params=params)
        r.raise_for_status()
        lh = r.json().get("lighthouseResult", {})
        cats = lh.get("categories", {})
        audits = lh.get("audits", {})

        def valor(chave: str) -> float | None:
            v = audits.get(chave, {}).get("numericValue")
            return float(v) if v is not None else None

        lcp = valor("largest-contentful-paint")
        return Medicao(
            url=url, estrategia=estrategia,
            notas={nome: round((cats[c].get("score") or 0) * 100) for c, nome in CATEGORIAS.items() if c in cats},
            lcp_s=round(lcp / 1000, 2) if lcp is not None else None,
            cls=round(v, 3) if (v := valor("cumulative-layout-shift")) is not None else None,
            tbt_ms=round(v) if (v := valor("total-blocking-time")) is not None else None,
        )
