from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.base import AIClient
from app.integrations.ai.gemini import GeminiClient
from app.models.contact import Contact
from app.models.content_piece import ContentPiece
from app.models.email_send import EmailSend
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_metric import SocialMetric
from app.models.user import User
from app.services.insights import gerar_insights

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_ai_client() -> AIClient:
    return GeminiClient(api_key=settings.GEMINI_API_KEY)


@router.post("/insights")
async def insights(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    dicas = await gerar_insights(db, current_user.tenant_id, get_ai_client())
    return {"dicas": dicas}


@router.get("/resumo")
async def resumo(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    tenant_id = current_user.tenant_id
    agora = datetime.now(timezone.utc)

    async def _count(stmt) -> int:
        return (await db.execute(stmt)).scalar_one()

    conteudos_por_status: dict[str, int] = {}
    result = await db.execute(
        select(ContentPiece.status, func.count(ContentPiece.id))
        .where(ContentPiece.tenant_id == tenant_id)
        .group_by(ContentPiece.status)
    )
    for status, total in result.all():
        conteudos_por_status[status] = total

    contatos_por_origem: dict[str, int] = {}
    result = await db.execute(
        select(Contact.origem, func.count(Contact.id))
        .where(Contact.tenant_id == tenant_id, Contact.status == "ativo")
        .group_by(Contact.origem)
    )
    for origem, total in result.all():
        contatos_por_origem[origem] = total

    # produção semanal: pautas e conteúdos criados por semana, últimas 8 semanas
    producao_semanal = []
    for i in range(7, -1, -1):
        fim = agora - timedelta(weeks=i)
        inicio = fim - timedelta(weeks=1)
        pautas_semana = await _count(
            select(func.count(Pauta.id)).where(
                Pauta.tenant_id == tenant_id,
                Pauta.criado_em >= inicio,
                Pauta.criado_em < fim,
            )
        )
        conteudos_semana = await _count(
            select(func.count(ContentPiece.id)).where(
                ContentPiece.tenant_id == tenant_id,
                ContentPiece.criado_em >= inicio,
                ContentPiece.criado_em < fim,
            )
        )
        producao_semanal.append(
            {
                "semana": inicio.date().isoformat(),
                "pautas": pautas_semana,
                "conteudos": conteudos_semana,
            }
        )

    proximos = (
        (
            await db.execute(
                select(ScheduledPost)
                .where(
                    ScheduledPost.tenant_id == tenant_id,
                    ScheduledPost.data_agendada >= date.today(),
                )
                .order_by(ScheduledPost.data_agendada, ScheduledPost.horario)
                .limit(6)
            )
        )
        .scalars()
        .all()
    )

    ultima_metrica = (
        await db.execute(
            select(SocialMetric)
            .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == "conta")
            .order_by(SocialMetric.coletado_em.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    instagram = ultima_metrica.metricas if ultima_metrica else None

    ultima_metrica_gmb = (
        await db.execute(
            select(SocialMetric)
            .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == "google_business")
            .order_by(SocialMetric.coletado_em.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    google_business = ultima_metrica_gmb.metricas if ultima_metrica_gmb else None

    return {
        "instagram": instagram,
        "google_business": google_business,
        "conteudos_por_status": conteudos_por_status,
        "contatos_por_origem": contatos_por_origem,
        "contatos_ativos": sum(contatos_por_origem.values()),
        "emails_enviados": await _count(
            select(func.count(EmailSend.id)).where(
                EmailSend.tenant_id == tenant_id, EmailSend.status == "enviado"
            )
        ),
        "pautas_total": await _count(
            select(func.count(Pauta.id)).where(Pauta.tenant_id == tenant_id)
        ),
        "producao_semanal": producao_semanal,
        "proximos_agendamentos": [
            {
                "id": str(p.id),
                "titulo": p.titulo,
                "canal": p.canal,
                "formato": p.formato,
                "data_agendada": p.data_agendada.isoformat(),
                "horario": p.horario,
                "status": p.status,
            }
            for p in proximos
        ],
    }
