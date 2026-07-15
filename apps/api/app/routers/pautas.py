from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.base import AIClient
from app.integrations.ai.gemini import GeminiClient
from app.integrations.sources.cnj import fetch_cnj
from app.integrations.sources.stf import fetch_stf
from app.integrations.sources.tst import fetch_tst
from app.models.pauta import Pauta
from app.models.tenant import TenantConfig
from app.models.user import User
from app.schemas.pauta import PautaManualCreate, PautaOut

router = APIRouter(prefix="/pautas", tags=["pautas"])


def get_ai_client() -> AIClient:
    return GeminiClient(api_key=settings.GEMINI_API_KEY)


EXTRACTION_PROMPT = """\
Você é assistente de uma advogada com áreas de prática: {areas}.

Leia o material abaixo, extraído de fontes jurídicas oficiais (STF, TST, CNJ), e
identifique até 8 temas relevantes.

Para cada tema, retorne:
- titulo: nome curto e claro do tema
- angulo: "direitos" (oportunidade para o cliente) ou "sinceridade" (riscos/cautela)
- area: área do direito
- fonte: qual fonte trouxe o tema (STF, TST ou CNJ)
- relevante_para_conteudo: true se o tema é simples de explicar, trabalhista ou
  previdenciário, e tem potencial de atrair cliente; false se é relevante
  juridicamente mas técnico/processual demais para virar post.

Responda em JSON: {{"pautas": [...]}}

MATERIAL:
{material}
"""


@router.post("/buscar", response_model=list[PautaOut])
async def buscar_pautas(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Pauta]:
    ai_client = get_ai_client()
    docs = [await fetch_stf(), await fetch_tst(), await fetch_cnj()]
    material = "\n\n".join(f"=== {d.fonte} ===\n{d.texto}" for d in docs)

    result = await db.execute(
        select(TenantConfig).where(TenantConfig.tenant_id == current_user.tenant_id)
    )
    tenant_config = result.scalar_one_or_none()
    areas = ", ".join(tenant_config.voz.get("areas", [])) if tenant_config else ""

    prompt = EXTRACTION_PROMPT.format(areas=areas, material=material)
    extraction = await ai_client.generate_json(prompt)

    pautas = []
    for item in extraction.get("pautas", []):
        pauta = Pauta(
            tenant_id=current_user.tenant_id,
            titulo=item["titulo"],
            angulo=item["angulo"],
            area=item["area"],
            origem="buscada",
            fonte=item["fonte"],
            relevante_para_conteudo=item["relevante_para_conteudo"],
            status="sugerida",
        )
        db.add(pauta)
        pautas.append(pauta)

    await db.commit()
    for p in pautas:
        await db.refresh(p)
    return pautas


@router.get("", response_model=list[PautaOut])
async def listar_pautas(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    relevante_para_conteudo: Annotated[bool | None, Query()] = None,
) -> list[Pauta]:
    query = select(Pauta).where(Pauta.tenant_id == current_user.tenant_id)
    if relevante_para_conteudo is not None:
        query = query.where(Pauta.relevante_para_conteudo == relevante_para_conteudo)
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
        origem="manual",
        fonte="manual",
        relevante_para_conteudo=True,
        status="sugerida",
    )
    db.add(pauta)
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
