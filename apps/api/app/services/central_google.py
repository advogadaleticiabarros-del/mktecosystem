"""Central do Google: liga a conexão salva (refresh token) às coletas e às escritas.

Interface:
- `await abrir(db, tenant_id)` -> `(api, conexao)` com o access token renovado, ou levanta
  `GoogleNaoConectado`;
- `await atualizar_painel(db, tenant_id)`: coleta tudo (Google + site), salva e devolve o painel;
- `await ultimo_painel(db, tenant_id)` -> (painel, coletado_em) ou (None, None);
- `await atualizar_todos(db)` e `await publicar_posts_prontos(db, agora)`: jobs do agendador.

`transport` (httpx) e `site` (adaptador de `checagem_site`) são injetáveis para teste.
"""
import logging
import uuid
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.crypto import decrypt_token
from app.integrations.social.google_api import GoogleApi, GoogleApiErro
from app.integrations.social.google_business_client import GoogleBusinessClient
from app.models.presenca_google import GooglePost
from app.models.social_connection import SocialConnection
from app.models.social_metric import SocialMetric
from app.services import gestao_google
from app.services.checagem_site import Site, SiteSftp, checar_site
from app.services.presenca_google import EVENTOS_CONTATO, coletar_painel

logger = logging.getLogger(__name__)

TIPO_PAINEL = "google_painel"
MAX_TENTATIVAS_POST = 3


class GoogleNaoConectado(Exception):
    pass


async def _conexao(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection:
    conexao = (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == tenant_id,
        SocialConnection.plataforma == "google_business",
        SocialConnection.status == "ativo",
    ))).scalar_one_or_none()
    if conexao is None:
        raise GoogleNaoConectado("Google não conectado. Conecte na Visão Geral.")
    return conexao


async def abrir(
    db: AsyncSession, tenant_id: uuid.UUID, transport: httpx.AsyncBaseTransport | None = None
) -> tuple[GoogleApi, SocialConnection]:
    conexao = await _conexao(db, tenant_id)
    cliente = GoogleBusinessClient(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET, transport=transport)
    access_token = await cliente.renovar_access_token(decrypt_token(conexao.access_token_encrypted))
    return GoogleApi(access_token, transport=transport), conexao


def _site_padrao() -> Site | None:
    if not settings.BLOG_SFTP_HOST:
        return None
    from app.integrations.publish.sftp_client import SFTPClient

    raiz = settings.BLOG_SFTP_PATH.rstrip("/")
    if raiz.endswith("/blog"):
        raiz = raiz[: -len("/blog")]
    sftp = SFTPClient(settings.BLOG_SFTP_HOST, settings.BLOG_SFTP_PORT, settings.BLOG_SFTP_USER,
                      settings.BLOG_SFTP_PASSWORD)
    return SiteSftp(sftp, raiz)


async def atualizar_painel(
    db: AsyncSession, tenant_id: uuid.UUID, *,
    transport: httpx.AsyncBaseTransport | None = None, site: Site | None = None,
) -> dict:
    api, conexao = await abrir(db, tenant_id, transport)
    painel = await coletar_painel(api, conexao.page_id, conexao.ig_user_id)

    site = site or _site_padrao()
    if site is not None and painel.get("dominio"):
        try:
            painel["site"] = await checar_site(site, painel["dominio"])
        except Exception as erro:  # a hospedagem fora do ar não pode derrubar o painel
            logger.exception("Checagem do site falhou")
            painel["site"] = None
            painel["erros"]["site"] = {"tipo": "falha", "mensagem": str(erro), "ativar_em": None}
        finally:
            fechar = getattr(getattr(site, "_sftp", None), "close", None)
            if fechar:
                await fechar()

    ga = painel.get("analytics")
    if ga and ga.get("propriedade"):
        try:
            painel["eventos_principais"] = await gestao_google.garantir_eventos_principais(
                api, ga["propriedade"], list(EVENTOS_CONTATO)
            )
        except GoogleApiErro as erro:
            painel["erros"]["eventos_principais"] = erro.como_dict()

    gsc = painel.get("search_console")
    if gsc and painel.get("dominio"):
        try:
            await gestao_google.enviar_sitemap(api, gsc["site"], f"https://{painel['dominio']}/sitemap.xml")
            painel["sitemap_enviado"] = True
        except GoogleApiErro as erro:
            painel["sitemap_enviado"] = False
            painel["erros"]["sitemap"] = erro.como_dict()

    db.add(SocialMetric(tenant_id=tenant_id, tipo=TIPO_PAINEL, referencia_id=None, metricas=painel))
    await db.commit()
    return painel


