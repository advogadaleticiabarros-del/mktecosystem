"""Ferramentas com APIs públicas (lista public-apis, 11/11/2026): datas do calendário, CEP, CNPJ, fotos, PageSpeed,
e-mail, links curtos, conferência de links e recorte de fundo.

As que precisam de chave usam a cadastrada em Configurações (ou a variável de ambiente); sem chave respondem 409
com o nome do serviço a cadastrar.
"""
import uuid
from datetime import date, timedelta
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db import get_db
from app.integrations.brasil import DadosBrasil
from app.models.user import User
from app.services.chaves_api import obter_chave
from app.services.datas_editoriais import datas_do_periodo

router = APIRouter(prefix="/ferramentas", tags=["ferramentas"])

Usuario = Annotated[User, Depends(get_current_user)]
Banco = Annotated[AsyncSession, Depends(get_db)]


def get_transport() -> httpx.AsyncBaseTransport | None:
    """Transporte HTTP das integrações; os testes trocam por um MockTransport."""
    return None


Transporte = Annotated[httpx.AsyncBaseTransport | None, Depends(get_transport)]


async def _chave(db: AsyncSession, tenant_id: uuid.UUID, provedor: str, nome: str) -> str:
    chave = await obter_chave(db, tenant_id, provedor)
    if not chave:
        raise HTTPException(status_code=409, detail=f"Cadastre a chave do {nome} em Configurações para usar isso.")
    return chave


def _falha(erro: Exception) -> HTTPException:
    return HTTPException(status_code=502, detail=f"O serviço externo não respondeu agora ({type(erro).__name__}). "
                                                 "Tente de novo em alguns minutos.")


@router.get("/datas")
async def datas(user: Usuario, transporte: Transporte, inicio: date | None = None, fim: date | None = None) -> dict:
    inicio = inicio or date.today()
    fim = fim or inicio + timedelta(days=60)
    if fim < inicio or (fim - inicio).days > 400:
        raise HTTPException(status_code=422, detail="Período inválido (máximo de 400 dias).")
    feriados, aviso = [], None
    try:
        for ano in range(inicio.year, fim.year + 1):
            feriados += await DadosBrasil(transporte).feriados(ano)
    except httpx.HTTPError:
        aviso = "Não deu para buscar os feriados agora; as outras datas estão abaixo."
    return {"aviso": aviso, "datas": [
        {"data": d.data.isoformat(), "nome": d.nome, "tipo": d.tipo, "area": d.area, "ideia": d.ideia}
        for d in datas_do_periodo(inicio, fim, feriados)]}


@router.get("/cep/{cep}")
async def cep(cep: str, user: Usuario, transporte: Transporte) -> dict:
    try:
        endereco = await DadosBrasil(transporte).cep(cep)
    except httpx.HTTPError as e:
        raise _falha(e)
    if endereco is None:
        raise HTTPException(status_code=404, detail="CEP não encontrado.")
    return endereco.__dict__


@router.get("/cnpj/{cnpj}")
async def cnpj(cnpj: str, user: Usuario, transporte: Transporte) -> dict:
    try:
        empresa = await DadosBrasil(transporte).cnpj(cnpj)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except httpx.HTTPError as e:
        raise _falha(e)
    if empresa is None:
        raise HTTPException(status_code=404, detail="CNPJ não encontrado na Receita.")
    dados = dict(empresa.__dict__)
    dados["abertura"] = empresa.abertura.isoformat() if empresa.abertura else None
    return dados


class FotosIn(BaseModel):
    consulta: str = Field(min_length=2, max_length=100)
    quantidade: int = Field(default=15, ge=1, le=40)
    evitar: list[str] = []
    orientacao: str = "portrait"


@router.post("/fotos")
async def fotos(payload: FotosIn, db: Banco, user: Usuario) -> list[dict]:
    from app.integrations.imagens.banco import criar_banco_de_fotos

    banco = criar_banco_de_fotos(pexels=await obter_chave(db, user.tenant_id, "pexels"),
                                 pixabay=await obter_chave(db, user.tenant_id, "pixabay"))
    try:
        achadas = await banco.buscar(payload.consulta, payload.quantidade, payload.evitar, payload.orientacao)
    except RuntimeError as e:
        raise _falha(e)
    return [f.__dict__ for f in achadas]


class UrlIn(BaseModel):
    url: str = Field(pattern=r"^https?://")
    estrategia: str = Field(default="mobile", pattern="^(mobile|desktop)$")


@router.post("/pagespeed")
async def pagespeed(payload: UrlIn, db: Banco, user: Usuario, transporte: Transporte) -> dict:
    from app.integrations.site.pagespeed import PageSpeed

    try:
        medicao = await PageSpeed(await obter_chave(db, user.tenant_id, "google"), transporte).medir(
            payload.url, payload.estrategia)
    except httpx.HTTPError as e:
        raise _falha(e)
    return medicao.__dict__


class EmailIn(BaseModel):
    email: str


@router.post("/verificar-email")
async def verificar_email(payload: EmailIn, user: Usuario, transporte: Transporte) -> dict:
    from app.integrations.email.verificador import VerificadorEmail

    return (await VerificadorEmail(transporte).verificar(payload.email)).__dict__


class LinksIn(BaseModel):
    urls: list[str] = Field(min_length=1, max_length=500)


@router.post("/conferir-links")
async def conferir_links(payload: LinksIn, db: Banco, user: Usuario, transporte: Transporte) -> dict:
    from app.integrations.site.safe_browsing import SafeBrowsing

    chave = await _chave(db, user.tenant_id, "google", "Google (PageSpeed e Safe Browsing)")
    try:
        perigosos = await SafeBrowsing(chave, transporte).conferir(payload.urls)
    except httpx.HTTPError as e:
        raise _falha(e)
    return {"seguro": not perigosos, "perigosos": perigosos}


class EncurtarIn(BaseModel):
    url: str = Field(pattern=r"^https?://")


@router.post("/encurtar")
async def encurtar(payload: EncurtarIn, db: Banco, user: Usuario, transporte: Transporte) -> dict:
    from app.integrations.links.bitly import Bitly

    bitly = Bitly(await _chave(db, user.tenant_id, "bitly", "Bitly"), transporte)
    try:
        return {"link": await bitly.encurtar(payload.url)}
    except httpx.HTTPError as e:
        raise _falha(e)


@router.get("/cliques")
async def cliques(db: Banco, user: Usuario, transporte: Transporte, link: str = Query(min_length=5)) -> dict:
    from app.integrations.links.bitly import Bitly

    bitly = Bitly(await _chave(db, user.tenant_id, "bitly", "Bitly"), transporte)
    try:
        return {"link": link, "cliques": await bitly.cliques(link)}
    except httpx.HTTPError as e:
        raise _falha(e)


@router.post("/recortar")
async def recortar(arquivo: UploadFile, db: Banco, user: Usuario, transporte: Transporte) -> Response:
    from app.integrations.imagens.remove_bg import RemoveBg, SemCredito

    imagem = await arquivo.read()
    if not imagem or len(imagem) > 12 * 1024 * 1024:
        raise HTTPException(status_code=422, detail="Envie uma imagem de até 12 MB.")
    removedor = RemoveBg(await _chave(db, user.tenant_id, "removebg", "remove.bg"), transporte)
    try:
        png = await removedor.recortar(imagem)
    except SemCredito as e:
        raise HTTPException(status_code=402, detail=str(e))
    except httpx.HTTPError as e:
        raise _falha(e)
    return Response(content=png, media_type="image/png")
