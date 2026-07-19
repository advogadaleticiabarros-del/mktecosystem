"""Agendador in-process: boas-vindas/newsletter de hora em hora, rascunho às segundas.

Ativado só com ENABLE_SCHEDULER=true (produção). Em dev/testes fica desligado
para não disparar envios acidentais.
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select

from app.config import settings
from app.db import SessionLocal
from app.integrations.ai.gemini import GeminiClient
from app.integrations.email.resend_client import ResendClient
from app.models.tenant import Tenant
from app.services.email_campaigns import gerar_rascunho_newsletter
from app.services.email_sender import processar_boas_vindas, processar_fila_newsletter

logger = logging.getLogger(__name__)


def _resend() -> ResendClient:
    return ResendClient(api_key=settings.RESEND_API_KEY, sender=settings.EMAIL_FROM)


async def job_envios() -> None:
    async with SessionLocal() as db:
        resend = _resend()
        bv = await processar_boas_vindas(db, resend)
        nl = await processar_fila_newsletter(db, resend)
        if bv or nl:
            logger.info("Envios: %d boas-vindas, %d newsletter.", bv, nl)


async def job_rascunho_newsletter() -> None:
    async with SessionLocal() as db:
        ai = GeminiClient(api_key=settings.GEMINI_API_KEY)
        tenants = (await db.execute(select(Tenant).where(Tenant.ativo))).scalars().all()
        for tenant in tenants:
            try:
                campanha = await gerar_rascunho_newsletter(db, tenant.id, ai)
                if campanha is not None:
                    logger.info("Rascunho de newsletter criado para %s.", tenant.slug)
            except Exception:
                logger.exception("Falha ao gerar newsletter para %s", tenant.slug)


def criar_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(job_envios, CronTrigger(minute=15))
    # Segunda 11:00 UTC = 08:00 em Brasília
    scheduler.add_job(job_rascunho_newsletter, CronTrigger(day_of_week="mon", hour=11))
    return scheduler
