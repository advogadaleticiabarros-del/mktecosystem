import os

if "DATABASE_URL" not in os.environ:
    raise SystemExit(
        "Defina DATABASE_URL (postgresql+asyncpg://...) no ambiente antes de rodar este script."
    )

import asyncio
from datetime import date

from sqlalchemy import select

from app.db import SessionLocal
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant

TITULO = "Prazo pra processar a empresa após demissão (estático - Me faça uma pergunta)"
DATA_ALVO = date(2026, 7, 23)
HORARIO_ALVO = "12:00"


async def main():
    async with SessionLocal() as db:
        tenant = (await db.execute(select(Tenant))).scalars().first()
        if tenant is None:
            raise SystemExit("Nenhum tenant encontrado no banco.")
        print(f"Tenant: {tenant.nome} ({tenant.id})")

        agendamento = ScheduledPost(
            tenant_id=tenant.id,
            content_piece_id=None,
            titulo=TITULO,
            canal="instagram",
            formato="post",
            data_agendada=DATA_ALVO,
            horario=HORARIO_ALVO,
            status="pronto",
        )
        db.add(agendamento)
        await db.commit()

        print(f"ScheduledPost: {agendamento.id} -> {agendamento.data_agendada} {agendamento.horario} status={agendamento.status}")


if __name__ == "__main__":
    asyncio.run(main())
