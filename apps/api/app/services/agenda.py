"""Auto-agendamento: conteúdo aprovado entra na próxima vaga do calendário.

Instagram: 1 publicação por dia (pedido da Letícia em 16/10/2026: com várias por dia, os posts não têm tempo de
esquentar). Cada peça aprovada vai para o primeiro dia, a partir de amanhã, sem nenhum post do Instagram (Stories não
contam: o Orbit não publica Stories). Em dia de Reels, só o Reels.
Horários pelo alcance real do perfil nos últimos 12 meses (análise do Instagram no Orbit): Reels 21:00 (melhor
horário), feed 14:00 de segunda a sexta e 11:00 no sábado e no domingo.
Peça com `corpo.programacao` (data e hora combinadas na produção) vai para essa data e hora.

O resto (artigo, jornal, legenda solta, stories) segue o playbook antigo: 2 vagas por dia (11:00 e 17:00).
Um content_piece nunca gera duas entradas (unique constraint).
"""
import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.services.agendamento_horario import hoje_brasilia

HORARIOS_PLAYBOOK = ["11:00", "17:00"]
TIPOS_DO_FEED = {"carrossel", "carousel", "estatico", "frase", "pergunta", "reels"}
HORARIO_REELS, HORARIO_FEED_SEMANA, HORARIO_FEED_FIM_DE_SEMANA = "21:00", "14:00", "11:00"

FORMATO_POR_TIPO = {
    "carrossel": "carrossel",
    "carousel": "carrossel",
    "legenda": "post",
    "caption": "post",
    "stories": "story",
    "story": "story",
    "artigo": "artigo",
    "jornal": "newsletter",
    "reels": "reels",
    "estatico": "post",
    "frase": "post",
    "pergunta": "post",
}

CANAL_POR_TIPO = {"artigo": "blog", "jornal": "blog"}


def horario_instagram(tipo: str, dia: date) -> str:
    if tipo == "reels":
        return HORARIO_REELS
    return HORARIO_FEED_FIM_DE_SEMANA if dia.weekday() >= 5 else HORARIO_FEED_SEMANA


async def proxima_vaga(db: AsyncSession, tenant_id: uuid.UUID) -> tuple[date, str]:
    """Encontra o primeiro (dia, horário) livre do playbook a partir de amanhã."""
    dia = hoje_brasilia() + timedelta(days=1)
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


async def dia_livre_no_instagram(db: AsyncSession, tenant_id: uuid.UUID) -> date:
    """Primeiro dia, a partir de amanhã, sem nenhuma publicação do Instagram (Stories não contam)."""
    amanha = hoje_brasilia() + timedelta(days=1)
    ocupados = set(
        (
            await db.execute(
                select(ScheduledPost.data_agendada).where(
                    ScheduledPost.tenant_id == tenant_id,
                    ScheduledPost.canal == "instagram",
                    ScheduledPost.formato.not_in(("story", "trial")),  # Stories e Trial Reels não ocupam o dia
                    ScheduledPost.data_agendada >= amanha,
                )
            )
        ).scalars().all()
    )
    dia = amanha
    while dia in ocupados:
        dia += timedelta(days=1)
    return dia


def _programacao_combinada(piece: ContentPiece) -> tuple[date, str] | None:
    """Data/hora já combinadas com a Letícia na produção (`corpo.programacao`), se houver."""
    prog = (piece.corpo or {}).get("programacao") or {}
    try:
        return date.fromisoformat(prog["data"]), prog.get("hora") or "12:00"
    except (KeyError, TypeError, ValueError):
        return None


async def cancelar_agendamento_pendente(db: AsyncSession, piece: ContentPiece) -> None:
    """Tira do calendário a peça que voltou para ajuste; o que já foi publicado fica."""
    resultado = await db.execute(
        select(ScheduledPost).where(ScheduledPost.content_piece_id == piece.id)
    )
    agendamento = resultado.scalar_one_or_none()
    if agendamento is not None and agendamento.status != "publicado":
        await db.delete(agendamento)


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

    programacao = _programacao_combinada(piece)
    if programacao:
        dia, horario = programacao
    elif piece.tipo in TIPOS_DO_FEED:
        dia = await dia_livre_no_instagram(db, piece.tenant_id)
        horario = horario_instagram(piece.tipo, dia)
    else:
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
