import uuid

import pytest
from sqlalchemy import select

from app.core.unsubscribe import make_unsubscribe_token, verify_unsubscribe_token
from app.models.contact import Contact
from app.models.tenant import Tenant


async def _make_tenant(db_session) -> Tenant:
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db_session.add(tenant)
    await db_session.commit()
    return tenant


def test_unsubscribe_token_roundtrip():
    contact_id = uuid.uuid4()
    token = make_unsubscribe_token(contact_id)
    assert verify_unsubscribe_token(token) == contact_id


def test_unsubscribe_token_tampered_rejected():
    token = make_unsubscribe_token(uuid.uuid4())
    parts = token.split(".")
    tampered = f"{uuid.uuid4().hex}.{parts[1]}"
    assert verify_unsubscribe_token(tampered) is None
    assert verify_unsubscribe_token("lixo") is None
    assert verify_unsubscribe_token("") is None


@pytest.mark.anyio
async def test_criar_contato_grava_consentimento(client, db_session):
    tenant = await _make_tenant(db_session)
    resp = await client.post(
        "/public/contacts",
        json={
            "tenant_slug": tenant.slug,
            "nome": "Maria",
            "email": "maria@example.com",
            "origem": "lp",
            "website": "",
        },
    )
    assert resp.status_code == 200
    result = await db_session.execute(select(Contact).where(Contact.email == "maria@example.com"))
    contact = result.scalar_one()
    assert contact.status == "ativo"
    assert contact.consentimento_em is not None
    assert contact.welcome_step == 0


@pytest.mark.anyio
async def test_honeypot_descarta_sem_gravar(client, db_session):
    tenant = await _make_tenant(db_session)
    resp = await client.post(
        "/public/contacts",
        json={
            "tenant_slug": tenant.slug,
            "nome": "Bot",
            "email": "bot@example.com",
            "origem": "lp",
            "website": "http://spam.example",
        },
    )
    assert resp.status_code == 200
    result = await db_session.execute(select(Contact).where(Contact.email == "bot@example.com"))
    assert result.scalar_one_or_none() is None


@pytest.mark.anyio
async def test_contato_duplicado_idempotente(client, db_session):
    tenant = await _make_tenant(db_session)
    payload = {
        "tenant_slug": tenant.slug,
        "nome": "Maria",
        "email": "maria@example.com",
        "origem": "blog",
        "website": "",
    }
    assert (await client.post("/public/contacts", json=payload)).status_code == 200
    assert (await client.post("/public/contacts", json=payload)).status_code == 200
    result = await db_session.execute(select(Contact).where(Contact.email == "maria@example.com"))
    assert len(result.scalars().all()) == 1


@pytest.mark.anyio
async def test_tenant_desconhecido_404(client, db_session):
    resp = await client.post(
        "/public/contacts",
        json={
            "tenant_slug": "nao-existe",
            "nome": "X",
            "email": "x@example.com",
            "origem": "lp",
            "website": "",
        },
    )
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_unsubscribe_marca_descadastrado(client, db_session):
    from datetime import datetime, timezone

    tenant = await _make_tenant(db_session)
    contact = Contact(
        tenant_id=tenant.id,
        nome="Maria",
        email="maria@example.com",
        origem="lp",
        consentimento_em=datetime.now(timezone.utc),
    )
    db_session.add(contact)
    await db_session.commit()

    token = make_unsubscribe_token(contact.id)
    resp = await client.get(f"/public/unsubscribe?token={token}")
    assert resp.status_code == 200
    await db_session.refresh(contact)
    assert contact.status == "descadastrado"


@pytest.mark.anyio
async def test_unsubscribe_token_invalido_400(client, db_session):
    resp = await client.get("/public/unsubscribe?token=invalido")
    assert resp.status_code == 400
