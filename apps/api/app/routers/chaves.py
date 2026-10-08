from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.models.user import User
from app.services.chaves_api import PROVEDORES, ChaveRecusada, remover_chave, salvar_chave, status_chaves

router = APIRouter(prefix="/chaves", tags=["chaves"])


class ChaveIn(BaseModel):
    chave: str


def _provedor(provedor: str) -> str:
    if provedor not in PROVEDORES:
        raise HTTPException(status_code=404, detail="Serviço desconhecido")
    return provedor


@router.get("")
async def listar(
    db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)]
) -> list[dict]:
    return await status_chaves(db, current_user.tenant_id)


@router.put("/{provedor}")
async def salvar(
    provedor: str,
    payload: ChaveIn,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Testa a chave no serviço e guarda criptografada. A resposta nunca traz a chave."""
    try:
        return await salvar_chave(db, current_user.tenant_id, _provedor(provedor), payload.chave)
    except ChaveRecusada as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{provedor}", status_code=204)
async def remover(
    provedor: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    await remover_chave(db, current_user.tenant_id, _provedor(provedor))
    return Response(status_code=204)
