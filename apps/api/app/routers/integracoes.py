import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import encrypt_token
from app.core.deps import get_current_user
from app.core.security import create_access_token, decode_access_token
from app.db import get_db
from app.integrations.social.google_business_client import GoogleBusinessClient
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


async def _salvar_conexao_a_partir_da_pagina(
    db: AsyncSession,
    tenant_id: uuid.UUID,
    client: MetaClient,
    pagina: dict,
    expira_em: datetime | None,
) -> SocialConnection:
    conta_ig = await client.buscar_conta_instagram(pagina["id"], pagina["access_token"])
    if conta_ig is None:
        raise HTTPException(status_code=422, detail="Essa Página não tem uma conta Instagram Business vinculada")

    nome_conta = await client.buscar_nome_conta_instagram(conta_ig["id"], pagina["access_token"])

    existente = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == tenant_id, SocialConnection.plataforma == "instagram"
        )
    )
    conexao = existente.scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=tenant_id, plataforma="instagram")
        db.add(conexao)

    conexao.page_id = pagina["id"]
    conexao.ig_user_id = conta_ig["id"]
    conexao.nome_conta = nome_conta or pagina["name"]
    conexao.access_token_encrypted = encrypt_token(pagina["access_token"])
    conexao.expira_em = expira_em
    conexao.status = "ativo"

    await db.commit()
    return conexao


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

    expira_em = datetime.now(timezone.utc) + timedelta(seconds=token_longo.get("expires_in", 5184000))
    await _salvar_conexao_a_partir_da_pagina(db, user.tenant_id, client, paginas[0], expira_em)
    return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?conectado=instagram")


class TokenManualIn(BaseModel):
    access_token: str


@router.post("/instagram/token", response_model=SocialConnectionOut)
async def conectar_com_token_manual(
    payload: TokenManualIn,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SocialConnection:
    """Conecta usando um token de usuário do sistema gerado no Gerenciador de
    Negócios — alternativa ao fluxo OAuth quando o app ainda não tem os
    escopos avançados liberados pela revisão da Meta."""
    client = get_meta_client()
    paginas = await client.buscar_paginas(payload.access_token)
    if not paginas:
        raise HTTPException(
            status_code=422,
            detail="Nenhuma Página do Facebook encontrada para esse token. Confirme que o usuário "
            "do sistema tem a Página atribuída com controle total.",
        )
    # Tokens de usuário do sistema não expiram; sem data de expiração conhecida.
    return await _salvar_conexao_a_partir_da_pagina(db, current_user.tenant_id, client, paginas[0], None)


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


# Perfil da Empresa (ler e gerir), Analytics (ler e marcar eventos principais) e Search Console (ler e sitemap).
GOOGLE_SCOPES = " ".join([
    "https://www.googleapis.com/auth/business.manage",
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/analytics.edit",  # marcar eventos de contato como principais
    "https://www.googleapis.com/auth/webmasters",
])


def get_google_client() -> GoogleBusinessClient:
    return GoogleBusinessClient(
        client_id=settings.GOOGLE_CLIENT_ID, client_secret=settings.GOOGLE_CLIENT_SECRET
    )


@router.get("/google-business/iniciar")
async def iniciar_conexao_google_business(
    token: Annotated[str, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RedirectResponse:
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    state = create_access_token(current_user.id)
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "scope": GOOGLE_SCOPES,
        "state": state,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    }
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}")


@router.get("/google-business/callback")
async def callback_google_business(
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

    client = get_google_client()
    tokens = await client.trocar_code_por_tokens(code, settings.GOOGLE_REDIRECT_URI)

    contas = await client.listar_contas(tokens["access_token"])
    if not contas:
        raise HTTPException(status_code=422, detail="Nenhuma conta do Google Meu Negócio encontrada")
    conta = contas[0]

    locais = await client.listar_locais(tokens["access_token"], conta["name"])
    if not locais:
        raise HTTPException(status_code=422, detail="Nenhum local encontrado nessa conta")
    local = locais[0]

    existente = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == user.tenant_id,
            SocialConnection.plataforma == "google_business",
        )
    )
    conexao = existente.scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=user.tenant_id, plataforma="google_business")
        db.add(conexao)

    conexao.page_id = conta["name"]
    conexao.ig_user_id = local["name"]
    conexao.nome_conta = local.get("title", conta.get("accountName", ""))
    conexao.access_token_encrypted = encrypt_token(tokens["refresh_token"])
    conexao.expira_em = None
    conexao.status = "ativo"

    await db.commit()
    return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?conectado=google_business")


