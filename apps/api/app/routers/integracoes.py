import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import encrypt_token
from app.core.deps import get_current_user
from app.core.security import create_access_token, decode_access_token
from app.db import get_db
from app.integrations.social.meta_client import MetaClient
from app.models.social_connection import SocialConnection
from app.models.user import User
from app.schemas.social_connection import SocialConnectionOut

router = APIRouter(prefix="/integracoes", tags=["integracoes"])

SCOPES = "pages_show_list,pages_read_engagement,instagram_basic,instagram_content_publish,business_management"


def get_meta_client() -> MetaClient:
    return MetaClient(app_id=settings.META_APP_ID, app_secret=settings.META_APP_SECRET)


@router.get("", response_model=list[SocialConnectionOut])
async def listar_conexoes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[SocialConnection]:
    result = await db.execute(
        select(SocialConnection).where(SocialConnection.tenant_id == current_user.tenant_id)
    )
    return list(result.scalars().all())


@router.get("/instagram/iniciar")
async def iniciar_conexao_instagram(
    token: Annotated[str, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RedirectResponse:
    # Navegação de página inteira (não fetch) não envia header Authorization,
    # então o token de sessão chega via query param aqui e é revalidado.
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    # o state carrega o tenant_id assinado, para o callback (público) saber a quem associar
    state = create_access_token(current_user.id)
    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "response_type": "code",
    }
    return RedirectResponse(f"https://www.facebook.com/v21.0/dialog/oauth?{urlencode(params)}")


@router.get("/instagram/callback")
async def callback_instagram(
    db: Annotated[AsyncSession, Depends(get_db)],
    code: Annotated[str, Query()],
    state: Annotated[str, Query()],
) -> RedirectResponse:
    user_id = decode_access_token(state)
    if user_id is None:
        raise HTTPException(status_code=400, detail="state inválido")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=400, detail="usuário não encontrado")

    client = get_meta_client()
    token_curto = await client.trocar_code_por_token(code, settings.META_REDIRECT_URI)
    token_longo = await client.trocar_por_token_longa_duracao(token_curto["access_token"])

    paginas = await client.buscar_paginas(token_longo["access_token"])
    if not paginas:
        raise HTTPException(status_code=422, detail="Nenhuma Página do Facebook encontrada para esta conta")

    pagina = paginas[0]
    conta_ig = await client.buscar_conta_instagram(pagina["id"], pagina["access_token"])
    if conta_ig is None:
        raise HTTPException(status_code=422, detail="Essa Página não tem uma conta Instagram Business vinculada")

    nome_conta = await client.buscar_nome_conta_instagram(conta_ig["id"], pagina["access_token"])
    expira_em = datetime.now(timezone.utc) + timedelta(seconds=token_longo.get("expires_in", 5184000))

    existente = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == user.tenant_id, SocialConnection.plataforma == "instagram"
        )
    )
    conexao = existente.scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=user.tenant_id, plataforma="instagram")
        db.add(conexao)

    conexao.page_id = pagina["id"]
    conexao.ig_user_id = conta_ig["id"]
    conexao.nome_conta = nome_conta or pagina["name"]
    conexao.access_token_encrypted = encrypt_token(pagina["access_token"])
    conexao.expira_em = expira_em
    conexao.status = "ativo"

    await db.commit()
    return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?conectado=instagram")


@router.delete("/instagram", status_code=204)
async def desconectar_instagram(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    result = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == current_user.tenant_id, SocialConnection.plataforma == "instagram"
        )
    )
    conexao = result.scalar_one_or_none()
    if conexao is not None:
        conexao.status = "desconectado"
        await db.commit()
