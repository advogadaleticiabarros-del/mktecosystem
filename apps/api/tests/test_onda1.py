from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.core.security import create_access_token, hash_password
from app.models.content_piece import ContentPiece
from app.models.marketing_memory import MarketingMemory
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant, TenantConfig
from app.models.user import User


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={"oab": "OAB/ES 39.948"}))
    user = User(
        tenant_id=tenant.id,
        email="leticia@example.com",
        nome="Letícia",
        hashed_password=hash_password("senha"),
        role="owner",
    )
    pauta = Pauta(
        tenant_id=tenant.id,
        titulo="Direitos da gestante",
        angulo="direitos",
        area="Trabalhista",
        origem="manual",
        fonte="manual",
        relevante_para_conteudo=True,
    )
    db.add_all([user, pauta])
    await db.flush()
    piece = ContentPiece(
        tenant_id=tenant.id,
        pauta_id=pauta.id,
        tipo="carrossel",
        corpo={"slides": ["a", "b", "c", "d", "e"]},
    )
    db.add(piece)
    await db.commit()
    return tenant, user, pauta, piece


@pytest.mark.anyio
async def test_aprovar_agenda_no_calendario(client, db_session):
    tenant, user, pauta, piece = await _setup(db_session)
    token = create_access_token(user.id)

    resp = await client.patch(
        f"/content/{piece.id}",
        json={"status": "aprovado"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200

    agendado = (await db_session.execute(select(ScheduledPost))).scalar_one()
    assert agendado.content_piece_id == piece.id
    assert agendado.titulo == "Direitos da gestante"
    assert agendado.formato == "carrossel"
    assert agendado.canal == "instagram"
    assert agendado.data_agendada == date.today() + timedelta(days=1)
    assert agendado.horario == "11:00"
    assert agendado.status == "pronto"


@pytest.mark.anyio
async def test_aprovar_duas_vezes_nao_duplica_agenda(client, db_session):
    tenant, user, pauta, piece = await _setup(db_session)
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    await client.patch(f"/content/{piece.id}", json={"status": "aprovado"}, headers=headers)
    await client.patch(f"/content/{piece.id}", json={"status": "aprovado"}, headers=headers)

    agendados = (await db_session.execute(select(ScheduledPost))).scalars().all()
    assert len(agendados) == 1


@pytest.mark.anyio
async def test_editar_corpo_registra_licao(client, db_session):
    tenant, user, pauta, piece = await _setup(db_session)
    token = create_access_token(user.id)

    resp = await client.patch(
        f"/content/{piece.id}",
        json={"corpo": {"slides": ["novo gancho", "b", "c", "d", "e"]}},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200

    memoria = (await db_session.execute(select(MarketingMemory))).scalar_one()
    assert memoria.aprendizado is not None
    assert "slides" in memoria.aprendizado
    assert memoria.metricas == {"tipo_evento": "edicao"}


@pytest.mark.anyio
async def test_calendario_crud_e_listagem_mes(client, db_session):
    tenant, user, _, _ = await _setup(db_session)
    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/calendario",
        json={
            "titulo": "Post manual",
            "canal": "instagram",
            "formato": "post",
            "data_agendada": "2026-08-10",
            "horario": "17:00",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    criado = resp.json()

    resp = await client.get("/calendario?mes=2026-08", headers=headers)
    assert [a["id"] for a in resp.json()] == [criado["id"]]

    resp = await client.get("/calendario?mes=2026-09", headers=headers)
    assert resp.json() == []

    resp = await client.patch(
        f"/calendario/{criado['id']}", json={"status": "publicado"}, headers=headers
    )
    assert resp.json()["status"] == "publicado"

    resp = await client.delete(f"/calendario/{criado['id']}", headers=headers)
    assert resp.status_code == 204


@pytest.mark.anyio
async def test_dashboard_resumo(client, db_session):
    tenant, user, pauta, piece = await _setup(db_session)
    token = create_access_token(user.id)

    resp = await client.get("/dashboard/resumo", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["pautas_total"] == 1
    assert body["conteudos_por_status"] == {"rascunho": 1}
    assert len(body["producao_semanal"]) == 8
    assert body["producao_semanal"][-1]["conteudos"] == 1
