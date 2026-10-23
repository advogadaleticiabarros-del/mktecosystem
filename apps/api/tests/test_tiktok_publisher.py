from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.core.crypto import decrypt_token
from app.integrations.social.tiktok_api import ErroTikTok, TokensTikTok
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant
from app.services.tiktok import marcar_publicado, publicar_fila_tiktok, remarcar, salvar_conexao, situacao

BRT = timezone(timedelta(hours=-3))
SEXTA = datetime(2026, 10, 23, 15, 0, tzinfo=BRT)  # fila montada numa sexta à tarde
DEPOIS = SEXTA + timedelta(days=30)  # todos os horários da fila já chegaram


def _tokens(access="act.1", expira_em=None):
    agora = datetime.now(timezone.utc)
    return TokensTikTok(access, "rt.1", "oid-1", expira_em or agora + timedelta(hours=20), agora + timedelta(days=300))


async def _tenant(db, conectar=True, tokens=None):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    if conectar:
        await salvar_conexao(db, tenant.id, tokens or _tokens(), {"display_name": "Letícia Barros", "username": "leticia"})
    return tenant


async def _reels(db, tenant, titulo="Tema", corpo=None, dia=date(2026, 10, 20), status="aprovado",
                 status_agenda="pronto", tipo="reels", agendar=True):
    pauta = Pauta(tenant_id=tenant.id, titulo=titulo, angulo="reels", area="Família", origem="manual", fonte="manual",
                  relevante_para_conteudo=True)
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo=tipo, status=status,
                         corpo=corpo if corpo is not None else {"video": "https://api.x/media/r.mp4", "legenda": "Legenda IG"})
    db.add(piece)
    await db.flush()
    if agendar:
        db.add(ScheduledPost(tenant_id=tenant.id, content_piece_id=piece.id, titulo=titulo, canal="instagram",
                             formato="reels", data_agendada=dia, horario="21:00", status=status_agenda))
    await db.commit()
    return piece


async def _setup(db, conectar=True, tokens=None, **kw):
    tenant = await _tenant(db, conectar, tokens)
    return tenant, await _reels(db, tenant, **kw)


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


async def rodar(db, api, agora, **kw):
    return await publicar_fila_tiktok(db, credenciais=credenciais, baixar=baixar, fabrica_api=api, agora=agora, **kw)


async def montar_e_publicar(db, api, **kw):
    """Monta a fila na sexta (nada vence ainda) e roda de novo quando os horários já chegaram."""
    assert await rodar(db, api, SEXTA, **kw) == 0
    return await rodar(db, api, DEPOIS, **kw)


@pytest.mark.anyio
async def test_salvar_conexao_guarda_tokens_criptografados(db_session):
    await _setup(db_session)
    c = (await db_session.execute(select(SocialConnection).where(SocialConnection.plataforma == "tiktok"))).scalar_one()
    assert c.nome_conta == "Letícia Barros (@leticia)" and c.status == "ativo" and c.ig_user_id == "oid-1"
    assert "act.1" not in c.access_token_encrypted
    assert TokensTikTok.de_json(decrypt_token(c.access_token_encrypted)).access_token == "act.1"


@pytest.mark.anyio
async def test_fila_propria_segue_a_grade_do_tiktok_na_ordem_do_instagram(db_session):
    tenant = await _tenant(db_session)
    # criados fora de ordem: a fila segue a data do Instagram (séries ficam na ordem)
    await _reels(db_session, tenant, "Parte 2", dia=date(2026, 10, 27))
    await _reels(db_session, tenant, "Parte 1", dia=date(2026, 10, 20))
    await _reels(db_session, tenant, "Parte 3", dia=date(2026, 11, 3))
    assert await rodar(db_session, APIFalsa(), SEXTA) == 0
    fila = (await situacao(db_session, tenant.id))["fila"]
    # grade: domingo 10h, segunda 18h, terça 12h, quarta 20h, quinta 18h
    assert [(f["titulo"], f["data"], f["horario"]) for f in fila] == [
        ("Parte 1", "2026-10-25", "10:00"), ("Parte 2", "2026-10-26", "18:00"), ("Parte 3", "2026-10-27", "12:00")]


@pytest.mark.anyio
async def test_envia_no_horario_do_tiktok_mesmo_antes_do_instagram(db_session):
    _, piece = await _setup(db_session, dia=date(2026, 12, 1),
                            corpo={"video": "https://api.x/media/r.mp4", "legenda": "IG", "legenda_tiktok": "TT"})
    api = APIFalsa()
    assert await rodar(db_session, api, SEXTA) == 0
    assert await rodar(db_session, api, datetime(2026, 10, 25, 10, 1, tzinfo=BRT)) == 1
    assert api.publicados == [(b"mp4:https://api.x/media/r.mp4", "TT", False)]
    await db_session.refresh(piece)
    assert piece.corpo["tiktok"]["status"] == "publicado" and piece.corpo["tiktok"]["post_id"] == "123"
    assert await rodar(db_session, api, DEPOIS) == 0  # não republica


