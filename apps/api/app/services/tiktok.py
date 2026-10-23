"""TikTok no Orbit: conexão da conta e envio automático dos Reels aprovados (mesmo vídeo do Instagram).

Interface:
- `salvar_conexao(db, tenant_id, tokens, perfil)`: guarda a conta conectada (SocialConnection plataforma="tiktok",
  tokens criptografados num JSON; `ig_user_id`/`page_id` guardam o open_id).
- `publicar_reels_no_tiktok(db, ...)`: para cada Reels aprovado cujo horário do Instagram já chegou, a partir do dia
  em que a conta foi conectada, envia o vídeo uma única vez e anota em `corpo["tiktok"]`:
  - `status="publicado"`: saiu direto e público (app auditado pela TikTok);
  - `status="no_rascunho"`: foi para a caixa de rascunhos do TikTok (app ainda sem auditoria); falta alguém abrir a
    notificação no app, colar a legenda (a tela /tiktok mostra) e publicar;
  - `status="erro"` depois de 3 falhas (`"tentando"` antes disso).
  Legenda: `corpo["legenda_tiktok"]` se houver, senão a do Instagram. Peça com `rotulo_ia` sai marcada como IA.
  O acesso (24 h) é renovado sozinho.
- `situacao(db, tenant_id)`: conexão, rascunhos esperando publicação (com legenda) e últimos envios.
- `marcar_publicado(db, tenant_id, piece_id)`: quem publicou o rascunho pelo app avisa o Orbit.
"""
import logging
import uuid
from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from app.core.crypto import decrypt_token, encrypt_token
from app.integrations.social.tiktok_api import TikTokAPI, TokensTikTok, renovar_tokens
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.services.agendamento_horario import horario_ja_chegou
from app.services.chaves_api import obter_chave, separar_tiktok

logger = logging.getLogger(__name__)
LIMITE_TENTATIVAS = 3
ENCERRADOS = ("publicado", "no_rascunho", "erro")


async def credenciais_do_painel(db: AsyncSession, tenant_id: uuid.UUID) -> tuple[str, str]:
    chave = await obter_chave(db, tenant_id, "tiktok")
    if not chave:
        raise RuntimeError("Credenciais da TikTok não cadastradas no painel de chaves")
    return separar_tiktok(chave)


async def baixar_video(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=180, follow_redirects=True) as client:
        r = await client.get(url)
    r.raise_for_status()
    return r.content


async def _conexao(db: AsyncSession, tenant_id: uuid.UUID) -> SocialConnection | None:
    return (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == tenant_id, SocialConnection.plataforma == "tiktok",
        SocialConnection.status == "ativo"))).scalar_one_or_none()


def _gravar_tokens(conexao: SocialConnection, tokens: TokensTikTok) -> None:
    conexao.access_token_encrypted = encrypt_token(tokens.para_json())
    conexao.expira_em = tokens.expira_em


async def salvar_conexao(db: AsyncSession, tenant_id: uuid.UUID, tokens: TokensTikTok, perfil: dict) -> SocialConnection:
    conexao = (await db.execute(select(SocialConnection).where(
        SocialConnection.tenant_id == tenant_id, SocialConnection.plataforma == "tiktok"))).scalar_one_or_none()
    if conexao is None:
        conexao = SocialConnection(tenant_id=tenant_id, plataforma="tiktok")
        db.add(conexao)
    if conexao.status != "ativo":
        conexao.conectado_em = datetime.now(timezone.utc)  # Reels anteriores à (re)conexão não vão para o TikTok
    nome, usuario = perfil.get("display_name") or "TikTok", perfil.get("username")
    conexao.page_id = conexao.ig_user_id = tokens.open_id
    conexao.nome_conta = f"{nome} (@{usuario})" if usuario else nome
    conexao.status = "ativo"
    _gravar_tokens(conexao, tokens)
    await db.commit()
    return conexao


async def _acesso_valido(db, conexao, credenciais, renovar) -> str:
    tokens = TokensTikTok.de_json(decrypt_token(conexao.access_token_encrypted))
    if tokens.expira_em - timedelta(minutes=10) > datetime.now(timezone.utc):
        return tokens.access_token
    ck, cs = await credenciais(db, conexao.tenant_id)
    novos = await renovar(ck, cs, tokens.refresh_token)
    _gravar_tokens(conexao, novos)
    await db.commit()
    return novos.access_token


