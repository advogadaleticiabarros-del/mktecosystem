import os

if "DATABASE_URL" not in os.environ:
    raise SystemExit(
        "Defina DATABASE_URL (postgresql+asyncpg://...) no ambiente antes de rodar este script."
    )

import asyncio
from datetime import date

from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.pauta import Pauta
from app.models.scheduled_post import ScheduledPost
from app.models.tenant import Tenant

TITULO = "BPC para criança com deficiência: o benefício de R$ 1.621 que muita mãe não conhece"
META_DESCRIPTION = "Seu filho tem deficiência e a rotina pesa no bolso? O BPC/LOAS paga 1 salário mínimo por mês, sem precisar ter contribuído com o INSS. Veja quem tem direito."
RESUMO = "O BPC paga 1 salário mínimo por mês a crianças com deficiência de famílias de baixa renda, sem precisar ter contribuído ao INSS. Veja se seu filho tem direito."

CORPO_HTML = open("_teste_bpc_corpo_html.txt", encoding="utf-8").read()

HORARIO_ALVO = "19:00"


async def main():
    async with SessionLocal() as db:
        tenant = (await db.execute(select(Tenant))).scalars().first()
        if tenant is None:
            raise SystemExit("Nenhum tenant encontrado no banco.")
        print(f"Tenant: {tenant.nome} ({tenant.id})")

        pauta = Pauta(
            tenant_id=tenant.id,
            titulo="BPC para criança com deficiência",
            angulo="direitos",
            area="Previdenciário",
            origem="manual",
            fonte="Claude (teste assistido)",
            relevante_para_conteudo=True,
            status="aprovada",
        )
        db.add(pauta)
        await db.flush()

        piece = ContentPiece(
            tenant_id=tenant.id,
            pauta_id=pauta.id,
            tipo="artigo",
            corpo={
                "titulo": TITULO,
                "html": CORPO_HTML,
                "meta_description": META_DESCRIPTION,
                "resumo": RESUMO,
            },
            status="aprovado",
            versao=1,
        )
        db.add(piece)
        await db.flush()

        agendamento = ScheduledPost(
            tenant_id=tenant.id,
            content_piece_id=piece.id,
            titulo=pauta.titulo,
            canal="blog",
            formato="artigo",
            data_agendada=date.today(),
            horario=HORARIO_ALVO,
            status="pronto",
        )
        db.add(agendamento)
        await db.commit()

        print(f"Pauta: {pauta.id}")
        print(f"ContentPiece: {piece.id}")
        print(f"ScheduledPost: {agendamento.id} -> {agendamento.data_agendada} {agendamento.horario} status={agendamento.status}")


if __name__ == "__main__":
    asyncio.run(main())
