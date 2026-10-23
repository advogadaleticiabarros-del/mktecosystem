"""Rotas da tela "Presença no Google": painel, melhorias e gestão do Perfil da Empresa."""
import uuid
from datetime import date, datetime, timezone
from typing import Annotated, Literal

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.ai.base import AIClient
from app.integrations.ai.fabrica import criar_ia
from app.integrations.ai.gemini import GeminiClient
from app.integrations.social.google_api import GoogleApiErro
from app.models.presenca_google import GooglePost, RecomendacaoStatus
from app.models.user import User
from app.services import central_google, gestao_google
from app.services.conformidade_oab import verificar_texto_oab
from app.services.diagnostico_presenca import diagnosticar
from app.services.presenca_google import buscar_perfil

router = APIRouter(prefix="/presenca", tags=["presenca"])

Usuario = Annotated[User, Depends(get_current_user)]
Banco = Annotated[AsyncSession, Depends(get_db)]


def google_transport() -> httpx.AsyncBaseTransport | None:
    """Ponto de troca para testes (Google falso). Em produção, rede de verdade."""
    return None


def get_ia() -> AIClient:
    return criar_ia() or GeminiClient(api_key=settings.GEMINI_API_KEY)


def _erro_http(erro: Exception) -> HTTPException:
    if isinstance(erro, central_google.GoogleNaoConectado):
        return HTTPException(422, str(erro))
    if isinstance(erro, gestao_google.TextoBloqueadoOab):
        return HTTPException(422, {"mensagem": "O texto fere as regras da OAB.", "problemas": erro.problemas})
    if isinstance(erro, GoogleApiErro):
        return HTTPException(502, {"mensagem": erro.mensagem, "tipo": erro.tipo, "ativar_em": erro.ativar_em})
    if isinstance(erro, ValueError):
        return HTTPException(422, str(erro))
    raise erro


async def _abrir(db: AsyncSession, user: User):
    try:
        return await central_google.abrir(db, user.tenant_id, google_transport())
    except central_google.GoogleNaoConectado as erro:
        raise _erro_http(erro) from erro


# ---------------------------------------------------------------- Painel e melhorias


async def _resposta_painel(db: AsyncSession, tenant_id: uuid.UUID) -> dict:
    painel, coletado_em = await central_google.ultimo_painel(db, tenant_id)
    if painel is None:
        return {"painel": None, "coletado_em": None, "recomendacoes": []}
    status = {
        s.chave: s.status
        for s in (await db.execute(select(RecomendacaoStatus).where(RecomendacaoStatus.tenant_id == tenant_id))).scalars()
    }
    from app.services import linkedin

    extras = [a for a in [linkedin.aviso_conexao(await linkedin.conexao(db, tenant_id), datetime.now(timezone.utc).date())] if a]
    recomendacoes = [{**r, "status": status.get(r["chave"], "pendente")} for r in extras + diagnosticar(painel)]
    return {"painel": painel, "coletado_em": coletado_em, "recomendacoes": recomendacoes}


@router.get("")
async def ver_painel(db: Banco, user: Usuario) -> dict:
    return await _resposta_painel(db, user.tenant_id)


@router.post("/atualizar")
async def atualizar(db: Banco, user: Usuario) -> dict:
    try:
        await central_google.atualizar_painel(db, user.tenant_id, transport=google_transport())
    except central_google.GoogleNaoConectado as erro:
        raise _erro_http(erro) from erro
    return await _resposta_painel(db, user.tenant_id)


class StatusIn(BaseModel):
    status: Literal["pendente", "feita", "ignorada"]


@router.put("/recomendacoes/{chave}")
async def marcar_recomendacao(chave: str, payload: StatusIn, db: Banco, user: Usuario) -> dict:
    registro = (await db.execute(select(RecomendacaoStatus).where(
        RecomendacaoStatus.tenant_id == user.tenant_id, RecomendacaoStatus.chave == chave
    ))).scalar_one_or_none()
    if registro is None:
        registro = RecomendacaoStatus(tenant_id=user.tenant_id, chave=chave, status=payload.status)
        db.add(registro)
    registro.status = payload.status
    registro.atualizado_em = datetime.now(timezone.utc)
    await db.commit()
    return {"chave": chave, "status": payload.status}


class TextoIn(BaseModel):
    texto: str
    contexto: Literal["geral", "resposta_avaliacao"] = "geral"


@router.post("/conferir-oab")
async def conferir_oab(payload: TextoIn, user: Usuario) -> dict:
    return {"problemas": verificar_texto_oab(payload.texto, payload.contexto)}


