import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.base import AIClient
from app.integrations.ai.gemini import GeminiClient
from app.models.contact import Contact
from app.models.email_campaign import EmailCampaign
from app.models.user import User
from app.schemas.contact import ContactOut
from app.schemas.email_campaign import EmailCampaignOut, EmailCampaignUpdate
from app.services.email_campaigns import gerar_boas_vindas, gerar_rascunho_newsletter

router = APIRouter(prefix="/email", tags=["email"])

STATUS_PERMITIDOS = {"rascunho", "aprovado", "arquivado"}


def get_ai_client() -> AIClient:
    return GeminiClient(api_key=settings.GEMINI_API_KEY)


@router.get("/contacts", response_model=list[ContactOut])
async def listar_contatos(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Contact]:
    result = await db.execute(
        select(Contact)
        .where(Contact.tenant_id == current_user.tenant_id)
        .order_by(Contact.criado_em.desc())
    )
    return list(result.scalars().all())


@router.get("/campaigns", response_model=list[EmailCampaignOut])
async def listar_campanhas(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[EmailCampaign]:
    result = await db.execute(
        select(EmailCampaign)
        .where(
            EmailCampaign.tenant_id == current_user.tenant_id,
            EmailCampaign.status != "arquivado",
        )
        .order_by(EmailCampaign.criado_em.desc())
    )
    return list(result.scalars().all())


@router.post("/campaigns/gerar-boas-vindas", response_model=list[EmailCampaignOut])
async def gerar_sequencia_boas_vindas(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[EmailCampaign]:
    return await gerar_boas_vindas(db, current_user.tenant_id, get_ai_client())


@router.post("/campaigns/gerar-newsletter", response_model=EmailCampaignOut | None)
async def gerar_newsletter(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> EmailCampaign | None:
    campanha = await gerar_rascunho_newsletter(db, current_user.tenant_id, get_ai_client())
    if campanha is None:
        raise HTTPException(
            status_code=422,
            detail="Sem artigos aprovados nos últimos 7 dias para montar a newsletter.",
        )
    return campanha


@router.patch("/campaigns/{campaign_id}", response_model=EmailCampaignOut)
async def atualizar_campanha(
    campaign_id: uuid.UUID,
    payload: EmailCampaignUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> EmailCampaign:
    result = await db.execute(
        select(EmailCampaign).where(
            EmailCampaign.id == campaign_id,
            EmailCampaign.tenant_id == current_user.tenant_id,
        )
    )
    campanha = result.scalar_one_or_none()
    if campanha is None:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    if payload.status is not None:
        if payload.status not in STATUS_PERMITIDOS:
            raise HTTPException(status_code=422, detail=f"Status inválido: {payload.status}")
        if payload.status == "aprovado" and campanha.status != "aprovado":
            campanha.aprovado_em = datetime.now(timezone.utc)
        campanha.status = payload.status

    if payload.assunto is not None:
        campanha.assunto = payload.assunto
    if payload.corpo_html is not None:
        campanha.corpo_html = payload.corpo_html
    if payload.corpo_texto is not None:
        campanha.corpo_texto = payload.corpo_texto

    await db.commit()
    await db.refresh(campanha)
    return campanha
