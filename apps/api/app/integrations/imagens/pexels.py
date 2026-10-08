"""Banco de fotos Pexels (uso comercial liberado, sem atribuição obrigatória).

Interface: `Pexels(chave).buscar(consulta, quantidade)` → fotos verticais, em
português, com crédito do fotógrafo e link da página (para conferir a licença).
"""
from dataclasses import dataclass

import httpx

URL = "https://api.pexels.com/v1/search"


@dataclass(frozen=True)
class FotoBanco:
    id: int
    url: str
    autor: str
    pagina: str
    descricao: str
    largura: int
    altura: int


class Pexels:
    def __init__(self, chave: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._chave = chave
        self._transport = transport

    async def buscar(self, consulta: str, quantidade: int = 15, orientacao: str = "portrait") -> list[FotoBanco]:
        params = {"query": consulta, "per_page": quantidade, "orientation": orientacao, "locale": "pt-BR"}
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as client:
            resposta = await client.get(URL, params=params, headers={"Authorization": self._chave})
        resposta.raise_for_status()
        return [
            FotoBanco(id=f["id"], url=f["src"]["original"], autor=f.get("photographer", ""), pagina=f.get("url", ""),
                      descricao=f.get("alt") or "", largura=f.get("width", 0), altura=f.get("height", 0))
            for f in resposta.json().get("photos", [])
        ]