@pytest.mark.anyio
async def test_novo_reels_aprovado_entra_na_proxima_vaga_livre(db_session):
    tenant = await _tenant(db_session)
    await _reels(db_session, tenant, "Primeiro")
    await rodar(db_session, APIFalsa(), SEXTA)
    await _reels(db_session, tenant, "Novo", dia=date(2026, 10, 10))  # data antiga não fura a fila
    await rodar(db_session, APIFalsa(), SEXTA + timedelta(hours=1))
    fila = (await situacao(db_session, tenant.id))["fila"]
    assert [(f["titulo"], f["data"]) for f in fila] == [("Primeiro", "2026-10-25"), ("Novo", "2026-10-26")]


@pytest.mark.anyio
async def test_fora_da_fila_rascunho_sem_video_pausado_e_versao_sem_agenda(db_session):
    tenant = await _tenant(db_session)
    await _reels(db_session, tenant, "Rascunho", status="rascunho")
    await _reels(db_session, tenant, "Sem vídeo", corpo={"legenda": "x"})
    await _reels(db_session, tenant, "Pausado", status_agenda="pausado")
    await _reels(db_session, tenant, "Versão antiga", agendar=False)
    await _reels(db_session, tenant, "Só TikTok", tipo="tiktok", agendar=False)
    await rodar(db_session, APIFalsa(), SEXTA)
    assert [f["titulo"] for f in (await situacao(db_session, tenant.id))["fila"]] == ["Só TikTok"]


@pytest.mark.anyio
async def test_remarcar_e_tirar_da_fila(db_session):
    tenant = await _tenant(db_session)
    a = await _reels(db_session, tenant, "A")
    b = await _reels(db_session, tenant, "B", dia=date(2026, 10, 21))
    await rodar(db_session, APIFalsa(), SEXTA)
    assert await remarcar(db_session, tenant.id, a.id, date(2026, 10, 29), "19:30") is True
    assert await remarcar(db_session, tenant.id, b.id, None, None) is True  # tira do TikTok
    await rodar(db_session, APIFalsa(), SEXTA + timedelta(hours=1))  # não volta para a fila
    assert [(f["titulo"], f["data"], f["horario"]) for f in (await situacao(db_session, tenant.id))["fila"]] == [
        ("A", "2026-10-29", "19:30")]
    api = APIFalsa()
    assert await rodar(db_session, api, DEPOIS) == 1
    assert await remarcar(db_session, tenant.id, a.id, date(2026, 12, 1), "10:00") is False  # já enviado


@pytest.mark.anyio
async def test_renova_o_acesso_vencido_antes_de_publicar(db_session):
    vencido = _tokens(access="act.velho", expira_em=datetime.now(timezone.utc) - timedelta(minutes=1))
    await _setup(db_session, tokens=vencido)
    api = APIFalsa()

    async def renovar(ck, cs, refresh_token):
        assert (ck, cs, refresh_token) == ("ck", "cs", "rt.1")
        return _tokens(access="act.novo")

    await montar_e_publicar(db_session, api, renovar=renovar)
    assert api.tokens_usados == ["act.novo"]
    c = (await db_session.execute(select(SocialConnection).where(SocialConnection.plataforma == "tiktok"))).scalar_one()
    assert TokensTikTok.de_json(decrypt_token(c.access_token_encrypted)).access_token == "act.novo"


@pytest.mark.anyio
async def test_sem_conexao_tiktok_nao_faz_nada(db_session):
    await _setup(db_session, conectar=False)
    assert await montar_e_publicar(db_session, APIFalsa()) == 0


@pytest.mark.anyio
async def test_tres_falhas_marcam_erro_e_param(db_session):
    _, piece = await _setup(db_session)
    api = APIFalsa(falhar=True)
    await rodar(db_session, api, SEXTA)
    for _ in range(4):
        await rodar(db_session, api, DEPOIS)
    await db_session.refresh(piece)
    assert piece.corpo["tiktok"]["status"] == "erro" and piece.corpo["tiktok"]["tentativas"] == 3
    assert "upload recusado" in piece.corpo["tiktok"]["motivo"]


@pytest.mark.anyio
async def test_sem_auditoria_vai_para_o_rascunho_e_a_tela_mostra_a_legenda(db_session):
    tenant, piece = await _setup(db_session, corpo={"video": "https://api.x/media/r.mp4", "legenda": "Legenda IG",
                                                    "rotulo_ia": True})
    api = APIFalsa(modo="rascunho")
    assert await montar_e_publicar(db_session, api) == 1
    assert api.publicados[0][2] is True  # rótulo de IA
    s = await situacao(db_session, tenant.id)
    assert s["conectado"] and s["nome"] == "Letícia Barros (@leticia)"
    assert [(e["status"], e["legenda"]) for e in s["no_rascunho"]] == [("no_rascunho", "Legenda IG")]
    assert s["fila"] == []
    assert await rodar(db_session, api, DEPOIS) == 0  # não reenvia o que já está no rascunho

    assert await marcar_publicado(db_session, tenant.id, piece.id) is True
    assert (await situacao(db_session, tenant.id))["no_rascunho"] == []
    await db_session.refresh(piece)
    assert piece.corpo["tiktok"]["status"] == "publicado" and piece.corpo["tiktok"]["publicado_pelo_app"]
