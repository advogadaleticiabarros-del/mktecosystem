"""Rotas da tela LinkedIn: situação da conexão e fila de posts (rascunho → aprovado → publicado)."""
import uuid
from datetime import datetime, timezone
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.social.linkedin_api import LinkedInErro, link_do_post
from app.models.presenca_google import LinkedInPost
from app.models.user import User
from app.routers.integracoes import linkedin_transport
from app.routers.presenca import get_ia
from app.services import linkedin
from app.services.central_google import _site_padrao, artigo_no_ar
from app.services.conformidade_oab import verificar_texto_oab

router = APIRouter(prefix="/linkedin", tags=["linkedin"])

Usuario = Annotated[User, Depends(get_current_user)]
Banco = Annotated[AsyncSession, Depends(get_db)]


@router.get("")
async def situacao(db: Banco, user: Usuario) -> dict:
    c = await linkedin.conexao(db, user.tenant_id)
    if c is None:
        return {"conectado": False}
    hoje = datetime.now(timezone.utc).date()  # expira_em é UTC: as duas datas na mesma referência
    expira = c.expira_em if c.expira_em is None or c.expira_em.tzinfo else c.expira_em.replace(tzinfo=timezone.utc)
    dias = (expira.astimezone(timezone.utc).date() - hoje).days if expira else None
    return {"conectado": True, "nome": c.nome_conta, "expira_em": c.expira_em, "dias_para_vencer": dias,
            "aviso": linkedin.aviso_conexao(c, hoje)}


class PostIn(BaseModel):
    texto: str = Field(min_length=10, max_length=linkedin.LIMITE_TEXTO)
    link: str | None = None
    publicar_em: datetime | None = None
    status: Literal["rascunho", "aprovado"] = "rascunho"


def _dict(p: LinkedInPost) -> dict:
    return {
        "id": str(p.id), "texto": p.texto, "link": p.link, "publicar_em": p.publicar_em, "status": p.status,
        "erro": p.erro, "criado_em": p.criado_em, "problemas": verificar_texto_oab(p.texto),
        "link_publicado": link_do_post(p.post_urn) if p.post_urn else None,
    }


def _validar(payload: PostIn) -> None:
    if payload.status == "aprovado":
        problemas = [x for x in verificar_texto_oab(payload.texto) if x["nivel"] == "bloqueia"]
        if problemas:
            raise HTTPException(422, {"mensagem": "O texto fere as regras da OAB.", "problemas": problemas})


async def _meu(db: AsyncSession, user: User, post_id: uuid.UUID) -> LinkedInPost:
    post = await db.get(LinkedInPost, post_id)
    if post is None or post.tenant_id != user.tenant_id:
        raise HTTPException(404, "Post não encontrado.")
    return post


@router.get("/posts")
async def listar(db: Banco, user: Usuario) -> list[dict]:
    posts = (await db.execute(select(LinkedInPost).where(LinkedInPost.tenant_id == user.tenant_id)
                              .order_by(LinkedInPost.publicar_em.desc()))).scalars().all()
    return [_dict(p) for p in posts]


@router.post("/posts", status_code=201)
async def criar(payload: PostIn, db: Banco, user: Usuario) -> dict:
    _validar(payload)
    post = LinkedInPost(tenant_id=user.tenant_id, texto=payload.texto, link=payload.link or None, status=payload.status,
                        publicar_em=payload.publicar_em or datetime.now(timezone.utc))
    db.add(post)
    await db.commit()
    return _dict(post)


@router.put("/posts/{post_id}")
async def editar(post_id: uuid.UUID, payload: PostIn, db: Banco, user: Usuario) -> dict:
    post = await _meu(db, user, post_id)
    if post.status == "publicado":
        raise HTTPException(422, "Post já publicado no LinkedIn.")
    _validar(payload)
    post.texto, post.link, post.status = payload.texto, payload.link or None, payload.status
    post.publicar_em = payload.publicar_em or post.publicar_em
    post.erro = None
    await db.commit()
    return _dict(post)


@router.delete("/posts/{post_id}", status_code=204)
async def apagar(post_id: uuid.UUID, db: Banco, user: Usuario) -> None:
    post = await _meu(db, user, post_id)
    if post.status == "publicado" and post.post_urn:
        try:
            api, _ = await linkedin.abrir(db, user.tenant_id, linkedin_transport())
            await api.apagar(post.post_urn)
        except (linkedin.LinkedInNaoConectado, LinkedInErro) as erro:
            if getattr(erro, "status", 0) != 404:
                raise HTTPException(422, f"Não deu para apagar no LinkedIn: {erro}") from erro
    await db.delete(post)
    await db.commit()


@router.post("/posts/{post_id}/publicar-agora")
async def publicar_agora(post_id: uuid.UUID, db: Banco, user: Usuario) -> dict:
    post = await _meu(db, user, post_id)
    if post.status == "publicado":
        raise HTTPException(422, "Post já publicado.")
    site = _site_padrao()
    try:
        if not await artigo_no_ar(site, post.link, linkedin.DOMINIO):
            raise HTTPException(422, "O artigo deste post ainda não está no site. Publique o artigo antes.")
        await linkedin.publicar_post(db, post, linkedin_transport(), site)
    except linkedin.LinkedInNaoConectado as erro:
        raise HTTPException(422, str(erro)) from erro
    except LinkedInErro as erro:
        raise HTTPException(502, erro.mensagem) from erro
    except ValueError as erro:
        raise HTTPException(422, str(erro)) from erro
    finally:
        fechar = getattr(getattr(site, "_sftp", None), "close", None)
        if fechar:
            await fechar()
    return _dict(post)


class TemaIn(BaseModel):
    tema: str = Field(min_length=3, max_length=500)


@router.post("/posts/sugerir")
async def sugerir(payload: TemaIn, user: Usuario) -> dict:
    texto = await linkedin.sugerir_post(get_ia(), payload.tema)
    return {"texto": texto, "problemas": verificar_texto_oab(texto)}
