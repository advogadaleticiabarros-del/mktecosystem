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

    esperado, dia = [], AMANHA
    while len(esperado) < 3:
        if dia.weekday() not in (1, 4):  # terça e sexta ficam para os Reels
            esperado.append(dia)
        dia += timedelta(days=1)
    assert [a.data_agendada for a in (pergunta, frase, carrossel)] == esperado
    assert carrossel.formato == "carrossel" and pergunta.formato == frase.formato == "post"
    for a in (pergunta, frase, carrossel):
        assert a.horario == horario_instagram(a.formato, a.data_agendada)


def _proximo(dia: date, dias_semana: set[int]) -> date:
    while dia.weekday() not in dias_semana:
        dia += timedelta(days=1)
    return dia


@pytest.mark.anyio
async def test_reels_so_terca_e_sexta_e_o_feed_nos_outros_dias(db_session):
    """Pedido de 23/10/2026: Reels só 2 vezes por semana, para cada um ter tempo de se destacar."""
    tenant = await _tenant(db_session)
    r1 = await _aprovar(db_session, tenant, "reels")
    r2 = await _aprovar(db_session, tenant, "reels")
    r3 = await _aprovar(db_session, tenant, "reels")
    estatico = await _aprovar(db_session, tenant, "estatico")

    dias = [r.data_agendada for r in (r1, r2, r3)]
    assert all(d.weekday() in (1, 4) for d in dias) and len(set(dias)) == 3
    assert dias[0] == _proximo(AMANHA, {1, 4}) and dias == sorted(dias)
    assert {r.horario for r in (r1, r2, r3)} == {"21:00"} and r1.formato == "reels"
    assert estatico.data_agendada.weekday() not in (1, 4)
    assert estatico.data_agendada == _proximo(AMANHA, {0, 2, 3, 5, 6})


@pytest.mark.anyio
async def test_reels_com_data_combinada_fora_de_terca_ou_sexta_vai_para_a_proxima(db_session):
    tenant = await _tenant(db_session)
    quarta = date(2026, 10, 28)
    a = await _aprovar(db_session, tenant, "reels", corpo={"programacao": {"data": quarta.isoformat(), "hora": "21:00"}})
    assert (a.data_agendada, a.horario) == (date(2026, 10, 30), "21:00")


@pytest.mark.anyio
async def test_pula_o_dia_que_ja_tem_post_e_ignora_blog_e_stories(db_session):
    tenant = await _tenant(db_session)
    primeiro = _proximo(AMANHA, {0, 2, 3, 5, 6})
    segundo = _proximo(primeiro + timedelta(days=1), {0, 2, 3, 5, 6})
    for dia, canal, formato in [(primeiro, "instagram", "post"), (segundo, "blog", "artigo"),
                                (segundo, "instagram", "story")]:
        db_session.add(ScheduledPost(tenant_id=tenant.id, titulo="x", canal=canal, formato=formato,
                                     data_agendada=dia, horario="10:00", status="pronto"))
    await db_session.flush()

    carrossel = await _aprovar(db_session, tenant, "carrossel")
    assert carrossel.data_agendada == segundo


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


@pytest.mark.anyio
async def test_trial_reels_nao_ocupa_o_dia_dos_seguidores(db_session):
    """Trial Reels só aparece para quem não segue: não conta na regra de 1 publicação por dia."""
    tenant = await _tenant(db_session)
    dia = _proximo(AMANHA, {0, 2, 3, 5, 6})
    db_session.add(ScheduledPost(tenant_id=tenant.id, titulo="x", canal="instagram", formato="trial",
                                 data_agendada=dia, horario="12:00", status="pronto"))
    await db_session.flush()
    carrossel = await _aprovar(db_session, tenant, "carrossel")
    assert carrossel.data_agendada == dia
