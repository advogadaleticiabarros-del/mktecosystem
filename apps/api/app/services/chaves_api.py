"""Chaves de API de serviços externos, cadastradas pela tela de Configurações.

Interface:
- `salvar_chave(db, tenant_id, provedor, chave)` — testa a chave no próprio
  serviço e só então guarda criptografada (Fernet, a mesma do token do
  Instagram). Chave recusada levanta `ChaveRecusada` e nada é salvo.
- `status_chaves(db, tenant_id)` — o que a tela pode mostrar: configurada,
  4 últimos caracteres, quando foi validada. Nunca o valor.
- `obter_chave(db, tenant_id, provedor)` — valor em claro para uso interno;
  sem cadastro, cai na variável de ambiente (ex.: OPENAI_API_KEY).
- `remover_chave(db, tenant_id, provedor)`.
"""
import uuid
from datetime import datetime, timezone

import httpx
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token, encrypt_token
from app.models.chave_api import ChaveApi


class ChaveRecusada(ValueError):
    """O serviço disse que a chave não vale."""


async def validar_openai(chave: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
    async with httpx.AsyncClient(transport=transport, timeout=20) as client:
        resposta = await client.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {chave}"})
    if resposta.status_code in (401, 403):
        raise ChaveRecusada(
            "A OpenAI recusou essa chave. Confira se copiou a chave inteira e se ela está ativa no painel da OpenAI."
        )
    resposta.raise_for_status()


async def validar_pexels(chave: str, transport: httpx.AsyncBaseTransport | None = None) -> None:
    async with httpx.AsyncClient(transport=transport, timeout=20) as client:
        resposta = await client.get("https://api.pexels.com/v1/search", params={"query": "office", "per_page": 1},
                                    headers={"Authorization": chave})
    if resposta.status_code in (401, 403):
        raise ChaveRecusada("O Pexels recusou essa chave. Confira se copiou a chave inteira em pexels.com/api.")
    resposta.raise_for_status()


PROVEDORES = {
    "openai": {
        "nome": "OpenAI",
        "uso": "Terceira fonte do Jornalista: pesquisa na web, inclusive sites de tribunais e do governo.",
        "variavel": "OPENAI_API_KEY",
        "validar": validar_openai,
    },
    "pexels": {
        "nome": "Pexels",
        "uso": "Banco de fotos para capas e slides: busca a imagem certa para o tema de cada post.",
        "variavel": "PEXELS_API_KEY",
        "validar": validar_pexels,
    },
}


def _status(provedor: str, linha: ChaveApi | None) -> dict:
    info = PROVEDORES[provedor]
    via_ambiente = linha is None and bool(getattr(settings, info["variavel"], ""))
    return {
        "provedor": provedor,
        "nome": info["nome"],
        "uso": info["uso"],
        "configurada": linha is not None or via_ambiente,
        "final": linha.final if linha else None,
        "validada_em": linha.validada_em.isoformat() if linha else None,
        "origem": "painel" if linha else ("servidor" if via_ambiente else None),
    }


async def _linha(db: AsyncSession, tenant_id: uuid.UUID, provedor: str) -> ChaveApi | None:
    return (
        await db.execute(select(ChaveApi).where(ChaveApi.tenant_id == tenant_id, ChaveApi.provedor == provedor))
    ).scalar_one_or_none()


async def salvar_chave(db: AsyncSession, tenant_id: uuid.UUID, provedor: str, chave: str, validar=None) -> dict:
    if provedor not in PROVEDORES:
        raise KeyError(provedor)
    chave = chave.strip()
    if len(chave) < 8:
        raise ChaveRecusada("Essa chave parece incompleta. Copie de novo a chave inteira.")
    await (validar or PROVEDORES[provedor]["validar"])(chave)

    linha = await _linha(db, tenant_id, provedor)
    if linha is None:
        linha = ChaveApi(tenant_id=tenant_id, provedor=provedor)
        db.add(linha)
    linha.chave_criptografada = encrypt_token(chave)
    linha.final = chave[-4:]
    linha.validada_em = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(linha)
    return _status(provedor, linha)


async def status_chaves(db: AsyncSession, tenant_id: uuid.UUID) -> list[dict]:
    return [_status(p, await _linha(db, tenant_id, p)) for p in PROVEDORES]


async def obter_chave(db: AsyncSession, tenant_id: uuid.UUID, provedor: str) -> str | None:
    linha = await _linha(db, tenant_id, provedor)
    if linha is not None:
        return decrypt_token(linha.chave_criptografada)
    return getattr(settings, PROVEDORES[provedor]["variavel"], "") or None


async def remover_chave(db: AsyncSession, tenant_id: uuid.UUID, provedor: str) -> None:
    await db.execute(delete(ChaveApi).where(ChaveApi.tenant_id == tenant_id, ChaveApi.provedor == provedor))
    await db.commit()
