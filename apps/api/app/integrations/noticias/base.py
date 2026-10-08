"""Seam das fontes de notícia do Jornalista: cada adapter busca uma consulta e
devolve `Noticia`s (título, link, veículo, data, trecho). Duas fontes
independentes (Google Notícias e Tavily) permitem contar quantos veículos
diferentes deram o mesmo fato."""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Noticia:
    titulo: str
    url: str
    fonte: str
    trecho: str
    publicado_em: datetime | None
    site: str = ""  # endereço do veículo (o link do Google Notícias é um redirecionamento)


class Buscador(Protocol):
    async def buscar(self, consulta: str, dias: int) -> list[Noticia]: ...


class BuscadorMultiplo:
    """Junta várias fontes; uma fonte fora do ar não derruba as outras."""

    def __init__(self, buscadores: list[Buscador]) -> None:
        self._buscadores = buscadores

    async def buscar(self, consulta: str, dias: int) -> list[Noticia]:
        noticias: list[Noticia] = []
        erros = 0
        for b in self._buscadores:
            try:
                noticias += await b.buscar(consulta, dias)
            except Exception:
                erros += 1
        if erros == len(self._buscadores):
            raise RuntimeError(f"nenhuma fonte respondeu para '{consulta}'")
        return noticias
