from datetime import date, datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

from sqlalchemy import select

import pytest

from app.core.crypto import encrypt_token
from app.models.content_piece import ContentPiece
from app.models.instagram_post import InstagramPost
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.social_connection import SocialConnection
from app.models.tenant import Tenant, TenantConfig
from app.services.instagram_publisher import publicar_agendamentos_prontos
from tests.fakes import RenderizadorFalso


async def _setup(db, com_conexao=True, tipo="carrossel", corpo=None, formato="carrossel"):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={}, identidade_visual={"cores": {}}))
    if com_conexao:
        db.add(
            SocialConnection(
                tenant_id=tenant.id,
                plataforma="instagram",
                page_id="111",
                ig_user_id="999",
                nome_conta="adv.leticiabarros2",
                access_token_encrypted=encrypt_token("token-falso"),
                status="ativo",
            )
        )
    pauta = Pauta(
        tenant_id=tenant.id, titulo="Tema", angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True,
    )
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(
        tenant_id=tenant.id, pauta_id=pauta.id, tipo=tipo,
        corpo=corpo if corpo is not None else {"slides": ["a", "b", "c"], "legenda": "Legenda"},
        status="aprovado",
    )
    db.add(piece)
    await db.flush()
    agendamento = ScheduledPost(
        tenant_id=tenant.id, content_piece_id=piece.id, titulo="Tema",
        canal="instagram", formato=formato,
        data_agendada=date.today() - timedelta(days=1), horario="11:00", status="pronto",
    )
    db.add(agendamento)
    await db.commit()
    return tenant, agendamento


def _api_falsa(MockAPI, post_id="post_123"):
    instancia = MockAPI.return_value
    instancia.publicar_carrossel = AsyncMock(return_value=post_id)
    instancia.publicar_imagem_unica = AsyncMock(return_value=post_id)
    return instancia


@pytest.mark.anyio
async def test_publica_carrossel_com_legenda(db_session, tmp_path):
    tenant, agendamento = await _setup(db_session)

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 1
    urls, = api.publicar_carrossel.await_args.args[1:]
    assert len(urls) == 3
    assert api.publicar_carrossel.await_args.kwargs["legenda"] == "Legenda"
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"
    assert agendamento.platform_post_id == "post_123"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "tipo,corpo",
    [
        ("frase", {"frase": "Pensão não é ajuda.", "legenda": "L"}),
        ("pergunta", {"pergunta": "Fui demitida grávida. E agora?", "legenda": "L"}),
        ("estatico", {"texto_overlay": "Atestado verdadeiro protege", "legenda": "L"}),
    ],
)
async def test_frase_pergunta_e_estatico_publicam_imagem_unica(db_session, tmp_path, tipo, corpo):
    tenant, agendamento = await _setup(db_session, tipo=tipo, corpo=corpo, formato="post")

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 1
    api.publicar_carrossel.assert_not_awaited()
    ig_user_id, url = api.publicar_imagem_unica.await_args.args
    assert ig_user_id == "999"
    assert url.endswith(f"{agendamento.id}-0.png")
    assert api.publicar_imagem_unica.await_args.kwargs["legenda"] == "L"


@pytest.mark.anyio
async def test_sem_conexao_pula_silenciosamente(db_session):
    tenant, agendamento = await _setup(db_session, com_conexao=False)
    publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())
    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "pronto"


@pytest.mark.anyio
async def test_tipo_sem_imagem_nao_e_tentado(db_session):
    """Legenda solta, stories e reels não têm imagem própria: ficam como
    'pronto' para publicação manual, sem gastar tentativas."""
    tenant, agendamento = await _setup(db_session, tipo="legenda", corpo={"texto": "x"}, formato="post")

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI:
        api = _api_falsa(MockAPI)
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 0
    api.publicar_imagem_unica.assert_not_awaited()
    await db_session.refresh(agendamento)
    assert agendamento.status == "pronto"
    assert agendamento.tentativas == 0


@pytest.mark.anyio
async def test_peca_sem_texto_da_imagem_vai_direto_para_erro(db_session, tmp_path):
    """Tentar de novo não resolve uma frase vazia: marca erro na hora."""
    tenant, agendamento = await _setup(db_session, tipo="frase", corpo={"legenda": "L"}, formato="post")

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        _api_falsa(MockAPI)
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "erro"


@pytest.mark.anyio
async def test_falha_incrementa_tentativas_e_marca_erro_apos_3(db_session, tmp_path):
    tenant, agendamento = await _setup(db_session)
    agendamento.tentativas = 2
    await db_session.commit()

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        api.publicar_carrossel = AsyncMock(side_effect=Exception("erro da API"))
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "erro"
    assert agendamento.tentativas == 3


@pytest.mark.anyio
async def test_publica_primeiro_comentario_do_perfil_depois_do_post(db_session, tmp_path):
    corpo = {"slides": ["a", "b"], "legenda": "L", "primeiro_comentario": "Base legal: art. 7º."}
    await _setup(db_session, corpo=corpo)

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        api.comentar = AsyncMock(return_value="c1")
        await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    api.comentar.assert_awaited_once_with("post_123", "Base legal: art. 7º.")


