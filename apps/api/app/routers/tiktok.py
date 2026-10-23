"""Tela TikTok: conexão, fila própria (remarcar/tirar), envios e rascunhos esperando quem publique pelo app."""
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
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


class Vaga(BaseModel):
    data: date | None = None  # None tira o vídeo do TikTok
    horario: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")


@router.put("/{piece_id}/agenda", status_code=204)
async def remarcar(piece_id: uuid.UUID, vaga: Vaga, db: Banco, user: Usuario) -> None:
    if not await tiktok.remarcar(db, user.tenant_id, piece_id, vaga.data, vaga.horario):
        raise HTTPException(404, "Esse vídeo não está esperando na fila do TikTok.")


@router.post("/{piece_id}/publicado", status_code=204)
async def marcar_publicado(piece_id: uuid.UUID, db: Banco, user: Usuario) -> None:
    if not await tiktok.marcar_publicado(db, user.tenant_id, piece_id):
        raise HTTPException(404, "Esse Reels não está esperando publicação no TikTok.")
