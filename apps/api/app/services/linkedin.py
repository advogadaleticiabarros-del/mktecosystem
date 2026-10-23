"""LinkedIn no Orbit: conexão do perfil da Dra., fila de posts e publicação.

Interface:
- `await abrir(db, tenant_id)` -> (api, conexao). Levanta `LinkedInNaoConectado` sem conexão ou com ela vencida.
- `await dados_do_artigo(site, link)` -> card do link: título, descrição e capa lidos do próprio site (o site barra
  clientes automáticos por HTTP, por isso a leitura é pelo adaptador `Site`, via SFTP).
- `await publicar_post(db, post)` e `await publicar_prontos(db, agora)`: a fila; post com link para artigo que
  ainda não está no site espera, como os posts do Google.
- `link_com_utm(link, quando)`: links do site saem com utm_source=linkedin (o painel do Google separa o que veio
  do LinkedIn em `analytics.linkedin`).
- `aviso_conexao(conexao, hoje)` -> melhoria "reconectar" quando faltam 7 dias ou menos (o token dura 60 dias).
- `await sugerir_post(ia, tema)` -> texto no tom da Dra. para o LinkedIn, já conferido pela checagem da OAB.
"""
import logging
import re
import uuid
from datetime import date, datetime, timezone
from html import unescape
from urllib.parse import urlencode, urlparse, urlunparse

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crypto import decrypt_token
from app.integrations.ai.base import AIClient
from app.integrations.social.linkedin_api import LinkedInApi, LinkedInErro
from app.models.presenca_google import LinkedInPost
from app.models.social_connection import SocialConnection
from app.services.central_google import AGUARDANDO_ARTIGO, _site_padrao, artigo_no_ar
from app.services.checagem_site import Site
from app.services.conformidade_oab import verificar_texto_oab
from app.services.site_descoberta import SITE

logger = logging.getLogger(__name__)
PLATAFORMA = "linkedin"
DOMINIO = urlparse(SITE).hostname
LIMITE_TEXTO = 3000
DIAS_AVISO = 7
CAMPANHA_UTM = "empresa-em-dia"


class LinkedInNaoConectado(Exception):
    pass


async def conexao(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection | None:
    return (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == tenant_id, SocialConnection.plataforma == PLATAFORMA,
        SocialConnection.status == "ativo",
    ))).scalar_one_or_none()


def _vencida(c: SocialConnection, agora: datetime) -> bool:
    if c.expira_em is None:
        return False
    expira = c.expira_em if c.expira_em.tzinfo else c.expira_em.replace(tzinfo=timezone.utc)
    return expira <= agora


async def abrir(db: AsyncSession, tenant_id: uuid.UUID, transport: httpx.AsyncBaseTransport | None = None,
                agora: datetime | None = None) -> tuple[LinkedInApi, SocialConnection]:
    c = await conexao(db, tenant_id)
    if c is None:
        raise LinkedInNaoConectado("LinkedIn não conectado. Conecte na Visão Geral.")
    if _vencida(c, agora or datetime.now(timezone.utc)):
        raise LinkedInNaoConectado("A conexão com o LinkedIn venceu (dura 60 dias). Reconecte na Visão Geral.")
    return LinkedInApi(decrypt_token(c.access_token_encrypted), transport=transport), c


def aviso_conexao(c: SocialConnection | None, hoje: date) -> dict | None:
    if c is None or c.expira_em is None:
        return None
    dias = (c.expira_em.date() - hoje).days
    if dias > DIAS_AVISO:
        return None
    titulo = "A conexão com o LinkedIn venceu" if dias < 0 else f"A conexão com o LinkedIn vence em {dias} dia(s)"
    return {
        "chave": f"linkedin-reconectar-{c.expira_em:%Y-%m-%d}", "area": "configuracao",
        "prioridade": "alta" if dias < 2 else "media", "titulo": titulo,
        "motivo": "O LinkedIn só deixa a conexão valer 60 dias. Sem ela, os posts agendados esperam.",
        "acao": "Visão Geral → LinkedIn → Reconectar, com o login da Dra.", "itens": [], "link": None,
        "aplicar": None,
    }


def _meta(html: str, *nomes: str) -> str | None:
    for nome in nomes:
        m = re.search(rf'<meta[^>]+(?:name|property)=["\']{re.escape(nome)}["\'][^>]*content=["\']([^"\']*)', html, re.I)
        if m and m.group(1).strip():
            return unescape(m.group(1).strip())
    return None