@pytest.mark.anyio
async def test_falha_no_primeiro_comentario_nao_desfaz_a_publicacao(db_session, tmp_path):
    corpo = {"slides": ["a", "b"], "legenda": "L", "primeiro_comentario": "Base legal: art. 7º."}
    _, agendamento = await _setup(db_session, corpo=corpo)

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        api.comentar = AsyncMock(side_effect=RuntimeError("permissão negada"))
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 1
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"
    assert agendamento.platform_post_id == "post_123"


@pytest.mark.anyio
async def test_sem_primeiro_comentario_nao_comenta(db_session, tmp_path):
    await _setup(db_session)

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        api.comentar = AsyncMock()
        await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    api.comentar.assert_not_awaited()


@pytest.mark.anyio
async def test_peca_publicada_passa_a_contar_como_postada_no_editorial(db_session, tmp_path):
    await _setup(db_session)

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        _api_falsa(MockAPI)
        await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    piece = (await db_session.execute(select(ContentPiece))).scalar_one()
    assert piece.status == "publicado"


@pytest.mark.anyio
async def test_publica_reels_agendado_com_legenda_e_primeiro_comentario(db_session, tmp_path):
    corpo = {"video": "https://api.exemplo/media/reel.mp4", "legenda": "Legenda do reel",
             "primeiro_comentario": "📚 Base legal"}
    tenant, agendamento = await _setup(db_session, tipo="reels", corpo=corpo, formato="reels")

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI, post_id="reel_1")
        api.publicar_reels = AsyncMock(return_value="reel_1")
        api.comentar = AsyncMock()
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 1
    assert api.publicar_reels.await_args.args[1:] == ("https://api.exemplo/media/reel.mp4",)
    assert api.publicar_reels.await_args.kwargs["legenda"] == "Legenda do reel"
    api.comentar.assert_awaited_once_with("reel_1", "📚 Base legal")
    await db_session.refresh(agendamento)
    assert agendamento.status == "publicado"


@pytest.mark.anyio
async def test_trial_reels_agendado_sai_no_modo_trial_com_capa(db_session, tmp_path):
    corpo = {"video": "https://api.exemplo/media/reel-b.mp4", "legenda": "Gancho B", "trial_reels": True}
    tenant, agendamento = await _setup(db_session, tipo="reels", corpo=corpo, formato="trial")

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI, post_id="trial_1")
        api.publicar_reels = AsyncMock(return_value="trial_1")
        api.comentar = AsyncMock()
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 1
    assert api.publicar_reels.await_args.kwargs["trial"] is True
    assert api.publicar_reels.await_args.kwargs["graduacao"] == "SS_PERFORMANCE"
    assert api.publicar_reels.await_args.kwargs["capa_ms"] == 1200


@pytest.mark.anyio
async def test_reels_que_depende_do_teste_fica_segurado_se_o_teste_foi_mal(db_session, tmp_path):
    """Pedido de 27/10/2026: o post para seguidores só sai se o Reels de teste foi bem."""
    corpo = {"video": "https://api.exemplo/media/reel.mp4", "legenda": "L", "depende_do_teste": "trial_1"}
    tenant, agendamento = await _setup(db_session, tipo="reels", corpo=corpo, formato="reels")
    db_session.add_all([InstagramPost(tenant_id=tenant.id, media_id=f"m{i}", publicado_em=datetime(2026, 10, i + 1, tzinfo=timezone.utc),
                                      formato="Reels", area="Trabalhista", visualizacoes=300) for i in range(5)])
    await db_session.commit()

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        api.insights_reels = AsyncMock(return_value={"views": 50, "shares": 0, "saved": 0})
        api.publicar_reels = AsyncMock(return_value="reel_1")
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 0 and api.publicar_reels.await_count == 0
    await db_session.refresh(agendamento)
    assert agendamento.status == "segurado"
    api.insights_reels.assert_awaited_once_with("trial_1")


@pytest.mark.anyio
async def test_reels_que_depende_do_teste_sai_se_o_teste_foi_bem(db_session, tmp_path):
    corpo = {"video": "https://api.exemplo/media/reel.mp4", "legenda": "L", "depende_do_teste": "trial_1"}
    tenant, agendamento = await _setup(db_session, tipo="reels", corpo=corpo, formato="reels")

    with patch("app.services.instagram_publisher.InstagramAPI") as MockAPI, patch(
        "app.services.instagram_publisher.MEDIA_DIR", tmp_path
    ):
        api = _api_falsa(MockAPI)
        api.insights_reels = AsyncMock(return_value={"views": 400, "shares": 2, "saved": 1})
        api.publicar_reels = AsyncMock(return_value="reel_1")
        api.comentar = AsyncMock()
        publicados = await publicar_agendamentos_prontos(db_session, renderizador=RenderizadorFalso())

    assert publicados == 1
    assert api.publicar_reels.await_args.kwargs["trial"] is False
