"""TikTok no Orbit: conexão da conta e fila própria de vídeos (agenda independente do Instagram, desde 23/10/2026).

Interface:
- `salvar_conexao(db, tenant_id, tokens, perfil)`: guarda a conta conectada (SocialConnection plataforma="tiktok",
  tokens criptografados num JSON; `ig_user_id`/`page_id` guardam o open_id).
- `publicar_fila_tiktok(db, ..., agora=None)`: (1) põe na fila do TikTok cada vídeo aprovado que ainda não tem vaga,
  na próxima vaga livre da `GRADE_TIKTOK`, na ordem da data do Instagram (séries ficam em ordem). Entram os Reels
  com agendamento de Instagram ativo (não pausado/cancelado; versões sem agendamento ficam de fora) e as peças
  `tipo="tiktok"` (vídeos só do TikTok). A vaga fica em `corpo["tiktok"]` (`data`, `horario`, `titulo`).
  (2) Envia cada vídeo cujo horário do TikTok chegou, uma única vez, e anota em `corpo["tiktok"]`:
  - `status="publicado"`: saiu direto e público (app auditado pela TikTok);
  - `status="no_rascunho"`: foi para a caixa de rascunhos do TikTok (app ainda sem auditoria); falta alguém abrir a
    notificação no app, colar a legenda (a tela /tiktok mostra) e publicar;
  - `status="erro"` depois de 3 falhas (`"tentando"` antes disso).
  Legenda: `corpo["legenda_tiktok"]` se houver, senão a do Instagram. Peça com `rotulo_ia` sai marcada como IA.
  O acesso (24 h) é renovado sozinho.
- `remarcar(db, tenant_id, piece_id, data, horario)`: muda a vaga de um vídeo ainda não enviado; `data=None` tira
  o vídeo do TikTok (`fora=True`, não volta para a fila).
- `situacao(db, tenant_id)`: conexão, fila (próximas vagas), rascunhos esperando publicação (com legenda) e últimos
  envios.
- `marcar_publicado(db, tenant_id, piece_id)`: quem publicou o rascunho pelo app avisa o Orbit.
"""
import logging
import uuid
from datetime import date, datetime, timedelta, timezone

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

from app.core.crypto import decrypt_token, encrypt_token
from app.integrations.social.tiktok_api import TikTokAPI, TokensTikTok, renovar_tokens
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.services.agendamento_horario import FUSO_PADRAO, horario_ja_chegou
from app.services.chaves_api import obter_chave, separar_tiktok

logger = logging.getLogger(__name__)
LIMITE_TENTATIVAS = 3
ENCERRADOS = ("publicado", "no_rascunho", "erro")
# 5 vídeos por semana, em 3 faixas para testar (docs/ESTRATEGIA_TIKTOK.md; rever com os números em 20/11/2026)
GRADE_TIKTOK = {6: "10:00", 0: "18:00", 1: "12:00", 2: "20:00", 3: "18:00"}  # dom, seg, ter, qua, qui
AGENDAS_INATIVAS = ("pausado", "cancelado")


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


async def _videos(db: AsyncSession, tenant_id: uuid.UUID) -> list[tuple[ContentPiece, ScheduledPost | None, Pauta | None]]:
    """Vídeos que podem ir ao TikTok, com o agendamento do Instagram (se houver) e a pauta (para o título)."""
    linhas = await db.execute(
        select(ContentPiece, ScheduledPost, Pauta)
        .outerjoin(ScheduledPost, ScheduledPost.content_piece_id == ContentPiece.id)
        .outerjoin(Pauta, Pauta.id == ContentPiece.pauta_id)
        .where(ContentPiece.tenant_id == tenant_id, ContentPiece.tipo.in_(["reels", "tiktok"])))
    return linhas.all()


def _estado(piece: ContentPiece) -> dict:
    return (piece.corpo or {}).get("tiktok") or {}


def _titulo(piece: ContentPiece, agendamento: ScheduledPost | None, pauta: Pauta | None) -> str:
    return (agendamento.titulo if agendamento else None) or (piece.corpo or {}).get("titulo") or \
        (pauta.titulo if pauta else "Vídeo")


def _na_fila(piece: ContentPiece) -> bool:
    estado = _estado(piece)
    return bool(estado.get("data")) and not estado.get("fora") and estado.get("status") not in ENCERRADOS


def _espera_vaga(piece: ContentPiece, agendamento: ScheduledPost | None) -> bool:
    estado = _estado(piece)
    if estado.get("data") or estado.get("fora") or estado.get("status") or not (piece.corpo or {}).get("video") \
            or piece.status not in ("aprovado", "publicado"):
        return False
    if piece.tipo == "tiktok":
        return True
    return agendamento is not None and agendamento.canal == "instagram" and agendamento.formato == "reels" \
        and agendamento.status not in AGENDAS_INATIVAS