async def ultimo_painel(db: AsyncSession, tenant_id: uuid.UUID) -> tuple[dict | None, datetime | None]:
    registro = (await db.execute(
        select(SocialMetric)
        .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == TIPO_PAINEL)
        .order_by(SocialMetric.coletado_em.desc())
        .limit(1)
    )).scalar_one_or_none()
    return (registro.metricas, registro.coletado_em) if registro else (None, None)


async def salvar_secao(db: AsyncSession, tenant_id: uuid.UUID, secao: str, valor) -> None:
    """Atualiza uma seção do último painel salvo (ex.: o perfil logo depois de editar)."""
    registro = (await db.execute(
        select(SocialMetric)
        .where(SocialMetric.tenant_id == tenant_id, SocialMetric.tipo == TIPO_PAINEL)
        .order_by(SocialMetric.coletado_em.desc())
        .limit(1)
    )).scalar_one_or_none()
    if registro is None:
        return
    registro.metricas = {**registro.metricas, secao: valor}
    await db.commit()


async def atualizar_todos(db: AsyncSession) -> int:
    conexoes = (await db.execute(select(SocialConnection).where(
        SocialConnection.plataforma == "google_business", SocialConnection.status == "ativo"
    ))).scalars().all()
    feitos = 0
    for conexao in conexoes:
        try:
            await atualizar_painel(db, conexao.tenant_id)
            feitos += 1
        except Exception:
            logger.exception("Falha ao atualizar o painel do Google (tenant %s)", conexao.tenant_id)
    return feitos


async def publicar_post(db: AsyncSession, post: GooglePost, transport: httpx.AsyncBaseTransport | None = None) -> None:
    api, conexao = await abrir(db, post.tenant_id, transport)
    resultado = await gestao_google.publicar_post(
        api, conexao.page_id, conexao.ig_user_id, post.texto, post.botao, post.link, post.imagem_url
    )
    post.google_name = resultado["name"]
    post.link_publicado = resultado["link"]
    post.status = "publicado"
    post.erro = None
    await db.commit()


AGUARDANDO_ARTIGO = "Aguardando o artigo ir ao ar no site; o post sai assim que ele estiver publicado."


async def artigo_no_ar(site: Site | None, link: str | None, dominio: str | None) -> bool:
    """O link do post aponta para uma página que existe no site? Links de fora do site (ou sem como
    conferir) contam como no ar."""
    if not link or site is None or not dominio:
        return True
    url = urlparse(link)
    if (url.hostname or "").lower() not in (dominio, f"www.{dominio}"):
        return True
    caminho = url.path.lstrip("/")
    if not caminho or caminho.endswith("/"):
        caminho += "index.html"
    return await site.ler(caminho) is not None


async def publicar_posts_prontos(
    db: AsyncSession, agora: datetime | None = None, transport: httpx.AsyncBaseTransport | None = None,
    site: Site | None = None,
) -> int:
    """Publica os posts aprovados cujo horário chegou. Post com link para artigo do site que ainda não
    existe fica aprovado, com o aviso em `erro`, e é tentado de novo na próxima rodada."""
    agora = agora or datetime.now(timezone.utc)
    prontos = (await db.execute(select(GooglePost).where(
        GooglePost.status == "aprovado", GooglePost.publicar_em <= agora
    ))).scalars().all()
    if not prontos:
        return 0
    site = site or _site_padrao()
    publicados = 0
    for post in prontos:
        painel, _ = await ultimo_painel(db, post.tenant_id)
        try:
            no_ar = await artigo_no_ar(site, post.link, (painel or {}).get("dominio"))
        except Exception:
            logger.exception("Não deu para conferir o artigo do post %s; publica mesmo assim", post.id)
            no_ar = True
        if not no_ar:
            if post.erro != AGUARDANDO_ARTIGO:
                post.erro = AGUARDANDO_ARTIGO
                await db.commit()
            continue
        try:
            await publicar_post(db, post, transport)
            publicados += 1
        except Exception as erro:
            logger.exception("Falha ao publicar post do Google %s", post.id)
            post.status = "erro"
            post.erro = getattr(erro, "mensagem", None) or str(erro)
            await db.commit()
    fechar = getattr(getattr(site, "_sftp", None), "close", None)
    if fechar:
        await fechar()
    return publicados

