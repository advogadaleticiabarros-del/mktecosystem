"""Auto-agendamento: conteúdo aprovado entra na próxima vaga do playbook.

Playbook padrão: 2 publicações/dia (11:00 e 17:00), começando amanhã.
Um content_piece nunca gera duas entradas (unique constraint).
"""
import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost

HORARIOS_PLAYBOOK = ["11:00", "17:00"]

FORMATO_POR_TIPO = {
    "carrossel": "carrossel",
    "carousel": "carrossel",
    "legenda": "post",
    "caption": "post",
    "stories": "story",
    "story": "story",
    "artigo": "artigo",
}

CANAL_POR_TIPO = {"artigo": "blog"}


async def proxima_vaga(db: AsyncSession, tenant_id: uuid.UUID) -> tuple[date, str]:
    """Encontra o primeiro (dia, horário) livre a partir de amanhã."""
    dia = date.today() + timedelta(days=1)
    while True:
        ocupados = (
            (
                await db.execute(
                    select(ScheduledPost.horario).where(
                        ScheduledPost.tenant_id == tenant_id,
                        ScheduledPost.data_agendada == dia,
                    )
                )
            )
            .scalars()
            .all()
        )
        for horario in HORARIOS_PLAYBOOK:
            if horario not in ocupados:
                return dia, horario
        dia += timedelta(days=1)


async def agendar_conteudo_aprovado(
    db: AsyncSession, piece: ContentPiece
) -> ScheduledPost | None:
    """Cria a entrada no calendário para um conteúdo recém-aprovado."""
    existente = await db.execute(
        select(ScheduledPost).where(ScheduledPost.content_piece_id == piece.id)
    )
    if existente.scalar_one_or_none() is not None:
        return None

    pauta = (
        await db.execute(select(Pauta).where(Pauta.id == piece.pauta_id))
    ).scalar_one_or_none()
    titulo = pauta.titulo if pauta else f"Conteúdo {piece.tipo}"

    dia, horario = await proxima_vaga(db, piece.tenant_id)
    agendamento = ScheduledPost(
        tenant_id=piece.tenant_id,
        content_piece_id=piece.id,
        titulo=titulo,
        canal=CANAL_POR_TIPO.get(piece.tipo, "instagram"),
        formato=FORMATO_POR_TIPO.get(piece.tipo, "post"),
        data_agendada=dia,
        horario=horario,
        status="pronto",
    )
    db.add(agendamento)
    return agendamento
