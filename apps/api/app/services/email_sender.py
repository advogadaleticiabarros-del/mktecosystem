"""Processadores de envio: sequência de boas-vindas e fila de newsletter.

Invariantes:
- Só envia campanha com status="aprovado".
- Só envia para contato status="ativo".
- Nunca ultrapassa LIMITE_DIARIO envios por dia (todos os tenants somados).
- (campaign_id, contact_id) é único: um contato nunca recebe a mesma campanha 2x.
"""
import logging
from datetime import datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.unsubscribe import make_unsubscribe_token
from app.integrations.email.resend_client import ResendClient, montar_rodape
from app.models.contact import Contact
from app.models.email_campaign import EmailCampaign
from app.models.email_send import EmailSend
from app.models.tenant import TenantConfig

logger = logging.getLogger(__name__)

LIMITE_DIARIO = 90  # margem sob o teto de 100/dia do Resend Free
CADENCIA_DIAS = {0: 0, 1: 2, 2: 5}  # welcome_step atual -> dias desde criado_em


async def contar_envios_hoje(db: AsyncSession) -> int:
    inicio_do_dia = datetime.combine(
        datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc
    )
    result = await db.execute(
        select(func.count(EmailSend.id)).where(EmailSend.criado_em >= inicio_do_dia)
    )
    return result.scalar_one()


async def _assinatura(db: AsyncSession, tenant_id) -> str:
    result = await db.execute(select(TenantConfig).where(TenantConfig.tenant_id == tenant_id))
    config = result.scalar_one_or_none()
    oab = (config.voz or {}).get("oab", "") if config else ""
    return oab


async def _enviar(
    db: AsyncSession,
    resend: ResendClient,
    campanha: EmailCampaign,
    contato: Contact,
) -> bool:
    unsubscribe_url = (
        f"{settings.PUBLIC_API_URL}/public/unsubscribe"
        f"?token={make_unsubscribe_token(contato.id)}"
    )
    rodape = montar_rodape(await _assinatura(db, contato.tenant_id), unsubscribe_url)
    try:
        resend_id = await resend.send(
            to=contato.email,
            subject=campanha.assunto,
            html=campanha.corpo_html + rodape,
            text=f"{campanha.corpo_texto}\n\nDescadastrar: {unsubscribe_url}",
        )
    except Exception:
        logger.exception("Falha ao enviar campanha %s para %s", campanha.id, contato.email)
        db.add(
            EmailSend(
                tenant_id=contato.tenant_id,
                campaign_id=campanha.id,
                contact_id=contato.id,
                status="erro",
            )
        )
        await db.commit()
        return False

    db.add(
        EmailSend(
            tenant_id=contato.tenant_id,
            campaign_id=campanha.id,
            contact_id=contato.id,
            resend_id=resend_id,
            status="enviado",
        )
    )
    await db.commit()
    return True


async def processar_boas_vindas(db: AsyncSession, resend: ResendClient) -> int:
    """Envia o próximo passo da sequência para contatos com tempo decorrido."""
    agora = datetime.now(timezone.utc)
    enviados = 0

    result = await db.execute(
        select(Contact).where(Contact.status == "ativo", Contact.welcome_step < 3)
    )
    for contato in result.scalars().all():
        if await contar_envios_hoje(db) >= LIMITE_DIARIO:
            logger.info("Limite diário atingido; boas-vindas pausadas até amanhã.")
            break

        dias_necessarios = CADENCIA_DIAS[contato.welcome_step]
        criado_em = contato.criado_em
        if criado_em.tzinfo is None:
            criado_em = criado_em.replace(tzinfo=timezone.utc)
        if agora - criado_em < timedelta(days=dias_necessarios):
            continue

        tipo = f"boas_vindas_{contato.welcome_step + 1}"
        template = (
            await db.execute(
                select(EmailCampaign).where(
                    EmailCampaign.tenant_id == contato.tenant_id,
                    EmailCampaign.tipo == tipo,
                    EmailCampaign.status == "aprovado",
                )
            )
        ).scalars().first()
        if template is None:
            continue

        ja_recebeu = (
            await db.execute(
                select(EmailSend).where(
                    EmailSend.campaign_id == template.id,
                    EmailSend.contact_id == contato.id,
                    EmailSend.status != "erro",
                )
            )
        ).scalar_one_or_none()
        if ja_recebeu is not None:
            contato.welcome_step += 1
            await db.commit()
            continue

        if await _enviar(db, resend, template, contato):
            contato.welcome_step += 1
            await db.commit()
            enviados += 1

    return enviados


async def processar_fila_newsletter(db: AsyncSession, resend: ResendClient) -> int:
    """Envia newsletters aprovadas para a base ativa, respeitando o teto diário."""
    enviados = 0
    campanhas = (
        (
            await db.execute(
                select(EmailCampaign).where(
                    EmailCampaign.tipo == "newsletter",
                    EmailCampaign.status == "aprovado",
                )
            )
        )
        .scalars()
        .all()
    )

    for campanha in campanhas:
        ja_enviados = select(EmailSend.contact_id).where(
            EmailSend.campaign_id == campanha.id, EmailSend.status != "erro"
        )
        pendentes = (
            (
                await db.execute(
                    select(Contact).where(
                        Contact.tenant_id == campanha.tenant_id,
                        Contact.status == "ativo",
                        Contact.id.not_in(ja_enviados),
                    )
                )
            )
            .scalars()
            .all()
        )

        atingiu_limite = False
        for contato in pendentes:
            if await contar_envios_hoje(db) >= LIMITE_DIARIO:
                logger.info("Limite diário atingido; newsletter continua amanhã.")
                atingiu_limite = True
                break
            if await _enviar(db, resend, campanha, contato):
                enviados += 1

        if not atingiu_limite:
            restantes = (
                await db.execute(
                    select(func.count(Contact.id)).where(
                        Contact.tenant_id == campanha.tenant_id,
                        Contact.status == "ativo",
                        Contact.id.not_in(
                            select(EmailSend.contact_id).where(
                                EmailSend.campaign_id == campanha.id,
                                EmailSend.status != "erro",
                            )
                        ),
                    )
                )
            ).scalar_one()
            if restantes == 0:
                campanha.status = "enviado"
                campanha.enviado_em = datetime.now(timezone.utc)
                await db.commit()

    return enviados