@router.delete("/google-business", status_code=204)
async def desconectar_google_business(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    result = await db.execute(
        select(SocialConnection).where(
            SocialConnection.tenant_id == current_user.tenant_id,
            SocialConnection.plataforma == "google_business",
        )
    )
    conexao = result.scalar_one_or_none()
    if conexao is not None:
        conexao.status = "desconectado"
        await db.commit()


# ---------------------------------------------------------------- LinkedIn (perfil pessoal da Dra.)


def linkedin_transport():
    """Ponto de troca para testes (LinkedIn falso). Em produção, rede de verdade."""
    return None


def _redirect_linkedin() -> str:
    return f"{settings.PUBLIC_API_URL}/integracoes/linkedin/callback"


async def _credenciais_linkedin(db: AsyncSession, tenant_id: uuid.UUID) -> tuple[str, str]:
    from app.services.chaves_api import obter_chave, separar_linkedin

    chave = await obter_chave(db, tenant_id, "linkedin")
    if not chave:
        raise HTTPException(status_code=422, detail="Cadastre antes as chaves do LinkedIn em Configurações.")
    return separar_linkedin(chave)


@router.get("/linkedin/iniciar")
async def iniciar_conexao_linkedin(token: Annotated[str, Query()], db: Annotated[AsyncSession, Depends(get_db)]) -> RedirectResponse:
    from app.integrations.social import linkedin_api

    user_id = decode_access_token(token)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none() if user_id else None
    if user is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    client_id, _ = await _credenciais_linkedin(db, user.tenant_id)
    return RedirectResponse(linkedin_api.url_autorizacao(client_id, _redirect_linkedin(), create_access_token(user.id)))


@router.get("/linkedin/callback")
async def callback_linkedin(
    db: Annotated[AsyncSession, Depends(get_db)],
    state: Annotated[str, Query()],
    code: Annotated[str | None, Query()] = None,
    error: Annotated[str | None, Query()] = None,
) -> RedirectResponse:
    from app.integrations.social import linkedin_api

    if error or not code:
        return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?erro=linkedin")
    user_id = decode_access_token(state)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none() if user_id else None
    if user is None:
        raise HTTPException(status_code=400, detail="state inválido")
    client_id, client_secret = await _credenciais_linkedin(db, user.tenant_id)
    transport = linkedin_transport()
    tokens = await linkedin_api.trocar_code(client_id, client_secret, code, _redirect_linkedin(), transport)
    perfil = await linkedin_api.perfil(tokens["access_token"], transport)

    conexao = (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == user.tenant_id, SocialConnection.plataforma == "linkedin"
    ))).scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=user.tenant_id, plataforma="linkedin")
        db.add(conexao)
    conexao.page_id = f"urn:li:person:{perfil['sub']}"
    conexao.ig_user_id = ""
    conexao.nome_conta = perfil.get("name") or "LinkedIn"
    conexao.access_token_encrypted = encrypt_token(tokens["access_token"])
    conexao.expira_em = datetime.now(timezone.utc) + timedelta(seconds=int(tokens.get("expires_in", 5184000)))
    conexao.status = "ativo"
    await db.commit()
    return RedirectResponse(f"{settings.FRONTEND_URL}/visao-geral?conectado=linkedin")


@router.delete("/linkedin", status_code=204)
async def desconectar_linkedin(db: Annotated[AsyncSession, Depends(get_db)],
                               current_user: Annotated[User, Depends(get_current_user)]) -> None:
    conexao = (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == current_user.tenant_id, SocialConnection.plataforma == "linkedin"
    ))).scalar_one_or_none()
    if conexao is not None:
        conexao.status = "desconectado"
        await db.commit()
