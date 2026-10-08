"""Auto-agendamento: conteúdo aprovado entra na próxima vaga do calendário.

Instagram segue o ciclo editorial de 2 dias (estratégia de 08/10/2026):
- dia de tema: pergunta 12:00, frase 15:00, carrossel 20:00 — as três peças
  da mesma pauta no mesmo dia, uma pauta por dia de tema;
- dia de respiro (o dia seguinte): estático 19:00, de preferência logo depois
  do dia de tema da sua pauta.
Os dias de tema alternam a partir de `CICLO_ANCORA`, então o calendário é o
mesmo não importa a ordem em que as peças são aprovadas.

O resto (artigo, jornal, legenda solta, stories, reels) segue o playbook
antigo: 2 vagas por dia (11:00 e 17:00), começando amanhã.
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
CICLO_ANCORA = date(2026, 10, 9)  # primeiro dia de tema do ciclo
HORARIO_DIA_DE_TEMA = {"pergunta": "12:00", "frase": "15:00", "carrossel": "20:00"}
HORARIO_DIA_DE_RESPIRO = {"estatico": "19:00"}

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


def eh_dia_de_tema(dia: date) -> bool:
    return (dia - CICLO_ANCORA).days % 2 == 0


async def proxima_vaga(db: AsyncSession, tenant_id: uuid.UUID) -> tuple[date, str]:
    """Encontra o primeiro (dia, horário) livre do playbook a partir de amanhã."""
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


async def _ciclo_ocupado(db: AsyncSession, tenant_id: uuid.UUID) -> dict[date, list[tuple[uuid.UUID, str]]]:
    """(pauta, tipo) de cada peça do ciclo já agendada, por dia, de amanhã em diante."""
    tipos = list(HORARIO_DIA_DE_TEMA) + list(HORARIO_DIA_DE_RESPIRO)
    linhas = await db.execute(
        select(ScheduledPost.data_agendada, ContentPiece.pauta_id, ContentPiece.tipo)
        .join(ContentPiece, ContentPiece.id == ScheduledPost.content_piece_id)
        .where(
            ScheduledPost.tenant_id == tenant_id,
            ScheduledPost.canal == "instagram",
            ScheduledPost.data_agendada > date.today(),
            ContentPiece.tipo.in_(tipos),
        )
    )
    ocupado: dict[date, list[tuple[uuid.UUID, str]]] = {}
    for dia, pauta_id, tipo in linhas.all():
        ocupado.setdefault(dia, []).append((pauta_id, tipo))
    return ocupado


async def vaga_no_ciclo(db: AsyncSession, piece: ContentPiece) -> tuple[date, str]:
    ocupado = await _ciclo_ocupado(db, piece.tenant_id)
    amanha = date.today() + timedelta(days=1)

    if piece.tipo in HORARIO_DIA_DE_TEMA:
        dia = amanha if eh_dia_de_tema(amanha) else amanha + timedelta(days=1)
        while True:
            pecas = ocupado.get(dia, [])
            outras_pautas = {p for p, _ in pecas if p != piece.pauta_id}
            if not outras_pautas and (piece.pauta_id, piece.tipo) not in pecas:
                return dia, HORARIO_DIA_DE_TEMA[piece.tipo]
            dia += timedelta(days=2)

    horario = HORARIO_DIA_DE_RESPIRO[piece.tipo]
    livre = lambda d: not any(tipo == piece.tipo for _, tipo in ocupado.get(d, []))  # noqa: E731
    dias_do_tema = sorted(
        d for d, pecas in ocupado.items()
        if eh_dia_de_tema(d) and any(p == piece.pauta_id for p, _ in pecas)
    )
    if dias_do_tema and livre(dias_do_tema[0] + timedelta(days=1)):
        return dias_do_tema[0] + timedelta(days=1), horario
    dia = amanha if not eh_dia_de_tema(amanha) else amanha + timedelta(days=1)
    while not livre(dia):
        dia += timedelta(days=2)
    return dia, horario


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

    if piece.tipo in HORARIO_DIA_DE_TEMA or piece.tipo in HORARIO_DIA_DE_RESPIRO:
        dia, horario = await vaga_no_ciclo(db, piece)
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
