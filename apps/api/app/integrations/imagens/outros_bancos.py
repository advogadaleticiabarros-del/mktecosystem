"""Mais bancos de fotos além do Pexels, com a mesma interface `buscar(consulta, quantidade)` → `list[FotoBanco]`.

- `Openverse()`: sem chave. Só traz obras em domínio público ou CC0 (uso comercial sem atribuição obrigatória).
- `Pixabay(chave)`: licença Pixabay (uso comercial sem atribuição). A URL é a versão grande (até 1280 px no lado
  maior); serve para slide, não para capa em tela cheia sem conferir o tamanho.
"""
import httpx

from app.integrations.imagens.pexels import FotoBanco

OPENVERSE = "https://api.openverse.org/v1/images/"
PIXABAY = "https://pixabay.com/api/"


class Openverse:
    def __init__(self, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._transport = transport

    async def buscar(self, consulta: str, quantidade: int = 15, orientacao: str = "portrait") -> list[FotoBanco]:
        params = {"q": consulta, "page_size": min(quantidade, 20), "license": "cc0,pdm", "category": "photograph",
                  "mature": "false"}
        if orientacao == "portrait":
            params["aspect_ratio"] = "tall"
        async with httpx.AsyncClient(transport=self._transport, timeout=30, headers={"User-Agent": "Orbit"}) as c:
            r = await c.get(OPENVERSE, params=params)
        r.raise_for_status()
        return [
            FotoBanco(id=f["id"], url=f["url"], autor=f.get("creator") or "", pagina=f.get("foreign_landing_url") or "",
                      descricao=f.get("title") or "", largura=f.get("width") or 0, altura=f.get("height") or 0,
                      fonte="openverse", licenca=(f.get("license") or "").upper())
            for f in r.json().get("results", [])
        ]


class Pixabay:
    def __init__(self, chave: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._chave = chave
        self._transport = transport

    async def buscar(self, consulta: str, quantidade: int = 15, orientacao: str = "portrait") -> list[FotoBanco]:
        params = {"key": self._chave, "q": consulta, "lang": "pt", "image_type": "photo", "safesearch": "true",
                  "per_page": max(3, min(quantidade, 200))}
        if orientacao == "portrait":
            params["orientation"] = "vertical"
        async with httpx.AsyncClient(transport=self._transport, timeout=30) as c:
            r = await c.get(PIXABAY, params=params)
        r.raise_for_status()
        return [
            FotoBanco(id=f["id"], url=f["largeImageURL"], autor=f.get("user") or "", pagina=f.get("pageURL") or "",
                      descricao=f.get("tags") or "", largura=f.get("imageWidth") or 0,
                      altura=f.get("imageHeight") or 0, fonte="pixabay",
                      licenca="Licença Pixabay (uso comercial, sem atribuição)")
            for f in r.json().get("hits", [])[:quantidade]
        ]
