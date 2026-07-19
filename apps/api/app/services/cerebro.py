"""Cérebro do ecossistema: aprende com as edições que a cliente faz.

Cada vez que um conteúdo gerado é editado antes da aprovação, registramos o
que mudou. Nas próximas gerações, essas lições entram no prompt para o mesmo
tenant — o sistema erra cada vez menos no tom daquele cliente.
"""
import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta

MAX_LICOES_NO_PROMPT = 5


def _resumo_diff(antes: dict, depois: dict) -> str:
    """Resumo curto e legível do que a edição mudou."""
    campos_alterados = []
    for chave in set(antes) | set(depois):
        if antes.get(chave) != depois.get(chave):
            valor_antes = json.dumps(antes.get(chave), ensure_ascii=False)[:200]
            valor_depois = json.dumps(depois.get(chave), ensure_ascii=False)[:200]
            campos_alterados.append(f"campo '{chave}': de {valor_antes} para {valor_depois}")
    return "; ".join(campos_alterados)[:1900]


async def registrar_edicao(
    db: AsyncSession, piece: ContentPiece, corpo_novo: dict
) -> None:
    resumo = _resumo_diff(piece.corpo or {}, corpo_novo)
    if not resumo:
        return
    pauta = (
        await db.execute(select(Pauta).where(Pauta.id == piece.pauta_id))
    ).scalar_one_or_none()
    db.add(
        MarketingMemory(
            tenant_id=piece.tenant_id,
            content_piece_id=piece.id,
            tema=pauta.titulo if pauta else "",
            angulo=pauta.angulo if pauta else "",
            formato=piece.tipo,
            metricas={"tipo_evento": "edicao"},
            aprendizado=resumo,
        )
    )


async def memorias_de_edicao(db: AsyncSession, tenant_id: uuid.UUID) -> str:
    """Últimas lições de edição do tenant, formatadas para entrar no prompt."""
    result = await db.execute(
        select(MarketingMemory)
        .where(
            MarketingMemory.tenant_id == tenant_id,
            MarketingMemory.aprendizado.is_not(None),
        )
        .order_by(MarketingMemory.id.desc())
        .limit(MAX_LICOES_NO_PROMPT)
    )
    licoes = [m.aprendizado for m in result.scalars().all() if m.aprendizado]
    return "\n".join(f"- [{i+1}] {licao}" for i, licao in enumerate(licoes))
