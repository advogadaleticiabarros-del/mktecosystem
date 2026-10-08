from datetime import date, timedelta

import pytest

from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.tenant import Tenant
from app.services.agenda import agendar_conteudo_aprovado, eh_dia_de_tema


def _primeiro_dia_de_tema(a_partir: date) -> date:
    dia = a_partir
    while not eh_dia_de_tema(dia):
        dia += timedelta(days=1)
    return dia


AMANHA = date.today() + timedelta(days=1)
TEMA_1 = _primeiro_dia_de_tema(AMANHA)
TEMA_2 = TEMA_1 + timedelta(days=2)


async def _tenant(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    return tenant


async def _pauta(db, tenant, titulo):
    pauta = Pauta(
        tenant_id=tenant.id, titulo=titulo, angulo="direitos", area="Trabalhista",
        origem="manual", fonte="manual", relevante_para_conteudo=True, status="sugerida",
    )
    db.add(pauta)
    await db.flush()
    return pauta


async def _aprovar(db, tenant, pauta, tipo):
    piece = ContentPiece(tenant_id=tenant.id, pauta_id=pauta.id, tipo=tipo, corpo={}, status="aprovado", versao=1)
    db.add(piece)
    await db.flush()
    agendamento = await agendar_conteudo_aprovado(db, piece)
    await db.flush()
    return agendamento


def test_dias_de_tema_alternam():
    assert eh_dia_de_tema(TEMA_1)
    assert not eh_dia_de_tema(TEMA_1 + timedelta(days=1))
    assert eh_dia_de_tema(TEMA_2)


@pytest.mark.anyio
async def test_pecas_do_mesmo_tema_ficam_no_mesmo_dia_cada_uma_no_seu_horario(db_session):
    tenant = await _tenant(db_session)
    pauta = await _pauta(db_session, tenant, "Gestante")

    pergunta = await _aprovar(db_session, tenant, pauta, "pergunta")
    frase = await _aprovar(db_session, tenant, pauta, "frase")
    carrossel = await _aprovar(db_session, tenant, pauta, "carrossel")

    assert {a.data_agendada for a in (pergunta, frase, carrossel)} == {TEMA_1}
    assert (pergunta.horario, frase.horario, carrossel.horario) == ("12:00", "15:00", "20:00")
    assert pergunta.formato == frase.formato == "post"
    assert carrossel.formato == "carrossel"


@pytest.mark.anyio
async def test_segundo_tema_vai_para_o_proximo_dia_de_tema(db_session):
    tenant = await _tenant(db_session)
    p1 = await _pauta(db_session, tenant, "Gestante")
    p2 = await _pauta(db_session, tenant, "Pensão")

    await _aprovar(db_session, tenant, p1, "carrossel")
    outro = await _aprovar(db_session, tenant, p2, "frase")

    assert outro.data_agendada == TEMA_2


@pytest.mark.anyio
async def test_estatico_vai_para_o_dia_de_respiro_seguinte_ao_tema(db_session):
    tenant = await _tenant(db_session)
    pauta = await _pauta(db_session, tenant, "Gestante")

    await _aprovar(db_session, tenant, pauta, "carrossel")
    estatico = await _aprovar(db_session, tenant, pauta, "estatico")

    assert estatico.data_agendada == TEMA_1 + timedelta(days=1)
    assert estatico.horario == "19:00"
    assert estatico.formato == "post"


@pytest.mark.anyio
async def test_estatico_sem_tema_agendado_pega_o_primeiro_respiro_livre(db_session):
    tenant = await _tenant(db_session)
    p1 = await _pauta(db_session, tenant, "Gestante")
    p2 = await _pauta(db_session, tenant, "Pensão")

    e1 = await _aprovar(db_session, tenant, p1, "estatico")
    e2 = await _aprovar(db_session, tenant, p2, "estatico")

    assert not eh_dia_de_tema(e1.data_agendada)
    assert e1.data_agendada >= AMANHA
    assert e2.data_agendada == e1.data_agendada + timedelta(days=2)


@pytest.mark.anyio
async def test_artigo_continua_no_blog_fora_do_ciclo(db_session):
    tenant = await _tenant(db_session)
    pauta = await _pauta(db_session, tenant, "Gestante")
    artigo = await _aprovar(db_session, tenant, pauta, "artigo")
    assert artigo.canal == "blog"
    assert artigo.horario in ("11:00", "17:00")
