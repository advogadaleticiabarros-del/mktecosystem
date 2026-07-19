import uuid
from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.models.scheduled_post import ScheduledPost
from app.models.user import User

router = APIRouter(prefix="/calendario", tags=["calendario"])

CANAIS = {"instagram", "blog", "email"}
FORMATOS = {"carrossel", "post", "story", "artigo", "newsletter"}
STATUS = {"planejado", "pronto", "publicado"}


class AgendamentoCreate(BaseModel):
    titulo: str
    canal: str = "instagram"
    formato: str = "post"
    data_agendada: date
    horario: str = "11:00"


class AgendamentoUpdate(BaseModel):
    titulo: str | None = None
    canal: str | None = None
    formato: str | None = None
    data_agendada: date | None = None
    horario: str | None = None
    status: str | None = None


class AgendamentoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content_piece_id: uuid.UUID | None
    titulo: str
    canal: str
    formato: str
    data_agendada: date
    horario: str
    status: str


def _validar(canal: str | None, formato: str | None, status: str | None) -> None:
    if canal is not None and canal not in CANAIS:
        raise HTTPException(status_code=422, detail=f"Canal inválido: {canal}")
    if formato is not None and formato not in FORMATOS:
        raise HTTPException(status_code=422, detail=f"Formato inválido: {formato}")
    if status is not None and status not in STATUS:
        raise HTTPException(status_code=422, detail=f"Status inválido: {status}")


@router.get("", response_model=list[AgendamentoOut])
async def listar_mes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    mes: Annotated[str | None, Query(pattern=r"^\d{4}-\d{2}$")] = None,
) -> list[ScheduledPost]:
    if mes:
        ano, mes_num = int(mes[:4]), int(mes[5:7])
        inicio = date(ano, mes_num, 1)
    else:
        hoje = date.today()
        inicio = date(hoje.year, hoje.month, 1)
    fim = (inicio + timedelta(days=32)).replace(day=1)

    result = await db.execute(
        select(ScheduledPost)
        .where(
            ScheduledPost.tenant_id == current_user.tenant_id,
            ScheduledPost.data_agendada >= inicio,
            ScheduledPost.data_agendada < fim,
        )
        .order_by(ScheduledPost.data_agendada, ScheduledPost.horario)
    )
    return list(result.scalars().all())


@router.post("", response_model=AgendamentoOut, status_code=201)
async def criar_agendamento(
    payload: AgendamentoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ScheduledPost:
    _validar(payload.canal, payload.formato, None)
    agendamento = ScheduledPost(
        tenant_id=current_user.tenant_id,
        titulo=payload.titulo,
        canal=payload.canal,
        formato=payload.formato,
        data_agendada=payload.data_agendada,
        horario=payload.horario,
    )
    db.add(agendamento)
    await db.commit()
    await db.refresh(agendamento)
    return agendamento


@router.patch("/{agendamento_id}", response_model=AgendamentoOut)
async def atualizar_agendamento(
    agendamento_id: uuid.UUID,
    payload: AgendamentoUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ScheduledPost:
    _validar(payload.canal, payload.formato, payload.status)
    result = await db.execute(
        select(ScheduledPost).where(
            ScheduledPost.id == agendamento_id,
            ScheduledPost.tenant_id == current_user.tenant_id,
        )
    )
    agendamento = result.scalar_one_or_none()
    if agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    for campo in ("titulo", "canal", "formato", "data_agendada", "horario", "status"):
        valor = getattr(payload, campo)
        if valor is not None:
            setattr(agendamento, campo, valor)

    await db.commit()
    await db.refresh(agendamento)
    return agendamento


@router.delete("/{agendamento_id}", status_code=204)
async def remover_agendamento(
    agendamento_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    result = await db.execute(
        select(ScheduledPost).where(
            ScheduledPost.id == agendamento_id,
            ScheduledPost.tenant_id == current_user.tenant_id,
        )
    )
    agendamento = result.scalar_one_or_none()
    if agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    await db.delete(agendamento)
    await db.commit()
