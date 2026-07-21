import uuid
from typing import Annotated
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.groq_client import GroqClient
from app.integrations.social.google_business_client import GoogleBusinessClient
from app.models.social_connection import SocialConnection
from app.models.user import User
from app.schemas.avaliacao import ResponderAvaliacaoIn
from app.services.triagem_avaliacoes import classificar_avaliacoes

router = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])


def get_google_client() -> GoogleBusinessClient:
    return GoogleBusinessClient(
        client_id=settings.GOOGLE_CLIENT_ID, client_secret=settings.GOOGLE_CLIENT_SECRET
    )


def get_groq_client() -> GroqClient:
    return GroqClient(api_key=settings.GROQ_API_KEY)


async def _conexao_ativa(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection:
    result = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == tenant_id,
            SocialConnection.plataforma == "google_business",
            SocialConnection.status == "ativo",
        )
    )
    conexao = result.scalar_one_or_none()
    if conexao is None:
        raise HTTPException(
            status_code=422, detail="Google Meu Negócio não conectado. Conecte na Visão Geral."
        )
    return conexao


@router.get("")
async def listar_avaliacoes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[dict]:
    conexao = await _conexao_ativa(db, current_user.tenant_id)
    client = get_google_client()
    access_token = await client.renovar_access_token(decrypt_token(conexao.access_token_encrypted))
    avaliacoes = await client.listar_avaliacoes(access_token, conexao.ig_user_id)
    return await classificar_avaliacoes(avaliacoes, get_groq_client())


@router.post("/{review_id:path}/responder")
async def responder_avaliacao(
    review_id: str,
    payload: ResponderAvaliacaoIn,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    conexao = await _conexao_ativa(db, current_user.tenant_id)
    client = get_google_client()
    access_token = await client.renovar_access_token(decrypt_token(conexao.access_token_encrypted))
    await client.responder_avaliacao(access_token, unquote(review_id), payload.texto)
    return {"status": "ok"}
