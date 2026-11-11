"""Busca de fotos em vários bancos ao mesmo tempo, sem repetir imagem já usada.

Interface: `BancoDeFotos(fontes).buscar(consulta, quantidade, evitar=())` → `list[FotoBanco]`
- intercala as fontes (uma de cada) para a escolha não ficar presa a um banco só;
- pula fotos cuja URL ou página esteja em `evitar` (regra: nunca repetir imagem entre posts) e duplicadas entre bancos;
- uma fonte fora do ar não derruba as outras; se todas falharem, levanta `RuntimeError`.

`criar_banco_de_fotos(pexels=None, pixabay=None)` monta com o que tiver chave; o Openverse entra sempre.
"""
import asyncio
from itertools import zip_longest
from typing import Iterable, Protocol

from app.integrations.imagens.pexels import FotoBanco


class FonteDeFotos(Protocol):
    async def buscar(self, consulta: str, quantidade: int = 15, orientacao: str = "portrait") -> list[FotoBanco]: ...


class BancoDeFotos:
    def __init__(self, fontes: list[FonteDeFotos]) -> None:
        self._fontes = fontes

    async def buscar(self, consulta: str, quantidade: int = 15, evitar: Iterable[str] = (),
                     orientacao: str = "portrait") -> list[FotoBanco]:
        resultados = await asyncio.gather(*(f.buscar(consulta, quantidade, orientacao) for f in self._fontes),
                                          return_exceptions=True)
        listas = [r for r in resultados if not isinstance(r, BaseException)]
        if self._fontes and not listas:
            raise RuntimeError(f"nenhum banco de fotos respondeu para '{consulta}'")
        bloqueadas = set(evitar)
        fotos: list[FotoBanco] = []
        for rodada in zip_longest(*listas):
            for foto in rodada:
                if foto is None or foto.url in bloqueadas or (foto.pagina and foto.pagina in bloqueadas):
                    continue
                bloqueadas.update({foto.url, foto.pagina} - {""})
                fotos.append(foto)
        return fotos[:quantidade]


def criar_banco_de_fotos(pexels: str | None = None, pixabay: str | None = None) -> BancoDeFotos:
    from app.integrations.imagens.outros_bancos import Openverse, Pixabay
    from app.integrations.imagens.pexels import Pexels

    fontes: list[FonteDeFotos] = []
    if pexels:
        fontes.append(Pexels(pexels))
    if pixabay:
        fontes.append(Pixabay(pixabay))
    fontes.append(Openverse())
    return BancoDeFotos(fontes)
