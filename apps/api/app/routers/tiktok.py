"""Tela TikTok: conexão, Reels enviados e rascunhos esperando quem publique pelo app."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.models.user import User
from app.services import tiktok

router = APIRouter(prefix="/tiktok", tags=["tiktok"])

Usuario = Annotated[User, Depends(get_current_user)]
Banco = Annotated[AsyncSession, Depends(get_db)]


@router.get("")
async def situacao(db: Banco, user: Usuario) -> dict:
    return await tiktok.situacao(db, user.tenant_id)


@router.post("/{piece_id}/publicado", status_code=204)
async def marcar_publicado(piece_id: uuid.UUID, db: Banco, user: Usuario) -> None:
    if not await tiktok.marcar_publicado(db, user.tenant_id, piece_id):
        raise HTTPException(404, "Esse Reels não está esperando publicação no TikTok.")