# ---------------------------------------------------------------- Avaliações


class SugerirRespostaIn(BaseModel):
    autor: str = ""
    nota: int = 5
    comentario: str = ""


@router.post("/avaliacoes/sugerir")
async def sugerir_resposta(payload: SugerirRespostaIn, user: Usuario) -> dict:
    texto = await gestao_google.sugerir_resposta(get_ia(), payload.model_dump())
    return {"texto": texto, "problemas": verificar_texto_oab(texto, "resposta_avaliacao")}


class ResponderIn(BaseModel):
    name: str
    texto: str = Field(min_length=2, max_length=4000)


@router.post("/avaliacoes/responder")
async def responder(payload: ResponderIn, db: Banco, user: Usuario) -> dict:
    api, conexao = await _abrir(db, user)
    if not payload.name.startswith(f"{conexao.page_id}/{conexao.ig_user_id}/reviews/"):
        raise HTTPException(422, "Avaliação de outro perfil.")
    try:
        await gestao_google.responder_avaliacao(api, payload.name, payload.texto)
    except Exception as erro:
        raise _erro_http(erro) from erro
    painel, _ = await central_google.ultimo_painel(db, user.tenant_id)
    if painel and painel.get("avaliacoes"):
        avaliacoes = painel["avaliacoes"]
        for a in avaliacoes["lista"]:
            if a["name"] == payload.name:
                if not a["resposta"]:
                    avaliacoes["sem_resposta"] = max(0, avaliacoes["sem_resposta"] - 1)
                a["resposta"] = payload.texto
        await central_google.salvar_secao(db, user.tenant_id, "avaliacoes", avaliacoes)
    return {"status": "ok"}


# ---------------------------------------------------------------- Perfil


class PerfilIn(BaseModel):
    descricao: str | None = None
    site: str | None = None
    servicos: list[dict] | None = None


@router.post("/perfil/sugerir-descricao")
async def sugerir_descricao(db: Banco, user: Usuario) -> dict:
    painel, _ = await central_google.ultimo_painel(db, user.tenant_id)
    if not painel or not painel.get("perfil"):
        raise HTTPException(422, "Atualize o painel antes.")
    palavras = [p["termo"] for p in painel.get("palavras_chave") or []]
    palavras += [c["termo"] for c in (painel.get("search_console") or {}).get("consultas", [])[:15]]
    texto = await gestao_google.sugerir_descricao(get_ia(), painel["perfil"], palavras)
    return {"texto": texto, "problemas": verificar_texto_oab(texto)}


@router.patch("/perfil")
async def editar_perfil(payload: PerfilIn, db: Banco, user: Usuario) -> dict:
    api, conexao = await _abrir(db, user)
    try:
        campos = await gestao_google.editar_perfil(
            api, conexao.ig_user_id, descricao=payload.descricao, site=payload.site, servicos=payload.servicos
        )
        perfil = await buscar_perfil(api, conexao.ig_user_id)
    except Exception as erro:
        raise _erro_http(erro) from erro
    await central_google.salvar_secao(db, user.tenant_id, "perfil", perfil)
    return {"alterados": campos, "perfil": perfil}


class BotaoIn(BaseModel):
    tipo: Literal["APPOINTMENT", "ONLINE_APPOINTMENT"] = "APPOINTMENT"
    url: str


@router.put("/botao")
async def definir_botao(payload: BotaoIn, db: Banco, user: Usuario) -> dict:
    api, conexao = await _abrir(db, user)
    try:
        await gestao_google.definir_botao(api, conexao.ig_user_id, payload.tipo, payload.url)
    except Exception as erro:
        raise _erro_http(erro) from erro
    return {"status": "ok"}


class FotoIn(BaseModel):
    url: str
    categoria: str = "ADDITIONAL"


@router.post("/fotos")
async def enviar_foto(payload: FotoIn, db: Banco, user: Usuario) -> dict:
    if not payload.url.startswith(settings.PUBLIC_API_URL):
        raise HTTPException(422, "Envie a foto pelo Orbit antes (o Google baixa dela).")
    api, conexao = await _abrir(db, user)
    try:
        return await gestao_google.enviar_foto(api, conexao.page_id, conexao.ig_user_id, payload.url, payload.categoria)
    except Exception as erro:
        raise _erro_http(erro) from erro


# ---------------------------------------------------------------- Posts


