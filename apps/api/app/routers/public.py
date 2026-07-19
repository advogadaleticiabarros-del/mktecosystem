from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.unsubscribe import verify_unsubscribe_token
from app.db import get_db
from app.models.contact import Contact
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
