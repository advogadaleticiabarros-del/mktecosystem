"""Dados públicos do Brasil, sem chave: feriados nacionais, endereço pelo CEP e empresa pelo CNPJ.

Interface: `DadosBrasil(transport=None)`
- `await feriados(ano)` → `list[Feriado]` em ordem de data (só nacionais).
- `await cep(cep)` → `Endereco | None` (None quando o CEP não existe).
- `await cnpj(cnpj)` → `Empresa | None` (None quando o CNPJ não existe).

Fonte principal: BrasilAPI. Se ela cair, feriados vêm do Nager.Date e CEP do ViaCEP; o chamador não precisa saber.
CNPJ inválido (dígitos errados) levanta `ValueError` antes de qualquer chamada. Erro das duas fontes levanta
`httpx.HTTPError`.
"""
import re
from dataclasses import dataclass
from datetime import date

import httpx

BRASILAPI = "https://brasilapi.com.br/api"
NAGER = "https://date.nager.at/api/v3/PublicHolidays"
VIACEP = "https://viacep.com.br/ws"


@dataclass(frozen=True)
class Feriado:
    data: date
    nome: str


@dataclass(frozen=True)
class Endereco:
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    uf: str


@dataclass(frozen=True)
class Empresa:
    cnpj: str
    razao_social: str
    nome_fantasia: str
    situacao: str
    atividade: str
    cnae: str
    porte: str
    cidade: str
    uf: str
    telefone: str
    email: str
    abertura: date | None


def so_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def cnpj_valido(cnpj: str) -> bool:
    n = so_digitos(cnpj)
    if len(n) != 14 or n == n[0] * 14:
        return False

    def digito(base: str, pesos: list[int]) -> str:
        resto = sum(int(d) * p for d, p in zip(base, pesos)) % 11
        return "0" if resto < 2 else str(11 - resto)

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = digito(n[:12], pesos1)
    d2 = digito(n[:12] + d1, [6] + pesos1)
    return n[12:] == d1 + d2


class DadosBrasil:
    def __init__(self, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._transport = transport

    def _cliente(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=self._transport, timeout=20, headers={"User-Agent": "Orbit"})

    async def feriados(self, ano: int) -> list[Feriado]:
        async with self._cliente() as c:
            try:
                r = await c.get(f"{BRASILAPI}/feriados/v1/{ano}")
                r.raise_for_status()
                lista = [Feriado(date.fromisoformat(f["date"]), f["name"]) for f in r.json()]
            except (httpx.HTTPError, ValueError, KeyError):
                r = await c.get(f"{NAGER}/{ano}/BR")
                r.raise_for_status()
                lista = [Feriado(date.fromisoformat(f["date"]), f.get("localName") or f["name"])
                         for f in r.json() if f.get("global", True)]
        return sorted(lista, key=lambda f: f.data)

    async def cep(self, cep: str) -> Endereco | None:
        n = so_digitos(cep)
        if len(n) != 8:
            return None
        async with self._cliente() as c:
            try:
                r = await c.get(f"{BRASILAPI}/cep/v2/{n}")
                if r.status_code == 404:
                    return None
                r.raise_for_status()
                d = r.json()
                return Endereco(n, d.get("street") or "", d.get("neighborhood") or "", d.get("city") or "",
                                d.get("state") or "")
            except httpx.HTTPError:
                r = await c.get(f"{VIACEP}/{n}/json/")
                r.raise_for_status()
                d = r.json()
                if d.get("erro"):
                    return None
                return Endereco(n, d.get("logradouro", ""), d.get("bairro", ""), d.get("localidade", ""),
                                d.get("uf", ""))

    async def cnpj(self, cnpj: str) -> Empresa | None:
        n = so_digitos(cnpj)
        if not cnpj_valido(n):
            raise ValueError("CNPJ inválido: confira os números.")
        async with self._cliente() as c:
            r = await c.get(f"{BRASILAPI}/cnpj/v1/{n}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        d = r.json()
        abertura = d.get("data_inicio_atividade")
        return Empresa(
            cnpj=n,
            razao_social=d.get("razao_social") or "",
            nome_fantasia=d.get("nome_fantasia") or "",
            situacao=d.get("descricao_situacao_cadastral") or "",
            atividade=d.get("cnae_fiscal_descricao") or "",
            cnae=str(d.get("cnae_fiscal") or ""),
            porte=d.get("porte") or d.get("descricao_porte") or "",
            cidade=d.get("municipio") or "",
            uf=d.get("uf") or "",
            telefone=so_digitos(d.get("ddd_telefone_1") or ""),
            email=(d.get("email") or "").lower(),
            abertura=date.fromisoformat(abertura) if abertura else None,
        )
