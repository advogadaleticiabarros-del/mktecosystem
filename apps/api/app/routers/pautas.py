import uuid
from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.groq_client import GroqClient
from app.integrations.search.tavily_client import TavilyClient
from app.models.pauta import Pauta
from app.models.user import User
from app.schemas.pauta import PautaManualCreate, PautaOut, PautaStatusUpdate, PedidoJornalista
from app.services.chaves_api import obter_chave
from app.services.jornalista import apurar, criar_jornalista
from app.services.verificacao_atualidade import verificar_atualidade

router = APIRouter(prefix="/pautas", tags=["pautas"])


async def _verificar_e_marcar(pauta: Pauta) -> None:
    """Roda a verificação de atualidade e marca o alerta na própria pauta.

    Silenciosa por design: se a Tavily não estiver configurada ou a
    verificação falhar, a pauta segue sem alerta, nunca bloqueia a criação.
    """
    if not settings.TAVILY_API_KEY:
        return
    alerta, verificado_em = await verificar_atualidade(
        titulo=pauta.titulo,
        area=pauta.area,
        ai_client=GroqClient(api_key=settings.GROQ_API_KEY),
        tavily_client=TavilyClient(api_key=settings.TAVILY_API_KEY),
    )
    pauta.alerta_atualidade = alerta
    pauta.verificado_em = verificado_em


async def _jornalista(db: AsyncSession, tenant_id: uuid.UUID):
    jornalista = criar_jornalista(openai_key=await obter_chave(db, tenant_id, "openai"))
    if jornalista is None:
        raise HTTPException(status_code=503, detail="Jornalista sem chave de IA (configure GEMINI_API_KEY).")
    return jornalista


@router.post("/buscar", response_model=list[PautaOut])
async def buscar_pautas(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Pauta]:
    """Roda a ronda do Jornalista na hora (a mesma que o agendador faz às 07h40)."""
    buscador, redator = await _jornalista(db, current_user.tenant_id)
    return await apurar(db, current_user.tenant_id, buscador, redator, date.today())


@router.post("/jornalista", response_model=list[PautaOut])
async def pedir_ao_jornalista(
    payload: PedidoJornalista,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Pauta]:
    """Pede ao Jornalista que investigue um assunto específico (últimos 30 dias)."""
    buscador, redator = await _jornalista(db, current_user.tenant_id)
    return await apurar(db, current_user.tenant_id, buscador, redator, date.today(), foco=payload.foco.strip())


@router.get("", response_model=list[PautaOut])
async def listar_pautas(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    relevante_para_conteudo: Annotated[bool | None, Query()] = None,
    status: Annotated[list[str] | None, Query()] = None,
    data_inicio: Annotated[date | None, Query()] = None,
    data_fim: Annotated[date | None, Query()] = None,
) -> list[Pauta]:
    query = select(Pauta).where(Pauta.tenant_id == current_user.tenant_id)
    if relevante_para_conteudo is not None:
        query = query.where(Pauta.relevante_para_conteudo == relevante_para_conteudo)
    if status:
        query = query.where(Pauta.status.in_(status))
    if data_inicio is not None:
        query = query.where(Pauta.data_editorial >= data_inicio)
    if data_fim is not None:
        query = query.where(Pauta.data_editorial <= data_fim)
    if data_inicio is not None or data_fim is not None:
        query = query.order_by(Pauta.data_editorial.desc())
    else:
        query = query.order_by(Pauta.criado_em.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("", response_model=PautaOut, status_code=201)
async def criar_pauta_manual(
    payload: PautaManualCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Pauta:
    pauta = Pauta(
        tenant_id=current_user.tenant_id,
        titulo=payload.titulo,
        angulo=payload.angulo,
        area=payload.area,
        origem=payload.origem,
        fonte="chatgpt-radar" if payload.origem.startswith("radar_juridico") else "manual",
        relevante_para_conteudo=True,
        status="sugerida",
        conteudo_bruto=payload.conteudo_bruto,
        data_editorial=payload.data_editorial or date.today(),
    )
    db.add(pauta)
    await db.flush()
    await _verificar_e_marcar(pauta)
    await db.commit()
    await db.refresh(pauta)
    return pauta


@router.get("/resumo-diario", response_model=list[PautaOut])
async def resumo_diario(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Pauta]:
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    query = (
        select(Pauta)
        .where(Pauta.tenant_id == current_user.tenant_id)
        .where(Pauta.criado_em >= since)
        .order_by(Pauta.area, Pauta.criado_em.desc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())


@router.patch("/{pauta_id}", response_model=PautaOut)
async def mudar_status(
    pauta_id: uuid.UUID,
    payload: PautaStatusUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Pauta:
    pauta = (
        await db.execute(select(Pauta).where(Pauta.id == pauta_id, Pauta.tenant_id == current_user.tenant_id))
    ).scalar_one_or_none()
    if pauta is None:
        raise HTTPException(status_code=404, detail="Pauta não encontrada")
    pauta.status = payload.status
    await db.commit()
    await db.refresh(pauta)
    return pauta
