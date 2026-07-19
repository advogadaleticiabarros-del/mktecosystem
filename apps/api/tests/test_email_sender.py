import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.models.contact import Contact
from app.models.email_campaign import EmailCampaign
from app.models.email_send import EmailSend
from app.models.tenant import Tenant, TenantConfig
from app.services.email_sender import (
    contar_envios_hoje,
    processar_boas_vindas,
    processar_fila_newsletter,
)


def _contact(tenant_id, email, criado_ha_dias=0, step=0, status="ativo"):
    agora = datetime.now(timezone.utc)
    return Contact(
        tenant_id=tenant_id,
        nome="Contato",
        email=email,
        origem="lp",
        consentimento_em=agora,
        status=status,
        welcome_step=step,
        criado_em=agora - timedelta(days=criado_ha_dias),
    )


async def _tenant(db):
    tenant = Tenant(nome="Letícia", slug="leticia-barros", nicho="juridico")
    db.add(tenant)
    await db.flush()
    db.add(TenantConfig(tenant_id=tenant.id, voz={"oab": "OAB/ES 39.948"}))
    await db.commit()
    return tenant


def _campanha(tenant_id, tipo, status="aprovado"):
    return EmailCampaign(
        tenant_id=tenant_id,
        tipo=tipo,
        assunto=f"Assunto {tipo}",
        corpo_html="<p>Olá</p>",
        corpo_texto="Olá",
        status=status,
    )


def _mock_resend():
    resend = AsyncMock()
    resend.send.return_value = "re_abc"
    return resend


@pytest.mark.anyio
async def test_boas_vindas_passo1_imediato(db_session):
    tenant = await _tenant(db_session)
    db_session.add(_campanha(tenant.id, "boas_vindas_1"))
    db_session.add(_contact(tenant.id, "novo@example.com", criado_ha_dias=0, step=0))
    await db_session.commit()

    resend = _mock_resend()
    enviados = await processar_boas_vindas(db_session, resend)
    assert enviados == 1
    resend.send.assert_awaited_once()

    result = await db_session.execute(select(Contact))
    assert result.scalar_one().welcome_step == 1


@pytest.mark.anyio
async def test_boas_vindas_passo2_espera_2_dias(db_session):
    tenant = await _tenant(db_session)
    db_session.add(_campanha(tenant.id, "boas_vindas_2"))
    db_session.add(_contact(tenant.id, "cedo@example.com", criado_ha_dias=1, step=1))
    db_session.add(_contact(tenant.id, "pronto@example.com", criado_ha_dias=3, step=1))
    await db_session.commit()

    resend = _mock_resend()
    enviados = await processar_boas_vindas(db_session, resend)
    assert enviados == 1
    to_arg = resend.send.await_args.kwargs["to"]
    assert to_arg == "pronto@example.com"


@pytest.mark.anyio
async def test_boas_vindas_template_nao_aprovado_pula(db_session):
    tenant = await _tenant(db_session)
    db_session.add(_campanha(tenant.id, "boas_vindas_1", status="rascunho"))
    db_session.add(_contact(tenant.id, "novo@example.com", step=0))
    await db_session.commit()

    resend = _mock_resend()
    enviados = await processar_boas_vindas(db_session, resend)
    assert enviados == 0
    resend.send.assert_not_awaited()


@pytest.mark.anyio
async def test_boas_vindas_ignora_descadastrado(db_session):
    tenant = await _tenant(db_session)
    db_session.add(_campanha(tenant.id, "boas_vindas_1"))
    db_session.add(_contact(tenant.id, "fora@example.com", step=0, status="descadastrado"))
    await db_session.commit()

    enviados = await processar_boas_vindas(db_session, _mock_resend())
    assert enviados == 0


@pytest.mark.anyio
async def test_newsletter_envia_e_completa(db_session):
    tenant = await _tenant(db_session)
    campanha = _campanha(tenant.id, "newsletter")
    db_session.add(campanha)
    db_session.add(_contact(tenant.id, "a@example.com"))
    db_session.add(_contact(tenant.id, "b@example.com"))
    db_session.add(_contact(tenant.id, "fora@example.com", status="descadastrado"))
    await db_session.commit()

    resend = _mock_resend()
    enviados = await processar_fila_newsletter(db_session, resend)
    assert enviados == 2

    await db_session.refresh(campanha)
    assert campanha.status == "enviado"
    assert campanha.enviado_em is not None

    sends = (await db_session.execute(select(EmailSend))).scalars().all()
    assert len(sends) == 2


@pytest.mark.anyio
async def test_newsletter_nao_reenvia_para_quem_ja_recebeu(db_session):
    tenant = await _tenant(db_session)
    campanha = _campanha(tenant.id, "newsletter")
    db_session.add(campanha)
    contato = _contact(tenant.id, "a@example.com")
    db_session.add(contato)
    await db_session.flush()
    db_session.add(
        EmailSend(
            tenant_id=tenant.id,
            campaign_id=campanha.id,
            contact_id=contato.id,
            resend_id="re_1",
        )
    )
    await db_session.commit()

    resend = _mock_resend()
    enviados = await processar_fila_newsletter(db_session, resend)
    assert enviados == 0
    resend.send.assert_not_awaited()


@pytest.mark.anyio
async def test_corte_diario_respeitado(db_session, monkeypatch):
    import app.services.email_sender as sender_mod

    monkeypatch.setattr(sender_mod, "LIMITE_DIARIO", 1)
    tenant = await _tenant(db_session)
    db_session.add(_campanha(tenant.id, "newsletter"))
    db_session.add(_contact(tenant.id, "a@example.com"))
    db_session.add(_contact(tenant.id, "b@example.com"))
    await db_session.commit()

    enviados = await processar_fila_newsletter(db_session, _mock_resend())
    assert enviados == 1
    assert await contar_envios_hoje(db_session) == 1
