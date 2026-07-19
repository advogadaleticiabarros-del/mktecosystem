import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.unsubscribe import verify_unsubscribe_token
from app.db import get_db
from app.models.contact import Contact
from app.models.email_send import EmailSend
from app.models.tenant import Tenant
from app.schemas.contact import ContactCreate

router = APIRouter(prefix="/public", tags=["public"])


@router.post("/contacts")
async def criar_contato(
    payload: ContactCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    if payload.website:
        # honeypot preenchido: bot. Responde ok sem gravar para não dar sinal.
        return {"status": "ok"}

    result = await db.execute(select(Tenant).where(Tenant.slug == payload.tenant_slug))
    tenant = result.scalar_one_or_none()
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")

    email = payload.email.lower().strip()
    existing = await db.execute(
        select(Contact).where(Contact.tenant_id == tenant.id, Contact.email == email)
    )
    if existing.scalar_one_or_none() is not None:
        return {"status": "ok"}

    db.add(
        Contact(
            tenant_id=tenant.id,
            nome=payload.nome.strip(),
            email=email,
            origem=payload.origem,
            consentimento_em=datetime.now(timezone.utc),
        )
    )
    await db.commit()
    return {"status": "ok"}


UNSUBSCRIBE_PAGE = """\
<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><title>Descadastro confirmado</title></head>
<body style="font-family: sans-serif; max-width: 480px; margin: 80px auto; text-align: center;">
  <h1>Descadastro confirmado</h1>
  <p>Você não receberá mais nossos e-mails. Se mudar de ideia, é só se inscrever de novo.</p>
</body>
</html>
"""


@router.get("/unsubscribe", response_class=HTMLResponse)
async def descadastrar(
    token: Annotated[str, Query()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HTMLResponse:
    contact_id = verify_unsubscribe_token(token)
    if contact_id is None:
        raise HTTPException(status_code=400, detail="Token inválido")

    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if contact is not None:
        contact.status = "descadastrado"
        await db.commit()
    return HTMLResponse(UNSUBSCRIBE_PAGE)


def _verificar_assinatura_svix(request: Request, payload: bytes) -> bool:
    """Verifica a assinatura Svix do webhook (formato do Resend).

    Assinado: "{svix-id}.{svix-timestamp}.{payload}" com HMAC-SHA256, chave =
    base64 do segredo após o prefixo "whsec_".
    """
    secret = settings.RESEND_WEBHOOK_SECRET
    if not secret:
        return False
    msg_id = request.headers.get("svix-id", "")
    timestamp = request.headers.get("svix-timestamp", "")
    signatures = request.headers.get("svix-signature", "")
    if not (msg_id and timestamp and signatures):
        return False

    try:
        key = base64.b64decode(secret.split("_", 1)[1] if "_" in secret else secret)
    except Exception:
        return False
    to_sign = f"{msg_id}.{timestamp}.{payload.decode()}".encode()
    expected = base64.b64encode(hmac.new(key, to_sign, hashlib.sha256).digest()).decode()

    for candidate in signatures.split(" "):
        parts = candidate.split(",", 1)
        if len(parts) == 2 and hmac.compare_digest(parts[1], expected):
            return True
    return False


@router.post("/webhooks/resend")
async def webhook_resend(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    payload = await request.body()
    if not _verificar_assinatura_svix(request, payload):
        raise HTTPException(status_code=401, detail="Assinatura inválida")

    evento = json.loads(payload)
    tipo = evento.get("type", "")
    email_id = (evento.get("data") or {}).get("email_id", "")
    if tipo not in ("email.bounced", "email.complained") or not email_id:
        return {"status": "ignorado"}

    result = await db.execute(select(EmailSend).where(EmailSend.resend_id == email_id))
    send = result.scalar_one_or_none()
    if send is None:
        return {"status": "ignorado"}

    novo_status_contato = "bounce" if tipo == "email.bounced" else "descadastrado"
    send.status = "bounce" if tipo == "email.bounced" else "reclamacao"

    contato = (
        await db.execute(select(Contact).where(Contact.id == send.contact_id))
    ).scalar_one_or_none()
    if contato is not None:
        contato.status = novo_status_contato

    await db.commit()
    return {"status": "processado"}