async def _reels_prontos(db: AsyncSession, conexao: SocialConnection) -> list[ContentPiece]:
    agora = datetime.now(timezone.utc)
    desde = conexao.conectado_em.date() if conexao.conectado_em else agora.date()
    linhas = await db.execute(
        select(ScheduledPost, ContentPiece).join(ContentPiece, ContentPiece.id == ScheduledPost.content_piece_id).where(
            ScheduledPost.tenant_id == conexao.tenant_id, ScheduledPost.canal == "instagram",
            ScheduledPost.formato == "reels", ScheduledPost.data_agendada >= desde,
            ScheduledPost.data_agendada <= agora.date(), ContentPiece.status.in_(["aprovado", "publicado"])))
    prontos = []
    for agendamento, piece in linhas.all():
        estado = (piece.corpo or {}).get("tiktok") or {}
        if (piece.corpo or {}).get("video") and estado.get("status") not in ENCERRADOS \
                and horario_ja_chegou(agendamento.data_agendada, agendamento.horario, agora):
            prontos.append(piece)
    return prontos


def _anotar(piece: ContentPiece, **estado) -> None:
    piece.corpo = {**(piece.corpo or {}), "tiktok": {**((piece.corpo or {}).get("tiktok") or {}), **estado}}
    flag_modified(piece, "corpo")


def _legenda(corpo: dict) -> str:
    return corpo.get("legenda_tiktok") or corpo.get("legenda") or ""


async def publicar_reels_no_tiktok(db: AsyncSession, credenciais=credenciais_do_painel, fabrica_api=TikTokAPI,
                                   renovar=renovar_tokens, baixar=baixar_video) -> int:
    conexoes = (await db.execute(select(SocialConnection).where(
        SocialConnection.plataforma == "tiktok", SocialConnection.status == "ativo"))).scalars().all()
    enviados = 0
    for conexao in conexoes:
        for piece in await _reels_prontos(db, conexao):
            corpo = piece.corpo or {}
            try:
                api = fabrica_api(await _acesso_valido(db, conexao, credenciais, renovar))
                r = await api.publicar_video(await baixar(corpo["video"]), _legenda(corpo), ia=bool(corpo.get("rotulo_ia")))
            except Exception as erro:
                logger.exception("TikTok: falha ao enviar a peça %s", piece.id)
                tentativas = int((corpo.get("tiktok") or {}).get("tentativas", 0)) + 1
                _anotar(piece, tentativas=tentativas, motivo=str(erro)[:300],
                        status="erro" if tentativas >= LIMITE_TENTATIVAS else "tentando")
                await db.commit()
                continue
            _anotar(piece, status="publicado" if r["modo"] == "publico" else "no_rascunho", modo=r["modo"],
                    publish_id=r["publish_id"], post_id=r.get("post_id"), privacidade=r.get("privacidade"),
                    em=datetime.now(timezone.utc).isoformat())
            await db.commit()
            enviados += 1
    return enviados


async def situacao(db: AsyncSession, tenant_id: uuid.UUID) -> dict:
    conexao = await _conexao(db, tenant_id)
    linhas = (await db.execute(
        select(ScheduledPost, ContentPiece).join(ContentPiece, ContentPiece.id == ScheduledPost.content_piece_id).where(
            ScheduledPost.tenant_id == tenant_id, ScheduledPost.canal == "instagram",
            ScheduledPost.formato == "reels").order_by(ScheduledPost.data_agendada.desc()))).all()
    envios = []
    for agendamento, piece in linhas:
        estado = (piece.corpo or {}).get("tiktok")
        if estado:
            envios.append({"id": str(piece.id), "titulo": agendamento.titulo, "status": estado.get("status"),
                           "modo": estado.get("modo"), "em": estado.get("em"), "motivo": estado.get("motivo"),
                           "legenda": _legenda(piece.corpo or {}), "video": (piece.corpo or {}).get("video")})
    return {
        "conectado": conexao is not None,
        "nome": conexao.nome_conta if conexao else None,
        "desde": conexao.conectado_em if conexao else None,
        "no_rascunho": [e for e in envios if e["status"] == "no_rascunho"],
        "ultimos": envios[:12],
    }


async def marcar_publicado(db: AsyncSession, tenant_id: uuid.UUID, piece_id: uuid.UUID) -> bool:
    piece = await db.get(ContentPiece, piece_id)
    if piece is None or piece.tenant_id != tenant_id or ((piece.corpo or {}).get("tiktok") or {}).get("status") != "no_rascunho":
        return False
    _anotar(piece, status="publicado", publicado_pelo_app=datetime.now(timezone.utc).isoformat())
    await db.commit()
    return True
