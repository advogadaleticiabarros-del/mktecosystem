"""Tela Desempenho: todos os canais numa visão só (dados das coletas diárias, sem chamar API externa)."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.models.user import User
from app.services.desempenho import montar_desempenho

router = APIRouter(prefix="/desempenho", tags=["desempenho"])


@router.get("")
async def desempenho(db: Annotated[AsyncSession, Depends(get_db)],
                     user: Annotated[User, Depends(get_current_user)]) -> dict:
    return await montar_desempenho(db, user.tenant_id)
