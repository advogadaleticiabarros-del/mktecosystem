import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.base import AIClient
from app.integrations.ai.gemini import GeminiClient
from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.tenant import TenantConfig
from app.models.user import User
from app.schemas.content_piece import ContentPieceOut, ContentPieceUpdate, GerarRequest

router = APIRouter(prefix="/content", tags=["content"])


def get_ai_client() -> AIClient:
    return GeminiClient(api_key=settings.GEMINI_API_KEY)


VOZ_BLOCK = """\
REGRAS DE VOZ (inegociáveis, sempre aplicar):
{principios}

PROIBIÇÕES:
{proibicoes}

Identificação: {oab}
"""

PROMPTS = {
    "artigo": (
        "Escreva um artigo de blog completo (1200-1800 palavras) sobre '{titulo}' "
        "(ângulo: {angulo}, área: {area}). Estrutura: gancho, H2s com keyword, "
        "Perguntas frequentes, Leia também, 1 caso típico do escritório, 2 CTAs.\n"
        "{voz}\nResponda em JSON: {{\"titulo\": str, \"html\": str}}"
    ),
    "carrossel": (
        "Crie um carrossel de 5 slides de Instagram resumindo o tema '{titulo}' "
        "(ângulo: {angulo}). Cada slide: uma ideia curta e direta.\n"
        "{voz}\nResponda em JSON: {{\"slides\": [str, str, str, str, str]}}"
    ),
    "legenda": (
        "Escreva a legenda do post de Instagram sobre '{titulo}' (ângulo: {angulo}). "
        "Gancho + 3 parágrafos + chamada para o blog + gancho do próximo post + "
        "7 hashtags do setor.\n"
        "{voz}\nResponda em JSON: {{\"texto\": str}}"
    ),
    "stories": (
        "Crie um roteiro de 3 stories (9:16) sobre '{titulo}' (ângulo: {angulo}): "
        "anúncio do tema, ponto principal, chamada para o link do blog.\n"
        "{voz}\nResponda em JSON: {{\"roteiro\": [str, str, str]}}"
    ),
}


@router.post("/gerar", response_model=list[ContentPieceOut])
async def gerar_conteudo(
    payload: GerarRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ContentPiece]:
    ai_client = get_ai_client()

    pauta_result = await db.execute(
        select(Pauta).where(
            Pauta.id == payload.pauta_id, Pauta.tenant_id == current_user.tenant_id
        )
    )
    pauta = pauta_result.scalar_one_or_none()
    if pauta is None:
        raise HTTPException(status_code=404, detail="Pauta not found")

    config_result = await db.execute(
        select(TenantConfig).where(TenantConfig.tenant_id == current_user.tenant_id)
    )
    tenant_config = config_result.scalar_one_or_none()
    voz_data = tenant_config.voz if tenant_config else {}
    voz_block = VOZ_BLOCK.format(
        principios="\n".join(f"- {p}" for p in voz_data.get("principios", [])),
        proibicoes="\n".join(f"- {p}" for p in voz_data.get("proibicoes", [])),
        oab=voz_data.get("oab", ""),
    )

    pieces = []
    for tipo, template in PROMPTS.items():
        prompt = template.format(
            titulo=pauta.titulo, angulo=pauta.angulo, area=pauta.area, voz=voz_block
        )
        corpo = await ai_client.generate_json(prompt)
        piece = ContentPiece(
            tenant_id=current_user.tenant_id,
            pauta_id=pauta.id,
            tipo=tipo,
            corpo=corpo,
            status="rascunho",
            versao=1,
        )
        db.add(piece)
        pieces.append(piece)

    await db.commit()
    for p in pieces:
        await db.refresh(p)
    return pieces


@router.patch("/{piece_id}", response_model=ContentPieceOut)
async def atualizar_content_piece(
    piece_id: str,
    payload: ContentPieceUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ContentPiece:
    try:
        piece_uuid = uuid.UUID(piece_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid piece_id format")

    result = await db.execute(
        select(ContentPiece).where(
            ContentPiece.id == piece_uuid, ContentPiece.tenant_id == current_user.tenant_id
        )
    )
    piece = result.scalar_one_or_none()
    if piece is None:
        raise HTTPException(status_code=404, detail="Content piece not found")

    if payload.corpo is not None:
        piece.corpo = payload.corpo
    if payload.status is not None:
        piece.status = payload.status

    if payload.status == "aprovado":
        pauta_result = await db.execute(select(Pauta).where(Pauta.id == piece.pauta_id))
        pauta = pauta_result.scalar_one()
        db.add(
            MarketingMemory(
                tenant_id=current_user.tenant_id,
                content_piece_id=piece.id,
                tema=pauta.titulo,
                angulo=pauta.angulo,
                formato=piece.tipo,
                metricas={},
                aprendizado=None,
            )
        )

    await db.commit()
    await db.refresh(piece)
    return piece
