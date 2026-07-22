import asyncio
import os
import time

from sqlalchemy import select

from app.db import SessionLocal
from app.models.scheduled_post import ScheduledPost

AGENDAMENTO_ID = "c3777c55-2d22-439a-83dc-b1e25dcb1a1b"
INTERVALO_S = 60
TENTATIVAS_MAX = 20


async def checar() -> ScheduledPost | None:
    async with SessionLocal() as db:
        return (
            await db.execute(select(ScheduledPost).where(ScheduledPost.id == AGENDAMENTO_ID))
        ).scalar_one_or_none()


async def main():
    for tentativa in range(1, TENTATIVAS_MAX + 1):
        agendamento = await checar()
        print(f"[{tentativa}] status={agendamento.status} tentativas={agendamento.tentativas} platform_post_id={agendamento.platform_post_id}")
        if agendamento.status == "publicado":
            print("PUBLICADO.")
            return
        if agendamento.tentativas >= 3:
            print("FALHOU (excedeu tentativas).")
            return
        time.sleep(INTERVALO_S)
    print("TIMEOUT sem publicar dentro do prazo monitorado.")


if __name__ == "__main__":
    if "DATABASE_URL" not in os.environ:
        raise SystemExit("Defina DATABASE_URL antes de rodar.")
    asyncio.run(main())
