from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.core.crypto import decrypt_token, encrypt_token
from app.integrations.social.tiktok_api import ErroTikTok, TokensTikTok
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant
from app.services.tiktok import marcar_publicado, publicar_reels_no_tiktok, salvar_conexao, situacao


def _tokens(access="act.1", expira_em=None):
    agora = datetime.now(timezone.utc)
    return TokensTikTok(access, "rt.1", "oid-1", expira_em or agora + timedelta(hours=20), agora + timedelta(days=300))


async def _setup(db, conectar=True, tokens=None, tipo="reels", corpo=None, dia=None):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    if conectar:
        await salvar_conexao(db, tenant.id, tokens or _tokens(), {"display_name": "Letícia Barros", "username": "leticia"})
    pauta = Pauta(tenant_id=tenant.id, titulo="Tema", angulo="reels", area="Família", origem="manual", fonte="manual",
                  relevante_para_conteudo=True)
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo=tipo, status="aprovado",
                         corpo=corpo if corpo is not None else {"video": "https://api.x/media/r.mp4", "legenda": "Legenda IG"})
    db.add(piece)
    await db.flush()
    db.add(ScheduledPost(tenant_id=tenant.id, content_piece_id=piece.id, titulo="Tema", canal="instagram", formato="reels",
                         data_agendada=dia or date.today(), horario="00:00", status="pronto"))
    await db.commit()
    return tenant, piece


class APIFalsa:
    def __init__(self, falhar=False, modo="publico"):
        self.publicados, self.falhar, self.tokens_usados, self.modo = [], falhar, [], modo

    def __call__(self, access_token):
        self.tokens_usados.append(access_token)
        return self

    async def publicar_video(self, video, legenda, ia=False):
        if self.falhar:
            raise ErroTikTok("upload recusado")
        self.publicados.append((video, legenda, ia))
        return {"modo": self.modo, "publish_id": "p-1", "privacidade": "PUBLIC_TO_EVERYONE" if self.modo == "publico" else None,
                "post_id": "123" if self.modo == "publico" else None}


async def baixar(url):
    return b"mp4:" + url.encode()


async def credenciais(db, tenant_id):
    return "ck", "cs"


@pytest.mark.anyio
async def test_salvar_conexao_guarda_tokens_criptografados(db_session):
    tenant, _ = await _setup(db_session)
    c = (await db_session.execute(select(SocialConnection).where(SocialConnection.plataforma == "tiktok"))).scalar_one()
    assert c.nome_conta == "Letícia Barros (@leticia)" and c.status == "ativo" and c.ig_user_id == "oid-1"
    assert "act.1" not in c.access_token_encrypted
    assert TokensTikTok.de_json(decrypt_token(c.access_token_encrypted)).access_token == "act.1"


@pytest.mark.anyio
async def test_publica_reels_aprovado_e_marca_na_peca(db_session):
    _, piece = await _setup(db_session, corpo={"video": "https://api.x/media/r.mp4", "legenda": "IG", "legenda_tiktok": "TT"})
    api = APIFalsa()
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api) == 1
    assert api.publicados == [(b"mp4:https://api.x/media/r.mp4", "TT", False)]
    await db_session.refresh(piece)
    assert piece.corpo["tiktok"]["status"] == "publicado" and piece.corpo["tiktok"]["post_id"] == "123"
    # rodar de novo não republica
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api) == 0


@pytest.mark.anyio
async def test_renova_o_acesso_vencido_antes_de_publicar(db_session):
    vencido = _tokens(access="act.velho", expira_em=datetime.now(timezone.utc) - timedelta(minutes=1))
    await _setup(db_session, tokens=vencido)
    api = APIFalsa()

    async def renovar(ck, cs, refresh_token):
        assert (ck, cs, refresh_token) == ("ck", "cs", "rt.1")
        return _tokens(access="act.novo")

    await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api, renovar=renovar)
    assert api.tokens_usados == ["act.novo"]
    c = (await db_session.execute(select(SocialConnection).where(SocialConnection.plataforma == "tiktok"))).scalar_one()
    assert TokensTikTok.de_json(decrypt_token(c.access_token_encrypted)).access_token == "act.novo"


@pytest.mark.anyio
async def test_sem_conexao_tiktok_nao_faz_nada(db_session):
    await _setup(db_session, conectar=False)
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=APIFalsa()) == 0


@pytest.mark.anyio
async def test_ignora_reels_futuro_rascunho_e_sem_video(db_session):
    _, futuro = await _setup(db_session, dia=date.today() + timedelta(days=3))
    api = APIFalsa()
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api) == 0
    futuro.status = "rascunho"
    await db_session.commit()
    assert api.publicados == []


@pytest.mark.anyio
async def test_tres_falhas_marcam_erro_e_param(db_session):
    _, piece = await _setup(db_session)
    api = APIFalsa(falhar=True)
    for _ in range(4):
        await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api)
    await db_session.refresh(piece)
    assert piece.corpo["tiktok"]["status"] == "erro" and piece.corpo["tiktok"]["tentativas"] == 3
    assert "upload recusado" in piece.corpo["tiktok"]["motivo"]


@pytest.mark.anyio
async def test_sem_auditoria_vai_para_o_rascunho_e_a_tela_mostra_a_legenda(db_session):
    tenant, piece = await _setup(db_session, corpo={"video": "https://api.x/media/r.mp4", "legenda": "Legenda IG",
                                                    "rotulo_ia": True})
    api = APIFalsa(modo="rascunho")
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api) == 1
    assert api.publicados[0][2] is True  # rótulo de IA
    s = await situacao(db_session, tenant.id)
    assert s["conectado"] and s["nome"] == "Letícia Barros (@leticia)"
    assert [(e["status"], e["legenda"]) for e in s["no_rascunho"]] == [("no_rascunho", "Legenda IG")]
    # não reenvia o que já está no rascunho
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api) == 0

    assert await marcar_publicado(db_session, tenant.id, piece.id) is True
    assert (await situacao(db_session, tenant.id))["no_rascunho"] == []
    await db_session.refresh(piece)
    assert piece.corpo["tiktok"]["status"] == "publicado" and piece.corpo["tiktok"]["publicado_pelo_app"]


@pytest.mark.anyio
async def test_reels_de_antes_da_conexao_nao_vao(db_session):
    await _setup(db_session, dia=date.today() - timedelta(days=2))
    api = APIFalsa()
    assert await publicar_reels_no_tiktok(db_session, credenciais=credenciais, baixar=baixar, fabrica_api=api) == 0
