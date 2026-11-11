"""Auto-agendamento: conteúdo aprovado entra na próxima vaga do calendário.

Instagram: até 2 publicações no feed por dia (pedido da Jessica em 10/11/2026: "quando sair reels pode sair as outras
publicações ao meio dia"; antes era 1 por dia, regra de 16/10/2026): 1 post (estático ou carrossel) às 12h e 1 Reels às
19h. Cada post aprovado vai para o primeiro dia, a partir de amanhã, sem outro post do feed; cada Reels, para o primeiro
dia de Reels sem outro Reels (Stories e Trial Reels não contam: o Orbit não publica Stories).
Reels só 2 vezes por semana, na terça e na sexta (pedido de 23/10/2026: cada Reels precisa de tempo para se
destacar). A série Mito ou Lei sai em Reels seg/qua/sáb 19h por data combinada. Reels com data combinada fora de terça ou sexta vai para a
próxima terça ou sexta livre.
Horários: Reels no máximo às 19:00 (pedido de 10/11/2026: às 21h os Reels não tinham visualizações nem curtidas;
nenhum Reels passa das 19:00, nem com hora combinada); post do feed às 12:00 todos os dias.
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
HORARIO_REELS, HORARIO_FEED = "19:00", "12:00"  # pedido de 10/11/2026: feed ao meio dia, Reels às 19h
HORARIO_MAXIMO_REELS = "19:00"  # pedido de 10/11/2026: Reels nunca depois das 19h
DIAS_REELS = {1, 4}  # terça e sexta: 2 Reels por semana (pedido de 23/10/2026)

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


def limitar_horario_reels(horario: str) -> str:
    """Reels nunca depois das 19:00 (pedido de 10/11/2026)."""
    return min(horario, HORARIO_MAXIMO_REELS) if horario else HORARIO_REELS


def horario_instagram(tipo: str, dia: date) -> str:
    return HORARIO_REELS if tipo == "reels" else HORARIO_FEED


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


async def dia_livre_no_instagram(db: AsyncSession, tenant_id: uuid.UUID, tipo: str = "carrossel",
                                 a_partir: date | None = None) -> date:
    """Primeiro dia livre do Instagram (Stories não contam) a partir de amanhã (ou de `a_partir`).
    Reels: dia de Reels sem outro Reels. Post do feed: qualquer dia sem outro post do feed (o Reels não ocupa a vaga)."""
    amanha = max(hoje_brasilia() + timedelta(days=1), a_partir or date.min)
    eh_reels = tipo == "reels"
    dias_permitidos = DIAS_REELS if eh_reels else set(range(7))
    filtro_formato = (ScheduledPost.formato == "reels") if eh_reels else ScheduledPost.formato.not_in(
        ("story", "trial", "reels"))  # Stories e Trial Reels não ocupam o dia
    ocupados = set(
        (
            await db.execute(
                select(ScheduledPost.data_agendada).where(
                    ScheduledPost.tenant_id == tenant_id,
                    ScheduledPost.canal == "instagram",
                    filtro_formato,
                    ScheduledPost.data_agendada >= amanha,
                )
            )
        ).scalars().all()
    )
    dia = amanha
    while dia in ocupados or dia.weekday() not in dias_permitidos:
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
    if programacao and piece.tipo == "reels" and programacao[0].weekday() not in DIAS_REELS:
        # A regra dos 2 Reels por semana vale também para a data combinada: vai para a próxima terça ou sexta livre.
        dia = await dia_livre_no_instagram(db, piece.tenant_id, "reels", a_partir=programacao[0])
        horario = HORARIO_REELS
    elif programacao:
        dia, horario = programacao
        if piece.tipo == "reels":
            horario = limitar_horario_reels(horario)
    elif piece.tipo in TIPOS_DO_FEED:
        dia = await dia_livre_no_instagram(db, piece.tenant_id, piece.tipo)
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
