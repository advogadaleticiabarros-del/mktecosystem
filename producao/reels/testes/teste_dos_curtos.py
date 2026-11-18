"""Roda DENTRO do container da API (18/11/2026): cada Reels curto agendado (Mito ou Lei e Flagrante) ganha uma cópia
como Reels de teste (Trial Reels), além do Reels normal, que continua no horário de sempre.
Pedido da Jessica: "todos os reels curtos que ainda estão para sair, vamos jogar para reels teste, mas mantenha a data
de publicação normal" + "é para publicar duas vezes" + teste "mesmo dia, 10h".
Graduação MANUAL: o normal das 19h já chega aos seguidores; o teste só mede o alcance em quem não segue.
A cópia não leva a marcação do TikTok nem a programação da peça original. Idempotente.
Uso: docker compose exec -T -e PYTHONPATH=/app api python /tmp/teste_dos_curtos.py [--hoje-as HH:MM] [--simular]
"""
import asyncio
import copy
import sys
from sqlalchemy import select

from app.db import SessionLocal
from app.models.content_piece import ContentPiece
from app.models.scheduled_post import ScheduledPost
from app.services.agenda import hoje_brasilia

HORA_TESTE = "10:00"
PREFIXOS = ("Mito ou Lei:", "Reels Flagrante:")
FORA_DA_COPIA = ("tiktok", "programacao", "versoes_anteriores", "depende_do_teste")


async def main(simular: bool, hoje_as: str | None):
    hoje = hoje_brasilia()
    async with SessionLocal() as db:
        normais = (await db.execute(select(ScheduledPost).where(
            ScheduledPost.canal == "instagram", ScheduledPost.formato == "reels", ScheduledPost.status == "pronto",
            ScheduledPost.data_agendada >= hoje).order_by(ScheduledPost.data_agendada))).scalars().all()
        criados = 0
        for sp in normais:
            if not sp.titulo.startswith(PREFIXOS):
                continue
            titulo = f"Teste · {sp.titulo}"
            ja = (await db.execute(select(ScheduledPost).where(ScheduledPost.tenant_id == sp.tenant_id,
                  ScheduledPost.formato == "trial", ScheduledPost.titulo == titulo,
                  ScheduledPost.data_agendada == sp.data_agendada))).scalars().first()
            if ja:
                print("já existe:", titulo); continue
            hora = (hoje_as or HORA_TESTE) if sp.data_agendada == hoje else HORA_TESTE
            if sp.data_agendada == hoje and hora >= sp.horario:
                print("sem tempo hoje:", titulo); continue
            original = await db.get(ContentPiece, sp.content_piece_id)
            corpo = {k: copy.deepcopy(v) for k, v in (original.corpo or {}).items() if k not in FORA_DA_COPIA}
            corpo.update(trial_reels=True, trial_graduacao="MANUAL", teste_de=str(sp.id))
            peca = ContentPiece(tenant_id=sp.tenant_id, pauta_id=original.pauta_id, tipo="reels", status="aprovado",
                                versao=1, corpo=corpo)
            db.add(peca)
            await db.flush()
            db.add(ScheduledPost(tenant_id=sp.tenant_id, content_piece_id=peca.id, titulo=titulo, canal="instagram",
                                 formato="trial", data_agendada=sp.data_agendada, horario=hora, status="pronto"))
            criados += 1
            print("teste:", sp.data_agendada, hora, "| normal", sp.horario, "|", sp.titulo)
        print("criados:", criados)
        if simular:
            await db.rollback()
        else:
            await db.commit()


args = sys.argv[1:]
asyncio.run(main("--simular" in args, args[args.index("--hoje-as") + 1] if "--hoje-as" in args else None))