def _vagas_livres(depois_de: datetime, ocupadas: set[tuple[str, str]]):
    """Vagas da GRADE_TIKTOK depois de `depois_de` (hora de Brasília), pulando as já ocupadas."""
    dia = depois_de.date()
    while True:
        horario = GRADE_TIKTOK.get(dia.weekday())
        if horario and (dia.isoformat(), horario) not in ocupadas:
            hora, minuto = (int(p) for p in horario.split(":"))
            if datetime(dia.year, dia.month, dia.day, hora, minuto, tzinfo=FUSO_PADRAO) > depois_de:
                yield dia, horario
        dia += timedelta(days=1)


def _encher_fila(videos, agora: datetime) -> None:
    ocupadas = {(e["data"], e["horario"]) for e in (_estado(p) for p, _, _ in videos) if e.get("data") and not e.get("fora")}
    esperando = sorted(
        ((p, a) for p, a, _ in videos if _espera_vaga(p, a)),
        key=lambda pa: (pa[1].data_agendada if pa[1] else date.max, pa[1].horario if pa[1] else "", str(pa[0].id)))
    vagas = _vagas_livres(agora.astimezone(FUSO_PADRAO), ocupadas)
    for piece, _ in esperando:
        dia, horario = next(vagas)
        _anotar(piece, data=dia.isoformat(), horario=horario)


def _anotar(piece: ContentPiece, **estado) -> None:
    piece.corpo = {**(piece.corpo or {}), "tiktok": {**((piece.corpo or {}).get("tiktok") or {}), **estado}}
    flag_modified(piece, "corpo")


def _legenda(corpo: dict) -> str:
    return corpo.get("legenda_tiktok") or corpo.get("legenda") or ""


async def publicar_fila_tiktok(db: AsyncSession, credenciais=credenciais_do_painel, fabrica_api=TikTokAPI,
                               renovar=renovar_tokens, baixar=baixar_video, agora: datetime | None = None) -> int:
    agora = agora or datetime.now(timezone.utc)
    conexoes = (await db.execute(select(SocialConnection).where(
        SocialConnection.plataforma == "tiktok", SocialConnection.status == "ativo"))).scalars().all()
    enviados = 0
    for conexao in conexoes:
        videos = await _videos(db, conexao.tenant_id)
        _encher_fila(videos, agora)
        await db.commit()
        vencidos = [p for p, _, _ in videos if _na_fila(p) and horario_ja_chegou(
            date.fromisoformat(_estado(p)["data"]), _estado(p)["horario"], agora)]
        for piece in vencidos:
            corpo = piece.corpo or {}
            try:
                api = fabrica_api(await _acesso_valido(db, conexao, credenciais, renovar))
                r = await api.publicar_video(await baixar(corpo["video"]), _legenda(corpo), ia=bool(corpo.get("rotulo_ia")))
            except Exception as erro:
                logger.exception("TikTok: falha ao enviar a peça %s", piece.id)
                tentativas = int(_estado(piece).get("tentativas", 0)) + 1
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


async def remarcar(db: AsyncSession, tenant_id: uuid.UUID, piece_id: uuid.UUID, data: date | None,
                   horario: str | None) -> bool:
    piece = await db.get(ContentPiece, piece_id)
    if piece is None or piece.tenant_id != tenant_id or _estado(piece).get("status") in ENCERRADOS:
        return False
    if data is None:
        _anotar(piece, fora=True)
    else:
        _anotar(piece, data=data.isoformat(), horario=horario or GRADE_TIKTOK.get(data.weekday(), "18:00"), fora=False)
    await db.commit()
    return True


async def situacao(db: AsyncSession, tenant_id: uuid.UUID) -> dict:
    conexao = await _conexao(db, tenant_id)
    fila, envios = [], []
    for piece, agendamento, pauta in await _videos(db, tenant_id):
        estado, corpo = _estado(piece), piece.corpo or {}
        item = {"id": str(piece.id), "titulo": _titulo(piece, agendamento, pauta), "status": estado.get("status"),
                "modo": estado.get("modo"), "em": estado.get("em"), "motivo": estado.get("motivo"),
                "legenda": _legenda(corpo), "video": corpo.get("video"), "data": estado.get("data"),
                "horario": estado.get("horario")}
        if _na_fila(piece):
            fila.append(item)
        if estado.get("status"):
            envios.append(item)
    fila.sort(key=lambda e: (e["data"], e["horario"]))
    envios.sort(key=lambda e: e["em"] or "", reverse=True)
    return {
        "conectado": conexao is not None,
        "nome": conexao.nome_conta if conexao else None,
        "desde": conexao.conectado_em if conexao else None,
        "grade": {str(dia): horario for dia, horario in GRADE_TIKTOK.items()},
        "fila": fila,
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
