from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.models.user import User
from app.services.analise_instagram import montar_analise
from app.services.coleta_instagram import coletar_instagram

router = APIRouter(prefix="/analise", tags=["analise"])


@router.get("/instagram")
async def analise_instagram(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return await montar_analise(db, current_user.tenant_id)


@router.post("/instagram/atualizar")
async def atualizar_analise_instagram(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Busca agora os dados no Instagram (a coleta automática roda todo dia às 06h)."""
    await coletar_instagram(db, tenant_id=current_user.tenant_id)
    return await montar_analise(db, current_user.tenant_id)