async def dados_do_artigo(site: Site | None, link: str) -> dict:
    """Card do link. Para páginas do site: título e descrição das metas e a capa (og:image do próprio site)."""
    card = {"link": link}
    url = urlparse(link)
    if site is None or (url.hostname or "").lower() not in (DOMINIO, f"www.{DOMINIO}"):
        return card
    caminho = url.path.lstrip("/") or "index.html"
    html = await site.ler(caminho)
    if not html:
        return card
    titulo = _meta(html, "og:title") or (re.search(r"<title>(.*?)</title>", html, re.S | re.I) or [None, None])[1]
    card["titulo"] = unescape(titulo.split(" | ")[0].strip()) if titulo else None
    card["descricao"] = _meta(html, "og:description", "description")
    imagem = _meta(html, "og:image")
    ler_bytes = getattr(site, "ler_bytes", None)
    if imagem and ler_bytes:
        alvo = urlparse(imagem)
        if (alvo.hostname or DOMINIO).lower() in (DOMINIO, f"www.{DOMINIO}"):
            caminho_img = alvo.path.lstrip("/")
            if not alvo.hostname:  # relativo à página
                base = caminho.rsplit("/", 1)[0] + "/" if "/" in caminho else ""
                caminho_img = re.sub(r"[^/]+/\.\./", "", base + imagem)
            capa = await ler_bytes(caminho_img)
            if capa:
                card["capa"] = capa
    return card


def link_com_utm(link: str, quando: datetime | None = None) -> str:
    """Etiqueta os links do próprio site com a origem LinkedIn, para o Analytics separar visitas e contatos por post.
    Links de fora e links que já têm UTM ficam como estão."""
    url = urlparse(link)
    if (url.hostname or "").lower() not in (DOMINIO, f"www.{DOMINIO}") or "utm_" in url.query:
        return link
    etiquetas = {"utm_source": "linkedin", "utm_medium": "social", "utm_campaign": CAMPANHA_UTM}
    if quando:
        etiquetas["utm_content"] = f"{quando:%Y-%m-%d}"
    query = "&".join(filter(None, [url.query, urlencode(etiquetas)]))
    return urlunparse(url._replace(query=query))


async def publicar_post(db: AsyncSession, post: LinkedInPost, transport: httpx.AsyncBaseTransport | None = None,
                        site: Site | None = None) -> None:
    problemas = [p for p in verificar_texto_oab(post.texto) if p["nivel"] == "bloqueia"]
    if problemas:
        raise ValueError("O texto fere as regras da OAB: " + "; ".join(p["trecho"] for p in problemas))
    api, c = await abrir(db, post.tenant_id, transport)
    artigo = await dados_do_artigo(site, post.link) if post.link else None
    if artigo:
        artigo["link"] = link_com_utm(post.link, post.publicar_em)
    post.post_urn = await api.publicar(c.page_id, post.texto, artigo)
    post.status = "publicado"
    post.erro = None
    await db.commit()


async def publicar_prontos(db: AsyncSession, agora: datetime | None = None,
                           transport: httpx.AsyncBaseTransport | None = None, site: Site | None = None) -> int:
    agora = agora or datetime.now(timezone.utc)
    prontos = (await db.execute(select(LinkedInPost).where(
        LinkedInPost.status == "aprovado", LinkedInPost.publicar_em <= agora
    ))).scalars().all()
    if not prontos:
        return 0
    site = site or _site_padrao()
    publicados = 0
    for post in prontos:
        try:
            if not await artigo_no_ar(site, post.link, DOMINIO):
                if post.erro != AGUARDANDO_ARTIGO:
                    post.erro = AGUARDANDO_ARTIGO
                    await db.commit()
                continue
            await publicar_post(db, post, transport, site)
            publicados += 1
        except LinkedInNaoConectado as erro:  # espera a reconexão, sem perder o agendamento
            post.erro = str(erro)
            await db.commit()
        except (LinkedInErro, ValueError) as erro:
            logger.exception("Falha ao publicar post do LinkedIn %s", post.id)
            if getattr(erro, "reconectar", False):
                post.erro = erro.mensagem
            else:
                post.status = "erro"
                post.erro = getattr(erro, "mensagem", None) or str(erro)
            await db.commit()
    fechar = getattr(getattr(site, "_sftp", None), "close", None)
    if fechar:
        await fechar()
    return publicados


VOZ_LINKEDIN = """Você escreve posts do LinkedIn da Dra. Letícia Barros, advogada trabalhista e previdenciária em
Vitória/ES (OAB/ES 39.948). No LinkedIn o público inclui donos de empresa, RH e contadores, além de trabalhadores.
Tom: claro, direto, sem juridiquês, frases curtas, fala com "você", assina com "eu". Abra com uma frase forte sobre
o problema concreto, explique a regra com lei e data certas, termine com o que fazer agora (lista curta numerada).
Regras da OAB (obrigatórias): sem promessa de resultado, sem autoelogio, sem preço ou "consulta gratuita", sem
"envie seu caso" ou "me chama", sem contar casos de clientes. No máximo 3 hashtags no fim. Entre 600 e 1.300
caracteres. Responda só com o texto do post."""


async def sugerir_post(ia: AIClient, tema: str) -> str:
    prompt = f"{VOZ_LINKEDIN}\n\nTema do post: {tema}"
    texto = (await ia.generate_text(prompt)).strip().strip('"')
    problemas = [p for p in verificar_texto_oab(texto) if p["nivel"] == "bloqueia"]
    if problemas:
        motivos = "; ".join(f"\"{p['trecho']}\" ({p['motivo']})" for p in problemas)
        texto = (await ia.generate_text(f"{prompt}\n\nA versão anterior foi recusada por: {motivos}. Reescreva sem isso.")).strip().strip('"')
    return texto[:LIMITE_TEXTO]