class PostIn(BaseModel):
    texto: str = Field(min_length=10, max_length=gestao_google.LIMITE_POST)
    botao: str | None = None
    link: str | None = None
    imagem_url: str | None = None
    publicar_em: datetime | None = None
    status: Literal["rascunho", "aprovado"] = "rascunho"


def _post_dict(p: GooglePost) -> dict:
    return {
        "id": str(p.id), "texto": p.texto, "botao": p.botao, "link": p.link, "imagem_url": p.imagem_url,
        "publicar_em": p.publicar_em, "status": p.status, "link_publicado": p.link_publicado, "erro": p.erro,
        "criado_em": p.criado_em, "problemas": verificar_texto_oab(p.texto),
    }


def _validar_post(payload: PostIn) -> None:
    if payload.botao and payload.botao not in gestao_google.BOTOES_POST:
        raise HTTPException(422, "Botão inválido.")
    if payload.botao and payload.botao != "CALL" and not payload.link:
        raise HTTPException(422, "Esse botão precisa de um link.")
    if payload.status == "aprovado":
        try:
            gestao_google._conferir(payload.texto)
        except gestao_google.TextoBloqueadoOab as erro:
            raise _erro_http(erro) from erro


@router.get("/posts")
async def listar_posts(db: Banco, user: Usuario) -> list[dict]:
    posts = (await db.execute(
        select(GooglePost).where(GooglePost.tenant_id == user.tenant_id).order_by(GooglePost.publicar_em.desc())
    )).scalars().all()
    return [_post_dict(p) for p in posts]


@router.post("/posts", status_code=201)
async def criar_post(payload: PostIn, db: Banco, user: Usuario) -> dict:
    _validar_post(payload)
    post = GooglePost(tenant_id=user.tenant_id, **payload.model_dump(exclude={"publicar_em"}),
                      publicar_em=payload.publicar_em or datetime.now(timezone.utc))
    db.add(post)
    await db.commit()
    return _post_dict(post)


async def _meu_post(db: AsyncSession, user: User, post_id: uuid.UUID) -> GooglePost:
    post = await db.get(GooglePost, post_id)
    if post is None or post.tenant_id != user.tenant_id:
        raise HTTPException(404, "Post não encontrado.")
    return post


@router.put("/posts/{post_id}")
async def editar_post(post_id: uuid.UUID, payload: PostIn, db: Banco, user: Usuario) -> dict:
    post = await _meu_post(db, user, post_id)
    if post.status == "publicado":
        raise HTTPException(422, "Post já publicado no Google.")
    _validar_post(payload)
    for campo, valor in payload.model_dump(exclude={"publicar_em"}).items():
        setattr(post, campo, valor)
    post.publicar_em = payload.publicar_em or post.publicar_em
    post.erro = None
    await db.commit()
    return _post_dict(post)


@router.delete("/posts/{post_id}", status_code=204)
async def apagar_post(post_id: uuid.UUID, db: Banco, user: Usuario) -> None:
    post = await _meu_post(db, user, post_id)
    if post.status == "publicado" and post.google_name:
        api, _ = await _abrir(db, user)
        try:
            await api.chamar("DELETE", f"https://mybusiness.googleapis.com/v4/{post.google_name}")
        except GoogleApiErro as erro:
            if erro.tipo != "nao_encontrado":
                raise _erro_http(erro) from erro
    await db.delete(post)
    await db.commit()


@router.post("/posts/{post_id}/publicar-agora")
async def publicar_agora(post_id: uuid.UUID, db: Banco, user: Usuario) -> dict:
    post = await _meu_post(db, user, post_id)
    if post.status == "publicado":
        raise HTTPException(422, "Post já publicado.")
    painel, _ = await central_google.ultimo_painel(db, user.tenant_id)
    site = central_google._site_padrao()
    try:
        no_ar = await central_google.artigo_no_ar(site, post.link, (painel or {}).get("dominio"))
    finally:
        fechar = getattr(getattr(site, "_sftp", None), "close", None)
        if fechar:
            await fechar()
    if not no_ar:
        raise HTTPException(422, "O artigo deste post ainda não está no site. Publique o artigo antes.")
    try:
        await central_google.publicar_post(db, post, google_transport())
    except Exception as erro:
        raise _erro_http(erro) from erro
    return _post_dict(post)


class TemaIn(BaseModel):
    tema: str = Field(min_length=3, max_length=500)


@router.post("/posts/sugerir")
async def sugerir_post(payload: TemaIn, user: Usuario) -> dict:
    texto = await gestao_google.sugerir_post(get_ia(), payload.tema)
    return {"texto": texto, "problemas": verificar_texto_oab(texto)}
