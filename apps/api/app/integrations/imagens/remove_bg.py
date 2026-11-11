"""remove.bg: tira o fundo de uma foto (ex.: retrato da Dra. para a capa em quadro 3D).

Interface: `RemoveBg(chave).recortar(imagem: bytes)` → PNG com fundo transparente.
Plano grátis: 50 recortes por mês em tamanho de prévia (até 0,25 megapixel); tamanho cheio gasta crédito.
Sem crédito levanta `SemCredito`. A foto original nunca é alterada (regra: imagem da Dra. sem filtro).
"""
import httpx

URL = "https://api.remove.bg/v1.0/removebg"


class SemCredito(RuntimeError):
    pass


class RemoveBg:
    def __init__(self, chave: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._chave = chave
        self._transport = transport

    async def recortar(self, imagem: bytes, tamanho: str = "auto") -> bytes:
        async with httpx.AsyncClient(transport=self._transport, timeout=90) as c:
            r = await c.post(URL, headers={"X-Api-Key": self._chave}, data={"size": tamanho, "format": "png"},
                             files={"image_file": ("foto.jpg", imagem)})
        if r.status_code == 402:
            raise SemCredito("Acabaram os créditos do remove.bg deste mês.")
        r.raise_for_status()
        return r.content
