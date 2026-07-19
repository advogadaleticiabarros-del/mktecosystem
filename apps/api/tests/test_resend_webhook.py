import base64
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.config import settings
from app.models.contact import Contact
from app.models.email_campaign import EmailCampaign
from app.models.email_send import EmailSend
from app.models.tenant import Tenant

SECRET = "whsec_" + base64.b64encode(b"segredo-de-teste-32-bytes-ok!!!").decode()


def _svix_headers(payload: bytes, secret: str = SECRET) -> dict[str, str]:
    msg_id = "msg_teste"
    timestamp = str(int(datetime.now(timezone.utc).timestamp()))
    to_sign = f"{msg_id}.{timestamp}.{payload.decode()}".encode()
    key = base64.b64decode(secret.split("_", 1)[1])
    signature = base64.b64encode(hmac.new(key, to_sign, hashlib.sha256).digest()).decode()
    return {
        "svix-id": msg_id,
        "svix-timestamp": timestamp,
        "svix-signature": f"v1,{signature}",
        "content-type": "application/json",
    }


async def _setup(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    contato = Contact(
        tenant_id=tenant.id,
        nome="Maria",
        email="maria@example.com",
        origem="lp",
        consentimento_em=datetime.now(timezone.utc),
    )
    campanha = EmailCampaign(
        tenant_id=tenant.id, tipo="newsletter", assunto="Oi", corpo_html="<p>x</p>"
    )
    db.add_all([contato, campanha])
    await db.flush()
    send = EmailSend(
        tenant_id=tenant.id,
        campaign_id=campanha.id,
        contact_id=contato.id,
        resend_id="re_bounce_1",
    )
    db.add(send)
    await db.commit()
    return contato, send


@pytest.mark.anyio
async def test_bounce_marca_contato_e_send(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "RESEND_WEBHOOK_SECRET", SECRET)
    contato, send = await _setup(db_session)

    payload = json.dumps(
        {"type": "email.bounced", "data": {"email_id": "re_bounce_1"}}
    ).encode()
    resp = await client.post(
        "/public/webhooks/resend", content=payload, headers=_svix_headers(payload)
    )
    assert resp.status_code == 200

    await db_session.refresh(contato)
    await db_session.refresh(send)
    assert contato.status == "bounce"
    assert send.status == "bounce"


@pytest.mark.anyio
async def test_reclamacao_descadastra(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "RESEND_WEBHOOK_SECRET", SECRET)
    contato, send = await _setup(db_session)

    payload = json.dumps(
        {"type": "email.complained", "data": {"email_id": "re_bounce_1"}}
    ).encode()
    resp = await client.post(
        "/public/webhooks/resend", content=payload, headers=_svix_headers(payload)
    )
    assert resp.status_code == 200
    await db_session.refresh(contato)
    assert contato.status == "descadastrado"


@pytest.mark.anyio
async def test_assinatura_invalida_401(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "RESEND_WEBHOOK_SECRET", SECRET)
    await _setup(db_session)

    payload = json.dumps({"type": "email.bounced", "data": {"email_id": "re_bounce_1"}}).encode()
    headers = _svix_headers(payload)
    headers["svix-signature"] = "v1,invalida"
    resp = await client.post("/public/webhooks/resend", content=payload, headers=headers)
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_evento_desconhecido_ignorado(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "RESEND_WEBHOOK_SECRET", SECRET)
    await _setup(db_session)

    payload = json.dumps({"type": "email.opened", "data": {"email_id": "re_bounce_1"}}).encode()
    resp = await client.post(
        "/public/webhooks/resend", content=payload, headers=_svix_headers(payload)
    )
    assert resp.status_code == 200
