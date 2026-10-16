"""Instagram: 1 publicação por dia (pedido da Letícia, 16/10/2026). Em dia de Reels, só o Reels, à noite.
Horários pelo alcance real do perfil: Reels 21h; feed 14h de segunda a sexta e 11h no sábado e no domingo."""
from datetime import date, timedelta

import pytest

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant
from app.services.agenda import agendar_conteudo_aprovado, horario_instagram

AMANHA = date.today() + timedelta(days=1)


async def _tenant(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    return tenant


async def _aprovar(db, tenant, tipo, titulo="Gestante", corpo=None):
    pauta = Pauta(tenant_id=tenant.id, titulo=titulo, angulo="direitos", area="Trabalhista", origem="manual",
                  fonte="manual", relevante_para_conteudo=True, status="sugerida")
    db.add(pauta)
    await db.flush()
    piece = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo=tipo, corpo=corpo or {}, status="aprovado", versao=1)
    db.add(piece)
    await db.flush()
    agendamento = await agendar_conteudo_aprovado(db, piece)
    await db.flush()
    return agendamento


def test_horarios_reels_a_noite_feed_14h_na_semana_e_11h_no_fim_de_semana():
    sexta, sabado, domingo = date(2026, 10, 16), date(2026, 10, 17), date(2026, 10, 18)
    assert horario_instagram("reels", sexta) == horario_instagram("reels", domingo) == "21:00"
    assert horario_instagram("carrossel", sexta) == "14:00"
    assert horario_instagram("frase", sabado) == horario_instagram("estatico", domingo) == "11:00"


@pytest.mark.anyio
async def test_cada_peca_aprovada_vai_para_o_proximo_dia_sem_post(db_session):
    tenant = await _tenant(db_session)
    pergunta = await _aprovar(db_session, tenant, "pergunta")
    frase = await _aprovar(db_session, tenant, "frase")
    carrossel = await _aprovar(db_session, tenant, "carrossel")

    assert [a.data_agendada for a in (pergunta, frase, carrossel)] == [AMANHA + timedelta(days=i) for i in range(3)]
    assert carrossel.formato == "carrossel" and pergunta.formato == frase.formato == "post"
    for a in (pergunta, frase, carrossel):
        assert a.horario == horario_instagram(a.formato, a.data_agendada)


@pytest.mark.anyio
async def test_dia_de_reels_fica_so_com_o_reels(db_session):
    tenant = await _tenant(db_session)
    reels = await _aprovar(db_session, tenant, "reels")
    estatico = await _aprovar(db_session, tenant, "estatico")

    assert reels.data_agendada == AMANHA and reels.horario == "21:00" and reels.formato == "reels"
    assert estatico.data_agendada == AMANHA + timedelta(days=1)


@pytest.mark.anyio
async def test_pula_o_dia_que_ja_tem_post_e_ignora_blog_e_stories(db_session):
    tenant = await _tenant(db_session)
    for dia, canal, formato in [(AMANHA, "instagram", "post"), (AMANHA + timedelta(days=1), "blog", "artigo"),
                                (AMANHA + timedelta(days=1), "instagram", "story")]:
        db_session.add(ScheduledPost(tenant_id=tenant.id, titulo="x", canal=canal, formato=formato,
                                     data_agendada=dia, horario="10:00", status="pronto"))
    await db_session.flush()

    carrossel = await _aprovar(db_session, tenant, "carrossel")
    assert carrossel.data_agendada == AMANHA + timedelta(days=1)


@pytest.mark.anyio
async def test_programacao_combinada_continua_valendo(db_session):
    tenant = await _tenant(db_session)
    a = await _aprovar(db_session, tenant, "reels", corpo={"programacao": {"data": "2026-10-23", "hora": "21:00"}})
    assert (a.data_agendada, a.horario) == (date(2026, 10, 23), "21:00")


@pytest.mark.anyio
async def test_artigo_continua_no_blog(db_session):
    tenant = await _tenant(db_session)
    artigo = await _aprovar(db_session, tenant, "artigo")
    assert artigo.canal == "blog" and artigo.horario in ("11:00", "17:00")
